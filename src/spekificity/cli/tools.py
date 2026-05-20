"""Skill: /spek.tools - Query code graph via MCP tools."""

from loguru import logger
import click
import json

from ..mcp.client import get_mcp_client


def execute(tool: str = None, symbol: str = None, file: str = None, max_results: int = 10, list_tools: bool = False, format: str = "text") -> None:
    """
    Query CodeGraph via MCP tools.
    
    Examples:
        spek tools --list                           # Show available tools
        spek tools --tool lookup_symbol --symbol UserService
        spek tools --tool find_references --symbol authenticate --max-results 20
        spek tools --tool analyze_impact --symbol Config
        spek tools --tool get_graph_stats
    """
    logger.info("Starting /spek.tools (MCP tool interface)...")
    
    click.echo("\n🔧 CodeGraph MCP Tools")
    click.echo()
    
    client = get_mcp_client()
    
    try:
        # List available tools
        if list_tools:
            click.echo("📚 Available MCP Tools:")
            click.echo()
            tools = client.get_available_tools()
            for i, t in enumerate(tools, 1):
                click.echo(f"  {i}. {t}")
            click.echo()
            click.echo("Examples:")
            click.echo("  spek tools --tool lookup_symbol --symbol UserService")
            click.echo("  spek tools --tool find_references --symbol authenticate")
            click.echo("  spek tools --tool analyze_impact --symbol Config")
            click.echo("  spek tools --tool get_graph_stats")
            click.echo()
            return
        
        # Validate tool selection
        if not tool:
            click.echo("❌ Please specify --tool or use --list to see available tools")
            raise click.Abort()
        
        # Execute tool
        click.echo(f"🔍 Executing: {tool}")
        click.echo()
        
        result = None
        
        if tool == "lookup_symbol":
            if not symbol:
                click.echo("❌ --symbol required for lookup_symbol")
                raise click.Abort()
            result = client.lookup_symbol(symbol)
        
        elif tool == "find_references":
            if not symbol:
                click.echo("❌ --symbol required for find_references")
                raise click.Abort()
            result = client.find_references(symbol, max_results=max_results)
        
        elif tool == "analyze_impact":
            if not symbol:
                click.echo("❌ --symbol required for analyze_impact")
                raise click.Abort()
            result = client.analyze_impact(symbol)
        
        elif tool == "get_graph_stats":
            result = client.get_graph_stats()
        
        elif tool == "list_symbols_in_file":
            if not file:
                click.echo("❌ --file required for list_symbols_in_file")
                raise click.Abort()
            result = client.list_symbols_in_file(file)
        
        elif tool == "find_callers":
            if not symbol:
                click.echo("❌ --symbol required for find_callers")
                raise click.Abort()
            result = client.find_callers(symbol)
        
        else:
            # Generic invocation
            kwargs = {}
            if symbol:
                kwargs["symbol"] = symbol
            if file:
                kwargs["file_path"] = file
            kwargs["max_results"] = max_results
            result = client.invoke_tool(tool, **kwargs)
        
        # Display results
        if result.get("success", False):
            click.echo("✅ Success:")
            click.echo()
            
            if format == "json":
                click.echo(json.dumps(result, indent=2))
            else:
                # Format as readable text/table
                for key, value in result.items():
                    if key != "success":
                        if isinstance(value, dict):
                            click.echo(f"  {key}:")
                            for k, v in value.items():
                                click.echo(f"    {k}: {v}")
                        elif isinstance(value, list):
                            if value and isinstance(value[0], dict):
                                click.echo(f"  {key} ({len(value)} items):")
                                for item in value[:5]:  # Show first 5
                                    click.echo(f"    • {item}")
                            else:
                                click.echo(f"  {key}: {value}")
                        else:
                            click.echo(f"  {key}: {value}")
        else:
            click.echo("❌ Tool execution failed:")
            click.echo(f"  Error: {result.get('error', result.get('message', 'Unknown error'))}")
        
        click.echo()
        
        logger.info(f"Tool execution complete: {tool}")
    
    except click.Abort:
        logger.error("Tool execution aborted")
        raise
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise
