# Data Model: Spekificity Platform

**Purpose**: Defines entity schemas and configuration structures for the spekificity platform.

## Configuration Schema (`.spekificity/config.json`)

Core orchestration state and project configuration.

```json
{
  "spek_version": "1.0.0",
  "spek_initialized": true,
  "spek_initialized_timestamp": "2026-05-03T15:00:00Z",
  "spek_platform_branch": "002-spek-platform-lifecycle",
  "spek_schema_version": "1.0",
  "tools": {
    "speckit": {
      "installed": true,
      "version": "0.1.0",
      "initialized": true,
      "initialized_timestamp": "2026-05-03T15:01:00Z"
    },
    "graphify": {
      "installed": true,
      "version": "1.0.0",
      "initialized": true,
      "vault_location": ".obsidian"
    },
    "obsidian": {
      "installed": false,
      "optional": true,
      "initialized": false,
      "vault_location": null
    },
    "caveman": {
      "available": true,
      "integrated": true,
      "last_check": "2026-05-03T15:01:00Z"
    }
  },
  "skills": {
    "spekificity_installed": true,
    "speckit_installed": true,
    "caveman_installed": true,
    "last_skill_index_update": "2026-05-03T15:02:00Z"
  },
  "spek_custom_preferences": {},
  "orchestration_history": [
    {
      "operation": "init",
      "step": "specify_init",
      "status": "success",
      "timestamp": "2026-05-03T15:01:00Z",
      "error_message": null
    }
  ]
}
```

## Entity Definitions

### Orchestration State

Tracks overall platform initialization and tool integration status.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spek_version` | string | yes | Semantic version of spekificity (e.g., "1.0.0") |
| `spek_initialized` | boolean | yes | Whether platform is fully initialized |
| `spek_initialized_timestamp` | ISO 8601 | yes | When initialization completed |
| `spek_platform_branch` | string | yes | Git branch name (e.g., "002-spek-platform-lifecycle") |
| `spek_schema_version` | string | yes | Config schema version (for migrations) |

### Tool Integration Status

Each tool (speckit, graphify, obsidian, caveman) tracks its own initialization state.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `installed` | boolean | no | Whether tool is installed globally |
| `version` | string | no | Semantic version if installed |
| `initialized` | boolean | yes | Whether tool initialized in this project |
| `initialized_timestamp` | ISO 8601 | no | When initialization completed |
| `vault_location` | string | no | Path to vault (graphify/obsidian) |

### Skill Installation Status

Tracks which skill layers are installed.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spekificity_installed` | boolean | yes | Spekificity custom skills installed |
| `speckit_installed` | boolean | yes | Speckit skills installed (via specify init) |
| `caveman_installed` | boolean | yes | Caveman skills installed |
| `last_skill_index_update` | ISO 8601 | no | When skill-index.md last updated |

### Orchestration History

Audit trail of all setup/init/update operations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | yes | "setup", "init", or "update" |
| `step` | string | yes | Step name (e.g., "specify_init", "graphify_setup") |
| `status` | string | yes | "success", "failure", or "skipped" |
| `timestamp` | ISO 8601 | yes | When step completed |
| `error_message` | string \| null | no | Error details if status is "failure" |

## Directory Structure

```
.spekificity/
├── config.json              # Orchestration state (instance-specific)
├── config-schema.json       # JSON schema for validation
├── version.txt              # Platform version (1.0.0)
├── skill-index.md           # Unified skill discovery index
├── README.md                # Directory guide
├── setup-scripts/
│   ├── setup.sh             # spek setup command
│   ├── init.sh              # spek init command
│   ├── update.sh            # spek update command
│   ├── status.sh            # spek status command
│   ├── prerequisites.sh     # Tool detection
│   ├── platform.sh          # Platform detection
│   ├── config-handler.sh    # Config management
│   ├── skill-discovery.sh   # Skill indexing
│   ├── idempotency.sh       # State tracking
│   └── logging.sh           # Structured output
├── skills/
│   ├── spek.context-load.md
│   ├── spek.map-codebase.md
│   ├── spek.lessons-learnt.md
│   └── [custom skills]
├── workflows/
│   ├── setup-workflow.md
│   ├── init-workflow.md
│   ├── update-workflow.md
│   └── integration-guide.md
└── guides/
    ├── architecture.md
    ├── orchestration-model.md
    ├── skill-development.md
    ├── troubleshooting.md
    ├── manual-setup.md
    └── migration.md
```

## State Transitions

```
Fresh Project:
  no config → spek setup → config (not initialized)
           ↓ spek init → config.spek_initialized = true

Already Initialized:
  config (initialized) + spek init → idempotent update (preserve state)
  
Partial Failure:
  config (not initialized) + history entries → recovery path
  ↓ spek init → detect failure, recover, resume
```

## Configuration Customization

Users can modify `spek_custom_preferences` (dict) to persist custom settings:

```json
{
  "spek_custom_preferences": {
    "graphify_analysis_depth": "full",
    "obsidian_enable": false,
    "update_frequency": "weekly",
    "auto_lessons_capture": true
  }
}
```

These preferences are preserved across updates and reinitializations.

---

**Next**: See `.spekificity/guides/` for user-facing documentation and skill development patterns.
