"""Prerequisite checker for spek init."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class PrerequisiteResult:
    name: str
    present: bool
    version: str | None
    install_hint: str


_PREREQS: list[tuple[str, str, str, int | None, int | None]] = [
    ("python", "Python 3.11+", "https://www.python.org/downloads/", 3, 11),
    ("uv", "uv", "curl -LsSf https://astral.sh/uv/install.sh | sh", None, None),
    ("node", "Node.js 22+", "https://nodejs.org/en/download/", 22, 0),
    ("git", "git", "https://git-scm.com/downloads", None, None),
]


def _get_version(cmd: str) -> str | None:
    try:
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip().split("\n")[0] if result.returncode == 0 else None
    except Exception:
        return None


def _version_ok(raw: str | None, min_major: int, min_minor: int) -> bool:
    m = re.search(r"(\d+)\.(\d+)", raw or "")
    if not m:
        return False
    return (int(m.group(1)), int(m.group(2))) >= (min_major, min_minor)


def check_prerequisites() -> list[PrerequisiteResult]:
    """Check all prerequisites. Halts (sys.exit(1)) on first missing or out-of-date tool."""
    results: list[PrerequisiteResult] = []
    for cmd, name, install_hint, min_major, min_minor in _PREREQS:
        present = shutil.which(cmd) is not None
        version = _get_version(cmd) if present else None
        result = PrerequisiteResult(
            name=name,
            present=present,
            version=version,
            install_hint=install_hint,
        )
        results.append(result)
        if not present:
            print(f"[ERROR] Missing prerequisite: {name}")
            print(f"  Install: {install_hint}")
            sys.exit(1)
        if min_major is not None and not _version_ok(version, min_major, min_minor):
            print(f"[ERROR] {name} version too low (need ≥{min_major}.{min_minor}): {version}")
            print(f"  Upgrade: {install_hint}")
            sys.exit(1)

    # All tools present — verify CWD is a valid git repository
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print("[ERROR] Not in a git repository. Run: git init")
            sys.exit(1)
    except FileNotFoundError:
        pass  # git PATH absence already caught above

    return results
