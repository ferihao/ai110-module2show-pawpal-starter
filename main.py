"""Temporary terminal demo for the PawPal+ scheduling logic."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create a two-pet example and print its daily care plan."""
    owner = Owner(name="Jordan", available_time_minutes=60)

    biscuit = Pet(name="Biscuit", species="dog")
    biscuit.add_task(Task("Morning walk", duration_minutes=25, priority="high"))
    biscuit.add_task(Task("Breakfast", duration_minutes=10, priority="high"))

    mochi = Pet(name="Mochi", species="cat")
    mochi.add_task(Task("Playtime", duration_minutes=15, priority="medium"))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    scheduler = Scheduler(available_time_minutes=60)
    schedule = owner.request_daily_plan(scheduler)
    pet_names = {
        id(task): pet.name
        for pet in owner.pets
        for task in pet.tasks
    }

    print("Today's Schedule")
    print("=" * 16)
    for number, task in enumerate(schedule, start=1):
        print(
            f"{number}. {task.description} for {pet_names[id(task)]} "
            f"— {task.duration_minutes} min ({task.priority} priority)"
        )

    total_minutes = sum(task.duration_minutes for task in schedule)
    print(f"\nTotal scheduled time: {total_minutes} minutes")
    print(f"Why this plan: {scheduler.explain_plan(schedule)}")


if __name__ == "__main__":
    main()
