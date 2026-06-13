"""Run specify init to initialize SpecKit in the project."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


def run_specify_init(project_path: Path, integration: str) -> None:
    """Run specify init if .specify/ dir does not exist (idempotent)."""
    specify_dir = project_path / ".specify"
    if specify_dir.exists():
        print_status("SKIP", ".specify/ already exists — skipping specify init")
        return
    run_command(
        ["specify", "init", str(project_path), "--integration", integration],
        "specify init",
    )
    print_status("OK", "SpecKit initialized (.specify/)")
