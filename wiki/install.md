
# Spekificity Installation & One-Stop Setup Guide

This guide covers fully automated setup for Spekificity, including all system and Python dependencies.

## One-Stop Setup (Recommended)

### 1. Run the Bootstrap Script

Use the provided `setup.sh` script to check for and install all requirements:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- Check for Python 3.11+ (install if missing)
- Check for `uv` (install via pipx if missing)
- Check for Git (install if missing)
- Check for Obsidian (install via Homebrew, Chocolatey, or prompt manual install)
- Verify Obsidian CLI availability (bundled with the Obsidian app). The script checks that the `obsidian` command is registered in PATH and will print guidance to enable it if missing. For CI/headless alternatives see: https://obsidian.md/help/headless
- Install Spekificity and all Python dependencies via `uv tool install`
- Initialize your project with `spek init`

**No manual steps required.**

### 2. Open the Vault in Obsidian (Optional)

After setup, open the `vault/` directory in Obsidian for graph visualization and knowledge browsing:
1. Open Obsidian
2. Click "Open folder as vault"
3. Select your project's `vault/` directory
4. Use Obsidian's graph view, search, and plugins

### 3. Verify Installation

```bash
spek --version
spek --help
spek prepare --help
spek context --help
```

---

**Note:** The `setup.sh` script is cross-platform (macOS, Linux, Windows) and will prompt for any manual steps if a dependency cannot be installed automatically.
spek map --help
spek implement --help
spek conclude --help
spek lessons --help
spek tools --help
```

### 4. Start Using Spekificity

```bash
# 1. Prepare workspace

# 2. Load project context
spek context

# 3. Plan a feature
spek plan "Add user authentication"

# 4. Analyze code graph
spek map --symbol UserService

# 5. Execute tasks
spek implement

# 6. Archive outcomes
spek conclude

# 7. Extract lessons
spek lessons
```
---

## Detailed Installation Steps

### Prerequisites
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

- Perfect for CI/CD and team collaboration

#### Method 2: Via pip (Local Development)

```bash
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
2. Initializes the lat.md index
3. Detects SpecKit installation
4. Initializes SpecKit if available
5. Provides next steps

### Manual Setup

If you prefer manual control:

```bash
# Create directories
mkdir -p .spek vault/{user,session,repo,lessons} wiki/{specs,lessons}

# Initialize lat.md index
python -c "from spekificity.graph.lat_index import LatIndex; LatIndex()"

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


- Provides a markdown-first code + doc index and MCP query interface for agents
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

### Issue: lat.md index permission error

**Solution:**
```bash
# Ensure .spek directory exists
mkdir -p .spek

# Check permissions
ls -la .spek/

# Reinitialize lat.md index
spek init --skip-speckit
```

### Issue: Python version mismatch

**Solution:**
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

# Query lat.md
result = client.lookup_symbol("UserService")
result = client.find_references("authenticate")
result = client.analyze_impact("Config")

available_tools = client.get_available_tools()
```

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
- **Contributing:** See [wiki/specs/152-contributing-and-onboarding-spec.md](specs/152-contributing-and-onboarding-spec.md)

## Architecture Overview

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
│  - Initialize lat.md index               │
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
- **License:** MIT
---

## FAQ

### Q: Can I use Spekificity with an existing project?

**A:** Yes! Install Spekificity and run `spek init` in your project directory. It will integrate with your existing codebase.

### Q: Does Spekificity require SpecKit?

**A:** No, SpecKit is optional. Core functionality works without it. The `spek plan` command benefits from SpecKit.

### Q: Can I use Spekificity offline?

**A:** Mostly yes. The lat.md index and core CLI work offline. SpecKit commands may require online validation.

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

- 📢 Share your workflows

See [wiki/specs/152-contributing-and-onboarding-spec.md](specs/152-contributing-and-onboarding-spec.md) for details.
