# Spekificity Installation & Setup Guide

This guide covers installing Spekificity and configuring it for AI-driven development workflows.

## Quick Start (Recommended)

### 1. Install via `uv tool install`

```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

This installs Spekificity as a standalone tool with:
- ✅ Main CLI (`spek` command)
- ✅ Initialization utility (`spek-init` command)
- ✅ All dependencies pre-configured
- ✅ Ready for immediate use

### 2. Initialize Your Project

After installation, initialize your project:

```bash
# Using spek init command
spek init

# Or as standalone command
spek-init

# Verbose output for debugging
spek init --verbose
```

This automatically creates:
- ✅ `vault/` - Obsidian vault for ALL persistent memory (Git-backed)
  - `vault/user/` - User preferences
  - `vault/session/` - Session and feature state
  - `vault/repo/` - Repository decisions and patterns
  - `vault/lessons/` - Per-feature lessons learned
- ✅ `.spek/` - Project metadata and CodeGraph database
- ✅ `wiki/` - Documentation structure

Then runs `specify init .` to initialize SpecKit in your project.

**Optional:** Open the `vault/` directory in Obsidian for graph visualization and knowledge browsing:
1. Open Obsidian
2. Click "Open folder as vault"
3. Select your project's `vault/` directory
4. Use Obsidian's graph view, search, and plugins

### 3. Verify Installation

```bash
# Check CLI is available
spek --version
spek --help

# Verify all commands
spek prepare --help
spek context --help
spek plan --help
spek map --help
spek implement --help
spek post --help
spek lessons --help
spek tools --help
spek init --help
```

### 4. Start Using Spekificity

```bash
# 1. Prepare workspace
spek prepare

# 2. Load project context
spek context

# 3. Plan a feature
spek plan "Add user authentication"

# 4. Analyze code graph
spek map --symbol UserService

# 5. Execute tasks
spek implement

# 6. Archive outcomes
spek post

# 7. Extract lessons
spek lessons
```

---

## Detailed Installation Steps

### Prerequisites

- **Python 3.11+** (required)
- **uv** package manager (recommended)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Or via Homebrew: `brew install uv`

### Installation Methods

#### Method 1: Via `uv tool install` (Recommended)

```bash
# Install from GitHub repository
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# Verify installation
spek --version
```

**Advantages:**
- Isolated environment (doesn't pollute system Python)
- Easy to update: `uv tool upgrade spekificity`
- Easy to remove: `uv tool uninstall spekificity`
- Perfect for CI/CD and team collaboration

#### Method 2: Via pip (Local Development)

```bash
# Clone the repository
git clone https://github.com/marcelrienks/spekificity.git
cd spekificity

# Install in development mode
pip install -e .

# Verify
spek --version
```

#### Method 3: Via pip with GitHub URL

```bash
pip install git+https://github.com/marcelrienks/spekificity.git
```

---

## Post-Installation Setup

### Automatic Setup (Recommended)

```bash
spek init
```

This interactive setup wizard:
1. Creates necessary directories
2. Initializes CodeGraph database
3. Detects SpecKit installation
4. Initializes SpecKit if available
5. Provides next steps

### Manual Setup

If you prefer manual control:

```bash
# Create directories
mkdir -p .spek vault/{user,session,repo,lessons} wiki/{specs,lessons}

# Initialize CodeGraph
python -c "from spekificity.graph.codegraph import CodeGraph; CodeGraph()"

# Initialize SpecKit (optional)
specify init .
```

### Configure External Tools

#### SpecKit (Optional but Recommended)

SpecKit enables AI-powered specification generation. Install with:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Or let `spek init` handle it automatically.

#### CodeGraph

CodeGraph is included by default. It automatically:
- Creates SQLite database at `.spek/codegraph.db`
- Indexes Python symbols via AST analysis
- Provides query interface for agents

---

## Installation Troubleshooting

### Issue: `spek` command not found after installation

**Solution:**
```bash
# Verify uv installation
uv --version

# Reinstall spekificity
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git --force

# Check installation location
which spek
```

### Issue: SpecKit installation fails

**Solution:**
```bash
# Skip SpecKit during init
spek init --skip-speckit

# Install SpecKit separately
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Then run SpecKit init manually
specify init .
```

### Issue: CodeGraph database permission error

**Solution:**
```bash
# Ensure .spek directory exists
mkdir -p .spek

# Check permissions
ls -la .spek/

# Reinitialize CodeGraph
spek init --skip-speckit
```

### Issue: Python version mismatch

**Solution:**
```bash
# Check Python version
python --version

# Must be 3.11 or higher
# Update Python using your package manager
# macOS: brew install python@3.11
# Ubuntu: sudo apt-get install python3.11
# Windows: Download from python.org
```

---

## Configuration

### Environment Variables

```bash
# Enable verbose logging
export SPEKIFICITY_VERBOSE=1

# Set custom project root
export SPEKIFICITY_ROOT=/path/to/project

# Set custom .spek directory
export SPEK_DIR=/path/to/.spek
```

### Project Configuration

Configuration files (stored in vault/):
- `vault/user/preferences.md` - User preferences
- `vault/session/*.yaml` - Session and feature state
- `vault/repo/*.md` - Repository decisions and patterns
- `wiki/specs/` - Specification files
- `wiki/lessons/` - Lesson extraction outputs

---

## Next Steps After Installation

### 1. Configure Your Workspace

```bash
spek prepare --feature-name "my-feature"
```

### 2. Load Project Context

```bash
spek context --layer all
```

### 3. Create Your First Feature

```bash
spek plan "Implement feature X"
```

### 4. Query Code Graph

```bash
spek map --symbol MyClass
spek tools --list
```

### 5. Integrate with Your Workflow

See [workflow.md](workflow.md) for workflow integration patterns.

---

## Integration with AI Agents

Spekificity is designed to work with AI agents via MCP (Model Context Protocol):

```python
from spekificity.mcp.client import get_mcp_client

# Get MCP client (singleton)
client = get_mcp_client()

# Query CodeGraph
result = client.lookup_symbol("UserService")
result = client.find_references("authenticate")
result = client.analyze_impact("Config")

# Use with agents
available_tools = client.get_available_tools()
```

Or via CLI:

```bash
spek tools --list
spek tools --tool lookup_symbol --symbol UserService
spek tools --tool analyze_impact --symbol Config --format json
```

---

## Uninstallation

### Remove via `uv`

```bash
uv tool uninstall spekificity
```

### Clean up local files

```bash
# Remove project metadata and vault memory
rm -rf .spek vault

# Remove documentation (optional)
rm -rf wiki/lessons
```

---

## Support & Documentation

- **Quick Reference:** [quickstart.md](quickstart.md)
- **Full Documentation:** See this `wiki/` directory
- **Issues & Discussions:** GitHub Issues
- **Contributing:** See CONTRIBUTING.md

---

## Architecture Overview

```
Installation via uv
        ↓
┌───────────────────────────────────────┐
│  spekificity package installed        │
│  - spek CLI command                   │
│  - spek-init initialization utility   │
│  - All dependencies ready             │
└───────────────────────────────────────┘
        ↓
Run: spek init
        ↓
┌───────────────────────────────────────┐
│  Post-Installation Setup              │
│  - Create .spek directory             │
│  - Initialize CodeGraph               │
│  - Install SpecKit (if available)     │
│  - Run specify init .                 │
└───────────────────────────────────────┘
        ↓
Project Ready for Use
        ↓
Run: spek prepare → plan → implement → post
```

---

## Version Information

- **Current Version:** 0.1.0-alpha.1
- **Python Required:** 3.11+
- **License:** MIT

---

## FAQ

### Q: Can I use Spekificity with an existing project?

**A:** Yes! Install Spekificity and run `spek init` in your project directory. It will integrate with your existing codebase.

### Q: Does Spekificity require SpecKit?

**A:** No, SpecKit is optional. Core functionality works without it. The `spek plan` command benefits from SpecKit.

### Q: Can I use Spekificity offline?

**A:** Mostly yes. The CodeGraph and core CLI work offline. SpecKit commands may require online validation.

### Q: How do I update Spekificity?

**A:** 
```bash
uv tool upgrade spekificity
```

### Q: Can multiple projects use the same Spekificity installation?

**A:** Yes! Each project has its own `.spek/` and `vault/` directories, so they work independently.

### Q: Is Spekificity compatible with Windows?

**A:** Yes, but some features (git operations, shell commands) work best on Unix-like systems (macOS, Linux). On Windows, use WSL2 for best compatibility.

---

## Feedback & Contributions

We'd love to hear from you! Please:
- 📝 Report issues on GitHub
- 💡 Suggest improvements
- 🤝 Contribute code or documentation
- 📢 Share your workflows

See CONTRIBUTING.md for details.
