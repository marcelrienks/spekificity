```
Task Failure During Resume (Task 2):

Step 1: Detect Failure
  ├─ /speckit.implement <task2> returns error
  ├─ Error type: "Code conflict" or "Invalid task definition"
  └─ Status: Task 2 incomplete

Step 2: Attempt Recovery
  ├─ Retry 1: Reload code context (in case file changed)
  │  ├─ Query code graph: Fresh code state
  │  └─ Rerun task (once)
  ├─ If still fails:
  │  ├─ Retry 2: Don't attempt (skip recovery)
  │  └─ Escalate to user
  └─ Status: Failure confirmed

Step 3: Save Error State
  ├─ Update vault/session/:
  │  ├─ task_2_error = "Code conflict detected; ...",
  │  ├─ task_2_retry_count = 2,
  │  └─ phase = "error_recovery"
  ├─ Flush to disk
  └─ Status: Error saved for diagnostics

Step 4: Notify User
  ├─ Print: "❌ Task 2 failed: Code conflict"
  ├─ Print: "Previous code state: <previous-hash>"
  ├─ Print: "Current code state: <current-hash>"
  ├─ Print: "Conflict: Task assumes <old-structure>, code is now <new-structure>"
  ├─ Options:
  │  ├─ 1. Resolve conflict manually, then: spek.implement --resume --force
  │  ├─ 2. Skip task 2, continue with task 3: spek.implement --resume --skip-failed
  │  ├─ 3. Abort feature + reset: spek.prepare --reset
  └─ Await user decision

Step 5: Continue Based on User Choice
  ├─ --force: Rerun task 2 (after user resolves conflict)
  ├─ --skip-failed: Mark task 2 failed, continue to task 3
  └─ --reset: Abort and start fresh
```
