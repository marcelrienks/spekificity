"""Git utilities for verification and operations."""

from pathlib import Path
from loguru import logger
from typing import Optional, List
import subprocess


def get_git_root() -> Optional[Path]:
    """Get git repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except Exception as e:
        logger.error(f"Error getting git root: {e}")
    
    return None


def is_git_clean() -> bool:
    """Check if git working tree is clean."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        return result.returncode == 0 and len(result.stdout.strip()) == 0
    except Exception as e:
        logger.error(f"Error checking git status: {e}")
        return False


def get_current_branch() -> Optional[str]:
    """Get current git branch."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.error(f"Error getting current branch: {e}")
    
    return None


def get_status_summary() -> str:
    """Get git status summary."""
    try:
        result = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.error(f"Error getting git status: {e}")
    
    return ""


def get_uncommitted_files() -> List[str]:
    """Get list of uncommitted files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception as e:
        logger.error(f"Error getting uncommitted files: {e}")
    
    return []


def create_feature_branch(feature_name: str) -> bool:
    """Create a new feature branch."""
    try:
        branch_name = f"feature/{feature_name}"
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            logger.info(f"Created feature branch: {branch_name}")
            return True
        else:
            logger.error(f"Failed to create feature branch: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error creating feature branch: {e}")
        return False


def checkout_branch(branch_name: str) -> bool:
    """Checkout a git branch."""
    try:
        result = subprocess.run(
            ["git", "checkout", branch_name],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            logger.info(f"Checked out branch: {branch_name}")
            return True
        else:
            logger.error(f"Failed to checkout branch: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error checking out branch: {e}")
        return False


def commit(message: str, files: Optional[List[str]] = None) -> bool:
    """Commit changes."""
    try:
        if files:
            subprocess.run(
                ["git", "add"] + files,
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
        else:
            subprocess.run(
                ["git", "add", "-A"],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
        
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            logger.info(f"Committed: {message}")
            return True
        else:
            logger.warning(f"Commit failed or nothing to commit: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error committing: {e}")
        return False


def merge_branch(branch_name: str, message: Optional[str] = None) -> bool:
    """Merge a branch into current branch."""
    try:
        cmd = ["git", "merge", branch_name]
        if message:
            cmd.extend(["-m", message])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            logger.info(f"Merged {branch_name}")
            return True
        else:
            logger.error(f"Merge failed: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error merging: {e}")
        return False


def verify_git_state() -> dict:
    """Comprehensive git state verification."""
    return {
        "is_git_repo": get_git_root() is not None,
        "is_clean": is_git_clean(),
        "current_branch": get_current_branch(),
        "status_summary": get_status_summary(),
        "uncommitted_files": get_uncommitted_files()
    }
