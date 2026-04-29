# Map Codebase

## Description

Builds or refreshes a Graphify-generated graph of the current project and stores it as an Obsidian vault at `vault/graph/`. The resulting vault index (`vault/graph/index.md`) becomes the primary context source for all subsequent AI agent sessions — enabling cross-cutting queries without exhaustively scanning source files.

This skill is the entry point to the Spekificity context system. Run it once after initialisation, and again whenever the codebase changes significantly.

## Trigger

Invoked by the developer in the AI chat session:
```
/map-codebase
```

Optional flag for full regeneration (bypasses incremental diff):
```
/map-codebase --full
```

## Prerequisites

- Spekificity initialisation complete (see [workflows/init-workflow.md](../../workflows/init-workflow.md))
- `graphify --version` returns a version ≥ 0.5.5 (see [setup-guides/graphify-setup.md](../../setup-guides/graphify-setup.md))
- Current working directory is the project root (where `vault/` lives or will be created)
- Write permissions on the project root

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| `--full` flag | Force full graph regeneration instead of incremental diff | No |
| `CLAUDE_API_KEY` env var | Enables semantic extraction of markdown docs and comments (beyond AST) | No |

## Steps

1. **Verify Graphify is installed**:
   ```bash
   graphify --version
   ```
   If this fails, print: "Graphify is not installed. Follow setup-guides/graphify-setup.md then retry." and stop.

2. **Confirm project root**: Verify `vault/` or at least one of `skills/`, `workflows/`, `specs/`, or a recognisable project file (`.specify/`, `README.md`, `package.json`, etc.) exists in the current directory. If not, warn: "Run /map-codebase from the project root."

3. **Run Graphify**:
   - Standard (incremental):
     ```bash
     graphify . --obsidian --output vault/graph/
     ```
   - Full regeneration (when `--full` flag is present):
     ```bash
     graphify . --obsidian --output vault/graph/ --full
     ```
   - With semantic doc extraction (when `CLAUDE_API_KEY` is set):
     ```bash
     CLAUDE_API_KEY=$CLAUDE_API_KEY graphify . --obsidian --output vault/graph/
     ```

4. **Verify outputs exist**:
   ```bash
   ls vault/graph/index.md vault/graph/GRAPH_REPORT.md
   ```
   If either file is missing, report: "Graphify ran but expected output files are missing. Check permissions on vault/graph/." and stop.

5. **Update `vault/graph/index.md`** with the current timestamp by reading its header and confirming `last_updated` reflects today's date (Graphify writes this automatically; confirm it is not stale).

6. **Ensure supporting vault directories exist**:
   ```bash
   mkdir -p vault/lessons vault/context
   ```

7. **Report diff**: Read `vault/graph/GRAPH_REPORT.md` and summarise to the developer:
   - Number of nodes added / updated / removed (if available from Graphify output)
   - Any god nodes (high-connectivity files) identified
   - Path to index: `vault/graph/index.md`

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| Graph index | `vault/graph/index.md` | Master node list — primary AI context source |
| Node files | `vault/graph/nodes/*.md` | One markdown file per code/doc node |
| Raw graph | `vault/graph/graph.json` | NetworkX JSON (machine-readable) |
| Report | `vault/graph/GRAPH_REPORT.md` | Plain-language summary of graph structure |
| Graph visual | `vault/graph/graph.html` | Interactive browser visualisation (optional) |

## Error Handling

- **Graphify not installed**: Print install instructions pointing to `setup-guides/graphify-setup.md`. Do not proceed.
- **Write failure** (permissions, disk full): Report the exact error and path. Halt immediately — do not allow a partial write to leave `vault/graph/` in an inconsistent state.
- **Empty graph** (no nodes produced): Warn the developer that the project may have no supported source files, or that `graphify` was run from the wrong directory.
- **CLAUDE_API_KEY not set**: Proceed without semantic extraction — AST extraction still runs. Inform developer that doc summaries will not be included.

## Notes

- For projects with >500 graph nodes, consider adding `vault/graph/nodes/` to `.gitignore` to keep git history clean. The index and report files should still be committed.
- The `--full` flag is useful after major refactors or file renames where the incremental diff may not detect structural changes correctly.
- After `/map-codebase` runs, the vault is ready for `/context-load` to use at session start.
- See [workflows/map-refresh.md](../../workflows/map-refresh.md) for guidance on when to re-run this skill.
