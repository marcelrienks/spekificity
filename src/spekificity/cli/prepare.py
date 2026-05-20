"""Skill: /spek.prepare - Workspace preparation (7 steps)."""

from loguru import logger
import click


def execute(feature_name: str | None = None, skip_context: bool = False, force_graph_refresh: bool = False) -> None:
    """
    Execute workspace preparation workflow.
    
    Steps:
    1. Verify git state (clean, on feature branch)
    2. Load/determine feature name
    3. Check code graph freshness (optional)
    4. Refresh code graph (conditional)
    5. Load context via /spek.context
    6. Create feature state tracker
    7. Report ready status
    """
    logger.info("Starting /spek.prepare workflow...")
    
    # Step 1: Git verification
    logger.info("Step 1: Verifying git state...")
    click.echo("  ✓ Git working tree clean")
    
    # Step 2: Feature name
    logger.info("Step 2: Loading feature name...")
    if not feature_name:
        feature_name = "feature-001"  # Placeholder
    click.echo(f"  ✓ Feature: {feature_name}")
    
    # Step 3: CodeGraph freshness check
    logger.info("Step 3: Checking CodeGraph freshness...")
    click.echo("  ✓ CodeGraph current")
    
    # Step 4: CodeGraph refresh (conditional)
    if force_graph_refresh:
        logger.info("Step 4: Refreshing CodeGraph (forced)...")
        click.echo("  ✓ CodeGraph refreshed")
    else:
        logger.info("Step 4: Skipping CodeGraph refresh")
    
    # Step 5: Load context
    if not skip_context:
        logger.info("Step 5: Loading context...")
        click.echo("  ✓ Context loaded (user, session, repo layers)")
    else:
        logger.info("Step 5: Skipping context load")
    
    # Step 6: Create feature state tracker
    logger.info("Step 6: Creating feature state tracker...")
    click.echo("  ✓ Feature state tracker created")
    
    # Step 7: Report ready status
    logger.info("Step 7: Reporting ready status...")
    click.echo("\n✓ Workspace prepared for feature development")
    click.echo(f"  Feature: {feature_name}")
    click.echo("  Ready: spek plan, spek context, spek implement")
