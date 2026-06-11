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

- Python 3.11+ in PATH
- `git` in PATH and current directory is a valid git repository
- `uv` in PATH
- Node.js 22+ in PATH (required by lat.md)

---

## 3rd Party Tool Installation

Detect each tool via `shutil.which()`. If not found, install or instruct as described below.

| Tool | CLI Name | Install Method | Notes |
|------|----------|---------------|-------|
| SpecKit | `specify` | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | Python; installs via uv |
| lat.md | `lat` | `npm install -g lat.md` | Requires Node.js 22+ |
| Obsidian | `obsidian` | `brew install --cask obsidian` / `winget install -e --id Obsidian.Obsidian` (see below for two-phase flow) | v1.12.4+; CLI built into desktop app; one-time manual CLI registration required after install |

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
   | `copilot` | GitHub Copilot | `.github/agents/skills/` |
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

Verify `open-vault` command syntax against the Obsidian CLI docs before implementation — the exact subcommand may differ across versions.

All agent skill file vault operations use the Obsidian CLI (never direct filesystem writes). Correct Obsidian CLI syntax:

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

`lat init` creates the index in `.spek/lat/`. `lat mcp` starts the MCP server that agent skills query during workflow. MCP server must be running during agent sessions.

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
    └── spek-map.md
```

These files are the authoritative skill definitions. Editing them in the source repo is how skill behaviour is changed — not by modifying Python code.

They must be declared as `package_data` (or equivalent) so they are included in the installed distribution:

```toml
# pyproject.toml
[tool.setuptools.package-data]
spekificity = ["skills/*.md"]
```

### Copy Behaviour at Init

`spek init` resolves the installed package skill directory via `importlib.resources` (or `importlib_resources` for Python < 3.9), then copies each file to the target location for the selected integration:

| Destination format | Integrations | Path pattern |
|--------------------|--------------|--------------|
| Flat `.md` file | `claude`, `copilot`, `gemini`, `generic` | `<skills-dir>/spek-prepare.md` |
| Subfolder `SKILL.md` | `cursor`, `windsurf`, `cline`, `codex`, `kiro` | `<skills-dir>/spek-prepare/SKILL.md` |

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

**Required skill files:**
- `spek-prepare.md`
- `spek-plan.md`
- `spek-implement.md`
- `spek-conclude.md`
- `spek-lessons.md`
- `spek-context.md`
- `spek-map.md`

Full skill content is defined in those source files. For the skill format specification see [skills.md](skills.md).

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

Generate `.spek/config.yaml`:

```yaml
integration: claude  # any specify integration value; e.g. copilot, gemini, cursor-agent, windsurf, kiro-cli, amp, qwen, generic
script_type: sh      # or ps

tools:
  speckit:
    enabled: true
  lat_md:
    enabled: true
    index_path: .spek/lat/
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

Install a git post-commit hook for automatic lat.md index refresh (see [decision.md](decision.md#decision-7)).

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
- Re-run `specify init` only if `.specify/` is missing
- Re-install git hook only if not present
- Report what was created vs already present

**Obsidian re-run path:** Phase 1 halt (exit code `2`) is the designed checkpoint. On re-run after CLI registration, init resumes from where it halted — no steps are duplicated.
