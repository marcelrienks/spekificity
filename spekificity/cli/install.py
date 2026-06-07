"""Dependency verification and auto-installation logic."""

import subprocess
import sys
from typing import List, Tuple

import click


# Minimum required versions
DEPENDENCIES = {
    "python": "3.11",
    "git": None,  # Any version
    "uv": None,   # Any version
    "speckit": "0.9.6",
    "pydantic": "2.0",
}


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version meets minimum requirement (3.11+)."""
    current = sys.version_info
    major_minor = f"{current.major}.{current.minor}"
    
    if current.major >= 3 and current.minor >= 11:
        return True, f"Python {major_minor}"
    return False, f"Python {major_minor} (requires 3.11+)"


def check_command_exists(cmd: str) -> Tuple[bool, str]:
    """Check if a command is available in PATH."""
    try:
        result = subprocess.run(
            ["which", cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, f"{cmd} not found in PATH"
    except Exception as e:
        return False, f"Error checking {cmd}: {e}"


def verify_dependencies() -> Tuple[bool, List[str]]:
    """Verify all dependencies are available.
    
    Returns:
        (all_ok: bool, messages: List[str])
            all_ok: True if all dependencies present
            messages: List of status messages for each dependency
    """
    messages = []
    all_ok = True
    
    # Check Python version
    py_ok, py_msg = check_python_version()
    messages.append(f"{'✓' if py_ok else '✗'} {py_msg}")
    all_ok = all_ok and py_ok
    
    # Check git
    git_ok, git_msg = check_command_exists("git")
    messages.append(f"{'✓' if git_ok else '✗'} git: {git_msg}")
    all_ok = all_ok and git_ok
    
    # Check uv
    uv_ok, uv_msg = check_command_exists("uv")
    messages.append(f"{'✓' if uv_ok else '✗'} uv: {uv_msg}")
    all_ok = all_ok and uv_ok
    
    # Check Python packages (these will be auto-installed by pip, so just note them)
    messages.append("✓ speckit: (will auto-install)")
    messages.append("✓ pydantic: (will auto-install)")
    messages.append("✓ click: (will auto-install)")
    messages.append("✓ gitpython: (will auto-install)")
    
    return all_ok, messages


def display_dependency_status() -> bool:
    """Display dependency status and return True if all required deps present."""
    click.echo("Verifying dependencies...")
    all_ok, messages = verify_dependencies()
    
    for msg in messages:
        click.echo(f"  {msg}")
    
    if not all_ok:
        click.echo()
        click.echo("❌ Missing required dependencies. Install with:")
        click.echo("   git --version  (macOS: brew install git)")
        click.echo("   uv --version   (install from https://github.com/astral-sh/uv)")
        return False
    
    return True
