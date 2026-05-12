# workflow: map refresh

## purpose

guide for when and how to refresh the graphify → obsidian vault graph using the `/map-codebase` skill. a stale graph means ai agents may miss recently added files or reference deleted nodes — refreshing keeps context accurate.

> **token efficiency tip**: activate `/caveman lite` before starting this workflow to compress ai confirmation messages without losing step accuracy.

## prerequisites

- spekificity initialised (see [init-workflow.md](init-workflow.md))
- graphify installed (`graphify --version` succeeds)
- project root contains source files and/or `vault/`

---

## when to refresh

### always refresh before:
- starting a new speckit feature lifecycle (before `/speckit-enrich-specify`)
- running `/speckit-enrich-plan` (plan must reference current graph nodes)
- returning to a project after a break of >1 day

### refresh after:
- adding or deleting source files or documentation
- completing a feature implementation (covered automatically by `/speckit-enrich-implement`)
- significant refactoring (file renames, directory restructuring)
- merging a large pull request

### no refresh needed when:
- only comments or docstrings changed (ast structure unchanged)
- changes are limited to configuration files already in the graph
- starting a new ai session on an already-mapped project with no recent code changes

---

## how to refresh

### standard (incremental) refresh

in your ai chat session:
```
/map-codebase
```

graphify diffs the ast and updates only changed or new nodes. existing unchanged nodes are preserved. fast — suitable for routine refreshes.

### full regeneration

```
/map-codebase --full
```

regenerates the entire graph from scratch. use after:
- major refactors where file paths changed
- the incremental refresh produced an incorrect graph
- upgrading graphify to a new major version

---

## incremental vs full — decision guide

| situation | recommended |
|-----------|-------------|
| added 1–10 files | `/map-codebase` (incremental) |
| deleted files | `/map-codebase` (graphify removes deprecated nodes) |
| renamed files or directories | `/map-codebase --full` |
| changed >30% of codebase | `/map-codebase --full` |
| graphify upgraded (major version) | `/map-codebase --full` |
| first map run on a project | `/map-codebase` (graphify treats all nodes as new) |

---

## vault size guidance

| node count | recommendation |
|------------|---------------|
| < 100 | commit entire `vault/graph/` including `nodes/` |
| 100–500 | commit `vault/graph/index.md` and `vault/graph/graph_report.md`; optionally commit `nodes/` |
| > 500 | add `vault/graph/nodes/` to `.gitignore`; commit only `index.md` and `graph_report.md` |
| > 5000 | consider also gitignoring `vault/graph/graph.json` and `vault/graph/graph.html` |

to gitignore nodes at scale, add to `.gitignore`:
```
vault/graph/nodes/
vault/graph/graph.json
vault/graph/graph.html
```

---

## expected final state

after a successful refresh:
- `vault/graph/index.md` — updated with current timestamp and node count
- `vault/graph/nodes/` — contains one `.md` file per source file/document in the project
- `vault/graph/graph_report.md` — updated with current god nodes and graph summary
- ai sessions started with `/context-load` will load the refreshed index automatically

---

## on failure

- **graphify error**: see error handling in [skills/map-codebase/skill.md](../skills/map-codebase/skill.md)
- **stale graph suspected**: run `/map-codebase --full` to force complete regeneration
- **vault missing**: run the full init workflow from step 5 — see [init-workflow.md](init-workflow.md)
