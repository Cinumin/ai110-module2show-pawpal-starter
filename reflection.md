# PawPal+ Project Reflection

## 1. System Design
The user should be able to enter their own and their pet's information, add/edit tasks, generate a daily schedule based on the user's contraints and priorities.
Task
title: str
duration: float
priority: str

User
name: str
tasks: list[Task]
add_task(task)
edit_task(title, ...)
remove_task(title) 

Preferences
time_available: float
min_priority: str

Schedule
scheduled_tasks: list[Task]
generate(tasks, preferences)
display()

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I included four classes: Pet, User, Task, and Schedule. The Pet class contains the pet's information, such as name, age, species, and tasks. The User class has access and can modify the tasks by adding or removing and can adjust their preferences, priorities, and time availability. The Task class includes the task name, its priority, and time duration. The Schedule class manages the schedule by generating the tasks, displaying the schedule, and providing a reasoning.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, for instance, I altered the generate(pet, user) function in the Schedule class to take in the tasks from the Pet and User and return a list[Task]. Since the Pet has information containing its tasks and the User modifies those tasks, the Schedule can thus retrieve those tasks tailored to the Pet from the Pet class instead of the Task class, which contains the general task descriptions. In short, User is the actor who modifies the Task objects. Pet is where the list lives, containing the Task objects.
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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
