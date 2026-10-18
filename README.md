# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation Summary

PawPal+ uses four Python classes in [pawpal_system.py](./pawpal_system.py). `Task` stores a care activity and its scheduling details, while `Pet` owns its list of tasks. `Owner` manages multiple pets and combines all of their tasks through `get_all_tasks()`. `Scheduler` reads that combined task list, filters unfinished tasks that are due, prioritizes them, and creates a plan that fits the owner's available time.

## Features

- Multi-pet planning: one owner can manage tasks for any number of pets.
- Time sorting: tasks display in chronological `HH:MM` order.
- Smart daily plans: due, incomplete tasks are prioritized and selected within the available time.
- Conflict warnings: exact-time collisions are highlighted before a schedule is generated.
- Recurring care: completing a daily or weekly task creates the next occurrence automatically.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The terminal demo creates an owner with two pets and generates a prioritized daily plan:

```
Today's Schedule
================
Tasks sorted by time
--------------------
07:30 — Breakfast (10 min)
08:00 — Morning walk (25 min)
08:00 — Playtime (15 min)
09:30 — Brush coat (20 min)

Conflict warnings
-----------------
Warning: Conflict at 08:00: Morning walk for Biscuit; Playtime for Mochi

Today's Schedule
----------------
07:30 — Breakfast (10 min)
08:00 — Morning walk (25 min)
08:00 — Playtime (15 min)

Recurring task: Give medication was completed; the next task is due 2026-10-19.
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The suite verifies task completion, adding tasks to pets, chronological task sorting, daily recurrence, and duplicate-time conflict warnings. Based on these focused tests, the current confidence level is **★★★★☆ (4/5)**; future testing should cover overlapping durations and weekly scheduling.

Successful test output:

```
============================= test session starts ==============================
collected 5 items

tests/test_pawpal.py .....

============================== 5 passed in 0.01s ===============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts zero-padded `HH:MM` times chronologically with a `lambda` key. |
| Filtering | `Scheduler.filter_tasks()` | Returns tasks across all pets and optionally narrows them by pet name, completion state, or whether they are due today. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns a warning when two or more unfinished tasks share the exact same time. |
| Recurring tasks | `Pet.complete_task()` and `Task.create_next_occurrence()` | Completes the current task and adds a daily or weekly copy with the next due date. |

## Demo Walkthrough

1. Enter the owner name and the amount of time available today.
2. Add one or more pets, including optional care notes.
3. Add a task to a pet with a time, duration, priority, and frequency. The current-task table stays sorted by time.
4. If two unfinished tasks use the same time, PawPal+ shows a warning that identifies both tasks and suggests moving one of them.
5. Select **Generate schedule** to see due tasks chosen by priority within the available time; the displayed plan is sorted chronologically for readability.

The terminal demonstration in [main.py](./main.py) exercises the same behavior:

```
Tasks sorted by time
--------------------
07:30 — Breakfast (10 min)
08:00 — Morning walk (25 min)
08:00 — Playtime (15 min)

Warning: Conflict at 08:00: Morning walk for Biscuit; Playtime for Mochi
Recurring task: Give medication was completed; the next task is due 2026-10-19.
```
