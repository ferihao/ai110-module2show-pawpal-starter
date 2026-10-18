# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial design centers on three core user actions:

- A pet owner can add their pet's basic information, such as the pet's name and care needs, so the app can personalize the plan.
- A pet owner can create and update care tasks—for example, walks, meals, medication, or grooming—and give each task a duration and priority.
- A pet owner can view a generated plan for today that fits the available time, highlights the most important tasks, and explains why those tasks were selected.

The initial UML design would use these main objects:

- **Owner** holds the owner's name, available time, and preferences. It can add pets, update preferences, and request a daily plan.
- **Pet** holds a pet's name, species, and care needs. It can keep track of its care tasks and add or remove a task.
- **Task** holds a description, duration, priority, frequency, optional due date, and completion status. It can be edited, marked complete, and checked for whether it is due today.
- **Scheduler** holds the available time. It gets every task from the Owner, then sorts and filters them, creates a schedule that fits the time available, and explains why tasks were included or left out.

**b. Design changes**

After reviewing the first skeleton, I made two small design changes. First, I renamed the UML class from `CareTask` to `Task` so the diagram, reflection, and Python code use the same name. Second, I added an optional due date to `Task`, because recurrence alone cannot represent one-time or date-specific care such as a vet medication. I also made `Owner.request_daily_plan` accept a `Scheduler`; this makes the relationship explicit and avoids making the Owner class responsible for scheduling logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers whether a task is unfinished and due, each task's priority, its duration, and both the owner's and scheduler's available time. It first orders tasks from high to low priority, using shorter duration as a tie-breaker, then adds only tasks that fit in the remaining time. Time availability and task priority mattered most because they directly answer the owner's need to complete the most important care within a limited day.

**b. Tradeoffs**

The scheduler uses a lightweight conflict check: it warns only when unfinished tasks have exactly the same `HH:MM` time. It does not yet calculate whether a 30-minute task at 08:00 overlaps a task at 08:15. This keeps the first version easy to read and explain while still catching the most obvious conflict; overlap detection can be added later if the app needs more precise time planning.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI for design brainstorming, class scaffolding, algorithm suggestions, documentation, and test drafting. The most effective features were targeted code review and automatic editing: reviewing the class relationships led to `Owner.get_all_tasks()`, and focused prompts helped turn the requirements into small methods such as `sort_by_time()` and `detect_conflicts()`. I treated each project phase as a separate, focused work context; that kept planning, implementation, testing, and documentation prompts from becoming mixed together.

**b. Judgment and verification**

I rejected the more complicated idea of calculating every possible overlapping duration immediately. Instead, I kept conflict detection to exact `HH:MM` matches because its warning is easy for a pet owner to understand and the method stays small. I also renamed `CareTask` to `Task` so the diagram and code used a single, clean vocabulary. I verified these choices by running the multi-pet CLI demo and by testing completion, recurrence, sorting, and conflict warnings.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding a task to a pet, chronological sorting by time, daily recurrence, and duplicate-time conflict detection. These checks cover the core actions that change data and the scheduler algorithms most likely to produce an incorrect plan.

**b. Confidence**

I am 4 out of 5 confident in the current scheduler because the core behaviors pass automated tests and the multi-pet demo runs successfully. Next, I would test overlapping task durations, malformed time strings, weekly recurrence on different days, and plans where no task fits in the available time.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the way the four classes work together without duplicating responsibilities: Pets own tasks, Owners aggregate them, and the Scheduler makes planning decisions. That separation made it straightforward to use the same logic in both the terminal demo and Streamlit UI.

**b. What you would improve**

In another iteration, I would validate time input more carefully, detect overlapping durations rather than only identical times, and let the user mark tasks complete directly in the UI. I would also add persistent storage so pets and tasks survive beyond one Streamlit session.

**c. Key takeaway**

I learned that I am the lead architect even when AI writes much of the first draft. AI was strongest at proposing options and speeding up routine code, but I needed to choose the scope, keep the class relationships simple, check that the UML matched the code, and verify behavior with real tests and demos.
