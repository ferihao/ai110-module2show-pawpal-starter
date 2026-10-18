"""Core backend class skeletons for the PawPal+ pet-care planner."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care activity that may be scheduled for a day."""

    name: str
    category: str
    duration_minutes: int
    priority: str
    recurrence: str = "daily"
    completed: bool = False

    def update_details(self) -> None:
        """Update task details."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def is_due_today(self) -> bool:
        """Return whether this task should be considered today."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    care_needs: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task for this pet."""
        pass


@dataclass
class Owner:
    """A pet owner who can manage pets and request a daily plan."""

    name: str
    available_time_minutes: int
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        pass

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's scheduling preferences."""
        pass

    def request_daily_plan(self) -> list[Task]:
        """Request a daily plan from the scheduler."""
        pass


@dataclass
class Scheduler:
    """Creates a daily care plan from a collection of tasks."""

    available_time_minutes: int
    tasks: list[Task] = field(default_factory=list)

    def sort_tasks(self) -> list[Task]:
        """Sort tasks according to scheduling rules."""
        pass

    def filter_tasks(self) -> list[Task]:
        """Filter tasks that cannot be scheduled today."""
        pass

    def create_daily_plan(self) -> list[Task]:
        """Create a plan that fits within the available time."""
        pass

    def explain_plan(self) -> str:
        """Explain why tasks were included or excluded."""
        pass
