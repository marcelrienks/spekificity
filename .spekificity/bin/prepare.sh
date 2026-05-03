#!/usr/bin/env bash
# .spekificity/bin/prepare.sh — spek prepare command
#
# Loads vault context, checks graph currency, and refreshes graph if stale.
# Leaves the AI session primed with full codebase context before feature work.
#
# Usage: spek prepare [--force-refresh]

set -euo pipefail

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_LIB_DIR}/_lib.sh"

# ── flags ──────────────────────────────────────────────────────────────────────
FORCE_REFRESH=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force-refresh) FORCE_REFRESH=true ;;
        -h|--help)
            cat << 'EOF'
Usage: spek prepare [OPTIONS]

Load vault context, verify graph currency, and prime the AI session.

OPTIONS
  --force-refresh   Skip freshness check — always rebuild the graph
  -h, --help        Show this help

DESCRIPTION
  1. Checks graph currency (vault/graph/index.md vs git HEAD timestamp)
  2. If stale or absent (or --force-refresh), triggers graphify rebuild
  3. Invokes /spek.prepare skill to load context into the AI session

Run this before starting any manual or automated feature work.
EOF
            exit 0
            ;;
        *)
            print_err "unknown option: $1 (run 'spek prepare --help')"
            exit 1
            ;;
    esac
    shift
done

# ── checks ─────────────────────────────────────────────────────────────────────
check_initialized || exit 1

VAULT_PATH="$(get_vault_path)"
GRAPH_INDEX="${VAULT_PATH}/graph/index.md"

# ── graph state ────────────────────────────────────────────────────────────────
print_spek "checking graph currency..."

GRAPH_STATE="$(compute_graph_state)"

if [[ "${FORCE_REFRESH}" == "true" ]]; then
    GRAPH_STATE="stale"   # treat as stale to force rebuild
fi

case "${GRAPH_STATE}" in
    fresh)
        print_ok "graph is current (${GRAPH_INDEX})"
        ;;
    stale)
        print_warn "graph is stale — triggering graphify rebuild"
        if command -v graphify &>/dev/null; then
            print_graphify "running incremental rebuild..."
            graphify . --obsidian --output "${VAULT_PATH}/graph/" 2>&1 | \
                sed "s/^/$(printf '\033[2m')[graphify]$(printf '\033[0m') /"
            print_ok "graph rebuilt"
        else
            print_warn "graphify not installed — skipping graph rebuild (context may be outdated)"
            print_warn "install graphify: see setup-guides/graphify-setup.md"
        fi
        ;;
    absent)
        print_warn "graph not found — running full graphify build (first run may take longer)"
        if command -v graphify &>/dev/null; then
            print_graphify "running full build..."
            graphify . --obsidian --output "${VAULT_PATH}/graph/" --full 2>&1 | \
                sed "s/^/$(printf '\033[2m')[graphify]$(printf '\033[0m') /"
            print_ok "graph built at ${GRAPH_INDEX}"
        else
            print_warn "graphify not installed — vault graph unavailable"
            print_warn "install graphify: see setup-guides/graphify-setup.md"
        fi
        ;;
esac

# ── invoke /spek.prepare skill ─────────────────────────────────────────────────
echo ""
print_spek "preparation complete — invoke '/spek.prepare' in your AI session to load vault context."
print_spek "skill location: .spekificity/skills/spek.prepare.md"
echo ""

# Verify skill file exists
SKILL_FILE="${SPEKIFICITY_DIR}/skills/spek.prepare.md"
if [[ ! -f "${SKILL_FILE}" ]]; then
    print_warn "skill file not found at ${SKILL_FILE} — run 'spek init' to install skills"
fi

exit 0
