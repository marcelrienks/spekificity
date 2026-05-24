# ATOMIC SPECIFICATION: Conclude-Processing (C3.6)

**Depends On:** lessons-format.md, architectural-decisions.md, patterns-library.md  

---

## Overview

`/spek.conclude` extracts lessons from completed feature work, updates vault with decisions and patterns, syncs repo memory, and archives session state.

---

## Scope & Relationship

**This spec defines:**
- **IMPLEMENTATION DETAILS** — How each of the 10 conclude-feature steps are executed
- **ERROR HANDLING** — Detailed error recovery for vault writes, file I/O, graph sync failures
- **VALIDATION** — Success criteria for each step (what makes a step succeed vs. fail)
- **INTEGRATION** — Detailed integration points (vault file formats, repo memory structure, graph refresh)

**Related specs define orchestration and high-level design:**
- [Conclude Command](conclude-command.md) orchestrates the workflow and defines the 10-step sequence
- [Conclude Processing](conclude-processing.md) (THIS SPEC) provides implementation details for each step

**Use together:**
- For *overall workflow sequence, integration points*: Start with conclude-command.md
- For *implementation details, error recovery, validation*: Consult this spec (conclude-processing.md)

---

## Execution Sequence

```
/spek.conclude
├─ Step 1: Collect artifacts
│  ├─ Read spec/plan/tasks/execution trace
│  ├─ Gather code changes (git diff)
│  └─ Compile feature artifacts
├─ Step 2: Activate caveman mode
│  ├─ Set compression mode (full, lite, ultra)
│  └─ Load compression rules
├─ Step 3: Generate lessons
│  ├─ Extract: What Built, How Built, Tasks, Decisions, Patterns, Lessons, Metrics
│  ├─ Write vault/lessons/<date>-<feature>-<name>.md
│  └─ Compress with caveman mode
├─ Step 4: Update vault
│  ├─ Append decisions → vault/decision.md
│  ├─ Refine patterns → vault/patterns.md
│  └─ Mark lessons complete
├─ Step 5: Sync repo memory
│  ├─ Compress recent decisions → vault/repo/architectural-decisions.md
│  ├─ Update patterns index → vault/repo/patterns-index.md
│  └─ Update codebase map → vault/repo/codebase-map.md
├─ Step 6: Refresh code graph
│  └─ /spek.map (incremental sync of changed files)
├─ Step 7: Archive session memory
│  └─ Archive vault/session/
└─ Step 8: Report completion
   └─ "Feature complete. Lessons written. Vault updated."
```

---

## Step Details

### Steps 1-3: Collect + Generate Lessons

See [lessons-format.md](lessons-format.md) and [conclude-command.md](conclude-command.md) for detailed specs.

### Step 4: Update Vault

**Decision Update:**
1. Extract decisions from lessons
2. De-duplicate (check vault/decision.md for existing)
3. Append new decisions with feature source
4. Mark status as "active"

**Pattern Update:**
1. Extract patterns from lessons
2. Check vault/patterns.md for existing patterns
3. If new: Add with "First Used" = current feature
4. If existing: Update "Last Used" + increment frequency

### Step 5: Sync Repo Memory

**Decisions Sync:**
1. Read vault/decision.md (all active decisions)
2. Filter to last 3 features
3. Compress each decision (1-2 sentences)
4. Create summary table
5. Write vault/repo/architectural-decisions.md

**Patterns Sync:**
1. Read vault/patterns.md
2. Sort by frequency (most used first)
3. Keep top 10-15 recent patterns
4. Write vault/repo/patterns-index.md

**Codebase Map:**
1. If code structure changed significantly
2. Run `git diff --stat` (identify affected files)
3. Update vault/repo/codebase-map.md
4. Mark changes + timestamp

### Step 6: Refresh Code Graph

**Process:**
- Call `/spek.map` (incremental mode)
- Re-index only changed files (fast)
- Update vault/graph/nodes.jsonl with new nodes
- Update edges (new function calls, dependencies)

**Benefit:** Graph stays fresh without full rebuild

### Step 7: Archive Session Memory

**Archive vault/session/:**
1. Copy to vault/session/archive/<date>-<feature>.md (for reference)
2. Delete from vault/session/ (ephemeral cleanup)
3. Note: vault/lessons/ contains permanent record

### Step 8: Report Completion

**Report:**
```
✓ Feature Complete
├─ Lessons: vault/lessons/2026-05-19-003-*.md
├─ Decisions: 2 new, appended to vault/decision.md
├─ Patterns: 3 updated, 1 new in vault/patterns.md
├─ Code graph: refreshed (vault/graph/nodes.jsonl)
├─ Repo memory: synced (vault/repo/)
└─ Session archived: vault/session/archive/
```

---

## Success Criteria

- ✅ All 10 steps complete in <30 seconds (fast execution)
- ✅ Lessons extracted + compressed (caveman mode applied)
- ✅ Vault updated (decisions + patterns appended correctly)
- ✅ Repo memory synced (compressed cache updated)
- ✅ Code graph refreshed (incremental sync completes)
- ✅ Session state archived (ephemeral memory cleaned up)
- ✅ User informed of all changes (completion report clear + actionable)

---

## Error Handling

**If any step fails:**
- Log error
- Continue to next step (don't fail midway)
- Report which steps succeeded/failed

**Fallback:**
- If vault write fails → Archive to temp location + suggest manual move
- If lessons generation fails → Report error, offer retry
- If graph sync fails → Report warning, use last-known state

---

## Success Criteria

✅ Lessons extracted and written to vault  
✅ Decisions de-duplicated and appended  
✅ Patterns updated with frequency  
✅ Repo memory synced (recent decisions + patterns)  
✅ Code graph refreshed (incremental)  
✅ Session state archived  
✅ Completion reported to user  

---

## Implementation Checklist

- [ ] Collect feature artifacts
- [ ] Generate lessons using lessons-format
- [ ] Extract + append decisions to vault/decision.md
- [ ] Update patterns in vault/patterns.md
- [ ] Sync to vault/repo/ (decisions + patterns)
- [ ] Call /spek.map (incremental sync)
- [ ] Archive vault/session/
- [ ] Report completion

---

## References

**Related Specs:**
- [lessons-format.md](lessons-format.md) — Lessons template
- [architectural-decisions.md](architectural-decisions.md) — Decisions structure
- [patterns-library.md](patterns-library.md) — Patterns structure
- [conclude-command.md](conclude-command.md) — Full /spek.conclude spec
- [spek-map-command.md](spek-map-command.md) — Code graph refresh

**External:**
- [extracted spec Layer 3](speckit-integration-contract.md#layer-3-conclude-processing-layer-spekconclude)