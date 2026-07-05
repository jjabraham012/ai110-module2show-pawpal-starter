from pawpal_system import Pet, Task, Owner, Scheduler

owner = Owner("Jordan")

dog = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=4)
cat = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task(
    description="Evening walk",
    category="walk",
    time="6:00 PM",
    priority="medium",
    duration_minutes=30,
))

cat.add_task(Task(
    description="Play with feather toy",
    category="enrichment",
    time="5:00 PM",
    priority="medium",
    duration_minutes=20,
))

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
    time="7:00 AM",
    priority="high",
    duration_minutes=10,
))

scheduler = Scheduler(owner, available_minutes=120)
scheduler.generate_daily_plan()

print("=== UNSORTED PLAN ===\n")
print(scheduler.get_plan_summary())

print("\n\n=== SORTED BY TIME ===\n")
scheduler.sort_by_time()
print(scheduler.get_plan_summary())

print("\n\n=== CONFLICT DETECTION ===\n")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts found.")

print("\n\n=== FILTER BY PET: Buddy ===\n")
buddy_tasks = scheduler.filter_by_pet("Buddy")
for task in buddy_tasks:
    print(task)

print("\n\n=== FILTER BY PET: Mochi ===\n")
mochi_tasks = scheduler.filter_by_pet("Mochi")
for task in mochi_tasks:
    print(task)

print("\n\n=== RECURRING TASK: Marking 'Morning walk' complete ===\n")
morning_walk = next(t for t in dog.tasks if t.description == "Morning walk")
next_task = scheduler.mark_task_complete(morning_walk)
print(f"Completed: {morning_walk}")
if next_task:
    print(f"Auto-created next occurrence: {next_task}")
    print(f"  Due date: {next_task.due_date}")

print(f"\nBuddy now has {len(dog.tasks)} tasks:")
for task in dog.tasks:
    print(f"  {task}")

print("\n\n=== FILTER BY STATUS: Pending only ===\n")
pending = scheduler.filter_by_status(completed=False)
for task in pending:
    print(task)