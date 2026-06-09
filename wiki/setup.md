# Setup: Installation & Configuration

This document describes setup and configuration for Spekificity.

---

## Design Model: CLI for Scaffolding, Agent Skills for Workflow

Spekificity separates two concerns:

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| **Scaffolding** | `spek` CLI (`spek init`) | One-time per-project setup of infrastructure and skill files |
| **Workflow** | Agent skills (`/spek.*`) | Feature development (prepare, plan, implement, conclude) |

**Critical:** `spek` CLI has only one command: `spek init`. There are no CLI commands for `prepare`, `plan`, `implement`, or `conclude`. All workflow operations are agentic skills that run inside the agent environment (Claude Code, Copilot, etc.), installed by `spek init`.

---

## Tool Requirements

| Tool | Role | Installation |
|------|------|------|
| **SpecKit** | Spec → plan → implement orchestration engine | Auto-installed by `spek init` |
| **lat.md** | Code and documentation indexing + MCP queries | Auto-installed by `spek init` |
| **Obsidian CLI** | All vault read/write operations | Auto-installed by `spek init` |
| **Obsidian Desktop** | Vault graph visualization (optional) | Manual install if desired |
| **Caveman** | Token compression skill (Claude integration) | Auto-installed by `spek init` |

**All vault operations use the Obsidian CLI** for consistent indexing, backlink updates, and graph state. Obsidian desktop is optional and only needed for interactive graph browsing.

---

## Prerequisites

Only these are required before Spekificity:

- **Python 3.11+** — Check: `python3 --version`
- **Git** — Check: `git --version`
- **`uv` package manager** — Check: `uv --version`. Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

All other dependencies (SpecKit, lat.md, Obsidian CLI) are auto-installed by `spek init`.

---

## Installation

### Step 1: Install `spek` CLI Globally

```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

Verify:
```bash
spek --version
```

### Step 2: Per-Project Initialization

Navigate to a git repository:

```bash
cd /path/to/your/project
git status  # Must be a valid git repo; run git init first if not
```

Run:

```bash
spek init
```

`spek init` **auto-detects and installs missing dependencies** (SpecKit, lat.md, Obsidian CLI). Then it prompts for:

**What `spek init` does:**
1. Checks for SpecKit, lat.md, Obsidian CLI; installs if missing
2. Creates `.spek/` directory structure
3. Initializes lat.md code index + documentation index
4. Creates agent skill files in correct location
5. Runs `specify init .` for SpecKit configuration

**Then it prompts for agent integration type and script type:**
1. **AI agent integration type** — selects which format skill files are generated in:
   - `claude` → installs skills to `.claude/commands/`
   - `copilot` → installs skills to `.github/agents/skills/`
   - `gemini` → installs skills to agent-specific directory
   - `generic` → installs skills to `.spek/skills/`
2. **Script type** — `sh` or `ps` (PowerShell)

Non-interactive (CI/scripted):
```bash
spek init --integration claude --script sh
```

### Directory Structure Created

```
your-project/
├── .spek/
│   ├── vault/ (.spek/vault/)           ← Persistent knowledge vault
│   │   ├── lessons/                    ← Per-feature retrospectives
│   │   ├── decisions.md                ← Architectural decisions (append-only)
│   │   └── patterns.md                 ← Reusable patterns
│   ├── memory/                         ← Repo-scoped memory (YAML)
│   ├── lat/                            ← lat.md code + docs index (non-human-readable)
│   └── config.yaml                     ← Spekificity project config
├── .claude/commands/                   ← Agent skill files (if Claude integration)
│   ├── spek-prepare.md
│   ├── spek-plan.md
│   ├── spek-implement.md
│   └── spek-conclude.md
└── .specify/                           ← SpecKit per-project config (from specify init .)
    ├── memory/constitution.md
    ├── extensions.yml
    └── templates/
```

**Skill file location varies by integration type selected.** Copilot: `.github/agents/skills/`. Generic: `.spek/skills/`.

`spek init` also runs `specify init .` to configure SpecKit for the project.

### Step 3: Verify Setup

```bash
# Check .spek structure
ls -la .spek/
ls -la .spek/vault/          # decisions.md, patterns.md, lessons/
ls -la .spek/memory/
ls -la .spek/lat/

# Check skill files (Claude integration example)
ls -la .claude/commands/     # spek-prepare.md, spek-plan.md, etc.

# Check SpecKit config
ls -la .specify/
```

---

## Understanding the Infrastructure

### Vault (`.spek/vault/`)

Persistent knowledge base for the project. Plain markdown files, but **all agent reads and writes go through the Obsidian CLI** — not direct filesystem I/O. This ensures Obsidian's link graph and index stay consistent.

```
.spek/vault/
├── lessons/                        ← Per-feature retrospectives (written by /spek.conclude)
│   └── YYYY-MM-DD-feature-name.md  ← Naming: date + feature name
├── decisions.md                    ← Architectural decisions (append-only)
└── patterns.md                     ← Reusable patterns and best practices
```

- Git-tracked. Commit via `git add .spek/vault/; git commit -m "..."`
- **All vault reads and writes go through Obsidian CLI** — agents do not write vault files directly via filesystem. CLI ensures consistent indexing, backlink updates, and graph state.
- Obsidian desktop optional — only needed for graph visualization in desktop app.

**Vault is at `.spek/vault/`, not `vault/` at project root.**

---

### lat.md (`.spek/lat/`)

Code analysis and indexing tool. Installed separately; `spek init` creates the per-project index directory.

`lat.md` provides:
- Pre-indexed code symbols, definitions, call graphs
- Separate indexing for documentation (markdown files, wiki)
- MCP tool interface for agent queries (`lat_symbols`, `lat_references`, `lat_callers`, `lat_impact`)
- Framework-aware extractors (Go, Python, TypeScript, etc.)

**Used by `/spek.prepare`**: When `/spek.prepare` runs, it indexes both code and documentation via lat.md and stores the results in the Obsidian vault for context loading.

Usage during workflow:
- `/lat.query` — Query code/doc intelligence
- `/lat.sync` — Refresh index after code changes (run after `/spek.conclude`)

---

### Agent Skill Files

`spek init` generates skill files — markdown instructions that tell the agent exactly how to execute each skill. These are the core product. `spek init` generates them in the format the chosen integration expects.

**How agents discover skill files:**
- **Claude Code:** Automatically discovers `.claude/commands/*.md` as slash commands. A file named `spek-prepare.md` becomes `/spek.prepare`.
- **Copilot:** Agent instruction files at `.github/agents/skills/` following GitHub Copilot agent skill spec.
- **Generic:** Agent-agnostic markdown files at `.spek/skills/` (agent must be configured to load them).

**Skill file structure (all integrations):**

Each generated skill file must contain:

```markdown
# /spek.prepare

## Purpose
[One line: what this skill does]

## When to invoke
[Triggers and preconditions]

## Steps
[Numbered, exact sequence the agent executes]
1. [Specific action — tool call, file read, skill invocation]
2. [...]

## Tool Permissions Required
[List each tool the agent must have permission to use]
- lat.md MCP: lat_symbols, lat_references, lat_sync
- Filesystem: read/write .spek/vault/, read .specify/

## Third-Party Tool Usage
[Exact syntax for each external tool]

### lat.md
- Index code: `lat_sync --path .`
- Index docs: `lat_sync --path .spek/vault/ --mode docs`
- Query: `lat_symbols <symbol>`, `lat_references <symbol>`

### SpecKit
- Invoke: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`

### Obsidian CLI (required — all vault operations)
- Read note: `obsidian read --vault .spek/vault/ --note decisions.md`
- Write/create note: `obsidian write --vault .spek/vault/ --note lessons/YYYY-MM-DD-feature.md`
- Append to note: `obsidian append --vault .spek/vault/ --note decisions.md`
- Export vault: `obsidian export --vault .spek/vault/ --format json`

### Caveman (if Claude integration)
- Activate: `/caveman full`

## Output
[What artifacts are created, where they are stored]
```

**Why explicit tool instructions matter:** Agent skills need to know the exact MCP tool names, filesystem paths, and command syntax for each third-party tool. Without this, the agent will hallucinate or fail silently. `spek init` must generate skill files with complete, accurate tool interaction instructions for the chosen integration.

---

### SpecKit (`.specify/`)

`spek init` runs `specify init .` which creates:

```
.specify/
├── memory/constitution.md     ← Project principles (edit to add domain constraints)
├── extensions.yml             ← Hook system (Spekificity registers enrichment skills here)
└── templates/                 ← Spec/Plan/Task templates (override if needed; defaults work)
```

`spek init` is idempotent — safe to re-run. Existing config preserved.

---

## Post-Installation: Commit to Git

```bash
git add .spek/ .specify/ .claude/
git commit -m "Initialize Spekificity: vault, skills, SpecKit, lat.md"
```

---

## Configuration Reference

### `.spek/config.yaml`

```yaml
tools:
  speckit:
    enabled: true
    mode: global

  code_analysis:
    enabled: true
    tool: lat.md
    mode: global

  vault:
    enabled: true
    location: .spek/vault/

context_loading:
  enable_cache: true
  cache_expiry_minutes: 60

token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000
```

---

## Troubleshooting

### Install Issues

- **`spek: command not found`** → Not installed. Run: `uv tool install spekificity --from git+...`
- **Python 3.11+ missing** → Install from [python.org](https://python.org)
- **Git not found** → Install from [git-scm.com](https://git-scm.com)
- **`uv` not in PATH** → Ensure `~/.cargo/bin` or `~/.local/bin` in PATH

### Per-Project Init Issues

- **`spek init` fails with git error** → Not a git repo. Run `git init` first.
- **`.spek/vault/` missing** → Init didn't complete. Re-run `spek init`
- **`.specify/` missing** → SpecKit installation failed. Check npm/Python; re-run `spek init`
- **Skill files missing** → Check `.claude/commands/` (or appropriate dir for integration). Re-run `spek init`
- **Dependency installation fails** → Check npm, Python paths accessible; retry `spek init`

### Vault Issues

- **Agent says vault does not exist** → Check `.spek/vault/` exists. Re-run `spek init` if missing
- **Obsidian shows no nodes** → Open `.spek/vault/` as vault root, not project root
- **Wrong vault path** → Vault is at `.spek/vault/`. Not `vault/` at project root.

---

## What's Next

Setup complete.

1. Run `/spek.prepare` in agent (initializes lat.md indexes + vault context)
2. See [wiki/workflow.md](workflow.md) for 4-stage feature workflow
3. See [wiki/skills.md](skills.md) for `/spek.*` skill reference

---

## External Resources

- [SpecKit](https://github.com/github/spec-kit) — Spec-driven workflow engine
- [lat.md](https://github.com/langchain-ai/lat-md) — Code and doc analysis tool
- [Obsidian CLI](https://obsidian.md/help/cli) — Required for all vault read/write operations
- [Obsidian Desktop](https://obsidian.md) — Optional, graph visualization only
- [Caveman](https://github.com/marcelrienks/caveman) — Token compression skill
