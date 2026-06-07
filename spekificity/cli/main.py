"""Spekificity CLI entry point and command router."""

import sys
from typing import Optional

import click

from spekificity import __version__


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
@click.pass_context
def cli(ctx: click.Context, version: bool, verbose: bool, color: bool) -> None:
    """Spekificity: Spec-driven agent development framework.
    
    Transform feature intent into executable specifications and persistent knowledge.
    
    Usage:
        spek --help                 Show this help message
        spek --version              Show version
        spek <command> --help       Show command help
        spek init                   Initialize project
        spek prepare [FEATURE]      Onboard to feature, load context
        spek plan [FEATURE]         Generate spec, plan, tasks
        spek implement [TASK]       Execute task with context injection
        spek conclude [FEATURE]     Analyze outcomes, update vault
    """
    if version:
        click.echo(f"spek version {__version__}")
        sys.exit(0)
    
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["color"] = color
    
    # If no subcommand, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(short_help="Initialize project for Spekificity")
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize Spekificity in current project.
    
    Creates vault/, .spek/, specs/ directories and initializes per-project configuration.
    """
    click.echo("❯ Initializing Spekificity...")
    click.echo("  (init command not yet implemented)")
    
    if ctx.obj.get("verbose"):
        click.echo("  Verbose mode enabled")


@cli.command(short_help="Onboard to feature, load prior context")
@click.argument("feature", required=False)
@click.pass_context
def prepare(ctx: click.Context, feature: Optional[str]) -> None:
    """Prepare for feature development.
    
    Loads vault (decisions, patterns, lessons), indexes codebase via lat.md,
    and generates a navigation guide.
    """
    click.echo("❯ Preparing feature context...")
    if feature:
        click.echo(f"  Feature: {feature}")
    click.echo("  (prepare command not yet implemented)")


@cli.command(short_help="Generate spec, clarify, plan implementation")
@click.argument("feature", required=False)
@click.pass_context
def plan(ctx: click.Context, feature: Optional[str]) -> None:
    """Generate specification and implementation plan.
    
    Converts feature description to spec.md, identifies ambiguities,
    and generates plan.md and tasks.md.
    """
    click.echo("❯ Planning feature implementation...")
    if feature:
        click.echo(f"  Feature: {feature}")
    click.echo("  (plan command not yet implemented)")


@cli.command(short_help="Execute task with context injection")
@click.argument("task", required=False)
@click.option("--resume", is_flag=True, help="Resume interrupted task")
@click.pass_context
def implement(ctx: click.Context, task: Optional[str], resume: bool) -> None:
    """Execute implementation task.
    
    Injects relevant context (decisions, patterns, code), tracks progress,
    logs decisions made during implementation.
    """
    click.echo("❯ Implementing task...")
    if task:
        click.echo(f"  Task: {task}")
    if resume:
        click.echo("  Resuming interrupted task")
    click.echo("  (implement command not yet implemented)")


@cli.command(short_help="Analyze outcomes, update vault")
@click.argument("feature", required=False)
@click.pass_context
def conclude(ctx: click.Context, feature: Optional[str]) -> None:
    """Conclude feature development.
    
    Analyzes outcomes vs success criteria, extracts lessons,
    updates vault with new patterns and decisions.
    """
    click.echo("❯ Concluding feature...")
    if feature:
        click.echo(f"  Feature: {feature}")
    click.echo("  (conclude command not yet implemented)")


def main() -> None:
    """Entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
