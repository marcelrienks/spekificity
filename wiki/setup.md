# Setup Guide: Prerequisites and Tool Installation

This guide walks through installing and configuring the three core tools that Spekificity integrates.

---

## Overview

Spekificity requires three essential tools:

| Tool | Purpose | Install Mode | Required |
|------|---------|--------------|----------|
| **SpecKit** | Spec-driven workflow engine | Global | ✅ Required |
| **Knowledge Vault** | Markdown knowledge store | Local (project) | ✅ Required |
| **Code Analysis Tool** | Code indexing and graph | Local or Global | ✅ Required |

---

## Prerequisites (All Tools)

- **Python 3.11+** — Check with `python3 --version`
- **Git** — Check with `git --version`
- **`uv` package manager** — Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Internet access** for initial installation
- **Project folder** initialized as a git repository

---

## Tool 1: SpecKit (Global Installation)

SpecKit is the spec-driven development workflow engine. Spekificity wraps and enriches its commands; SpecKit remains unchanged and upgradable.

### Installation Steps

1. Install globally via `uv`:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. Verify installation:
   ```bash
   which specify
   # Expected: /users/<you>/.local/bin/specify or similar
   specify --version
   # Expected output: specify-cli x.x.x
   ```

3. Initialize SpecKit in your project:
   ```bash
   cd /path/to/your/project
   specify init .
   ```

   When prompted:
   - **AI Assistant**: Select your agent type (e.g., `copilot` for GitHub Copilot, `claude` for Claude Code)
   - **Script Type**: Select `sh`

   This creates:
   - `.specify/` — SpecKit configuration, templates, scripts, extensions
   - Agent-specific config files (varies by agent selection)

4. Verify SpecKit initialization:
   ```bash
   ls .specify/
   # Expected: extensions.yml  memory/  scripts/  templates/
   ```

### Configuration

SpecKit configuration lives in `.specify/`:

- **`.specify/extensions.yml`** — Hook definitions for `before_specify`, `before_plan`, `before_implement`, etc. Spekificity enrichment skills can be registered here.
- **`.specify/memory/constitution.md`** — Project constitution. Edit this to add project-specific principles.
- **`.specify/templates/`** — Override SpecKit default templates for spec, plan, and tasks.

### Re-Initialization

Running `specify init .` is **idempotent** — safe to run multiple times:
- If SpecKit is already initialized, it updates templates and scripts without overwriting your constitution or custom configuration.
- After upgrading SpecKit: run `uv tool upgrade specify-cli` then re-run `specify init .` to pick up new templates.

### Version Compatibility

| SpecKit version | Spekificity compatible | Notes |
|-----------------|----------------------|-------|
| ≥ 0.8.0 | ✓ | Extensions/hooks system required |
| 0.7.x | ⚠ | No extensions.yml; enrichment skills must be invoked manually |
| < 0.7.0 | ✗ | Unsupported |

### Troubleshooting

- **`specify: command not found`** → Run the install command above; ensure `~/.local/bin` is in your PATH
- **`specify init .` fails with git error** → Ensure the project folder is a git repository (`git init` first)
- **Hooks in `extensions.yml` not firing** → Check `enabled: true` and `optional: false`; confirm SpecKit ≥ 0.8.0
- **Templates not applied** → Check `.specify/templates/` for overrides; run `specify init .` again

---

## Tool 2: Obsidian Vault (Local Setup)

The Obsidian vault is your persistent memory layer—lessons learned, decisions, patterns, and project context stored as plain markdown files. Spekificity agents read and write to this vault directly as the authoritative knowledge base.

### Vault Location in Spekificity

```
your-project/
├── vault/                    ← Created automatically by spek init
│   ├── lessons/              ← written by spek conclude (per-feature lessons)
│   ├── patterns.md           ← reusable patterns discovered
│   ├── decision.md           ← architectural decisions and rationale
│   └── intention.md          ← project vision and guiding principles
├── vault/                  ← Persistent memory (Obsidian vault: user, session, repo, lessons)
└── wiki/                     ← Documentation specs and guides
```

### Automatic Initialization

When you run `spek init`, the vault is created automatically:

```bash
spek init
```

This creates:
- ✅ `vault/` directory with full structure
- ✅ `vault/lessons/` for per-feature lessons (one `.md` file per feature)
- ✅ `vault/patterns.md` — template for reusable patterns
- ✅ `vault/decision.md` — template for architectural decisions
- ✅ `vault/intention.md` — template for project vision

**You do not need to create vault files manually.**

### Important: Plain Markdown (No Obsidian App Required)

**The vault is just markdown files on your filesystem.** Spekificity agents access it directly via file I/O:

- ✅ **Agents work without Obsidian** — They read/write `.md` files directly
- ✅ **Vault is fully git-committable** — Commit `vault/` to version control
- ✅ **Tool-agnostic** — Use any markdown editor or command-line tools
- ⚠️ **Obsidian app is optional** — Use only if you want graph visualization or rich UI

### Optional: Obsidian Desktop App (Enhanced UI)

If you want the interactive visualization and backlink browsing (optional):

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

## Tool 3: Indexing Tool (lat.md)

Spekificity uses an indexing tool to make source code and documentation queryable for context injection during feature development. The recommended, canonical tool for this project is `lat.md`.

### Current Recommendation: lat.md

`lat.md` focuses on creating a Markdown-first knowledge layer that links specs, vault content, and source metadata. It provides:
- Markdown-native indexing (frontmatter, headings, wikilinks)
- Pluggable extractors for source symbols and basic dependency edges
- Incremental refresh and watch mode for fast updates
- Connectors for Obsidian-style vaults so documentation and code share a single graph
- Agent-friendly query interface (MCP or HTTP API) for context injection

See [wiki/specs/050-latmd-setup-and-integration.md](../specs/050-latmd-setup-and-integration.md) for complete lat.md setup and integration details.

---

## Post-Installation Verification

After installing all tools:

1. **Verify SpecKit:**
   ```bash
   specify --version
   ```

2. **Verify Vault:**
   ```bash
   ls wiki/vault/context/
   # Expected: decisions.md, patterns.md
   ```

3. **Verify Indexing Tool:**
   See lat.md setup docs for complete verification.

4. **Commit to Git:**
   ```bash
   git add wiki/vault/ .specify/
   git commit -m "Initialize Spekificity tools and vault"
   ```

---

## Next Steps

Once all tools are installed and verified:

1. Run `/spek.prepare` to initialize workspace and load context
2. Run `/spek.plan [feature description]` to begin a feature workflow
3. See [wiki/workflow.md](../workflow.md) for complete workflow documentation

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
    location: wiki/vault/
    mode: local

context_loading:
  enable_cache: true
  cache_expiry_minutes: 60
  model: "claude-haiku-4.5"
  temperature: 0.3
  max_tokens_output: 2000

token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000
```

---

## Troubleshooting

### General

- **Tool install fails** → Ensure Python 3.11+ and `uv` are installed
- **`PATH` issues** → Verify `~/.local/bin` is in your PATH: `echo $PATH`
- **Permission errors** → On Linux, ensure user permissions on project folder

### Tool-Specific

See individual tool sections above for tool-specific troubleshooting.

---

## See Also

- [wiki/specs/050-latmd-setup-and-integration.md](../specs/050-latmd-setup-and-integration.md) (recommended indexing tool)
