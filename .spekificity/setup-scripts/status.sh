#!/bin/bash

# status.sh — spek status command
# Reports initialization status, installed version, and tool integration
# Primary entry point for `spek status`

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source helper modules
source "$SCRIPT_DIR/logging.sh"
source "$SCRIPT_DIR/config-handler.sh"
source "$SCRIPT_DIR/skill-discovery.sh"

# Parse command-line arguments
OUTPUT_FORMAT="human"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            OUTPUT_FORMAT="json"
            ;;
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
Usage: spek status [OPTIONS]

Check spekificity platform initialization and tool integration status.

OPTIONS:
  --json         Output in JSON format (machine-readable)
  --verbose      Show detailed status information
  -h, --help     Show this help message

EXAMPLES:
  spek status              # Show human-readable status
  spek status --json       # Show JSON status
  spek status --verbose    # Show detailed information
EOF
}

# Human-readable status output
print_human_status() {
    print_header "Spekificity Platform Status"
    echo ""
    
    # Check if initialized
    if ! [[ -f ".spekificity/config.json" ]]; then
        log_warning "Platform not initialized. Run: spek init"
        return 1
    fi
    
    # Read status from config
    local version=$(read_config ".spek_version")
    local initialized=$(read_config ".spek_initialized")
    local timestamp=$(read_config ".spek_initialized_timestamp")
    local branch=$(read_config ".spek_platform_branch")
    
    echo -e "${COLOR_BOLD}Version:${COLOR_RESET} $version"
    echo -e "${COLOR_BOLD}Branch:${COLOR_RESET} $branch"
    echo -e "${COLOR_BOLD}Initialized:${COLOR_RESET} $initialized"
    if [[ "$initialized" == "true" ]]; then
        echo -e "${COLOR_BOLD}Initialized at:${COLOR_RESET} $timestamp"
    fi
    echo ""
    
    # Tool integration status
    print_header "Tool Integration"
    
    local speckit_installed=$(read_config ".tools.speckit.installed")
    local speckit_version=$(read_config ".tools.speckit.version")
    local speckit_init=$(read_config ".tools.speckit.initialized")
    
    local graphify_installed=$(read_config ".tools.graphify.installed")
    local graphify_version=$(read_config ".tools.graphify.version")
    local graphify_init=$(read_config ".tools.graphify.initialized")
    
    local obsidian_installed=$(read_config ".tools.obsidian.installed")
    local obsidian_init=$(read_config ".tools.obsidian.initialized")
    
    local caveman_available=$(read_config ".tools.caveman.available")
    local caveman_integrated=$(read_config ".tools.caveman.integrated")
    
    echo -e "${COLOR_BOLD}speckit/specify:${COLOR_RESET}"
    echo "  Installed: $speckit_installed ($speckit_version)"
    echo "  Initialized: $speckit_init"
    
    echo -e "${COLOR_BOLD}graphify:${COLOR_RESET}"
    echo "  Installed: $graphify_installed ($graphify_version)"
    echo "  Initialized: $graphify_init"
    
    echo -e "${COLOR_BOLD}Obsidian (optional):${COLOR_RESET}"
    echo "  Installed: $obsidian_installed"
    echo "  Initialized: $obsidian_init"
    
    echo -e "${COLOR_BOLD}caveman (optional):${COLOR_RESET}"
    echo "  Available: $caveman_available"
    echo "  Integrated: $caveman_integrated"
    echo ""
    
    # Skills status
    print_header "Installed Skills"
    
    local spekificity_installed=$(read_config ".skills.spekificity_installed")
    local speckit_installed=$(read_config ".skills.speckit_installed")
    local caveman_installed=$(read_config ".skills.caveman_installed")
    
    echo -e "${COLOR_BOLD}Spekificity custom skills:${COLOR_RESET} $spekificity_installed"
    echo -e "${COLOR_BOLD}Speckit skills:${COLOR_RESET} $speckit_installed"
    echo -e "${COLOR_BOLD}Caveman skills:${COLOR_RESET} $caveman_installed"
    echo ""
    
    # Skill discovery
    if [[ -f ".spekificity/skill-index.md" ]]; then
        echo -e "${COLOR_BOLD}Available skills:${COLOR_RESET}"
        echo "  See: .spekificity/skill-index.md"
        local skill_count=$(grep -c "^|.*|.*|" ".spekificity/skill-index.md" || echo 0)
        echo "  Total skills registered: $((skill_count - 1)) (approx)"
    fi
    echo ""
    
    # Recent operations
    print_header "Recent Operations"
    local history_count=$(jq '.orchestration_history | length' ".spekificity/config.json" 2>/dev/null || echo 0)
    if [[ $history_count -gt 0 ]]; then
        echo "Last 5 operations:"
        jq -r '.orchestration_history[-5:] | .[] | "  [\(.status)] \(.operation) > \(.step) (\(.timestamp))"' ".spekificity/config.json" 2>/dev/null || true
    else
        echo "No operations recorded"
    fi
    echo ""
    
    return 0
}

# JSON status output
print_json_status() {
    if [[ ! -f ".spekificity/config.json" ]]; then
        echo '{"error": "Platform not initialized", "initialized": false}'
        return 1
    fi
    
    # Output the entire config as JSON
    cat ".spekificity/config.json"
    return 0
}

main() {
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        print_json_status
    else
        print_human_status
    fi
}

# Run main function
if main; then
    exit 0
else
    exit 1
fi
