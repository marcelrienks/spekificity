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
    echo "❗ Obsidian CLI (obsidian) not found in PATH. The Obsidian CLI is required for core automation."
    echo "If you have the Obsidian desktop app, enable the CLI in Settings → General → Command line interface and register it in your PATH."
    echo "For CI/headless options or more installation guidance see: https://obsidian.md/help/headless"
    echo "Please install or register the Obsidian CLI and re-run this script."
    exit 1
else
    echo "✓ Obsidian CLI (obsidian) available"
fi

# (Obsidian CLI verification handled above)

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
