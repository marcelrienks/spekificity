#!/bin/bash

# update.sh — spek update command
# Updates the spekificity custom layer (skills, scripts, workflows, guides).
# Does NOT modify third-party tools (speckit, graphify, obsidian, caveman).
# FR-021: idempotent — running on an already-current installation exits 0.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/logging.sh"
source "$SCRIPT_DIR/config-handler.sh"

# ── flags ──────────────────────────────────────────────────────────────────────
DRY_RUN=false
FORCE=false

print_help() {
    cat << EOF
Usage: spek update [OPTIONS]

Update spekificity custom layer independently.
Only updates skills, scripts, and workflows — NOT speckit, graphify, or obsidian.

OPTIONS:
  --dry-run       Show what would be updated without making changes
  --force         Overwrite even if destination is newer (user modifications)
  --verbose       Show detailed output
  -h, --help      Show this help message

EXAMPLES:
  spek update              # Update to latest version
  spek update --dry-run    # Preview changes without applying
  spek update --force      # Force overwrite (discards local customisations)
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)   DRY_RUN=true ;;
        --force)     FORCE=true ;;
        --verbose)   VERBOSE_MODE=true ;;
        -h|--help)   print_help; exit 0 ;;
        *) log_error "Unknown option: $1"; print_help; exit 1 ;;
    esac
    shift
done

# ── resolve source root ────────────────────────────────────────────────────────
# The spekificity source tree is two levels up from setup-scripts/:
#   .spekificity/setup-scripts/ → .spekificity/ → <project root>
SPEKIFICITY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST_SKILLS_DIR="${SPEKIFICITY_DIR}/skills"

# ── version check (idempotency guard) ─────────────────────────────────────────
SOURCE_VERSION_FILE="${SOURCE_ROOT}/.spekificity/version.txt"
INSTALLED_VERSION_FILE="${SPEKIFICITY_DIR}/version.txt"

SOURCE_VERSION=""
INSTALLED_VERSION=""
[[ -f "${SOURCE_VERSION_FILE}" ]]    && SOURCE_VERSION="$(cat "${SOURCE_VERSION_FILE}" | tr -d '[:space:]')"
[[ -f "${INSTALLED_VERSION_FILE}" ]] && INSTALLED_VERSION="$(cat "${INSTALLED_VERSION_FILE}" | tr -d '[:space:]')"

if [[ -n "${SOURCE_VERSION}" && -n "${INSTALLED_VERSION}" ]]; then
    if [[ "${SOURCE_VERSION}" == "${INSTALLED_VERSION}" && "${FORCE}" == "false" ]]; then
        log_info "Already up to date (version ${INSTALLED_VERSION})"
        exit 0
    fi
fi

if [[ "${DRY_RUN}" == "true" ]]; then
    print_header "Spekificity Update — Dry Run Preview"
    log_info "Source version:    ${SOURCE_VERSION:-unknown}"
    log_info "Installed version: ${INSTALLED_VERSION:-unknown}"
    echo ""
else
    print_header "Spekificity Update"
    log_info "Source version:    ${SOURCE_VERSION:-unknown}"
    log_info "Installed version: ${INSTALLED_VERSION:-unknown}"
    echo ""
fi

UPDATED_COUNT=0
SKIPPED_COUNT=0

# ── helper: copy_if_newer ─────────────────────────────────────────────────────
# copy_if_newer <src> <dest>
# Copies src to dest only if src is newer than dest (or dest is missing),
# unless --force is set. In dry-run mode, prints what would happen.
copy_if_newer() {
    local src="$1"
    local dest="$2"
    local label="${3:-$(basename "$src")}"

    if [[ ! -f "${src}" ]]; then
        return 0
    fi

    local should_copy=false
    if [[ ! -f "${dest}" ]]; then
        should_copy=true
    elif [[ "${FORCE}" == "true" ]]; then
        should_copy=true
    else
        # Compare mtimes: copy only if src is strictly newer
        local src_ts dest_ts
        if stat --version &>/dev/null 2>&1; then
            src_ts=$(stat -c %Y "${src}" 2>/dev/null || echo 0)
            dest_ts=$(stat -c %Y "${dest}" 2>/dev/null || echo 0)
        else
            src_ts=$(stat -f %m "${src}" 2>/dev/null || echo 0)
            dest_ts=$(stat -f %m "${dest}" 2>/dev/null || echo 0)
        fi
        [[ "${src_ts}" -gt "${dest_ts}" ]] && should_copy=true
    fi

    if [[ "${should_copy}" == "true" ]]; then
        if [[ "${DRY_RUN}" == "true" ]]; then
            echo "  [would update] ${label}"
        else
            mkdir -p "$(dirname "${dest}")"
            cp "${src}" "${dest}"
            log_verbose "Updated: ${label}"
        fi
        (( UPDATED_COUNT++ )) || true
    else
        log_verbose "Skip (up to date): ${label}"
        (( SKIPPED_COUNT++ )) || true
    fi
}

# ── 1. Update spek.* skills ────────────────────────────────────────────────────
log_step "skills" "Updating spek.* skills"
SOURCE_SKILLS_DIR="${SOURCE_ROOT}/.spekificity/skills"
if [[ -d "${SOURCE_SKILLS_DIR}" ]]; then
    while IFS= read -r src_file; do
        fname="$(basename "${src_file}")"
        copy_if_newer "${src_file}" "${DEST_SKILLS_DIR}/${fname}" "skills/${fname}"
    done < <(find "${SOURCE_SKILLS_DIR}" -maxdepth 1 -name "spek.*.md" 2>/dev/null)
fi

# ── 2. Update project-root skills (context-load, map-codebase, lessons-learnt) ─
log_step "skills" "Updating project skills"
SOURCE_SKILLS_ROOT="${SOURCE_ROOT}/skills"
DEST_SKILLS_ROOT="${SOURCE_ROOT}/skills"
# These live in source root — no copy needed unless running from installed copy.
# If SOURCE_ROOT != project root (i.e. running from a globally-installed spek),
# copy updated skill files to the target project's skills/ directory.
if [[ "${SOURCE_ROOT}" != "$(pwd)" ]]; then
    for skill_dir in context-load map-codebase lessons-learnt; do
        src="${SOURCE_SKILLS_ROOT}/${skill_dir}/skill.md"
        dest="${DEST_SKILLS_ROOT}/${skill_dir}/skill.md"
        copy_if_newer "${src}" "${dest}" "skills/${skill_dir}/skill.md"
    done
fi

# ── 3. Update bin scripts ─────────────────────────────────────────────────────
log_step "scripts" "Updating bin scripts"
SOURCE_BIN="${SOURCE_ROOT}/.spekificity/bin"
DEST_BIN="${SPEKIFICITY_DIR}/bin"
for script in _lib.sh prepare.sh automate.sh post.sh; do
    copy_if_newer "${SOURCE_BIN}/${script}" "${DEST_BIN}/${script}" "bin/${script}"
done

# ── 4. Update setup-scripts (non-destructive: skip if dest is newer) ──────────
log_step "scripts" "Updating setup-scripts"
for script in setup.sh init.sh status.sh update.sh; do
    copy_if_newer "${SCRIPT_DIR}/${script}" "${SPEKIFICITY_DIR}/setup-scripts/${script}" "setup-scripts/${script}" || true
done

# ── 5. Regenerate skill-index.md ──────────────────────────────────────────────
if [[ "${DRY_RUN}" == "false" ]]; then
    log_step "index" "Regenerating skill-index.md"
    SKILL_INDEX="${SPEKIFICITY_DIR}/skill-index.md"
    {
        echo "# skill index"
        echo ""
        echo "_auto-generated by \`spek update\` on $(date '+%Y-%m-%d')_"
        echo ""
        echo "| command | file | status |"
        echo "|---------|------|--------|"
        # spek.* skills
        if [[ -d "${DEST_SKILLS_DIR}" ]]; then
            while IFS= read -r f; do
                cmd="/$(basename "${f}" .md)"
                echo "| \`${cmd}\` | \`.spekificity/skills/$(basename "${f}")\` | ✓ installed |"
            done < <(find "${DEST_SKILLS_DIR}" -maxdepth 1 -name "spek.*.md" | sort)
        fi
        # speckit.* skills from .github/agents/
        AGENTS_DIR="${SOURCE_ROOT}/.github/agents"
        if [[ -d "${AGENTS_DIR}" ]]; then
            while IFS= read -r f; do
                cmd="/$(basename "${f}" .md)"
                echo "| \`${cmd}\` | \`.github/agents/$(basename "${f}")\` | ✓ installed |"
            done < <(find "${AGENTS_DIR}" -maxdepth 1 -name "speckit.*.md" 2>/dev/null | sort)
        fi
    } > "${SKILL_INDEX}"
    log_info "Skill index regenerated: ${SKILL_INDEX}"
fi

# ── 6. Bump installed version ─────────────────────────────────────────────────
if [[ "${DRY_RUN}" == "false" && -n "${SOURCE_VERSION}" ]]; then
    echo "${SOURCE_VERSION}" > "${INSTALLED_VERSION_FILE}"
    write_config ".spek_version" "\"${SOURCE_VERSION}\""
fi

# ── summary ───────────────────────────────────────────────────────────────────
echo ""
if [[ "${DRY_RUN}" == "true" ]]; then
    log_info "Dry run complete. ${UPDATED_COUNT} file(s) would be updated, ${SKIPPED_COUNT} already up to date."
    log_info "Run without --dry-run to apply changes."
else
    if [[ ${UPDATED_COUNT} -eq 0 ]]; then
        log_info "Already up to date — no changes applied."
    else
        log_success "Update complete. ${UPDATED_COUNT} file(s) updated."
        [[ -n "${SOURCE_VERSION}" ]] && log_info "Version: ${SOURCE_VERSION}"
    fi
fi

exit 0

