"""Shared subprocess runner and status formatter."""

from __future__ import annotations

import subprocess
import sys
from contextlib import contextmanager

VERBOSE = False


def run_command(cmd: list[str], description: str, timeout: int | None = None) -> subprocess.CompletedProcess:
    """Run a command without shell=True. Raises RuntimeError on failure or missing binary."""
    if VERBOSE:
        print(f"[DEBUG] Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,
        )
        if VERBOSE and result.stdout:
            print(f"[DEBUG] Output:\n{result.stdout}")
        return result
    except FileNotFoundError:
        raise RuntimeError(f"{description}: command not found — {cmd[0]!r}")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"{description}: timed out after {timeout}s")
    except subprocess.CalledProcessError as exc:
        if VERBOSE:
            print(f"[DEBUG] Error output:\n{exc.stderr}")
        # Exit code 130 = SIGINT (Ctrl+C) — propagate as KeyboardInterrupt for clean exit
        if exc.returncode == 130:
            raise KeyboardInterrupt() from exc
        raise RuntimeError(
            f"{description}: exited {exc.returncode}\n{exc.stderr.strip()}"
        ) from exc


def print_status(tag: str, message: str) -> None:
    """Print a formatted status line: [TAG] message. Only shown in verbose mode."""
    global _progress_action, _progress_has_verbose
    if VERBOSE:
        if _progress_action and not _progress_has_verbose:
            print()  # Move to new line before first verbose message in this progress action
            _progress_has_verbose = True
        print(f"[{tag}] {message}")


_progress_action = ""
_progress_has_verbose = False


def progress_start(action: str) -> None:
    """Show action description."""
    global _progress_action, _progress_has_verbose
    _progress_action = action
    _progress_has_verbose = False
    print(f"{action}... ", end="", flush=True)


def progress_ok() -> None:
    """Mark as successful."""
    global _progress_action, _progress_has_verbose
    if _progress_has_verbose:
        print("✓")  # New line (already moved to new line from verbose messages)
    else:
        print(" ✓")  # Same line as progress indicator
    _progress_action = ""
    _progress_has_verbose = False


def progress_error(message: str = "") -> None:
    """Mark as failed."""
    if message:
        sys.stdout.write(f"✗ ({message})\n")
    else:
        sys.stdout.write("✗\n")
    sys.stdout.flush()
