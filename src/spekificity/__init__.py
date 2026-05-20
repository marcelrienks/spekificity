"""Spekificity: Specification-driven framework for rapid AI agent development."""

__version__ = "0.1.0-alpha.1"
__author__ = "Marcel Rienks"
__license__ = "MIT"

# Core components exposed at package level
from .cli.main import cli  # noqa: F401

__all__ = ["cli"]
