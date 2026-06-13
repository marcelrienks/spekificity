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
    ("python", "Python 3.10+", "https://www.python.org/downloads/", 3, 10),
    ("uv", "uv 0.1+", "curl -LsSf https://astral.sh/uv/install.sh | sh", 0, 1),
    ("node", "Node.js 18+", "https://nodejs.org/en/download/", 18, 0),
    ("git", "git 2.0+", "https://git-scm.com/downloads", 2, 0),
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
        # For Python, accept both python and python3 (prefer python3)
        check_cmd = cmd
        if cmd == "python":
            check_cmd = "python3" if shutil.which("python3") else "python"

        present = shutil.which(check_cmd) is not None
        version = _get_version(check_cmd) if present else None
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

    # All tools present — verify/initialize git repository if needed
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            # Not a git repo — initialize it
            subprocess.run(["git", "init"], check=True, capture_output=True)
            print_status("OK", "Initialized git repository")
    except FileNotFoundError:
        pass  # git PATH absence already caught above

    return results
