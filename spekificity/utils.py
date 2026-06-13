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
    global _progress_action
    if VERBOSE:
        if _progress_action:
            print()  # Move to new line after progress_start
            _progress_action = ""
        print(f"[{tag}] {message}")


_progress_action = ""


def progress_start(action: str) -> None:
    """Show action description."""
    global _progress_action
    _progress_action = action
    print(f"{action}...", end=" ", flush=True)


def progress_ok() -> None:
    """Mark as successful."""
    print("✓")


def progress_error(message: str = "") -> None:
    """Mark as failed."""
    if message:
        sys.stdout.write(f"✗ ({message})\n")
    else:
        sys.stdout.write("✗\n")
    sys.stdout.flush()
