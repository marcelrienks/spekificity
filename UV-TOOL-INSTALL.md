# UV Tool Install Setup - Complete Reference

## Overview

Spekificity is now fully configured as a standalone tool installable via `uv tool install`. This enables one-command installation with automatic post-install setup.

---

## Quick Installation

```bash
# Install Spekificity as a tool
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# Initialize project
spek init

# Start using Spekificity
spek prepare
spek context
spek plan "Your feature"
```

**That's it!** All dependencies, directories, and configurations are set up automatically.

---

## What Gets Installed

### Entry Points

| Command | Purpose | Type |
|---------|---------|------|
| `spek` | Main CLI with 9 subcommands | Primary tool |
| `spek-init` | Standalone initialization utility | Post-install |

### Installed Components

✅ **Core CLI (spek)**
- prepare - Workspace initialization
- context - Load project context
- plan - SpecKit orchestration
- map - CodeGraph analysis
- implement - Task execution
- post - Outcome archival
- lessons - Retrospective analysis
- tools - MCP tool queries
- **init** - Project initialization (NEW)

✅ **Dependencies**
- click (CLI framework)
- pydantic (data validation)
- sqlalchemy (database)
- gitpython (git operations)
- loguru (logging)
- pygments (syntax highlighting)
- pyyaml (config files)
- jinja2 (templates)

✅ **Optional Features**
- SpecKit (auto-installed if available)
- CodeGraph (included by default)

---

## Post-Installation Setup

### Automatic Setup

```bash
# Single command initializes everything
spek init
```

This automatically:
1. Creates `.cel/` directory (project metadata)
2. Creates `.memories/session/` directory (session storage)
3. Creates `wiki/` directory structure
4. Initializes CodeGraph SQLite database
5. Checks for SpecKit and installs if needed
6. Runs `specify init .`

**Output:**
```
🚀 Initializing Spekificity project...

✓ Created memory structure in ./.memories
✓ Created wiki structure in ./wiki
✓ Created .cel directory at ./.cel
✓ CodeGraph initialized at ./.cel/codegraph.db
✓ SpecKit initialized successfully

✅ Spekificity initialization complete!

Next steps:
  1. Run: spek prepare           (Initialize workspace)
  2. Run: spek context           (Load project context)
  3. Run: spek plan [feature]    (Create specification & plan)
```

### Manual Setup (if needed)

```bash
# Skip SpecKit if not needed
spek init --skip-speckit

# Skip CodeGraph
spek init --skip-codegraph

# Verbose output
spek init --verbose

# Initialize specific directory
spek init --cwd /path/to/project
```

---

## Configuration

### pyproject.toml Entry Points

```toml
[project.scripts]
spek = "spekificity.cli.main:cli"           # Main CLI
spek-init = "spekificity.cli.init:execute"  # Init utility

[tool.uv]
# Configuration for uv tool install
# Usage: uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

### Optional Dependencies

```toml
[project.optional-dependencies]
speckit = ["specify-cli>=0.1.0"]           # SpecKit integration
codegraph = ["sqlalchemy>=2.0.0"]          # CodeGraph backend
integrations = ["specify-cli>=0.1.0"]      # All integrations
dev = [...]                                 # Development tools
```

---

## Usage After Installation

### Basic Workflow

```bash
# 1. Initialize workspace
spek prepare

# 2. Load project context
spek context

# 3. Plan a feature
spek plan "Add user authentication"

# 4. Analyze code graph
spek map --symbol UserService
spek map --dependencies

# 5. Execute implementation
spek implement

# 6. Archive outcomes
spek post

# 7. Extract lessons
spek lessons
```

### MCP Tools for Agents

```bash
# List available tools
spek tools --list

# Query symbols
spek tools --tool lookup_symbol --symbol UserService
spek tools --tool find_references --symbol authenticate
spek tools --tool analyze_impact --symbol Config

# Get statistics
spek tools --tool get_graph_stats --format json
```

---

## Version Management

### Update Spekificity

```bash
uv tool upgrade spekificity
```

### Check Installed Version

```bash
spek --version
# Output: Spekificity v0.1.0-alpha.1
```

### List Installed Tools

```bash
uv tool list
# Shows: spekificity 0.1.0-alpha.1 (spek, spek-init)
```

---

## Troubleshooting

### Issue: Commands not found after installation

**Solution:**
```bash
# Verify installation
uv tool list

# Reinstall if needed
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git --force

# Check PATH
echo $PATH
```

### Issue: spek-init not working

**Solution:**
```bash
# Use spek init instead
spek init

# Or explicitly run it
which spek-init
/path/to/spek-init
```

### Issue: SpecKit installation fails

**Solution:**
```bash
# Skip SpecKit during init
spek init --skip-speckit

# Install separately
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Re-run init
spek init
```

### Issue: Permission denied on `.cel` directory

**Solution:**
```bash
# Check permissions
ls -la .cel/

# Fix permissions
chmod 755 .cel/

# Reinitialize
spek init --skip-speckit
```

---

## Project Structure After Installation

```
your-project/
├── .cel/                          # Project metadata
│   ├── codegraph.db              # Symbol database
│   └── config.toml               # Project config
├── .memories/                     # Memory layers
│   ├── session/                  # Session data
│   ├── user.yaml                 # User preferences
│   └── repo.yaml                 # Repository facts
├── wiki/                          # Documentation
│   ├── specs/                    # Specifications
│   ├── lessons/                  # Lessons learned
│   └── *.md                      # Architecture docs
├── src/                          # Your project code
├── tests/                        # Your tests
├── .git/                         # Git repository
└── pyproject.toml                # Project config
```

---

## Integration Examples

### With AI Agents

```python
# Python API
from spekificity.mcp.client import get_mcp_client

client = get_mcp_client()
result = client.lookup_symbol("UserService")
result = client.find_references("authenticate")
```

### With CLI

```bash
# Get data for downstream processing
spek tools --tool get_graph_stats --format json | jq .

spek map --symbol Config --format json | jq .

spek context --layer all | grep -i "feature"
```

### With Workflows

```bash
#!/bin/bash
# Automated feature workflow

set -e

FEATURE="$1"

echo "🚀 Starting feature: $FEATURE"

# Prepare workspace
spek prepare --feature-name "$FEATURE"

# Load context
spek context

# Create plan
spek plan "$FEATURE"

# Execute
spek implement

# Archive
spek post --merge

# Extract lessons
spek lessons

echo "✅ Feature complete!"
```

---

## Key Features of uv Tool Install

✅ **Isolated Environment**
- No pollution of system Python
- Each tool has independent dependencies
- Clean uninstall: `uv tool uninstall spekificity`

✅ **Easy Updates**
- `uv tool upgrade spekificity`
- Always get latest version

✅ **Simple Sharing**
- Single installation command for teams
- Works consistently across platforms
- No installation guide needed

✅ **Automated Setup**
- Post-install initialization
- Creates directories automatically
- Installs dependencies as needed

✅ **Multiple Entry Points**
- `spek` for main CLI
- `spek-init` for setup utility
- Both available immediately after install

---

## Comparison with Other Installation Methods

| Method | Setup Time | Isolation | Updates | Complexity |
|--------|-----------|-----------|---------|-----------|
| **uv tool install** | 2 min | ✅ Full | ✅ Easy | Minimal |
| pip install | 1 min | ❌ None | ❌ Manual | Low |
| Development clone | 5 min | ❌ None | ❌ Git | Medium |
| Docker | 10 min | ✅ Full | ⚠️ Rebuild | High |

---

## What's Next?

After installation with `uv tool install`:

1. **Initialize** → `spek init`
2. **Learn** → Read `wiki/quickstart.md`
3. **Configure** → Check `.cel/config.toml`
4. **Use** → Start with `spek prepare`
5. **Integrate** → Use MCP tools with agents

---

## Additional Resources

- **Full Installation Guide:** [INSTALLATION.md](INSTALLATION.md)
- **Quick Reference:** [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- **Documentation:** See `wiki/` directory
- **Architecture:** See `wiki/architecture.md`

---

## Summary

Spekificity is now **fully ready for uv tool install**:

✅ Entry points configured (`spek`, `spek-init`)
✅ Post-install setup automated (`spek init`)
✅ Dependencies managed via pyproject.toml
✅ Complete documentation provided
✅ All tests passing (36/36)
✅ Ready for production use

**Installation in one command:**
```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

**Setup in one command:**
```bash
spek init
```

**Done!** Spekificity is ready to use.
