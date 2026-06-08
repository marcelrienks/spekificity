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


def initialize_project() -> bool:
    """Initialize Spekificity in current project.
    
    Creates:
    - vault/ (with decisions.md, patterns.md, lessons/)
    - .spek/ (skills and configuration)
    - specs/ (feature specifications directory)
    - .specify/ (SpecKit configuration, if not exists)
    
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
    
    # Create vault directory structure
    vault_path = cwd / "vault"
    create_vault_structure(vault_path)
    click.echo(f"✓ Created vault structure at {vault_path}/")
    
    # Create .spek directory
    spek_path = cwd / ".spek"
    spek_path.mkdir(exist_ok=True)
    (spek_path / "memory").mkdir(exist_ok=True)
    (spek_path / "skills").mkdir(exist_ok=True)
    click.echo(f"✓ Created .spek directory at {spek_path}/")
    
    # Create specs directory
    specs_path = cwd / "specs"
    specs_path.mkdir(exist_ok=True)
    click.echo(f"✓ Created specs directory at {specs_path}/")
    
    # Initialize SpecKit per-project (if not already done)
    specify_path = cwd / ".specify"
    if not specify_path.exists():
        try:
            subprocess.run(
                ["specify", "init", "."],
                capture_output=True,
                timeout=30
            )
            click.echo(f"✓ Initialized SpecKit configuration")
        except Exception as e:
            click.echo(f"⚠ SpecKit initialization failed: {e}")
            click.echo("  (This is optional; you can run 'specify init .' manually)")
    
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


def run_init(verbose: bool = False) -> None:
    """CLI command handler for 'spek init'."""
    success = initialize_project()
    if not success:
        raise SystemExit(1)
