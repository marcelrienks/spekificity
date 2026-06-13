"""Shared subprocess runner and status formatter."""

from __future__ import annotations

import subprocess
import sys
from contextlib import contextmanager


def run_command(cmd: list[str], description: str, timeout: int | None = None) -> subprocess.CompletedProcess:
    """Run a command without shell=True. Raises RuntimeError on failure or missing binary."""
    try:
        return subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise RuntimeError(f"{description}: command not found — {cmd[0]!r}")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"{description}: timed out after {timeout}s")
    except subprocess.CalledProcessError as exc:
        # Exit code 130 = SIGINT (Ctrl+C) — propagate as KeyboardInterrupt for clean exit
        if exc.returncode == 130:
            raise KeyboardInterrupt() from exc
        raise RuntimeError(
            f"{description}: exited {exc.returncode}\n{exc.stderr.strip()}"
        ) from exc


def print_status(tag: str, message: str) -> None:
    """Print a formatted status line: [TAG] message."""
    print(f"[{tag}] {message}")


_progress_action = ""


def progress_start(action: str) -> None:
    """Show action description."""
    global _progress_action
    _progress_action = action
    sys.stdout.write(f"{action}... ")
    sys.stdout.flush()


def progress_ok() -> None:
    """Mark as successful."""
    sys.stdout.write("✓\n")
    sys.stdout.flush()


def progress_error(message: str = "") -> None:
    """Mark as failed."""
    if message:
        sys.stdout.write(f"✗ ({message})\n")
    else:
        sys.stdout.write("✗\n")
    sys.stdout.flush()
