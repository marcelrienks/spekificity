# Spekificity Platform Directory

Local per-project spekificity platform configuration, skills, and orchestration.

## Directory Structure

- **`setup-scripts/`** — Bash scripts for `spek setup`, `spek init`, `spek update`, `spek status` commands
- **`skills/`** — Spekificity custom skill files (markdown, prefixed with `spek.*`)
- **`workflows/`** — Workflow documentation (setup-workflow.md, init-workflow.md, update-workflow.md, integration-guide.md)
- **`guides/`** — Developer and user guides (architecture.md, orchestration-model.md, skill-development.md, troubleshooting.md, manual-setup.md, migration.md)

## Configuration Files

- **`config.json`** — Orchestration state and project configuration (created by `spek init`)
- **`version.txt`** — Current spekificity platform version (1.0.0)
- **`skill-index.md`** — Unified skill discovery index (created/updated by `spek init`)
- **`config-schema.json`** — JSON schema for config validation

## Usage

Users interact primarily via `spek` commands:

```bash
spek setup    # Detect and install prerequisites
spek init     # Orchestrate all tool initialization
spek update   # Update custom spekificity layer
spek status   # Check initialization and integration status
```

All orchestration is driven by scripts in `setup-scripts/` and state tracked in `config.json`.

---

**Version**: 1.0.0  
**Status**: Platform initialization in progress
