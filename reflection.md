# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    My UML diagram included four classes connected by different types of relationships, not just inheritance. The goal was to separate the data classes like pets and tasks to more logicy classes like scheduling to keep the whole app organized.

- What classes did you include, and what responsibilities did you assign to each?

    The Pet class holds the basic animal info like names, species, breeds, ages, and is responsible for editing the profile. The Task class represents a single care activity and tracks its category, priority, duration, and completion status. The Schedule class represents the whole calendar system, basically knows how many minutes are available, and handles generating a daily plan that fits tasks within that time. Finally, the Owner class acts as the user and manages the list of pets, stores preferences, and serves as the entry point for seeing the daily plan.

**b. Design changes**

- Did your design change during implementation?

    Yes, my design changed a lot once I started writing and testing the actual code.

- If yes, describe at least one change and why you made it.

    The biggest change was renaming "Schedule" to "Scheduler" and expanding it significantly. The original UML had a simple Schedule that just held a date and a task list. During implementation, Scheduler became the brain of the app — it gained sort_by_time(), filter_by_pet(), filter_by_status(), detect_conflicts(), and mark_task_complete() methods. I also added a due_date field to Task and a find_pet_for_task() helper to Owner, neither of which were in the original UML. These additions came naturally as I built features that needed them.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

    The scheduler considers two main constraints: task priority and available time. It sorts all tasks by priority  and adds them to the daily plan until the time budget runs out. After building the plan, sort_by_time() reorders it chronologically so the user sees tasks in the order they should actually happen.

- How did you decide which constraints mattered most?

    Priority felt like the most important constraint because a pet owner would always want high-priority tasks like medication or feeding scheduled before optional enrichment activities. Time was the natural second constraint since the owner has a limited number of minutes each day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

    The conflict detection only checks for exact time-slot matches. It does not check whether task durations actually overlap, so a 40-minute task at 7:00 AM and a 10-minute task at 7:30 AM would not be flagged even though they technically overlap.

- Why is that tradeoff reasonable for this scenario?

    For a pet care app where tasks are entered as simple time labels like saying 7 AM rather than precise calendar blocks, exact-match detection catches the most obvious scheduling mistakes without adding unnecessary complexity. A pet owner using this tool is more likely to accidentally put two tasks at the same time than to carefully calculate overlapping durations.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

    I used Claude throughout every phase. In Phase 1, I described my three core actions and Claude generated the Mermaid.js UML diagram and Python class skeletons using dataclasses. In Phase 2, Claude fleshed out the full implementations. In Phase 4, I asked Claude to add sorting, filtering, conflict detection, and recurring task logic. In Phase 5, Claude drafted the full test suite. I also used Claude for the Streamlit UI wiring and README documentation.

- What kinds of prompts or questions were most helpful?

    The most effective prompts were ones where I attached my actual files and gave specific instructions, like "add a sort_by_time method that parses AM/PM strings." Vague prompts like "make it better" produced less useful results. Showing Claude the exact format I wanted saved a lot of back-and-forth.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

    When Claude first generated the test file, it used classes and a sys.path hack that didn't match the simple flat-function format my assignment expected. I rejected that structure and pasted the expected format back, asking Claude to redo it. The second version matched exactly what I needed.

- How did you evaluate or verify what the AI suggested?

    I verified by reading the generated code line by line, checking that each test targeted a real bug or feature, and running the tests to confirm they passed. For the scheduling logic, I also ran main.py and manually checked the terminal output against what I expected — for example, confirming that 7 AM appeared before 12 PM after sorting, and that the conflict warning named the correct tasks.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

    I tested six areas: basic task completion and pet task management, chronological sorting, recurring task creation for daily, weekly, and non-recurring frequencies, conflict detection for same-time and different-time tasks, filtering by pet name and completion status, and edge cases like an empty schedule and a task too long to fit.

- Why were these tests important?

    Each test targets a specific feature that could silently break if the code changes. The sorting test catches bugs in AM/PM parsing. The recurrence tests ensure completing a daily task actually creates tomorrow's instance. The conflict test confirms the scheduler flags overlaps instead of ignoring them. The edge case tests prevent crashes when there are no tasks or when a task exceeds the time budget.

**b. Confidence**

- How confident are you that your scheduler works correctly?

    I am really confident as all 16 tests pass, covering happy paths and edge cases for every major feature. The CLI demo in main.py produces the expected output for sorting, conflicts, filtering, and recurrence.

- What edge cases would you test next if you had more time?

    I would test overlapping durations, tasks spanning midnight, what happens when all tasks are already completed, and whether the UI correctly handles the recurring task toast notification after multiple rapid clicks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am most satisfied with how cleanly the Scheduler class turned out. It started as a simple "Schedule" in the UML with just a date and task list, but grew into a proper algorithm layer with sorting, filtering, conflict detection, and recurrence. The separation between pawpal_system.py and app.py made it easy to test everything in the terminal before touching Streamlit.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    I would improve conflict detection to check overlapping durations rather than just exact time matches. I would also add persistent storage so pets and tasks survive a browser refresh, and I would let the owner set preferences that actually influence the scheduling algorithm.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    The most important thing I learned is that AI is most useful when you treat it as a fast drafting tool, not a decision-maker. Every time I gave Claude specific constraints, the output was, most-of-the-time, immediately usable. When I was vague, I had to redo things.
