from pawpal_system import Pet, Task

def test_mark_complete_changes_status():
    task = Task(description="Morning walk", category="walk", time="7:00 AM")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Evening walk", category="walk", time="6:00 PM"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(description="Feeding", category="feeding", time="7:00 PM"))
    assert len(pet.tasks) == 2