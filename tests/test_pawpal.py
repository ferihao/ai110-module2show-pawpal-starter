"""Tests for basic PawPal+ task and pet behavior."""

from pawpal_system import Pet, Task


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
