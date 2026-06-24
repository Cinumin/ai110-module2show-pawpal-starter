from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration: float       # minutes
    priority: str         # "low", "medium", "high"


@dataclass
class Pet:
    name: str
    species: str          # "dog", "cat", "other"


@dataclass
class Preferences:
    time_available: float # total minutes available
    min_priority: str     # minimum priority to include ("low", "medium", "high")


class User:
    def __init__(self, name: str, pet: Pet):
        self.name: str = name
        self.pet: Pet = pet
        self.tasks: list[Task] = []
        self.preferences: Preferences = None

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, title: str, **kwargs) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass


class Schedule:
    def __init__(self):
        self.scheduled_tasks: list[Task] = []

    def generate(self, tasks: list[Task], preferences: Preferences) -> None:
        pass

    def display(self) -> None:
        pass
