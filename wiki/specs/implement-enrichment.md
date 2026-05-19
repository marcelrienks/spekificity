# ATOMIC SPECIFICATION: Implement Enrichment (C3.5)

**Status:** ATOMIC SPECIFICATION  
**Type:** Integration Layer 2f — /spek.implement Wrapper  
**Depends On:** decorator-wrapper-pattern.md  

---

## Overview

`/spek.implement` wraps `/speckit.implement` to collect execution artifacts and update session memory with progress.

---

## Execution Sequence

```
/spek.implement
├─ PRE: Validate preconditions
│  ├─ Check tasks.md exists (not empty)
│  ├─ Check git working dir is clean
│  └─ Load feature state
├─ CORE: Run SpecKit
│  ├─ Call /speckit.implement
│  ├─ Execute all tasks
│  ├─ Generate code changes
│  └─ Capture execution trace
├─ POST: Collect + Update
│  ├─ Collect all artifacts (code, logs, errors)
│  ├─ Analyze success/failure rates
│  ├─ Update /memories/session/current-feature.md
│  └─ Report completion status
└─ Return: Artifacts + status
```

---

## Pre-Execution

**Preconditions:**
- tasks.md exists and is complete
- Git working directory is clean
- No uncommitted changes (or user stashed them)

**Process:**
- Validate preconditions
- Log feature state (what we're implementing)
- Report ready status

---

## Core Execution

**Command:** `/speckit.implement`

**Process:**
- SpecKit executes all tasks sequentially (or parallel if configured)
- Each task generates code changes
- Execution trace logged (task ID, status, duration, errors)

**Output:**
- Modified files (code changes)
- Execution trace (log of what ran)
- Errors/warnings (if any tasks failed)

---

## Post-Execution: Artifact Collection

**Collect:**
1. Code changes (git diff)
   - List of modified files
   - Lines added/deleted
   - Diff content
2. Execution trace
   - Task execution log
   - Task success/failure
   - Duration per task
   - Any errors/warnings
3. Test results (if tests run)
   - Pass/fail counts
   - Failed test names
4. Build output (if compiled)
   - Build success/failure
   - Warnings/errors

**Analyze:**
- Success rate: how many tasks completed?
- Partial completion: 60% complete vs. 100%?
- Error summary: what went wrong?

**Update Memory:**
- Mark /memories/session/current-feature.md phase as "implementing"
- Set completion % based on task success
- Log session entry: "[IMPLEMENTED] X/Y tasks complete"
- Note blockers (failed tasks)

**Report:**
- User-visible summary: "✓ Implementation complete (Y/Y tasks) or ⚠ Partial (X/Y tasks)"
- List of failures (if any)
- Next steps (fix failures or proceed to post)

---

## Error Handling

**If task fails:**
- Log error
- Continue with remaining tasks (partial completion is valid)
- Report summary of failures

**If git commit fails:**
- Don't block (implementation still succeeded)
- Suggest manual commit

**If multiple tasks fail:**
- Still continue
- Report summary

---

## Success Criteria

✅ Preconditions validated  
✅ All tasks executed (or partial completion tracked)  
✅ Artifacts collected (code, logs, errors)  
✅ Memory updated with progress  
✅ User informed of completion status  

---

## Implementation Checklist

- [ ] Validate tasks.md exists and is complete
- [ ] Check git working directory is clean
- [ ] Call /speckit.implement
- [ ] Collect execution trace and artifacts
- [ ] Analyze success/failure rates
- [ ] Update /memories/session/current-feature.md
- [ ] Report completion status

---

## References

**Related Specs:**
- [decorator-wrapper-pattern.md](decorator-wrapper-pattern.md)
- [session-memory.md](session-memory.md) — Feature state updated here

**External:**
- [extracted spec Layer 2f](speckit-integration-contract.md#2f-enriched-implement-spekimplement)
