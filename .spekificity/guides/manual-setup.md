# Manual Setup Guide: Step-by-Step for Developers

**Purpose**: Manual steps for setting up spekificity without automation (useful for learning, debugging, or restricted environments).

## Prerequisites

Verify you have:
- macOS or Linux (Windows: WSL2)
- Python 3.11 or higher
- Terminal/shell (bash/zsh)
- Git (for version control)

Check:
```bash
python3 --version        # Should show 3.11 or higher
git --version           # Should show 2.x or higher
```

---

## Step 1: Create Project Structure

```bash
# Go to project root
cd /path/to/project

# Create spekificity directory
mkdir -p .spekificity/{setup-scripts,skills,workflows,guides,bin}

# Create specs directory (for feature documentation)
mkdir -p specs/001-spekificity-platform

# Create speckit directory (if not exists)
mkdir -p .specify .github/agents
```

---

## Step 2: Install Global Tools

### Install uv (package manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:
```bash
uv --version
```

### Install speckit/specify

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Verify:
```bash
specify --version
```

### Install graphify

```bash
uv tool install graphifyy
```

Verify:
```bash
graphify --version
```

### Install Python 3.11+ (if needed)

**macOS**:
```bash
brew install python@3.11
```

**Ubuntu/Debian**:
```bash
sudo apt update && sudo apt install -y python3.11
```

Verify:
```bash
python3.11 --version
```

---

## Step 3: Initialize Git

If not already a git repository:

```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create initial commit
git add .gitignore
git commit -m "init: project setup"
```

---

## Step 4: Copy Spekificity Files

Copy from reference spekificity project:

```bash
# Option A: Copy from repo (if you have access)
cp -r /path/to/spekificity/.spekificity ./

# Option B: Create files manually (see below)
# Option C: Create minimal version then run setup
```

**What to copy**:
- `.spekificity/setup-scripts/` — All shell scripts
- `.spekificity/skills/` — Skill markdown files
- `.spekificity/guides/` — Documentation
- `.spekificity/bin/spek` — Main dispatcher
- `.spekificity/config-schema.json` — JSON schema
- `.spekificity/version.txt` — Version number

---

## Step 5: Create Configuration File

Create `.spekificity/config.json`:

```json
{
  "spek_version": "1.0.0",
  "spek_initialized": false,
  "spek_initialized_timestamp": null,
  "spek_platform_branch": "002-spek-platform-lifecycle",
  "spek_schema_version": "1.0.0",
  "tools": {
    "speckit": {
      "installed": false,
      "version": null,
      "initialized": false,
      "initialized_timestamp": null
    },
    "graphify": {
      "installed": false,
      "version": null,
      "initialized": false,
      "initialized_timestamp": null
    },
    "obsidian": {
      "installed": false,
      "available": false,
      "version": null,
      "initialized": false,
      "vault_path": null,
      "initialized_timestamp": null
    },
    "caveman": {
      "available": false,
      "integrated": false
    }
  },
  "skills": {
    "spekificity_installed": false,
    "speckit_installed": false,
    "caveman_available": false,
    "last_skill_index_update": null
  },
  "spek_custom_preferences": {},
  "orchestration_history": []
}
```

---

## Step 6: Initialize Speckit

```bash
# Navigate to project root
cd /path/to/project

# Run speckit initialization
specify init .
```

**Expected output**:
```
✓ Initialized specify framework
✓ Created .specify/ directory
✓ Installed speckit skills to .github/agents/
```

**Verify**:
```bash
ls .specify/              # Should have constitution.md, feature.json
ls .github/agents/        # Should have speckit.*.md files
```

---

## Step 7: Initialize Graphify

```bash
# Initialize graphify for codebase analysis
graphify init

# Generate initial graph
graphify analyze --output .obsidian/graph/
```

**Expected output**:
```
✓ Graph generated
✓ Stored in .obsidian/graph/index.md
```

**Verify**:
```bash
cat .obsidian/graph/index.md | head -20  # Should show graph structure
```

---

## Step 8: Setup Obsidian Vault (Optional)

If Obsidian app installed:

```bash
# Create vault structure
mkdir -p .obsidian/vault/{context,lessons}

# Create vault config
cat > .obsidian/vault-info.json << 'EOF'
{
  "vault_name": "Project Vault",
  "vault_path": ".obsidian/",
  "created": "2026-05-03",
  "version": "1.0.0"
}
EOF
```

Then open Obsidian:
1. Open Obsidian app
2. Open vault → select `.obsidian/` directory
3. View graph (should show codebase structure)

---

## Step 9: Install Spekificity Skills

Create skill files in `.spekificity/skills/`:

### Skill 1: Context Load

Create `.spekificity/skills/spek.context-load.md`:

```markdown
# Skill: Load Vault Context

**Command**: `/spek.context-load`

## Description

Load architectural decisions, patterns, and codebase graph from vault into AI context.

## Implementation

1. Read `.obsidian/graph/index.md` (codebase structure)
2. Read `vault/context/decisions.md` (architectural decisions)
3. Read `vault/context/patterns.md` (design patterns)
4. Format as markdown output
5. Return formatted context to AI

## Usage

```
/spek.context-load
```

Returns: Markdown formatted context for AI consumption.
```

### Skill 2: Map Codebase

Create `.spekificity/skills/spek.map-codebase.md`:

```markdown
# Skill: Map Codebase

**Command**: `/spek.map-codebase`

## Description

Analyze codebase and update dependency graph.

## Implementation

1. Run: `graphify analyze`
2. Output to: `.obsidian/graph/index.md`
3. Update vault index
4. Report changes

## Usage

```
/spek.map-codebase [--depth deep|shallow]
```

Returns: Updated graph markdown.
```

### Skill 3: Lessons Learned

Create `.spekificity/skills/spek.lessons-learnt.md`:

```markdown
# Skill: Capture Learning

**Command**: `/spek.lessons-learnt`

## Description

Capture what was learned during feature implementation.

## Implementation

1. Prompt for learning inputs
2. Format as structured markdown
3. Store in `vault/lessons/<date>-<feature>.md`
4. Return confirmation

## Usage

```
/spek.lessons-learnt
```

Returns: Confirmation of saved learning.
```

---

## Step 10: Generate Skill Index

Create `.spekificity/skill-index.md`:

```markdown
# Spekificity Unified Skill Index

**Last Updated**: 2026-05-03

## Spekificity Custom Skills

| Namespace | Command | Description | Status |
|-----------|---------|-------------|--------|
| spek | `/spek.context-load` | Load vault context | active |
| spek | `/spek.map-codebase` | Update codebase graph | active |
| spek | `/spek.lessons-learnt` | Capture learning | active |

## Speckit Skills

| Namespace | Command | Description | Status |
|-----------|---------|-------------|--------|
| speckit | `/speckit.specify` | Create feature spec | active |
| speckit | `/speckit.plan` | Create implementation plan | active |
| speckit | `/speckit.tasks` | Generate tasks | active |
| speckit | `/speckit.implement` | Execute implementation | active |

## Integration

- All skills available in AI chat (GitHub Copilot, Claude)
- Skills reference each other via namespace
- Execution order: `/spek.context-load` → `/speckit.*` workflow
```

---

## Step 11: Create Main Dispatcher

Create `.spekificity/bin/spek`:

```bash
#!/bin/bash

# Spekificity Platform Dispatcher
# Routes commands to setup/init/update/status

SPEK_VERSION="1.0.0"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SETUP_SCRIPTS_DIR="${PROJECT_ROOT}/.spekificity/setup-scripts"

# Source helpers
source "${SETUP_SCRIPTS_DIR}/logging.sh" 2>/dev/null || {
    echo "Error: logging.sh not found"
    exit 1
}

case "${1:-help}" in
    setup)
        exec "${SETUP_SCRIPTS_DIR}/setup.sh" "${@:2}"
        ;;
    init)
        exec "${SETUP_SCRIPTS_DIR}/init.sh" "${@:2}"
        ;;
    update)
        exec "${SETUP_SCRIPTS_DIR}/update.sh" "${@:2}"
        ;;
    status)
        exec "${SETUP_SCRIPTS_DIR}/status.sh" "${@:2}"
        ;;
    -h|--help|help)
        cat << 'HELP'
Spekificity Platform v1.0.0

Usage: spek <command> [options]

Commands:
  setup    Detect prerequisites and prepare environment
  init     Initialize all tools (speckit, graphify, obsidian, caveman)
  update   Update spekificity platform layer
  status   Show current initialization status

Options:
  -h, --help     Show this help
  --verbose      Enable verbose output

Examples:
  spek setup                # Check prerequisites
  spek init                 # Initialize platform
  spek status               # Show status
  spek status --json        # Show status as JSON

More info: .spekificity/guides/
HELP
        ;;
    *)
        log_error "Unknown command: $1"
        exec "${SETUP_SCRIPTS_DIR}/setup.sh" --help
        exit 1
        ;;
esac
```

Make executable:
```bash
chmod +x .spekificity/bin/spek
```

---

## Step 12: Test Installation

```bash
# Test main dispatcher
.spekificity/bin/spek setup

# Check status
.spekificity/bin/spek status

# Verify configuration
cat .spekificity/config.json | jq .
```

**Expected output**:
```
✓ Platform detected: macOS
✓ Python 3.11.6 installed
✓ uv 0.1.25 installed
✓ git 2.43.0 installed
✓ Setup complete
```

---

## Step 13: Test Skills

In your AI chat (GitHub Copilot or Claude):

```
/context-load
```

Expected: AI loads vault context (even if minimal).

```
/speckit.specify

Create a test feature
```

Expected: AI creates spec file (`.specify/feature.json` or equivalent).

---

## Step 14: Commit Setup

```bash
# Add all files
git add -A

# Commit
git commit -m "setup: spekificity platform initialization"

# Verify
git log --oneline -5
```

---

## Troubleshooting Manual Setup

| Issue | Solution |
|-------|----------|
| `Python 3.11 not found` | Install: `brew install python@3.11` (macOS) or `apt install python3.11` (Linux) |
| `uv not found` | Install: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `specify not found` | Install: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` |
| `Permission denied` on spek | Run: `chmod +x .spekificity/bin/spek` |
| Config validation fails | Delete `.spekificity/config.json` and re-run setup |

---

## Next Steps

1. ✅ **Setup complete**: Run `spek setup && spek init`
2. 🚀 **Start feature work**: Run `/context-load`
3. 📖 **Learn workflow**: Read `.spekificity/guides/architecture.md`
4. 🔄 **Run first feature**: Use `/speckit-enrich-specify`

---

**Manual setup complete!** You now have a working spekificity platform. Time to build features.
