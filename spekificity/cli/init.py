"""Per-project initialization (`spek init` command)."""

import os
import subprocess
from pathlib import Path
from typing import Optional

import click

from spekificity.cli.install import display_dependency_status
from spekificity.core.vault import create_vault_structure, load_vault


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
            timeout=5
        )
        return True
    except Exception:
        return False


def prompt_for_integration() -> str:
    """Prompt user for AI coding agent integration.

    Returns:
        Integration name (copilot, claude, gemini, generic)
    """
    integrations = ["copilot", "claude", "gemini", "generic"]
    click.echo("\nSelect AI coding agent integration:")
    for i, integration in enumerate(integrations, 1):
        click.echo(f"  {i}. {integration}")

    while True:
        try:
            choice = click.prompt("Enter choice (1-4)", type=int)
            if 1 <= choice <= len(integrations):
                return integrations[choice - 1]
            click.echo("Invalid choice. Please try again.")
        except (ValueError, click.Abort):
            click.echo("Invalid input. Using default: copilot")
            return "copilot"


def prompt_for_script_type() -> str:
    """Prompt user for script type.

    Returns:
        Script type (sh or ps)
    """
    script_types = ["sh", "ps"]
    click.echo("\nSelect script type:")
    for i, script_type in enumerate(script_types, 1):
        click.echo(f"  {i}. {script_type}")

    while True:
        try:
            choice = click.prompt("Enter choice (1-2)", type=int)
            if 1 <= choice <= len(script_types):
                return script_types[choice - 1]
            click.echo("Invalid choice. Please try again.")
        except (ValueError, click.Abort):
            click.echo("Invalid input. Using default: sh")
            return "sh"


def initialize_project(
    integration: Optional[str] = None,
    script_type: Optional[str] = None
) -> bool:
    """Initialize Spekificity in current project.

    Creates:
    - .spek/vault/ (with decisions.md, patterns.md, lessons/)
    - .spek/ (with memory/, skills/ subdirectories)
    - .specify/ (SpecKit configuration via specify init)

    Args:
        integration: AI integration to use (copilot, claude, gemini, generic).
                    If None, prompts user interactively.
        script_type: Script type to use (sh, ps).
                    If None, prompts user interactively.

    Returns:
        True if initialization successful
    """
    cwd = Path.cwd()

    click.echo(f"Initializing Spekificity in {cwd}")
    click.echo()

    # Verify dependencies
    if not display_dependency_status():
        return False

    click.echo()

    # Check git repo
    if not is_git_repo():
        click.echo("❌ Not a git repository. Please run 'git init' first.")
        return False

    click.echo("✓ Git repository detected")

    # Create .spek directory first
    spek_path = cwd / ".spek"
    spek_path.mkdir(exist_ok=True)

    # Create vault directory structure inside .spek
    vault_path = spek_path / "vault"
    create_vault_structure(vault_path)
    click.echo(f"✓ Created vault structure at {vault_path}/")

    # Create remaining .spek subdirectories
    (spek_path / "memory").mkdir(exist_ok=True)
    (spek_path / "skills").mkdir(exist_ok=True)
    click.echo(f"✓ Created .spek directory at {spek_path}/")

    # Collect SpecKit configuration inputs
    click.echo("\nConfiguring SpecKit project...")
    if integration is None:
        integration = prompt_for_integration()
    if script_type is None:
        script_type = prompt_for_script_type()

    # Initialize SpecKit per-project (if not already done)
    specify_path = cwd / ".specify"
    if not specify_path.exists():
        try:
            cmd = [
                "specify",
                "init",
                ".",
                "--here",
                "--force",
                f"--integration={integration}",
                f"--script={script_type}"
            ]
            subprocess.run(cmd, timeout=60, check=True)
            click.echo("✓ Initialized SpecKit configuration")
        except subprocess.CalledProcessError as e:
            click.echo(f"⚠ SpecKit initialization failed: {e}")
            click.echo("  (This is optional; you can run 'specify init . --here --force' manually)")
            return False
        except Exception as e:
            click.echo(f"⚠ SpecKit initialization failed: {e}")
            click.echo("  (This is optional; you can run 'specify init . --here --force' manually)")
            return False

    click.echo()
    click.echo("✓ Spekificity initialized successfully!")
    click.echo()
    click.echo("Next steps (use agent skills in Claude Code):")
    click.echo("  1. Review vault structure: ls -la vault/")
    click.echo("  2. Load context: /spek.prepare [FEATURE_NAME]")
    click.echo("  3. Plan feature: /spek.plan [FEATURE_DESCRIPTION]")
    click.echo("  4. Implement: /spek.implement [FEATURE_NAME]")
    click.echo("  5. Conclude: /spek.conclude [FEATURE_NAME]")

    return True


def run_init(
    verbose: bool = False,
    integration: Optional[str] = None,
    script_type: Optional[str] = None
) -> None:
    """CLI command handler for 'spek init'.

    Args:
        verbose: Enable verbose output
        integration: AI integration to use (copilot, claude, gemini, generic)
        script_type: Script type to use (sh, ps)
    """
    success = initialize_project(integration=integration, script_type=script_type)
    if not success:
        raise SystemExit(1)
