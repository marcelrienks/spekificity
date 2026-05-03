#!/usr/bin/env bash
# .spekificity/bin/_lib.sh — shared utilities for spek bin scripts
#
# Source this file at the top of each .spekificity/bin/*.sh script:
#   source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
#
# Provides: print_spek, print_speckit, print_graphify, read_config, write_config,
#           check_initialized, atomic_write_json, compute_graph_state

set -euo pipefail

# ── paths ──────────────────────────────────────────────────────────────────────
_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${_LIB_DIR}/../.." && pwd)"
SPEKIFICITY_DIR="${PROJECT_ROOT}/.spekificity"
CONFIG_FILE="${SPEKIFICITY_DIR}/config.json"
WORKFLOW_STATE_FILE="${SPEKIFICITY_DIR}/workflow-state.json"

# ── color codes (TTY-safe) ─────────────────────────────────────────────────────
if [[ -t 1 ]]; then
    _C_RESET='\033[0m'; _C_GREEN='\033[32m'; _C_YELLOW='\033[33m'
    _C_RED='\033[31m'; _C_CYAN='\033[36m'; _C_DIM='\033[2m'; _C_BOLD='\033[1m'
else
    _C_RESET=''; _C_GREEN=''; _C_YELLOW=''
    _C_RED=''; _C_CYAN=''; _C_DIM=''; _C_BOLD=''
fi

# ── output helpers ─────────────────────────────────────────────────────────────
print_spek()      { echo -e "${_C_CYAN}[spek]${_C_RESET} $*"; }
print_speckit()   { echo -e "${_C_DIM}[speckit]${_C_RESET} $*"; }
print_graphify()  { echo -e "${_C_DIM}[graphify]${_C_RESET} $*"; }
print_ok()        { echo -e "${_C_GREEN}[spek]${_C_RESET} ✓ $*"; }
print_warn()      { echo -e "${_C_YELLOW}[spek]${_C_RESET} ⚠ $*"; }
print_err()       { echo -e "${_C_RED}[spek]${_C_RESET} ✗ $*" >&2; }

# ── config read ────────────────────────────────────────────────────────────────
# read_config <key_path>
# Reads a JSON value from config.json using jq dot-notation path.
# Example: read_config '.vault.path'  → vault/
# Returns empty string if key not found or config missing.
read_config() {
    local key_path="${1:-.}"
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        echo ""
        return 0
    fi
    command -v jq &>/dev/null || { cat "${CONFIG_FILE}"; return 0; }
    jq -r "${key_path} // empty" "${CONFIG_FILE}" 2>/dev/null || echo ""
}

# ── config write ───────────────────────────────────────────────────────────────
# write_config <key_path> <value>
# Sets a JSON key in config.json. Creates file with minimal schema if absent.
# Example: write_config '.tools.speckit.installed' 'true'
write_config() {
    local key_path="$1"
    local value="$2"
    if ! command -v jq &>/dev/null; then
        print_warn "jq not found — cannot update config.json"
        return 1
    fi
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        echo '{"schema_version":"1.0"}' > "${CONFIG_FILE}"
    fi
    local tmp
    tmp="$(mktemp "${SPEKIFICITY_DIR}/config.tmp.XXXXXX")"
    jq "${key_path} = ${value}" "${CONFIG_FILE}" > "${tmp}"
    mv "${tmp}" "${CONFIG_FILE}"
}

# ── initialisation check ───────────────────────────────────────────────────────
# check_initialized [--quiet]
# Returns 0 if platform is initialised, 1 if not.
# Prints a warning unless --quiet.
check_initialized() {
    local quiet="${1:-}"
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        [[ "${quiet}" == "--quiet" ]] || print_warn "platform not initialised — run 'spek init' first"
        return 1
    fi
    local ts
    ts="$(read_config '.initialized_at')"
    if [[ -z "${ts}" ]]; then
        [[ "${quiet}" == "--quiet" ]] || print_warn "platform not fully initialised — run 'spek init' to complete setup"
        return 1
    fi
    return 0
}

# ── atomic JSON write ──────────────────────────────────────────────────────────
# atomic_write_json <file_path> <json_string>
# Writes JSON atomically (tmp → mv) to prevent partial writes on interruption.
atomic_write_json() {
    local target="$1"
    local json="$2"
    local dir
    dir="$(dirname "${target}")"
    local tmp
    tmp="$(mktemp "${dir}/.tmp.XXXXXX")"
    echo "${json}" > "${tmp}"
    mv "${tmp}" "${target}"
}

# ── graph state ────────────────────────────────────────────────────────────────
# compute_graph_state
# Prints one of: fresh | stale | absent
# fresh  → vault/graph/index.md exists and is newer than (or equal to) git HEAD
# stale  → vault/graph/index.md exists but git HEAD has newer commits
# absent → vault/graph/index.md does not exist
compute_graph_state() {
    local vault_path
    vault_path="$(read_config '.vault.path')"
    vault_path="${vault_path:-vault/}"
    # strip trailing slash for stat
    vault_path="${vault_path%/}"
    local graph_index="${PROJECT_ROOT}/${vault_path}/graph/index.md"

    if [[ ! -f "${graph_index}" ]]; then
        echo "absent"
        return 0
    fi

    # get git HEAD commit timestamp (epoch seconds)
    local head_ts
    head_ts="$(git -C "${PROJECT_ROOT}" log -1 --format=%ct HEAD 2>/dev/null || echo 0)"

    # get graph index mtime (cross-platform: Darwin vs Linux)
    local graph_ts
    if stat --version &>/dev/null 2>&1; then
        # GNU stat (Linux)
        graph_ts="$(stat -c %Y "${graph_index}" 2>/dev/null || echo 0)"
    else
        # BSD stat (macOS)
        graph_ts="$(stat -f %m "${graph_index}" 2>/dev/null || echo 0)"
    fi

    if [[ "${graph_ts}" -ge "${head_ts}" ]]; then
        echo "fresh"
    else
        echo "stale"
    fi
}

# ── vault path helper ──────────────────────────────────────────────────────────
# get_vault_path
# Returns absolute path to the vault directory (from config or default).
get_vault_path() {
    local rel_path
    rel_path="$(read_config '.vault.path')"
    rel_path="${rel_path:-vault/}"
    # return as absolute
    echo "${PROJECT_ROOT}/${rel_path%/}"
}

# ── workflow state helpers ─────────────────────────────────────────────────────
# read_workflow_state <jq_path>
# Reads a value from workflow-state.json.
read_workflow_state() {
    local key_path="${1:-.}"
    if [[ ! -f "${WORKFLOW_STATE_FILE}" ]]; then
        echo ""
        return 0
    fi
    command -v jq &>/dev/null || { echo ""; return 0; }
    jq -r "${key_path} // empty" "${WORKFLOW_STATE_FILE}" 2>/dev/null || echo ""
}
