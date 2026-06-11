"""Detect and install lat.md via npm."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field

from spekificity.utils import run_command, print_status


@dataclass
class ToolInstallResult:
    tool: str
    status: str  # "installed" | "already_present" | "skipped" | "needs_user_action"
    message: str
    exit_code: int = 0


def install_lat() -> ToolInstallResult:
    """Install lat.md via npm if not already in PATH."""
    if shutil.which("lat"):
        print_status("SKIP", "lat already installed")
        return ToolInstallResult(tool="lat_md", status="already_present", message="lat already in PATH")
    run_command(["npm", "install", "-g", "lat.md"], "install lat.md")
    print_status("OK", "lat.md installed")
    return ToolInstallResult(tool="lat_md", status="installed", message="lat.md installed via npm")
