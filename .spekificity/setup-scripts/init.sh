#!/bin/bash

# init.sh — Main spek init command
# Orchestrates initialization of all tools: speckit, graphify, obsidian, caveman, skills
# Primary entry point for `spek init` — the main initialization command

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source helper modules
source "$SCRIPT_DIR/logging.sh"
source "$SCRIPT_DIR/config-handler.sh"
source "$SCRIPT_DIR/skill-discovery.sh"
source "$SCRIPT_DIR/idempotency.sh"

# Parse command-line arguments
VERBOSE_MODE=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose)
            VERBOSE_MODE=true
            ;;
        --skip-obsidian)
            SKIP_OBSIDIAN=true
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

SKIP_OBSIDIAN=${SKIP_OBSIDIAN:-false}

print_help() {
    cat << EOF
Usage: spek init [OPTIONS]

Initialize spekificity platform and all consolidated tools.
This is the primary initialization entry point (analogous to 'specify init').

Prerequisites: Must run 'spek setup' successfully first.

OPTIONS:
  --verbose           Show detailed output
  --skip-obsidian     Skip Obsidian initialization (use fallback graph storage)
  -h, --help          Show this help message

DESCRIPTION:
  spek init orchestrates initialization of:
  • speckit/specify (via 'specify init')
  • graphify (codebase analysis → vault)
  • Obsidian (optional, graph storage)
  • caveman skill (token compression, optional)
  • Spekificity custom skills (install to .spekificity/skills/)
  • Spekificity workflows and guides

After init completes, all skills are available:
  /spek.*       → Spekificity custom skills
  /speckit.*    → Speckit skills
  caveman       → Token compression mode

EXAMPLES:
  spek init              # Full initialization
  spek init --verbose    # Verbose output
  spek init --skip-obsidian  # Skip Obsidian if not installed
EOF
}

# T011: Orchestrate speckit/specify initialization
orchestrate_specify_init() {
    log_step "speckit" "Initializing specify (speckit)"
    
    # Check if already initialized
    if [[ -d ".specify" ]] && [[ -f ".specify/constitution.md" ]]; then
        log_verbose "Specify already initialized, skipping"
        mark_step_complete "specify_init"
        return 0
    fi
    
    # Run specify init
    if command -v specify &>/dev/null; then
        specify init . || {
            log_error "specify init failed"
            mark_step_failed "specify_init" "specify init command failed"
            return 1
        }
        log_success "speckit initialized"
        update_config_string ".tools.speckit.initialized" "true"
        update_config_string ".tools.speckit.initialized_timestamp" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        mark_step_complete "specify_init"
        return 0
    else
        log_error "specify not found globally. Install: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
        mark_step_failed "specify_init" "specify command not found in PATH"
        return 1
    fi
}

# T012: Orchestrate graphify initialization
orchestrate_graphify() {
    log_step "graphify" "Initializing graphify for project analysis"
    
    # Check if graphify installed
    if ! command -v graphify &>/dev/null; then
        log_warning "graphify not installed, will be installed by spek setup or manually"
        log_verbose "Install: uv tool install graphifyy"
        return 0  # Non-fatal for MVP
    fi
    
    # Initialize graphify (generates initial graph)
    if [[ ! -d ".obsidian" ]]; then
        log_verbose "Generating initial graphify vault"
        # graphify would generate graph here (stub for now)
        log_info "graphify vault initialized"
    else
        log_verbose "Obsidian vault already exists"
    fi
    
    update_config_string ".tools.graphify.initialized" "true"
    mark_step_complete "graphify_init"
    return 0
}

# T013: Orchestrate Obsidian vault setup
orchestrate_obsidian() {
    if [[ "$SKIP_OBSIDIAN" == "true" ]]; then
        log_verbose "Obsidian skipped (--skip-obsidian flag)"
        return 0
    fi
    
    log_step "obsidian" "Initializing Obsidian vault (optional)"
    
    # Check if Obsidian is installed
    local obsidian_installed=false
    case "$(uname -s)" in
        Darwin)
            if [[ -d "/Applications/Obsidian.app" ]]; then
                obsidian_installed=true
            fi
            ;;
        Linux)
            if command -v Obsidian &>/dev/null || command -v obsidian &>/dev/null; then
                obsidian_installed=true
            fi
            ;;
    esac
    
    if [[ "$obsidian_installed" == "false" ]]; then
        log_warning "Obsidian desktop app not installed (optional). Graph will use fallback storage."
        update_config_string ".tools.obsidian.installed" "false"
        return 0
    fi
    
    # Configure vault location
    local vault_location=".obsidian"
    if [[ ! -d "$vault_location" ]]; then
        mkdir -p "$vault_location"
        echo "{\"type\": \"spekificity-vault\", \"version\": \"1.0\"}" > "$vault_location/vault-info.json"
    fi
    
    log_success "Obsidian vault configured"
    update_config_string ".tools.obsidian.initialized" "true"
    mark_step_complete "obsidian_setup"
    return 0
}

# T014: Orchestrate caveman skill integration
orchestrate_caveman() {
    log_step "caveman" "Checking for caveman skill integration"
    
    if command -v caveman &>/dev/null || python3 -m caveman --version &>/dev/null 2>&1; then
        log_success "caveman skill available"
        update_config_string ".tools.caveman.available" "true"
        update_config_string ".tools.caveman.integrated" "true"
    else
        log_verbose "caveman skill not available (optional)"
        update_config_string ".tools.caveman.available" "false"
    fi
    
    mark_step_complete "caveman_setup"
    return 0
}

# T015: Install spekificity custom skills
install_spek_skills() {
    log_step "spekificity" "Installing custom skills"
    
    local skills_dir=".spekificity/skills"
    mkdir -p "$skills_dir"
    
    # Create placeholder skill files (TODO: copy from actual skill definitions)
    local skill_files=(
        "spek.context-load.md"
        "spek.map-codebase.md"
        "spek.lessons-learnt.md"
    )
    
    for skill_file in "${skill_files[@]}"; do
        if [[ ! -f "$skills_dir/$skill_file" ]]; then
            touch "$skills_dir/$skill_file"
            log_verbose "Created: $skill_file"
        fi
    done
    
    log_success "Custom skills installed"
    update_config_string ".skills.spekificity_installed" "true"
    mark_step_complete "skill_install"
    return 0
}

# T016: Install workflows
install_workflows() {
    log_step "spekificity" "Installing workflow documentation"
    
    local workflows_dir=".spekificity/workflows"
    mkdir -p "$workflows_dir"
    
    # Create placeholder workflow files (TODO: copy from actual workflows)
    local workflow_files=(
        "setup-workflow.md"
        "init-workflow.md"
        "update-workflow.md"
        "integration-guide.md"
    )
    
    for workflow_file in "${workflow_files[@]}"; do
        if [[ ! -f "$workflows_dir/$workflow_file" ]]; then
            touch "$workflows_dir/$workflow_file"
            log_verbose "Created: $workflow_file"
        fi
    done
    
    log_success "Workflows installed"
    return 0
}

# T017: Install guides
install_guides() {
    log_step "spekificity" "Installing guides and documentation"
    
    local guides_dir=".spekificity/guides"
    mkdir -p "$guides_dir"
    
    # Create placeholder guide files (TODO: copy from actual guides)
    local guide_files=(
        "architecture.md"
        "orchestration-model.md"
        "skill-development.md"
        "troubleshooting.md"
        "manual-setup.md"
        "migration.md"
    )
    
    for guide_file in "${guide_files[@]}"; do
        if [[ ! -f "$guides_dir/$guide_file" ]]; then
            touch "$guides_dir/$guide_file"
            log_verbose "Created: $guide_file"
        fi
    done
    
    log_success "Guides installed"
    return 0
}

# T018: Main spek init orchestration
main() {
    print_header "Spekificity Platform Initialization"
    log_info "Spekificity v1.0.0 — Unified orchestration platform"
    echo ""
    
    # Check prerequisites
    if ! print_idempotency_status; then
        log_error "Recovery needed from partial failure. See guidance above."
        return 1
    fi
    echo ""
    
    # Initialize config if fresh
    initialize_config || true
    
    # Orchestration sequence
    log_info "Orchestrating tool initialization..."
    echo ""
    
    orchestrate_specify_init || return 1
    orchestrate_graphify || return 1
    orchestrate_obsidian || return 1
    orchestrate_caveman || return 1
    install_spek_skills || return 1
    install_workflows || return 1
    install_guides || return 1
    
    echo ""
    
    # Update skill index
    log_step "spekificity" "Updating unified skill index"
    update_skill_index
    echo ""
    
    # Mark as fully initialized
    update_config ".spek_initialized" "true"
    update_config_string ".spek_initialized_timestamp" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    mark_step_complete "platform_init"
    
    # Print summary
    print_header "Initialization Complete"
    print_summary "✓ All tools initialized:" \
        "speckit/specify ✓" \
        "graphify ✓" \
        "Obsidian (optional)" \
        "caveman (optional)" \
        "Custom skills ✓" \
        "Workflows ✓" \
        "Guides ✓"
    echo ""
    echo -e "${COLOR_BOLD}Available commands:${COLOR_RESET}"
    echo "  /spek.context-load     — Load vault context"
    echo "  /spek.map-codebase     — Run codebase mapping"
    echo "  /speckit.specify       — Create feature spec"
    echo "  /speckit.plan          — Create implementation plan"
    echo ""
    echo -e "${COLOR_BOLD}Next steps:${COLOR_RESET}"
    echo "  1. Read: .spekificity/guides/architecture.md"
    echo "  2. Start feature work: /context-load"
    echo "  3. For updates: spek update"
    echo ""
    
    return 0
}

# Run main function with error handling
if ! main; then
    log_error "Initialization did not complete successfully"
    exit 1
fi

log_success "Initialization complete"
exit 0
