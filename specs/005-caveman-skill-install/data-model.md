# Data Model: Caveman Skill Install

## Entities

### CavemanInstallResult

Result returned by `install_caveman()`. Mirrors the `ToolInstallResult` dataclass pattern used across all existing install modules.

**Fields**:
| Field | Type | Values |
|-------|------|--------|
| `tool` | `str` | Always `"caveman"` |
| `status` | `str` | `"installed"` / `"skipped"` / `"failed"` |
| `skill_status` | `str` | `"installed"` / `"skipped"` / `"failed"` / `"n/a"` |
| `hook_status` | `str` | `"installed"` / `"skipped"` / `"failed"` / `"n/a"` (n/a for non-Claude) |
| `message` | `str` | Human-readable detail for `print_status` |
| `exit_code` | `int` | `0` always (failure is non-fatal) |

**Invariants**:
- `status = "installed"` when at least one of `skill_status` or `hook_status` is `"installed"`
- `status = "skipped"` when both are `"skipped"` or `"n/a"`
- `status = "failed"` when any component failed and none installed

---

### CavemanHookEntry (settings.json shape)

The JSON structure written to `.claude/settings.json` for each hook event.

```
{
  "hooks": {
    "<event>": [           ← "SessionStart" | "UserPromptSubmit"
      {
        "hooks": [
          {
            "type": "command",        ← always "command"
            "command": "<str>",       ← "<abs-node> \"<abs-hook-script>\""
            "timeout": 5,             ← seconds, always 5
            "statusMessage": "<str>"  ← human label shown in Claude Code UI
          }
        ]
      }
    ]
  }
}
```

**Idempotency key**: presence of substring `caveman-activate` in any `command` field under `SessionStart`; `caveman-mode-tracker` under `UserPromptSubmit`.

---

### SkillFileSource

Resolution chain for the SKILL.md file. Tried in order; first successful read wins.

| Priority | Source | Path |
|----------|--------|------|
| 1 | Global Claude skills | `~/.claude/skills/caveman/SKILL.md` |
| 2 | Plugin cache (latest SHA) | `~/.claude/plugins/cache/caveman/caveman/<sha>/plugins/caveman/skills/caveman/SKILL.md` |
| 3 | GitHub raw | `https://raw.githubusercontent.com/JuliusBrussee/caveman/main/plugins/caveman/skills/caveman/SKILL.md` |

---

### HookScriptSource

Resolution chain for the Node.js hook scripts (required before project settings.json can be written).

| Priority | Source | Check |
|----------|--------|-------|
| 1 | Global hooks dir | `~/.claude/hooks/caveman-activate.js` exists |
| 2 | Plugin cache installer | Run `node <cache>/bin/install.js --skip-skills` |
| 3 | GitHub npx | Run `npx -y "github:JuliusBrussee/caveman" --skip-skills` |

---

## State Transitions

```
spek init (claude integration)
  ├── ensure_hooks_installed()
  │     ├── already present → hook_prereq = OK
  │     ├── plugin cache → run installer → hook_prereq = OK
  │     └── npx fallback → run install → hook_prereq = OK or FAILED
  │
  ├── [hook_prereq = FAILED] → skip hook write, warn
  │
  ├── fetch_skill_file()
  │     ├── global skills → skill_content = <bytes>
  │     ├── plugin cache → skill_content = <bytes>
  │     ├── github raw → skill_content = <bytes>
  │     └── all fail → skill_content = None, warn
  │
  ├── copy_skill_to_integration_dir()
  │     ├── exists → skip
  │     ├── skill_content = None → skip with warn
  │     └── write → skill_status = "installed"
  │
  └── write_project_hooks()          [claude only]
        ├── settings.json has hook already → hook_status = "skipped"
        ├── node not in PATH → hook_status = "failed", warn
        └── write hooks → hook_status = "installed"
```
