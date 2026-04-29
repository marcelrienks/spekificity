# Workflow: Map Refresh

## Purpose

Guide for when and how to refresh the Graphify → Obsidian vault graph using the `/map-codebase` skill. A stale graph means AI agents may miss recently added files or reference deleted nodes — refreshing keeps context accurate.

> **Token efficiency tip**: Activate `/caveman lite` before starting this workflow to compress AI confirmation messages without losing step accuracy.

## Prerequisites

- Spekificity initialised (see [init-workflow.md](init-workflow.md))
- Graphify installed (`graphify --version` succeeds)
- Project root contains source files and/or `vault/`

---

## When to Refresh

### Always refresh before:
- Starting a new SpecKit feature lifecycle (before `/speckit-enrich-specify`)
- Running `/speckit-enrich-plan` (plan must reference current graph nodes)
- Returning to a project after a break of >1 day

### Refresh after:
- Adding or deleting source files or documentation
- Completing a feature implementation (covered automatically by `/speckit-enrich-implement`)
- Significant refactoring (file renames, directory restructuring)
- Merging a large pull request

### No refresh needed when:
- Only comments or docstrings changed (AST structure unchanged)
- Changes are limited to configuration files already in the graph
- Starting a new AI session on an already-mapped project with no recent code changes

---

## How to Refresh

### Standard (incremental) refresh

In your AI chat session:
```
/map-codebase
```

Graphify diffs the AST and updates only changed or new nodes. Existing unchanged nodes are preserved. Fast — suitable for routine refreshes.

### Full regeneration

```
/map-codebase --full
```

Regenerates the entire graph from scratch. Use after:
- Major refactors where file paths changed
- The incremental refresh produced an incorrect graph
- Upgrading Graphify to a new major version

---

## Incremental vs Full — Decision Guide

| Situation | Recommended |
|-----------|-------------|
| Added 1–10 files | `/map-codebase` (incremental) |
| Deleted files | `/map-codebase` (Graphify removes deprecated nodes) |
| Renamed files or directories | `/map-codebase --full` |
| Changed >30% of codebase | `/map-codebase --full` |
| Graphify upgraded (major version) | `/map-codebase --full` |
| First map run on a project | `/map-codebase` (Graphify treats all nodes as new) |

---

## Vault Size Guidance

| Node count | Recommendation |
|------------|---------------|
| < 100 | Commit entire `vault/graph/` including `nodes/` |
| 100–500 | Commit `vault/graph/index.md` and `vault/graph/GRAPH_REPORT.md`; optionally commit `nodes/` |
| > 500 | Add `vault/graph/nodes/` to `.gitignore`; commit only `index.md` and `GRAPH_REPORT.md` |
| > 5000 | Consider also gitignoring `vault/graph/graph.json` and `vault/graph/graph.html` |

To gitignore nodes at scale, add to `.gitignore`:
```
vault/graph/nodes/
vault/graph/graph.json
vault/graph/graph.html
```

---

## Expected Final State

After a successful refresh:
- `vault/graph/index.md` — updated with current timestamp and node count
- `vault/graph/nodes/` — contains one `.md` file per source file/document in the project
- `vault/graph/GRAPH_REPORT.md` — updated with current god nodes and graph summary
- AI sessions started with `/context-load` will load the refreshed index automatically

---

## On Failure

- **Graphify error**: See error handling in [skills/map-codebase/SKILL.md](../skills/map-codebase/SKILL.md)
- **Stale graph suspected**: Run `/map-codebase --full` to force complete regeneration
- **Vault missing**: Run the full init workflow from Step 5 — see [init-workflow.md](init-workflow.md)
