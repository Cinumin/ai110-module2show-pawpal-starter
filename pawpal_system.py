from dataclasses import dataclass, field
from uuid import uuid4

PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Task:
    title: str
    duration: float      # minutes
    priority: str        # "low", "medium", "high"
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Pet:
    name: str
    species: str         # "dog", "cat", "other"
    age: float
    tasks: list[Task] = field(default_factory=list)


class User:
    def __init__(self, name: str, time_available: float, min_priority: str):
        self.name: str = name
        self.time_available: float = time_available   # minutes
        self.min_priority: str = min_priority         # "low", "medium", "high"
        self.pets: list[Pet] = []

    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def edit_task(self, pet: Pet, task_id: str, **kwargs) -> None:
        pass

    def remove_task(self, pet: Pet, task_id: str) -> None:
        pass


class Schedule:
    def __init__(self):
        self.scheduled_tasks: list[Task] = []

    def generate(self, pet: Pet, user: User) -> list[Task]:
        pass

    def display(self) -> None:
        pass

    def display_reasoning(self) -> None:
        pass
