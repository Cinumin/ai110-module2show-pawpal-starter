from pawpal_system import Task, Pet, User, Schedule





def main() -> None:
    owner = User(name="Alice", time_available=120, min_priority="low")
    pet1 = Pet(name="Buddy", species="dog", age=3)
    pet1.add_task(Task(title="Morning walk", duration=30, priority="high"))
    pet1.add_task(Task(title="Feed breakfast", duration=10, priority="medium"))
    pet1.add_task(Task(title="Playtime", duration=20, priority="low"))

    pet2 = Pet(name="Whiskers", species="cat", age=2)
    pet2.add_task(Task(title="Feed breakfast", duration=10, priority="medium"))
    pet2.add_task(Task(title="Nap time", duration=40, priority="low"))
    pet2.add_task(Task(title="Grooming", duration=15, priority="high"))

    print("Today's schedule for Alice and her pets:")
    for pet in (pet1, pet2):
        schedule = Schedule()
        schedule.generate(pet, owner)
        schedule.display()


if __name__ == "__main__":
    main()

