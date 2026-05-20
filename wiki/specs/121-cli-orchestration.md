# SPECIFICATION: CLI Orchestration (C2.0)

**Status:** ATOMIC SPECIFICATION  
**Type:** Workflow Orchestration — Command-Line Interface and Workflow Sequencing  
**Version:** 2026-05-19  
**Depends On:** speckit-integration-contract.md, prepare-command.md, post-command.md, feature-state-tracking.md  

---

## Overview

The CLI is the user-facing entry point to Spekificity. `spek plan` is the primary orchestration command for pre-implementation flow, `spek implement` is the primary execution command after review, and support commands such as `spek prepare`, `spek context`, `spek map`, `spek post`, and `spek lessons` remain user-facing while also being callable internally when needed.

**Scope:**
- Entry points and command routing
- Workflow sequencing (required order of operations)
- Flag/parameter handling
- Feature state machine (tracking which skills have been run)
- Exit codes and status reporting
- Lifecycle integration with SpecKit

---

## Entry Points

### Command: `spek`

**Base command for all Spekificity operations.**

```bash
spek [global-options] <command> [command-options]
```

**Global Options:**
```bash
--workspace <path>       # Override workspace root (default: git root)
--vault <path>           # Override vault location (default: wiki/vault/)
--dry-run                # Preview changes, don't write (applies to all commands)
--verbose                # Enable verbose logging (debug output)
--caveman-mode <mode>    # Force caveman compression mode (lite|full|ultra)
--help, -h               # Show help
--version, -v            # Show version
```

**Return:** Exit code (0=success, 1=error, 2=validation error, 3=user action required)

---

## Command Reference

### 1. `spek prepare` — Start Feature

**Purpose:** Initialize workspace and load context for a new feature.

```bash
spek prepare [options]
  --feature-name <name>        # Feature name/identifier (interactive if not provided)
  --skip-context               # Skip context loading (assume already loaded)
  --force-graph-refresh        # Force code graph rebuild
  --auto                       # Non-interactive (use defaults)
```

**Behavior:**
1. Validate git state (clean repo, on feature branch)
2. Determine feature name (interactive or from `--feature-name`)
3. Check code graph freshness (refresh if stale, unless `--skip-context`)
4. Load context via `/spek.context`
5. Create feature state file (`/memories/session/current-feature.md`)
6. Write ready status to feature state

**Output:**
- Feature state initialized
- Context loaded and available
- Ready for `/spek.plan`

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [Prepare Command](prepare-command.md)

---

### 2. `spek plan` — Orchestrate SpecKit Workflow

**Purpose:** Orchestrate the pre-implementation workflow from feature description through approved task list.

```bash
spek plan [options]
  --feature-name <name>       # Feature name (auto-loaded from feature state if omitted)
  --description <text>        # Feature description (interactive if not provided)
  --dry-run                   # Preview spec, don't write
```

**Behavior:**
1. Validate feature state exists (must run `/spek.prepare` first)
2. Get feature description (interactive or from `--description`)
3. Load or refresh project context required for orchestration
4. Call `/speckit.specify`
5. Call `/speckit.clarify` if needed
6. Call `/speckit.plan`
7. Call `/speckit.analyze` and surface findings

## Success Criteria

- ✅ All CLI commands execute without crashing (robust error handling)
- ✅ Feature state tracked correctly (phase transitions accurate)
- ✅ Workflow sequencing enforced (can't skip required steps)
- ✅ Parameters validated (clear errors for invalid flags/args)
- ✅ Exit codes correct (0=success, 1=error, 2=validation, 3=user-action)
- ✅ Help + version work (`--help`, `--version` flags)
- ✅ Integration seamless (users think in workflow, not technical layers)
8. Support in-place remediation loop when findings require changes
9. Call `/speckit.tasks`
10. Update feature state (`current-feature.md`)

**Output:**
- `specs/spec.md` created/updated
- `specs/plan.md` created/updated
- `specs/tasks.md` created/updated
- Feature state updated (automation complete)
- Ready for `/spek.implement`

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [Speckit Integration Contract](speckit-integration-contract.md), [spek.plan Workflow](spek-plan-workflow.md)

---

### 3. `spek implement` — Execute Tasks

**Purpose:** Execute implementation tasks from task list.

```bash
spek implement [options]
  --dry-run                   # Preview changes, don't write
  --tasks <list>              # Specific tasks to run (e.g., "1,3,5")
  --skip-tests                # Skip test execution
```

**Behavior:**
1. Validate feature state, spec, plan, and tasks exist
2. Call `/speckit.implement` to execute tasks
3. Log execution trace (all commands, outputs, timing)
4. Update feature state (mark tasks complete, capture trace)

**Output:**
- Tasks executed
- Execution trace logged
- Code changes recorded
- Feature state updated (implement complete)
- Ready for `/spek.post`

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [Speckit Integration Contract](speckit-integration-contract.md), [Enrichment Layer](enrichment-layer.md)

---

### 4. `spek post` — Archive and Persist

**Purpose:** Extract lessons, update vault, archive feature state.

```bash
spek post [options]
  --caveman-mode <mode>       # Compression level (lite|full|ultra)
  --dry-run                   # Preview changes, don't write
```

**Behavior:**
1. Validate feature state complete (all prior steps done)
2. Extract lessons from artifacts (spec, plan, tasks, code, trace)
3. Update vault (decisions, patterns)
4. Sync repo memory (`/memories/repo/`)
5. Refresh code graph via `/spek.map`
6. Archive feature state
7. Report completion

**Output:**
- `wiki/vault/lessons/<date>-<feature>.md` created
- `wiki/vault/decision.md` updated
- `wiki/vault/patterns.md` updated
- `/memories/repo/` synced
- Code graph refreshed
- Session memory archived
- Ready for next feature

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [Post Command](post-command.md), [Post Processing](post-processing.md)

---

### 5. `spek map` — Refresh Code Graph

**Purpose:** Generate or update code graph (code + documentation index).

```bash
spek map [options]
  --force                     # Force full rebuild (don't use cache)
  --incremental               # Incremental sync (only changed files)
  --dry-run                   # Preview changes, don't write
```

**Behavior:**
1. Run graphify to index code symbols
2. Export Obsidian document nodes
3. Merge code + doc nodes
4. Write to `wiki/vault/graph/nodes.jsonl`
5. Update graph metadata (`wiki/vault/graph/config.json`)

**Output:**
- `wiki/vault/graph/nodes.jsonl` created/updated
- `wiki/vault/graph/config.json` created/updated
- Context available for refreshing

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [/spek.map Command](spek-map-command.md)

---

### 6. `spek context` — Load Context

**Purpose:** Load vault decisions, patterns, lessons, and code graph into session memory.

```bash
spek context [options]
  --force                     # Reload context (don't use cache)
  --minimal                   # Load minimal context (code graph only)
```

**Behavior:**
1. Load decisions from `wiki/vault/decision.md` (or cache)
2. Load patterns from `wiki/vault/patterns.md` (or cache)
3. Load recent lessons (top 3-5) from `wiki/vault/lessons/`
4. Load code graph from `wiki/vault/graph/nodes.jsonl`
5. Compose into session context (`/memories/session/context-loaded.md`)

**Output:**
- `/memories/session/context-loaded.md` created
- Full context available for skills

**Error Handling:** Per [error-handling-and-recovery.md](error-handling-and-recovery.md)

**Related:** [Context Layer](context-layer.md), [Memory Architecture](memory-architecture.md)

---

## Feature State Machine

**State tracking via `/memories/session/current-feature.md`:**

```
[IDLE] → /spek.prepare → [PREPARED]
[PREPARED] → /spek.plan → [TASKED]
[TASKED] → /spek.implement → [IMPLEMENTED]
[IMPLEMENTED] → /spek.post → [ARCHIVED]
[ARCHIVED] → (ready for next feature)

Or: [ANY_STATE] --skip-context--> [ANY_STATE] (reuse context within session)
Or: [ANY_STATE] --force-graph-refresh--> re-run /spek.map, continue
```

**State File Format (`/memories/session/current-feature.md`):**

```markdown
# Current Feature State

**Feature:** feature-003-spek-workflow-cli  
**Date:** 2026-05-19  
**Status:** IMPLEMENTED  
**Last Updated:** 2026-05-19 15:30:22 UTC  

## Workflow Progress

| Step | Command | Status | Timestamp | Output |
|------|---------|--------|-----------|--------|
| 1 | /spek.prepare | ✓ COMPLETE | 2026-05-19 10:00:15 | Context loaded |
| 2 | /spek.plan | ✓ COMPLETE | 2026-05-19 10:18:30 | spec.md, plan.md, tasks.md |
| 3 | /spek.implement | ✓ COMPLETE | 2026-05-19 15:30:22 | 24 files modified, 1200 lines added |
| 4 | /spek.post | ⏳ PENDING | — | Ready to run |

## Artifacts

- Spec: specs/spec.md (234 lines)
- Plan: specs/plan.md (412 lines)
- Tasks: specs/tasks.md (8 tasks)
- Code changes: 24 files, 1200 lines added, 340 removed

## Context Status

- Context loaded: 2026-05-19 10:00:15 (age: 5.5h)
- Graph version: 2026-05-19 08:30:00 (age: 7h)
- Vault accessible: ✓ YES
```

---

## Exit Codes

| Code | Meaning | User Action |
|------|---------|-------------|
| **0** | Success | None (continue to next step) |
| **1** | Error (recoverable) | Check logs, run command again |
| **2** | Validation error | Fix input parameters, retry |
| **3** | User action required | Follow guidance in error message, then retry |
| **127** | Command not found | Check spek installation |

**Example Exit Sequences:**

- `spek prepare` → Exit 0 → User runs `spek specify` → Exit 0 → Continue
- `spek prepare` → Exit 3 (git dirty) → User runs `git add .` → User runs `spek prepare` → Exit 0
- `spek specify` → Exit 1 (speckit error) → Run `spek specify` again (retry) → Exit 0

---

## Workflow Sequencing Rules

**Rule 1: Strict Ordering (Most Strict)**
```
Must run in order: prepare → specify → plan → tasks → implement → post
Cannot skip steps. Must complete each before proceeding.
```

**Rule 2: Resume Within Session (Flexible)**
```
If restarting within same session: Can re-run prepare with --skip-context (avoid context reload)
Example: /spek.prepare → specify → plan → (pause) → prepare --skip-context → plan → tasks
```

**Rule 3: Anytime Map (Flexible)**
```
Can run /spek.map anytime (doesn't affect feature state)
Use to refresh code graph without blocking feature work
```

**Rule 4: Manual Context Override (Flexible)**
```
Can run /spek.context --force to reload context mid-feature
Use if vault was updated externally or context feels stale
```

**Rule 5: Dry-Run Validation (No-Op)**
```
All commands support --dry-run: Preview changes without writing
Use to test workflow or validate parameters before commit
```

---

## Integration with SpecKit

**Orchestration Boundary:**
- Spekificity CLI calls SpecKit commands but **does not modify** SpecKit behavior
- SpecKit defines spec/plan/tasks/implement logic
- Spekificity CLI adds: context injection, vault persistence, graph management, lesson extraction

**Command Flow:**
```
User: spek specify --description "..."
  ↓
Spekificity CLI:
  ├─ Load context from vault + repo memory + graph
  ├─ Call /speckit.specify with (context + description)
  ├─ Receive spec.md from SpecKit
  ├─ Write spec.md to workspace
  └─ Update feature state
```

**For details:** [Speckit Integration Contract](speckit-integration-contract.md)

---

## Status Reporting

**On Success:**
```
✓ /spek.prepare complete
  - Workspace: /Users/.../spekificity
  - Feature: 003-spek-full-workflow-cli
  - Context loaded: 5 decisions, 8 patterns, 2 recent lessons, 3421 code symbols
  - Ready for: spek specify
```

**On Error:**
```
✗ /spek.prepare failed
  Error: Git working tree is dirty
  Unstaged: src/main.py, src/utils.py
  
  Fix: git add . && git commit -m "checkpoint"
  Then: spek prepare
  
  (Exit code: 3)
```

**On Warning (Recoverable):**
```
⚠ /spek.post warning
  Vault not accessible (permissions): Using cached decisions (2h old)
  
  Tip: Check vault permissions: chmod 755 wiki/vault/
  
  Continuing: Feature archival with stale context
  (Exit code: 0, proceeding)
```

---

## Configuration

**Config file:** `.spekificity/config.yaml`

```yaml
workspace:
  root: ${PWD}  # Git root of project
  vault: wiki/vault/
  specs: specs/
  
memory:
  repo: /memories/repo/
  session: /memories/session/
  
graph:
  cache_dir: wiki/vault/graph/
  refresh_interval_hours: 24
  force_refresh_on_prepare: false
  
speckit:
  timeout_seconds: 300
  verbose: false
  
caveman:
  default_mode: full
  enabled: true
  
error:
  log_file: .cel/error-log.md
  retry_transient_errors: true
  retry_backoff_seconds: [10, 30, 60]
```

---

## Testing & Validation

**CLI Integration Tests:**

- [ ] Test 1: Full happy path (prepare → specify → plan → tasks → implement → post)
- [ ] Test 2: Resume within session (`prepare --skip-context`)
- [ ] Test 3: Force graph refresh (`prepare --force-graph-refresh`)
- [ ] Test 4: Dry-run all commands (preview changes, don't write)
- [ ] Test 5: Invalid feature state (e.g., try `specify` without `prepare`) → Fail + guidance
- [ ] Test 6: SpecKit timeout → Retry + eventual success
- [ ] Test 7: Vault inaccessible → Fallback + warning
- [ ] Test 8: Exit codes match expected values

**Feature State Tests:**

- [ ] Feature state created after `/spek.prepare`
- [ ] Feature state transitions correctly (IDLE → PREPARED → ... → ARCHIVED)
- [ ] Feature state survives session restart (when archive incomplete)
- [ ] Feature state correctly reflects command status

**Parameter Tests:**

- [ ] `--feature-name` override works
- [ ] `--dry-run` prevents file writes
- [ ] `--verbose` enables debug logging
- [ ] Global `--workspace` override works

---

## Final Notes

This spec defines the **CLI orchestration layer** — the user-facing command interface and workflow sequencing. Implementation details for individual commands (e.g., 7 steps of `prepare`) are in dedicated command specs.

**Implementation Reference:**
- [Prepare Command](prepare-command.md) — 7-step detail
- [Post Command](post-command.md) — 10-step detail
- [Speckit Integration Contract](speckit-integration-contract.md) — Integration details
- [Error Handling and Recovery](error-handling-and-recovery.md) — Error strategy
