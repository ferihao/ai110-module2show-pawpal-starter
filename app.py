"""Streamlit interface for the PawPal+ pet-care planner."""

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Build a practical care plan for all of your pets.")

st.subheader("Owner details")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time today (minutes)", min_value=1, max_value=480, value=60
)

# Session state keeps this object alive when Streamlit reruns the script.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name, available_time_minutes=int(available_time)
    )

owner = st.session_state.owner
owner.name = owner_name
owner.available_time_minutes = int(available_time)
scheduler = Scheduler(available_time_minutes=owner.available_time_minutes)

st.divider()
st.subheader("Add a pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    care_needs = st.text_input("Care needs (optional)")
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if pet_name.strip():
        owner.add_pet(Pet(pet_name.strip(), species, care_needs.strip()))
        st.success(f"Added {pet_name.strip()}.")
    else:
        st.error("Enter a pet name before adding it.")

if owner.pets:
    st.markdown("**Your pets:** " + ", ".join(pet.name for pet in owner.pets))
else:
    st.info("Add a pet to start creating care tasks.")

st.divider()
st.subheader("Add a care task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
        description = st.text_input("Task description")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        task_time = st.text_input("Scheduled time (HH:MM)", value="09:00")
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["daily", "once", "weekly"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        if description.strip():
            selected_pet = next(
                pet for pet in owner.pets if pet.name == selected_pet_name
            )
            selected_pet.add_task(
                Task(
                    description=description.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                    time=task_time,
                )
            )
            st.success(f"Added {description.strip()} for {selected_pet.name}.")
        else:
            st.error("Enter a task description before adding it.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        pet_names = {
            id(task): pet.name for pet in owner.pets for task in pet.tasks
        }
        st.markdown("**Current tasks (sorted by time)**")
        st.dataframe(
            [
                {
                    "Pet": pet_names[id(task)],
                    "Task": task.description,
                    "Time": task.time,
                    "Minutes": task.duration_minutes,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Complete": task.completed,
                }
                for task in scheduler.sort_by_time(all_tasks)
            ],
            use_container_width=True,
            hide_index=True,
        )

        conflicts = scheduler.detect_conflicts(owner)
        if conflicts:
            st.markdown("**Scheduling conflicts**")
            for warning in conflicts:
                st.warning(f"{warning}. Move one task to another time.")

st.divider()
st.subheader("Today's Schedule")
if st.button("Generate schedule", disabled=not owner.pets):
    plan = owner.request_daily_plan(scheduler)

    if plan:
        pet_names = {
            id(task): pet.name for pet in owner.pets for task in pet.tasks
        }
        for position, task in enumerate(scheduler.sort_by_time(plan), start=1):
            st.write(
                f"{position}. **{task.description}** for {pet_names[id(task)]} "
                f"— {task.duration_minutes} minutes ({task.priority} priority)"
            )
        st.caption(scheduler.explain_plan(plan))
    else:
        st.info("No due tasks fit within the available time.")
