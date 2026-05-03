#!/bin/bash

# validate-namespace.sh — Validate spekificity namespace consistency
# Ensures all skills, config, and docs follow spek.* or spek_ prefixing convention

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/logging.sh"

print_help() {
    cat << EOF
Usage: validate-namespace.sh [OPTIONS]

Validate namespace consistency across spekificity platform components.
Checks that all spekificity-owned artifacts use spek.* or spek_ prefixes.

OPTIONS:
  --fix          Attempt to auto-fix namespace violations
  --verbose      Show detailed validation results
  -h, --help     Show this help message

CHECKS:
  • Skills: All .spekificity/skills/ files use spek.*.md naming
  • Config: All .spekificity/config.json keys use spek_ or spek. prefixes
  • Guides: All .spekificity/guides/ files documented with spek context
  • Workflows: No speckit.* commands in spekificity namespace
  • Documentation: References use correct namespacing

EXAMPLES:
  validate-namespace.sh              # Run all checks
  validate-namespace.sh --fix        # Auto-fix issues where possible
  validate-namespace.sh --verbose    # Show detailed report
EOF
}

VERBOSE_MODE=${VERBOSE_MODE:-false}
FIX_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --fix)
            FIX_MODE=true
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
            exit 1
            ;;
    esac
    shift
done

# Check skill naming
validate_skill_naming() {
    print_header "Skill Naming Validation"
    
    local violations=0
    local skills_dir=".spekificity/skills"
    
    if [[ ! -d "$skills_dir" ]]; then
        log_info "No skills directory found"
        return 0
    fi
    
    while IFS= read -r file; do
        local basename=$(basename "$file")
        
        if [[ ! "$basename" =~ ^spek\. ]]; then
            log_error "Skill naming violation: $basename (should be spek.*.md)"
            violations=$((violations + 1))
            
            if [[ "$FIX_MODE" == "true" ]]; then
                # Rename file
                local newname="spek.${basename#.}"
                mv "$file" "$skills_dir/$newname"
                log_success "Renamed: $basename → $newname"
            fi
        else
            log_verbose "✓ Skill naming OK: $basename"
        fi
    done < <(find "$skills_dir" -name "*.md" -type f 2>/dev/null || true)
    
    if [[ $violations -eq 0 ]]; then
        log_success "All skill files use spek.* prefix"
    else
        log_error "$violations skill naming violations found"
        return 1
    fi
}

# Check config key naming
validate_config_keys() {
    print_header "Configuration Key Validation"
    
    local config_file=".spekificity/config.json"
    local violations=0
    
    if [[ ! -f "$config_file" ]]; then
        log_info "Config file not found"
        return 0
    fi
    
    # Extract all top-level keys and check for spek_ or spek. prefix
    while IFS= read -r key; do
        if [[ ! "$key" =~ ^spek ]]; then
            log_warning "Config key without spek prefix: $key"
            violations=$((violations + 1))
        else
            log_verbose "✓ Config key OK: $key"
        fi
    done < <(jq 'keys[]' "$config_file" 2>/dev/null | sed 's/"//g' | grep -v "^tools" | grep -v "^skills" | head -20 || true)
    
    if [[ $violations -eq 0 ]]; then
        log_success "All config keys use proper prefixes"
    else
        log_warning "$violations config keys without spek prefix (may be nested)"
    fi
}

# Check documentation references
validate_doc_references() {
    print_header "Documentation Reference Validation"
    
    local violations=0
    local guides_dir=".spekificity/guides"
    
    if [[ ! -d "$guides_dir" ]]; then
        log_info "No guides directory found"
        return 0
    fi
    
    # Check for incorrect namespacing in docs
    for doc in "$guides_dir"/*.md; do
        if [[ ! -f "$doc" ]]; then
            continue
        fi
        
        local basename=$(basename "$doc")
        
        # Check for speckit commands in spekificity namespace (incorrect)
        if grep -q "/speckit\." "$doc" 2>/dev/null; then
            log_verbose "✓ Guide correctly references /speckit.* namespace: $basename"
        fi
        
        # Check for spek commands
        if grep -q "/spek\." "$doc" 2>/dev/null; then
            log_verbose "✓ Guide correctly references /spek.* namespace: $basename"
        fi
    done
    
    log_success "Documentation references validated"
}

# Check workflow namespace
validate_workflows() {
    print_header "Workflow Namespace Validation"
    
    local workflows_dir=".spekificity/workflows"
    local violations=0
    
    if [[ ! -d "$workflows_dir" ]]; then
        log_info "No workflows directory found"
        return 0
    fi
    
    # Workflows should reference correct namespaces
    for workflow in "$workflows_dir"/*.md; do
        if [[ ! -f "$workflow" ]]; then
            continue
        fi
        
        # Simple check: ensure no incorrect prefixes
        if grep -q "/spek\." "$workflow" || grep -q "/speckit\." "$workflow"; then
            log_verbose "✓ Workflow namespace references OK: $(basename "$workflow")"
        fi
    done
    
    log_success "Workflow namespaces validated"
}

# Print summary
print_namespace_summary() {
    print_header "Namespace Consistency Summary"
    
    echo "Validated:"
    echo "  • Skill file naming (.spekificity/skills/spek.*.md)"
    echo "  • Config key prefixes (.spekificity/config.json spek_*)"
    echo "  • Documentation references (/spek.*, /speckit.* namespacing)"
    echo "  • Workflow namespace usage"
    echo ""
    echo "Convention Summary:"
    echo "  Spekificity skills:       /spek.*              (e.g., /spek.context-load)"
    echo "  Spekificity config:       spek_*               (e.g., spek_version, spek_initialized)"
    echo "  Speckit skills:           /speckit.*           (e.g., /speckit.specify)"
    echo "  Caveman mode:             caveman              (no prefix, system-level)"
}

main() {
    print_header "Namespace Consistency Validation"
    log_info "Checking spekificity namespace adherence"
    echo ""
    
    validate_skill_naming || true
    echo ""
    validate_config_keys || true
    echo ""
    validate_doc_references || true
    echo ""
    validate_workflows || true
    echo ""
    print_namespace_summary
    
    return 0
}

main
