# setup guide: graphify

## overview

graphify (`graphifyy`) is a headless cli tool that builds a dependency and relationship graph of a codebase using ast analysis and stores it as an obsidian vault. in the spekificity workflow, graphify is the engine behind the `/map-codebase` skill — it produces the vault graph that ai agents use for context-efficient session loading.

code extraction uses tree-sitter ast locally (no api key required; supports 25+ languages). optional semantic extraction of documentation and markdown requires a claude api key.

## install mode

**global** — installed per machine via `uv tool install`, not per project.

## prerequisites

- python 3.11+
- `uv` installed (`uv --version` returns a version)
- internet access for initial install

## installation steps

1. install graphify globally:
   ```bash
   uv tool install graphifyy
   ```

2. confirm the `graphify` command is on your path:
   ```bash
   which graphify
   # expected: /users/<you>/.local/bin/graphify or similar
   ```

## verification

```bash
graphify --version
# expected output: graphifyy x.x.x
```

## usage in spekificity

the `/map-codebase` skill runs:

```bash
graphify . --obsidian --output vault/graph/
```

- `.` — map the current project directory
- `--obsidian` — generate obsidian vault files (markdown nodes + `index.md`)
- `--output vault/graph/` — write all output to the `vault/graph/` directory

**optional: semantic extraction of docs** (requires claude api key):

```bash
claude_api_key=sk-... graphify . --obsidian --output vault/graph/
```

without the key, code ast extraction still runs fully — only markdown/doc semantic summaries are skipped.

## configuration

no configuration file required. all options are passed as cli flags.

## version compatibility

| graphify version | spekificity compatible | notes |
|-----------------|----------------------|-------|
| ≥ 0.5.5 | ✓ | `--obsidian` flag required |
| < 0.5.5 | ✗ | `--obsidian` flag not available |

## troubleshooting

- **symptom**: `graphify: command not found` → **fix**: run `uv tool install graphifyy`; ensure `~/.local/bin` is in your `path` (`export path="$home/.local/bin:$path"`)
- **symptom**: `permission denied: vault/graph/` → **fix**: ensure the project root is writable (`chmod u+w .`)
- **symptom**: graph is empty / no nodes → **fix**: confirm you are running `graphify` from the project root, not a subdirectory
- **symptom**: incremental refresh not updating changed files → **fix**: run with `--full` flag to force a full regeneration: `graphify . --obsidian --output vault/graph/ --full`
