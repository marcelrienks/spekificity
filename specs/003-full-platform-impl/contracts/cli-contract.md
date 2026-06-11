# CLI Contract: `spek` Command

**Feature**: Full Platform Implementation
**Date**: 2026-06-11

## Command Structure

```
spek [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Flag | Description |
|------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help and exit |

### Commands

#### `spek init [PATH]`

Initialize Spekificity in a project directory.

```
spek init [OPTIONS] [PATH]
```

**Arguments**:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `PATH` | directory path | `.` (current directory) | Target project directory |

**Options**:

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--integration` | string | (prompted) | Agent integration type |
| `--script` | `sh` \| `ps` | (prompted) | Script type for hooks |
| `--no-git-hooks` | flag | `False` | Skip git hook installation |

**Exit Codes**:

| Code | Meaning |
|------|---------|
| `0` | Success — init complete |
| `1` | Error — missing prerequisite, tool install failure, or unexpected error |
| `2` | Partial init — user action required (Obsidian CLI registration) |

**Output format** (stdout):

Each step prints a status line:
```
[OK] <what was done>
[SKIP] <what was skipped and why>
[WARN] <non-fatal warning>
[ERROR] <what failed>
```

On Obsidian Phase 1 halt (exit code 2), stderr contains the full CLI registration instructions block from `wiki/setup.md`.

## Accepted Integration Values

Any value accepted by `specify integration list`. Common values:

```
claude, copilot, gemini, cursor-agent, windsurf, cline, codex,
kiro-cli, amp, qwen, generic
```

Plus any other valid `specify` integration value. Unknown values are accepted and fall back to `.agents/skills/` with subfolder format; no MCP config is written.

## Idempotency Contract

Running `spek init` twice on the same project MUST:
- Exit with code `0`
- Print `[SKIP]` for every step that was already complete
- Not overwrite any existing skill files, config files, or git hooks
- Not re-run `specify init` if `.specify/` already exists

## Opt-Out Contract

- `--no-git-hooks` flag: skip git hook installation entirely
- `.spek/.disable-git-hooks` file: skip git hook installation (same effect as flag)
- If git hook is already present: skip without error (idempotent)
