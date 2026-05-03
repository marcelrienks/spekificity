#!/bin/bash

# setup.sh — Main spek setup command
# Orchestrates prerequisite detection and installation guidance
# Primary entry point for `spek setup`

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source helper modules
source "$SCRIPT_DIR/logging.sh"
source "$SCRIPT_DIR/prerequisites.sh"
source "$SCRIPT_DIR/platform.sh"
source "$SCRIPT_DIR/config-handler.sh"

# Parse command-line arguments
VERBOSE_MODE=false
DRY_RUN=false
SKIP_OPTIONAL=false
CONFIRM_MANUAL_TOOL=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose)
            VERBOSE_MODE=true
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --skip-optional)
            SKIP_OPTIONAL=true
            ;;
        --confirm-manual)
            shift
            CONFIRM_MANUAL_TOOL="${1:-}"
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
    shift
done

print_help() {
    cat << EOF
Usage: spek setup [OPTIONS]

Detect and prepare prerequisites for spekificity platform initialization.
This is the first step before running 'spek init'.

OPTIONS:
  --dry-run               Detect tools and report status without installing anything
  --skip-optional         Skip optional tools (graphify, obsidian, caveman, gh)
  --confirm-manual <tool> Mark a manual-only tool as confirmed installed (e.g. obsidian)
  --verbose               Show detailed output
  -h, --help              Show this help message

DESCRIPTION:
  spek setup checks for required tools (Python 3.11+, uv, git, speckit) and
  optional tools (graphify, Obsidian, caveman, gh). It auto-installs those that
  can be installed programmatically, and provides step-by-step instructions for
  manual-only tools (e.g. Obsidian GUI).

  Use --confirm-manual obsidian after manually installing Obsidian to record
  its installation in config.json and remove the pending warning.

  After setup completes successfully, run: spek init

EXAMPLES:
  spek setup                            # Run prerequisite check + install
  spek setup --dry-run                  # Detect only, no installs
  spek setup --skip-optional            # Required tools only
  spek setup --confirm-manual obsidian  # Record Obsidian as manually installed
  spek setup --verbose                  # Show detailed output
EOF
}

main() {
    # ── handle --confirm-manual ─────────────────────────────────────────────────
    if [[ -n "${CONFIRM_MANUAL_TOOL}" ]]; then
        CONFIG_FILE="${PROJECT_ROOT}/.spekificity/config.json"
        if [[ ! -f "${CONFIG_FILE}" ]]; then
            log_error "config.json not found — run 'spek init' first"
            return 1
        fi
        if command -v jq &>/dev/null; then
            local tmp
            tmp="$(mktemp "${PROJECT_ROOT}/.spekificity/config.tmp.XXXXXX")"
            jq ".tools.${CONFIRM_MANUAL_TOOL}.manual_confirmed = true | .tools.${CONFIRM_MANUAL_TOOL}.installed = true" \
                "${CONFIG_FILE}" > "${tmp}" && mv "${tmp}" "${CONFIG_FILE}"
            log_success "${CONFIRM_MANUAL_TOOL} marked as manually confirmed in config.json"
        else
            log_error "jq required for --confirm-manual — install jq and retry"
            return 1
        fi
        return 0
    fi

    print_header "Spekificity Platform Setup"
    log_info "Spekificity v$(cat "${PROJECT_ROOT}/.spekificity/version.txt" 2>/dev/null || echo '?')"
    [[ "${DRY_RUN}" == "true" ]] && log_info "[dry-run mode — no installs will be performed]"
    [[ "${SKIP_OPTIONAL}" == "true" ]] && log_info "[--skip-optional — optional tools will be skipped]"
    echo ""
    
    # Step 1: Detect platform
    log_step "spekificity" "Detecting platform"
    detect_platform || {
        log_error "Platform detection failed"
        return 1
    }
    print_platform_info
    echo ""
    
    # Step 2: Check all prerequisites
    if ! check_all_prerequisites; then
        if [[ "${DRY_RUN}" == "true" ]]; then
            log_warn "Dry-run complete — some prerequisites are missing (no installs performed)"
            return 0
        fi
        log_error "Setup failed: required prerequisites not available"
        echo ""
        echo "Next steps:"
        echo "  1. Install missing prerequisites (see instructions above)"
        echo "  2. Run: spek setup"
        return 1
    fi
    echo ""

    if [[ "${DRY_RUN}" == "true" ]]; then
        log_success "Dry-run complete — all checked prerequisites present"
        return 0
    fi
    
    # Step 3: Initialize config if needed
    log_step "spekificity" "Initializing configuration"
    initialize_config || log_verbose "Config already exists"
    log_success "Configuration ready"
    echo ""
    
    # Step 4: Summary
    print_header "Setup Summary"
    print_summary "✓ Prerequisites verified:" \
        "Python 3.11+ ✓" \
        "uv package manager ✓" \
        "git ✓" \
        "Platform: $PLATFORM ✓"
    echo ""
    echo "Optional tools will be installed by 'spek init' if missing."
    echo ""
    echo -e "${COLOR_BOLD}Next step:${COLOR_RESET}"
    echo "  Run: ${COLOR_CYAN}spek init${COLOR_RESET}"
    echo ""
    
    return 0
}

# Run main function with error handling
if ! main; then
    log_error "Setup did not complete successfully"
    exit 1
fi

log_success "Setup complete"
exit 0
