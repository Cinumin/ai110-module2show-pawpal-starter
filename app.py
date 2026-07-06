import streamlit as st
from pawpal_system import Task, Pet, User, Schedule, sort_by_time
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def _task_rows(tasks):
    """Format tasks into clean, display-friendly table rows."""
    return [
        {
            "Title": t.title,
            "Time": t.start_time or "—",
            "Duration (min)": t.duration,
            "Priority": t.priority.capitalize(),
            "Frequency": t.frequency,
            "Status": "✅ Done" if t.completed else "⬜ Pending",
        }
        for t in tasks
    ]


st.title("🐾 PawPal+")

conflict_banner = st.container()

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=False):
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

    tab_tasks, tab_filter, tab_schedule = st.tabs(["📋 Tasks", "🔍 Filter", "📅 Schedule"])

    with tab_tasks:
        st.caption(f"Add tasks for {selected_pet.name}.")

        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        col4, col5 = st.columns(2)
        with col4:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        with col5:
            start_time_input = st.text_input("Start time (HH:MM, optional)", value="")

        if st.button("Add task"):
            owner.add_task(
                selected_pet,
                Task(
                    title=task_title,
                    duration=duration,
                    priority=priority,
                    frequency=frequency,
                    start_time=start_time_input,
                ),
            )

        if selected_pet.tasks:
            st.success(f"{len(selected_pet.tasks)} task(s) for {selected_pet.name}")
            st.table(_task_rows(selected_pet.tasks))
            for task in selected_pet.tasks:
                if not task.completed and st.button(f"Mark '{task.title}' complete", key=f"complete-{task.id}"):
                    owner.complete_task(selected_pet, task.id)
                    st.rerun()
        else:
            st.info("No tasks yet. Add one above.")

    with tab_filter:
        filter_pet_name = st.selectbox("Pet", ["All pets"] + pet_names, key="filter_pet")
        filter_status = st.selectbox("Status", ["All", "Pending", "Completed"], key="filter_status")

        filter_pet = None if filter_pet_name == "All pets" else next(p for p in owner.pets if p.name == filter_pet_name)
        filter_completed = {"All": None, "Pending": False, "Completed": True}[filter_status]
        filtered = owner.sorted_tasks(pet=filter_pet, completed=filter_completed)

        if filtered:
            st.success(f"Showing {len(filtered)} task(s)")
            st.table(_task_rows(filtered))
        else:
            st.info("No tasks match the selected filters.")

    with tab_schedule:
        st.caption(f"Generate a schedule for {selected_pet.name} based on {owner.name}'s constraints.")
        order_by = st.radio("Order by", ["Priority", "Time"], horizontal=True)

        if st.button("Generate schedule"):
            schedule = Schedule()
            schedule.generate(selected_pet, owner)
            st.session_state.schedule = schedule

        schedule = st.session_state.get("schedule")
        if schedule is not None and schedule.pet is selected_pet:
            if schedule.scheduled_tasks:
                ordered = sort_by_time(schedule.scheduled_tasks) if order_by == "Time" else schedule.scheduled_tasks
                total = sum(t.duration for t in schedule.scheduled_tasks)
                st.success(f"{len(schedule.scheduled_tasks)} task(s) scheduled, {total} minutes total")
                st.table(_task_rows(ordered))
            else:
                st.info(f"No tasks scheduled for {selected_pet.name}.")

            st.markdown("**Scheduling reasoning:**")
            for task in schedule.scheduled_tasks:
                st.write(f"✅ included — '{task.title}' (priority '{task.priority}', {task.duration} min)")
            for task in schedule._skipped_priority:
                st.write(f"⛔ skipped — '{task.title}' priority '{task.priority}' below minimum")
            for task in schedule._skipped_time:
                st.write(f"⏱️ skipped — '{task.title}' not enough time remaining")

    with conflict_banner:
        conflicts = owner.detect_conflicts()
        timed = [t for t in owner.all_tasks() if t.start_time]
        if conflicts:
            st.error(f"⚠️ {len(conflicts)} scheduling conflict(s) detected")
            for task_a, task_b in conflicts:
                st.warning(
                    f"'{task_a.title}' ({task_a.start_time}) overlaps with "
                    f"'{task_b.title}' ({task_b.start_time})"
                )
        elif timed:
            st.success("✅ No scheduling conflicts detected.")
