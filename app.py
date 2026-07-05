import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, your pet care planning assistant.
Add your pets, create care tasks, and generate a daily schedule based on priority and available time.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.divider()

st.subheader("Owner & Pets")

owner.name = st.text_input("Owner name", value=owner.name)

with st.form("add_pet_form"):
    st.markdown("**Add a new pet**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pet_name = st.text_input("Name")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Fish", "Rabbit", "Other"])
    with col3:
        breed = st.text_input("Breed")
    with col4:
        age = st.number_input("Age", min_value=0, max_value=30, value=1)
    add_pet = st.form_submit_button("Add Pet")

if add_pet and pet_name:
    owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=age))
    st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("**Your pets:**")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.breed}, age {pet.age}) — {len(pet.tasks)} tasks")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add care tasks for your pets. These feed into the scheduler.")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    with st.form("add_task_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_pet_name = st.selectbox("Pet", pet_names)
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
            task_time = st.text_input("Time", placeholder="e.g. 7:00 AM")
        with col3:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=30)
        add_task = st.form_submit_button("Add Task")

    if add_task and task_title and task_time:
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        selected_pet.add_task(Task(
            description=task_title,
            category=category,
            time=task_time,
            priority=priority,
            duration_minutes=int(duration),
        ))
        st.success(f"Added '{task_title}' for {selected_pet_name}!")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("**Current tasks:**")
        task_data = []
        for pet in owner.pets:
            for task in pet.tasks:
                task_data.append({
                    "Pet": pet.name,
                    "Task": task.description,
                    "Time": task.time,
                    "Category": task.category,
                    "Priority": task.priority,
                    "Minutes": task.duration_minutes,
                })
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("📋 Build Schedule")

available = st.slider("Available minutes today", min_value=30, max_value=300, value=120)

if st.button("Generate schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.warning("Add some tasks first before generating a schedule.")
    else:
        scheduler = Scheduler(owner, available_minutes=available)
        scheduler.generate_daily_plan()
        st.session_state.daily_plan = scheduler.daily_plan
        st.session_state.scheduler = scheduler

if "daily_plan" in st.session_state and st.session_state.daily_plan:
    st.write("**Today's Plan:**")
    for i, task in enumerate(st.session_state.daily_plan):
        pet_name = ""
        for pet in owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break

        status = "✅" if task.completed else "⬜"
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"{status} **{i+1}. {task.time}** — {task.description} ({pet_name}, {task.category}, {task.priority}, {task.duration_minutes} min)")
        with col2:
            if not task.completed:
                if st.button("Done", key=f"done_{i}"):
                    task.mark_complete()
                    st.rerun()

    scheduler = st.session_state.scheduler
    used = available - scheduler.get_time_remaining()
    remaining = scheduler.get_time_remaining()
    st.caption(f"Total: {used} min used, {remaining} min remaining")

    st.markdown("**Why this plan?** The scheduler sorts all tasks by priority (high → medium → low) and fills the day until your available time runs out. High-priority tasks are always scheduled first.")