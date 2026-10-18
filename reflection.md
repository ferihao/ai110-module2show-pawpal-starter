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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to brainstorm the UML classes, turn that design into dataclass skeletons, and review the relationships between the classes before implementing them. The most useful prompt was asking how the Scheduler should retrieve tasks from an Owner with multiple pets. It led to the `Owner.get_all_tasks()` method and kept the Scheduler focused on planning rather than storing pet data.

**b. Judgment and verification**

I did not keep the original `CareTask` name because the Python implementation used the simpler `Task` name. I updated the UML and reflection so every artifact used the same name. I also accepted the suggestion to add a due date, but kept it optional to avoid making every recurring daily task require a date. I verified the design by running the terminal demo with two pets and by adding automated tests for task completion and task addition.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
