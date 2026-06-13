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
        try:
            run_command(
                ["brew", "install", "--cask", "--no-quarantine", "obsidian"],
                "install Obsidian via brew",
                timeout=300,
            )
            print_status("OK", "Obsidian installed via brew")
        except RuntimeError:
            print_status("SKIP", "Obsidian install skipped (brew unavailable or timed out)")
            return ToolInstallResult(tool="obsidian", status="skipped", message="Obsidian install failed")
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
    print(
        "\n"
        "⚠  Obsidian installed, but vault functionality is not yet active.\n"
        "\n"
        "One manual step required in Obsidian:\n"
        "  1. Open Obsidian\n"
        "  2. Go to Settings → General → Command line interface → Enable\n"
        "  3. Follow the prompt to register the CLI (creates the `obsidian` binary in PATH)\n"
        "     - macOS:   symlink at /usr/local/bin/obsidian\n"
        "     - Windows: Obsidian.com redirector added to PATH\n"
        "     - Linux:   binary copied to ~/.local/bin/obsidian\n"
        "  4. Restart your terminal\n"
        "\n"
        "Then re-run:  spek init\n"
        "\n"
        "spek init will complete all remaining setup autonomously.",
        file=_sys.stderr,
    )
