"""Install the caveman skill and (for Claude Code) project-level activation hooks."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from spekificity.skills_install.integrations import get_skills_config
from spekificity.utils import print_status


@dataclass
class CavemanInstallResult:
    tool: str = "caveman"
    status: str = "installed"
    skill_status: str = "n/a"
    hook_status: str = "n/a"
    message: str = ""
    exit_code: int = 0


_GITHUB_RAW_SKILL = (
    "https://raw.githubusercontent.com/JuliusBrussee/caveman/main"
    "/plugins/caveman/skills/caveman/SKILL.md"
)
_SESSION_START_MARKER = "caveman-activate"
_USER_PROMPT_MARKER = "caveman-mode-tracker"


def _strip_jsonc(src: str) -> str:
    """Remove // and /* */ comments (string-aware) and trailing commas from JSON."""
    out: list[str] = []
    i = 0
    n = len(src)
    in_string = False
    in_line = False
    in_block = False
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if in_line:
            if c == "\n":
                in_line = False
                out.append(c)
            i += 1
            continue
        if in_block:
            if c == "*" and nxt == "/":
                in_block = False
                i += 2
            else:
                i += 1
            continue
        if in_string:
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == "/" and nxt == "/":
            in_line = True
            i += 2
            continue
        if c == "/" and nxt == "*":
            in_block = True
            i += 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def _fetch_skill_content() -> Optional[bytes]:
    """Resolve SKILL.md: global skills → plugin cache → GitHub raw."""
    global_skill = Path.home() / ".claude" / "skills" / "caveman" / "SKILL.md"
    if global_skill.exists():
        try:
            return global_skill.read_bytes()
        except OSError:
            pass

    cache_root = Path.home() / ".claude" / "plugins" / "cache" / "caveman" / "caveman"
    if cache_root.is_dir():
        try:
            shas = sorted(
                [d for d in cache_root.iterdir() if d.is_dir()],
                key=lambda d: d.stat().st_mtime,
                reverse=True,
            )
            for sha_dir in shas:
                candidate = sha_dir / "plugins" / "caveman" / "skills" / "caveman" / "SKILL.md"
                if candidate.exists():
                    return candidate.read_bytes()
        except OSError:
            pass

    try:
        with urllib.request.urlopen(_GITHUB_RAW_SKILL, timeout=10) as resp:
            return resp.read()
    except (urllib.error.URLError, OSError):
        pass

    print_status("WARN", "caveman: SKILL.md not found — skill file skipped. Run /caveman manually in your agent.")
    return None


def _copy_skill(project_path: Path, integration: str, content: Optional[bytes]) -> str:
    """Write SKILL.md to integration skills dir. Returns 'installed', 'skipped', or 'failed'."""
    if content is None:
        return "failed"

    skills_dir_str, use_subfolder = get_skills_config(integration)
    skills_dir = project_path / skills_dir_str

    dest = (skills_dir / "caveman" / "SKILL.md") if use_subfolder else (skills_dir / "caveman.md")

    if dest.exists():
        print_status("SKIP", f"caveman skill already present at {dest.relative_to(project_path)}")
        return "skipped"

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    print_status("OK", f"caveman skill installed → {dest.relative_to(project_path)}")
    return "installed"


def _ensure_global_hooks() -> bool:
    """Ensure ~/.claude/hooks/caveman-activate.js exists. Install via cache or npx if absent."""
    activate = Path.home() / ".claude" / "hooks" / "caveman-activate.js"
    if activate.exists():
        return True

    node = shutil.which("node")
    if not node:
        print_status("WARN", "caveman hooks: node not in PATH — cannot install global hooks")
        return False

    cache_root = Path.home() / ".claude" / "plugins" / "cache" / "caveman" / "caveman"
    if cache_root.is_dir():
        try:
            shas = sorted(
                [d for d in cache_root.iterdir() if d.is_dir()],
                key=lambda d: d.stat().st_mtime,
                reverse=True,
            )
            for sha_dir in shas:
                installer = sha_dir / "bin" / "install.js"
                if installer.exists():
                    proc = subprocess.run(
                        [node, str(installer), "--skip-skills", "--non-interactive"],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if proc.returncode == 0 and activate.exists():
                        return True
                    break
        except (OSError, subprocess.TimeoutExpired):
            pass

    npx = shutil.which("npx")
    if npx:
        try:
            proc = subprocess.run(
                [npx, "-y", "github:JuliusBrussee/caveman", "--skip-skills", "--non-interactive"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if proc.returncode == 0 and activate.exists():
                return True
        except (OSError, subprocess.TimeoutExpired):
            pass

    print_status("WARN", "caveman hooks: could not install global hooks — auto-activation skipped")
    return False


def _has_hook(settings: dict, event: str, marker: str) -> bool:
    entries = settings.get("hooks", {}).get(event, [])
    if not isinstance(entries, list):
        return False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        for hook in entry.get("hooks", []):
            if isinstance(hook, dict) and marker in hook.get("command", ""):
                return True
    return False


def _add_hook(settings: dict, event: str, command: str, status_msg: str) -> None:
    settings.setdefault("hooks", {}).setdefault(event, []).append({
        "hooks": [{"type": "command", "command": command, "timeout": 5, "statusMessage": status_msg}]
    })


def _write_project_hooks(project_path: Path) -> str:
    """Write SessionStart + UserPromptSubmit caveman hooks to project .claude/settings.json."""
    node = shutil.which("node")
    if not node:
        print_status("WARN", "caveman hooks: node not in PATH — skipping project hook write")
        return "failed"

    if not _ensure_global_hooks():
        return "failed"

    hooks_dir = Path.home() / ".claude" / "hooks"
    activate_cmd = f'"{node}" "{hooks_dir / "caveman-activate.js"}"'
    tracker_cmd = f'"{node}" "{hooks_dir / "caveman-mode-tracker.js"}"'

    settings_path = project_path / ".claude" / "settings.json"
    settings: dict = {}
    if settings_path.exists():
        try:
            raw = settings_path.read_text(encoding="utf-8")
            settings = json.loads(_strip_jsonc(raw)) if raw.strip() else {}
        except (json.JSONDecodeError, OSError):
            settings = {}

    if _has_hook(settings, "SessionStart", _SESSION_START_MARKER):
        print_status("SKIP", "caveman hooks already configured in .claude/settings.json")
        return "skipped"

    _add_hook(settings, "SessionStart", activate_cmd, "Loading caveman mode...")
    _add_hook(settings, "UserPromptSubmit", tracker_cmd, "Tracking caveman mode...")

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = settings_path.with_suffix(".json.tmp")
    try:
        tmp.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, settings_path)
    except OSError as exc:
        print_status("WARN", f"caveman hooks: could not write .claude/settings.json — {exc}")
        return "failed"

    print_status("OK", "caveman hooks written → .claude/settings.json")
    return "installed"


def install_caveman(project_path: Path, integration: str) -> CavemanInstallResult:
    """Install caveman skill file and (for claude integration) project-level activation hooks."""
    result = CavemanInstallResult()

    content = _fetch_skill_content()
    result.skill_status = _copy_skill(project_path, integration, content)

    if integration == "claude":
        result.hook_status = _write_project_hooks(project_path)
    else:
        result.hook_status = "n/a"

    if result.skill_status == "installed" or result.hook_status == "installed":
        result.status = "installed"
    elif "failed" in (result.skill_status, result.hook_status):
        result.status = "failed"
    else:
        result.status = "skipped"

    result.message = f"skill={result.skill_status} hooks={result.hook_status}"
    return result
