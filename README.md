# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Priority-based scheduling — high-priority tasks are scheduled first within the time available.
- Sorting by time — tasks are ordered chronologically, with unscheduled tasks listed last.
- Conflict warnings — overlapping scheduled tasks (even across different pets) are flagged.
- Daily & weekly recurrence — completing a recurring task automatically queues its next occurrence.
- Due-date aware filtering — completed tasks and not-yet-due tasks are excluded from today's plan.
- Priority-threshold filtering — tasks below your minimum priority setting are left out of the schedule.
- Scheduling reasoning — see exactly why each task was included or skipped (priority vs. time constraints).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
--- Buddy's Schedule (3 tasks, 60 min) ---
1. [HIGH] Morning walk — 30 min
2. [MEDIUM] Feed breakfast — 10 min
3. [LOW] Playtime — 20 min

--- Whiskers's Schedule (3 tasks, 65 min) ---
1. [HIGH] Grooming — 15 min
2. [MEDIUM] Feed breakfast — 10 min
3. [LOW] Nap time — 40 min
```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+
Task completion & due status

test_mark_complete_changes_task_status — completing a task flips completed to True.
test_is_due_for_once_task_matches_completed_flag — a one-off task is due until completed, then not.
test_is_due_respects_due_date — a task isn't due before its due_date, is due on/after it.
test_is_due_true_when_no_due_date — no due_date means due immediately.
test_is_due_false_when_completed_regardless_of_due_date — completed tasks are never due, even if their due date has arrived.
Recurrence (next_occurrence / complete_task)

test_next_occurrence_none_for_once_task — one-off tasks don't spawn a next occurrence.
test_next_occurrence_daily_due_tomorrow — daily tasks spawn a new, uncompleted task with a fresh id, due the next day.
test_next_occurrence_weekly_due_in_seven_days — weekly tasks spawn one due 7 days out.
test_complete_task_spawns_next_occurrence_for_daily_task — completing a daily task marks it done and adds the next occurrence to the pet.
test_complete_task_does_not_spawn_for_once_task — completing a one-off task spawns nothing.
test_completing_daily_task_creates_pending_task_for_next_day — the spawned task actually lands in pet.tasks and correctly transitions from not-due-today to due-tomorrow.
Conflict detection (overlaps / detect_conflicts)

test_overlaps_detects_intersecting_time_windows — overlapping time windows are flagged, non-overlapping ones aren't.
test_overlaps_ignores_unscheduled_tasks — a task with no start_time never overlaps anything.
test_detect_conflicts_across_pets — conflicts are detected even across two different pets owned by the same user.
test_detect_conflicts_ignores_not_yet_due_tasks — a task whose due date hasn't arrived yet is excluded from conflict checks.
test_detect_conflicts_flags_duplicate_start_times — two tasks with the identical start time are flagged as conflicting.
Filtering & sorting

test_filter_tasks_by_pet_and_status — filtering by pet and by completion status works independently.
test_sorted_tasks_returns_chronological_order — scheduled tasks come back sorted ascending by start time, regardless of insertion order.
test_sorted_tasks_places_unscheduled_tasks_last — unscheduled tasks (no start_time) always sort after scheduled ones.
Basic setup

test_add_task_increases_pet_task_count — adding a task to a pet increases its task list.
```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
python -m pytest
=================================================================== test session starts ===================================================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/angelazhao/CodePath/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 20 items                                                                                                                                        

tests/test_pawpal.py ....................                                                                                                           [100%]

=================================================================== 20 passed in 0.02s ====================================================================
```
Confidence Level: 5 Stars
## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `sort_by_time()`, `Schedule.generate()` (priority sort), `User.sorted_tasks()` | e.g., by priority, duration |
| Filtering | `Pet.pending_tasks()`, `Schedule.generate()` (`_skipped_priority`/`_skipped_time`), `User.filter_tasks()` | e.g., skip tasks if time runs out |
| Conflict handling | `Task.overlaps()`, `Task.time_range_minutes()`, `User.detect_conflicts()` | e.g., overlapping time slots |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()`, `User.complete_task()` | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
