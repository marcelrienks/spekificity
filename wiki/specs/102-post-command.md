# ATOMIC SPECIFICATION: Post Command (C4.2)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Skill — /spek.post (10-step feature completion + vault sync)  
**Depends On:** lessons-format.md, architectural-decisions.md, post-processing.md  

---

## Overview

`/spek.post` completes feature work by extracting lessons, updating vault, and syncing memory (10 steps, 5-10K tokens).

---

## Scope & Relationship

**This spec defines:**
- **ORCHESTRATION** — The 10-step sequence that `/spek.post` executes
- **INTEGRATION POINTS** — Which systems are called and in what order
- **INPUTS & OUTPUTS** — What data flows in/out of each step
- **ERROR HANDLING** — High-level error recovery for each step

**Related specs define implementation details:**
- [Post Processing](post-processing.md) provides detailed implementation for each of the 10 steps (lessons generation, vault updates, graph sync, etc.)
- [Post Command](post-command.md) (THIS SPEC) orchestrates the workflow

**Use together:**
- For *overall workflow sequence, integration points, high-level design*: Start here (post-command.md)
- For *detailed implementation of each step, error recovery details, validation*: See post-processing.md

---

## 10-Step Sequence

```
/spek.post [--caveman-mode=full|lite|ultra] [--dry-run]
├─ Step 1: Collect artifacts (spec/plan/tasks/execution trace/code changes)
├─ Step 2: Activate caveman mode for compression
├─ Step 3: Generate lessons document (vault/lessons/<date>-<feature>-<name>.md)
├─ Step 4: Update vault/decision.md (append new decisions)
├─ Step 5: Update vault/patterns.md (add/refine patterns)
├─ Step 6: Sync to /memories/repo/architectural-decisions.md
├─ Step 7: Sync to /memories/repo/patterns-index.md
├─ Step 8: Refresh code graph via /spek.map (incremental)
├─ Step 9: Archive /memories/session/current-feature.md
└─ Step 10: Report completion
```

---

## Step Details

### Step 1: Collect Artifacts
- Read /memories/session/current-feature.md (feature state)
- Read spec.md, plan.md, tasks.md (if exist)
- Collect execution trace (from /spek.implement)
- Collect code changes (git diff)
- Extract errors/warnings

**Output:** Artifacts dict

### Step 2: Activate Caveman Mode
- Parse `--caveman-mode` param (default: full)
- Load compression rules (active voice, concrete, short, specific)
- Set token budget

### Step 3: Generate Lessons
- Extract 8 sections from artifacts
- Compress with caveman mode
- Write vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md
- **Output:** Lesson file created

### Step 4-5: Update Vault Decisions + Patterns
- Extract from lessons
- De-duplicate against existing
- Append to vault/decision.md (with feature source, status=active)
- Update vault/patterns.md (First Used / Last Used / frequency)

### Steps 6-7: Sync Repo Memory
- Compress recent decisions (last 3 features)
- Write /memories/repo/architectural-decisions.md
- Create patterns index
- Write /memories/repo/patterns-index.md

### Step 8: Refresh Code Graph
- Call `/spek.map` (incremental mode)
- Update vault/graph/nodes.jsonl with new symbols
- Update edges (new calls, dependencies)

### Step 9: Archive Session Memory
- Copy /memories/session/current-feature.md to archive/
- Mark complete
- Delete from /memories/session/

### Step 10: Report
- Display completion summary
- List lessons file path
- List decisions + patterns added
- Show next steps

---

## Success Criteria

✅ Lessons extracted and compressed  
✅ Vault updated (decisions + patterns)  
✅ Repo memory synced  
✅ Code graph refreshed  
✅ Session state archived  
✅ User informed of completion  

---

## Implementation Checklist

- [ ] Implement artifact collection
- [ ] Activate caveman compression
- [ ] Generate lessons (see lessons-format.md)
- [ ] Extract + append decisions
- [ ] Extract + update patterns
- [ ] Sync repo memory
- [ ] Call /spek.map
- [ ] Archive session memory
- [ ] Report completion

---

## References

**Related Specs:**
- [lessons-format.md](lessons-format.md) — Lessons template
- [post-processing.md](post-processing.md) — Post-processing layer details
- [architectural-decisions.md](architectural-decisions.md) — Decision sync
- [patterns-library.md](patterns-library.md) — Pattern sync

**External:**
- [extracted spec /spek.post](prepare-and-post-skills.md#spekpost)
