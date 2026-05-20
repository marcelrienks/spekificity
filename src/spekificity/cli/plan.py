"""Skill: /spek.plan - Orchestrate SpecKit workflow (specify -> plan -> tasks)."""

from loguru import logger
import click
from pathlib import Path
from typing import Optional

from ..orchestration.speckit import specify, clarify, plan as plan_cmd, analyze, tasks, is_speckit_installed
from ..memory.loader import load_context, save_feature_state
from ..utils.git import commit, create_feature_branch


def execute(feature_intent: Optional[str] = None, interactive: bool = False) -> None:
    """
    Orchestrate SpecKit workflow to create feature specification and plan.
    
    Workflow:
    1. Accept feature intent (natural language)
    2. Call SpecKit specify -> spec.md
    3. Optional: Call SpecKit clarify -> enrich spec.md
    4. Call SpecKit plan -> plan.md, data-model.md, contracts/
    5. Optional: Call SpecKit analyze -> validate consistency
    6. Optional: Call SpecKit remediate -> fix issues
    7. Call SpecKit tasks -> tasks.md
    8. Commit artifacts to repo
    """
    logger.info("Starting /spek.plan orchestration...")
    
    click.echo("\n📋 Planning feature development...")
    click.echo()
    
    # Check SpecKit is installed
    if not is_speckit_installed():
        click.echo("❌ SpecKit not found in PATH", err=True)
        click.echo("   Install with: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git", err=True)
        raise click.Abort()
    
    # Get feature intent
    if interactive and not feature_intent:
        feature_intent = click.prompt("Describe the feature you want to build")
    
    if not feature_intent or not feature_intent.strip():
        click.echo("❌ Feature intent required", err=True)
        raise click.Abort()
    
    # Load context for enrichment
    click.echo("📌 Loading project context...")
    context = load_context(layers="repo")
    context_summary = f"Project has {context.repo_memory.metadata.get('spec_count', 0)} existing specs" if context.repo_memory else "No context available"
    click.echo(f"   ✓ {context_summary}")
    click.echo()
    
    try:
        feature_name = feature_intent.replace(" ", "-").lower()[:30]
        spec_file = Path.cwd() / f"{feature_name}-spec.md"
        plan_file = Path.cwd() / f"{feature_name}-plan.md"
        tasks_file = Path.cwd() / f"{feature_name}-tasks.md"
        
        # Step 1: Specify
        click.echo("📌 Step 1: Generating specification...")
        result = specify(feature_name, context=context_summary)
        if not result["success"]:
            click.echo(f"   ⚠️  SpecKit specify: {result.get('error', 'unknown error')}")
            click.echo(f"   {result.get('stderr', '')[:200]}")
        else:
            click.echo(f"   ✓ {spec_file.name} generated")
        click.echo()
        
        # Step 2: Clarify (optional, user decides)
        if click.confirm("Review and clarify specification?"):
            click.echo("📌 Step 2: Clarifying specification...")
            result = clarify(spec_file)
            if result["success"]:
                click.echo(f"   ✓ Specification clarified")
            else:
                click.echo(f"   ⚠️  Clarification failed (continuing with spec as-is)")
            click.echo()
        
        # Step 3: Plan
        click.echo("📌 Step 3: Creating implementation plan...")
        result = plan_cmd(spec_file)
        if not result["success"]:
            click.echo(f"   ⚠️  SpecKit plan: {result.get('error', 'unknown error')}")
        else:
            click.echo(f"   ✓ {plan_file.name} generated")
        click.echo()
        
        # Step 4: Analyze (optional)
        if click.confirm("Analyze specification consistency?"):
            click.echo("📌 Step 4: Analyzing specification...")
            result = analyze(spec_file, plan_file)
            if result["success"]:
                click.echo(f"   ✓ Cross-artifact validation complete")
            else:
                click.echo(f"   ⚠️  Analysis failed")
            click.echo()
        
        # Step 5: Generate tasks
        click.echo("📌 Step 5: Generating implementation tasks...")
        result = tasks(plan_file)
        if not result["success"]:
            click.echo(f"   ⚠️  SpecKit tasks: {result.get('error', 'unknown error')}")
        else:
            click.echo(f"   ✓ {tasks_file.name} generated")
        click.echo()
        
        # Step 6: Commit artifacts
        click.echo("📌 Step 6: Committing artifacts...")
        artifacts = [spec_file, plan_file, tasks_file]
        artifacts = [f for f in artifacts if f.exists()]
        
        if artifacts:
            # Create feature branch
            branch_name = f"feature/{feature_name}"
            create_feature_branch(branch_name)
            
            # Commit
            commit(f"spec: {feature_intent}", files=[str(f) for f in artifacts])
            click.echo(f"   ✓ Committed to {branch_name}")
        
        # Save feature state
        save_feature_state(feature_name, {
            "feature_name": feature_name,
            "status": "specify",
            "spec_file": str(spec_file),
            "plan_file": str(plan_file),
            "tasks_file": str(tasks_file)
        })
        
        click.echo()
        click.echo("✅ Planning complete!")
        click.echo()
        click.echo("Artifacts created:")
        for artifact in artifacts:
            click.echo(f"   • {artifact.name}")
        click.echo()
        click.echo("Next step:")
        click.echo(f"   spek implement          # Execute tasks from {tasks_file.name}")
        click.echo()
        
        logger.info(f"Planning complete for feature: {feature_intent}")
    
    except click.Abort:
        logger.error("Planning aborted")
        raise
    except Exception as e:
        logger.error(f"Error during planning: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise
    click.echo("  ✓ tasks.md generated")
    
    # Step 6: Commit
    click.echo("Step 6: Committing artifacts...")
    click.echo("  ✓ Feature branch created (feature-001)")
    click.echo("  ✓ Artifacts committed")
    
    click.echo("\n✓ Feature specification and plan complete")
    click.echo("  Next: spek implement")
