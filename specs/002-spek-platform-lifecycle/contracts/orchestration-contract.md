# Contract: Orchestration Interface

**Version**: 1.0.0  
**Namespace**: spekificity-orchestration  
**Status**: Active

## Purpose

Define the contract for orchestrating tool initialization (speckit, graphify, obsidian, caveman) in spekificity.

---

## Function: `orchestrate_specify_init()`

### Contract

```bash
orchestrate_specify_init() -> (exit_code: int, state_update: object)
```

### Input

None (operates on global environment)

### Output

```json
{
  "exit_code": 0,
  "state_update": {
    "tool": "speckit",
    "status": "success",
    "version": "0.1.0",
    "initialized_timestamp": "2026-05-03T15:30:00Z"
  }
}
```

### Behavior

1. **Check**: Is `specify` installed globally?
   - If no: Install via `uv tool install specify-cli --from git+...`
   - If yes: Continue

2. **Execute**: Run `specify init .`
   - Creates `.specify/` configuration
   - Installs `.github/agents/speckit.*.md` skills

3. **Update Config**: Record state in `.spekificity/config.json`
   ```json
   {
     "tools.speckit.installed": true,
     "tools.speckit.version": "<version>",
     "tools.speckit.initialized": true,
     "tools.speckit.initialized_timestamp": "<now>"
   }
   ```

4. **Record History**: Append to `orchestration_history`
   ```json
   {
     "step": "specify_init",
     "status": "success",
     "timestamp": "<now>",
     "version": "0.1.0"
   }
   ```

### Exit Codes

- **0**: Success (specify initialized)
- **1**: Failure (specify not installed or init failed)

### Error Handling

| Error | Recovery |
|-------|----------|
| `specify: command not found` | Install: `uv tool install specify-cli --from git+...` |
| `.specify/` already exists | Skip (idempotent, continue) |
| Permission denied | Suggest: `chmod +x .specify/` |

### Idempotency

- **First run**: Full initialization
- **Re-run**: Detect existing `.specify/` → skip init → return success

---

## Function: `orchestrate_graphify()`

### Contract

```bash
orchestrate_graphify() -> (exit_code: int, state_update: object)
```

### Output

```json
{
  "exit_code": 0,
  "state_update": {
    "tool": "graphify",
    "status": "success",
    "version": "1.0.0",
    "initialized_timestamp": "2026-05-03T15:31:00Z"
  }
}
```

### Behavior

1. **Check**: Is `graphify` installed?
   - If no: Install via `uv tool install graphifyy`
   - If yes: Continue

2. **Execute**: Run `graphify init` and `graphify analyze`
   - Generates project dependency graph
   - Stores in `.obsidian/graph/index.md`

3. **Update Config**:
   ```json
   {
     "tools.graphify.installed": true,
     "tools.graphify.initialized": true,
     "tools.graphify.initialized_timestamp": "<now>"
   }
   ```

4. **Record History**: Similar to specify_init

### Exit Codes

- **0**: Success
- **1**: Failure

### Error Handling

| Error | Recovery |
|-------|----------|
| `graphify: command not found` | Install: `uv tool install graphifyy` |
| Graph generation timeout | Suggest: Re-run or use `--depth shallow` |

### Idempotency

- **Re-run**: Detect existing `.obsidian/graph/` → update incrementally

---

## Function: `orchestrate_obsidian()`

### Contract

```bash
orchestrate_obsidian() -> (exit_code: int, state_update: object)
```

### Output

```json
{
  "exit_code": 0,
  "state_update": {
    "tool": "obsidian",
    "status": "optional",
    "available": true,
    "initialized_timestamp": "2026-05-03T15:32:00Z"
  }
}
```

### Behavior

1. **Check**: Is Obsidian app installed?
   - If yes: Continue with vault setup
   - If no: Mark as unavailable, continue (non-fatal)

2. **Setup Vault**: If Obsidian available
   - Create `.obsidian/` vault directory structure
   - Create `vault-info.json` metadata
   - Configure vault in Obsidian preferences

3. **Update Config**:
   ```json
   {
     "tools.obsidian.available": true,
     "tools.obsidian.initialized": true,
     "tools.obsidian.vault_path": ".obsidian/"
   }
   ```

### Exit Codes

- **0**: Success (Obsidian available and setup)
- **0**: Success (Obsidian not available, but non-fatal)
- **1**: Failure (Obsidian setup error)

### Non-Fatal Behavior

If Obsidian not available or setup fails:
- Continue orchestration (non-blocking)
- Use fallback JSON storage (`.spekificity/graph.json`)
- Mark in config: `tools.obsidian.available = false`

---

## Function: `orchestrate_caveman()`

### Contract

```bash
orchestrate_caveman() -> (exit_code: int, state_update: object)
```

### Output

```json
{
  "exit_code": 0,
  "state_update": {
    "tool": "caveman",
    "status": "optional",
    "available": false,
    "integrated": false
  }
}
```

### Behavior

1. **Check**: Is caveman skill available in environment?
   - If yes: Mark available, integrate
   - If no: Mark unavailable, continue

2. **Update Config**:
   ```json
   {
     "tools.caveman.available": false,
     "tools.caveman.integrated": false
   }
   ```

3. **Record History**: Note caveman status

### Non-Fatal Behavior

- Caveman not available → Continue (non-blocking)
- Project functional without caveman mode
- User can use caveman commands manually if installed later

---

## Global Orchestration Flow

```
┌──────────────────────────────────┐
│ spek init (entry point)          │
└─────────┬────────────────────────┘
          │
          ├─→ validate_prerequisites()
          │   └─→ Check Python, uv, git
          │
          ├─→ orchestrate_specify_init()
          │   └─→ Create .specify/
          │   └─→ Install speckit skills
          │
          ├─→ orchestrate_graphify()
          │   └─→ Create graph
          │
          ├─→ orchestrate_obsidian()
          │   └─→ Create vault (optional)
          │
          ├─→ orchestrate_caveman()
          │   └─→ Check availability (optional)
          │
          ├─→ install_spek_skills()
          │   └─→ Populate .spekificity/skills/
          │
          ├─→ install_workflows()
          │   └─→ Populate .spekificity/workflows/
          │
          ├─→ install_guides()
          │   └─→ Populate .spekificity/guides/
          │
          └─→ update_skill_index()
              └─→ Generate .spekificity/skill-index.md
```

---

## State Contract

After successful orchestration, config must contain:

```json
{
  "spek_initialized": true,
  "spek_initialized_timestamp": "2026-05-03T15:35:00Z",
  "tools": {
    "speckit": {
      "installed": true,
      "initialized": true
    },
    "graphify": {
      "installed": true,
      "initialized": true
    },
    "obsidian": {
      "available": true/false,
      "initialized": true/false
    },
    "caveman": {
      "available": true/false,
      "integrated": true/false
    }
  },
  "skills": {
    "spekificity_installed": true,
    "speckit_installed": true
  },
  "orchestration_history": [
    { "step": "specify_init", "status": "success", "timestamp": "..." },
    { "step": "graphify_init", "status": "success", "timestamp": "..." },
    ...
  ]
}
```

---

## Testing Criteria

- ✅ Each orchestration function returns correct exit code
- ✅ Config state updated after each phase
- ✅ Idempotent: Re-run produces same result
- ✅ Non-fatal tools don't block orchestration
- ✅ History entries created for each step
- ✅ Error messages clear and actionable
- ✅ Recovery guidance provided for failures

---

## Dependencies

- `config-handler.sh`: Update config, read config
- `logging.sh`: Log steps and errors
- `idempotency.sh`: Detect partial failures
- `prerequisites.sh`: Validate prerequisites

---

**Status**: Ready for implementation  
**Last Updated**: 2026-05-03
