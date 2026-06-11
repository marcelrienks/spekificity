"""Run lat.md code and doc indexes."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


def run_lat_index(project_path: Path) -> None:
    """Run lat init (code) and lat init --docs (doc index). Idempotent via .spek/lat/ check."""
    lat_dir = project_path / ".spek" / "lat"
    if lat_dir.exists():
        print_status("SKIP", "lat index already present at .spek/lat/")
        return
    run_command(["lat", "init"], "lat init (code index)")
    print_status("OK", "lat.md code index initialized")
    run_command(["lat", "init", "--docs"], "lat init --docs (doc index)")
    print_status("OK", "lat.md doc index initialized")
