"""Shared subprocess runner and status formatter."""

from __future__ import annotations

import subprocess


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
        raise RuntimeError(
            f"{description}: exited {exc.returncode}\n{exc.stderr.strip()}"
        ) from exc


def print_status(tag: str, message: str) -> None:
    """Print a formatted status line: [TAG] message."""
    print(f"[{tag}] {message}")
