#!/usr/bin/env bash
# .spekificity/bin/post.sh — spek post command
#
# Post-implementation lifecycle: lessons capture + vault graph refresh
#
# Usage:
#   spek post
#   spek post --no-lessons
#   spek post --no-graph

set -euo pipefail

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_LIB_DIR}/_lib.sh"

# ── flags ──────────────────────────────────────────────────────────────────────
NO_LESSONS=false
NO_GRAPH=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-lessons)
            NO_LESSONS=true
            ;;
        --no-graph)
            NO_GRAPH=true
            ;;
        -h|--help)
            cat << 'EOF'
Usage: spek post [OPTIONS]

Post-implementation lifecycle: lessons capture and vault graph refresh.

Run this after a feature implementation is complete to capture structured
lessons and refresh the obsidian vault graph.

OPTIONS
  --no-lessons  Skip lesson capture (vault/lessons/ write)
  --no-graph    Skip vault graph refresh (graphify incremental run)
  -h, --help    Show this help

EXAMPLES
  spek post
  spek post --no-lessons
  spek post --no-graph
EOF
            exit 0
            ;;
        -*)
            print_err "unknown option: $1"
            exit 1
            ;;
        *)
            print_err "unexpected argument: $1"
            exit 1
            ;;
    esac
    shift
done

# ── checks ─────────────────────────────────────────────────────────────────────
check_initialized || exit 1

# ── detect context ─────────────────────────────────────────────────────────────
FEATURE_BRANCH=""
FEATURE_DIR=""
FEATURE_DESCRIPTION=""

if [[ -f "${WORKFLOW_STATE_FILE}" ]]; then
    FEATURE_BRANCH="$(read_workflow_state '.feature_branch' 2>/dev/null || echo "")"
    FEATURE_DIR="$(read_workflow_state '.feature_dir' 2>/dev/null || echo "")"
    FEATURE_DESCRIPTION="$(read_workflow_state '.feature_description' 2>/dev/null || echo "")"
fi

if [[ -z "${FEATURE_BRANCH}" ]]; then
    FEATURE_BRANCH="$(git -C "${PROJECT_ROOT}" branch --show-current 2>/dev/null || echo "")"
fi

if [[ -z "${FEATURE_BRANCH}" ]]; then
    print_warn "could not detect current feature branch — lessons will not be tagged to a branch"
fi

# ── status summary ─────────────────────────────────────────────────────────────
print_spek "post-implementation workflow"
if [[ -n "${FEATURE_BRANCH}" ]]; then
    print_spek "  feature: ${FEATURE_DESCRIPTION:-${FEATURE_BRANCH}}"
    print_spek "  branch:  ${FEATURE_BRANCH}"
fi
if [[ -n "${FEATURE_DIR}" ]]; then
    print_spek "  dir:     ${FEATURE_DIR}"
fi
echo ""

# ── flag summary ───────────────────────────────────────────────────────────────
if [[ "${NO_LESSONS}" == "true" ]]; then
    print_warn "--no-lessons: lesson capture will be skipped"
fi
if [[ "${NO_GRAPH}" == "true" ]]; then
    print_warn "--no-graph: vault graph refresh will be skipped"
fi

echo ""
print_spek "invoke '/spek.post' in your AI session to run post-implementation steps."
print_spek "skill location: ${SPEKIFICITY_DIR}/skills/spek.post.md"
echo ""

# Pass flag context to skill via workflow-state.json
if [[ -f "${WORKFLOW_STATE_FILE}" ]]; then
    if command -v jq &>/dev/null; then
        UPDATED="$(jq \
            --arg no_lessons "${NO_LESSONS}" \
            --arg no_graph "${NO_GRAPH}" \
            '.post_flags = {no_lessons: ($no_lessons == "true"), no_graph: ($no_graph == "true")}' \
            "${WORKFLOW_STATE_FILE}")"
        atomic_write_json "${WORKFLOW_STATE_FILE}" "${UPDATED}"
    fi
fi

exit 0
