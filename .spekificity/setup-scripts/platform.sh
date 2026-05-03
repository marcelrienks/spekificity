#!/bin/bash

# platform.sh — Multi-platform support (macOS, Linux, Windows/WSL)
# Detects OS and provides platform-specific installation commands

set -euo pipefail

# Source logging
source "$(dirname "${BASH_SOURCE[0]}")/logging.sh"

# Detect platform and package manager
detect_platform() {
    local os_type=$(uname -s)
    local is_wsl=false
    
    # Check for WSL
    if grep -qi microsoft /proc/version 2>/dev/null; then
        is_wsl=true
    fi
    
    case "$os_type" in
        Darwin)
            log_verbose "Platform: macOS"
            export PLATFORM="macos"
            export PKG_MANAGER="brew"
            ;;
        Linux)
            if [[ "$is_wsl" == "true" ]]; then
                log_verbose "Platform: Windows (WSL)"
                export PLATFORM="wsl"
                export PKG_MANAGER="apt"
            else
                log_verbose "Platform: Linux"
                export PLATFORM="linux"
                
                # Detect package manager
                if command -v apt &>/dev/null; then
                    export PKG_MANAGER="apt"
                elif command -v yum &>/dev/null; then
                    export PKG_MANAGER="yum"
                elif command -v pacman &>/dev/null; then
                    export PKG_MANAGER="pacman"
                elif command -v zypper &>/dev/null; then
                    export PKG_MANAGER="zypper"
                else
                    export PKG_MANAGER="unknown"
                fi
            fi
            ;;
        MINGW* | MSYS* | CYGWIN*)
            log_verbose "Platform: Windows (native shell)"
            export PLATFORM="windows"
            export PKG_MANAGER="choco"  # Assuming Chocolatey for Windows
            ;;
        *)
            log_error "Unsupported platform: $os_type"
            return 1
            ;;
    esac
    
    log_info "Detected: $PLATFORM ($os_type) with package manager: $PKG_MANAGER"
    return 0
}

# Get installation command for a tool on current platform
get_install_command() {
    local tool="$1"
    
    case "$PLATFORM" in
        macos)
            case "$tool" in
                python)
                    echo "brew install python@3.11"
                    ;;
                uv)
                    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
                    ;;
                git)
                    echo "brew install git"
                    ;;
                speckit)
                    echo "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
                    ;;
                graphify)
                    echo "uv tool install graphifyy"
                    ;;
                obsidian)
                    echo "Download from https://obsidian.md/ and install"
                    ;;
                *)
                    echo "Unknown tool: $tool"
                    ;;
            esac
            ;;
        linux | wsl)
            case "$tool" in
                python)
                    echo "sudo $PKG_MANAGER update && sudo $PKG_MANAGER install -y python3.11 python3.11-venv"
                    ;;
                uv)
                    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
                    ;;
                git)
                    echo "sudo $PKG_MANAGER install -y git"
                    ;;
                speckit)
                    echo "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
                    ;;
                graphify)
                    echo "uv tool install graphifyy"
                    ;;
                obsidian)
                    echo "Download from https://obsidian.md/ or use snap/appimage"
                    ;;
                *)
                    echo "Unknown tool: $tool"
                    ;;
            esac
            ;;
        windows)
            case "$tool" in
                python)
                    echo "choco install python311 (or download from https://www.python.org/downloads/)"
                    ;;
                uv)
                    echo "iwr https://astral.sh/uv/install.ps1 | iex (PowerShell) or use WSL"
                    ;;
                git)
                    echo "choco install git (or https://git-scm.com/download/win)"
                    ;;
                speckit)
                    echo "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
                    ;;
                graphify)
                    echo "uv tool install graphifyy"
                    ;;
                obsidian)
                    echo "Download from https://obsidian.md/ and install"
                    ;;
                *)
                    echo "Unknown tool: $tool"
                    ;;
            esac
            ;;
        *)
            log_error "Unknown platform: $PLATFORM"
            return 1
            ;;
    esac
}

# Print platform information
print_platform_info() {
    print_header "Platform Information"
    log_info "Platform: $PLATFORM"
    log_info "Package Manager: $PKG_MANAGER"
    log_info "OS: $(uname -s)"
    log_info "Architecture: $(uname -m)"
}

# Export functions if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f detect_platform
    export -f get_install_command
    export -f print_platform_info
fi
