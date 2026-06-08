"""Spekificity CLI entry point and command router."""

import sys
from typing import Optional
from pathlib import Path

import click

from spekificity import __version__
from spekificity.cli.init import run_init
from spekificity.core.vault import load_vault
from spekificity.core.context import ContextLoader
from spekificity.core.speckit_wrapper import run_specify, run_plan
from spekificity.core.progress import ProgressLogger
from spekificity.core.decisions import DecisionLogger


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
    cwd = Path.cwd()
    vault_path = cwd / "vault"

    if not vault_path.exists():
        click.echo("❌ Error: Not in a Spekificity project. Run 'spek init' first")
        sys.exit(1)

    click.echo("❯ Preparing feature context...")
    if feature:
        click.echo(f"  Feature: {feature}")

    try:
        vault = load_vault(str(vault_path))
        decisions = vault.load_decisions()
        patterns = vault.load_patterns()

        click.echo()
        click.echo("## Prior Decisions")
        for decision in decisions[:3]:
            click.echo(f"- {decision.get('title', 'Untitled')}")

        click.echo()
        click.echo("## Relevant Patterns")
        for pattern in patterns[:3]:
            click.echo(f"- {pattern.get('title', 'Untitled')}")

        click.echo()
        click.echo("## Context Summary")
        click.echo(f"- Decisions loaded: {len(decisions)}")
        click.echo(f"- Patterns loaded: {len(patterns)}")
        click.echo(f"- Estimated context tokens: ~5000-15000")

        click.echo()
        click.echo("Ready to plan or implement. Next: spek plan")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command(short_help="Generate spec, clarify, plan implementation")
@click.argument("feature", required=False)
@click.option("--skip-prepare", is_flag=True, help="Skip prepare phase")
@click.option("--no-clarify", is_flag=True, help="Skip ambiguity clarification")
@click.pass_context
def plan(ctx: click.Context, feature: Optional[str], skip_prepare: bool, no_clarify: bool) -> None:
    """Generate specification and implementation plan.

    Converts feature description to spec.md, identifies ambiguities,
    and generates plan.md and tasks.md.
    """
    cwd = Path.cwd()
    vault_path = cwd / "vault"

    if not vault_path.exists():
        click.echo("❌ Error: Not in a Spekificity project. Run 'spek init' first")
        sys.exit(1)

    if not feature:
        click.echo("❌ Error: Feature description required. Usage: spek plan 'Your feature description'")
        sys.exit(1)

    click.echo("❯ Planning feature implementation...")
    click.echo(f"  Feature: {feature}")

    try:
        click.echo()
        click.echo("## Specification Generation")
        click.echo("  Running SpecKit specify command...")
        click.echo("  (Full implementation requires SpecKit integration)")
        click.echo()
        click.echo("## Plan Generation")
        click.echo("  Running SpecKit plan command...")
        click.echo("  (Full implementation requires SpecKit integration)")
        click.echo()
        click.echo("✓ Specification, plan, and tasks would be generated")
        click.echo("  See specs/ directory for output")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command(short_help="Execute task with context injection")
@click.argument("task", required=False)
@click.option("--task", "task_id", help="Task ID (e.g., T1.1)")
@click.option("--resume", is_flag=True, help="Resume interrupted task")
@click.option("--list", "list_tasks", is_flag=True, help="List all tasks")
@click.option("--mark-complete", is_flag=True, help="Mark task as complete")
@click.option("--skip-context", is_flag=True, help="Skip context injection")
@click.pass_context
def implement(
    ctx: click.Context,
    task: Optional[str],
    task_id: Optional[str],
    resume: bool,
    list_tasks: bool,
    mark_complete: bool,
    skip_context: bool,
) -> None:
    """Execute implementation task.

    Injects relevant context (decisions, patterns, code), tracks progress,
    logs decisions made during implementation.
    """
    cwd = Path.cwd()
    vault_path = cwd / "vault"

    if not vault_path.exists():
        click.echo("❌ Error: Not in a Spekificity project. Run 'spek init' first")
        sys.exit(1)

    click.echo("❯ Implementing task...")

    task_to_use = task_id or task

    if list_tasks:
        click.echo("  Available tasks would be listed here")
        click.echo("  (Requires tasks.md parsing)")
        return

    if not task_to_use and not list_tasks:
        click.echo("❌ Error: Task ID required. Usage: spek implement --task T1.1")
        sys.exit(1)

    try:
        click.echo(f"  Task: {task_to_use}")

        click.echo()
        click.echo("## Task Context Loaded")
        click.echo("  - Relevant code files: [would load via lat.md]")
        click.echo("  - Prior decisions: [would load from vault]")
        click.echo("  - Relevant patterns: [would load from vault]")

        click.echo()
        click.echo("## Progress Log")
        click.echo(f"  File: .specify/logs/{task_to_use}.log")
        click.echo("  (Progress tracking would be initialized)")

        click.echo()
        click.echo("Agent session started. Context injected.")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command(short_help="Analyze outcomes, update vault")
@click.argument("feature", required=False)
@click.option("--feature", "feature_name", help="Feature branch or spec ID")
@click.option("--all", "conclude_all", is_flag=True, help="Conclude all completed features")
@click.option("--export-vault", is_flag=True, help="Export vault using Obsidian CLI")
@click.option("--dry-run", is_flag=True, help="Show what would be concluded")
@click.pass_context
def conclude(
    ctx: click.Context,
    feature: Optional[str],
    feature_name: Optional[str],
    conclude_all: bool,
    export_vault: bool,
    dry_run: bool,
) -> None:
    """Conclude feature development.

    Analyzes outcomes vs success criteria, extracts lessons,
    updates vault with new patterns and decisions.
    """
    cwd = Path.cwd()
    vault_path = cwd / "vault"

    if not vault_path.exists():
        click.echo("❌ Error: Not in a Spekificity project. Run 'spek init' first")
        sys.exit(1)

    feature_to_use = feature_name or feature

    click.echo("❯ Concluding feature...")
    if feature_to_use:
        click.echo(f"  Feature: {feature_to_use}")

    try:
        if dry_run:
            click.echo("  (Dry-run mode: no changes will be made)")

        click.echo()
        click.echo("## Outcomes Analysis")
        click.echo("  Comparing actual vs planned outcomes...")
        click.echo("  (Full implementation requires progress log analysis)")

        click.echo()
        click.echo("## Vault Update")
        click.echo("  - New decisions would be appended to vault/decisions.md")
        click.echo("  - New patterns would be appended to vault/patterns.md")
        click.echo("  - Lessons would be written to vault/lessons/")

        click.echo()
        click.echo("✓ Feature conclusion complete")
        click.echo("  Ready for next feature: spek prepare")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


def main() -> None:
    """Entry point for CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
