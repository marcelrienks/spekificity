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

# Check if spek is available
if ! command -v spek &> /dev/null; then
    echo "❌ Error: 'spek' command not found."
    echo ""
    echo "Please install Spekificity first:"
    echo "  uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git"
    exit 1
fi

echo "✓ Found 'spek' command"
echo ""

# Run spek init
echo "Initializing Spekificity..."
spek init

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review your project structure"
echo "  2. Run: spek prepare"
echo "  3. Run: spek context"
echo "  4. Run: spek plan [feature-name]"
echo ""
