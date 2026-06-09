# Setup Implementation Spec

## Overview

`spek` is a Python CLI with one command: `spek init`. Its responsibility is:

1. Verifying prerequisites
2. Detecting and installing 3rd party dependencies
3. Scaffolding the `.spek/` directory structure
4. Generating agent skill files for the chosen integration
5. Running SpecKit per-project init (`specify init .`)
6. Installing git hooks

All workflow execution (prepare, plan, implement, conclude) happens through agent skill files installed by `spek init`. The CLI does not implement workflow logic — it delivers the skill files that do.

---

## Prerequisites Verification

Before proceeding, `spek init` must verify:

- Python 3.11+ in PATH
- `git` in PATH and current directory is a valid git repository
- `uv` in PATH

Fail with descriptive error message if any check fails.

---

## 3rd Party Tool Installation

Detect each tool via `shutil.which()`. If not found in PATH, install using the tool's standard package manager.

| Tool | Role | Install Method |
|------|------|---------------|
| SpecKit (`specify`) | Spec → plan → implement orchestration | TBD — confirm against SpecKit release |
| lat.md (`lat`) | Code and documentation indexing, MCP interface | TBD — confirm against lat.md release |
| Obsidian CLI (`obsidian`) | All vault read/write operations | TBD — confirm against Obsidian CLI release |

**Note:** Exact package names and install commands must be resolved against each tool's actual published release. The table above records role and install mechanism — populate the Install Method column once package registry names are confirmed.

Obsidian desktop is **not** installed — it is optional and only needed for interactive graph visualization by a human user. Obsidian CLI is the only Obsidian dependency required by Spekificity.

---

## Prompts

After prerequisite checks and tool installation, prompt the user for:

1. **AI agent integration type** — selects where skill files are generated:
   - `claude` → `.claude/commands/`
   - `copilot` → `.github/agents/skills/`
   - `gemini` → TBD (confirm with Gemini agent specification)
   - `generic` → `.spek/skills/`

2. **Script type** — `sh` or `ps` (PowerShell)

Support non-interactive mode:
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
├── lat/                            ← lat.md index directory (non-human-readable)
└── config.yaml                     ← Project configuration
```

Skill file directory depends on integration type selected. SpecKit also creates `.specify/` via `specify init .`.

---

## Vault Initialization

Initialize vault using Obsidian CLI (not direct filesystem writes):

```bash
obsidian init --vault .spek/vault/
obsidian write --vault .spek/vault/ --note decisions.md --content "# Decisions\n"
obsidian write --vault .spek/vault/ --note patterns.md --content "# Patterns\n"
```

All subsequent vault operations by agent skills must also go through the Obsidian CLI. Direct filesystem writes to `.spek/vault/` are not permitted — they bypass Obsidian's indexing, backlink tracking, and graph state.

---

## Agent Skill File Generation

Generate one skill file per `/spek.*` command. File name maps from command name with dots replaced by hyphens: `/spek.prepare` → `spek-prepare.md`.

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

## When to invoke
[Triggers and preconditions]

## Steps
[Numbered, exact sequence the agent executes]
1. [Specific action — tool call, file read, skill invocation]
2. [...]

## Tool Permissions Required
- lat.md MCP: lat_symbols, lat_references, lat_sync
- Obsidian CLI: read/write .spek/vault/
- SpecKit: specify, speckit.* skill invocations

## Third-Party Tool Usage

### lat.md
- Index code: `lat_sync --path .`
- Index docs: `lat_sync --path .spek/vault/ --mode docs`
- Query: `lat_symbols <symbol>`, `lat_references <symbol>`

### SpecKit
- Invoke: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`

### Obsidian CLI (all vault operations)
- Read note: `obsidian read --vault .spek/vault/ --note decisions.md`
- Write/create note: `obsidian write --vault .spek/vault/ --note lessons/YYYY-MM-DD-feature.md`
- Append to note: `obsidian append --vault .spek/vault/ --note decisions.md`

## Output
[What artifacts are created, where they are stored]
```

Skill files must contain complete, accurate tool interaction instructions for the chosen integration. Without exact MCP tool names, filesystem paths, and command syntax, the agent will fail silently or hallucinate behavior.

---

## SpecKit Initialization

Run after directory creation:

```bash
specify init .
```

This creates `.specify/` with:

```
.specify/
├── memory/constitution.md     ← Project principles (populated by /speckit.constitution skill)
├── extensions.yml             ← SpecKit hook configuration
└── templates/                 ← Spec/plan/task templates
```

`.specify/memory/constitution.md` may not exist immediately after `specify init .` — it is created when the `/speckit.constitution` skill is first invoked (one-time, interactive). `spek.prepare` checks for it and triggers the skill if missing.

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
lat sync . --incremental
```

Mark executable. Opt-out: if `.spek/.disable-git-hooks` exists, skip installation entirely.

---

## Idempotency

`spek init` is safe to re-run:

- Skip tools already present in PATH
- Skip directories that already exist
- Skip skill files that already exist (do not overwrite)
- Re-run `specify init .` only if `.specify/` is missing
- Report what was created vs already present

---

## References

- **Workflow behavior delivered by skills:** [workflow.md](workflow.md)
- **Skills reference:** [skills.md](skills.md)
- **Vault and memory conventions:** [conventions.md](conventions.md)
- **Architectural decisions behind setup choices:** [decision.md](decision.md) (Decisions 1, 7)
