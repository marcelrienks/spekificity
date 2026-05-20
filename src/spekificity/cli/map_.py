"""Skill: /spek.map - Code graph analysis and queries."""

from loguru import logger
import click
from typing import Optional

from ..graph.codegraph import CodeGraph


def execute(
    query: Optional[str] = None,
    symbol: Optional[str] = None,
    references: bool = False,
    impact: bool = False,
    refresh: bool = False,
    output_format: str = "text"
) -> None:
    """
    Analyze code graph and query for symbols, references, and impact.
    
    Args:
        query: Search query (optional)
        symbol: Specific symbol to analyze
        references: Show references to a symbol
        impact: Analyze impact of changes
        refresh: Refresh code graph
        output_format: Output format (text, json, markdown)
    """
    logger.info(f"Starting /spek.map analysis (symbol={symbol}, references={references}, impact={impact})")
    
    try:
        graph = CodeGraph()
        
        # Refresh if requested
        if refresh:
            click.echo("🔄 Refreshing CodeGraph...")
            count = graph.refresh()
            click.echo(f"   ✓ Refreshed: {count} symbols indexed")
            click.echo()
        
        # Show stats
        stats = graph.get_stats()
        click.echo("📊 CodeGraph Status:")
        click.echo(f"   Symbols: {stats.get('node_count', 0)}")
        click.echo(f"   Relations: {stats.get('edge_count', 0)}")
        click.echo(f"   Last refresh: {stats.get('last_refresh', 'never')}")
        click.echo(f"   Database: {stats.get('db_size_mb', 0):.2f} MB")
        click.echo()
        
        # Symbol lookup
        if symbol:
            click.echo(f"🔍 Looking up symbol: {symbol}")
            node = graph.get_symbol(symbol)
            
            if node:
                click.echo(f"   ✓ Found: {node.node_type}")
                click.echo(f"     Name: {node.name}")
                if node.path:
                    click.echo(f"     File: {node.path}")
                if node.line_start:
                    click.echo(f"     Lines: {node.line_start}-{node.line_end}")
                if node.metadata:
                    click.echo(f"     Metadata: {node.metadata}")
                click.echo()
            else:
                click.echo(f"   ⚠️  Symbol not found: {symbol}")
                click.echo()
        
        # Show references
        if references and symbol:
            click.echo(f"🔗 References to {symbol}:")
            refs = graph.get_references(symbol)
            
            if refs:
                for ref in refs:
                    click.echo(f"   • {ref.name} ({ref.node_type})")
                    if ref.path:
                        click.echo(f"     {ref.path}:{ref.line_start}")
            else:
                click.echo("   (No references found)")
            click.echo()
        
        # Impact analysis
        if impact and symbol:
            click.echo(f"⚠️  Impact Analysis: {symbol}")
            analysis = graph.analyze_impact(symbol)
            
            click.echo(f"   Risk Level: {analysis.risk_level.upper()}")
            click.echo(f"   Affected Files: {len(analysis.affected_files)}")
            for file in analysis.affected_files[:5]:
                click.echo(f"     • {file}")
            if len(analysis.affected_files) > 5:
                click.echo(f"     ... and {len(analysis.affected_files) - 5} more")
            
            click.echo(f"   Affected Symbols: {len(analysis.affected_symbols)}")
            for sym in analysis.affected_symbols[:5]:
                click.echo(f"     • {sym}")
            if len(analysis.affected_symbols) > 5:
                click.echo(f"     ... and {len(analysis.affected_symbols) - 5} more")
            
            click.echo(f"   Recommendations:")
            for rec in analysis.recommendations:
                click.echo(f"     • {rec}")
            click.echo()
        
        click.echo("✅ Analysis complete")
        logger.info("CodeGraph analysis complete")
    
    except Exception as e:
        logger.error(f"Error during code graph analysis: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise
