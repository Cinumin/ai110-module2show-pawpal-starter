from dataclasses import dataclass, field
from uuid import uuid4

PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


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
    id: str = field(default_factory=lambda: str(uuid4())) # each time a new Task is created, a unique id is generated using uuid4

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    # -> None is a return type annotation
    def reset(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def is_schedulable(self, min_priority: str) -> bool:
        """Return True if this task's priority meets or exceeds min_priority."""
        return PRIORITY_ORDER[self.priority] >= PRIORITY_ORDER[min_priority]


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

    def pending_tasks(self) -> list[Task]:
        """Return all tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


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

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this user's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Schedule:
    def __init__(self):
        self.pet: Pet | None = None
        self.scheduled_tasks: list[Task] = []
        self._skipped_priority: list[Task] = []
        self._skipped_time: list[Task] = []

    def generate(self, pet: Pet, user: User) -> list[Task]:
        """Build a schedule of the pet's pending tasks that fit the user's priority and time constraints."""
        self.pet = pet
        self._skipped_priority = []
        self._skipped_time = []

        eligible = []
        for task in pet.pending_tasks():
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

    def display(self) -> None:
        """Print the current schedule's tasks."""
        if not self.scheduled_tasks:
            print(f"No tasks scheduled for {self.pet.name}.")
            return
        total = sum(t.duration for t in self.scheduled_tasks)
        print(f"\n--- {self.pet.name}'s Schedule ({len(self.scheduled_tasks)} tasks, {total} min) ---")
        for i, task in enumerate(self.scheduled_tasks, 1):
            print(f"{i}. [{task.priority.upper()}] {task.title} — {task.duration} min")
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
