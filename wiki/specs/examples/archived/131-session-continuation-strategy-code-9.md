```
Session Start
  ├─ `/spek.context` (load vault context)
  ├─ `/spek.prepare` (create feature branch)
  └─ `vault/session/` (create session state)

Feature Work
  ├─ `/spek.plan` (specify → plan)
  ├─ `/spek.implement` (execute tasks)
  ├─ `/spek.conclude` (lessons, vault update)
  └─ Feature COMPLETE

Session End
  ├─ Archive: `vault/session/` → `vault/`
  ├─ Git: merge feature branch to main
  └─ Session finished

---

SCENARIO: Interrupt Mid-Implementation (Task 2 of 3)

Session Start (Day 1, 14:00)
  ├─ /spek.prepare → Feature branch created
  └─ /spek.plan → specify + plan complete (60% of session)

Session Interrupted (Day 1, 14:45)
  ├─ /spek.implement running
  ├─ Task 1 DONE
  ├─ Task 2 IN PROGRESS → Interrupted (Ctrl+C or context limit)
  └─ Feature state saved: phase=implementing, % = 60, last_completed_task=1

Session Restart (Day 2, 10:00)
  ├─ /spek.context (reload vault context)
  ├─ /spek.prepare --resume (detect existing feature state)
  └─ /spek.implement --resume (resume from task 2)

Feature Continuation (Day 2, 10:00-10:30)
  ├─ Task 2 restarted (code context reloaded)
  ├─ Task 3 executed
  ├─ /spek.conclude (lessons generated from combined work)
  └─ Feature COMPLETE

Session End (Day 2, 10:30)
  ├─ Archive → vault/
  ├─ Git merge to main
  └─ Sessions combined (Day 1 + Day 2 logged)
```
