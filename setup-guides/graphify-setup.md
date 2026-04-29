# Setup Guide: Graphify

## Overview

Graphify (`graphifyy`) is a headless CLI tool that builds a dependency and relationship graph of a codebase using AST analysis and stores it as an Obsidian vault. In the Spekificity workflow, Graphify is the engine behind the `/map-codebase` skill — it produces the vault graph that AI agents use for context-efficient session loading.

Code extraction uses tree-sitter AST locally (no API key required; supports 25+ languages). Optional semantic extraction of documentation and markdown requires a Claude API key.

## Install Mode

**Global** — installed per machine via `uv tool install`, not per project.

## Prerequisites

- Python 3.11+
- `uv` installed (`uv --version` returns a version)
- Internet access for initial install

## Installation Steps

1. Install Graphify globally:
   ```bash
   uv tool install graphifyy
   ```

2. Confirm the `graphify` command is on your PATH:
   ```bash
   which graphify
   # Expected: /Users/<you>/.local/bin/graphify or similar
   ```

## Verification

```bash
graphify --version
# Expected output: graphifyy X.X.X
```

## Usage in Spekificity

The `/map-codebase` skill runs:

```bash
graphify . --obsidian --output vault/graph/
```

- `.` — map the current project directory
- `--obsidian` — generate Obsidian vault files (markdown nodes + `index.md`)
- `--output vault/graph/` — write all output to the `vault/graph/` directory

**Optional: semantic extraction of docs** (requires Claude API key):

```bash
CLAUDE_API_KEY=sk-... graphify . --obsidian --output vault/graph/
```

Without the key, code AST extraction still runs fully — only markdown/doc semantic summaries are skipped.

## Configuration

No configuration file required. All options are passed as CLI flags.

## Version Compatibility

| Graphify Version | Spekificity Compatible | Notes |
|-----------------|----------------------|-------|
| ≥ 0.5.5 | ✓ | `--obsidian` flag required |
| < 0.5.5 | ✗ | `--obsidian` flag not available |

## Troubleshooting

- **Symptom**: `graphify: command not found` → **Fix**: Run `uv tool install graphifyy`; ensure `~/.local/bin` is in your `PATH` (`export PATH="$HOME/.local/bin:$PATH"`)
- **Symptom**: `Permission denied: vault/graph/` → **Fix**: Ensure the project root is writable (`chmod u+w .`)
- **Symptom**: Graph is empty / no nodes → **Fix**: Confirm you are running `graphify` from the project root, not a subdirectory
- **Symptom**: Incremental refresh not updating changed files → **Fix**: Run with `--full` flag to force a full regeneration: `graphify . --obsidian --output vault/graph/ --full`
