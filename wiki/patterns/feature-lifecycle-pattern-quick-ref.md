# Feature Lifecycle Pattern — Quick Reference

**Category:** Workflow  
**Problem:** Feature work has multiple steps; no clear sequencing leads to skipped phases  
**Solution:** Explicit lifecycle: prepare → specify → plan → implement → post  
**Used in:** All skills (required ordering)  

---

## What It Is

Mandatory feature lifecycle with clear phase transitions:

```
FEATURE LIFECYCLE

START
  ↓
/spek.prepare → prepared
  ├─ Verify git state
  ├─ Load context
  └─ Create feature state file
  ↓
/spek.plan (specify) → specifying
  ├─ Load decisions + patterns
  ├─ Call /speckit.specify
  └─ Validate spec aligns with decisions
  ↓
/spek.plan (plan) → planning
  ├─ Load decisions + patterns + code graph
  ├─ Call /speckit.plan
  └─ Validate plan follows architecture
  ↓
/spek.implement → implementing
  ├─ Load decisions + patterns + code graph
  ├─ Execute implementation tasks
  └─ Collect code diff
  ↓
/spek.conclude → completing
  ├─ Extract lessons
  ├─ Update vault
  └─ Archive session
  ↓
COMPLETE
```
  /spek.plan (specify) → 25% (specifying)
---

## Why Use It

- ✅ Deterministic (same inputs → same outputs)
  /spek.plan (plan) → 50% (planning)
- ✅ Progress visible (phase tracked)
- ✅ Resumable (feature state persists across sessions)
- ✅ Auditable (session log records all transitions)

---
  /spek.conclude → 100% (completing)
## When to Use

✅ Multi-phase workflows with dependencies  
✅ Process compliance (no skipping steps)  
✅ Multi-session features (resumable)  
  /spek.conclude → 100% (completing)
    ├─ Extract lessons
    ├─ Update vault
    └─ Archive session

---

## State File: /memories/session/current-feature.md

```yaml
---
feature_name: "auth-refactor"
feature_id: "042"
status: "initialized | specifying | planning | implementing | completing"
session_start: "2026-05-19T10:00:00Z"
session_count: 1
phase: "prepared | specifying | planning | implementing | completing"
completion: "not-started | in-progress | complete"
---

## Progress
- ✅ Spec drafted
- [ ] Plan drafted
- [ ] Tasks generated
- [ ] Implementation complete

## Session Log
- Session 1: [timestamp] Prepared, loaded context
- Session 2: [timestamp] Specified, generated spec
```

---

## Phase Validation Rules

```
Preconditions for each phase:

SPECIFY:
  ✓ Feature state file exists
  ✓ Git state clean
  ✓ Context loaded
  → Can proceed

PLAN:
  ✓ spec.md exists
  ✓ SPECIFY phase complete
  → Can proceed

IMPLEMENT:
  ✓ spec.md exists
  ✓ plan.md exists
  ✓ tasks.md exists
  → Can proceed

POST:
  ✓ Feature implementation complete
  ✓ Artifacts collected
  → Can proceed
```

---

## Example: Phase Transition

```python
def run_specify_phase(feature_name):
    """Transition from PREPARED to SPECIFYING"""
    
    # Load current feature state
    state = load_feature_state(feature_name)
    
    # Validate preconditions
    assert state.phase == "prepared", \
        f"Cannot run specify; current phase is {state.phase}"
    assert os.path.exists("spec.md") is False, \
        "Spec already exists; cannot re-run specify"
    
    # Update state: transition to specifying
    state.phase = "specifying"
    state.completion = "in-progress"
    state.session_log.append(f"[{now}] SPECIFYING phase started")
    save_feature_state(state)
    
    # Run specify
    context = load_context()
    spec = speckit_specify(feature_name, context=context)
    
    # Validate output
    assert "## Overview" in spec
    assert "## Success Criteria" in spec
    
    # Save artifact
    save_file("spec.md", spec)
    
    print(f"✓ Specify phase complete (phase: {state.phase})")
```

---

## Related Patterns

- **Feature State Tracking** — State file structure
- **Skill Chaining** — How skills orchestrate across phases
- **Error Categorization** — Handle errors per phase

---

## Where It's Used

- **Primary:** [cli-orchestration.md](../specs/cli-orchestration.md)
- **Implemented in:**
  - [prepare-command.md](../specs/prepare-command.md)
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md)
  - [spek-implement-workflow.md](../specs/spek-implement-workflow.md)
  - [post-command.md](../specs/post-command.md)
- **Tracked in:**
  - [feature-state-tracking.md](../specs/feature-state-tracking.md)

---

## Quick Checklist

- [ ] State file created at /spek.prepare?
- [ ] Preconditions validated before each phase?
- [ ] Phase transition updates state (phase visible)?
- [ ] Session log records all transitions?
- [ ] No skipping phases (validator enforces order)?
- [ ] Resumable (state persists across sessions)?
- [ ] Error recovery documented (what if phase fails)?

---

## Notes on Resource Use

- Resource usage varies by feature and environment; teams should configure monitoring and tracking according to their needs.

Avoid embedding fixed numeric estimates in public-facing docs; keep budgeting and limits configurable within team configuration files.
