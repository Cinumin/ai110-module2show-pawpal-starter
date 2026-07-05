from dataclasses import asdict

import streamlit as st
from pawpal_system import Task, Pet, User, Schedule
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
time_available = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=600, value=120
)
min_priority = st.selectbox("Minimum task priority to schedule", ["low", "medium", "high"], index=0)

if "owner" not in st.session_state:
    st.session_state.owner = User(name=owner_name, time_available=time_available, min_priority=min_priority)
owner = st.session_state.owner
owner.name = owner_name
owner.time_available = time_available
owner.min_priority = min_priority

st.divider()

st.subheader("Pets")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Pet age", min_value=0.0, value=1.0)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, age=pet_age))

if owner.pets:
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

if owner.pets:
    st.divider()

    pet_names = [p.name for p in owner.pets]
    selected_name = st.selectbox("Active pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_name)

    st.markdown("### Tasks")
    st.caption(f"Add tasks for {selected_pet.name}.")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        owner.add_task(selected_pet, Task(title=task_title, duration=duration, priority=priority))

    if selected_pet.tasks:
        st.write(f"Current tasks for {selected_pet.name}:")
        st.table([asdict(t) for t in selected_pet.tasks])
    else:
        st.info("No tasks yet. Add one above.")

    st.divider()

    st.subheader("Build Schedule")
    st.caption(f"Generate a schedule for {selected_pet.name} based on {owner.name}'s constraints.")

    if st.button("Generate schedule"):
        schedule = Schedule()
        schedule.generate(selected_pet, owner)

        if schedule.scheduled_tasks:
            total = sum(t.duration for t in schedule.scheduled_tasks)
            st.write(f"{len(schedule.scheduled_tasks)} tasks scheduled, {total} minutes total:")
            st.table([asdict(t) for t in schedule.scheduled_tasks])
        else:
            st.info(f"No tasks scheduled for {selected_pet.name}.")

        st.markdown("**Scheduling reasoning:**")
        for task in schedule.scheduled_tasks:
            st.write(f"✅ included — '{task.title}' (priority '{task.priority}', {task.duration} min)")
        for task in schedule._skipped_priority:
            st.write(f"⛔ skipped — '{task.title}' priority '{task.priority}' below minimum")
        for task in schedule._skipped_time:
            st.write(f"⏱️ skipped — '{task.title}' not enough time remaining")
