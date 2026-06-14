"""Run lat.md code and doc indexes."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


def run_lat_index(project_path: Path) -> None:
    """Run lat init to initialize knowledge graph. Idempotent via .spek/lat/ check."""
    lat_dir = project_path / ".spek" / "lat"
    if lat_dir.exists():
        print_status("SKIP", "lat index already present")
        return

    run_command(["lat", "init", str(lat_dir)], "lat init", timeout=300)
    print_status("OK", "lat.md initialized")
