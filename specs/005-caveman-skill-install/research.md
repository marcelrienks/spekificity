# Research: Caveman Skill Install

## Caveman Package Source

**Decision**: Use the installed Claude Code plugin cache as the primary source; fall back to GitHub raw download.

**Rationale**: The caveman plugin (`caveman@caveman`) is a Claude Code plugin installable from `github:JuliusBrussee/caveman`. Users who already have it installed have a local cache at `~/.claude/plugins/cache/caveman/caveman/<sha>/`. This avoids a network round-trip in the common case. If not cached, a single HTTP GET to `https://raw.githubusercontent.com/JuliusBrussee/caveman/main/skills/caveman/SKILL.md` fetches the skill file without requiring npm/npx at all.

**Alternatives considered**:
- Run `npx -y github:JuliusBrussee/caveman` from Python → adds 5-10s latency to `spek init`, requires npx, installs hooks globally as a side effect
- Bundle SKILL.md in the spekificity package → user chose option B (fetch), eliminates this

---

## Hook Installation for Claude Code

**Decision**: Write hooks to project `.claude/settings.json` referencing the globally installed hook scripts at `~/.claude/hooks/`. Use the absolute node path (from `shutil.which("node")`) because Claude Code GUI launchers don't inherit PATH.

**Hook command format** (mirrors caveman's own installer in `bin/install.js`):
```
"<abs-node-path>" "<abs-hooks-dir>/caveman-activate.js"
"<abs-node-path>" "<abs-hooks-dir>/caveman-mode-tracker.js"
```

**Where `abs-hooks-dir` = `~/.claude/hooks/` (expanduser)**

**Idempotency**: Before writing, check if any existing hook command contains the substring `caveman-activate` (SessionStart) or `caveman-mode-tracker` (UserPromptSubmit). If present, skip and report as skipped. This mirrors `hasCavemanHook()` from caveman's `settings.js`.

**settings.json hook shape**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"/path/to/node\" \"/home/user/.claude/hooks/caveman-activate.js\"",
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
            "command": "\"/path/to/node\" \"/home/user/.claude/hooks/caveman-mode-tracker.js\"",
            "timeout": 5,
            "statusMessage": "Tracking caveman mode..."
          }
        ]
      }
    ]
  }
}
```

**Rationale**: Project-level hooks scope caveman to the project directory. Using the global hook scripts (rather than copying them) ensures the user gets any updates from caveman upgrades without re-running `spek init`.

**Alternatives considered**:
- Copy hook scripts to project `.claude/hooks/` → self-contained but stale; user updates caveman, project hooks don't update
- Reference hooks via relative path → Claude Code GUI doesn't reliably resolve relative paths in hook commands

---

## Prerequisite: Global Caveman Hooks

**Decision**: Before installing skill file or writing project hooks, ensure `~/.claude/hooks/caveman-activate.js` exists. If not, run the caveman installer: `node <plugin-cache>/bin/install.js --skip-skills` if the plugin cache is available, otherwise `npx -y "github:JuliusBrussee/caveman" --skip-skills`.

**Rationale**: The project `.claude/settings.json` hooks reference global scripts. Those scripts must exist or the hook will fail silently on every session start.

---

## SKILL.md Resolution Order

1. `~/.claude/skills/caveman/SKILL.md` (globally installed, already extracted by Claude Code plugin system)
2. `~/.claude/plugins/cache/caveman/caveman/<latest-sha>/plugins/caveman/skills/caveman/SKILL.md` (plugin cache, scan for latest)
3. GitHub raw: `https://raw.githubusercontent.com/JuliusBrussee/caveman/main/plugins/caveman/skills/caveman/SKILL.md`

**Fallback behavior**: If all sources fail, log `[WARN]` and skip skill file install. Do not abort `spek init`.

---

## Skill File Format by Integration

All integrations use the same SKILL.md content. Placement follows existing `copy.py` pattern:

| Integration type | Destination |
|-----------------|-------------|
| Flat (`claude`, `copilot`, `generic`) | `<skills-dir>/caveman.md` |
| Subfolder (all others) | `<skills-dir>/caveman/SKILL.md` |

---

## JSONC Handling for settings.json

Claude Code's `settings.json` may contain JSONC (comments, trailing commas). Python's `json.loads()` will fail on these. Use a simple comment-strip regex before parsing, mirroring caveman's `stripJsonComments()`. Write output as clean JSON (no comments).
