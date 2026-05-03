#!/bin/bash

# prerequisites.sh — Prerequisite detection and installation guidance for spekificity
# Detects system tools (Python, uv, git, speckit, graphify, obsidian) and provides install instructions

set -euo pipefail

# Source logging
source "$(dirname "${BASH_SOURCE[0]}")/logging.sh"

# Detect Python 3.11+
check_python() {
    log_verbose "Checking for Python 3.11+"
    
    local python_cmd
    if command -v python3 &>/dev/null; then
        python_cmd="python3"
    elif command -v python &>/dev/null; then
        python_cmd="python"
    else
        log_error "Python not found"
        echo "Install: https://www.python.org/downloads/" >&2
        return 1
    fi
    
    local version=$($python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' 2>/dev/null || echo "0.0")
    log_verbose "Python version: $version"
    
    # Version check (3.11+)
    if [[ $(echo "$version 3.11" | awk '{print ($1 >= $2)}') -eq 1 ]]; then
        print_summary_row "Python" "installed" "$version"
        export PYTHON_CMD="$python_cmd"
        return 0
    else
        log_error "Python version $version < 3.11 required"
        echo "Upgrade: brew install python@3.11" >&2
        return 1
    fi
}

# Detect uv package manager
check_uv() {
    log_verbose "Checking for uv package manager"
    
    if command -v uv &>/dev/null; then
        local version=$(uv --version 2>/dev/null | awk '{print $2}')
        print_summary_row "uv" "installed" "$version"
        return 0
    else
        log_error "uv not found"
        echo "Install: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
        return 1
    fi
}

# Detect git
check_git() {
    log_verbose "Checking for git"
    
    if command -v git &>/dev/null; then
        local version=$(git --version | awk '{print $3}')
        print_summary_row "git" "installed" "$version"
        return 0
    else
        log_error "git not found"
        echo "Install: Use your OS package manager (brew, apt, etc.)" >&2
        return 1
    fi
}

# Detect speckit (global)
check_speckit() {
    log_verbose "Checking for speckit globally"
    
    if command -v specify &>/dev/null; then
        local version=$(specify --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
        print_summary_row "speckit/specify" "installed" "$version"
        return 0
    else
        log_warning "speckit/specify not found (will be installed by spek init)"
        print_summary_row "speckit/specify" "missing" ""
        return 1
    fi
}

# Detect graphify (global)
check_graphify() {
    log_verbose "Checking for graphify"
    
    if command -v graphify &>/dev/null; then
        local version=$(graphify --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
        print_summary_row "graphify" "installed" "$version"
        return 0
    else
        log_warning "graphify not found (will be installed by spek init)"
        print_summary_row "graphify" "missing" ""
        return 1
    fi
}

# Detect Obsidian (optional)
check_obsidian() {
    log_verbose "Checking for Obsidian (optional)"
    
    local obsidian_path
    case "$(uname -s)" in
        Darwin)
            obsidian_path="/Applications/Obsidian.app/Contents/MacOS/Obsidian"
            ;;
        Linux)
            obsidian_path=$(which Obsidian 2>/dev/null || echo "")
            ;;
        *)
            obsidian_path=""
            ;;
    esac
    
    if [[ -n "$obsidian_path" ]] && [[ -x "$obsidian_path" ]]; then
        print_summary_row "Obsidian" "optional (installed)" "desktop"
        return 0
    else
        print_summary_row "Obsidian" "optional" "not installed"
        log_info "Obsidian is optional. Spekificity works with or without it."
        return 1
    fi
}

# Detect caveman skill (optional)
check_caveman() {
    log_verbose "Checking for caveman skill"
    
    if command -v caveman &>/dev/null || python3 -m caveman --version &>/dev/null 2>&1; then
        print_summary_row "caveman skill" "optional (available)" ""
        return 0
    else
        print_summary_row "caveman skill" "optional" "not available"
        return 1
    fi
}

# Run all prerequisite checks
check_all_prerequisites() {
    print_header "Prerequisite Detection"
    echo ""
    echo "Checking for required and optional tools..."
    echo ""
    
    local required_ok=true
    
    # Required prerequisites
    echo -e "${COLOR_BOLD}Required:${COLOR_RESET}"
    check_python || required_ok=false
    check_uv || required_ok=false
    check_git || required_ok=false
    
    echo ""
    echo -e "${COLOR_BOLD}Third-party (installed later by spek init if missing):${COLOR_RESET}"
    check_speckit || true
    check_graphify || true
    
    echo ""
    echo -e "${COLOR_BOLD}Optional:${COLOR_RESET}"
    check_obsidian || true
    check_caveman || true
    
    if [[ "$required_ok" == "false" ]]; then
        log_error "Some required prerequisites are missing. Install them and run 'spek setup' again."
        return 1
    fi
    
    return 0
}

# Export functions if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f check_python
    export -f check_uv
    export -f check_git
    export -f check_speckit
    export -f check_graphify
    export -f check_obsidian
    export -f check_caveman
    export -f check_all_prerequisites
fi
