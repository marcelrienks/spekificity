"""Spekificity CLI entry point and command router."""

import sys
import logging
from typing import Optional
from pathlib import Path

import click

from spekificity import __version__
from spekificity.cli.init import run_init
from spekificity.cli.logging_config import setup_logging, CLIError, handle_error
from spekificity.core.vault import load_vault
from spekificity.core.context import ContextLoader
from spekificity.core.speckit_wrapper import run_specify, run_plan, validate_spec
from spekificity.core.progress import ProgressLogger
from spekificity.core.decisions import DecisionLogger
from spekificity.integrations.lat_md import load_index, query_relevant_context
from spekificity.integrations.semantic_search import SemanticSearcher
from spekificity.integrations.speckit import SpecKitError


class SpekGroup(click.Group):
    """Custom click Group for better help formatting."""

    def format_help(self, ctx: click.Context, formatter) -> None:
        """Format help output with sections."""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        
        formatter.write_section("Commands")
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            help_text = cmd.get_short_help_str(100) or ""
            commands.append((subcommand, help_text))
        
        if commands:
            with formatter.section("Commands"):
                formatter.write_dl(commands)
        
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)


@click.group(
    cls=SpekGroup,
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option("--version", is_flag=True, help="Show version and exit.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--color/--no-color", default=True, help="Enable/disable colored output.")
@click.option("--debug", is_flag=True, help="Enable debug logging (very verbose).")
@click.pass_context
def cli(ctx: click.Context, version: bool, verbose: bool, color: bool, debug: bool) -> None:
    """Spekificity: Spec-driven agent development framework.

    Transform feature intent into executable specifications and persistent knowledge.

    CLI Commands (for project initialization):
        spek --help                 Show this help message
        spek --version              Show version
        spek init                   Initialize Spekificity in project

    Agent Skills (for interactive workflows - use in Claude Code):
        /spek.prepare [FEATURE]     Load prior context, onboard to feature
        /spek.plan [FEATURE]        Generate spec, plan, and tasks
        /spek.implement [FEATURE]   Execute tasks with context injection
        /spek.conclude              Analyze outcomes, extract lessons, update vault

    Documentation: wiki/skills.md
    """
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
    ctx.obj["color"] = color
    ctx.obj["debug"] = debug
    ctx.obj["logger"] = logger

    # If no subcommand, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(short_help="Initialize project for Spekificity")
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize Spekificity in current project.

    Creates vault/, .spek/, specs/ directories and initializes per-project configuration.
    """
    try:
        run_init(verbose=ctx.obj.get("verbose", False))
    except SystemExit as e:
        sys.exit(e.code if e.code else 1)


@cli.command(short_help="Onboard to feature, load prior context")
@click.argument("feature", required=False)
@click.option("--no-index", is_flag=True, help="Skip codebase indexing (faster)")
@click.option("--compressed", is_flag=True, help="Use Caveman compression for output")
@click.pass_context
def prepare(ctx: click.Context, feature: Optional[str], no_index: bool, compressed: bool) -> None:
    """Prepare for feature development.

    Loads vault (decisions, patterns, lessons), indexes codebase via lat.md,
    and generates a navigation guide.
    """
    logger = ctx.obj.get("logger")
    cwd = Path.cwd()
    vault_path = cwd / "vault"

    if not vault_path.exists():
        msg = "Not in a Spekificity project. Run 'spek init' first"
        if logger:
            logger.error(msg)
        click.echo(f"❌ Error: {msg}", err=True)
        sys.exit(1)

    click.echo("❯ Preparing feature context...")
    if feature:
        click.echo(f"  Feature: {feature}")
        if logger:
            logger.info(f"Preparing context for: {feature}")

    try:
        # Load vault
        vault = load_vault(str(vault_path))
        decisions = vault.load_decisions()
        patterns = vault.load_patterns()

        if logger:
            logger.debug(f"Loaded {len(decisions)} decisions, {len(patterns)} patterns")

        click.echo()
        click.echo("## Prior Decisions")
        for decision in decisions[:3]:
            click.echo(f"- {decision.get('title', 'Untitled')}")

        click.echo()
        click.echo("## Relevant Patterns")
        for pattern in patterns[:3]:
            click.echo(f"- {pattern.get('title', 'Untitled')}")

        # Load codebase index
        if not no_index and feature:
            click.echo()
            click.echo("## Codebase Index")
            try:
                if logger:
                    logger.debug("Syncing lat.md index...")
                index = load_index(str(cwd))
                index.sync_index()

                # Query for relevant files
                context = query_relevant_context(feature, str(cwd), max_files=3, max_functions=3)
                files = context.get("files", [])

                if files:
                    click.echo("  Relevant files:")
                    for f in files[:3]:
                        path = f.get("path", f.get("file", "unknown"))
                        click.echo(f"    - {path}")
                if logger:
                    logger.debug(f"Found {len(files)} relevant files")
            except Exception as e:
                warning = f"lat.md indexing failed: {e} (using fallback)"
                if logger:
                    logger.warning(warning)
                click.echo(f"  ⚠ {warning}")

        click.echo()
        click.echo("## Context Summary")
        click.echo(f"- Decisions loaded: {len(decisions)}")
        click.echo(f"- Patterns loaded: {len(patterns)}")
        click.echo(f"- Estimated context tokens: ~5000-15000")

        click.echo()
        click.echo("Ready to plan or implement. Next: spek plan")

        if logger:
            logger.info("Feature preparation complete")

    except Exception as e:
        if logger:
            logger.error(f"Prepare failed: {e}", exc_info=ctx.obj.get("debug"))
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command(short_help="[DEPRECATED] Use agent skill instead")
@click.argument("feature", required=False)
@click.pass_context
def plan(ctx: click.Context, feature: Optional[str]) -> None:
    """[DEPRECATED] Generate specification and implementation plan.

    This CLI command is deprecated. Use the agent skill instead:
      /spek.plan [feature-name]

    The interactive workflow (spec → clarification → plan → tasks) requires
    Claude Code agent context, not a pure CLI invocation.

    For documentation: wiki/skills.md#spek.plan
    """
    click.echo(
        "Error: 'spek plan' requires Claude Code agent context. Use the agent skill:\n\n"
        "  /spek.plan [feature-name]\n\n"
        "This interactive workflow generates spec → clarification → plan → tasks with your input.\n"
        "Documentation: wiki/skills.md#spek.plan"
    )
    sys.exit(1)


@cli.command(short_help="[DEPRECATED] Use agent skill instead")
@click.argument("task", required=False)
@click.pass_context
def implement(ctx: click.Context, task: Optional[str]) -> None:
    """[DEPRECATED] Execute implementation task.

    This CLI command is deprecated. Use the agent skill instead:
      /spek.implement [feature-name|spec-file] [--steps N]

    The interactive workflow (context injection, task execution, decision logging)
    requires Claude Code agent context, not a pure CLI invocation.

    For documentation: wiki/skills.md#spek.implement
    """
    click.echo(
        "Error: 'spek implement' requires Claude Code agent context. Use the agent skill:\n\n"
        "  /spek.implement [feature-name|spec-file] [--steps N]\n\n"
        "This interactive workflow executes tasks with context injection and progress tracking.\n"
        "Documentation: wiki/skills.md#spek.implement"
    )
    sys.exit(1)


@cli.command(short_help="[DEPRECATED] Use agent skill instead")
@click.argument("feature", required=False)
@click.pass_context
def conclude(ctx: click.Context, feature: Optional[str]) -> None:
    """[DEPRECATED] Conclude feature development.

    This CLI command is deprecated. Use the agent skill instead:
      /spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]

    The interactive workflow (analysis, lessons extraction, vault sync)
    requires Claude Code agent context, not a pure CLI invocation.

    For documentation: wiki/skills.md#spek.conclude
    """
    click.echo(
        "Error: 'spek conclude' requires Claude Code agent context. Use the agent skill:\n\n"
        "  /spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]\n\n"
        "This interactive workflow analyzes outcomes, extracts lessons, and updates the vault.\n"
        "Documentation: wiki/skills.md#spek.conclude"
    )
    sys.exit(1)


def main() -> None:
    """Entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
