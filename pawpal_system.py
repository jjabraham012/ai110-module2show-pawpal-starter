from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional, Tuple


def _parse_time(time_str: str) -> Tuple[int, int]:
    """Convert a time string like '7:00 AM' into (hour24, minute) for sorting."""
    time_str = time_str.strip().upper()
    parts = time_str.replace("AM", "").replace("PM", "").strip().split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    if "PM" in time_str and hour != 12:
        hour += 12
    if "AM" in time_str and hour == 12:
        hour = 0
    return (hour, minute)


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    category: str
    time: str
    priority: str = "medium"
    frequency: str = "daily"
    duration_minutes: int = 30
    completed: bool = False
    due_date: Optional[date] = None

    def __post_init__(self):
        if self.due_date is None:
            self.due_date = date.today()

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as done and return a new Task for the next occurrence if recurring."""
        self.completed = True
        if self.frequency == "daily":
            next_task = Task(
                description=self.description,
                category=self.category,
                time=self.time,
                priority=self.priority,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                due_date=self.due_date + timedelta(days=1),
            )
            return next_task
        elif self.frequency == "weekly":
            next_task = Task(
                description=self.description,
                category=self.category,
                time=self.time,
                priority=self.priority,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                due_date=self.due_date + timedelta(weeks=1),
            )
            return next_task
        return None

    def mark_incomplete(self) -> None:
        """Reset this task to not done."""
        self.completed = False

    def edit_task(self, **kwargs) -> None:
        """Update any task attribute by keyword."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self) -> str:
        """Return a formatted string showing task status and details."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.time} - {self.description} ({self.category}, {self.priority} priority, {self.duration_minutes}min, {self.frequency})"


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Return all tasks matching a category."""
        return [t for t in self.tasks if t.category == category]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def edit_pet(self, **kwargs) -> None:
        """Update pet attributes by keyword."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "tasks":
                setattr(self, key, value)

    def __str__(self) -> str:
        """Return a formatted string with pet name and details."""
        return f"{self.name} ({self.species}, {self.breed}, age {self.age})"


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str) -> None:
        """Initialize owner with a name and empty pet list."""
        self.name: str = name
        self.pets: List[Pet] = []
        self.preferences: List[str] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Gather every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def find_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Return the pet that owns a given task."""
        for pet in self.pets:
            if task in pet.tasks:
                return pet
        return None

    def set_preferences(self, preferences: List[str]) -> None:
        """Update owner care preferences."""
        self.preferences = preferences

    def __str__(self) -> str:
        """Return owner name and list of pet names."""
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "none"
        return f"{self.name} (pets: {pet_names})"


class Scheduler:
    """The brain that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner, available_minutes: int = 120) -> None:
        """Initialize scheduler with an owner and time budget."""
        self.owner: Owner = owner
        self.available_minutes: int = available_minutes
        self.daily_plan: List[Task] = []

    def get_all_tasks(self) -> List[Task]:
        """Pull every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def generate_daily_plan(self) -> List[Task]:
        """Build a priority-sorted daily plan that fits within available time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks = self.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order.get(t.priority, 1))

        self.daily_plan = []
        time_used = 0

        for task in sorted_tasks:
            if not task.completed and time_used + task.duration_minutes <= self.available_minutes:
                self.daily_plan.append(task)
                time_used += task.duration_minutes

        return self.daily_plan

    def sort_by_time(self) -> List[Task]:
        """Sort the daily plan by task time in chronological order."""
        self.daily_plan = sorted(self.daily_plan, key=lambda t: _parse_time(t.time))
        return self.daily_plan

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return only tasks belonging to a specific pet."""
        results = []
        for task in self.daily_plan:
            pet = self.owner.find_pet_for_task(task)
            if pet and pet.name == pet_name:
                results.append(task)
        return results

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.daily_plan if t.completed == completed]

    def detect_conflicts(self) -> List[str]:
        """Find tasks scheduled at the same time and return warning messages."""
        time_map = {}
        for task in self.daily_plan:
            if task.time not in time_map:
                time_map[task.time] = []
            time_map[task.time].append(task)

        warnings = []
        for time_slot, tasks in time_map.items():
            if len(tasks) > 1:
                names = ", ".join(f"'{t.description}'" for t in tasks)
                warnings.append(f"⚠️  Conflict at {time_slot}: {names} are scheduled at the same time.")
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and auto-schedule the next occurrence if recurring."""
        pet = self.owner.find_pet_for_task(task)
        next_task = task.mark_complete()
        if next_task and pet:
            pet.add_task(next_task)
            return next_task
        return None

    def get_time_remaining(self) -> int:
        """Return unused minutes after planning."""
        used = sum(t.duration_minutes for t in self.daily_plan)
        return self.available_minutes - used

    def add_task_to_plan(self, task: Task) -> bool:
        """Manually add a task if time allows."""
        if task.duration_minutes <= self.get_time_remaining():
            self.daily_plan.append(task)
            return True
        return False

    def remove_task_from_plan(self, task: Task) -> None:
        """Remove a task from the daily plan."""
        if task in self.daily_plan:
            self.daily_plan.remove(task)

    def get_plan_summary(self) -> str:
        """Return a formatted string of today's full schedule."""
        if not self.daily_plan:
            return "No tasks planned for today."

        lines = [f"📋 Today's Schedule for {self.owner.name}"]
        lines.append(f"   Available time: {self.available_minutes} min\n")

        for i, task in enumerate(self.daily_plan, 1):
            pet = self.owner.find_pet_for_task(task)
            pet_name = pet.name if pet else "?"
            lines.append(f"  {i}. {task.time} — {task.description}")
            lines.append(f"     Pet: {pet_name} | {task.category} | {task.priority} priority | {task.duration_minutes} min")

        used = sum(t.duration_minutes for t in self.daily_plan)
        lines.append(f"\n   Total: {used} min used, {self.get_time_remaining()} min remaining")
        return "\n".join(lines)