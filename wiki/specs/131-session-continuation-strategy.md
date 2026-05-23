---
title: "Session Continuation & Token Budget Management"
status: "COMPLETE"
date: "2026-05-20"
---

# Session Continuation & Token Budget Management

**Status:** COMPLETE  
**Date:** 2026-05-20  
**Session Restart Frequency:** Daily (high priority)  
**Feature Duration:** Single session (< 1 hour, simple resume)  
**Token Budget Model:** Soft limit (warn at 80%, continue allowed)  
**Checkpoint Strategy:** Task-level (resume from last completed task)  
**Budget Exhaustion:** Graceful abort + state preservation

---

## 1. Session Continuation Model

### 1.1 Overview

**Assumption:** Features typically fit in one session (< 1 hour). Sessions end frequently (daily context limit or user interrupt). Workflow must survive frequent interruptions and resume cleanly.

**Session Lifecycle:**
```
Session Start (Day 1, 14:00)
  ├─ /spek.context (load vault context)
  ├─ /spek.prepare (create feature branch)
  └─ vault/session/ (create session state)

Feature Work (Day 1, 14:00-15:30)
  ├─ /spek.plan (specify → plan)
  ├─ /spek.implement (task 1, task 2, task 3)
  ├─ /spek.conclude (lessons, vault update)
  └─ Feature COMPLETE

Session End (Day 1, 15:30)
  ├─ Archive: vault/session/ → vault/
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
feature-id: add-logging-001
feature-name: Add Logging to Core Modules
phase: implementing
progress-percent: 60
started-at: 2026-05-20T14:00:00Z
last-checkpoint: 2026-05-20T14:45:00Z
total-sessions: 2
---

# Feature State: Add Logging

## Summary
Feature initiated Day 1 (14:00), interrupted mid-task Day 1 (14:45), resumed Day 2 (10:00).

## Phase Timeline
- specify: ✓ (2026-05-20T14:15:00Z, ~1000 tokens)
- plan: ✓ (2026-05-20T14:30:00Z, ~500 tokens)
- implement: ⧐ (2026-05-20T14:45:00Z, in progress, ~1200 tokens so far)
- post: ○ (pending)

## Implementation Progress
- Task 1 (Add imports): ✓ COMPLETE (2026-05-20T14:40:00Z, 150 tokens)
- Task 2 (Add log calls): ⧐ IN PROGRESS - INTERRUPTED at 2026-05-20T14:45:00Z
  - Code context: Working on main.py (lines 10-50)
  - Error state: None (clean interrupt)
  - Retry count: 0
  - Next action: Resume task 2 from where it stopped
- Task 3 (Config updates): ○ NOT STARTED

## Vault Context Loaded (Session 1)
- Decisions: 5 loaded
- Patterns: 3 loaded
- Lessons: 2 relevant loaded
- Total tokens (context): ~800

## Token Usage (Session 1)
- Phase: specify (1000) + plan (500) + implement (1200) = 2700 tokens
- Context reload cost (if needed): ~800 tokens
- Total: 2700 tokens (Session 1 only)
- Budget remaining: 5300 tokens (if 8K budget)

## Resumed Session (Session 2)

Checkpoint created: 2026-05-21T10:00:00Z

### Context Reload (Session 2)
- Vault reloaded: 5 decisions + 3 patterns + 2 lessons (~800 tokens)
- Previous state restored: phase=implementing, task 2 active
- Error check: None
- Status: Ready to resume

### Implementation Resumed
- Task 2 retry: From checkpoint
  - Code context reloaded: main.py (lines 10-50, previous state preserved)
  - Tokens used: ~150 (reuse previous tokens for code context if possible)
- Task 3: To be executed

### Token Usage (Session 2)
- Context reload: ~800 tokens
- Task 2 rerun: ~150 tokens
- Task 3: ~150 tokens (estimated)
- Total (Session 2): ~1100 tokens
- Combined total: 2700 + 1100 = 3800 tokens

## Lessons Captured (Post-Feature)
- Session 1 insights: Decided to use logging.info() for main.py
- Session 2 insights: Config structure simplified based on Task 2 experience
- Combined lessons: Both insights merged into single vault/lessons/<date>-<feature>.md
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

**Budget:** 8000 tokens per session (configurable)

**Warning Thresholds:**
- 60%: No warning (normal progress)
- 70%: Info message (pacing on track)
- 80%: **WARNING** (token usage significant, prepare to wrap up)
- 90%: **ALERT** (tokens nearly exhausted, feature may not complete this session)
- 100%+: Feature continues (soft limit, no hard stop)

### 5.2 Token Tracking in Session State

```yaml
---
feature-id: add-logging-001
phase: implementing
progress-percent: 60

# Token Usage Tracking
token-budget:
  total-per-session: 8000
  session-1-used: 2700
  session-2-used: 1100
  combined-total: 3800
  remaining: 4200
  budget-percentage: 47%
  warning-level-reached: false

token-usage-by-phase:
  specify: 1000
  plan: 500
  implement: 1200
  context-reload: 800
  total: 3500
---
```

### 5.3 Token Estimation & Warnings

**During Session (Real-Time Tracking):**

```
/spek.plan progress:
  ✓ Specify complete (1000 tokens used)
  Token budget: 1000 / 8000 (12%)
  
  ✓ Plan complete (500 tokens used)
  Token budget: 1500 / 8000 (18%)
  
/spek.implement progress:
  ✓ Task 1 complete (150 tokens used)
  Token budget: 1650 / 8000 (20%)
  
  ✓ Task 2 complete (200 tokens used)
  Token budget: 1850 / 8000 (23%)
  
  ⧐ Task 3 in progress... (estimated 150 tokens)
  Token budget: ~2000 / 8000 (25%) — On track

/spek.conclude phase (lessons generation):
  Estimating lessons token cost: ~300 tokens
  Final budget projection: 2300 / 8000 (28%)
  ✓ Feature will complete within budget

---

SCENARIO: Token Exhaustion Risk

/spek.plan phase 1:
  ✓ Specify complete (2500 tokens — higher than expected!)
  Token budget: 2500 / 8000 (31%)
  
  ⧐ Plan in progress... (estimated 1500 tokens)
  Token budget: ~4000 / 8000 (50%)
  
  ⧐ Plan complete (1500 tokens used)
  Token budget: 4000 / 8000 (50%)
  
/spek.implement phase:
  ⧐ Task 1 in progress... (estimated 400 tokens)
  Token budget: ~4400 / 8000 (55%)
  
  ✓ Task 1 complete (400 tokens)
  Token budget: 4400 / 8000 (55%)
  
  ⧐ Task 2 in progress... (estimated 500 tokens)
  Token budget: ~4900 / 8000 (61%)
  
  ⚠️  WARNING: Token usage higher than expected
      Suggest: Continue with Task 2 (50% complete)
      Or: Save state + resume next session
  
  ✓ Task 2 complete (500 tokens)
  Token budget: 4900 / 8000 (61%)
  
  ⧐ Task 3 in progress... (estimated 600 tokens)
  Token budget: ~5500 / 8000 (68%) — OK but tight
  
  ✓ Task 3 complete (600 tokens)
  Token budget: 5500 / 8000 (68%)
  
  ⚠️  ALERT: Approaching budget limit (over 80%)
      /spek.conclude estimated cost: 300-400 tokens
      Final projection: 5800-5900 / 8000 (73%)
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
