"""Detect and install Obsidian per platform."""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass

from spekificity.utils import run_command, print_status


@dataclass
class ToolInstallResult:
    tool: str
    status: str  # "installed" | "already_present" | "skipped" | "needs_user_action"
    message: str
    exit_code: int = 0


def install_obsidian() -> ToolInstallResult:
    """Detect and install Obsidian. Returns needs_user_action if obsidian CLI not in PATH after install."""
    if shutil.which("obsidian"):
        print_status("SKIP", "obsidian already in PATH")
        return ToolInstallResult(tool="obsidian", status="already_present", message="obsidian already in PATH")

    platform = sys.platform
    if platform == "darwin":
        run_command(["brew", "install", "--cask", "obsidian"], "install Obsidian via brew")
        print_status("OK", "Obsidian installed via brew")
    elif platform == "win32":
        run_command(["winget", "install", "-e", "--id", "Obsidian.Obsidian"], "install Obsidian via winget")
        print_status("OK", "Obsidian installed via winget")
    else:
        print_status("WARN", "Linux detected — cannot auto-install Obsidian")
        print("Download Obsidian from: https://obsidian.md/download")
        return ToolInstallResult(tool="obsidian", status="skipped", message="Linux: manual install required")

    # Phase 2 check: was obsidian CLI registered?
    if not shutil.which("obsidian"):
        _print_registration_instructions()
        return ToolInstallResult(
            tool="obsidian",
            status="needs_user_action",
            message="Obsidian installed but CLI not in PATH — register via Obsidian Settings → General → Enable CLI",
            exit_code=2,
        )

    return ToolInstallResult(tool="obsidian", status="installed", message="Obsidian installed and CLI available")


def _print_registration_instructions() -> None:
    import sys as _sys
    print(file=_sys.stderr)
    print("Obsidian CLI registration required:", file=_sys.stderr)
    print("  1. Open Obsidian", file=_sys.stderr)
    print("  2. Go to Settings → General", file=_sys.stderr)
    print("  3. Enable 'Obsidian CLI'", file=_sys.stderr)
    print("  4. Re-run: spek init", file=_sys.stderr)
    print(file=_sys.stderr)
