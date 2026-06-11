"""Shared subprocess runner and status formatter."""

from __future__ import annotations

import subprocess


def run_command(cmd: list[str], description: str) -> subprocess.CompletedProcess:
    """Run a command without shell=True. Raises RuntimeError on failure or missing binary."""
    try:
        return subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise RuntimeError(f"{description}: command not found — {cmd[0]!r}")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"{description}: exited {exc.returncode}\n{exc.stderr.strip()}"
        ) from exc


def print_status(tag: str, message: str) -> None:
    """Print a formatted status line: [TAG] message."""
    print(f"[{tag}] {message}")
