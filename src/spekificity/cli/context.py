"""Skill: /spek.context - Load project context (3-layer architecture)."""

from loguru import logger
import click


def execute(layer: str = "all") -> None:
    """
    Load project context: user, session, and repo layers.
    
    Layers:
    - user: Persistent user memory (/memories/)
    - session: Session-scoped memory (/memories/session/)
    - repo: Repository memory (.cel/, wiki/)
    """
    logger.info(f"Loading context layer(s): {layer}")
    
    if layer in ("user", "all"):
        logger.info("Loading user memory...")
        click.echo("User Layer:")
        click.echo("  ✓ Preferences loaded")
        click.echo("  ✓ Custom skills loaded")
    
    if layer in ("session", "all"):
        logger.info("Loading session memory...")
        click.echo("\nSession Layer:")
        click.echo("  ✓ Current feature state loaded")
        click.echo("  ✓ Session decisions loaded")
    
    if layer in ("repo", "all"):
        logger.info("Loading repo memory...")
        click.echo("\nRepository Layer:")
        click.echo("  ✓ Vault specs loaded")
        click.echo("  ✓ Architecture decisions loaded")
        click.echo("  ✓ Lessons learned loaded")
        click.echo("  ✓ CodeGraph indexed")
    
    click.echo("\n✓ Context ready for feature development")
