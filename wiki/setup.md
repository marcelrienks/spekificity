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

## Tool 2: Knowledge Vault (Local Setup)

The knowledge vault (Obsidian-format markdown) stores lessons learned, decisions, patterns, and project context. Spekificity agents read and write to this vault directly as plain markdown files.

### Vault Location in Spekificity

```
your-project/
└── wiki/
    └── vault/
        ├── lessons/         ← written by /spek.conclude
        ├── context/         ← maintained by agent across sessions
        │   ├── decisions.md
        │   └── patterns.md
        └── graph/           ← populated by code analysis tool
```

### Initialization Steps

1. Create vault directory:
   ```bash
   mkdir -p wiki/vault/lessons
   mkdir -p wiki/vault/context
   mkdir -p wiki/vault/graph
   ```

2. Create initial vault files:
   ```bash
   # Decisions index
   touch wiki/vault/context/decisions.md
   
   # Patterns library
   touch wiki/vault/context/patterns.md
   ```

3. Verify vault structure:
   ```bash
   ls -R wiki/vault/
   # Expected: context/  lessons/  graph/
   cat wiki/vault/context/decisions.md
   # Expected: (file readable, even if empty)
   ```

### Important: Plain Markdown (No Obsidian App Needed)

**The vault is just markdown files on your filesystem.** Spekificity agents access it directly via file I/O. The Obsidian app is entirely optional:

- ✅ **Agents work without Obsidian** — They read/write `.md` files directly
- ✅ **Vault is fully git-committable** — Commit `wiki/vault/` to version control
- ⚠️ **Obsidian app is optional** — Use only if you want to browse backlinks or visualize the knowledge graph in a rich UI

### Optional: Obsidian Desktop App (Interactive UI)

If you want the interactive visualization and backlink browsing (optional):

#### macOS
1. Download from [obsidian.md/download](https://obsidian.md/download)
2. Open the `.dmg` and drag Obsidian to Applications
3. Launch Obsidian
4. Select **Open folder as vault**
5. Navigate to `your-project/wiki/vault/` and select it
6. Obsidian will index and build the graph view

#### Linux
1. Download the `.appimage` from [obsidian.md/download](https://obsidian.md/download)
2. Make executable: `chmod +x obsidian-*.appimage`
3. Run: `./obsidian-*.appimage`
4. Select **Open folder as vault** → navigate to `your-project/wiki/vault/`

#### Configuration (Optional)

No configuration required for agent-only use. The `.obsidian/` directory is created automatically by the app on first open and can be committed to git to preserve graph layout settings.

**Safe to gitignore:**
- `wiki/vault/.obsidian/workspace.json` — Window/panel layout (regenerates each app open)
- `wiki/vault/.obsidian/cache` — Link index cache (regenerates each app open)

These are already excluded in the project `.gitignore`.

### Troubleshooting

- **Obsidian shows no graph nodes** → Ensure you opened `wiki/vault/` as the vault root, not the project root
- **Backlinks missing after agent writes** → Close and reopen vault to trigger re-indexing
- **Agent says vault does not exist** → Confirm `wiki/vault/` is present; if not, run code analysis tool initialization

---

## Tool 3: Code Analysis Tool

Spekificity uses a code analysis tool to index your codebase and make it queryable for context injection during feature development. Two options are available:

### Current Recommendation: CodeGraph

CodeGraph (SQLite + MCP) is the recommended primary tool for Spekificity. It provides:
- Pre-indexed queries without file scanning overhead
- Built-in impact analysis tools
- Real-time sync on file changes
- Broad framework support

See [wiki/specs/codegraph-setup-and-integration.md](../specs/codegraph-setup-and-integration.md) for complete CodeGraph setup and integration details.

### Alternative: Graphify (Transition Reference)

Graphify is an alternative multi-language code indexing tool (legacy/transition reference). The CodeGraph approach is recommended for Spekificity integration.

#### Graphify Installation (If Chosen)

If you explicitly choose Graphify for your project:

1. **Check Python version:**
   ```bash
   python3 --version
   # Expected: 3.11 or higher
   ```

2. **Install via uv:**
   ```bash
   uv tool install graphifyy
   ```

3. **Verify installation:**
   ```bash
   graphify --version
   # Expected output: graphifyy x.x.x
   ```

4. **Initialize vault graph directory:**
   ```bash
   mkdir -p wiki/vault/graph/nodes
   mkdir -p wiki/vault/graph/cache
   ```

5. **Run initial full build:**
   ```bash
   graphify . --output jsonl --obsidian-dir wiki/vault/graph/nodes/
   ```

   This generates:
   - `wiki/vault/graph/nodes.jsonl` — Queryable graph
   - `wiki/vault/graph/graph.html` — Interactive visualization
   - `wiki/vault/graph/GRAPH_REPORT.md` — Human-readable summary

6. **Verify graph generated:**
   ```bash
   wc -l wiki/vault/graph/nodes.jsonl
   # Expected: 50+ lines (depends on codebase size)
   ```

#### Graphify Git Hook (Optional)

Auto-refresh the graph on every commit:

```bash
graphify hook install
```

This installs `.git/hooks/post-commit` that runs `graphify . --update` after each commit.

#### Graphify Configuration

Copy this template into `.spekificity/config.yaml` for Graphify:

```yaml
graphify:
  installation:
    mode: global  # "global" = uv tool; "local" = pip in venv
  
  code_generation:
    languages:
      - python
      - typescript
      - javascript
      - go
      - rust
    
    exclude:
      - "node_modules/**"
      - "venv/**"
      - ".venv/**"
      - "__pycache__/**"
      - "dist/**"
  
  caching:
    enabled: true
    cache_dir: graph/cache/
  
  output:
    primary_format: jsonl
    generate_html: true
  
  refresh:
    enable_git_hook: true
    watch_debounce_ms: 1000
  
  performance:
    parallel_enabled: true
    max_workers: 4
```

#### Graphify Usage

```bash
# Incremental refresh (only changed files)
graphify .

# Full rebuild (expensive, rarely needed)
graphify . --full

# Watch mode (auto-refresh on file save)
graphify . --watch

# Query the graph using jq:
jq '.[] | select(.name == "authenticate")' wiki/vault/graph/nodes.jsonl
```

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

3. **Verify Code Analysis Tool:**
   - If CodeGraph: See CodeGraph setup docs
   - If Graphify:
     ```bash
     graphify --version
     ls wiki/vault/graph/
     ```

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

### .spekificity/config.yaml Template

```yaml
tools:
  speckit:
    enabled: true
    mode: global  # installed globally via uv
  
  code_analysis:
    enabled: true
    tool: codegraph  # or "graphify"
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

- [wiki/specs/codegraph-setup-and-integration.md](../specs/050-codegraph-setup-and-integration.md) (recommended code analysis tool)
