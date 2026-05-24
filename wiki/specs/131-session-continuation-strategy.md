# Session Continuation & Token Budget Management


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Date:** 2026-05-20  
**Session Restart Frequency:** regular (as needed)  
**Feature Duration:** Single session (short, simple resume)  
**Token Budget Model:** Soft limit (configured threshold; warnings issued)  
**Checkpoint Strategy:** Task-level (resume from last completed task)  
**Budget Exhaustion:** Graceful abort + state preservation

---


## 1.1 Overview

**Assumption:** Features typically fit in one session (< 1 hour). Sessions end frequently (daily context limit or user interrupt). Workflow must survive frequent interruptions and resume cleanly.

**Session Lifecycle:**

> Example moved to [Example: 131-session-continuation-strategy-code-9.md](./examples/131-session-continuation-strategy-code-9.md)


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


## 12. References

- **Memory Architecture:** [specs/memory-architecture.md](../specs/030-memory-architecture.md)
- **Feature State Tracking:** [specs/feature-state-tracking.md](../specs/040-feature-state-tracking.md)
- **Prepare Command:** [100-prepare-command.md](../specs/100-prepare-command.md)
- **Conclude Command:** [102-conclude-command.md](../specs/102-conclude-command.md)
- **Spek Implement Workflow:** [specs/spek-implement-workflow.md](../specs/105-spek-implement-workflow.md)
- **Token Budget (Phase 2):** [specs/token-budget.md](../specs/130-token-budget.md)

---


## 1. Session Continuation Model


## 2. State Preservation: vault/session/


## 2.1 Session State File: `current-feature.md`

**Location:** `vault/session/` (created by `/spek.prepare`)

**Contents:**


> Example moved to [Example: 131-session-continuation-strategy-code-8.md](./examples/131-session-continuation-strategy-code-8.md)



## 2.2 State Preservation Requirements

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


## 3.1 Resume Detection

**When user runs `/spek.prepare --resume` or `/spek.prepare` (no feature name):**


> Example moved to [Example: 131-session-continuation-strategy-code-7.md](./examples/131-session-continuation-strategy-code-7.md)



## 3.2 Resume Command Signature

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


## 4.1 Task-Level Checkpoints

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


## 4.2 Resume From Last Task

**When `/spek.implement --resume` is called:**


> Example moved to [Example: 131-session-continuation-strategy-code-6.md](./examples/131-session-continuation-strategy-code-6.md)



## 4.3 Resume Command Signature

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


## 5.1 Soft Limit Model

**Budget:** session token soft limit (configurable)

**Warning Thresholds:**
- Normal progress: informational
- Pacing message: informational (when usage increases)
- Warning: token usage significant (prepare to wrap up)
- Alert: tokens nearly exhausted (feature may not complete this session)
- Soft limit: feature may continue; user notified


## 5.2 Token Tracking in Session State

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


## 5.3 Token Estimation & Warnings

**During Session (Real-Time Tracking):**


> Example moved to [Example: 131-session-continuation-strategy-code-5.md](./examples/131-session-continuation-strategy-code-5.md)



## 5.4 Budget Exhaustion Handling

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


## 6.1 Interrupt Handling: Ctrl+C

**When user interrupts (Ctrl+C) during any phase:**


> Example moved to [Example: 131-session-continuation-strategy-code-4.md](./examples/131-session-continuation-strategy-code-4.md)



## 6.2 Error Recovery: Task Failure During Resume

**If a task fails during resume (e.g., code changed, task definition invalid):**


> Example moved to [Example: 131-session-continuation-strategy-code-3.md](./examples/131-session-continuation-strategy-code-3.md)



## 6.3 State Validation on Resume

**Before resuming, validate all state:**


> Example moved to [Example: 131-session-continuation-strategy-code-2.md](./examples/131-session-continuation-strategy-code-2.md)


---


## 7. Multi-Session Features: Lessons Aggregation


## 7.1 Session Metadata in Lessons

**When `/spek.conclude` runs after multi-session feature:****


> Example moved to [Example: 131-session-continuation-strategy-code-1.md](./examples/131-session-continuation-strategy-code-1.md)


---


## 8. Implementation Checklist


## 8.1 Feature Completion

**For each feature, verify before marking complete:**

✅ All tasks executed successfully (or user chose to skip)  
✅ Code diff collected and verified  
✅ State file updated to phase="completing" + progress=90%  
✅ Lessons generated (with multi-session metadata if applicable)  
✅ Vault updated (decisions + patterns)  
✅ vault/session/ prepared for archival  
✅ Feature branch ready to merge  
✅ User confirmed feature is ready for /spek.conclude  


## 8.2 Resume Capability

**For resume to work reliably:**

✅ vault/session/ created during /spek.prepare  
✅ State file updated after each phase + each task  
✅ Checkpoint saved on interrupt (Ctrl+C)  
✅ State validation passes pre-resume  
✅ Context can be reloaded from vault (no cache dependencies)  
✅ Task numbering consistent between sessions  
✅ Code graph queries work on both fresh + changed code  


## 8.3 Token Tracking

**For token budget to be informative:**

✅ Token usage logged per phase  
✅ Token usage logged per task  
✅ Context reload cost estimated  
✅ Warnings issued at 80% + 90% thresholds  
✅ Combined session totals tracked  
✅ Projection estimates (remaining budget, finish likelihood)  

---


## 10. Configuration


## 10.1 Token Budget (Configurable)

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


## 10.2 Resume Behavior (Configurable)

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


## 11.1 Updated `/spek.prepare`

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


## 11.2 Updated `/spek.implement`

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


## 11.3 New Command: `/spek token-status`

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


## 13. Future Enhancements (Phase 2+)

- [ ] Auto-compress context at 80% budget (soft limit + quality trade-off)
- [ ] Checkpoint every N tokens (not just per-task)
- [ ] Multi-branch feature support (pair programming across branches)
- [ ] Checkpoint snapshots for manual branching (if-then recovery paths)
- [ ] Estimated token cost per task (machine-learned model)
- [ ] Automated token optimization (suggest --compress flags)