from pawpal_system import Pet, Task, Owner, Scheduler

owner = Owner("Jordan")

dog = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=4)
cat = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task(
    description="Morning walk",
    category="walk",
    time="7:00 AM",
    priority="high",
    duration_minutes=40,
))

dog.add_task(Task(
    description="Give heartworm medication",
    category="meds",
    time="8:00 AM",
    priority="high",
    frequency="monthly",
    duration_minutes=5,
))

cat.add_task(Task(
    description="Wet food feeding",
    category="feeding",
    time="7:30 AM",
    priority="high",
    duration_minutes=10,
))

cat.add_task(Task(
    description="Play with feather toy",
    category="enrichment",
    time="5:00 PM",
    priority="medium",
    duration_minutes=20,
))

dog.add_task(Task(
    description="Evening walk",
    category="walk",
    time="6:00 PM",
    priority="medium",
    duration_minutes=30,
))

scheduler = Scheduler(owner, available_minutes=120)
scheduler.generate_daily_plan()

print(scheduler.get_plan_summary())

print("\n--- Marking 'Morning walk' as complete ---\n")
dog.tasks[0].mark_complete()

for task in scheduler.daily_plan:
    print(task)