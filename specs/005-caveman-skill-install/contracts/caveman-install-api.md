# Contract: caveman install API

## Module: `spekificity.caveman.install`

### Public Function

```python
def install_caveman(project_path: Path, integration: str) -> CavemanInstallResult
```

**Inputs**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `project_path` | `Path` | Absolute path to the project root (same as all other install modules) |
| `integration` | `str` | Integration name from `INTEGRATION_SKILLS_DIR` (e.g. `"claude"`, `"copilot"`) |

**Output**: `CavemanInstallResult` — never raises; all errors captured in `status`/`message` fields.

**Side effects**:
1. May create `<project_path>/<skills_dir>/caveman.md` or `<project_path>/<skills_dir>/caveman/SKILL.md`
2. For `claude` integration only: may create/update `<project_path>/.claude/settings.json`
3. May run a subprocess (`node` or `npx`) if global hook scripts are absent
4. Prints `[OK]`, `[SKIP]`, or `[WARN]` status lines via `print_status()`

**Idempotency**: Safe to call multiple times. Never overwrites existing skill files or existing hook entries.

---

## CLI contract: `spek init` output

The install step prints one of the following status lines:

```
[OK]   caveman skill installed → .claude/commands/caveman.md
[OK]   caveman hooks written → .claude/settings.json
[SKIP] caveman skill already present
[SKIP] caveman hooks already configured
[WARN] caveman skill fetch failed — manual install: /caveman in Claude Code
[WARN] caveman hook write failed — <reason>
```

Exit code from `spek init` is unaffected by caveman install status (FR-009).

---

## Contract: settings.json hook entries

When written, the project `.claude/settings.json` gains exactly these two entries (merged into any existing content):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"<node-abs-path>\" \"<home>/.claude/hooks/caveman-activate.js\"",
            "timeout": 5,
            "statusMessage": "Loading caveman mode..."
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"<node-abs-path>\" \"<home>/.claude/hooks/caveman-mode-tracker.js\"",
            "timeout": 5,
            "statusMessage": "Tracking caveman mode..."
          }
        ]
      }
    ]
  }
}
```

Where:
- `<node-abs-path>` = result of `shutil.which("node")` at install time
- `<home>` = `Path.home()` (OS-appropriate home directory)

Existing `hooks` entries are preserved. The file is written atomically (write to temp, rename).
