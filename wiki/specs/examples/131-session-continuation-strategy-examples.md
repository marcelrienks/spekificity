---
consolidated-from:
  - 131-session-continuation-strategy-code-1.md
  - 131-session-continuation-strategy-code-2.md
  - 131-session-continuation-strategy-code-3.md
  - 131-session-continuation-strategy-code-4.md
  - 131-session-continuation-strategy-code-5.md
  - 131-session-continuation-strategy-code-6.md
  - 131-session-continuation-strategy-code-7.md
  - 131-session-continuation-strategy-code-8.md
  - 131-session-continuation-strategy-code-9.md
consolidated-at: 2026-05-24T12:00:00Z
---

# Examples: 131 — Session Continuation Strategy

This file consolidates the example fragments for spec `131-session-continuation-strategy`.

## Sources

- 131-session-continuation-strategy-code-1.md
- 131-session-continuation-strategy-code-2.md
- 131-session-continuation-strategy-code-3.md
- 131-session-continuation-strategy-code-4.md
- 131-session-continuation-strategy-code-5.md
- 131-session-continuation-strategy-code-6.md
- 131-session-continuation-strategy-code-7.md
- 131-session-continuation-strategy-code-8.md
- 131-session-continuation-strategy-code-9.md

---

## Source: 131-session-continuation-strategy-code-1.md

```markdown
---
feature-id: add-logging-001
feature-name: Add Logging to Core Modules
sessions: 2
total-duration: 1.5 hours
created-at: 2026-05-21T10:30:00Z
---

# Lessons Learned: Add Logging to Core Modules

## Session Timeline
- **Session 1** (2026-05-20 14:00-14:45, 45 min): Specify + Plan + Partial Implement (Task 1-2 start)
- **Session 2** (2026-05-21 10:00-10:30, 30 min): Implement (Task 2-3) + Post

## What We Built
[standard lesson content, spanning both sessions]

## Implementation Insights (Multi-Session)
- Session 1 decision: Use logging.info() for core modules (rationale: ...)
- Session 2 refinement: Config structure simplified based on Task 2 feedback
- Combined insight: Logging + config are tightly coupled; future features should co-spec them

## Key Decisions (Accumulated)
- [Decision 1 from Session 1]
- [Decision 2 from Session 2]
[...] 

## Patterns Used (Accumulated)
- [Pattern 1 discovered Session 1]
- [Pattern 2 discovered Session 2]
[...] 

## Metrics
- Duration: 1.5 hours
- Sessions: 2
- Tasks: 3
- Code files modified: 3
- Lines of code: +45 logging lines
- Test coverage: 92%

## Resume Notes (Diagnostic Info)
- Interrupted Session 1: Ctrl+C during Task 2 (clean interrupt)
- Resumed Session 2: Fresh code graph + context reload; no issues
- Total token budget used: 3800 / 8000 (47%)
- No failures or recovery attempts needed
```

---

## Source: 131-session-continuation-strategy-code-2.md

```
Validation Checklist (/spek.prepare --resume):

✓ vault/session/ exists?
  └─ No: New feature workflow

✓ YAML frontmatter valid?
  └─ No: Corrupted state file; suggest --reset

✓ Feature branch still exists in git?
  └─ No: Branch deleted; can't resume; create new feature

✓ Feature branch on correct revision?
  └─ Different: Warn user about branch drift

✓ Spec file exists in vault?
 └─ No: Missing artifact; can't resume; start over

✓ Plan file exists in vault?
  └─ No: Missing artifact; can't resume; start over

✓ Feature phase is not "complete"?
  └─ Is "complete": Can't resume finished feature; start new one

✓ Token usage is < 2x budget?
  └─ Much higher: Suggest investigating token tracking; may be corrupted

✓ Timestamps are sensible (checkpoint < now < started)?
  └─ No: Time travel detected; corrupted state; suggest --reset

All checks pass?
  └─ Status: VALID — Resume safe
  
Any check fails?
  └─ Status: INVALID — Error handling (see 3b above)
```

---

## Source: 131-session-continuation-strategy-code-3.md

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

---

## Source: 131-session-continuation-strategy-code-4.md

```
Signal Handler (Ctrl+C):

Step 1: Catch Interrupt Signal
  ├─ Save current state immediately
  └─ Stop execution (no partial writes)

Step 2: Save Checkpoint
  ├─ Update vault/session/:
  │  ├─ last-checkpoint = NOW
  │  ├─ phase = current phase (specify|plan|implement|post)
  │  ├─ progress = best estimate based on completed steps
  │  └─ interrupted = true
  ├─ Flush to disk (ensure written)
  └─ Status: Checkpoint saved

Step 3: Clean Up Resources
  ├─ Close open files
  ├─ Cancel any in-flight API calls (to SpecKit, lat.md)
  ├─ Release locks (git, vault writes)
  └─ Status: Resources cleaned

Step 4: Notify User
  ├─ Print: "⚠️  Feature interrupted and saved"
  ├─ Print: "Feature state: phase=implementing, task 2 of 3"
  ├─ Print: "Resume with: spek.prepare --resume"
  └─ Exit code: 130 (SIGINT received)

Step 5: Exit Gracefully
  ├─ No data loss
  ├─ No corrupted state files
  ├─ Ready for resume next session
  └─ Session can be inspected for diagnostics
```

---

## Source: 131-session-continuation-strategy-code-5.md

```
/spek.plan progress:
  ✓ Specify complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ✓ Plan complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
/spek.implement progress:
  ✓ Task 1 complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ✓ Task 2 complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ⧐ Task 3 in progress... (estimated tokens omitted)
  Token budget: values omitted — On track

/spek.conclude phase (lessons generation):
  Estimating lessons token cost: estimate omitted
  Final budget projection: values omitted
  ✓ Feature will complete within budget (qualitative)
```

---

## Source: 131-session-continuation-strategy-code-6.md

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

---

## Source: 131-session-continuation-strategy-code-7.md

```
Step 1: Check for existing vault/session/
  ├─ Not found: New feature workflow (normal prepare)
  ├─ Found: Resume workflow (steps 2-5 below)

Step 2: Validate Feature State
  ├─ Parse YAML frontmatter (feature-id, phase, progress, last-checkpoint)
  ├─ Check Git state: Feature branch still exists? On correct branch?
  ├─ Check Feature artifacts: Spec + plan files exist in vault?
  ├─ Status: Valid state | Invalid (corrupted or stale) | Completed

Step 3a: Valid State → Resume Detected
  ├─ Restore context:
  │  ├─ Reload vault decisions + patterns from disk
  │  ├─ Load spec + plan from vault/specs/ and vault/plans/
  │  ├─ Query code graph for current code state (no cache; fresh)
  │  └─ Update vault/session/ with "resumed" timestamp
  ├─ Report: "Feature resumed: add-logging (phase: implementing, task 2 of 3)"
  └─ Ready: Return to caller for next step (/spek.implement --resume)

Step 3b: Invalid State → Error Handling
  ├─ Corrupted YAML: Notify user, suggest --reset (dangerous!)
  ├─ Missing feature branch: Notify user, suggest creating branch
  ├─ Missing spec/plan: Notify user, suggest re-running /spek.prepare (new feature)
  ├─ Feature marked "complete": Notify user (can't resume completed feature)
  └─ Recover: Ask user: retry resume | reset | new feature?

Step 3c: Completed Feature → Error
  ├─ Phase = "complete": Feature already finished
  ├─ Suggestion: "Start new feature with /spek.prepare <new-name>"
  └─ Abort: Exit with code 1
```
