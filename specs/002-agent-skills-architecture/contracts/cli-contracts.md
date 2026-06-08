# CLI Command Contracts

**Purpose**: Define the interface contract for `spek` CLI commands. Only `spek init` is active; all others redirect or error with helpful messages.

---

## Active Commands

### Command: `spek init`

**Purpose**: Initialize Spekificity project structure

**Signature**:
```bash
spek init [--verbose] [--color/--no-color] [--debug]
```

**Arguments**: None (no positional arguments)

**Options**:
- `--verbose, -v` (bool, optional) — Enable verbose logging output
- `--color/--no-color` (bool, default=true) — Enable/disable colored terminal output
- `--debug` (bool, optional) — Enable debug logging (very verbose)

**Output**:
```
✓ Spekificity initialized in /path/to/project
  Created:
    - vault/              (decisions, patterns, lessons storage)
    - .spek/              (project configuration)
    - specs/              (feature specifications)
    - .specify/           (internal SpecKit working directory)
  Next: spek prepare [FEATURE]
```

**Exit Codes**:
- `0` — Success
- `1` — Init failed (directory already initialized, permission error, etc.)
- `2` — Command-line argument error

**Error Handling**:
```bash
spek init  # If vault/ already exists
❌ Error: Spekificity already initialized in this directory.
   Use: spek prepare [FEATURE] to get started with a new feature.
```

---

## Deprecated/Redirected Commands

The following commands **existed** in prior implementation but are now deprecated. Users invoking them receive a helpful redirect message.

### Command: `spek prepare` (DEPRECATED)

**Old Signature**:
```bash
spek prepare [FEATURE] [--no-index] [--compressed]
```

**New Behavior**: Redirect to agent skill

**Output**:
```
Error: 'spek prepare' is a CLI stub. To use this workflow, invoke the agent skill:

  /spek.prepare [feature-name]

For documentation: wiki/skills.md#spek.prepare
Documentation: https://github.com/user/spekificity/wiki/skills.md#spek.prepare
```

**Implementation Note**: Keep fallback implementation for quick vault/code-index load if absolutely needed, but print deprecation warning.

---

### Command: `spek plan` (DEPRECATED)

**Old Signature**:
```bash
spek plan [FEATURE] [--skip-prepare] [--no-clarify]
```

**New Behavior**: Redirect to agent skill

**Output**:
```
Error: 'spek plan' requires Claude Code agent context. Use the agent skill:

  /spek.plan [feature-name]

This interactive workflow generates spec → clarification → plan → tasks with your input.
Documentation: wiki/skills.md#spek.plan
```

**Exit Code**: `1` (error)

---

### Command: `spek implement` (DEPRECATED)

**Old Signature**:
```bash
spek implement [TASK] [--task ID] [--resume] [--list] [--mark-complete] [--skip-context]
```

**New Behavior**: Redirect to agent skill

**Output**:
```
Error: 'spek implement' requires Claude Code agent context. Use the agent skill:

  /spek.implement [feature-name|spec-file] [--steps N]

This interactive workflow executes tasks with context injection and progress tracking.
Documentation: wiki/skills.md#spek.implement
```

**Exit Code**: `1` (error)

---

### Command: `spek conclude` (DEPRECATED)

**Old Signature**:
```bash
spek conclude [FEATURE] [--feature NAME] [--all] [--export-vault] [--dry-run]
```

**New Behavior**: Redirect to agent skill

**Output**:
```
Error: 'spek conclude' requires Claude Code agent context. Use the agent skill:

  /spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]

This interactive workflow analyzes outcomes, extracts lessons, and updates the vault.
Documentation: wiki/skills.md#spek.conclude
```

**Exit Code**: `1` (error)

---

## Help Output

### Global Help

```bash
$ spek --help

Spekificity: Spec-driven agent development framework.

Transform feature intent into executable specifications and persistent knowledge.

Usage:
  spek --help              Show this help message
  spek --version           Show version
  spek <command> --help    Show command help
  spek init                Initialize project (CLI)

For agent skills (interactive workflows), use Claude Code:
  /spek.prepare            Load prior context, onboard to feature
  /spek.plan               Generate spec, plan, and tasks
  /spek.implement          Execute task with context injection
  /spek.conclude           Analyze outcomes, update vault

Documentation: wiki/skills.md

Commands:
  init                     Initialize Spekificity in current project
```

### Command-Specific Help

```bash
$ spek init --help

Usage: spek init [OPTIONS]

  Initialize Spekificity in current project.
  
  Creates vault/, .spek/, specs/ directories and initializes per-project
  configuration.

Options:
  -v, --verbose    Enable verbose output
  --color          Enable colored output (default: true)
  --no-color       Disable colored output
  --debug          Enable debug logging
  -h, --help       Show this message and exit
```

---

## Backward Compatibility

**Breaking Changes**:
- `spek prepare`, `spek plan`, `spek implement`, `spek conclude` no longer work as CLI commands
- Users must invoke agent skills (`/spek.prepare`, etc.) instead

**Migration Path**:
1. User runs deprecated command (e.g., `spek plan`)
2. Receives error message with agent skill syntax
3. User runs agent skill (e.g., `/spek.plan`)
4. Workflow executes as designed

**Deprecation Timeline**:
- Phase 1 (this feature): Error messages + redirect instructions
- Phase 2 (future): Consider removing deprecated commands entirely

---

## Testing Scenarios

### Scenario 1: Init Success
```bash
$ spek init
✓ Spekificity initialized in /Users/example/project
```

### Scenario 2: Init Already Initialized
```bash
$ spek init
❌ Error: Spekificity already initialized in this directory.
   Use: spek prepare [FEATURE] to get started with a new feature.
```

### Scenario 3: Deprecated Command Invocation
```bash
$ spek plan "Add authentication"
Error: 'spek plan' requires Claude Code agent context. Use the agent skill:
  /spek.plan "Add authentication"
```

### Scenario 4: Help Shows Both CLI and Agent Skills
```bash
$ spek --help
[Shows init as CLI command]
[Shows prepare, plan, implement, conclude as agent skills with /spek.* syntax]
```
