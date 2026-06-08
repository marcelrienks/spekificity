"""Logging configuration for Spekificity CLI."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Configure logging for CLI with optional file output.

    Args:
        verbose: Enable debug-level logging
        log_file: Optional log file path

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("spekificity")

    # Clear any existing handlers
    logger.handlers = []

    # Set level
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)

    # Format
    formatter = logging.Formatter(
        fmt="%(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


class CLIError(Exception):
    """User-facing CLI error (exit cleanly with message)."""
    pass


class CLIWarning:
    """Non-fatal warning message."""

    def __init__(self, message: str):
        self.message = message

    def display(self):
        """Display warning to user."""
        click.echo(f"⚠ {self.message}", err=False)


def handle_error(error: Exception, verbose: bool = False) -> int:
    """Handle error and return exit code.

    Args:
        error: Exception to handle
        verbose: Show full traceback in debug mode

    Returns:
        Exit code (1 for general error, 2 for CLI error)
    """
    if isinstance(error, CLIError):
        click.echo(f"❌ Error: {error}", err=True)
        return 1

    if verbose:
        # Show full traceback in debug mode
        import traceback
        traceback.print_exc(file=sys.stderr)

    click.echo(f"❌ Error: {error}", err=True)
    return 1
