from pawpal_system import Pet, Task


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
