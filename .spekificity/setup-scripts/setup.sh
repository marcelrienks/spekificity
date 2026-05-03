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
while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose)
            VERBOSE_MODE=true
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
  --verbose      Show detailed output
  -h, --help     Show this help message

DESCRIPTION:
  spek setup checks for required tools (Python 3.11+, uv, git) and optional
  tools (speckit, graphify, Obsidian, caveman). It provides installation
  instructions for any missing prerequisites.

  After setup completes successfully, run: spek init

EXAMPLES:
  spek setup              # Run prerequisite check
  spek setup --verbose    # Show detailed output
EOF
}

main() {
    print_header "Spekificity Platform Setup"
    log_info "Spekificity v1.0.0 — Unified orchestration platform"
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
        log_error "Setup failed: required prerequisites not available"
        echo ""
        echo "Next steps:"
        echo "  1. Install missing prerequisites (see instructions above)"
        echo "  2. Run: spek setup"
        return 1
    fi
    echo ""
    
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
