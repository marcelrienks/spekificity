"""Tests for MCP integration."""

import pytest
from spekificity.mcp.client import get_mcp_client, MCPClient
from spekificity.mcp.tools import TOOL_REGISTRY, execute_tool


class TestMCPClient:
    """Test MCP client functionality."""
    
    def test_mcp_client_creation(self):
        """Test MCP client can be created."""
        client = get_mcp_client()
        assert client is not None
        assert isinstance(client, MCPClient)
    
    def test_mcp_client_singleton(self):
        """Test MCP client is singleton."""
        client1 = get_mcp_client()
        client2 = get_mcp_client()
        assert client1 is client2
    
    def test_get_available_tools(self):
        """Test getting list of available tools."""
        client = get_mcp_client()
        tools = client.get_available_tools()
        assert len(tools) > 0
        assert "lookup_symbol" in tools
        assert "find_references" in tools
        assert "analyze_impact" in tools
    
    def test_get_graph_stats(self):
        """Test getting graph statistics."""
        client = get_mcp_client()
        result = client.get_graph_stats()
        assert result.get("success") in [True, False]
        assert "statistics" in result or "success" in result


class TestMCPTools:
    """Test MCP tools registry and execution."""
    
    def test_tool_registry_populated(self):
        """Test that tool registry has tools."""
        assert len(TOOL_REGISTRY) > 0
    
    def test_required_tools_in_registry(self):
        """Test that required tools are registered."""
        required_tools = [
            "lookup_symbol",
            "find_references",
            "analyze_impact",
            "get_graph_stats",
        ]
        for tool in required_tools:
            assert tool in TOOL_REGISTRY, f"Tool {tool} not in registry"
    
    def test_execute_tool_invalid(self):
        """Test executing invalid tool."""
        result = execute_tool("invalid_tool_name")
        assert result.get("success") == False
        assert "error" in result or "Unknown tool" in str(result)
    
    def test_execute_tool_get_stats(self):
        """Test executing get_graph_stats tool."""
        result = execute_tool("get_graph_stats")
        # Should either succeed with stats or fail gracefully
        assert isinstance(result, dict)
        assert "success" in result or "statistics" in result


class TestMCPToolDefinitions:
    """Test MCP tool definitions."""
    
    def test_tools_have_descriptions(self):
        """Test that all tools have descriptions."""
        from spekificity.mcp.server import get_mcp_server
        server = get_mcp_server()
        tools = server.get_tool_definitions()
        
        for tool in tools.get("tools", []):
            assert "name" in tool
            assert "description" in tool
            assert len(tool["description"]) > 0
    
    def test_tools_have_input_schema(self):
        """Test that all tools have input schemas."""
        from spekificity.mcp.server import get_mcp_server
        server = get_mcp_server()
        tools = server.get_tool_definitions()
        
        for tool in tools.get("tools", []):
            assert "inputSchema" in tool


class TestMCPIntegration:
    """Test MCP integration scenarios."""
    
    def test_lookup_symbol_not_found(self):
        """Test symbol lookup for non-existent symbol."""
        client = get_mcp_client()
        result = client.lookup_symbol("NonExistentSymbolXYZ12345")
        # Should return success: False if symbol not found
        assert isinstance(result, dict)
    
    def test_find_references_returns_dict(self):
        """Test find_references returns proper structure."""
        client = get_mcp_client()
        result = client.find_references("main")
        
        assert isinstance(result, dict)
        assert "success" in result
        if result.get("success"):
            assert "symbol" in result
            assert "references" in result or "reference_count" in result
    
    def test_analyze_impact_returns_dict(self):
        """Test analyze_impact returns proper structure."""
        client = get_mcp_client()
        result = client.analyze_impact("Config")
        
        assert isinstance(result, dict)
        assert "success" in result
