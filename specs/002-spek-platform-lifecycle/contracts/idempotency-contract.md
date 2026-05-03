# Contract: Idempotency & State Recovery

**Version**: 1.0.0  
**Namespace**: spekificity-idempotency  
**Status**: Active

## Purpose

Define contract for state tracking, idempotent execution, and recovery from partial failures in spekificity.

---

## State Detection Functions

### Function: `is_already_initialized()`

### Contract

```bash
is_already_initialized() -> boolean
```

### Behavior

1. **Check**: Does `.spekificity/config.json` exist?
2. **Check**: Is `spek_initialized` field `true`?
3. **Return**: `true` if both conditions met, else `false`

### Example

```bash
# First run
is_already_initialized()  # false (no config)

# After spek init
is_already_initialized()  # true (config.spek_initialized = true)

# On re-run
is_already_initialized()  # true (still initialized)
```

---

### Function: `detect_partial_failure()`

### Contract

```bash
detect_partial_failure() -> object | null
```

### Output

**If partial failure detected**:
```json
{
  "has_failure": true,
  "last_failed_step": "specify_init",
  "last_failed_timestamp": "2026-05-03T15:30:00Z",
  "recovery_required": true,
  "guidance": [
    "Run: uv tool install specify-cli --from git+...",
    "Then retry: spek init"
  ]
}
```

**If no failure**:
```json
{
  "has_failure": false,
  "recovery_required": false
}
```

### Behavior

1. **Check**: Config exists but `spek_initialized = false`?
2. **Analyze**: `orchestration_history` entries
3. **Identify**: Last entry with `status = "failure"`
4. **Provide**: Recovery guidance for that step
5. **Return**: Failure info or null

### Detection Logic

```bash
if config.json exists and spek_initialized == false:
    if orchestration_history has entries:
        for each entry in reverse:
            if entry.status == "failure":
                return {
                    has_failure: true,
                    last_failed_step: entry.step,
                    guidance: get_recovery_guidance(entry.step)
                }
        # All entries succeeded but not marked initialized
        return {
            has_failure: false,
            recovery_required: true,
            reason: "setup incomplete, retry spek init"
        }
    else:
        # Config exists but no history
        return {
            has_failure: false,
            recovery_required: false
        }
else:
    return null  # No failure
```

---

### Function: `validate_prerequisites()`

### Contract

```bash
validate_prerequisites() -> array<prerequisite_result>
```

### Output

```json
[
  {
    "prerequisite": "Python 3.11+",
    "available": true,
    "version": "3.11.6",
    "status": "✓"
  },
  {
    "prerequisite": "uv",
    "available": true,
    "version": "0.1.25",
    "status": "✓"
  },
  {
    "prerequisite": "git",
    "available": true,
    "version": "2.43.0",
    "status": "✓"
  },
  {
    "prerequisite": "specify",
    "available": false,
    "version": null,
    "status": "✗",
    "recovery": "uv tool install specify-cli --from git+..."
  }
]
```

### Behavior

1. **Check**: Each prerequisite (Python, uv, git, speckit, graphify, etc.)
2. **Detect**: Availability and version
3. **Classify**: Required (fatal) vs optional (non-fatal)
4. **Return**: Array of results with recovery guidance

---

## Orchestration History

### Data Structure

```json
{
  "orchestration_history": [
    {
      "step": "specify_init",
      "status": "success",
      "timestamp": "2026-05-03T15:30:00Z",
      "version": "0.1.0",
      "duration_ms": 2500
    },
    {
      "step": "graphify_init",
      "status": "failure",
      "timestamp": "2026-05-03T15:32:00Z",
      "error": "graphify: command not found",
      "duration_ms": 1200
    },
    {
      "step": "obsidian_setup",
      "status": "skipped",
      "reason": "optional, Obsidian not installed",
      "timestamp": "2026-05-03T15:33:00Z"
    }
  ]
}
```

### Status Values

- **success**: Step completed without errors
- **failure**: Step failed with error (blocking)
- **skipped**: Step skipped (non-fatal or already done)
- **partial**: Step completed with warnings (non-blocking)

---

## Function: `mark_step_complete(step_name, status)`

### Contract

```bash
mark_step_complete(step_name: string, status: string) -> void
```

### Behavior

1. **Get**: Current timestamp
2. **Create**: History entry
3. **Append**: To `orchestration_history` in config
4. **Update**: Config file

### Example

```bash
mark_step_complete "specify_init" "success"
# Adds:
# {
#   "step": "specify_init",
#   "status": "success",
#   "timestamp": "2026-05-03T15:30:00Z"
# }
```

---

## Function: `mark_step_failed(step_name, error_message)`

### Contract

```bash
mark_step_failed(step_name: string, error: string) -> void
```

### Behavior

1. **Get**: Current timestamp
2. **Create**: History entry with error
3. **Append**: To `orchestration_history`
4. **Update**: Config file
5. **Set**: `spek_initialized = false`

---

## Function: `get_recovery_guidance(failed_step)`

### Contract

```bash
get_recovery_guidance(failed_step: string) -> array<string>
```

### Output

```bash
[
  "Error: specify not found",
  "Install: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git",
  "Verify: specify --version",
  "Then retry: spek init"
]
```

### Behavior

1. **Identify**: Failed step and error type
2. **Map**: To recovery steps
3. **Return**: Array of guidance strings
4. **Display**: As user-friendly instructions

### Recovery Mappings

| Failed Step | Error | Recovery |
|------------|-------|----------|
| `prerequisites_check` | Python not found | Install Python 3.11+ |
| `prerequisites_check` | uv not found | Install uv |
| `specify_init` | specify not found | Install speckit |
| `graphify_init` | graphify not found | Install graphify |
| `obsidian_setup` | Obsidian not installed | Skip (non-fatal) or install Obsidian app |
| `skill_install` | Permission denied | Check `.spekificity/` permissions |
| `config_update` | JSON parse error | Repair or delete config.json |

---

## Idempotent Execution Model

### Re-run Scenarios

#### Scenario 1: Fresh Run

```
No .spekificity/config.json exists

1. initialize_config()
   → Create config (spek_initialized = false)

2. Run orchestration phases (specify, graphify, obsidian, caveman)
   → Each phase checks: already done?
   → If not: execute, mark as success

3. Mark: spek_initialized = true

Result: Full setup completed
```

#### Scenario 2: Idempotent Re-run

```
Config exists, spek_initialized = true

1. Check: is_already_initialized()
   → true (config exists, initialized = true)

2. For each orchestration phase:
   → Check: is tool already initialized?
   → If yes: skip (not re-running)
   → If no: execute

3. Update: timestamps only (versions unchanged)

Result: State preserved, re-run is clean (no errors, fast)
```

#### Scenario 3: Partial Failure Recovery

```
Config exists, spek_initialized = false

1. Check: detect_partial_failure()
   → Returns: last_failed_step = "specify_init"

2. Display: recovery guidance
   → "Install specify, then retry"

3. On retry (spek init again):
   → Check: prerequisite fixed?
   → If yes: resume from failed step
   → If no: display error again

4. After recovery step succeeds:
   → Continue to next phase
   → Eventually: spek_initialized = true
```

---

## State Transitions

### State Diagram

```
┌─────────────────────────────┐
│ NO CONFIG                   │
│ (fresh start)               │
└────────────────┬────────────┘
                 │ spek init
                 ▼
┌──────────────────────────────────┐
│ CONFIG EXISTS                    │
│ spek_initialized = false         │
│ (in progress, or failed before)  │
└────────────────┬─────────────────┘
                 │ continues
                 │ (all phases pass)
                 ▼
┌──────────────────────────────────┐
│ CONFIG EXISTS                    │
│ spek_initialized = true          │
│ (fully initialized)              │
└────────────────┬─────────────────┘
                 │ spek init again
                 │ (idempotent re-run)
                 ▼
┌──────────────────────────────────┐
│ CONFIG PRESERVED                 │
│ spek_initialized = true          │
│ (no changes, fast)               │
└──────────────────────────────────┘
```

---

## Config State Schema

```json
{
  "spek_version": "1.0.0",
  "spek_initialized": boolean,
  "spek_initialized_timestamp": "ISO 8601 timestamp",
  "orchestration_history": [
    {
      "step": "string",
      "status": "success|failure|skipped|partial",
      "timestamp": "ISO 8601",
      "error": "string (optional)",
      "version": "string (optional)",
      "duration_ms": number
    }
  ],
  "tools": {
    "[tool_name]": {
      "installed": boolean,
      "initialized": boolean,
      "version": "string (optional)",
      "initialized_timestamp": "ISO 8601 (optional)"
    }
  }
}
```

---

## Recovery Workflow

### User Encounters Partial Failure

```
Command: spek init
Error: specify: command not found

System Response:
1. Detect: failed step = "specify_init"
2. Mark: history entry with failure
3. Set: spek_initialized = false
4. Print: recovery guidance
   "Install: uv tool install specify-cli --from git+..."
5. Exit: code 1
```

### User Follows Recovery Steps

```
User runs: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### User Retries

```
Command: spek init (again)
System Response:
1. Check: is_already_initialized()
   → false (spek_initialized = false)
2. Check: detect_partial_failure()
   → yes, failed at "specify_init"
3. Check: is prerequisite fixed?
   → Check: specify installed?
   → Yes! Continue
4. Resume: from "specify_init" phase
5. Execute: specify init (succeeds this time)
6. Continue: remaining phases
7. Mark: spek_initialized = true
8. Exit: code 0 (success)
```

---

## Testing Criteria

- ✅ Fresh install: Config created, all phases executed
- ✅ Idempotent re-run: No errors, fast execution
- ✅ Partial failure detected: Correct failed step identified
- ✅ Recovery guidance provided: Clear, actionable instructions
- ✅ Recovery retry succeeds: Resumes from failure point
- ✅ History accurate: All entries timestamped, statused
- ✅ State preserved: Config unchanged after idempotent re-run
- ✅ Failure graceful: Clear error messages, exit code 1

---

## Dependencies

- `config-handler.sh`: Read/write config, JSON manipulation
- `logging.sh`: Log state changes and errors
- `prerequisites.sh`: Verify environment prerequisites

---

**Status**: Ready for implementation  
**Last Updated**: 2026-05-03
