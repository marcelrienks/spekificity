"""Detect and install specify-cli via uv."""

from __future__ import annotations

import shutil
from dataclasses import dataclass

from spekificity.utils import run_command, print_status


@dataclass
class ToolInstallResult:
    tool: str
    status: str  # "installed" | "already_present" | "skipped" | "needs_user_action"
    message: str
    exit_code: int = 0


def install_speckit() -> ToolInstallResult:
    """Install specify-cli via uv tool install if not already in PATH."""
    if shutil.which("specify"):
        print_status("SKIP", "specify-cli already installed")
        return ToolInstallResult(tool="speckit", status="already_present", message="specify already in PATH")
    run_command(
        ["uv", "tool", "install", "specify-cli", "--from", "git+https://github.com/github/spec-kit.git"],
        "install specify-cli via uv",
    )
    print_status("OK", "specify-cli installed")
    return ToolInstallResult(tool="speckit", status="installed", message="specify-cli installed via uv")
