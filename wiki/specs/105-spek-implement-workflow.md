# ATOMIC SPECIFICATION: Implement Command (C4.5)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Skill — /spek.implement (5-step task execution + enrichment wrapper)  
**Depends On:** speckit-integration-contract.md, enrichment-layer.md, feature-state-tracking.md  
**Used By:** `/spek.plan` (after task generation), CLI entry point  

---

## Overview

`/spek.implement` executes approved implementation tasks from task list, enriched with project context (code graph, vault decisions, patterns). Tasks run sequentially with error resilience; final code diff captured for `/spek.conclude` artifact collection.

---

## Execution Sequence

```
/spek.implement [--tasks=<list>] [--skip-tests] [--dry-run] [--verbose]
├─ Step 1: Validate feature state + artifacts (spec, plan, tasks exist)
├─ Step 2: Load enrichment context (vault decisions, code graph, patterns)
├─ Step 3: Execute tasks sequentially (pre/core/post per task)
│  ├─ Per-task pre-execution (context injection)
│  ├─ Per-task core (call /speckit.implement <task>)
│  ├─ Per-task post (validate, collect code diff)
│  └─ Continue-on-error (skip failed, proceed to next)
├─ Step 4: Collect execution artifacts (git diff, logs, errors)
└─ Step 5: Update feature state + report completion
```

---

## Step Details

### Step 1: Validate Feature State & Artifacts

**Checks:**
- Feature state file exists (`/memories/session/current-feature.md`)
- Current phase is `implementing` (or permit transition from `planning`)
- `specs/<feature>/spec.md` exists
- `specs/<feature>/plan.md` exists
- `specs/<feature>/tasks.md` exists (parsed, task count > 0)

**Output:** Artifacts validated, phase set to `implementing`

**Error Handling:** If any check fails → halt with clear error message + guidance

---

### Step 2: Load Enrichment Context

**Load from vault:**
- Recent decisions (top 5, active only) → `/memories/session/context-loaded.md`
- Recent patterns (top 3, active only) → `/memories/session/context-loaded.md`

**Load from code graph:**
- Recently modified files (git log --oneline -20, extract file paths)
- Related modules (query graph for callees/callers of modified files)
- Code hotspots (frequently-connected nodes)

**Compile into enrichment prompt:**
```
ACTIVE DECISIONS:
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

PROVEN PATTERNS:
- [Pattern 1]: When to use + benefits
- [Pattern 2]: When to use + benefits

RELATED CODE CHANGES:
- Recent changes: [file list]
- Related modules: [module list]
- Code hotspots: [symbol list]
```

**Output:** Enrichment context string (1-2K tokens, injected before each task)

---

### Step 3: Execute Tasks Sequentially

**For each task in tasks.md (parsed, ordered by ID):**

#### Pre-Execution: Context Injection

```
1. Extract task description + requirements
2. Inject enrichment context (decisions, patterns, code info)
3. Construct enriched task prompt (original + context)
4. Output: "Task N/M: [task-name]" (one-line progress)
```

#### Core Execution: Call SpecKit

```
/speckit.implement <enriched-task>
  ├─ Input: task description + enrichment
  ├─ Process: SpecKit invokes agent to execute task
  ├─ Output: Code changes (edits to source files)
  └─ Capture: All file modifications (for Step 4)
```

**Timing:** Record start + end time per task (for metrics)

#### Post-Execution: Validate + Collect

```
1. Check git status: What files changed?
2. Compute git diff for changed files (staged + unstaged)
3. Validate output (code parses? no syntax errors? size reasonable?)
4. Continue to next task (even if validation warnings)
```

**Error Handling (per task):**
- **Success:** Output "Task N/M complete ✓" (one line)
- **Partial (syntax errors):** Output "Task N/M partial (errors) ⚠" + continue to next task
- **Failure (major issue):** Output "Task N/M failed ✗" + continue to next task
- **Exception (crash):** Log exception, output "Task N/M exception ✗" + continue

**Artifact Collection (per task):**
- Task ID + name
- Start/end time
- Status (complete/partial/failed/exception)
- Code diff (git diff output)
- Error log (if any)

---

### Step 4: Collect Execution Artifacts

**Artifact structure:**

```
Execution Trace:
{
  "feature_name": "...",
  "feature_id": "...",
  "execution_start": "2026-05-20T10:00:00Z",
  "execution_end": "2026-05-20T10:15:30Z",
  "task_results": [
    {
      "task_id": "1",
      "task_name": "...",
      "status": "complete|partial|failed|exception",
      "duration_seconds": 45,
      "code_diff": "[full diff output]",
      "error_log": "[errors if status != complete]"
    },
    ...
  ],
  "total_tasks": 5,
  "completed_tasks": 4,
  "failed_tasks": 1,
  "final_code_diff": "[aggregated diff for all tasks]"
}
```

**Storage:**
- Write to `.spekificity/artifacts/execution-trace.json`
- Also write human-readable summary to `/memories/session/current-feature.md` (append section)

**Git State:**
- All code changes staged (git add) but NOT committed
- User reviews + approves before merge
- `/spek.conclude` will commit after lessons written

---

### Step 5: Update Feature State + Report

**Update `/memories/session/current-feature.md`:**
- Phase: `implementing` → `completing`
- Completion %: `75%` → `90%`
- Append session log entry: "Implement: N/M tasks complete, M failed"

**Report Output:**

```
=== IMPLEMENTATION COMPLETE ===

Tasks: 4/5 complete (1 failed)
Duration: 15 minutes 30 seconds
Code changes: +150 lines, -20 lines, 8 files modified

Failed Tasks:
- Task 5: Database migration (syntax error in migration script)
  Action: Review error log; manual fix or retry

Next: Review staged changes, then run /spek.conclude to archive lessons
```

**Exit Code:**
- 0 (success: all tasks complete)
- 1 (partial: some tasks failed, but implementation done)
- 2 (failure: critical error, halted)

---

## Success Criteria

- ✅ Feature state validated (spec, plan, tasks exist and phase correct)
- ✅ Context loaded for enrichment (decisions, patterns, code graph injected)
- ✅ Tasks execute sequentially (one after another, with error resilience)
- ✅ Code changes captured (git diff collected for each task)
- ✅ Artifacts collected (execution trace includes all task results)
- ✅ Session state updated (feature marked implementing, progress tracked)
- ✅ Errors don't stop workflow (failed tasks don't block subsequent tasks)

---

## Implementation Checklist

- [ ] Implement Step 1 (validate feature state)
- [ ] Implement Step 2 (load enrichment context)
- [ ] Implement Step 3 (execute tasks sequentially)
- [ ] Implement Step 4 (collect artifacts)
- [ ] Implement Step 5 (update state + report)
- [ ] Add error handling + continue-on-error
- [ ] Add execution trace logging
- [ ] Add git diff collection

---

## References

**Related Specs:**
- [speckit-integration-contract.md](speckit-integration-contract.md) — SpecKit integration details
- [enrichment-layer.md](enrichment-layer.md) — Context injection strategy
- [feature-state-tracking.md](feature-state-tracking.md) — Feature state machine
- [conclude-processing.md](conclude-processing.md) — Conclude-feature workflow

**External:**
- [extracted spec /spek.implement](speckit-integration-contract.md#spekimplement)

✅ All artifacts valid (feature state, spec, plan, tasks)  
✅ Context loaded (decisions, patterns, code graph)  
✅ All tasks attempted (continue-on-error behavior)  
✅ Code diff collected (final unified diff for all tasks)  
✅ Execution trace saved (JSON + human-readable summary)  
✅ Feature state updated (phase = completing, %90)  
✅ User can proceed to `/spek.conclude`  

---

## Error Handling

**Error Category 1: Missing Artifacts (Blockers)**
- Action: HALT + GUIDE
- Example: "tasks.md not found. Run `/spek.plan` first."

**Error Category 2: Task Execution Failures (Resilient)**
- Action: Log error, output status, continue to next task
- Example: "Task 3 failed (syntax error). Proceeding to Task 4."

**Error Category 3: Code Validation Warnings (Continue)**
- Action: Log warning, continue (may need manual review)
- Example: "Task 2 generated code with complexity warning. Continuing."

**Error Category 4: System Errors (Graceful Degradation)**
- Action: Attempt retry (1x), if fails → log exception, continue
- Example: "Code graph query timeout. Attempting without context. Proceeding."

---

## Flags & Options

```bash
spek implement [options]
  --tasks=<list>         # Run specific tasks by ID (e.g., "1,3,5")
                         # Default: all tasks in order
  
  --skip-tests           # Don't run post-task validation/tests
                         # Default: validate after each task
  
  --dry-run              # Preview changes, don't write to disk
                         # Default: write changes
  
  --verbose              # Show full task output + context
                         # Default: one-line progress per task
  
  --context-only         # Don't execute; just load/report context
                         # Default: execute all tasks
```

---

## Integration Points

**With `/speckit.implement`:**
- Calls `/speckit.implement` per task (core execution layer)
- Provides enriched context (vault + code graph)
- Captures output (code diff)
- Handles errors independently (resilience)

**With Feature State (feature-state-tracking.md):**
- Read: current feature name, check phase
- Write: update phase to `completing`, increment % to 90

**With Execution Tracing (conclude-processing.md):**
- Generate execution trace (JSON + human summary)
- Pass to `/spek.conclude` Step 1 (collect artifacts)

**With Enrichment Layer (enrichment-layer.md):**
- Load context (decisions, patterns, code graph)
- Inject into task prompts (pre-execution)
- No post-execution validation loop (unlike plan phase)

---

## Related Specifications

- [CLI Orchestration](cli-orchestration.md) — `/spek implement` command definition
- [SpecKit Integration Contract](speckit-integration-contract.md) — Integration with `/speckit.implement`
- [Enrichment Layer](enrichment-layer.md) — Context injection pattern
- [Feature State Tracking](feature-state-tracking.md) — State transitions
- [Conclude Processing](conclude-processing.md) — Artifact collection workflow
- [Memory Architecture](memory-architecture.md) — Context loading lifecycle
