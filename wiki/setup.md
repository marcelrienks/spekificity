# Setup Guide: Installation & Configuration

Complete walkthrough for installing and configuring Spekificity.

---

## Overview

Spekificity integrates three core tools. `spek init` handles all setup automatically:

| Tool | Purpose | Configured By | Status |
|------|---------|---------------|--------|
| **Spekificity** | Agent skill framework + orchestration | `spek init` (automatic) | Runs in project |
| **SpecKit** | Spec-driven workflow engine | `spek init` (automatic) | Global install + per-project init |
| **lat.md** | Code analysis & indexing | `spek init` (automatic) | Per-project index |
| **Obsidian Vault** | Git-backed knowledge base | `spek init` (automatic) | Per-project directory |
| **Obsidian CLI** | Vault automation (exports, graph) | Manual install required | Global/Path |

---

## Prerequisites

Before running `spek init`, ensure:

- **Python 3.11+** — `python3 --version`
- **Git** — `git --version` + project must be a git repository (`git init` if needed)
- **`uv` package manager** — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Obsidian CLI** — Install Obsidian desktop app or standalone CLI. Required for `/spek.conclude` automation. See [obsidian.md/help/cli](https://obsidian.md/help/cli) for platform-specific instructions.
- **Internet access** for initial tool installation

---

## Installation & Initialization

### Step 1: Install Spekificity Globally

```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

Verify:
```bash
which spek
spek --version
```

### Step 2: Navigate to Your Project

```bash
cd /path/to/your/project
# Ensure git is initialized
git status  # Should show a valid repo, not "not a git repository"
```

### Step 3: Run `spek init` (One Command)

```bash
spek init
```

**What this does automatically:**

1. ✅ **Installs SpecKit globally** (if not already present) via `uv tool install specify-cli`
2. ✅ **Initializes SpecKit per-project** by running `specify init .` (creates `.specify/`)
3. ✅ **Creates vault structure** (`vault/` with lessons/, decision.md, patterns.md, vision.md)
4. ✅ **Scaffolds Spekificity skills** (`.spek/` with generated `/spek.*` commands)
5. ✅ **Initializes lat.md index** (`.lat/` directory with code graph)
6. ✅ **Creates specs directory** (`specs/` for feature specifications)
7. ✅ **Verifies dependencies** (checks for Obsidian CLI, git, Python, uv)
8. ✅ **Reports readiness** (summary of created directories and next steps)

### Step 4: Verify Installation

```bash
# Check Spekificity
spek --help
spek --version

# Check SpecKit integration
ls .specify/
# Expected: extensions.yml  memory/  scripts/  templates/

# Check vault
ls vault/
# Expected: decision.md  lessons/  patterns.md  vision.md

# Check lat.md
ls .lat/
# Expected: (depends on lat.md version; typically index files)

# Check specs
ls specs/
# Expected: (empty until features are created)
```

---

## Post-Installation Configuration

### SpecKit Configuration (`.specify/`)

After `spek init` completes, customize SpecKit behavior (optional):

- **`.specify/memory/constitution.md`** — Project principles. Edit to add domain-specific constraints.
- **`.specify/extensions.yml`** — Hook system. Spekificity registers enrichment skills here automatically.
- **`.specify/templates/`** — Override default templates for specs, plans, tasks if needed.

**Note:** `spek init` is **idempotent** — safe to run multiple times. Existing config preserved, templates updated.

### SpecKit Upgrade Path

After upgrading SpecKit:

```bash
# Upgrade SpecKit globally
uv tool upgrade specify-cli

# Re-run spek init to pull new templates
spek init
```

Existing configurations are preserved; only templates updated.

---

## Tool 2: Obsidian Vault (Git-Backed Knowledge Base)

The Obsidian vault is your persistent memory layer—lessons learned, decisions, patterns, and project context stored as plain markdown files. Spekificity agents read and write to this vault directly as the authoritative knowledge base.

**Obsidian CLI Requirement:** Spekificity automation (e.g., `/spek.conclude`) requires the Obsidian CLI for vault exports and graph generation. Install the Obsidian desktop app (includes CLI). The desktop app UI is optional for visualization; CLI is required for automation.

### Vault Location in Spekificity

```
your-project/
├── vault/                              ← Persistent knowledge vault (auto-created by spek init)
│   ├── lessons/                        ← Per-feature lessons (written by /spek.conclude)
│   │   └── YYYY-MM-DD-feature-name.md  ← Lesson file naming: date + feature name
│   ├── decision.md                     ← Architectural decisions and rationale
│   ├── patterns.md                     ← Reusable patterns and best practices
│   └── vision.md                       ← Project vision and guiding principles
├── specs/                              ← Feature specifications (created by /speckit.specify)
│   ├── NNNN-feature-name.md            ← Spec files: numeric prefix + kebab-case name
│   └── NNNN-feature-name-plan.md       ← Plan files: spec name + "-plan"
└── wiki/                               ← Documentation, guides, and reference
    ├── architecture.md
    ├── conventions.md
    ├── setup.md
    ├── workflow.md
    └── [other guides]
```

### Vault Initialization (Automatic via `spek init`)

`spek init` creates the vault structure automatically — no manual setup needed.

Created structure:
```
vault/
├── lessons/                 ← Per-feature retrospectives
├── decision.md              ← Architectural decisions (append-only)
├── patterns.md              ← Reusable patterns
└── vision.md                ← Project vision + principles
```

**Do NOT create vault files manually.** `spek init` handles all scaffolding.

### Vault: Plain Markdown Files

**The vault is plain markdown on your filesystem.** Agents access via file I/O.

- ✅ **Agents work without Obsidian desktop** — Read/write `.md` files directly via filesystem
- ✅ **Vault is fully git-tracked** — All vault files version-controlled; commit via `git add vault/; git commit -m "..."`
- ✅ **Editor-agnostic** — Edit with any markdown editor or command-line tools
- ✅ **Obsidian CLI required** — Enables vault automation (exports, graph generation) in `/spek.conclude`
- ℹ️ **Obsidian desktop optional** — Use only for graph visualization or interactive UI (not required for CLI automation)

### Optional: Obsidian Desktop App (For Visualization)

If you want graph visualization and interactive backlink browsing (optional, not required for automation):

#### macOS
1. Download from [obsidian.md/download](https://obsidian.md/download) or: `brew install obsidian`
2. Launch Obsidian
3. Select **Open folder as vault**
4. Navigate to `your-project/vault/` and select it
5. Obsidian will index and build the graph view

#### Windows/Linux
1. Download from [obsidian.md/download](https://obsidian.md/download)
2. Install and launch Obsidian
3. Select **Open folder as vault**
4. Navigate to `your-project/vault/` and select it

#### Configuration (Optional)

No configuration required for agent-only use. The `.obsidian/` directory is created automatically by the app on first open and can be committed to git to preserve graph layout settings.

**Safe to gitignore:**
- `vault/.obsidian/workspace.json` — Window/panel layout (regenerates)
- `vault/.obsidian/cache` — Link index cache (regenerates)

These are already excluded in the project `.gitignore`.

### Troubleshooting

- **Obsidian shows no graph nodes** → Ensure you opened `vault/` as the vault root, not the project root
- **Backlinks missing after agent writes** → Close and reopen vault to trigger re-indexing
- **Agent says vault does not exist** → Confirm `vault/` is present; if not, run `spek init` again

---

## Tool 3: lat.md (Code Analysis — Canonical via `spek init`)

Spekificity requires `lat.md` for code indexing and querying. It is the canonical, only-supported code analysis tool.

`lat.md` provides:
- Pre-indexed code symbols, definitions, relationships (no file scans)
- Incremental refresh + optional file-watcher for real-time updates
- MCP tool interface for agent-friendly queries (lat_symbols, lat_references, lat_callers, lat_impact, etc.)
- Pluggable extractors (framework-aware for Go, Python, TypeScript, etc.)

### Installation & Setup

`spek init` handles lat.md installation and initialization automatically:

1. **Installs globally** (if not present): `uv tool install lat-md`
2. **Initializes per-project**: Creates `.lat/` directory with index
3. **Configures MCP tools**: Registers with agent environment
4. **Runs initial index**: Scans codebase, creates symbol database

No manual commands needed. Verify post-initialization:

```bash
lat.md --version
lat.md query --help
ls .lat/
```

---

## Post-Installation Verification & Commit

After `spek init` completes:

```bash
# Verify all directories created
ls -la | grep -E '\.spek|vault|\.lat|specs|\.specify'

# Check key files
ls vault/               # decision.md, patterns.md, vision.md, lessons/
ls .spek/               # Generated skills
ls .specify/            # SpecKit config
ls .lat/                # Code index

# Commit to git
git add vault/ .spek/ .specify/ .lat/ specs/
git commit -m "Initialize Spekificity: vault, skills, SpecKit, lat.md index"
```

---

## Next Steps

Ready to start feature development:

1. **Load context:** `/spek.prepare` — workspace ready, vault synced, lat.md fresh
2. **Create spec & plan:** `/spek.plan --feature="feature-name"` — orchestrates SpecKit
3. **Implement:** `/spek.implement` — execute tasks with full context
4. **Archive:** `/spek.conclude` — save lessons, refresh graph, update vault

See [wiki/workflow.md](../workflow.md) for complete workflow guide.

---

## Configuration Reference

### .spek/config.yaml Template

```yaml
tools:
  speckit:
    enabled: true
    mode: global  # installed globally via uv
  
   code_analysis:
      enabled: true
      tool: lat.md
      mode: global
  
  vault:
    enabled: true
    location: vault/
    mode: local

context_loading:
  enable_cache: true
  cache_expiry_minutes: 60
  model: "<model-name>"
  temperature: 0.3
  max_tokens_output: 2000

token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000
```

---

## Troubleshooting

### `spek init` Issues

- **`spek: command not found`** → Ensure Spekificity installed: `uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git`; check PATH: `echo $PATH | grep .local/bin`
- **`spek init` fails with git error** → Ensure project is a git repo: `git status` should work; if not, run `git init` first
- **Obsidian CLI not found** → Install Obsidian desktop app or CLI separately. See [obsidian.md/help/cli](https://obsidian.md/help/cli). Required for `/spek.conclude` automation.
- **SpecKit installation fails** → Ensure Python 3.11+ and `uv` installed: `python3 --version` and `uv --version`
- **lat.md index error** → Usually transient. Re-run `spek init`. If persists, check disk space and file permissions.

### General Prerequisites

- **Python 3.11+ not found** → `python3 --version` should show ≥3.11. Install from python.org or use system package manager.
- **`uv` not in PATH** → After installing uv: `~/.cargo/bin/uv --version`. If not in PATH, add `~/.cargo/bin` to PATH or reinstall.
- **Permission errors** → On Linux/macOS: ensure user can write to project directory: `ls -ld . | head -c 1` should show `d`.
- **Internet connectivity** → `ping github.com` to verify. Tools install from GitHub; offline setup not supported initially.

### After `spek init` Completes

- **Vault dir missing** → Check: `ls vault/`. If not present, re-run `spek init`.
- **`.specify/` missing** → Check: `ls .specify/`. SpecKit may not have installed. Verify: `which specify` and `specify --version`. Run `spek init` again.
- **`.lat/` index incomplete** → lat.md may still be building. Wait a moment, then check: `ls .lat/` and `lat.md --version`.
- **Can't run `/spek.*` commands** → Ensure skills are generated in `.spek/`. Check: `ls .spek/skills/`. If empty, re-run `spek init`.

---

## See Also

- [wiki/workflow.md](../workflow.md) — Start here after setup completes
- [wiki/skills.md](../skills.md) — `/spek.*` command reference
- [github.com/github/spec-kit](https://github.com/github/spec-kit) — SpecKit documentation
- [obsidian.md/help/cli](https://obsidian.md/help/cli) — Obsidian CLI setup
