from dataclasses import dataclass, field
from datetime import date, timedelta
from uuid import uuid4

PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


def _time_to_minutes(t: str) -> int:
    """Convert an "HH:MM" clock time to minutes since midnight."""
    hours, minutes = t.split(":")
    return int(hours) * 60 + int(minutes)


def sort_by_time(tasks: list["Task"]) -> list["Task"]:
    """Sort tasks by start_time, with unscheduled tasks (no start_time) placed last."""
    return sorted(tasks, key=lambda t: (t.start_time == "", t.start_time))


@dataclass #intializes the class with default values and generates special methods like __init__ and __repr__
class Task:
    #name: type is a type annotation
    title: str
    duration: float           # minutes
    priority: str             # "low", "medium", "high"
    # fields with default values
    description: str = ""
    frequency: str = "once"   # "once", "daily", "weekly"
    completed: bool = False
    start_time: str = ""     # "HH:MM" 24-hour, "" means unscheduled
    last_completed_on: date | None = None
    due_date: date | None = None   # calendar date this occurrence becomes due; None = due immediately
    id: str = field(default_factory=lambda: str(uuid4())) # each time a new Task is created, a unique id is generated using uuid4

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
        self.last_completed_on = date.today()

    # -> None is a return type annotation
    def reset(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def is_schedulable(self, min_priority: str) -> bool:
        """Return True if this task's priority meets or exceeds min_priority."""
        return PRIORITY_ORDER[self.priority] >= PRIORITY_ORDER[min_priority]

    def time_range_minutes(self) -> tuple[int, int] | None:
        """Return (start, end) in minutes since midnight, or None if unscheduled."""
        if not self.start_time:
            return None
        start = _time_to_minutes(self.start_time)
        return start, start + self.duration

    def overlaps(self, other: "Task") -> bool:
        """Return True if this task's and other's scheduled time windows intersect."""
        this_range = self.time_range_minutes()
        other_range = other.time_range_minutes()
        if this_range is None or other_range is None:
            return False
        this_start, this_end = this_range
        other_start, other_end = other_range
        return this_start < other_end and other_start < this_end

    def is_due(self, today: date | None = None) -> bool:
        """Return True if this task is not completed and its due date has arrived."""
        if self.completed:
            return False
        today = today or date.today()
        return self.due_date is None or self.due_date <= today

    def next_occurrence(self, today: date | None = None) -> "Task | None":
        """Return a new pending Task for the next occurrence, or None if not recurring."""
        if self.frequency not in ("daily", "weekly"):
            return None
        today = today or date.today()
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(days=7)
        return Task(
            title=self.title,
            duration=self.duration,
            priority=self.priority,
            description=self.description,
            frequency=self.frequency,
            start_time=self.start_time,
            due_date=today + delta,
        )


@dataclass
class Pet:
    name: str
    species: str         # "dog", "cat", "other"
    age: float
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given id from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_task(self, task_id: str) -> Task | None:
        """Return the task with the given id, or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def pending_tasks(self, today: date | None = None) -> list[Task]:
        """Return all tasks that are currently due, accounting for recurrence."""
        today = today or date.today()
        return [t for t in self.tasks if t.is_due(today)]

    def complete_task(self, task_id: str, today: date | None = None) -> Task | None:
        """Mark a task complete and, if recurring, add its next occurrence. Returns the new task, if any."""
        task = self.get_task(task_id)
        if task is None:
            return None
        task.mark_complete()
        next_task = task.next_occurrence(today)
        if next_task is not None:
            self.add_task(next_task)
        return next_task


class User:
    def __init__(self, name: str, time_available: float, min_priority: str):
        self.name: str = name
        self.time_available: float = time_available   # minutes
        self.min_priority: str = min_priority         # "low", "medium", "high"
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this user's list of pets."""
        self.pets.append(pet)

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to the given pet."""
        pet.add_task(task)

    def edit_task(self, pet: Pet, task_id: str, **kwargs) -> None:
        """Update the given pet's task with the provided attribute values."""
        task = pet.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)

    def remove_task(self, pet: Pet, task_id: str) -> None:
        """Remove the task with the given id from the given pet."""
        pet.remove_task(task_id)

    def complete_task(self, pet: Pet, task_id: str) -> Task | None:
        """Mark the given pet's task complete, spawning its next occurrence if recurring."""
        return pet.complete_task(task_id)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this user's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def filter_tasks(self, pet: Pet | None = None, completed: bool | None = None) -> list[Task]:
        """Return tasks across all pets, optionally filtered by pet and/or completion status."""
        tasks = pet.tasks if pet is not None else self.all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def sorted_tasks(self, pet: Pet | None = None, completed: bool | None = None) -> list[Task]:
        """Return filtered tasks sorted by start_time (unscheduled tasks last)."""
        return sort_by_time(self.filter_tasks(pet=pet, completed=completed))

    def detect_conflicts(self, today: date | None = None) -> list[tuple[Task, Task]]:
        """Return pairs of tasks (from any of this user's pets) with overlapping scheduled times."""
        today = today or date.today()
        timed = [t for t in self.all_tasks() if t.start_time and t.is_due(today)]
        conflicts = []
        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                if timed[i].overlaps(timed[j]):
                    conflicts.append((timed[i], timed[j]))
        return conflicts


class Schedule:
    def __init__(self):
        self.pet: Pet | None = None
        self.scheduled_tasks: list[Task] = []
        self._skipped_priority: list[Task] = []
        self._skipped_time: list[Task] = []

    def generate(self, pet: Pet, user: User, today: date | None = None) -> list[Task]:
        """Build a schedule of the pet's pending tasks that fit the user's priority and time constraints."""
        self.pet = pet
        self._skipped_priority = []
        self._skipped_time = []

        eligible = []
        for task in pet.pending_tasks(today):
            if task.is_schedulable(user.min_priority):
                eligible.append(task)
            else:
                self._skipped_priority.append(task)

        eligible.sort(key=lambda task: PRIORITY_ORDER[task.priority], reverse=True)

        scheduled = []
        time_used = 0.0
        for task in eligible:
            if time_used + task.duration <= user.time_available:
                scheduled.append(task)
                time_used += task.duration
            else:
                self._skipped_time.append(task)

        self.scheduled_tasks = scheduled
        return self.scheduled_tasks

    def display(self, sort_by: str = "priority") -> None:
        """Print the current schedule's tasks, ordered by priority (default) or by time."""
        if not self.scheduled_tasks:
            print(f"No tasks scheduled for {self.pet.name}.")
            return
        total = sum(t.duration for t in self.scheduled_tasks)
        print(f"\n--- {self.pet.name}'s Schedule ({len(self.scheduled_tasks)} tasks, {total} min) ---")
        ordered = sort_by_time(self.scheduled_tasks) if sort_by == "time" else self.scheduled_tasks
        for i, task in enumerate(ordered, 1):
            when = f"{task.start_time} — " if task.start_time else ""
            print(f"{i}. [{task.priority.upper()}] {when}{task.title} — {task.duration} min")
            if task.description:
                print(f"   {task.description}")

    def display_reasoning(self) -> None:
        """Print why each task was included in or skipped from the schedule."""
        print("\n--- Scheduling Reasoning ---")
        for task in self.scheduled_tasks:
            print(f"  included : '{task.title}' — priority '{task.priority}', {task.duration} min")
        for task in self._skipped_priority:
            print(f"  skipped  : '{task.title}' — priority '{task.priority}' below minimum")
        for task in self._skipped_time:
            print(f"  skipped  : '{task.title}' — not enough time remaining")
