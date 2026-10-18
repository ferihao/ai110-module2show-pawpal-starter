"""Tests for PawPal+ task, recurrence, and scheduling behavior."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    """A task becomes complete when mark_complete is called."""
    task = Task(description="Give medication", duration_minutes=5)

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Adding a task stores it on the pet."""
    pet = Pet(name="Biscuit", species="dog")
    task = Task(description="Morning walk", duration_minutes=25)

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    """Tasks with HH:MM times are returned from earliest to latest."""
    scheduler = Scheduler(available_time_minutes=60)
    tasks = [
        Task("Dinner", 10, time="18:00"),
        Task("Morning walk", 25, time="08:00"),
        Task("Lunch", 10, time="12:30"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["08:00", "12:30", "18:00"]


def test_completing_daily_task_creates_next_day_occurrence() -> None:
    """Completing a daily task adds an unfinished copy due tomorrow."""
    today = date(2026, 10, 18)
    pet = Pet(name="Biscuit", species="dog")
    task = Task("Give medication", 5, frequency="daily", due_date=today)
    pet.add_task(task)

    next_task = pet.complete_task(task, today=today)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == today + timedelta(days=1)
    assert len(pet.tasks) == 2


def test_detect_conflicts_flags_duplicate_task_times() -> None:
    """Tasks assigned to the same time produce a conflict warning."""
    owner = Owner(name="Jordan", available_time_minutes=60)
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    biscuit.add_task(Task("Morning walk", 25, time="08:00"))
    mochi.add_task(Task("Playtime", 15, time="08:00"))
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    warnings = Scheduler(available_time_minutes=60).detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Conflict at 08:00" in warnings[0]
