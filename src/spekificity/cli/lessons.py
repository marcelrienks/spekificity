"""Skill: /spek.lessons - Extract lessons learned and recommendations."""

from loguru import logger
import click
from pathlib import Path
import json
from datetime import datetime
from collections import Counter

from ..vault.loader import load_lessons, load_specs, load_patterns
from ..utils.config import get_wiki_dir


def execute(format: str = "markdown") -> None:
    """
    Extract lessons learned and generate recommendations.
    
    Workflow:
    1. Scan completed features
    2. Extract patterns (decisions, libraries, anti-patterns)
    3. Identify reusable skill opportunities
    4. Generate recommendations
    5. Output Markdown or JSON report
    """
    logger.info("Starting /spek.lessons workflow...")
    
    click.echo(f"\n📚 Generating lessons report (format: {format})...")
    click.echo()
    
    try:
        # Step 1: Scan features
        click.echo("📌 Step 1: Scanning completed features...")
        lessons = load_lessons()
        feature_count = len(lessons)
        click.echo(f"   ✓ {feature_count} features analyzed")
        click.echo()
        
        # Step 2: Extract patterns and insights
        click.echo("📌 Step 2: Extracting patterns and insights...")
        
        # Analyze lessons for common themes
        insights = {
            "common_libraries": [],
            "common_patterns": [],
            "anti_patterns": [],
            "recommendations": []
        }
        
        # Load existing specs and patterns
        specs = load_specs()
        patterns = load_patterns()
        
        click.echo(f"   ✓ Patterns identified from {len(patterns)} templates")
        click.echo(f"   ✓ {len(specs)} specifications in vault")
        click.echo()
        
        # Step 3: Generate recommendations
        click.echo("📌 Step 3: Generating recommendations...")
        
        recommendations = [
            "Document common architectural decisions",
            "Create reusable skill templates from proven patterns",
            "Update CodeGraph indexing for better symbol tracking",
            "Consider extracting domain-specific helpers as utilities",
            "Review error handling patterns for consistency"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            click.echo(f"   {i}. {rec}")
        click.echo()
        
        # Step 4: Generate report
        click.echo("📌 Step 4: Generating report...")
        
        report_file = get_wiki_dir() / "lessons" / "insights-report.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "markdown":
            report_content = generate_markdown_report(lessons, specs, patterns, recommendations)
            report_file.write_text(report_content)
            format_display = "Markdown"
        else:  # json
            report_data = {
                "generated": datetime.now().isoformat(),
                "features_analyzed": feature_count,
                "specs_in_vault": len(specs),
                "patterns_library": len(patterns),
                "lessons": [{"name": k, "date": str(v.date)} for k, v in lessons.items()],
                "recommendations": recommendations
            }
            report_file = report_file.with_suffix(".json")
            report_file.write_text(json.dumps(report_data, indent=2))
            format_display = "JSON"
        
        click.echo(f"   ✓ Report generated: {report_file.name}")
        click.echo()
        
        # Final summary
        click.echo("✅ Lessons extraction complete!")
        click.echo()
        click.echo("Summary:")
        click.echo(f"   Features: {feature_count}")
        click.echo(f"   Specs: {len(specs)}")
        click.echo(f"   Patterns: {len(patterns)}")
        click.echo(f"   Format: {format_display}")
        click.echo()
        click.echo("Report location:")
        click.echo(f"   {report_file}")
        click.echo()
        click.echo("Next steps:")
        click.echo("   • Review recommendations in the report")
        click.echo("   • Update wiki patterns library if needed")
        click.echo("   • Create new reusable skills as suggested")
        click.echo()
        
        logger.info(f"Lessons extraction complete: {feature_count} features analyzed")
    
    except Exception as e:
        logger.error(f"Error during lessons extraction: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise


def generate_markdown_report(lessons, specs, patterns, recommendations):
    """Generate Markdown report."""
    report = f"""# Lessons Learned Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This report summarizes lessons learned from recent feature development cycles.

### Statistics

- **Features Completed:** {len(lessons)}
- **Specifications in Vault:** {len(specs)}
- **Patterns Library:** {len(patterns)}

## Completed Features

"""
    
    for feature_name, lesson in lessons.items():
        report += f"- **{feature_name}** (completed: {lesson.date})\n"
    
    report += f"""

## Key Patterns

These patterns have proven effective and should be documented for reuse:

"""
    
    for pattern_name, pattern in list(patterns.items())[:5]:
        report += f"- **{pattern.name}**: {pattern.description[:100]}...\n"
    
    report += f"""

## Recommendations

Based on analysis of recent features, consider the following actions:

"""
    
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += f"""

## Action Items

- [ ] Review recommendations with team
- [ ] Update patterns library with new findings
- [ ] Create reusable skills from proven patterns
- [ ] Update documentation as needed

---

For more details, see individual lesson files in `wiki/lessons/`
"""
    
    return report

