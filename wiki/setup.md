# Setup Guide: Installation & Configuration

Complete walkthrough for installing and configuring Spekificity.

---

## Overview: Responsibility Division

Spekificity setup is split into two phases:

| Phase | Command | Responsibility | Scope |
|-------|---------|-----------------|-------|
| **Global Install** | `uv tool install spekificity ...` | Spekificity package resolves + installs all dependencies | Python environment, global PATH |
| **Per-Project Init** | `spek init` | Initialize project-local structures | Single project directory |

**Spekificity Global Install Handles:**
- ✅ Installs SpecKit globally (if not present)
- ✅ Installs lat.md globally (if not present)
- ✅ Verifies Python 3.11+, git, uv in PATH
- ✅ Warns if Obsidian CLI missing (needed for `/spek.conclude`, but non-blocking)
- ✅ All other tool dependencies resolved automatically

**spek init Handles:**
- ✅ Per-project initialization (one-time per project)
- ✅ Runs `specify init .` for SpecKit project setup
- ✅ Creates vault structure
- ✅ Creates .spek/ with generated skills
- ✅ Initializes lat.md per-project index
- ✅ Creates specs/ directory

---

## Prerequisites (Minimal)

**Only three things must exist before running Spekificity install:**

- **Python 3.11+** — Check: `python3 --version`. If missing, install from [python.org](https://python.org) or system package manager.
- **Git** — Check: `git --version`. If missing, install from [git-scm.com](https://git-scm.com) or system package manager.
- **`uv` package manager** — Check: `uv --version`. If missing: `curl -LsSf https://astral.sh/uv/install.sh | sh`

That's it. Everything else (SpecKit, lat.md, Obsidian CLI checks) resolved by Spekificity installer.

---

## Installation & Initialization

### Step 1: Global Install (Dependency Resolution)

**Spekificity installer automatically resolves all dependencies:**

```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

This single command:
1. ✅ Installs Spekificity CLI globally
2. ✅ Auto-installs SpecKit globally (if missing)
3. ✅ Auto-installs lat.md globally (if missing)
4. ✅ Verifies Python 3.11+, git, uv in PATH
5. ✅ Warns if Obsidian CLI not in PATH (can be installed later)
6. ✅ Reports which tools were installed vs already present

**Verify global install:**
```bash
spek --version
which spek specify lat.md  # All three should be in PATH
```

### Step 2: Per-Project Initialization

**Navigate to your project (must be a git repository):**

```bash
cd /path/to/your/project
git status  # Should show valid repo; if not: git init first
```

**Run spek init (one-time per project):**

```bash
spek init
```

**What spek init does (per-project setup only):**

1. ✅ Runs `specify init .` (SpecKit per-project configuration)
2. ✅ Creates `vault/` structure (lessons/, decision.md, patterns.md, vision.md)
3. ✅ Creates `.spek/` with generated `/spek.*` skills
4. ✅ Initializes `.lat/` per-project lat.md index
5. ✅ Creates `specs/` directory for feature specifications
6. ✅ Reports readiness and next steps

### Step 3: Verify Per-Project Setup

```bash
# Check project directories
ls -la | grep -E '\.spek|vault|\.lat|specs|\.specify'

# Detailed verification
ls .specify/  # Expected: extensions.yml memory/ scripts/ templates/
ls vault/     # Expected: decision.md lessons/ patterns.md vision.md
ls .lat/      # lat.md per-project index
ls specs/     # Empty until features created

# All systems ready
spek --help
```

---

## Post-Installation Configuration (Optional)

### Customize SpecKit (`.specify/` — per-project)

After `spek init`, optionally customize SpecKit (all defaults work, this is optional):

- **`.specify/memory/constitution.md`** — Project principles. Edit to add domain-specific constraints or project philosophy.
- **`.specify/extensions.yml`** — Hook system. Spekificity registers enrichment skills here automatically; can add custom hooks.
- **`.specify/templates/`** — Override default Spec/Plan/Task templates if needed (advanced; not required).

**Note:** `spek init` is **idempotent** — safe to run multiple times. Existing config preserved.

### Check Obsidian CLI (Optional but Recommended)

If `/spek.conclude` (lesson extraction, graph refresh) will be used, ensure Obsidian CLI is available:

```bash
obsidian --version
```

If missing, install via Obsidian desktop app or standalone CLI: [obsidian.md/help/cli](https://obsidian.md/help/cli)

(Optional but recommended; `/spek.conclude` will warn if missing but continue without it.)

### Tool Upgrades

Upgrade Spekificity or any included tool:

```bash
# Upgrade all tools to latest
uv tool upgrade spekificity

# Or upgrade individually
uv tool upgrade specify-cli
uv tool upgrade lat-md
```

After upgrading SpecKit, re-run `spek init` in each project to pull new templates:
```bash
spek init
```

(Safe; preserves existing configurations.)

---

## Understanding the Tools (Post-Installation Reference)

### Obsidian Vault (Git-Backed Knowledge Base)

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

### lat.md (Code Analysis & Indexing)

`lat.md` is installed globally by the Spekificity installer and initialized per-project by `spek init`. It is the canonical, only-supported code analysis tool.

`lat.md` provides:
- Pre-indexed code symbols, definitions, call graphs (no file scans needed)
- Incremental refresh + optional file-watcher for real-time updates
- MCP tool interface for agent-friendly queries (lat_symbols, lat_references, lat_callers, lat_impact, etc.)
- Framework-aware extractors (Go, Python, TypeScript, etc.)
- Per-project index stored in `.lat/` (created by `spek init`)

**Verify post-initialization:**

```bash
lat.md --version
lat.md query --help
ls -la .lat/  # Per-project index files
```

**Usage in Spekificity workflow:**
- `/lat.query` — Query code intelligence (symbols, references, impact)
- `/lat.sync` — Refresh code index after changes
- Automatic queries during `/spek.plan` and `/spek.implement` phases

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

### Global Install Issues (Dependency Resolution)

- **`spek: command not found`** → Spekificity not installed. Run: `uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git`. Then check PATH: `which spek`
- **Python 3.11+ not found** → Installer check fails. Run: `python3 --version`. Should show ≥3.11. Install from [python.org](https://python.org) or system package manager.
- **Git not found** → Installer check fails. Run: `git --version`. Install from [git-scm.com](https://git-scm.com) or system package manager.
- **`uv` not in PATH** → Installer check fails. Run: `uv --version`. If not found, ensure `~/.cargo/bin` or `~/.local/bin` (depending on uv version) in PATH.
- **SpecKit/lat.md auto-install fails** → Usually network issue. Check: `ping github.com`. Ensure internet access, then re-run: `uv tool install spekificity ...`
- **Obsidian CLI warning** → Not a blocker. Optional, needed only for `/spek.conclude` automation. Install later from [obsidian.md/help/cli](https://obsidian.md/help/cli) if needed.

### Per-Project Init Issues (`spek init`)

- **`spek init` fails with git error** → Project not a git repo. Run: `git status`. Should show valid repo. If not: `git init` first.
- **Vault dir missing** → `spek init` didn't complete. Check output for errors. Re-run: `spek init`
- **`.specify/` missing** → SpecKit per-project init failed. Verify: `which specify` and `specify --version`. Re-run: `spek init`
- **`.lat/` incomplete** → lat.md per-project index building. Wait a moment, then check: `ls .lat/` and `lat.md --version`. Disk space? Check: `df -h`
- **Can't run `/spek.*` commands** → Skills not generated. Check: `ls .spek/skills/`. If empty, re-run: `spek init`
- **Permission errors** → User can't write to project dir. Check: `ls -ld . | head -c 1` should show `d`. Fix permissions if needed.

### After Successful Setup

- **Verify everything working:** Run `/spek.prepare` and check output for any warnings
- **First feature workflow:** Run `/spek.plan --feature="test"` to validate spec generation
- **Token counts off?** Ensure lat.md index fresh: `lat.md --version` and check `.lat/` directory size (should be non-empty)

---

## Next: Start Using Spekificity

Once setup completes, you're ready:

1. Run `/spek.prepare` to initialize workspace context
2. See [wiki/workflow.md](../workflow.md) for complete feature development workflow
3. See [wiki/skills.md](../skills.md) for `/spek.*` command reference

## External Resources

- [SpecKit (GitHub official)](https://github.com/github/spec-kit) — Spec-driven workflow engine
- [lat.md](https://github.com/langchain-ai/lat-md) — Code analysis tool
- [Obsidian CLI](https://obsidian.md/help/cli) — Vault automation
- [Obsidian Desktop](https://obsidian.md) — Optional graph visualization
