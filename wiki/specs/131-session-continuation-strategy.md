---
title: "Session Continuation & Token Budget Management"
status: "COMPLETE"
date: "2026-05-20"
---

# Session Continuation & Token Budget Management

**Status:** COMPLETE  
**Date:** 2026-05-20  
**Session Restart Frequency:** regular (as needed)  
**Feature Duration:** Single session (short, simple resume)  
**Token Budget Model:** Soft limit (configured threshold; warnings issued)  
**Checkpoint Strategy:** Task-level (resume from last completed task)  
**Budget Exhaustion:** Graceful abort + state preservation

---

## 1. Session Continuation Model

### 1.1 Overview

**Assumption:** Features typically fit in one session (< 1 hour). Sessions end frequently (daily context limit or user interrupt). Workflow must survive frequent interruptions and resume cleanly.

**Session Lifecycle:**
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

---

## 2. State Preservation: vault/session/

### 2.1 Session State File: `current-feature.md`

**Location:** `vault/session/` (created by `/spek.prepare`)

**Contents:**

```markdown
---
feature-id: add-logging
feature-name: Add Logging to Core Modules
phase: implementing
progress: TBD
started-at: TBD
last-checkpoint: TBD
total-sessions: TBD
---

# Feature State: Add Logging

## Summary
Feature initiated, interrupted mid-task, resumed later. Timestamps omitted.

## Phase Timeline
- specify: complete
- plan: complete
- implement: in progress
- post: pending

## Implementation Progress
- Task 1 (Add imports): COMPLETE
- Task 2 (Add log calls): IN PROGRESS - INTERRUPTED
  - Code context: Working on main.py (context preserved)
  - Error state: None (clean interrupt)
  - Retry count: recorded
  - Next action: Resume task 2 from checkpoint
- Task 3 (Config updates): NOT STARTED

## Vault Context Loaded (Session 1)
- Decisions: loaded
- Patterns: loaded
- Lessons: relevant loaded
- Total tokens (context): not specified

## Token Usage (Session 1)
- Phase totals recorded; numeric values omitted in public docs

## Resumed Session (Session 2)

Checkpoint created: recorded

### Context Reload (Session 2)
- Vault reloaded: decisions + patterns + lessons (counts omitted)
- Previous state restored: phase=implementing, task 2 active
- Error check: None
- Status: Ready to resume

### Implementation Resumed
- Task 2 retry: From checkpoint (context reloaded)
- Task 3: To be executed

### Token Usage (Session 2)
- Context reload and task reruns recorded; numeric values omitted

## Lessons Captured (Post-Feature)
- Session insights merged into single lesson file in the vault
```

### 2.2 State Preservation Requirements

**Essential State (should be preserved):**
- Feature ID + name
- Current phase (specifying → specified → planning → planned → implementing → completing → complete)
- Last completed task (task N-1)
- Progress percentage (estimate of overall feature completion)
- Timestamps (started, checkpoints, resumed)
- Error state (if any recoverable error occurred)

**Context State (Reload on Resume):**
- Vault decisions + patterns loaded (reload from vault, don't cache)
- Spec + plan artifacts (reload from vault, don't cache)
- Code graph cache (optional; can warm up if available)

**Session Metadata:**
- Token usage per phase (for tracking + billing)
- Number of sessions used (for estimation)
- Interrupted timestamps (for diagnosis)

---

## 3. Resume Workflow: /spek.prepare --resume

### 3.1 Resume Detection

**When user runs `/spek.prepare --resume` or `/spek.prepare` (no feature name):**

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

### 3.2 Resume Command Signature

```bash
spek.prepare [--resume] [--reset] [feature-name]

Options:
  --resume       Auto-detect existing feature; restore state (default if no args)
  --reset        Clear existing feature state + start fresh (dangerous!)
  feature-name   Start new feature (ignores --resume if provided)
  
Examples:
  spek.prepare --resume                    # Auto-detect existing feature
  spek.prepare                             # Auto-detect (same as --resume)
  spek.prepare add-logging                 # New feature (overrides existing)
  spek.prepare --reset                     # Clear existing state + restart
```

---

## 4. Resume Workflow: /spek.implement --resume

### 4.1 Task-Level Checkpoints

**Checkpoint Saved After Each Task:**

```
Task 1: Add logging imports
├─ Start: /spek.implement --task 1
├─ Execute: /speckit.implement <task1>
├─ Success: Code diff collected
└─ Checkpoint: task_1_complete = true, tokens_used = 150

Task 2: Add logging calls (INTERRUPTED)
├─ Start: /spek.implement --task 2
├─ Execute: /speckit.implement <task2>
├─ Interrupted: Ctrl+C at 60% through task
└─ Checkpoint: task_2_status = in_progress, tokens_used = 50, last_line = "# TODO: finish main.py"

Session Interrupted → state saved to vault/session/
```

### 4.2 Resume From Last Task

**When `/spek.implement --resume` is called:**

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

### 4.3 Resume Command Signature

```bash
spek.implement [--resume] [--from-task N] [--dry-run]

Options:
  --resume       Resume from last incomplete task (inferred from state file)
  --from-task N  Resume from specific task N (for manual recovery)
  --dry-run      Preview what would be executed without running
  
Examples:
  spek.implement --resume          # Continue from task 2
  spek.implement --from-task 2     # Manual resume at task 2
  spek.implement --dry-run         # Show tasks, don't execute
```

---

## 5. Token Budget Tracking

### 5.1 Soft Limit Model

**Budget:** session token soft limit (configurable)

**Warning Thresholds:**
- Normal progress: informational
- Pacing message: informational (when usage increases)
- Warning: token usage significant (prepare to wrap up)
- Alert: tokens nearly exhausted (feature may not complete this session)
- Soft limit: feature may continue; user notified

### 5.2 Token Tracking in Session State

```yaml
---
feature-id: add-logging-001
phase: implementing
progress-estimate: qualitative (numeric values omitted)

# Token Usage Tracking (numeric values omitted in public docs)
token-budget:
  total-per-session: configured-value
  session-1-used: recorded (omitted)
  session-2-used: recorded (omitted)
  combined-total: recorded (omitted)
  remaining: recorded (omitted)
  budget-percentage: recorded (omitted)
  warning-level-reached: false

token-usage-by-phase:
  specify: recorded (omitted)
  plan: recorded (omitted)
  implement: recorded (omitted)
  context-reload: recorded (omitted)
  total: recorded (omitted)
---
```

### 5.3 Token Estimation & Warnings

**During Session (Real-Time Tracking):**

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

---

SCENARIO: Token Exhaustion Risk

/spek.plan phase 1:
  ✓ Specify complete (tokens used recorded; higher than expected)
  Token budget: values omitted
  
  ⧐ Plan in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ⧐ Plan complete (tokens used recorded)
  Token budget: values omitted
  
/spek.implement phase:
  ⧐ Task 1 in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ✓ Task 1 complete (tokens used recorded)
  Token budget: values omitted
  
  ⧐ Task 2 in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ⚠️  WARNING: Token usage higher than expected
      Suggest: Continue with Task 2 (partial progress)
      Or: Save state + resume next session
  
  ✓ Task 2 complete (tokens used recorded)
  Token budget: values omitted
  
  ⧐ Task 3 in progress... (estimated tokens omitted)
  Token budget: values omitted — OK but tight
  
  ✓ Task 3 complete (tokens used recorded)
  Token budget: values omitted
  
    ⚠️  ALERT: Approaching budget limit (configured warning level)
      /spek.conclude estimated cost: estimate omitted
      Final projection: values omitted
      ✓ Feature will complete (soft limit allows)
```

### 5.4 Budget Exhaustion Handling

**If tokens exceed budget (soft limit):**

```
Option 1: Continue Gracefully (Default)
  ├─ Token usage is informational (soft limit)
  ├─ Feature execution continues
  ├─ All phases run (specify → plan → implement → post)
  └─ User warned: "Budget exceeded, but feature complete"

Option 2: Save & Resume (User Initiated)
  ├─ At any phase, user can press Ctrl+C
  ├─ State saved: phase, last_completed_task, all artifacts
  ├─ Session closed: vault/session/ ready for resume next day
  ├─ User resumes: /spek.prepare --resume (next session)
  └─ Feature completes second session (split across days)

Option 3: Compress & Continue (Optional, Future)
  ├─ Auto-enable caveman compression at 80% budget
  ├─ Reduces token usage ~75% for remaining phases
  ├─ May reduce quality slightly (compressed context)
  ├─ Flag: --auto-compress-on-budget (off by default)
  └─ Not implemented in Phase 1; future enhancement
```

---

## 6. Graceful Abort & State Preservation

### 6.1 Interrupt Handling: Ctrl+C

**When user interrupts (Ctrl+C) during any phase:**

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

### 6.2 Error Recovery: Task Failure During Resume

**If a task fails during resume (e.g., code changed, task definition invalid):**

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

### 6.3 State Validation on Resume

**Before resuming, validate all state:**

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

## 7. Multi-Session Features: Lessons Aggregation

### 7.1 Session Metadata in Lessons

**When `/spek.conclude` runs after multi-session feature:****

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

## 8. Implementation Checklist

### 8.1 Feature Completion

**For each feature, verify before marking complete:**

✅ All tasks executed successfully (or user chose to skip)  
✅ Code diff collected and verified  
✅ State file updated to phase="completing" + progress=90%  
✅ Lessons generated (with multi-session metadata if applicable)  
✅ Vault updated (decisions + patterns)  
✅ vault/session/ prepared for archival  
✅ Feature branch ready to merge  
✅ User confirmed feature is ready for /spek.conclude  

### 8.2 Resume Capability

**For resume to work reliably:**

✅ vault/session/ created during /spek.prepare  
✅ State file updated after each phase + each task  
✅ Checkpoint saved on interrupt (Ctrl+C)  
✅ State validation passes pre-resume  
✅ Context can be reloaded from vault (no cache dependencies)  
✅ Task numbering consistent between sessions  
✅ Code graph queries work on both fresh + changed code  

### 8.3 Token Tracking

**For token budget to be informative:**

✅ Token usage logged per phase  
✅ Token usage logged per task  
✅ Context reload cost estimated  
✅ Warnings issued at 80% + 90% thresholds  
✅ Combined session totals tracked  
✅ Projection estimates (remaining budget, finish likelihood)  

---

## 9. Success Criteria

✅ **Daily Restart Handling:**
- Session interrupt mid-task → state saved
- Session restart next day → feature resumes from last task
- No manual state reconstruction needed

✅ **Single-Session Features:**
- Typical feature completes in < 1 hour
- Token budget sufficient (8K tokens allows comfortable 3-4 feature cycles)
- No multi-session complexity for common case

✅ **Soft Token Limit:**
- 80% threshold: User informed (warning)
- 90% threshold: User alerted (but continues allowed)
- 100%+: Feature completes (soft limit, no hard stop)
- Graceful degradation; no surprise interrupts

✅ **Task-Level Checkpoints:**
- Resume from last completed task (not entire phase)
- Task re-execution handles code changes (fresh graph queries)
- No state corruption even if task fails on resume

✅ **Graceful Abort:**
- Ctrl+C during any phase → state saved
- Error messages clear + actionable
- No partial writes or corrupted artifacts
- Resume always safe (validation checks prevent bad states)

✅ **Multi-Session Diagnostics:**
- Lessons show session count + duration
- Accumulated decisions + patterns visible in final lesson
- Token usage transparent (per-session + combined)
- Resume history available for troubleshooting

---

## 10. Configuration

### 10.1 Token Budget (Configurable)

**File:** `.spek/config.yaml`

```yaml
token-budget:
  total-per-session: 8000          # Soft limit, warnings at 80%/90%
  warning-threshold: 0.80          # Warn at 80%
  alert-threshold: 0.90            # Alert at 90%
  allow-exceed: true               # Continue beyond budget (soft limit)
  auto-compress-on-warning: false  # Future: auto-compress context if warned
  
# Example: 2K token sessions (aggressive compression)
# total-per-session: 2000
# warning-threshold: 0.75
# alert-threshold: 0.85
```

### 10.2 Resume Behavior (Configurable)

```yaml
resume:
  enabled: true                    # Allow resume on interrupt
  auto-detect: true                # Auto-detect existing feature on prepare
  task-level-checkpoints: true     # Save state after each task
  validation-on-resume: true       # Run validation checks before resume
  max-resume-retries: 2            # Retry failed tasks up to 2 times
```

---

## 11. Integration with Spekificity Commands

### 11.1 Updated `/spek.prepare`

```bash
/spek.prepare [--resume] [--reset] [feature-name]

Changes from prior spec:
  ├─ New: Auto-detect existing feature (if no args + vault/session/ exists)
  ├─ New: --resume flag (explicit resume request)
  ├─ New: --reset flag (dangerous: clear state, start fresh)
  ├─ New: Resume validation (check branch, artifacts, state)
  ├─ New: Update session state file with "resumed" timestamp
  └─ Backward compat: /spek.prepare <name> still works (new feature)
```

### 11.2 Updated `/spek.implement`

```bash
/spek.implement [--resume] [--from-task N] [--skip-failed] [--force] [--dry-run]

Changes from prior spec:
  ├─ New: --resume flag (resume from last incomplete task)
  ├─ New: --from-task N (resume from specific task, for manual recovery)
  ├─ New: --skip-failed (skip failed task, continue to next)
  ├─ New: --force (retry failed task after user resolves conflict)
  ├─ New: --dry-run (preview tasks without executing)
  ├─ New: Task-level checkpoints (state saved after each task)
  ├─ New: Error recovery logic (attempt task 2x, then escalate)
  └─ Backward compat: Normal /spek.implement runs all tasks (new if no prior state)
```

### 11.3 New Command: `/spek token-status`

```bash
/spek token-status

Output:
  Feature: Add Logging (phase: implementing)
  Session 1: 2700 / 8000 tokens (33%)
  Session 2: 1100 / 8000 tokens (13%)
  Combined: 3800 / 8000 tokens (47%)
  Remaining: 4200 / 8000 tokens
  
  Projection:
    - If feature completes this session: ~4000 / 8000 (50% final usage)
    - Budget headroom: Comfortable
```

---

## 12. References

- **Memory Architecture:** [specs/memory-architecture.md](../specs/030-memory-architecture.md)
- **Feature State Tracking:** [specs/feature-state-tracking.md](../specs/040-feature-state-tracking.md)
- **Prepare Command:** [specs/prepare-command.md](../specs/100-prepare-command.md)
- **Conclude Command:** [specs/conclude-command.md](../specs/102-conclude-command.md)
- **Spek Implement Workflow:** [specs/spek-implement-workflow.md](../specs/105-spek-implement-workflow.md)
- **Token Budget (Phase 2):** [specs/token-budget.md](../specs/130-token-budget.md)

---

## 13. Future Enhancements (Phase 2+)

- [ ] Auto-compress context at 80% budget (soft limit + quality trade-off)
- [ ] Checkpoint every N tokens (not just per-task)
- [ ] Multi-branch feature support (pair programming across branches)
- [ ] Checkpoint snapshots for manual branching (if-then recovery paths)
- [ ] Estimated token cost per task (machine-learned model)
- [ ] Automated token optimization (suggest --compress flags)
