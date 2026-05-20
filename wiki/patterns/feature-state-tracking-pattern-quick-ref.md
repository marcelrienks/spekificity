# Feature State Tracking Pattern — Quick Reference

**Category:** State Management  
**Problem:** Feature work spans multiple phases; unclear which is current, what's completed  
**Solution:** Explicit state file tracking lifecycle phases  
**Used in:** All skills (read/write state)  

---

## What It Is

Persistent feature state file tracking progress through lifecycle:

```
FEATURE STATE TRACKING

/memories/session/current-feature.md

├─ YAML Frontmatter
│  ├─ feature_name: "auth-refactor"
│  ├─ feature_id: "042"
│  ├─ status: "initialized | specifying | planning | implementing | completing"
│  ├─ phase: "prepared | specifying | planning | implementing | completing"
│  ├─ completion: 0-100
│  └─ session_count: 1
│
└─ Markdown Sections
   ├─ Current Phase: [description]
   ├─ Progress by Phase: [checklist]
   ├─ Session Log: [timeline]
   └─ Notes: [scratchpad]

Lifecycle Transitions:
  initialized (0%)
    ↓ /spek.prepare
  prepared (0%)
    ↓ /spek.automate (specify)
  specifying (25%)
    ↓ /spek.automate (plan)
  planning (50%)
    ↓ /spek.implement
  implementing (75%)
    ↓ /spek.post
  completing (100%)
```

---

## Why Use It

- ✅ Progress visible (completion % tracked)
- ✅ Resumable (state persists across sessions)
- ✅ Auditable (session log records all work)
- ✅ Precondition validation (prevents phase skipping)
- ✅ Feature isolation (multiple features can track separately)

---

## When to Use

✅ Multi-session features (resume capability)  
✅ Progress visibility (user needs to know status)  
✅ Process compliance (no skipping phases)  
✅ Interruption resilience (state survives interrupts)  

❌ Single-shot tasks (state overhead)  
❌ Stateless systems (no phase concept)  
❌ Throwaway work (not worth archival)  

---

## State File Structure

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

## Current Phase: Implementing

Implementation in progress. Estimated 2 more sessions.

## Progress by Phase

- ✅ Spec drafted (0-25%)
- ✅ Plan drafted (25-50%)
- [ ] Tasks generated (50-75%)
- [ ] Implementation complete (75-100%)

## Session Log

- Session 1: [2026-05-19T10:00:00Z] Prepared, loaded context
- Session 1: [2026-05-19T10:30:00Z] Specified, generated spec.md
- Session 1: [2026-05-19T11:15:00Z] Planned, generated plan.md
- Session 2: [2026-05-20T14:00:00Z] Implementing tasks...

## Notes

- Spec slightly diverged from prior patterns (more REST endpoints)
- Plan suggests 3-layer cache architecture (aligned with decision cache-001)
- Awaiting code review before proceeding to post phase
```

---

## State Transitions

```
Preconditions for each transition:

INIT → PREPARED:
  ✓ /spek.prepare invoked
  ✓ Git state verified
  → Set phase="prepared", completion=0%

PREPARED → SPECIFYING:
  ✓ /spek.automate (specify) invoked
  ✓ Feature state exists
  ✓ Context loaded
  → Set phase="specifying", completion=25%

SPECIFYING → PLANNING:
  ✓ spec.md exists
  ✓ /spek.automate (plan) invoked
  → Set phase="planning", completion=50%

PLANNING → IMPLEMENTING:
  ✓ plan.md exists
  ✓ tasks.md exists
  ✓ /spek.implement invoked
  → Set phase="implementing", completion=75%

IMPLEMENTING → COMPLETING:
  ✓ Implementation complete
  ✓ /spek.post invoked
  → Set phase="completing", completion=100%

COMPLETING → DONE:
  ✓ Lessons written
  ✓ Vault updated
  ✓ Session archived
  → Archive to /memories/session/archive/
```

---

## Example: Create & Update State

```python
def create_feature_state(feature_name, feature_id):
    """Create new feature state file"""
    
    state = {
        "feature_name": feature_name,
        "feature_id": feature_id,
        "status": "initialized",
        "phase": "initialized",
        "completion": 0,
        "session_start": now_iso(),
        "session_count": 1,
    }
    
    content = to_yaml_frontmatter(state) + """
## Current Phase: Initialized

Feature state created. Ready for /spek.prepare.

## Progress by Phase

- [ ] Spec drafted (0-25%)
- [ ] Plan drafted (25-50%)
- [ ] Tasks generated (50-75%)
- [ ] Implementation complete (75-100%)

## Session Log

- Session 1: [{}] Initialized
""".format(now_iso())
    
    save_file("/memories/session/current-feature.md", content)


def update_feature_state(new_phase, completion_percent):
    """Update feature state after skill completion"""
    
    state = load_yaml_frontmatter("/memories/session/current-feature.md")
    
    # Validate transition
    assert can_transition(state["phase"], new_phase), \
        f"Cannot transition {state['phase']} → {new_phase}"
    
    # Update state
    state["phase"] = new_phase
    state["completion"] = completion_percent
    
    # Add session log entry
    append_to_file(
        "/memories/session/current-feature.md",
        f"- Session {state['session_count']}: [{now_iso()}] {new_phase}\n"
    )
    
    # Save
    save_yaml_frontmatter("/memories/session/current-feature.md", state)


def archive_feature_state(feature_name):
    """Archive completed feature state to vault"""
    
    source = "/memories/session/current-feature.md"
    destination = f"vault/sessions/{today()}-{feature_name}.md"
    
    # Move to archive
    shutil.move(source, destination)
    
    print(f"✓ Feature archived: {destination}")
```

---

## Precondition Validation

```python
def validate_preconditions(target_phase):
    """Validate that current state can transition to target phase"""
    
    state = load_feature_state()
    
    preconditions = {
        "specifying": ["prepared"],  # Must have completed prepare
        "planning": ["specifying", "spec.md"],  # spec.md must exist
        "implementing": ["planning", "plan.md", "tasks.md"],
        "completing": ["implementing"],
    }
    
    if target_phase not in preconditions:
        return True
    
    # Check all preconditions
    for precondition in preconditions[target_phase]:
        if precondition.endswith(".md"):
            # File must exist
            assert os.path.exists(precondition), \
                f"Precondition failed: {precondition} missing"
        else:
            # Phase must have completed
            assert state["phase"] >= precondition, \
                f"Precondition failed: {precondition} not complete"
    
    return True
```

---

## Related Patterns

- **Feature Lifecycle** — Phases that state tracks
- **Session-to-Vault Archival** — Archival process (final state)

---

## Where It's Used

- **Primary:** [feature-state-tracking.md](../specs/feature-state-tracking.md)
- **Created in:** [prepare-command.md](../specs/prepare-command.md)
- **Updated in:** 
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md)
  - [spek-implement-workflow.md](../specs/spek-implement-workflow.md)
  - [post-command.md](../specs/post-command.md)

---

## Quick Checklist

- [ ] State file created at feature start?
- [ ] YAML frontmatter has all fields?
- [ ] Preconditions validated before transitions?
- [ ] Completion % updated at each step?
- [ ] Session log records all work (timestamp + phase)?
- [ ] State persists across sessions?
- [ ] Archive process defined (completed → vault)?
- [ ] Multiple features can track separately?

---

## Token Cost

- **State file I/O:** ~10 tokens per write
- **Precondition validation:** ~50 tokens per transition
- **Session log:** ~5 tokens per entry

Total per feature: ~100-200 tokens (negligible overhead).
