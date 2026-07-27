# Setup Implementation Spec

## Overview

`spek` is a Python CLI with one command: `spek init`. Its responsibility is:

1. Verifying prerequisites
2. Detecting and installing 3rd party dependencies (where possible)
3. Scaffolding the `.spek/` directory structure
4. Generating agent skill files for the chosen integration
5. Running SpecKit per-project init (`specify init`)
6. Installing git hooks

All workflow execution (prepare, plan, implement, conclude) happens through agent skill files installed by `spek init`. The CLI does not implement workflow logic — it delivers the skill files that do.

---

## Prerequisites Verification

These runtime prerequisites are installed during the global `spek` setup step (`uv tool install spekificity`). `spek init` verifies they are present — it does not install them. Fail with a descriptive error if any are missing, directing the user to re-run setup.

- Python 3.10+ in PATH
- git 2.0+ in PATH (auto-initialized by `spek init` if needed)
- uv 0.1+ in PATH
- Node.js 18+ in PATH (required by lat.md)

---

## 3rd Party Tool Installation

Detect each tool via `shutil.which()`. If not found, install or instruct as described below.

| Tool | CLI Name | Install Method | Notes |
|------|----------|---------------|-------|
| SpecKit | `specify` | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | Python; installs via uv |
| lat.md | `lat` | `npm install -g lat.md` | Requires Node.js 18+ |
| Obsidian | `obsidian` | `brew install --cask obsidian` / `winget install -e --id Obsidian.Obsidian` (see below for two-phase flow) | v1.12.4+; CLI built into desktop app; one-time manual CLI registration required after install |
| Caveman | — | SKILL.md fetched from `github:JuliusBrussee/caveman` (plugin cache → GitHub raw fallback) | No CLI binary; installs as a skill file; for `claude` integration also writes project-level activation hooks to `.claude/settings.json` |

### Obsidian — Install + CLI Registration

**Obsidian desktop and the Obsidian CLI are the same thing.** The CLI (`obsidian` binary) ships as part of Obsidian desktop v1.12.4+. There is no separate CLI package to install.

`spek init` handles Obsidian in two phases across (at most) two runs:

---

**Phase 1 — Install Obsidian desktop (automated):**

`spek init` detects the Obsidian app by checking for a known app path or the `obsidian` binary in PATH. If the app is not installed, it installs it automatically:

| Platform | Install Command (run by `spek init`) |
|----------|--------------------------------------|
| macOS | `brew install --cask obsidian` |
| Windows | `winget install -e --id Obsidian.Obsidian` |
| Linux | Print download URL; cannot auto-install — user must install manually |

After installing, check for `obsidian` in PATH. If found, Phase 2 is already complete (CLI was registered in a prior session) — continue init normally.

If `obsidian` is **not** in PATH after install, the CLI has not been registered yet. Emit the warning below and halt.

---

**Phase 1 halt — warning output (non-zero exit):**

```
⚠  Obsidian installed, but vault functionality is not yet active.

One manual step required in Obsidian:
  1. Open Obsidian
  2. Go to Settings → General → Command line interface → Enable
  3. Follow the prompt to register the CLI (creates the `obsidian` binary in PATH)
     - macOS:   symlink at /usr/local/bin/obsidian
     - Windows: Obsidian.com redirector added to PATH
     - Linux:   binary copied to ~/.local/bin/obsidian
  4. Restart your terminal

Then re-run:  spek init

spek init will complete all remaining setup autonomously.
```

Exit with code `2` (partial init — action required, not an error).

---

**Phase 2 — Re-run after CLI registration:**

On re-run, `obsidian` is in PATH and Obsidian is running. `spek init` completes all vault setup autonomously via the CLI — no user input required:

1. Create `.spek/vault/` directory (filesystem)
2. Register and open the vault in Obsidian via CLI
3. Create initial content files via CLI (see [Vault Initialization](#vault-initialization))

`spek init` skips the Obsidian install (idempotent) and completes all remaining steps on this run.

---

**Constraint:** Obsidian desktop must be running during all vault operations. Agent skill files must include this as a precondition. `spek init` registers the vault autonomously during Phase 2 — no manual vault registration required.

---

## Prompts

After prerequisite checks and tool installation, prompt for:

1. **AI agent integration type** — value is passed directly to `specify init --integration`. Must be a value from the `specify` supported list (see `specify integration list`).

   Agents with known skill file locations:

   | Value | Agent | Skill File Location |
   |-------|-------|---------------------|
   | `claude` | Claude Code | `.claude/commands/` |
   | `copilot` | GitHub Copilot | `.github/skills/` |
   | `gemini` | Gemini CLI | `.gemini/skills/` |
   | `cursor-agent` | Cursor | `.cursor/skills/` |
   | `windsurf` | Windsurf | `.windsurf/skills/` |
   | `cline` | Cline | `.cline/skills/` |
   | `codex` | Codex CLI | `.codex/skills/` |
   | `kiro-cli` | Kiro (AWS) | `.kiro/skills/` |
   | `amp` | Amp (Sourcegraph) | `.amp/skills/` |
   | `qwen` | Qwen Code | `.qwen/skills/` |
   | `generic` | Any / tool-agnostic | `.agents/skills/` (**default**) |

   All other valid `specify` integration values (`agy`, `auggie`, `codebuddy`, `devin`, `forge`, `goose`, `hermes`, `junie`, `kilocode`, `kimi`, `lingma`, `opencode`, `qodercli`, `roo`, `rovodev`, `shai`, `tabnine`, `trae`, `vibe`, and others) are accepted and passed to `specify init` — `spek init` copies skill files to `.agents/skills/` for these (same as `generic`).

   Note: `.agents/skills/` is recognised as an alias by Cursor, Codex, Gemini CLI, and Goose — `generic` works as a multi-agent fallback.

2. **Script type** — `sh` or `ps` (PowerShell)

Non-interactive mode:
```bash
spek init --integration claude --script sh
```

Flags:
- `--integration`: any value from `specify integration list`; common values: `claude` | `copilot` | `gemini` | `cursor-agent` | `windsurf` | `cline` | `codex` | `kiro-cli` | `amp` | `qwen` | `generic`
- `--script`: `sh` | `ps`
- `--no-git-hooks`: skip git hook installation

---

## Directory Structure

Create under project root:

```
.spek/
├── vault/                          ← Persistent knowledge vault (Obsidian-managed)
│   ├── lessons/                    ← Per-feature retrospectives
│   ├── decisions.md                ← Architectural decisions (append-only)
│   └── patterns.md                 ← Reusable patterns
├── memory/                         ← Repo-scoped memory (YAML)
├── lat/                            ← lat.md index directory
└── config.yaml                     ← Project configuration
```

Skill file directory depends on integration type. SpecKit also creates `.specify/` via `specify init`.

---

## Vault Initialization

Runs during Phase 2 (re-run after CLI registration). Obsidian is running and `obsidian` is in PATH. `spek init` handles all vault setup autonomously:

```bash
# Create vault directory
mkdir -p .spek/vault/lessons

# Register and open vault in Obsidian via CLI
obsidian open-vault path=.spek/vault

# Create initial content files via CLI
obsidian create file=decisions content="# Decisions" vault=vault
obsidian create file=patterns content="# Patterns" vault=vault
obsidian create path="lessons/.keep" content="" vault=vault
```

All agent skill file vault operations use the Obsidian CLI (never direct filesystem writes). Obsidian CLI syntax:

```bash
# Read a note (vault must be open in Obsidian)
obsidian read file=decisions vault=vault

# Append to a note
obsidian append file=decisions content="## Decision: ..." vault=vault

# Read by path (for files in subdirectories)
obsidian read path="lessons/2026-06-09-feature.md" vault=vault

# Append by path
obsidian append path="lessons/2026-06-09-feature.md" content="..." vault=vault
```

`vault=vault` refers to the vault name as registered in Obsidian (the folder name by default). Skill files should use this name. The vault name matches the directory name: `vault`.

---

## lat.md Initialization

After directory creation, initialize lat.md in the project:

```bash
# Initialize lat.md index (run in project root)
lat init

# Start MCP server (agents connect via MCP protocol)
lat mcp
```

`lat init` creates the index in `.spek/lat.md/`. `lat mcp` starts the MCP server that agent skills query during workflow. MCP server must be running during agent sessions.

---

## Agent MCP Configuration

`spek init` writes the lat.md MCP server entry into the chosen integration's config file. This allows the agent to call lat.md tools during workflow without manual setup.

**Server entry (same for all integrations):**
```json
{
  "command": "lat",
  "args": ["mcp"]
}
```

**Per-integration config file and structure:**

| Integration | Config file (project-level) | Structure key | Notes |
|-------------|----------------------------|---------------|-------|
| `claude` | `.mcp.json` | `mcpServers` | Standard Claude Code project MCP config |
| `cursor-agent` | `.cursor/mcp.json` | `mcpServers` | Cursor project MCP config |
| `copilot` | `.vscode/mcp.json` | `servers` | VS Code native MCP (v1.99+); `"type": "stdio"` required |
| `windsurf` | `.windsurf/mcp.json` | `mcpServers` | |
| `cline` | `.vscode/settings.json` | `cline.mcpServers` | Written as flat key under VS Code workspace settings |
| `gemini` | `.gemini/settings.json` | `mcpServers` | |
| `codex` | `.codex/mcp.json` | `mcpServers` | |
| `kiro-cli` | `.kiro/mcp.json` | `mcpServers` | |
| `amp` | `.amp/mcp.json` | `mcpServers` | |
| `qwen` | `.qwen/mcp.json` | `mcpServers` | |
| `generic` + others | — | — | Print manual config instructions; no file written |

**Example formats:**

```json
// .mcp.json (claude)
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

```json
// .cursor/mcp.json (cursor-agent)
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

```json
// .vscode/mcp.json (copilot — VS Code 1.99+)
{
  "servers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"],
      "type": "stdio"
    }
  }
}
```

**Merge behaviour:**
- If config file exists: parse JSON, add `lat` entry under the correct key, write back. Do not clobber existing entries.
- If `lat` entry already present: skip (idempotent).
- If config file does not exist: create it with only the `lat` entry.

**`generic` and unrecognised integrations:**
Do not write a config file. Print instructions instead:

```
lat.md MCP server not auto-configured for this integration.
Add the following to your agent's MCP config manually:

  server name: lat
  command:     lat
  args:        mcp
  type:        stdio
```

---

## Agent Skill File Installation

Skill files are **not generated by Python code**. They are canonical `.md` files stored in the `spekificity` package source under `spekificity/skills/`. `spek init` copies them from the installed package to the local project — no string interpolation or code-side templating.

### Package Source Layout

```
spekificity/
└── skills/
    ├── spek-prepare.md
    ├── spek-plan.md
    ├── spek-implement.md
    ├── spek-conclude.md
    ├── spek-lessons.md
    ├── spek-context.md
    ├── spek-map.md
    ├── spek-blind-review.md
    └── spek-rarv.md
```

These files are the authoritative skill definitions. Editing them in the source repo is how skill behaviour is changed — not by modifying Python code.

They are declared as build artifacts so they are included in the installed distribution:

```toml
# pyproject.toml
[tool.hatch.build.targets.wheel]
packages = ["spekificity"]
artifacts = [
    "spekificity/skills/*.md",
]
```

### Copy Behaviour at Init

`spek init` resolves the installed package skill directory via `importlib.resources` (or `importlib_resources` for Python < 3.9), then copies each file to the target location for the selected integration:

| Destination format | Integrations | Path pattern |
|--------------------|--------------|--------------|
| Flat `.md` file | `claude`, `copilot`, `generic` | `<skills-dir>/spek-prepare.md` |
| Subfolder `SKILL.md` | `gemini`, `cursor-agent`, `windsurf`, `cline`, `codex`, `kiro-cli` | `<skills-dir>/spek-prepare/SKILL.md` |

Where `<skills-dir>` is the integration's root skills directory (see [Prompts](#prompts) table).

Example (pseudocode):

```python
import importlib.resources as pkg_resources
import shutil

skills_src = pkg_resources.files("spekificity") / "skills"
for skill_file in skills_src.iterdir():
    dest = resolve_dest(skill_file.name, integration, script_type)
    if not dest.exists():          # idempotent — never overwrite
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_file, dest)
```

Skill files already present at the destination are never overwritten (idempotent re-run).

**Bundled skill files:**
- `spek-prepare.md`
- `spek-plan.md`
- `spek-implement.md`
- `spek-conclude.md`
- `spek-lessons.md`
- `spek-context.md`
- `spek-map.md`
- `spek-blind-review.md`
- `spek-rarv.md`

Full skill content is defined in those source files. For the skill format specification see [skills.md](skills.md).

### Caveman Skill Installation

The Caveman skill is installed separately from bundled skills — it is fetched at init time rather than shipped inside the spekificity package.

**Source resolution order** (first success wins):
1. `~/.claude/skills/caveman/SKILL.md` — already extracted by the Claude Code plugin system
2. `~/.claude/plugins/cache/caveman/caveman/<sha>/plugins/caveman/skills/caveman/SKILL.md` — plugin cache
3. `https://raw.githubusercontent.com/JuliusBrussee/caveman/main/plugins/caveman/skills/caveman/SKILL.md` — GitHub raw fallback

**Placement** follows the same flat/subfolder rules as bundled skills:

| Destination format | Integrations | Path |
|--------------------|--------------|------|
| Flat `.md` | `claude`, `copilot`, `generic` | `<skills-dir>/caveman.md` |
| Subfolder `SKILL.md` | all others | `<skills-dir>/caveman/SKILL.md` |

**Claude Code auto-activation:** For the `claude` integration, `spek init` additionally writes two hook entries to the project's `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "\"<node>\" \"~/.claude/hooks/caveman-activate.js\"", "timeout": 5, "statusMessage": "Loading caveman mode..." }] }],
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "\"<node>\" \"~/.claude/hooks/caveman-mode-tracker.js\"", "timeout": 5, "statusMessage": "Tracking caveman mode..." }] }]
  }
}
```

These hooks activate caveman at `full` intensity automatically on every session start. Existing hook entries are preserved; duplicate entries are never written. If caveman installation fails for any reason (network unavailable, source not found), `spek init` logs a warning and continues — caveman failure is non-fatal.

---

## SpecKit Initialization

Run after directory creation:

```bash
specify init <project-name> --integration <agent-type>
```

Where `<agent-type>` is the integration value selected at prompt, passed through directly — no mapping or translation. The same value drives both `spek init` skill file placement and `specify init` configuration.

This creates `.specify/` with:

```
.specify/
├── memory/constitution.md     ← Project principles (populated by /speckit.constitution skill)
├── extensions.yml             ← SpecKit hook configuration
└── templates/                 ← Spec/plan/task templates
```

`.specify/memory/constitution.md` may not exist after `specify init` — it is created when `/speckit.constitution` is first invoked. `spek.prepare` checks for it and triggers the skill if missing.

---

## Configuration File

Generate `.spek/config.yaml` (idempotent — skip if already exists):

```yaml
integration: claude  # any specify integration value; e.g. copilot, gemini, cursor-agent, windsurf, kiro-cli, amp, qwen, generic
script_type: sh      # or ps

tools:
  speckit:
    enabled: true
  lat_md:
    enabled: true
    index_path: .spek/lat.md/
  vault:
    enabled: true
    path: .spek/vault/
    obsidian_vault_name: vault

context_loading:
  cache_expiry_minutes: 60

token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000

autolink:
  enabled: true
  threshold: 0.8
  keyword_tags: {}

token_budget:
  per_feature: null
  alert_thresholds: []

antisycophancy:
  enabled: true
  complexity_threshold: 2.0
  contradiction_pairs: []
```

---

## Memory YAML Schema

Files written to `.spek/memory/` use this structure:

```yaml
# .spek/memory/<scope>.yaml
scope: repo          # repo | session | user
updated: YYYY-MM-DD
entries:
  - key: string
    value: string
    tags: [string]
    created: YYYY-MM-DD
```

---

## Git Hooks

Install a git post-commit hook for automatic lat.md index refresh (see [decision.md](decision.md#git-hooks-integration-for-automatic-graph-refresh)).

Create `.git/hooks/post-commit`:

```bash
#!/bin/sh
lat update
```

Mark executable. Opt-out: if `.spek/.disable-git-hooks` exists, skip installation entirely.

---

## Idempotency

`spek init` is safe to re-run:

- Skip tools already present in PATH
- Skip Obsidian install if app already present; skip to CLI check
- If `obsidian` now in PATH (user completed GUI registration since last run): proceed with remaining steps
- Skip directories that already exist
- Skip skill files that already exist (do not overwrite)
- Skip caveman skill if already present at destination; skip caveman hooks if already in `.claude/settings.json`
- Re-run `specify init` only if `.specify/` is missing
- Re-install git hook only if not present
- Report what was created vs already present

**Obsidian re-run path:** Phase 1 halt (exit code `2`) is the designed checkpoint. On re-run after CLI registration, init resumes from where it halted — no steps are duplicated.
