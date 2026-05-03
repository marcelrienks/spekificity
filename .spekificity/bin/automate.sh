#!/usr/bin/env bash
# .spekificity/bin/automate.sh — spek automate command
#
# Drives the full speckit feature lifecycle autonomously:
#   preflight → spec → plan → tasks → analyse → remediation → implement → postflight
#
# Usage:
#   spek automate "<feature description>"
#   spek automate --resume
#   spek automate --no-pr "<feature description>"

set -euo pipefail

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_LIB_DIR}/_lib.sh"

# ── flags ──────────────────────────────────────────────────────────────────────
RESUME_MODE=false
NO_PR=false
FEATURE_DESCRIPTION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --resume)
            RESUME_MODE=true
            ;;
        --no-pr)
            NO_PR=true
            ;;
        -h|--help)
            cat << 'EOF'
Usage: spek automate "<feature description>" [OPTIONS]
       spek automate --resume [OPTIONS]

Drive the full speckit feature lifecycle autonomously.

OPTIONS
  --resume    Resume an interrupted automate session from last completed step
  --no-pr     Skip pull request creation at postflight
  -h, --help  Show this help

STEPS (in order)
  preflight → spec → plan → tasks → analyse → remediation → implement → postflight

The AI skill (/spek.automate) drives each step. Questions are surfaced
interactively via the [spek] ❓ prompt. State is saved after every step
so --resume can recover from any interruption.

EXAMPLES
  spek automate "add user authentication with JWT"
  spek automate --resume
  spek automate --no-pr "spike: explore graphify incremental mode"
EOF
            exit 0
            ;;
        -*)
            print_err "unknown option: $1"
            exit 1
            ;;
        *)
            FEATURE_DESCRIPTION="${FEATURE_DESCRIPTION:+${FEATURE_DESCRIPTION} }$1"
            ;;
    esac
    shift
done

# ── checks ─────────────────────────────────────────────────────────────────────
check_initialized || exit 1

# ── resume mode ────────────────────────────────────────────────────────────────
if [[ "${RESUME_MODE}" == "true" ]]; then
    if [[ ! -f "${WORKFLOW_STATE_FILE}" ]]; then
        print_err "no workflow-state.json found — nothing to resume"
        print_spek "start a new workflow with: spek automate \"<feature description>\""
        exit 1
    fi

    STATUS="$(read_workflow_state '.status')"
    NEXT_STEP="$(read_workflow_state '.next_step')"
    FEATURE_BRANCH="$(read_workflow_state '.feature_branch')"

    if [[ "${STATUS}" == "complete" ]]; then
        print_err "workflow is already complete (status: complete)"
        print_spek "nothing to resume. start a new feature with: spek automate \"<description>\""
        exit 1
    fi

    if [[ "${STATUS}" != "in-progress" && "${STATUS}" != "halted" ]]; then
        print_err "unexpected workflow status: ${STATUS}"
        print_spek "workflow-state.json may be corrupted. inspect: ${WORKFLOW_STATE_FILE}"
        exit 1
    fi

    print_spek "resuming workflow: ${FEATURE_BRANCH}"
    print_spek "next step: ${NEXT_STEP}"
    echo ""
    print_spek "invoke '/spek.automate' in your AI session — it will read workflow-state.json and continue from step: ${NEXT_STEP}"
    print_spek "skill location: ${SPEKIFICITY_DIR}/skills/spek.automate.md"
    exit 0
fi

# ── fresh start ────────────────────────────────────────────────────────────────
if [[ -z "${FEATURE_DESCRIPTION}" ]]; then
    print_err "feature description required"
    echo "  Usage: spek automate \"<feature description>\"" >&2
    exit 1
fi

# ── idempotency guard: check for existing complete workflow ────────────────────
if [[ -f "${WORKFLOW_STATE_FILE}" ]]; then
    EXISTING_STATUS="$(read_workflow_state '.status')"
    EXISTING_BRANCH="$(read_workflow_state '.feature_branch')"
    if [[ "${EXISTING_STATUS}" == "complete" ]]; then
        print_spek "previous workflow already complete: ${EXISTING_BRANCH}"
        print_spek "nothing to do (SC-007 idempotency guard)"
        print_spek "start a fresh feature by committing and removing workflow-state.json, or use --resume for an interrupted run"
        exit 0
    fi
fi

# ── preflight: check working tree ─────────────────────────────────────────────
print_spek "preflight checks..."

UNCOMMITTED="$(git -C "${PROJECT_ROOT}" status --porcelain 2>/dev/null || echo "")"
if [[ -n "${UNCOMMITTED}" ]]; then
    print_err "uncommitted changes detected — cannot create a clean feature branch"
    echo "" >&2
    echo "  Uncommitted files:" >&2
    echo "${UNCOMMITTED}" | sed 's/^/    /' >&2
    echo "" >&2
    echo "  Stash or commit changes first, then retry." >&2
    exit 2
fi

print_ok "working tree is clean"

# ── generate NNN-kebab-case branch name ───────────────────────────────────────
# Scan specs/ for highest existing NNN- prefix, increment by 1
SPECS_DIR="${PROJECT_ROOT}/specs"
NEXT_N=1
if [[ -d "${SPECS_DIR}" ]]; then
    MAX_N=0
    while IFS= read -r dir; do
        base="$(basename "${dir}")"
        if [[ "${base}" =~ ^([0-9]+)- ]]; then
            n="${BASH_REMATCH[1]#0*}"  # strip leading zeros
            n="${n:-0}"
            (( n > MAX_N )) && MAX_N="${n}"
        fi
    done < <(find "${SPECS_DIR}" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)
    NEXT_N=$(( MAX_N + 1 ))
fi

NNN="$(printf "%03d" "${NEXT_N}")"

# Convert description to kebab-case: lowercase, replace spaces/special chars with -
SLUG="$(echo "${FEATURE_DESCRIPTION}" | tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9 ]//g' | tr -s ' ' '-' | sed 's/^-//;s/-$//')"
BRANCH_NAME="${NNN}-${SLUG}"
FEATURE_DIR="specs/${BRANCH_NAME}"

print_ok "feature branch name: ${BRANCH_NAME}"

# ── detect branch conflict ─────────────────────────────────────────────────────
EXISTING_BRANCHES="$(git -C "${PROJECT_ROOT}" branch --list "${BRANCH_NAME}" 2>/dev/null)"
if [[ -n "${EXISTING_BRANCHES}" ]]; then
    echo ""
    print_warn "branch '${BRANCH_NAME}' already exists"
    echo ""
    echo -n "  [spek] reuse existing branch or create with suffix? [reuse/suffix]: "
    read -r BRANCH_CHOICE
    if [[ "${BRANCH_CHOICE}" =~ ^[Ss] ]]; then
        # Find next available suffix: -2, -3, ...
        SUFFIX=2
        while git -C "${PROJECT_ROOT}" branch --list "${BRANCH_NAME}-${SUFFIX}" &>/dev/null \
                && [[ -n "$(git -C "${PROJECT_ROOT}" branch --list "${BRANCH_NAME}-${SUFFIX}")" ]]; do
            (( SUFFIX++ ))
        done
        BRANCH_NAME="${BRANCH_NAME}-${SUFFIX}"
        print_spek "using suffixed branch: ${BRANCH_NAME}"
    else
        print_spek "reusing existing branch: ${BRANCH_NAME}"
        git -C "${PROJECT_ROOT}" checkout "${BRANCH_NAME}"
    fi
fi

# ── create feature branch ─────────────────────────────────────────────────────
if [[ -z "${EXISTING_BRANCHES}" ]] || [[ "${BRANCH_CHOICE:-}" =~ ^[Ss] ]]; then
    print_spek "creating branch ${BRANCH_NAME}..."
    git -C "${PROJECT_ROOT}" checkout -b "${BRANCH_NAME}"
    print_ok "branch created and checked out"
fi

# ── write initial workflow-state.json ─────────────────────────────────────────
NOW="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

INITIAL_STATE="$(cat << EOF
{
  "schema_version": "1.0",
  "feature_description": $(echo "${FEATURE_DESCRIPTION}" | jq -R .),
  "feature_branch": "${BRANCH_NAME}",
  "feature_dir": "${FEATURE_DIR}",
  "started_at": "${NOW}",
  "last_updated": "${NOW}",
  "status": "in-progress",
  "current_step": "preflight",
  "next_step": "spec",
  "completed_steps": ["preflight"],
  "pending_questions": [],
  "no_pr": ${NO_PR},
  "preflight": {
    "branch_created": true,
    "clean_working_tree": true
  },
  "postflight": {
    "lessons_written": false,
    "graph_refreshed": false,
    "pr_created": false,
    "pr_url": null
  }
}
EOF
)"

atomic_write_json "${WORKFLOW_STATE_FILE}" "${INITIAL_STATE}"
print_ok "workflow state initialised at ${WORKFLOW_STATE_FILE}"

# ── hand off to AI skill ───────────────────────────────────────────────────────
echo ""
print_spek "preflight complete ✓"
print_spek "  feature: ${FEATURE_DESCRIPTION}"
print_spek "  branch:  ${BRANCH_NAME}"
print_spek "  dir:     ${FEATURE_DIR}"
echo ""
print_spek "invoke '/spek.automate' in your AI session to start the lifecycle."
print_spek "skill location: ${SPEKIFICITY_DIR}/skills/spek.automate.md"
echo ""

exit 0
