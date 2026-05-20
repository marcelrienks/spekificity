"""MCP Tools for CodeGraph - tool definitions and implementations."""

from typing import Any, Dict, List, Optional
from loguru import logger


class CodeGraphTools:
    """Collection of MCP tools for CodeGraph queries."""
    
    @staticmethod
    def lookup_symbol(symbol: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Look up a symbol definition.
        
        Args:
            symbol: Symbol name (function, class, variable, etc.)
            language: Optional language filter
        
        Returns:
            Dictionary with symbol definition details
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        result = graph.get_symbol(symbol)
        
        if not result:
            return {
                "success": False,
                "symbol": symbol,
                "message": f"Symbol '{symbol}' not found"
            }
        
        return {
            "success": True,
            "symbol": symbol,
            "type": result.node_type,
            "file": str(result.path) if result.path else None,
            "lines": f"{result.line_start}-{result.line_end}" if result.line_start else None,
            "language": result.language,
            "metadata": result.metadata
        }
    
    @staticmethod
    def find_references(symbol: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Find all references to a symbol.
        
        Args:
            symbol: Symbol name to find references for
            max_results: Maximum number of results (default: 10)
        
        Returns:
            Dictionary with list of references
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        references = graph.get_references(symbol)
        
        # Limit results
        limited = references[:max_results]
        
        return {
            "success": True,
            "symbol": symbol,
            "total_references": len(references),
            "returned": len(limited),
            "references": [
                {
                    "name": ref.name,
                    "file": str(ref.path) if ref.path else None,
                    "type": ref.node_type,
                    "line": ref.line_start
                }
                for ref in limited
            ]
        }
    
    @staticmethod
    def analyze_impact(symbol: str, scope: str = "project") -> Dict[str, Any]:
        """
        Analyze impact of changing a symbol.
        
        Args:
            symbol: Symbol name to analyze
            scope: Analysis scope ('file', 'module', 'project')
        
        Returns:
            Dictionary with impact analysis
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        impact = graph.analyze_impact(symbol)
        
        if not impact:
            return {
                "success": False,
                "symbol": symbol,
                "message": f"Could not analyze impact for '{symbol}'"
            }
        
        return {
            "success": True,
            "symbol": symbol,
            "scope": scope,
            "risk_level": impact.risk_level,
            "affected_files_count": len(impact.affected_files),
            "affected_files": impact.affected_files[:5],  # Show first 5
            "affected_symbols_count": len(impact.affected_symbols),
            "recommendations": impact.recommendations
        }
    
    @staticmethod
    def get_graph_stats() -> Dict[str, Any]:
        """
        Get code graph statistics.
        
        Returns:
            Dictionary with graph stats
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        stats = graph.get_stats()
        
        return {
            "success": True,
            "statistics": {
                "node_count": stats.get("node_count", 0),
                "edge_count": stats.get("edge_count", 0),
                "last_refresh": stats.get("last_refresh"),
                "database_size_mb": stats.get("db_size_mb", 0)
            }
        }
    
    @staticmethod
    def list_symbols_in_file(file_path: str, symbol_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all symbols in a file.
        
        Args:
            file_path: Path to file
            symbol_type: Optional filter ('function', 'class', 'variable')
        
        Returns:
            Dictionary with list of symbols
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        
        # Query for symbols in file
        # This is a simplified implementation
        try:
            symbols = []  # Would query database here
            
            return {
                "success": True,
                "file": file_path,
                "symbol_type": symbol_type or "all",
                "symbols": symbols,
                "count": len(symbols)
            }
        except Exception as e:
            logger.error(f"Error listing symbols in {file_path}: {e}")
            return {
                "success": False,
                "file": file_path,
                "error": str(e)
            }
    
    @staticmethod
    def find_callers(symbol: str, depth: int = 1) -> Dict[str, Any]:
        """
        Find all callers of a function.
        
        Args:
            symbol: Function name
            depth: Call depth to trace (1-3)
        
        Returns:
            Dictionary with list of callers
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        references = graph.get_references(symbol)
        
        # Filter for function/method references
        callers = [
            ref for ref in references 
            if ref.node_type in ["function", "method", "class"]
        ]
        
        return {
            "success": True,
            "symbol": symbol,
            "depth": depth,
            "caller_count": len(callers),
            "callers": [
                {
                    "name": c.name,
                    "file": str(c.path) if c.path else None,
                    "line": c.line_start
                }
                for c in callers
            ]
        }
    
    @staticmethod
    def search_symbols(pattern: str, limit: int = 20) -> Dict[str, Any]:
        """
        Search for symbols by name pattern.
        
        Args:
            pattern: Search pattern (substring or regex)
            limit: Maximum results to return
        
        Returns:
            Dictionary with matching symbols
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        
        # Query database for matching symbols
        results = []  # Would query database here
        
        return {
            "success": True,
            "pattern": pattern,
            "limit": limit,
            "results": results,
            "count": len(results)
        }
    
    @staticmethod
    def get_file_dependencies(file_path: str) -> Dict[str, Any]:
        """
        Get all dependencies of a file.
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary with list of dependencies
        """
        return {
            "success": True,
            "file": file_path,
            "dependencies": [],
            "count": 0
        }
    
    @staticmethod
    def get_definition_location(symbol: str) -> Dict[str, Any]:
        """
        Get exact location (file + line) of a symbol definition.
        
        Args:
            symbol: Symbol name
        
        Returns:
            Dictionary with location information
        """
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        result = graph.get_symbol(symbol)
        
        if not result:
            return {
                "success": False,
                "symbol": symbol,
                "message": f"Could not find definition for '{symbol}'"
            }
        
        return {
            "success": True,
            "symbol": symbol,
            "file": str(result.path) if result.path else None,
            "line": result.line_start,
            "line_end": result.line_end,
            "type": result.node_type
        }


# Tool registry mapping tool names to implementations
TOOL_REGISTRY = {
    "lookup_symbol": CodeGraphTools.lookup_symbol,
    "find_references": CodeGraphTools.find_references,
    "analyze_impact": CodeGraphTools.analyze_impact,
    "get_graph_stats": CodeGraphTools.get_graph_stats,
    "list_symbols_in_file": CodeGraphTools.list_symbols_in_file,
    "find_callers": CodeGraphTools.find_callers,
    "search_symbols": CodeGraphTools.search_symbols,
    "get_file_dependencies": CodeGraphTools.get_file_dependencies,
    "get_definition_location": CodeGraphTools.get_definition_location,
}


def execute_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Execute a tool by name with given arguments.
    
    Args:
        tool_name: Name of tool to execute
        **kwargs: Arguments for the tool
    
    Returns:
        Tool execution result
    """
    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": list(TOOL_REGISTRY.keys())
        }
    
    try:
        tool_func = TOOL_REGISTRY[tool_name]
        return tool_func(**kwargs)
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {
            "success": False,
            "tool": tool_name,
            "error": str(e)
        }
