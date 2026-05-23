#!/usr/bin/env bash
# Spekificity Installation Script
# This script automates the setup of Spekificity after uv tool install
# 
# Usage:
#   bash setup.sh
#   Or after: uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
#     spek-init
#   Or:
#     spek init

set -e

echo "🚀 Spekificity Setup Script"
echo "================================"
echo ""


# 1. Check Python 3.11+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+ and re-run this script."
    exit 1
fi
PYVER=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
if [[ "$PYVER" < "3.11" ]]; then
    echo "❌ Python version $PYVER found. Please install Python 3.11+ and re-run."
    exit 1
fi
echo "✓ Python $PYVER found"

# 2. Check uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    pipx install uv
fi
echo "✓ uv found"

# 3. Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git and re-run this script."
    exit 1
fi
echo "✓ Git found"

# 4. Check Obsidian
if ! command -v obsidian &> /dev/null; then
    echo "Obsidian not found. Attempting to install..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install --cask obsidian || true
    elif [[ "$OSTYPE" == "linux"* ]]; then
        echo "Please install Obsidian manually from https://obsidian.md/download"
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
        choco install obsidian || true
    else
        echo "Please install Obsidian manually from https://obsidian.md/download"
    fi
fi
if command -v obsidian &> /dev/null; then
    echo "✓ Obsidian found"
else
    echo "❌ Obsidian not found. Please install manually and re-run."
    exit 1
fi

# 5. Verify Obsidian CLI availability (bundled with Obsidian app)
# The Obsidian CLI is provided by the Obsidian desktop app and registers
# as the `obsidian` command in PATH when enabled via Settings → General → Command line interface.
if ! command -v obsidian &> /dev/null; then
    echo "❌ Obsidian CLI (obsidian) not found in PATH."
    echo "Ensure the Obsidian desktop app is installed and the CLI is enabled:"
    echo "  1. Open Obsidian → Settings → General → Command line interface"
    echo "  2. Follow the on-screen prompt to register the CLI in your PATH"
    echo "  3. Restart your terminal and retry this script"
    echo "If you need CI/headless alternatives, see: https://obsidian.md/help/headless"
    exit 1
else
    echo "✓ Obsidian CLI (obsidian) available"
fi

# 6. Check Spekificity CLI
if ! command -v spek &> /dev/null; then
    echo "Installing Spekificity..."
    uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
fi
echo "✓ Found 'spek' command"

# 7. Run spek init
echo "Initializing Spekificity..."
spek init

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review your project structure"
echo "  2. Run: spek prepare"
echo "  3. Run: spek context"
echo "  4. Run: spek plan"
echo ""
