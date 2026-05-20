# HIGH-LEVEL OVERVIEW: Prepare and Post Skills

**Status:** HIGH-LEVEL OVERVIEW (2026-05-19)  
**Feature:** spekificity feature 003 — Full Workflow CLI  
**Purpose:** Entry/exit points for feature lifecycle; brackets all work with context + vault sync  
**Related:** [Detailed Prepare Spec](prepare-command.md), [Detailed Post Spec](post-command.md), [Integration Contract](speckit-integration-contract.md), [Memory Architecture](memory-architecture.md)

---

## Quick Summary

Two skills bracket every feature:

| Skill | Purpose | Timing | Cost | Output |
|-------|---------|--------|------|--------|
| **`/spek.prepare`** | Workspace init: git ✓, feature name, graph fresh?, context load | Feature start | ~5K tokens | Ready status + context loaded |
| **`/spek.post`** | Feature completion: lessons extract, vault sync, graph refresh | Feature end | ~5-10K tokens | Lessons + decisions + patterns archived |

Together they ensure **persistent memory** + **deterministic workflow** + **autonomy** (agent operates with full context).

---

## `/spek.prepare` — Quick Reference

**When:** Feature start  
**Command:** `/spek.prepare [--feature-name="..."] [--skip-context] [--force-graph-refresh]`

### 7-Step Sequence
1. Verify git state (clean + on feature branch)
2. Load/determine feature name
3. Check code graph freshness (optional unless forced)
4. Refresh graph if stale (calls `/spek.map`)
5. Load context via `/spek.context` (vault + repo memory + graph)
6. Create feature state tracker (`/memories/session/current-feature.md`)
7. Report ready status

### Common Scenarios
- **First time:** `spek.prepare` (interactive, full setup)
- **Resume after break:** `spek.prepare --skip-context` (reuse context, verify git)
- **Force fresh graph:** `spek.prepare --force-graph-refresh` (reindex all code)
- **Resume same session:** `spek.prepare --skip-context` (no-op if already prepared)

### Outputs
- ✓ Git state verified
- ✓ Feature name determined
- ✓ Code graph fresh or refreshed
- ✓ `/memories/session/context-loaded.md` (decisions, patterns, lessons)
- ✓ `/memories/session/current-feature.md` (feature state tracker)
- ✓ Ready for `/spek.automate`

**→ [Detailed Prepare Spec](prepare-command.md) for full step-by-step definitions**

---

## `/spek.post` — Quick Reference

**When:** Feature complete  
**Command:** `/spek.post [--caveman-mode=lite|full|ultra] [--dry-run]`

### 10-Step Sequence
1. Collect artifacts (spec, plan, tasks, code changes, execution trace)
2. Activate caveman mode for compression
3. Generate lessons document (vault/lessons/<date>-<feature>-<name>.md)
4. Update vault/decision.md (append new architectural decisions)
5. Update vault/patterns.md (add/refine reusable patterns)
6. Sync to /memories/repo/architectural-decisions.md (compressed cache)
7. Sync to /memories/repo/patterns-index.md (index)
8. Refresh code graph via `/spek.map` (incremental sync)
9. Archive `/memories/session/current-feature.md`
10. Report completion + next steps

### Common Scenarios
- **Normal:** `spek.post` (default caveman full mode)
- **Verbose lessons:** `spek.post --caveman-mode=lite` (less compression)
- **Ultra-compressed:** `spek.post --caveman-mode=ultra` (extreme compression)
- **Test run:** `spek.post --dry-run` (preview changes, don't write)

### Outputs
- ✓ `vault/lessons/<date>-<feature>.md` (self-contained lesson document)
- ✓ `vault/decision.md` updated (new decisions archived)
- ✓ `vault/patterns.md` updated (patterns refined)
- ✓ `/memories/repo/architectural-decisions.md` synced
- ✓ `/memories/repo/patterns-index.md` synced
- ✓ Code graph refreshed (includes lesson files)
- ✓ Session memory archived
- ✓ Ready for next feature (richer context)

**→ [Detailed Post Spec](post-command.md) for full step-by-step definitions**

---

## Key Integration Points

| Component | Called By | Calls | Purpose |
|-----------|-----------|-------|---------|
| `/spek.prepare` | User (session start) | `/spek.context`, `/spek.map` | Initialize workspace + context |
| `/spek.post` | User (feature end) | `/spek.map`, vault sync | Persist outcomes + prepare for next feature |
| `/spek.context` | `/spek.prepare` | Vault, repo memory, code graph | Load all relevant knowledge |
| `/spek.map` | `/spek.prepare`, `/spek.post` | graphify, Obsidian export | Index code + docs |
| Feature State | `/spek.prepare` (write), all workflows (read) | — | Track progress throughout feature |
| Vault | `/spek.post` (write), `/spek.context` (read) | — | Persist decisions, patterns, lessons |

---

## Success Criteria (Feature Lifecycle)

**Prepare success:** Workspace clean, context loaded, feature state initialized, ready for `/spek.automate`

**Post success:** Lessons extracted + archived, vault updated, repo memory synced, graph refreshed, session cleared

---

## Error Handling

Both skills include error handling for common failures:
- **Git errors** (not a repo, dirty working tree) → Report + guide user
- **Graph errors** (corrupted graph, export fails) → Log error, continue with stale graph
- **Context errors** (vault not found, empty context) → Log warning, continue
- **File write errors** (permission denied, disk full) → Try alternative location

**→ [Error Handling & Recovery Spec](error-handling-and-recovery.md) for cross-cutting error strategy**

---

## Dependencies & Related Specs

**Prepare depends on:**
- [Git Verification](git-verification.md) — Workspace state validation
- [Context Layer](context-layer.md) — Context injection
- [/spek.map Command](spek-map-command.md) — Graph refresh
- [Memory Architecture](memory-architecture.md) — Feature state tracking + session memory

**Post depends on:**
- [Lessons Format](lessons-format.md) — Lesson document template
- [Architectural Decisions](architectural-decisions.md) — Decision archival
- [Patterns Library](patterns-library.md) — Pattern refinement
- [Post Processing](post-processing.md) — Detailed post-feature workflow
- [Feature State Tracking](feature-state-tracking.md) — Feature state archive

**Both integrate with:**
- [Speckit Integration Contract](speckit-integration-contract.md) — How they fit into speckit workflow
- [Memory Architecture](memory-architecture.md) — 3-layer memory model + context loading

---

## Lifecycle Diagram

```
Session Start
    ↓
/spek.prepare (7 steps)
    ├── Git ✓
    ├── Feature name
    ├── Graph check/refresh
    ├── Context load (vault, repo memory, code graph)
    ├── Feature state init
    └── Ready
    ↓
User runs: /spek.automate, reviews outputs, then /spek.implement
    ↓
Feature Complete
    ↓
/spek.post (10 steps)
    ├── Collect artifacts
    ├── Generate lessons (caveman compressed)
    ├── Update vault (decisions, patterns)
    ├── Sync repo memory
    ├── Refresh code graph
    ├── Archive session state
    └── Ready for next feature (enriched context)
    ↓
Session End (or continue to next feature)
```

---

## Final Notes

This is a **high-level overview** of prepare and post skills. For detailed execution steps, error handling, and implementation details, consult the related specs listed above.

For implementation reference:
- [Detailed Prepare Spec](prepare-command.md) — Full 7-step sequence
- [Detailed Post Spec](post-command.md) — Full 10-step sequence  
- [Error Handling & Recovery](error-handling-and-recovery.md) — Cross-cutting error strategy
