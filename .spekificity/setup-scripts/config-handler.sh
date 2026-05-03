#!/bin/bash

# config-handler.sh — Spekificity configuration management functions
# Handles creation, validation, migration, and updates to .spekificity/config.json

set -euo pipefail

# Configuration file path (relative to project root)
CONFIG_FILE=".spekificity/config.json"
CONFIG_SCHEMA=".spekificity/config-schema.json"

# Initialize default config if not exists
initialize_config() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << EOF
{
  "spek_version": "1.0.0",
  "spek_initialized": false,
  "spek_initialized_timestamp": "$timestamp",
  "spek_platform_branch": "$branch",
  "spek_schema_version": "1.0",
  "tools": {
    "speckit": {
      "installed": false,
      "version": null,
      "initialized": false,
      "initialized_timestamp": null
    },
    "graphify": {
      "installed": false,
      "version": null,
      "initialized": false,
      "vault_location": null
    },
    "obsidian": {
      "installed": false,
      "version": null,
      "optional": true,
      "initialized": false,
      "vault_location": null
    },
    "caveman": {
      "available": false,
      "integrated": false,
      "last_check": null
    }
  },
  "skills": {
    "spekificity_installed": false,
    "speckit_installed": false,
    "caveman_installed": false,
    "last_skill_index_update": null
  },
  "spek_custom_preferences": {},
  "orchestration_history": []
}
EOF
        return 0
    fi
    return 1  # Config already exists
}

# Read config value using jq
read_config() {
    local key="$1"
    if [[ -f "$CONFIG_FILE" ]]; then
        jq -r "$key // empty" "$CONFIG_FILE" 2>/dev/null || echo ""
    fi
}

# Update config value using jq
update_config() {
    local key="$1"
    local value="$2"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Error: Config file not found at $CONFIG_FILE" >&2
        return 1
    fi
    
    # Use jq to update; preserve formatting
    local temp_file="${CONFIG_FILE}.tmp"
    jq "$key = $value" "$CONFIG_FILE" > "$temp_file"
    mv "$temp_file" "$CONFIG_FILE"
}

# Update config with string value
update_config_string() {
    local key="$1"
    local value="$2"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Error: Config file not found at $CONFIG_FILE" >&2
        return 1
    fi
    
    local temp_file="${CONFIG_FILE}.tmp"
    jq "$key = \"$value\"" "$CONFIG_FILE" > "$temp_file"
    mv "$temp_file" "$CONFIG_FILE"
}

# Record orchestration step in history
record_orchestration_step() {
    local operation="$1"      # setup, init, update
    local step="$2"           # step name (e.g., "prerequisites_check", "specify_init")
    local status="$3"         # success, failure, skipped
    local error_msg="${4:-}"  # optional error message
    
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Error: Config file not found at $CONFIG_FILE" >&2
        return 1
    fi
    
    local temp_file="${CONFIG_FILE}.tmp"
    local entry="{\"operation\": \"$operation\", \"step\": \"$step\", \"status\": \"$status\", \"timestamp\": \"$timestamp\""
    
    if [[ -n "$error_msg" ]]; then
        entry+=", \"error_message\": \"$error_msg\""
    else
        entry+=", \"error_message\": null"
    fi
    entry+="}"
    
    jq ".orchestration_history += [$entry]" "$CONFIG_FILE" > "$temp_file"
    mv "$temp_file" "$CONFIG_FILE"
}

# Validate config schema
validate_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Error: Config file not found at $CONFIG_FILE" >&2
        return 1
    fi
    
    if [[ ! -f "$CONFIG_SCHEMA" ]]; then
        echo "Warning: Config schema not found at $CONFIG_SCHEMA. Skipping validation." >&2
        return 0
    fi
    
    # Simple validation: check required fields
    local required_fields=("spek_version" "spek_initialized" "spek_initialized_timestamp" "spek_platform_branch")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$CONFIG_FILE" > /dev/null 2>&1; then
            echo "Error: Required field '$field' missing from config" >&2
            return 1
        fi
    done
    
    return 0
}

# Repair missing fields in config
repair_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "Error: Config file not found at $CONFIG_FILE" >&2
        return 1
    fi
    
    local temp_file="${CONFIG_FILE}.tmp"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Ensure all required fields exist with defaults
    jq '
        .spek_version //= "1.0.0" |
        .spek_initialized //= false |
        .spek_initialized_timestamp //= "'$timestamp'" |
        .spek_platform_branch //= "unknown" |
        .spek_schema_version //= "1.0" |
        .tools //= {} |
        .tools.speckit //= {installed: false, version: null, initialized: false} |
        .tools.graphify //= {installed: false, version: null, initialized: false} |
        .tools.obsidian //= {installed: false, version: null, optional: true, initialized: false} |
        .tools.caveman //= {available: false, integrated: false} |
        .skills //= {spekificity_installed: false, speckit_installed: false, caveman_installed: false} |
        .spek_custom_preferences //= {} |
        .orchestration_history //= []
    ' "$CONFIG_FILE" > "$temp_file"
    
    mv "$temp_file" "$CONFIG_FILE"
    echo "Config repaired successfully"
}

# Check if project is already initialized
is_already_initialized() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 1
    fi
    
    local initialized=$(read_config ".spek_initialized")
    [[ "$initialized" == "true" ]]
}

# Detect partial failure (incomplete initialization)
detect_partial_failure() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 1  # No config = no partial failure
    fi
    
    local initialized=$(read_config ".spek_initialized")
    local history_count=$(jq '.orchestration_history | length' "$CONFIG_FILE")
    
    # Partial failure: not initialized but has history entries
    if [[ "$initialized" != "true" ]] && [[ $history_count -gt 0 ]]; then
        return 0  # Partial failure detected
    fi
    
    return 1  # No partial failure
}

# Export functions if sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    export -f initialize_config
    export -f read_config
    export -f update_config
    export -f update_config_string
    export -f record_orchestration_step
    export -f validate_config
    export -f repair_config
    export -f is_already_initialized
    export -f detect_partial_failure
fi
