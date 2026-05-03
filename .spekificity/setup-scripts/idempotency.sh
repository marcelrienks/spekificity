#!/bin/bash

# idempotency.sh — Idempotent operation tracking and recovery
# Enables safe re-runs of spek setup/init by detecting state and skipping completed steps

set -euo pipefail

# Source config handler
source "$(dirname "${BASH_SOURCE[0]}")/config-handler.sh"

# Check if already fully initialized
is_already_initialized() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 1
    fi
    
    local initialized=$(read_config ".spek_initialized")
    [[ "$initialized" == "true" ]]
}

# Detect partial failure (incomplete initialization)
detect_partial_failure() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 1  # No config = no partial failure
    fi
    
    local initialized=$(read_config ".spek_initialized")
    local history_count=$(jq '.orchestration_history | length' "$CONFIG_FILE" 2>/dev/null || echo 0)
    
    # Partial failure: not initialized but has history entries
    if [[ "$initialized" != "true" ]] && [[ $history_count -gt 0 ]]; then
        return 0  # Partial failure detected
    fi
    
    return 1  # No partial failure
}

# Validate prerequisites are present
validate_prerequisites() {
    local errors=()
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        errors+=("Python 3.11+ not found. Run: brew install python@3.11")
    else
        local py_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ "$py_version" < "3.11" ]]; then
            errors+=("Python version $py_version < 3.11 required. Upgrade with: brew install python@3.11")
        fi
    fi
    
    # Check uv
    if ! command -v uv &> /dev/null; then
        errors+=("uv package manager not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh")
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        errors+=("git not found. Install with your OS package manager.")
    fi
    
    if [[ ${#errors[@]} -gt 0 ]]; then
        echo "Prerequisite validation failed:" >&2
        printf '  • %s\n' "${errors[@]}" >&2
        return 1
    fi
    
    return 0
}

# Get recovery guidance for specific failure
get_recovery_guidance() {
    local step="$1"
    
    case "$step" in
        "prerequisites_check")
            echo "Run: spek setup --verbose"
            ;;
        "specify_init")
            echo "Run: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
            echo "Then: spek init"
            ;;
        "graphify_init")
            echo "Run: uv tool install graphifyy"
            echo "Then: spek init"
            ;;
        "obsidian_setup")
            echo "Obsidian is optional. Skipping if not installed is safe."
            echo "To install: Download from https://obsidian.md/"
            echo "Then: spek init"
            ;;
        "skill_install")
            echo "Run: spek init --verbose"
            ;;
        *)
            echo "Unknown failure step: $step"
            ;;
    esac
}

# Mark step as complete (for progress tracking)
mark_step_complete() {
    local step="$1"
    record_orchestration_step "init" "$step" "success"
}

# Mark step as failed
mark_step_failed() {
    local step="$1"
    local error_msg="${2:-unknown error}"
    record_orchestration_step "init" "$step" "failure" "$error_msg"
}

# Print idempotency status
print_idempotency_status() {
    if is_already_initialized; then
        echo "✓ Project already initialized (idempotent mode: updating state)"
        return 0
    fi
    
    if detect_partial_failure; then
        echo "⚠ Partial initialization detected. Attempting recovery..."
        local last_step=$(jq -r '.orchestration_history[-1].step' "$CONFIG_FILE" 2>/dev/null || echo "unknown")
        echo "Last failed step: $last_step"
        echo "Recovery guidance:"
        get_recovery_guidance "$last_step"
        return 1
    fi
    
    echo "✓ Fresh initialization (no previous state)"
    return 0
}

# Export functions if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f is_already_initialized
    export -f detect_partial_failure
    export -f validate_prerequisites
    export -f get_recovery_guidance
    export -f mark_step_complete
    export -f mark_step_failed
    export -f print_idempotency_status
fi
