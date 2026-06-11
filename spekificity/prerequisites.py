"""Prerequisite checker for spek init."""

from __future__ import annotations

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


_PREREQS: list[tuple[str, str, str]] = [
    (
        "python",
        "Python 3.11+",
        "https://www.python.org/downloads/",
    ),
    (
        "uv",
        "uv",
        "curl -LsSf https://astral.sh/uv/install.sh | sh",
    ),
    (
        "node",
        "Node.js 22+",
        "https://nodejs.org/en/download/",
    ),
    (
        "git",
        "git",
        "https://git-scm.com/downloads",
    ),
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


def check_prerequisites() -> list[PrerequisiteResult]:
    """Check all prerequisites. Halts (sys.exit(1)) on first missing tool."""
    results: list[PrerequisiteResult] = []
    for cmd, name, install_hint in _PREREQS:
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
    return results
