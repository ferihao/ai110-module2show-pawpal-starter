"""Core backend models and scheduling logic for the PawPal+ planner."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """A single activity needed to care for a pet."""

    description: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily"
    due_date: date | None = None
    completed: bool = False

    def update_details(
        self,
        description: str | None = None,
        duration_minutes: int | None = None,
        priority: str | None = None,
        frequency: str | None = None,
        due_date: date | None = None,
    ) -> None:
        """Update only the details supplied by the caller."""
        if description is not None:
            self.description = description
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if due_date is not None:
            self.due_date = due_date

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def is_due_today(self, today: date | None = None) -> bool:
        """Return whether an unfinished task should be scheduled today."""
        if self.completed:
            return False

        current_day = today or date.today()
        if self.due_date is not None:
            return self.due_date == current_day

        return self.frequency.lower() == "daily"


@dataclass
class Pet:
    """A pet and its collection of care tasks."""

    name: str
    species: str
    care_needs: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task if it belongs to this pet."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    """A pet owner who manages pets and their care plan."""

    name: str
    available_time_minutes: int
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        self.pets.append(pet)

    def update_preferences(self, preferences: str) -> None:
        """Replace the owner's scheduling preferences."""
        self.preferences = preferences

    def get_all_tasks(self) -> list[Task]:
        """Return every task from every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.tasks]

    def request_daily_plan(
        self, scheduler: "Scheduler", today: date | None = None
    ) -> list[Task]:
        """Ask a scheduler to create this owner's plan for a day."""
        return scheduler.create_daily_plan(self, today)


@dataclass
class Scheduler:
    """Builds a prioritized daily plan from all of an owner's pets' tasks."""

    available_time_minutes: int

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order high-priority, shorter tasks first."""
        return sorted(
            tasks,
            key=lambda task: (
                self.PRIORITY_ORDER.get(task.priority.lower(), 3),
                task.duration_minutes,
            ),
        )

    def filter_tasks(self, tasks: list[Task], today: date | None = None) -> list[Task]:
        """Keep only tasks that are due and can fit in a daily plan."""
        return [
            task
            for task in tasks
            if task.duration_minutes > 0 and task.is_due_today(today)
        ]

    def create_daily_plan(
        self, owner: Owner, today: date | None = None
    ) -> list[Task]:
        """Select due tasks across all of an owner's pets within the time limit."""
        all_owner_tasks = owner.get_all_tasks()
        due_tasks = self.filter_tasks(all_owner_tasks, today)
        ordered_tasks = self.sort_tasks(due_tasks)

        plan: list[Task] = []
        remaining_time = min(self.available_time_minutes, owner.available_time_minutes)
        for task in ordered_tasks:
            if task.duration_minutes <= remaining_time:
                plan.append(task)
                remaining_time -= task.duration_minutes

        return plan

    def explain_plan(self, plan: list[Task]) -> str:
        """Explain the rule used to order and select the supplied plan."""
        if not plan:
            return "No due tasks fit within the available time."

        total_minutes = sum(task.duration_minutes for task in plan)
        task_descriptions = ", ".join(task.description for task in plan)
        return (
            f"Scheduled {task_descriptions} because these due tasks have the highest "
            f"priority and fit within the available time ({total_minutes} minutes)."
        )
