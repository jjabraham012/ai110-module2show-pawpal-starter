from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0

    def edit_pet(self, **kwargs) -> None:
        """Update pet attributes."""
        pass

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


@dataclass
class Task:
    title: str
    category: str  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    pet: Pet
    priority: str = "medium"  # "low", "medium", "high"
    duration_minutes: int = 30
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def edit_task(self, **kwargs) -> None:
        """Update task attributes."""
        pass

    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.title} for {self.pet.name} ({self.duration_minutes}min)"


@dataclass
class Schedule:
    date: date
    available_minutes: int = 120
    planned_tasks: List[Task] = field(default_factory=list)

    def generate_daily_plan(self, tasks: List[Task]) -> List[Task]:
        """Pick and order tasks that fit within available time."""
        pass

    def add_task_to_day(self, task: Task) -> bool:
        """Add a task if there is enough time remaining. Returns True on success."""
        pass

    def remove_task_from_day(self, task: Task) -> None:
        """Remove a task from the day's plan."""
        pass

    def get_time_remaining(self) -> int:
        """Return unused minutes in the schedule."""
        pass


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []
        self.preferences: List[str] = []
        self.schedule: Optional[Schedule] = None

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet and its associated tasks."""
        pass

    def set_preferences(self, preferences: List[str]) -> None:
        """Update owner care preferences."""
        pass

    def view_daily_plan(self) -> List[Task]:
        """Return today's planned tasks."""
        pass