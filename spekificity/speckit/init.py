"""Run specify init to initialize SpecKit in the project."""

from __future__ import annotations

import os
from pathlib import Path

from spekificity.utils import run_command, print_status


def run_specify_init(project_path: Path, integration: str) -> None:
    """Run specify init if .specify/ dir does not exist (idempotent)."""
    specify_dir = project_path / ".specify"
    if specify_dir.exists():
        print_status("SKIP", ".specify/ already exists — skipping specify init")
        return

    # Change to project directory so --here works, then restore after
    old_cwd = os.getcwd()
    try:
        os.chdir(project_path)
        run_command(
            ["specify", "init", "--here", "--force", "--integration", integration],
            "specify init",
        )
    finally:
        os.chdir(old_cwd)

    print_status("OK", "SpecKit initialized (.specify/)")
