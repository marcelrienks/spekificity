# map codebase

## description

builds or refreshes a graphify-generated graph of the current project and stores it as an obsidian vault at `vault/graph/`. the resulting vault index (`vault/graph/index.md`) becomes the primary context source for all subsequent ai agent sessions — enabling cross-cutting queries without exhaustively scanning source files.

this skill is the entry point to the spekificity context system. run it once after initialisation, and again whenever the codebase changes significantly.

## trigger

invoked by the developer in the ai chat session:
```
/map-codebase
```

optional flags:
```
/map-codebase --full          ← force full regeneration (bypass incremental diff)
/map-codebase --incremental   ← explicit incremental mode (default when graph exists)
/map-codebase --state <state> ← hint current graph state: fresh | stale | absent
```

## prerequisites

- spekificity initialisation complete (see [workflows/init-workflow.md](../../workflows/init-workflow.md))
- `graphify --version` returns a version ≥ 0.5.5 (see [setup-guides/graphify-setup.md](../../setup-guides/graphify-setup.md))
- current working directory is the project root (where `vault/` lives or will be created)
- write permissions on the project root

## inputs

| input | description | required |
|-------|-------------|----------|
| `--full` flag | force full graph regeneration instead of incremental diff | no |
| `--incremental` flag | explicit incremental mode — only processes changed files since last run | no |
| `--state <state>` | pre-computed graph staleness hint: `fresh`, `stale`, or `absent` (from `compute_graph_state()`) | no |
| `claude_api_key` env var | enables semantic extraction of markdown docs and comments (beyond ast) | no |

## steps

1. **verify graphify is installed**:
   ```bash
   graphify --version
   ```
   if this fails, print: "graphify is not installed. follow setup-guides/graphify-setup.md then retry." and stop.

2. **confirm project root**: verify `vault/` or at least one of `skills/`, `workflows/`, `specs/`, or a recognisable project file (`.specify/`, `readme.md`, `package.json`, etc.) exists in the current directory. if not, warn: "run /map-codebase from the project root."

3. **run graphify** — prefix all graphify output with `[graphify]` tag:
   - incremental (default when `vault/graph/index.md` exists and `--full` not passed):
     ```bash
     graphify . --obsidian --output vault/graph/ 2>&1 | sed 's/^/[graphify] /'
     ```
   - full regeneration (`--full` flag or graph is `absent`):
     ```bash
     graphify . --obsidian --output vault/graph/ --full 2>&1 | sed 's/^/[graphify] /'
     ```
   - with semantic doc extraction (when `claude_api_key` is set):
     ```bash
     claude_api_key=$claude_api_key graphify . --obsidian --output vault/graph/ 2>&1 | sed 's/^/[graphify] /'
     ```
   - if `--state absent` was passed, always use `--full` regardless of other flags.

4. **verify outputs exist**:
   ```bash
   ls vault/graph/index.md vault/graph/graph_report.md
   ```
   if either file is missing, report: "graphify ran but expected output files are missing. check permissions on vault/graph/." and stop.

5. **update `vault/graph/index.md`** with the current timestamp by reading its header and confirming `last_updated` reflects today's date (graphify writes this automatically; confirm it is not stale).

6. **ensure supporting vault directories exist**:
   ```bash
   mkdir -p vault/lessons vault/context
   ```

7. **report diff**: read `vault/graph/graph_report.md` and summarise to the developer:
   - number of nodes added / updated / removed (if available from graphify output)
   - any god nodes (high-connectivity files) identified
   - path to index: `vault/graph/index.md`

## outputs

| output | path | description |
|--------|------|-------------|
| graph index | `vault/graph/index.md` | master node list — primary ai context source |
| node files | `vault/graph/nodes/*.md` | one markdown file per code/doc node |
| raw graph | `vault/graph/graph.json` | networkx json (machine-readable) |
| report | `vault/graph/graph_report.md` | plain-language summary of graph structure |
| graph visual | `vault/graph/graph.html` | interactive browser visualisation (optional) |

## error handling

- **graphify not installed**: print install instructions pointing to `setup-guides/graphify-setup.md`. do not proceed.
- **write failure** (permissions, disk full): report the exact error and path. halt immediately — do not allow a partial write to leave `vault/graph/` in an inconsistent state.
- **empty graph** (no nodes produced): warn the developer that the project may have no supported source files, or that `graphify` was run from the wrong directory.
- **claude_api_key not set**: proceed without semantic extraction — ast extraction still runs. inform developer that doc summaries will not be included.

## notes

- for projects with >500 graph nodes, consider adding `vault/graph/nodes/` to `.gitignore` to keep git history clean. the index and report files should still be committed.
- the `--full` flag is useful after major refactors or file renames where the incremental diff may not detect structural changes correctly.
- after `/map-codebase` runs, the vault is ready for `/context-load` to use at session start.
- see [workflows/map-refresh.md](../../workflows/map-refresh.md) for guidance on when to re-run this skill.
