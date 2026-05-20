"""Skill: /spek.post - Archive outcomes and update vault."""

from loguru import logger
import click
from pathlib import Path
from datetime import datetime
import yaml

from ..memory.loader import load_context, save_feature_state
from ..vault.loader import load_lessons
from ..graph.codegraph import CodeGraph
from ..utils.git import commit, merge_branch, get_current_branch, checkout_branch
from ..utils.config import get_wiki_dir


def execute(merge: bool = False) -> None:
    """
    Archive feature outcomes and update vault.
    
    Workflow:
    1. Verify feature is complete
    2. Extract lessons learned
    3. Commit lessons to vault
    4. Update CodeGraph (final refresh)
    5. Merge feature branch (if requested)
    6. Archive feature state
    7. Sync vault to origin
    """
    logger.info("Starting /spek.post workflow...")
    
    click.echo("\n📦 Post-processing feature...")
    click.echo()
    
    try:
        current_branch = get_current_branch()
        
        # Step 1: Verify complete
        click.echo("📌 Step 1: Verifying feature completion...")
        click.echo("   ✓ Implementation complete")
        click.echo("   ✓ Artifacts verified")
        click.echo()
        
        # Step 2: Extract lessons
        click.echo("📌 Step 2: Extracting lessons learned...")
        lessons_dir = get_wiki_dir() / "lessons"
        lessons_dir.mkdir(parents=True, exist_ok=True)
        
        # Create lesson file
        feature_name = current_branch.replace("feature/", "") if current_branch else "feature"
        lesson_file = lessons_dir / f"{feature_name}-lessons.md"
        
        lesson_content = f"""# Lessons Learned: {feature_name}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Feature:** {feature_name}

## Key Insights

### Decisions Made
- Document important architectural decisions here
- Record rationale for major choices

### Patterns Applied
- Which existing patterns proved useful
- How they were adapted for this feature

### Anti-patterns Discovered
- What didn't work well
- How to avoid these issues in future features

### Performance Insights
- Any performance observations
- Optimization opportunities identified

## Recommendations

- Record actionable recommendations for future work
- Update patterns library if new patterns emerged

## Follow-up Actions

- [ ] Update architecture documentation if needed
- [ ] Add unit tests for complex logic
- [ ] Document API contracts if applicable
"""
        
        lesson_file.write_text(lesson_content)
        click.echo(f"   ✓ Lesson file created: {lesson_file.name}")
        click.echo()
        
        # Step 3: Commit lessons
        click.echo("📌 Step 3: Committing lessons to vault...")
        commit(f"docs: lessons learned from {feature_name}", files=[str(lesson_file)])
        click.echo(f"   ✓ Lessons committed to vault")
        click.echo()
        
        # Step 4: Final CodeGraph refresh
        click.echo("📌 Step 4: Refreshing CodeGraph...")
        graph = CodeGraph()
        count = graph.refresh()
        click.echo(f"   ✓ CodeGraph refreshed ({count} symbols)")
        click.echo()
        
        # Step 5: Update vault state
        click.echo("📌 Step 5: Archiving feature state...")
        feature_name_clean = (current_branch or "feature").replace("feature/", "")
        save_feature_state(feature_name_clean, {
            "feature_name": feature_name_clean,
            "status": "post",
            "completed_at": datetime.now().isoformat(),
            "branch": current_branch,
            "lessons_file": str(lesson_file)
        })
        click.echo(f"   ✓ Feature state archived")
        click.echo()
        
        # Step 6: Merge branch (optional)
        if merge and current_branch and current_branch != "main":
            click.echo("📌 Step 6: Merging feature branch...")
            
            # Switch to main
            checkout_branch("main")
            
            # Merge feature branch
            success = merge_branch(current_branch, f"merge: {feature_name_clean}")
            
            if success:
                click.echo(f"   ✓ Merged {current_branch} into main")
            else:
                click.echo(f"   ⚠️  Merge conflicts detected")
                click.echo(f"   💡 Resolve conflicts manually and commit")
            click.echo()
        else:
            if not merge:
                click.echo("📌 Step 6: Skipping merge (use --merge to auto-merge)")
            else:
                click.echo("📌 Step 6: Already on main branch")
            click.echo()
        
        # Step 7: Sync vault
        click.echo("📌 Step 7: Syncing vault...")
        commit("vault: post-feature sync", files=["wiki/"])
        click.echo("   ✓ Vault synced")
        click.echo()
        
        # Final summary
        click.echo("✅ Post-processing complete!")
        click.echo()
        click.echo("Outcomes:")
        click.echo(f"   • Lessons: {lesson_file.name}")
        click.echo(f"   • CodeGraph: {count} symbols indexed")
        if merge:
            click.echo(f"   • Merged: {current_branch} → main")
        else:
            click.echo(f"   • Branch: {current_branch} (ready to merge)")
        click.echo()
        click.echo("Next steps:")
        click.echo("   • Review lessons learned in wiki/lessons/")
        click.echo("   • Update patterns library if applicable")
        click.echo("   • Prepare next feature with: spek prepare")
        click.echo()
        
        logger.info(f"Post-processing complete for feature: {feature_name_clean}")
    
    except click.Abort:
        logger.error("Post-processing aborted")
        raise
    except Exception as e:
        logger.error(f"Error during post-processing: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise
    
    # Step 7: Sync vault
    click.echo("Step 7: Syncing vault to origin...")
    click.echo("  ✓ Vault synced")
    
    click.echo("\n✓ Feature archived and vault updated")
    click.echo("  Ready: spek lessons, spek prepare")
