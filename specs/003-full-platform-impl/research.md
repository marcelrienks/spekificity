# Research: Full Platform Implementation

**Feature**: Full Platform Implementation
**Branch**: `003-full-platform-impl`
**Date**: 2026-06-11

## Decision 1: Package Data Access Pattern

**Decision**: Use `importlib.resources` (stdlib, Python 3.11+) to locate and copy bundled skill files from the installed package.

**Rationale**: `importlib.resources` is stdlib in Python 3.9+ and the canonical approach for accessing package data files. `importlib.resources.files()` returns a `Traversable` that works correctly both from source and from installed wheels. No extra dependency needed.

**Alternatives considered**:
- `pkg_resources` (setuptools): Deprecated path; heavier dependency; superseded by `importlib.resources`
- `__file__` relative paths: Fragile with zip-imported packages and editable installs
- `importlib_resources` backport: Not needed since Python 3.11+ is the minimum

**Implementation pattern**:
```python
import importlib.resources as pkg_resources
import shutil

skills_src = pkg_resources.files("spekificity") / "skills"
for skill_file in skills_src.iterdir():
    dest = resolve_dest(skill_file.name, integration)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with pkg_resources.as_file(skill_file) as src_path:
            shutil.copy2(src_path, dest)
```

---

## Decision 2: pyproject.toml Package Data Declaration

**Decision**: Use `[tool.hatch.build.targets.wheel] include` pattern to bundle `skills/*.md`.

**Rationale**: Project uses hatchling as build backend. Hatchling includes all files under `spekificity/` by default unless excluded. Since `skills/*.md` files are under the package directory, they will be included automatically. Explicit declaration via `[tool.hatch.build.targets.wheel]` is a safety net.

**Alternatives considered**:
- `[tool.setuptools.package-data]`: Project uses hatchling, not setuptools
- Manual `MANIFEST.in`: setuptools-specific; not applicable

**Implementation**: Verify `skills/` directory is under `spekificity/` package root — hatchling includes all non-Python files under the package directory by default. Add explicit `package-data` entry as belt-and-suspenders.

---

## Decision 3: Subprocess Pattern for External Tools

**Decision**: Use `subprocess.run()` with `check=True`, capture stdout/stderr, surface errors with descriptive messages.

**Rationale**: `subprocess.run` is the modern, recommended approach. `check=True` raises `CalledProcessError` on non-zero exit. Capturing output lets us surface meaningful error messages. Never use `shell=True` to avoid injection risk.

**Implementation pattern**:
```python
import subprocess

def run_command(cmd: list[str], description: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{description} failed: {e.stderr.strip()}") from e
    except FileNotFoundError:
        raise RuntimeError(f"{description}: command '{cmd[0]}' not found in PATH")
```

---

## Decision 4: Platform Detection for Obsidian Install

**Decision**: Use `sys.platform` for OS detection; `platform.system()` as fallback.

**Rationale**: `sys.platform` returns `'darwin'` (macOS), `'win32'` (Windows), `'linux'` (Linux). Simple, no extra dependencies.

**Per-platform install commands**:
- macOS (`sys.platform == 'darwin'`): `brew install --cask obsidian`
- Windows (`sys.platform == 'win32'`): `winget install -e --id Obsidian.Obsidian`
- Linux: Print download URL; cannot auto-install; continue without vault setup

---

## Decision 5: Idempotency Pattern

**Decision**: Check-before-act pattern: each init step checks if its output already exists and skips if so.

**Rationale**: `spek init` must be safe to re-run (Phase 1 halt → user registers CLI → re-run). Each step has a clear "already done" condition.

**Per-step idempotency checks**:

| Step | "Already done" condition |
|------|--------------------------|
| Prerequisites | `shutil.which('tool') is not None` |
| SpecKit install | `shutil.which('specify') is not None` |
| lat.md install | `shutil.which('lat') is not None` |
| Obsidian install | App present at known path OR `shutil.which('obsidian') is not None` |
| `.spek/` dirs | `path.exists()` |
| Skill files | `dest_file.exists()` — never overwrite |
| MCP config | `'lat' in existing_config['mcpServers']` |
| `specify init` | `.specify/` directory exists |
| Git hook | `Path('.git/hooks/post-commit').exists()` |

---

## Decision 6: MCP Config Merge Strategy

**Decision**: Read existing config as JSON, merge `lat` entry under the correct key, write back. Skip if `lat` already present.

**Rationale**: Merging prevents clobbering existing MCP server entries. Skipping on existing `lat` entry ensures idempotency.

**Implementation pattern**:
```python
import json

def write_mcp_config(config_path: Path, servers_key: str, entry_key: str = "lat") -> None:
    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text())
    servers = config.setdefault(servers_key, {})
    if entry_key in servers:
        return  # idempotent
    servers[entry_key] = {"command": "lat", "args": ["mcp"]}
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))
```

For copilot (VS Code), the entry also needs `"type": "stdio"`.

---

## Decision 7: Skill File Destination Format per Integration

**Decision**: Two destination formats based on integration:
- **Flat `.md`** (claude, copilot, generic): `<skills-dir>/spek-prepare.md`
- **Subfolder `SKILL.md`** (gemini, cursor-agent, windsurf, cline, codex, kiro-cli, amp, qwen, others): `<skills-dir>/spek-prepare/SKILL.md`

**Rationale**: Matches agent-specific conventions documented in `wiki/setup.md` and `wiki/conventions.md`.

---

## Decision 8: Exit Codes

**Decision**: Use standard POSIX exit codes:
- `0`: Success
- `1`: Error (missing prerequisite, tool install failure, unexpected error)
- `2`: Partial init — user action required (Obsidian CLI registration)

**Rationale**: Exit code 2 allows scripts/CI to distinguish "needs user action" from "error". Click uses `sys.exit()` via `click.get_current_context().exit()` or raising `click.ClickException`.

---

## Decision 9: Git Hook Content

**Decision**: Post-commit hook runs `lat update` (not `lat init`) for incremental refresh.

**Rationale**: `lat update` does incremental index refresh (faster); `lat init` does full rebuild. Post-commit only needs to update changed files. Per `wiki/setup.md`.

**Hook content**:
```bash
#!/bin/sh
lat update
```

---

## Decision 10: Integration Values → Skills Directory Mapping

**Decision**: Maintain a dict mapping integration values to `(skills_dir, use_subfolder)` tuples. Unknown values fall back to `.agents/skills/` with subfolder format.

**Known mappings** (from `wiki/setup.md`):

| Integration | Skills Dir | Format |
|-------------|-----------|--------|
| `claude` | `.claude/commands/` | flat `.md` |
| `copilot` | `.github/agents/skills/` | flat `.md` |
| `generic` | `.agents/skills/` | flat `.md` |
| `gemini` | `.gemini/skills/` | subfolder `SKILL.md` |
| `cursor-agent` | `.cursor/skills/` | subfolder `SKILL.md` |
| `windsurf` | `.windsurf/skills/` | subfolder `SKILL.md` |
| `cline` | `.cline/skills/` | subfolder `SKILL.md` |
| `codex` | `.codex/skills/` | subfolder `SKILL.md` |
| `kiro-cli` | `.kiro/skills/` | subfolder `SKILL.md` |
| `amp` | `.amp/skills/` | subfolder `SKILL.md` |
| `qwen` | `.qwen/skills/` | subfolder `SKILL.md` |
| *(unknown)* | `.agents/skills/` | subfolder `SKILL.md` |

**MCP config mapping** (from `wiki/setup.md`):

| Integration | Config File | Servers Key | Extra Fields |
|-------------|-------------|-------------|--------------|
| `claude` | `.mcp.json` | `mcpServers` | — |
| `cursor-agent` | `.cursor/mcp.json` | `mcpServers` | — |
| `copilot` | `.vscode/mcp.json` | `servers` | `"type": "stdio"` |
| `windsurf` | `.windsurf/mcp.json` | `mcpServers` | — |
| `cline` | `.vscode/settings.json` | `cline.mcpServers` | — |
| `gemini` | `.gemini/settings.json` | `mcpServers` | — |
| `codex` | `.codex/mcp.json` | `mcpServers` | — |
| `kiro-cli` | `.kiro/mcp.json` | `mcpServers` | — |
| `amp` | `.amp/mcp.json` | `mcpServers` | — |
| `qwen` | `.qwen/mcp.json` | `mcpServers` | — |
| `generic` + others | — (print instructions) | — | — |
