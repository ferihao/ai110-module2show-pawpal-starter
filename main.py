"""Terminal demonstration of PawPal+'s scheduling algorithms."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print tasks in a compact, readable terminal format."""
    print(f"\n{title}")
    print("-" * len(title))
    for task in tasks:
        print(f"{task.time} — {task.description} ({task.duration_minutes} min)")


def main() -> None:
    """Create a two-pet example and demonstrate each scheduling algorithm."""
    owner = Owner(name="Jordan", available_time_minutes=60)
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")

    # The tasks are deliberately added out of time order; two share 08:00.
    biscuit.add_task(Task("Morning walk", 25, "high", time="08:00"))
    biscuit.add_task(Task("Breakfast", 10, "high", time="07:30"))
    mochi.add_task(Task("Playtime", 15, "medium", time="08:00"))
    mochi.add_task(Task("Brush coat", 20, "low", time="09:30"))
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    scheduler = Scheduler(available_time_minutes=60)
    print_tasks("Tasks sorted by time", scheduler.sort_by_time(owner.get_all_tasks()))

    biscuit_tasks = scheduler.filter_tasks(owner, pet_name="Biscuit", completed=False)
    print_tasks("Incomplete tasks for Biscuit", scheduler.sort_by_time(biscuit_tasks))

    print("\nConflict warnings")
    print("-----------------")
    for warning in scheduler.detect_conflicts(owner):
        print(f"Warning: {warning}")

    schedule = owner.request_daily_plan(scheduler)
    print_tasks("Today's Schedule", scheduler.sort_by_time(schedule))
    print(f"\nWhy this plan: {scheduler.explain_plan(schedule)}")

    recurring_task = Task(
        "Give medication", 5, "high", frequency="daily", time="18:00"
    )
    biscuit.add_task(recurring_task)
    next_task = biscuit.complete_task(recurring_task, today=date(2026, 10, 18))
    print(
        "\nRecurring task: Give medication was completed; "
        f"the next task is due {next_task.due_date}."
    )


if __name__ == "__main__":
    main()
