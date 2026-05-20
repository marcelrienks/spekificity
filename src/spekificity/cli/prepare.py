"""Skill: /spek.prepare - Workspace preparation (7 steps)."""

from loguru import logger
import click
from typing import Optional

from ..utils.git import verify_git_state, is_git_clean
from ..memory.loader import load_context, save_session_context, save_feature_state
from ..graph.codegraph import CodeGraph
from ..utils.models import FeatureState
from datetime import datetime


def execute(feature_name: Optional[str] = None, skip_context: bool = False, force_graph_refresh: bool = False) -> None:
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
    
    click.echo("\n🔧 Preparing workspace for feature development...")
    click.echo()
    
    try:
        # Step 1: Git verification
        click.echo("📌 Step 1: Verifying git state...")
        git_state = verify_git_state()
        
        if not git_state["is_git_repo"]:
            click.echo("  ❌ Not a git repository", err=True)
            raise click.Abort()
        
        if not git_state["is_clean"]:
            click.echo(f"  ⚠️  Working tree has uncommitted changes:")
            for file in git_state["uncommitted_files"][:5]:
                click.echo(f"     - {file}")
            if len(git_state["uncommitted_files"]) > 5:
                click.echo(f"     ... and {len(git_state['uncommitted_files']) - 5} more")
            click.echo("  💡 Tip: Commit or stash changes before proceeding")
            raise click.Abort()
        
        click.echo(f"  ✓ Git clean (branch: {git_state['current_branch']})")
        
        # Step 2: Feature name
        click.echo("\n📌 Step 2: Loading feature name...")
        if not feature_name:
            feature_name = click.prompt("Enter feature name", type=str)
        
        if not feature_name or not feature_name.strip():
            feature_name = f"feature-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        click.echo(f"  ✓ Feature: {feature_name}")
        
        # Step 3: CodeGraph freshness check
        click.echo("\n📌 Step 3: Checking CodeGraph freshness...")
        graph = CodeGraph()
        stats = graph.get_stats()
        
        if stats and stats.get("node_count", 0) > 0:
            if graph.is_stale():
                click.echo("  ⚠️  CodeGraph is stale (> 24 hours old)")
            else:
                click.echo(f"  ✓ CodeGraph current ({stats.get('node_count', 0)} symbols)")
        else:
            click.echo("  ℹ️  CodeGraph empty or first run")
        
        # Step 4: CodeGraph refresh (conditional)
        if force_graph_refresh or not stats or stats.get("node_count", 0) == 0:
            click.echo("\n📌 Step 4: Refreshing CodeGraph...")
            with click.progressbar(length=100, label="  Indexing") as bar:
                count = graph.refresh()
                bar.update(100)
            click.echo(f"  ✓ CodeGraph refreshed ({count} symbols indexed)")
        else:
            logger.info("Step 4: Skipping CodeGraph refresh")
        
        # Step 5: Load context
        if not skip_context:
            click.echo("\n📌 Step 5: Loading context...")
            context = load_context(feature_name=feature_name, layers="all")
            save_session_context(context)
            click.echo("  ✓ Context loaded (user, session, repo layers)")
        else:
            logger.info("Step 5: Skipping context load")
        
        # Step 6: Create feature state tracker
        click.echo("\n📌 Step 6: Creating feature state tracker...")
        feature_state = FeatureState(
            feature_name=feature_name,
            status="pending",
            branch_name=f"feature/{feature_name}",
            created_at=datetime.now()
        )
        save_feature_state(feature_name, feature_state.dict())
        click.echo(f"  ✓ Feature state created")
        
        # Step 7: Report ready status
        click.echo("\n📌 Step 7: Workspace ready for development")
        click.echo()
        click.echo("✅ Ready to proceed:")
        click.echo(f"   • Feature: {feature_name}")
        click.echo(f"   • Branch: {feature_state.branch_name}")
        click.echo(f"   • Context: Loaded and cached")
        click.echo(f"   • CodeGraph: {stats.get('node_count', 0) if stats else 0} symbols")
        click.echo()
        click.echo("Next steps:")
        click.echo("   1. spek plan              # Create feature spec and plan")
        click.echo("   2. spek implement        # Execute tasks")
        click.echo("   3. spek post             # Archive outcomes")
        click.echo()
        
        logger.info(f"Workspace prepared for feature: {feature_name}")
    
    except click.Abort:
        logger.error("Workspace preparation aborted")
        raise
    except Exception as e:
        logger.error(f"Error during workspace preparation: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise
    logger.info("Step 6: Creating feature state tracker...")
    click.echo("  ✓ Feature state tracker created")
    
    # Step 7: Report ready status
    logger.info("Step 7: Reporting ready status...")
    click.echo("\n✓ Workspace prepared for feature development")
    click.echo(f"  Feature: {feature_name}")
    click.echo("  Ready: spek plan, spek context, spek implement")
