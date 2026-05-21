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
/spek.prepare → 0% (prepared)
  ├─ Verify git state
  ├─ Load context
  └─ Create feature state file
  ↓
/spek.automate (specify) → 25% (specifying)
  ├─ Load decisions + patterns
  ├─ Call /speckit.specify
  └─ Validate spec aligns with decisions
  ↓
/spek.automate (plan) → 50% (planning)
  ├─ Load decisions + patterns + code graph
  ├─ Call /speckit.plan
  └─ Validate plan follows architecture
  ↓
/spek.implement → 75% (implementing)
  ├─ Load decisions + patterns + code graph
  ├─ Execute implementation tasks
  └─ Collect code diff
  ↓
/spek.post → 100% (completing)
  ├─ Extract lessons
  ├─ Update vault
  └─ Archive session
  ↓
COMPLETE
```

---

## Why Use It

- ✅ Deterministic (same inputs → same outputs)
- ✅ No skipped steps (validator prevents phase jumps)
- ✅ Progress visible (completion % tracked)
- ✅ Resumable (feature state persists across sessions)
- ✅ Auditable (session log records all transitions)

---

## When to Use

✅ Multi-phase workflows with dependencies  
✅ Process compliance (no skipping steps)  
✅ Multi-session features (resumable)  

❌ Ad-hoc development (phases too rigid)  
❌ Prototyping (overhead slows iteration)  
❌ One-shot scripts (state overhead)  

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
completion: 0-100
---

## Progress
- ✅ Spec drafted (0-25%)
- [ ] Plan drafted (25-50%)
- [ ] Tasks generated (50-75%)
- [ ] Implementation complete (75-100%)

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
    state.completion = 25
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
    
    print(f"✓ Specify phase complete (25% → {state.completion}%)")
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
- [ ] Phase transition updates state (completion %)?
- [ ] Session log records all transitions?
- [ ] No skipping phases (validator enforces order)?
- [ ] Resumable (state persists across sessions)?
- [ ] Error recovery documented (what if phase fails)?

---

## Token Cost

- **State file I/O:** ~10 tokens per transition
- **Precondition validation:** ~50 tokens
- **Session log updates:** ~5 tokens per entry

Total per feature: ~200 tokens (negligible vs. feature content).
