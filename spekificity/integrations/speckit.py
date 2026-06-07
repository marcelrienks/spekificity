"""Integration with SpecKit CLI for spec/plan/implement generation.

Low-level SpecKit command runners with subprocess management.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import re

import click


class SpecKitError(Exception):
    """SpecKit command execution error."""
    pass


def check_speckit_version() -> str:
    """Check SpecKit version and ensure it's v0.9.6 or later.

    Returns:
        SpecKit version string

    Raises:
        SpecKitError: if SpecKit not installed or version too old
    """
    try:
        result = subprocess.run(
            ["speckit", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            raise SpecKitError("SpecKit --version failed")

        version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout + result.stderr)
        if not version_match:
            raise SpecKitError("Could not parse SpecKit version")

        version = version_match.group(1)

        # Parse version
        major, minor, patch = map(int, version.split('.'))
        if major < 0 or (major == 0 and (minor < 9 or (minor == 9 and patch < 6))):
            raise SpecKitError(f"SpecKit {version} < 0.9.6 required")

        return version
    except subprocess.TimeoutExpired:
        raise SpecKitError("SpecKit version check timed out")
    except FileNotFoundError:
        raise SpecKitError("SpecKit not found in PATH. Install with: uv tool install speckit>=0.9.6")


def invoke_specify(
    feature_intent: str,
    output_dir: str = ".",
    env_vars: Optional[Dict[str, str]] = None,
    timeout: int = 300
) -> Dict[str, Any]:
    """Run `speckit specify` command.

    Args:
        feature_intent: Feature description for specification
        output_dir: Directory for output files
        env_vars: Environment variables to pass to SpecKit
        timeout: Command timeout in seconds

    Returns:
        Dict with 'spec' (Markdown), 'metadata' from SpecKit output

    Raises:
        SpecKitError: if command fails
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "speckit", "specify",
        "--intent", feature_intent,
        "--output", str(output_path),
    ]

    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(output_path),
            env=env
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise SpecKitError(f"speckit specify failed: {error_msg}")

        # Parse output (SpecKit returns JSON or Markdown)
        spec_file = output_path / "spec.md"
        if spec_file.exists():
            spec_text = spec_file.read_text()
        else:
            spec_text = result.stdout

        return {
            "spec": spec_text,
            "stdout": result.stdout,
            "metadata": {
                "command": " ".join(cmd),
                "output_dir": str(output_path)
            }
        }
    except subprocess.TimeoutExpired:
        raise SpecKitError(f"speckit specify timed out after {timeout}s")
    except Exception as e:
        raise SpecKitError(f"speckit specify error: {e}")


def invoke_plan(
    spec_file: str,
    output_dir: str = ".",
    env_vars: Optional[Dict[str, str]] = None,
    timeout: int = 300
) -> Dict[str, Any]:
    """Run `speckit plan` command.

    Args:
        spec_file: Path to spec.md
        output_dir: Directory for output files
        env_vars: Environment variables to pass to SpecKit
        timeout: Command timeout in seconds

    Returns:
        Dict with 'plan', 'tasks' (Markdown), 'metadata' from SpecKit output

    Raises:
        SpecKitError: if command fails
    """
    spec_path = Path(spec_file)
    if not spec_path.exists():
        raise SpecKitError(f"spec.md not found: {spec_file}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "speckit", "plan",
        "--spec", str(spec_path),
        "--output", str(output_path),
    ]

    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(output_path),
            env=env
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise SpecKitError(f"speckit plan failed: {error_msg}")

        # Parse output
        plan_file = output_path / "plan.md"
        tasks_file = output_path / "tasks.md"

        plan_text = plan_file.read_text() if plan_file.exists() else result.stdout
        tasks_text = tasks_file.read_text() if tasks_file.exists() else ""

        return {
            "plan": plan_text,
            "tasks": tasks_text,
            "stdout": result.stdout,
            "metadata": {
                "command": " ".join(cmd),
                "output_dir": str(output_path)
            }
        }
    except subprocess.TimeoutExpired:
        raise SpecKitError(f"speckit plan timed out after {timeout}s")
    except Exception as e:
        raise SpecKitError(f"speckit plan error: {e}")


def invoke_analyze(
    spec_file: str,
    timeout: int = 60
) -> Dict[str, Any]:
    """Run `speckit analyze` for spec validation.

    Args:
        spec_file: Path to spec.md
        timeout: Command timeout in seconds

    Returns:
        Dict with 'analysis', 'valid' (bool), 'issues' (list)

    Raises:
        SpecKitError: if command fails
    """
    spec_path = Path(spec_file)
    if not spec_path.exists():
        raise SpecKitError(f"spec.md not found: {spec_file}")

    cmd = [
        "speckit", "analyze",
        "--spec", str(spec_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # analyze may exit with non-zero if issues found
        analysis = result.stdout + result.stderr
        valid = result.returncode == 0

        return {
            "analysis": analysis,
            "valid": valid,
            "stdout": result.stdout,
            "metadata": {
                "command": " ".join(cmd),
            }
        }
    except subprocess.TimeoutExpired:
        raise SpecKitError(f"speckit analyze timed out after {timeout}s")
    except Exception as e:
        raise SpecKitError(f"speckit analyze error: {e}")
