"""spek CLI — entry point for `spek init`."""

import click


@click.group()
@click.version_option()
def main() -> None:
    """Spekificity — spec-driven agent development framework."""


@main.command()
@click.argument("path", default=".", type=click.Path(file_okay=False))
@click.option("--integration", default=None, help="Agent integration type (e.g. claude, copilot, gemini).")
@click.option("--script", "script_type", default=None, type=click.Choice(["sh", "ps"]), help="Script type.")
@click.option("--no-git-hooks", is_flag=True, default=False, help="Skip git hook installation.")
def init(path: str, integration: str | None, script_type: str | None, no_git_hooks: bool) -> None:
    """Initialize Spekificity in a project directory."""
    raise NotImplementedError("spek init — implementation pending")
