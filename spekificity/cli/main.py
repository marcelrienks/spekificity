"""Spekificity CLI entry point and command router."""

import sys

import click

from spekificity import __version__
from spekificity.cli.init import run_init
from spekificity.cli.logging_config import setup_logging, CLIError, handle_error


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option("--version", is_flag=True, help="Show version and exit.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--debug", is_flag=True, help="Enable debug logging (very verbose).")
@click.pass_context
def cli(ctx: click.Context, version: bool, verbose: bool, debug: bool) -> None:
    """Spekificity: Spec-driven agent development framework."""
    if version:
        click.echo(f"spek version {__version__}")
        sys.exit(0)

    # Setup logging
    verbose_mode = verbose or debug
    logger = setup_logging(verbose=verbose_mode)

    if debug:
        logger.debug("Debug mode enabled")

    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose_mode
    ctx.obj["debug"] = debug
    ctx.obj["logger"] = logger

    # If no subcommand, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(short_help="Initialize project for Spekificity")
@click.option(
    "--integration",
    type=click.Choice(["copilot", "claude", "gemini", "generic"], case_sensitive=False),
    help="AI coding agent integration (copilot, claude, gemini, generic). Interactive prompt if not specified."
)
@click.option(
    "--script",
    type=click.Choice(["sh", "ps"], case_sensitive=False),
    help="Script type to use (sh, ps). Interactive prompt if not specified."
)
@click.pass_context
def init(ctx: click.Context, integration: str, script: str) -> None:
    """Initialize Spekificity in current project.

    Creates .spek/ directory with vault/, memory/, and skills/ subdirectories.
    Initializes SpecKit configuration via 'specify init'.

    Interactive by default: prompts for AI integration and script type.
    Use --integration and --script flags to skip interactive prompts.

    Examples:
        spek init                                    # Interactive prompts
        spek init --integration copilot --script sh  # Non-interactive
    """
    try:
        run_init(
            verbose=ctx.obj.get("verbose", False),
            integration=integration,
            script_type=script
        )
    except SystemExit as e:
        sys.exit(e.code if e.code else 1)




def main() -> None:
    """Entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
