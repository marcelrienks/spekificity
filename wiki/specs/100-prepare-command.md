# ATOMIC SPECIFICATION: Prepare Command (C4.1)

**Depends On:** context-layer.md, git-verification.md  

---

## Overview

`/spek.prepare` initializes the workspace for feature work (7 steps, ~2-5 seconds total).

---

## Execution Sequence

```
/spek.prepare [--feature-name="..."] [--skip-context] [--force-graph-refresh]
├─ Step 1: Verify git state (clean, on feature branch)
├─ Step 2: Load/determine feature name
├─ Step 3: Check code graph freshness (optional, unless forced)
├─ Step 4: Refresh code graph (conditional, if stale)
├─ Step 5: Load context via /spek.context
├─ Step 6: Create feature state tracker (vault/session/)
└─ Step 7: Report ready status
```

---

## Step Details

### Step 1: Git Verification
- Check repo exists
- Verify working dir is clean (no uncommitted changes)
- Verify on a feature branch (or main for new features)
- **Output:** Git status ✓

### Step 2: Feature Name
- Use `--feature-name` if provided
- Else extract from branch name
- Else prompt user
- **Output:** Feature name (validated)

### Step 3: Code Graph Freshness Check
- If `--force-graph-refresh`: skip to Step 4
- Else check wiki/vault/graph/config.json mtime
- If age > 1 hour: offer refresh to user
- If age < 1 hour: skip Step 4

### Step 4: Code Graph Refresh (Conditional)
- Call `/spek.map` if triggered
- Validate merged nodes.jsonl
- **Output:** Fresh graph or skipped

### Step 5: Load Context
- If `--skip-context`: reuse existing
- Else call `/spek.context` (load vault + code graph + summarize)
- **Output:** vault/session/

### Step 6: Create Feature State
- Create vault/session/
- Write: feature name, status=initialized, phase=prepared
- Add first session log entry
- **Output:** Feature state file

### Step 7: Report Status
- Display summary: git ✓, graph ✓, context loaded, ready
- Show next step: run `/spek.plan [description]`

---

## Success Criteria

✅ Git workspace verified clean  
✅ Feature name determined  
✅ Code graph checked/refreshed  
✅ Context loaded  
✅ Feature state created  
✅ Ready for /spek.plan  

---

## Implementation Checklist

- [ ] Implement git verification (Step 1)
- [ ] Implement feature name loading (Step 2)
- [ ] Implement graph freshness check (Step 3)
- [ ] Call /spek.map for refresh (Step 4)
- [ ] Call /spek.context (Step 5)
- [ ] Create feature state (Step 6)
- [ ] Report completion (Step 7)

---

## References

**Related Specs:**
- [git-verification.md](git-verification.md) — Git state validation
- [memory-architecture.md](memory-architecture.md) — Context loading and memory layers
- [feature-state-tracking.md](feature-state-tracking.md) — Feature state
- [spek-map-command.md](spek-map-command.md) — Code graph refresh

**External:**
- [extracted spec /spek.prepare](prepare-and-post-skills.md#spekprepare)