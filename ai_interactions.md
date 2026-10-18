# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the VS Code AI coding agent(Codex) to build PawPal+ in small phases: create the dataclass-based logic layer, connect it to Streamlit
**What did the agent do?**

It created Mermaid diagrams and reported diagnostics

**What did you have to verify or fix manually?**

I reviewed the generated class relationships and kept the design to four core classes instead of adding unnecessary objects. I also checked that the Scheduler used `Owner.get_all_tasks()` rather than a single pet, that one-time tasks could actually appear in a plan, and that the exact-time conflict warning was intentionally a lightweight first version. The agent could not confirm GitHub repository visibility because the GitHub CLI was unavailable, so that setting still requires a manual check in GitHub.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | VS Code AI coding agent | VS Code AI coding agent(Codex) |
| **Prompt** | “Based on my skeletons in `pawpal_system.py`, how should the `Scheduler` retrieve all tasks from the `Owner`'s pets?” | “Implement `Owner.get_all_tasks()` and make `Scheduler.create_daily_plan(owner)` use it for a multi-pet plan.” |
| **Response summary** | Suggested giving `Owner` an aggregation method so the Scheduler does not need to navigate individual pets. | Produced the concrete method relationship and updated the scheduling flow to use it. |
| **What was useful** | Helped identify the correct boundary between data ownership and planning logic. | Turned the chosen design into a focused implementation quickly. |
| **Problems noticed** | It was conceptual, so it did not by itself confirm method names, types, or tests. | A direct implementation request can hide design tradeoffs if I accept it without reviewing the result. |
| **Decision** | Used as the design step. | Used after reviewing the design; this became the final implementation. |

**Which approach did you use in your final implementation and why?**

I used the two approaches in sequence: first the open-ended design prompt, then the specific implementation prompt. The first kept the multi-pet relationship clean; the second made the code efficient to implement. I verified the final choice with a two-pet CLI demo and tests for sorting, recurrence, and conflict detection.
