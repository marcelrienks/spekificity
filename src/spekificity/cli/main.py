"""Spekificity CLI: Main entry point for /spek.* commands."""

import click
from loguru import logger

# Import skill commands
from . import prepare, context, plan, map_, implement, post, lessons


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--version", is_flag=True, help="Show version")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, version: bool) -> None:
    """
    Spekificity: Specification-driven framework for rapid AI agent development.
    
    Usage:
        /spek.prepare          Prepare workspace for feature development
        /spek.context          Load and display project context
        /spek.plan             Create feature specification and plan
        /spek.map              Analyze code graph and dependencies
        /spek.implement        Execute implementation tasks
        /spek.post             Archive outcomes and update vault
        /spek.lessons          Extract lessons learned
    
    For detailed help on each command:
        spek COMMAND --help
    """
    if version:
        from .. import __version__
        click.echo(f"Spekificity v{__version__}")
        return
    
    if verbose:
        logger.enable("spekificity")
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="prepare")
@click.option("--feature-name", "-f", default=None, help="Feature name (auto-detected if not provided)")
@click.option("--skip-context", is_flag=True, help="Skip context loading (prepare only)")
@click.option("--force-graph-refresh", is_flag=True, help="Force CodeGraph refresh")
@click.pass_context
def prepare_cmd(ctx: click.Context, feature_name: str, skip_context: bool, force_graph_refresh: bool) -> None:
    """Prepare workspace for feature development."""
    prepare.execute(feature_name=feature_name, skip_context=skip_context, force_graph_refresh=force_graph_refresh)


@cli.command(name="context")
@click.option("--layer", type=click.Choice(["user", "session", "repo", "all"]), default="all", help="Context layer to load")
@click.pass_context
def context_cmd(ctx: click.Context, layer: str) -> None:
    """Load and display project context."""
    context.execute(layer=layer)


@cli.command(name="plan")
@click.argument("feature_intent", required=False, default=None)
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode (prompt for feature intent)")
@click.pass_context
def plan_cmd(ctx: click.Context, feature_intent: str, interactive: bool) -> None:
    """Create feature specification and plan."""
    plan.execute(feature_intent=feature_intent, interactive=interactive)


@cli.command(name="map")
@click.option("--symbol", "-s", default=None, help="Find symbol definition and references")
@click.option("--impact", default=None, help="Analyze impact of changes to a file")
@click.option("--dependencies", "-d", is_flag=True, help="Show dependency graph")
@click.option("--format", type=click.Choice(["ascii", "json", "markdown"]), default="markdown", help="Output format")
@click.pass_context
def map_cmd(ctx: click.Context, symbol: str, impact: str, dependencies: bool, format: str) -> None:
    """Analyze code graph and dependencies."""
    map_.execute(symbol=symbol, impact=impact, dependencies=dependencies, format=format)


@cli.command(name="implement")
@click.option("--dry-run", is_flag=True, help="Preview tasks without execution")
@click.option("--task", "-t", multiple=True, default=None, help="Execute specific task(s)")
@click.pass_context
def implement_cmd(ctx: click.Context, dry_run: bool, task: tuple) -> None:
    """Execute implementation tasks."""
    implement.execute(dry_run=dry_run, tasks=task)


@cli.command(name="post")
@click.option("--merge", is_flag=True, help="Automatically merge feature branch to main")
@click.pass_context
def post_cmd(ctx: click.Context, merge: bool) -> None:
    """Archive outcomes and update vault."""
    post.execute(merge=merge)


@cli.command(name="lessons")
@click.option("--format", type=click.Choice(["markdown", "json"]), default="markdown", help="Output format")
@click.pass_context
def lessons_cmd(ctx: click.Context, format: str) -> None:
    """Extract lessons learned."""
    lessons.execute(format=format)


if __name__ == "__main__":
    cli()
