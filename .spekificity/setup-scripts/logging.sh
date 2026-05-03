#!/bin/bash

# logging.sh — Structured logging and status output for spekificity orchestration
# Provides consistent, colorized output for all spek setup/init/update/status operations

set -euo pipefail

# Color codes (safe for non-TTY output)
if [[ -t 1 ]]; then
    # Terminal detected
    COLOR_RESET='\033[0m'
    COLOR_BOLD='\033[1m'
    COLOR_DIM='\033[2m'
    COLOR_GREEN='\033[32m'
    COLOR_YELLOW='\033[33m'
    COLOR_RED='\033[31m'
    COLOR_BLUE='\033[34m'
    COLOR_CYAN='\033[36m'
else
    # Non-TTY (piped output) - no colors
    COLOR_RESET=''
    COLOR_BOLD=''
    COLOR_DIM=''
    COLOR_GREEN=''
    COLOR_YELLOW=''
    COLOR_RED=''
    COLOR_BLUE=''
    COLOR_CYAN=''
fi

# Global verbose flag (set by caller with --verbose)
VERBOSE_MODE=${VERBOSE_MODE:-false}

# Log a step (spekificity component or third-party tool step)
log_step() {
    local component="$1"  # e.g., "spekificity", "speckit", "graphify", "obsidian"
    local step="$2"       # e.g., "Checking Python version"
    
    echo -e "${COLOR_CYAN}[${component}]${COLOR_RESET} ${step}..."
}

# Log success message
log_success() {
    local message="$1"
    echo -e "${COLOR_GREEN}✓${COLOR_RESET} ${COLOR_BOLD}${message}${COLOR_RESET}"
}

# Log error message
log_error() {
    local message="$1"
    echo -e "${COLOR_RED}✗${COLOR_RESET} ${COLOR_BOLD}Error: ${message}${COLOR_RESET}" >&2
}

# Log warning message
log_warning() {
    local message="$1"
    echo -e "${COLOR_YELLOW}⚠${COLOR_RESET} ${COLOR_BOLD}Warning: ${message}${COLOR_RESET}"
}

# Log info message
log_info() {
    local message="$1"
    echo -e "${COLOR_BLUE}ℹ${COLOR_RESET} ${message}"
}

# Log verbose output (only shown with --verbose)
log_verbose() {
    local message="$1"
    if [[ "$VERBOSE_MODE" == "true" ]]; then
        echo -e "${COLOR_DIM}  → ${message}${COLOR_RESET}"
    fi
}

# Print status section header
print_header() {
    local title="$1"
    echo ""
    echo -e "${COLOR_BOLD}${COLOR_CYAN}═══════════════════════════════════${COLOR_RESET}"
    echo -e "${COLOR_BOLD}${COLOR_CYAN} ${title}${COLOR_RESET}"
    echo -e "${COLOR_BOLD}${COLOR_CYAN}═══════════════════════════════════${COLOR_RESET}"
}

# Print summary table row
print_summary_row() {
    local tool="$1"
    local status="$2"
    local version="${3:-}"
    
    local status_symbol
    case "$status" in
        "installed")
            status_symbol="${COLOR_GREEN}✓${COLOR_RESET}"
            ;;
        "missing")
            status_symbol="${COLOR_RED}✗${COLOR_RESET}"
            ;;
        "optional")
            status_symbol="${COLOR_YELLOW}◯${COLOR_RESET}"
            ;;
        *)
            status_symbol="?"
            ;;
    esac
    
    if [[ -z "$version" ]]; then
        printf "  %s %-20s %s\n" "$status_symbol" "$tool" "$status"
    else
        printf "  %s %-20s %-15s %s\n" "$status_symbol" "$tool" "$version" "$status"
    fi
}

# Print execution summary
print_summary() {
    local title="$1"
    shift
    local items=("$@")
    
    echo ""
    echo -e "${COLOR_BOLD}${title}${COLOR_RESET}"
    for item in "${items[@]}"; do
        echo "  • $item"
    done
}

# Export functions if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f log_step
    export -f log_success
    export -f log_error
    export -f log_warning
    export -f log_info
    export -f log_verbose
    export -f print_header
    export -f print_summary_row
    export -f print_summary
    export VERBOSE_MODE
    export COLOR_RESET COLOR_BOLD COLOR_DIM COLOR_GREEN COLOR_YELLOW COLOR_RED COLOR_BLUE COLOR_CYAN
fi
