"""Run lat.md code and doc indexes."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


def run_lat_index(project_path: Path) -> None:
    """Run lat init to initialize knowledge graph. Idempotent via .spek/lat.md/ check."""
    spek_dir = project_path / ".spek"
    lat_md_dir = spek_dir / "lat.md"
    
    # Only run lat init if the knowledge base doesn't exist yet
    if not lat_md_dir.exists():
        spek_dir.mkdir(exist_ok=True)
        run_command(["lat", "init", str(spek_dir)], "lat init", timeout=300)
        print_status("OK", "lat.md initialized")
    else:
        print_status("SKIP", "lat index already present")
    
    # Always ensure symlink exists at project root so lat mcp can find it
    # (lat mcp looks for ./lat.md in the working directory)
    root_lat_md = project_path / "lat.md"
    if not root_lat_md.exists():
        root_lat_md.symlink_to(spek_dir / "lat.md")
