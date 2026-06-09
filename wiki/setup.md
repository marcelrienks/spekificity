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

Before proceeding, `spek init` must verify:

- Python 3.11+ in PATH
- `git` in PATH and current directory is a valid git repository
- `uv` in PATH
- Node.js 22+ in PATH (required by lat.md)

Fail with descriptive error message if any check fails.

---

## 3rd Party Tool Installation

Detect each tool via `shutil.which()`. If not found, install or instruct as described below.

| Tool | CLI Name | Install Method | Notes |
|------|----------|---------------|-------|
| SpecKit | `specify` | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | Python; installs via uv |
| lat.md | `lat` | `npm install -g lat.md` | Requires Node.js 22+ |
| Obsidian CLI | `obsidian` | Cannot be auto-installed — see below | Enabled in Obsidian desktop |

### Obsidian CLI — Manual Enable Required

The Obsidian CLI is built into Obsidian desktop v1.12.4+. It cannot be installed programmatically. If `obsidian` is not found in PATH:

1. Output instructions to the user: "Enable the Obsidian CLI: open Obsidian → Settings → General → Command line interface → Enable, then restart your terminal."
2. Halt `spek init` with a non-zero exit code until `obsidian` is detected.

**Constraint:** Obsidian desktop must be running during all vault operations. Agent skill files must include this as a precondition.

The `.spek/vault/` directory must also be registered as a vault in Obsidian desktop (File → Open vault → Open folder as vault). `spek init` creates the directory; the user must open it in Obsidian once.

---

## Prompts

After prerequisite checks and tool installation, prompt for:

1. **AI agent integration type** — selects where skill files are generated:
   - `claude` → `.claude/commands/`
   - `copilot` → `.github/agents/skills/`
   - `gemini` → TBD (confirm with Gemini agent specification)
   - `generic` → `.spek/skills/`

2. **Script type** — `sh` or `ps` (PowerShell)

Non-interactive mode:
```bash
spek init --integration claude --script sh
```

Flags:
- `--integration`: `claude` | `copilot` | `gemini` | `generic`
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

Create the `.spek/vault/` directory. Initial content files are created directly by filesystem (vault is not yet registered in Obsidian at this point):

```
.spek/vault/decisions.md  → "# Decisions\n"
.spek/vault/patterns.md   → "# Patterns\n"
.spek/vault/lessons/      → empty directory
```

After `spek init` completes, output instruction: "Open .spek/vault/ as a vault in Obsidian (File → Open vault → Open folder as vault). All subsequent vault operations require Obsidian to be running."

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

## Agent Skill File Generation

Generate one skill file per `/spek.*` command. File name maps from command with dots replaced by hyphens: `/spek.prepare` → `spek-prepare.md`.

**Required skill files:**
- `spek-prepare.md`
- `spek-plan.md`
- `spek-implement.md`
- `spek-conclude.md`
- `spek-lessons.md`
- `spek-context.md` (optional enhancement)
- `spek-map.md` (optional enhancement)

**Each skill file must contain:**

```markdown
# /spek.<command>

## Purpose
[One line: what this skill does]

## Preconditions
- Obsidian desktop is running with .spek/vault/ open as vault named "vault"
- lat.md MCP server is running (lat mcp)

## When to invoke
[Triggers and preconditions]

## Steps
[Numbered, exact sequence the agent executes]
1. [Specific action — tool call, file read, skill invocation]
2. [...]

## Tool Permissions Required
- lat.md MCP: confirm tool names against lat.md MCP server documentation
- Obsidian CLI: read/write .spek/vault/ (requires Obsidian desktop running)
- SpecKit: specify, /speckit.* skill invocations

## Third-Party Tool Usage

### lat.md (via MCP — confirm tool names against lat.md docs)
- Locate code: `lat locate <symbol>`
- Find references: `lat refs <symbol>`
- Search: `lat search <query>`
- MCP server: started with `lat mcp` before agent session

### SpecKit
- Invoke: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`

### Obsidian CLI (all vault operations — desktop must be running)
- Read note: `obsidian read file=<name> vault=vault`
- Read by path: `obsidian read path="<relative-path>" vault=vault`
- Append to note: `obsidian append file=<name> content="<text>" vault=vault`
- Append by path: `obsidian append path="<relative-path>" content="<text>" vault=vault`

## Output
[What artifacts are created, where they are stored]
```

---

## SpecKit Initialization

Run after directory creation:

```bash
specify init <project-name> --integration <agent-type>
```

Where `<agent-type>` maps from the integration selected at prompt: `claude`, `copilot`, `gemini`, or `generic`.

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
integration: claude  # or copilot, gemini, generic
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
lat init
```

Mark executable. Opt-out: if `.spek/.disable-git-hooks` exists, skip installation entirely.

---

## Idempotency

`spek init` is safe to re-run:

- Skip tools already present in PATH
- Skip directories that already exist
- Skip skill files that already exist (do not overwrite)
- Re-run `specify init` only if `.specify/` is missing
- Re-install git hook only if not present
- Report what was created vs already present

---

## References

- **Workflow behavior delivered by skills:** [workflow.md](workflow.md)
- **Skills reference:** [skills.md](skills.md)
- **Vault and memory conventions:** [conventions.md](conventions.md)
- **Architectural decisions behind setup choices:** [decision.md](decision.md) (Decisions 1, 7)
