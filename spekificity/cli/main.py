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
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize Spekificity in current project.

    Creates vault/, .spek/ directories and initializes SpecKit configuration.
    """
    try:
        run_init(verbose=ctx.obj.get("verbose", False))
    except SystemExit as e:
        sys.exit(e.code if e.code else 1)




def main() -> None:
    """Entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
