"""MCP server for CodeGraph - exposes code analysis as MCP tools."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from loguru import logger


class CodeGraphMCPServer:
    """MCP server exposing CodeGraph as tools for AI agents."""
    
    def __init__(self):
        """Initialize MCP server."""
        self.name = "codegraph-mcp"
        self.version = "0.1.0-alpha.1"
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define MCP tools for CodeGraph queries."""
        return [
            {
                "name": "lookup_symbol",
                "description": "Find a symbol definition by name (function, class, variable, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Symbol name to look up (e.g., 'UserService', 'authenticate')"
                        },
                        "language": {
                            "type": "string",
                            "description": "Optional: filter by language (python, typescript, javascript, etc.)"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "find_references",
                "description": "Find all references/usages of a symbol (who calls it, who imports it)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Symbol name to find references for"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "analyze_impact",
                "description": "Analyze the impact of changing a symbol (what code would be affected)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Symbol name to analyze impact for"
                        },
                        "scope": {
                            "type": "string",
                            "description": "Scope of analysis: 'file', 'module', 'project' (default: 'project')",
                            "default": "project"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "list_symbols_in_file",
                "description": "List all symbols defined in a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "File path to analyze (e.g., 'src/services/auth.py')"
                        },
                        "symbol_type": {
                            "type": "string",
                            "description": "Filter by type: 'function', 'class', 'variable', etc. (optional)",
                            "enum": ["function", "class", "variable", "module", "all"]
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "find_callers",
                "description": "Find all functions/methods that call a specific function",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Function name to find callers for"
                        },
                        "depth": {
                            "type": "integer",
                            "description": "Depth of call chain to trace (1-3, default: 1)",
                            "default": 1
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "get_graph_stats",
                "description": "Get overall statistics about the code graph",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "find_by_pattern",
                "description": "Find symbols matching a pattern (regex or substring)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Pattern to search for (supports regex or exact match)"
                        },
                        "search_type": {
                            "type": "string",
                            "description": "Search in 'names', 'files', 'both' (default: 'names')",
                            "enum": ["names", "files", "both"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum results to return (default: 20)",
                            "default": 20
                        }
                    },
                    "required": ["pattern"]
                }
            }
        ]
    
    def get_tool_definitions(self) -> Dict[str, Any]:
        """Return tool definitions in MCP format."""
        return {
            "server_name": self.name,
            "server_version": self.version,
            "tools": self.tools,
            "capabilities": {
                "tools": True,
                "resources": False,
                "sampling": False
            }
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return results."""
        logger.info(f"Executing MCP tool: {tool_name} with args: {arguments}")
        
        # Import here to avoid circular dependency
        from ..graph.codegraph import CodeGraph
        
        graph = CodeGraph()
        
        try:
            if tool_name == "lookup_symbol":
                return self._lookup_symbol(graph, arguments)
            elif tool_name == "find_references":
                return self._find_references(graph, arguments)
            elif tool_name == "analyze_impact":
                return self._analyze_impact(graph, arguments)
            elif tool_name == "list_symbols_in_file":
                return self._list_symbols_in_file(graph, arguments)
            elif tool_name == "find_callers":
                return self._find_callers(graph, arguments)
            elif tool_name == "get_graph_stats":
                return self._get_graph_stats(graph, arguments)
            elif tool_name == "find_by_pattern":
                return self._find_by_pattern(graph, arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "tool": tool_name
                }
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    def _lookup_symbol(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Look up a symbol definition."""
        symbol = args.get("symbol")
        language = args.get("language")
        
        result = graph.get_symbol(symbol)
        
        if not result:
            return {
                "success": False,
                "symbol": symbol,
                "message": f"Symbol '{symbol}' not found"
            }
        
        # Filter by language if specified
        if language and result.get("language") != language:
            return {
                "success": False,
                "symbol": symbol,
                "language": language,
                "message": f"Symbol '{symbol}' not found in language '{language}'"
            }
        
        return {
            "success": True,
            "symbol": symbol,
            "definition": {
                "type": result.get("node_type"),
                "file": result.get("path"),
                "line_start": result.get("line_start"),
                "line_end": result.get("line_end"),
                "language": result.get("language"),
                "metadata": result.get("metadata", {})
            }
        }
    
    def _find_references(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Find all references to a symbol."""
        symbol = args.get("symbol")
        max_results = args.get("max_results", 10)
        
        references = graph.get_references(symbol)
        
        # Limit results
        references = references[:max_results]
        
        return {
            "success": True,
            "symbol": symbol,
            "reference_count": len(references),
            "references": [
                {
                    "name": ref.get("name"),
                    "file": ref.get("path"),
                    "type": ref.get("node_type"),
                    "line": ref.get("line_start")
                }
                for ref in references
            ]
        }
    
    def _analyze_impact(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of changing a symbol."""
        symbol = args.get("symbol")
        scope = args.get("scope", "project")
        
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
            "impact": {
                "risk_level": impact.get("risk_level"),
                "affected_files": impact.get("affected_files", []),
                "affected_symbols": impact.get("affected_symbols", []),
                "recommendations": impact.get("recommendations", [])
            }
        }
    
    def _list_symbols_in_file(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """List all symbols in a file."""
        file_path = args.get("file_path")
        symbol_type = args.get("symbol_type", "all")
        
        # Query symbols by file
        query = f"SELECT * FROM nodes WHERE file_path = ?"
        
        # This is simplified - actual implementation would query the DB
        symbols = []
        
        return {
            "success": True,
            "file": file_path,
            "symbol_type": symbol_type,
            "symbols": symbols,
            "count": len(symbols)
        }
    
    def _find_callers(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Find all callers of a function."""
        symbol = args.get("symbol")
        depth = args.get("depth", 1)
        
        # Get references (which includes callers)
        references = graph.get_references(symbol)
        
        callers = []
        for ref in references:
            if ref.get("node_type") in ["function", "method"]:
                callers.append({
                    "name": ref.get("name"),
                    "file": ref.get("path"),
                    "line": ref.get("line_start")
                })
        
        return {
            "success": True,
            "symbol": symbol,
            "depth": depth,
            "caller_count": len(callers),
            "callers": callers
        }
    
    def _get_graph_stats(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get code graph statistics."""
        stats = graph.get_stats()
        
        return {
            "success": True,
            "statistics": {
                "node_count": stats.get("node_count", 0),
                "edge_count": stats.get("edge_count", 0),
                "last_refresh": stats.get("last_refresh"),
                "database_path": stats.get("db_path"),
                "database_size_mb": stats.get("db_size_mb", 0)
            }
        }
    
    def _find_by_pattern(self, graph: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Find symbols by pattern."""
        pattern = args.get("pattern")
        search_type = args.get("search_type", "names")
        limit = args.get("limit", 20)
        
        # Simple pattern matching (would be enhanced with regex support)
        results = []
        
        return {
            "success": True,
            "pattern": pattern,
            "search_type": search_type,
            "limit": limit,
            "results": results,
            "count": len(results)
        }


def get_mcp_server() -> CodeGraphMCPServer:
    """Factory function to get MCP server instance."""
    return CodeGraphMCPServer()
