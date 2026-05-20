"""MCP client for agent-side tool invocation."""

from typing import Any, Dict, Optional, List
from loguru import logger


class MCPClient:
    """Client for invoking MCP tools from agents."""
    
    def __init__(self):
        """Initialize MCP client."""
        self.server_name = "codegraph-mcp"
        self.server_version = "0.1.0-alpha.1"
    
    def lookup_symbol(self, symbol: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Look up a symbol definition."""
        from .tools import execute_tool
        return execute_tool("lookup_symbol", symbol=symbol, language=language)
    
    def find_references(self, symbol: str, max_results: int = 10) -> Dict[str, Any]:
        """Find all references to a symbol."""
        from .tools import execute_tool
        return execute_tool("find_references", symbol=symbol, max_results=max_results)
    
    def analyze_impact(self, symbol: str, scope: str = "project") -> Dict[str, Any]:
        """Analyze impact of changing a symbol."""
        from .tools import execute_tool
        return execute_tool("analyze_impact", symbol=symbol, scope=scope)
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get code graph statistics."""
        from .tools import execute_tool
        return execute_tool("get_graph_stats")
    
    def list_symbols_in_file(self, file_path: str, symbol_type: Optional[str] = None) -> Dict[str, Any]:
        """List symbols in a file."""
        from .tools import execute_tool
        return execute_tool("list_symbols_in_file", file_path=file_path, symbol_type=symbol_type)
    
    def find_callers(self, symbol: str, depth: int = 1) -> Dict[str, Any]:
        """Find callers of a function."""
        from .tools import execute_tool
        return execute_tool("find_callers", symbol=symbol, depth=depth)
    
    def search_symbols(self, pattern: str, limit: int = 20) -> Dict[str, Any]:
        """Search for symbols by pattern."""
        from .tools import execute_tool
        return execute_tool("search_symbols", pattern=pattern, limit=limit)
    
    def get_file_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Get dependencies of a file."""
        from .tools import execute_tool
        return execute_tool("get_file_dependencies", file_path=file_path)
    
    def get_definition_location(self, symbol: str) -> Dict[str, Any]:
        """Get definition location of a symbol."""
        from .tools import execute_tool
        return execute_tool("get_definition_location", symbol=symbol)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools."""
        from .tools import TOOL_REGISTRY
        return list(TOOL_REGISTRY.keys())
    
    def invoke_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Invoke a tool by name."""
        from .tools import execute_tool
        return execute_tool(tool_name, **kwargs)


# Global client instance
_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """Get or create the MCP client instance."""
    global _client
    if _client is None:
        _client = MCPClient()
        logger.debug("MCP client initialized")
    return _client
