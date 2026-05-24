```
Step 1: Load Feature State
  ├─ Parse vault/session/
  ├─ Extract: last_completed_task = 1, current_task = 2 (in_progress)
  └─ Status: Ready to resume task 2

Step 2: Reload Code Context
  ├─ Query code graph: Get fresh code state (post-Day-1)
  ├─ Load spec + plan (unchanged since Day 1)
  ├─ Load vault context (decisions + patterns)
  └─ Inject into enrichment layer (decorator wrapper)

Step 3: Resume Task Execution
  ├─ Task 1: Already done, skip
  ├─ Task 2: Resume from checkpoint
  │  ├─ Previous error state: None (clean interrupt)
  │  ├─ Rerun: /speckit.implement <task2> (fresh context, same task definition)
  │  ├─ Execute: Task 2 completes successfully (or fails if code changed)
  │  └─ Checkpoint: task_2_complete = true, tokens_used = 200 (total Day 1+2)
  ├─ Task 3: Execute
  │  ├─ Context inject: Previous tasks' insights available
  │  ├─ Execute: /speckit.implement <task3>
  │  └─ Checkpoint: task_3_complete = true, tokens_used = 150
  └─ All tasks done

Step 4: Collect Results
  ├─ Git diff: Combined changes (Task 1 + 2 + 3)
  ├─ Execution trace: All tasks + resume markers
  └─ Update state: phase=completing, progress=90%

Step 5: Finalize
  ├─ Run /spek.conclude (generates lessons with multi-session metadata)
  └─ Complete feature
```
