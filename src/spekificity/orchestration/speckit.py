"""SpecKit wrapper: Call SpecKit commands from spekificity."""

import subprocess
from pathlib import Path
from loguru import logger
from typing import Optional, Dict, Any
import json


def call_speckit_command(command: str, args: list) -> Dict[str, Any]:
    """
    Call a SpecKit command and capture output.
    
    Args:
        command: SpecKit command (specify, clarify, plan, analyze, tasks, etc.)
        args: Command arguments
    
    Returns:
        Dict with success status, stdout, stderr
    """
    try:
        cmd = ["specify", command] + args
        logger.info(f"Calling SpecKit: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "success": result.returncode == 0,
            "command": " ".join(cmd),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    except subprocess.TimeoutExpired:
        logger.error(f"SpecKit command timed out: {command}")
        return {
            "success": False,
            "command": command,
            "error": "Command timed out (5 minutes)",
            "stdout": "",
            "stderr": "Command execution timed out"
        }
    except FileNotFoundError:
        logger.error("SpecKit not found. Install with: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git")
        return {
            "success": False,
            "command": command,
            "error": "SpecKit not installed",
            "stdout": "",
            "stderr": "SpecKit executable not found in PATH"
        }
    except Exception as e:
        logger.error(f"Error calling SpecKit: {e}")
        return {
            "success": False,
            "command": command,
            "error": str(e),
            "stdout": "",
            "stderr": str(e)
        }


def specify(feature_name: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Call SpecKit specify command."""
    args = ["--output", f"{feature_name}-spec.md"]
    if context:
        args.extend(["--context", context])
    return call_speckit_command("specify", args)


def clarify(spec_file: Path) -> Dict[str, Any]:
    """Call SpecKit clarify command."""
    return call_speckit_command("clarify", [str(spec_file)])


def plan(spec_file: Path) -> Dict[str, Any]:
    """Call SpecKit plan command."""
    args = ["--input", str(spec_file), "--output", str(spec_file.parent / "plan.md")]
    return call_speckit_command("plan", args)


def analyze(spec_file: Path, plan_file: Path) -> Dict[str, Any]:
    """Call SpecKit analyze command."""
    args = ["--spec", str(spec_file), "--plan", str(plan_file)]
    return call_speckit_command("analyze", args)


def tasks(plan_file: Path) -> Dict[str, Any]:
    """Call SpecKit tasks command."""
    args = ["--input", str(plan_file), "--output", str(plan_file.parent / "tasks.md")]
    return call_speckit_command("tasks", args)


def is_speckit_installed() -> bool:
    """Check if SpecKit is installed."""
    result = subprocess.run(
        ["which", "specify"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
