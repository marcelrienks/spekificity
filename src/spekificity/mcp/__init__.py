"""Model Context Protocol (MCP) integration for Spekificity.

Exposes CodeGraph and context queries as MCP tools for AI agent consumption.
"""

from .server import CodeGraphMCPServer, get_mcp_server
from .tools import CodeGraphTools, TOOL_REGISTRY, execute_tool

__all__ = [
    "CodeGraphMCPServer",
    "get_mcp_server",
    "CodeGraphTools",
    "TOOL_REGISTRY",
    "execute_tool",
]
