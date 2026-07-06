from datetime import date, timedelta

from pawpal_system import Pet, Task, User


def test_mark_complete_changes_task_status():
    task = Task(title="Feed", duration=10, priority="medium")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="dog", age=3)
    assert len(pet.tasks) == 0

    task = Task(title="Walk", duration=15, priority="high")
    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_is_due_for_once_task_matches_completed_flag():
    task = Task(title="Vet visit", duration=30, priority="high", frequency="once")
    assert task.is_due() is True

    task.mark_complete()

    assert task.is_due() is False


def test_is_due_respects_due_date():
    today = date(2026, 7, 5)
    task = Task(title="Feed", duration=10, priority="medium", due_date=today + timedelta(days=1))

    assert task.is_due(today) is False
    assert task.is_due(today + timedelta(days=1)) is True


def test_is_due_true_when_no_due_date():
    task = Task(title="Playtime", duration=20, priority="low")

    assert task.is_due() is True


def test_is_due_false_when_completed_regardless_of_due_date():
    today = date(2026, 7, 5)
    task = Task(title="Feed", duration=10, priority="medium", due_date=today)
    task.mark_complete()

    assert task.is_due(today) is False


def test_next_occurrence_none_for_once_task():
    task = Task(title="Vet visit", duration=30, priority="high", frequency="once")

    assert task.next_occurrence() is None


def test_next_occurrence_daily_due_tomorrow():
    today = date(2026, 7, 5)
    task = Task(title="Feed", duration=10, priority="medium", frequency="daily")

    next_task = task.next_occurrence(today)

    assert next_task is not None
    assert next_task.id != task.id
    assert next_task.completed is False
    assert next_task.due_date == today + timedelta(days=1)


def test_next_occurrence_weekly_due_in_seven_days():
    today = date(2026, 7, 5)
    task = Task(title="Grooming", duration=20, priority="low", frequency="weekly")

    next_task = task.next_occurrence(today)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_complete_task_spawns_next_occurrence_for_daily_task():
    today = date(2026, 7, 5)
    pet = Pet(name="Rex", species="dog", age=3)
    task = Task(title="Feed", duration=10, priority="medium", frequency="daily")
    pet.add_task(task)

    spawned = pet.complete_task(task.id, today)

    assert task.completed is True
    assert spawned is not None
    assert spawned.due_date == today + timedelta(days=1)
    assert len(pet.tasks) == 2


def test_complete_task_does_not_spawn_for_once_task():
    pet = Pet(name="Rex", species="dog", age=3)
    task = Task(title="Vet visit", duration=30, priority="high", frequency="once")
    pet.add_task(task)

    spawned = pet.complete_task(task.id)

    assert task.completed is True
    assert spawned is None
    assert len(pet.tasks) == 1


def test_overlaps_detects_intersecting_time_windows():
    walk = Task(title="Walk", duration=30, priority="high", start_time="07:00")
    vet = Task(title="Vet", duration=30, priority="high", start_time="07:15")
    nap = Task(title="Nap", duration=30, priority="low", start_time="08:00")

    assert walk.overlaps(vet) is True
    assert walk.overlaps(nap) is False


def test_overlaps_ignores_unscheduled_tasks():
    walk = Task(title="Walk", duration=30, priority="high", start_time="07:00")
    playtime = Task(title="Playtime", duration=20, priority="low")

    assert walk.overlaps(playtime) is False


def test_detect_conflicts_across_pets():
    owner = User(name="Alice", time_available=120, min_priority="low")
    dog = Pet(name="Buddy", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    owner.add_task(dog, Task(title="Walk", duration=30, priority="high", start_time="07:00"))
    owner.add_task(cat, Task(title="Grooming", duration=30, priority="high", start_time="07:15"))
    owner.add_task(cat, Task(title="Nap", duration=30, priority="low", start_time="08:00"))

    conflicts = owner.detect_conflicts()

    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Walk", "Grooming"}


def test_detect_conflicts_ignores_not_yet_due_tasks():
    today = date(2026, 7, 5)
    owner = User(name="Alice", time_available=120, min_priority="low")
    dog = Pet(name="Buddy", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    owner.add_task(dog, Task(title="Walk", duration=30, priority="high", start_time="07:00"))
    owner.add_task(
        cat,
        Task(
            title="Grooming",
            duration=30,
            priority="high",
            start_time="07:15",
            due_date=today + timedelta(days=1),
        ),
    )

    conflicts = owner.detect_conflicts(today)

    assert conflicts == []


def test_filter_tasks_by_pet_and_status():
    owner = User(name="Alice", time_available=120, min_priority="low")
    dog = Pet(name="Buddy", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task(title="Walk", duration=30, priority="high")
    walk.mark_complete()
    owner.add_task(dog, walk)
    owner.add_task(cat, Task(title="Nap", duration=30, priority="low"))

    assert owner.filter_tasks(pet=dog) == [walk]
    assert owner.filter_tasks(completed=True) == [walk]
    assert len(owner.filter_tasks(completed=False)) == 1


def test_sorted_tasks_returns_chronological_order():
    owner = User(name="Alice", time_available=120, min_priority="low")
    pet = Pet(name="Buddy", species="dog", age=3)
    owner.add_pet(pet)

    noon = Task(title="Lunch", duration=15, priority="medium", start_time="12:00")
    morning = Task(title="Walk", duration=30, priority="high", start_time="07:00")
    evening = Task(title="Dinner", duration=15, priority="medium", start_time="18:30")
    owner.add_task(pet, noon)
    owner.add_task(pet, morning)
    owner.add_task(pet, evening)

    ordered = owner.sorted_tasks()

    assert ordered == [morning, noon, evening]


def test_completing_daily_task_creates_pending_task_for_next_day():
    today = date(2026, 7, 5)
    pet = Pet(name="Rex", species="dog", age=3)
    task = Task(title="Feed", duration=10, priority="medium", frequency="daily", start_time="08:00")
    pet.add_task(task)

    new_task = pet.complete_task(task.id, today)

    assert new_task is not None
    assert new_task in pet.tasks
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.is_due(today) is False
    assert new_task.is_due(today + timedelta(days=1)) is True


def test_detect_conflicts_flags_duplicate_start_times():
    owner = User(name="Alice", time_available=120, min_priority="low")
    dog = Pet(name="Buddy", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    owner.add_task(dog, Task(title="Walk", duration=20, priority="high", start_time="09:00"))
    owner.add_task(cat, Task(title="Feed", duration=20, priority="medium", start_time="09:00"))

    conflicts = owner.detect_conflicts()

    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Walk", "Feed"}


def test_sorted_tasks_places_unscheduled_tasks_last():
    owner = User(name="Alice", time_available=120, min_priority="low")
    pet = Pet(name="Buddy", species="dog", age=3)
    owner.add_pet(pet)

    unscheduled = Task(title="Playtime", duration=20, priority="low")
    later = Task(title="Nap", duration=30, priority="low", start_time="14:00")
    earlier = Task(title="Walk", duration=30, priority="high", start_time="07:00")
    owner.add_task(pet, unscheduled)
    owner.add_task(pet, later)
    owner.add_task(pet, earlier)

    ordered = owner.sorted_tasks()

    assert ordered == [earlier, later, unscheduled]
