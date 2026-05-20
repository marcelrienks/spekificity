"""Skill: /spek.context - Load project context (3-layer architecture)."""

from loguru import logger
import click
from typing import Optional

from ..memory.loader import load_context, save_session_context, get_cached_context
from ..vault.loader import get_vault_summary
from ..graph.codegraph import CodeGraph


def execute(layer: str = "all", feature_name: Optional[str] = None, cached: bool = False) -> None:
    """
    Load project context: user, session, and repo layers.
    
    Layers:
    - user: Persistent user memory (/memories/)
    - session: Session-scoped memory (/memories/session/)
    - repo: Repository memory (.cel/, wiki/)
    
    Args:
        layer: Which layers to load ("user", "session", "repo", or "all")
        feature_name: Optional feature name for session context
        cached: Use cached context if available
    """
    logger.info(f"Loading context layer(s): {layer}, cached={cached}")
    
    # Try cached context first
    if cached:
        cached_ctx = get_cached_context()
        if cached_ctx:
            click.echo("✓ Using cached context from session")
            display_context(cached_ctx)
            return
    
    # Load fresh context
    try:
        context = load_context(feature_name=feature_name, layers=layer)
        
        # Display results
        click.echo("\n📦 Context Loading Results:")
        click.echo()
        
        if layer in ("user", "all") and context.user_memory:
            click.echo("👤 User Layer:")
            click.echo(f"  ✓ Source: {context.user_memory.source_path}")
            click.echo(f"  ✓ Preferences: {len(context.user_memory.preferences)} items")
            click.echo(f"  ✓ Skills: {len(context.user_memory.skills)} items")
            click.echo()
        
        if layer in ("session", "all") and context.session_memory:
            click.echo("⏱️  Session Layer:")
            click.echo(f"  ✓ Source: {context.session_memory.source_path}")
            if context.session_memory.feature_state:
                click.echo(f"  ✓ Feature State: {context.session_memory.feature_state}")
            click.echo(f"  ✓ Decisions: {len(context.session_memory.decisions_made)} recorded")
            click.echo()
        
        if layer in ("repo", "all") and context.repo_memory:
            click.echo("🗂️  Repository Layer:")
            click.echo(f"  ✓ Source: {context.repo_memory.source_path}")
            
            # Get vault summary
            vault_summary = get_vault_summary()
            click.echo(f"  ✓ Specs: {vault_summary['specs']} documents")
            click.echo(f"  ✓ Decisions: {vault_summary['decisions']} recorded")
            click.echo(f"  ✓ Patterns: {vault_summary['patterns']} indexed")
            click.echo(f"  ✓ Lessons: {vault_summary['lessons']} learned")
            
            # Check CodeGraph
            graph = CodeGraph()
            stats = graph.get_stats()
            if stats:
                click.echo(f"  ✓ CodeGraph: {stats.get('node_count', 0)} symbols indexed")
            click.echo()
        
        # Save context for session reuse
        save_session_context(context)
        
        click.echo("✅ Context ready for feature development")
        logger.info("Context loading complete")
    
    except Exception as e:
        logger.error(f"Error loading context: {e}")
        click.echo(f"❌ Error loading context: {e}", err=True)
        raise


def display_context(context) -> None:
    """Display context information."""
    click.echo("\n📦 Context Summary:")
    click.echo(f"  Feature: {context.feature_name or 'none'}")
    click.echo(f"  Loaded: {context.loaded_at.isoformat()}")
    click.echo(f"  User Layer: {'✓' if context.user_memory else '✗'}")
    click.echo(f"  Session Layer: {'✓' if context.session_memory else '✗'}")
    click.echo(f"  Repo Layer: {'✓' if context.repo_memory else '✗'}")
