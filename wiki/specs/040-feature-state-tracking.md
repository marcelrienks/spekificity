# ATOMIC SPECIFICATION: Feature State Tracking (C4.4)



**Depends On:** memory-architecture.md  
**Used By:** /spek.prepare (create), /spek.conclude (update), all commands (read)  

---


## Overview

Feature state tracks progress through feature lifecycle (initialized → specifying → planning → implementing → completing).

---


## Success Criteria

- ✅ State accurately reflects current phase (transitions valid + timely)
- ✅ Progress updated at each step (phase marker advanced)
- ✅ Session log tracks all work (every command logs entry + timestamp)
- ✅ Transitions are valid (no skip phases, linear progression)
- ✅ State file readable by all commands (consistent YAML format)
- ✅ Archive process preserves history (old features remain available for reference)
- ✅ Feature state survives session interruption (persisted to disk)
- ## Update Triggers
- **Create:** /spek.prepare (Step 6)
- New feature file with initialized status
- **Update:** Each command completion
- /spek.plan specify phase → specifying (25%)
- /spek.plan plan phase → planning (50%)
- /spek.implement → implementing (75%)
- /spek.conclude → completing (100%)
- **Archive:** /spek.conclude (Step 9)
- Move to vault/session/archive/
- Keep for post-mortem reference
- ## Success Criteria
- ✅ State accurately reflects current phase
- ✅ Completion % updated
- ✅ Session log tracks all work
- ✅ Transitions are valid
- ## Implementation Checklist
- [ ] Create YAML frontmatter template
- [ ] Define phase transitions
- [ ] Implement state updates in each command
- [ ] Validate state integrity
- [ ] Archive on completion
- ## References
- **Related Specs:**
- [memory-architecture.md](030-memory-architecture.md) — Session memory structure
- [100-prepare-command.md](100-prepare-command.md) — State creation (Step 6)
- [102-conclude-command.md](102-conclude-command.md) — State archival (Step 9)
- **External:**
- [extracted spec Feature State Tracking](prepare-and-post-skills.md)


## State File: vault/session/


## YAML Frontmatter

```yaml
---
feature_name: "spek-full-workflow-cli"
feature_id: "003"
session_start: "2026-05-19T10:00:00Z"
  session_count: 1
  phase: "prepared | specifying | planning | implementing | completing"
  completion: progress-indicator
---
```


## Markdown Sections

```markdown

## Current Phase: [Prepared|Specifying|Planning|Implementing|Completing]


## Progress by Phase
- [ ] Spec drafted
- [ ] Plan drafted
- [ ] Tasks generated
- [ ] Implementation complete


## Progress Markers
- Prepared
- Specifying
- Planning
- Implementing


## Session Log
- Session 1: [timestamp] Prepared, loaded context
- Session 2: [timestamp] Specified, generated spec
- Session 3: [timestamp] Planned, created plan
```

---


## State Transitions

```
initialized
  ↓
prepare: prepared
  ↓
specify: specifying
  ↓
plan: planning
  ↓
implement: implementing
  ↓
post: completing
```

