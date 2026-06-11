"""Unit tests for spekificity.lat_md.mcp_config."""

from __future__ import annotations
import json
from pathlib import Path
import pytest
from spekificity.lat_md.mcp_config import write_mcp_config


class TestWriteMcpConfig:
    def test_creates_config_when_missing(self, tmp_path):
        config_path = tmp_path / ".mcp.json"
        write_mcp_config(config_path, "mcpServers", {}, "claude")
        data = json.loads(config_path.read_text())
        assert "lat" in data["mcpServers"]
        assert data["mcpServers"]["lat"]["command"] == "lat"

    def test_merges_into_existing(self, tmp_path):
        config_path = tmp_path / ".mcp.json"
        config_path.write_text(json.dumps({"mcpServers": {"other": {"command": "foo"}}}))
        write_mcp_config(config_path, "mcpServers", {}, "claude")
        data = json.loads(config_path.read_text())
        assert "other" in data["mcpServers"]
        assert "lat" in data["mcpServers"]

    def test_skip_if_lat_already_present(self, tmp_path):
        config_path = tmp_path / ".mcp.json"
        original = {"mcpServers": {"lat": {"command": "lat", "args": ["mcp"]}}}
        config_path.write_text(json.dumps(original))
        result = write_mcp_config(config_path, "mcpServers", {}, "claude")
        assert result.status == "already_present"

    def test_copilot_extra_fields(self, tmp_path):
        config_path = tmp_path / ".vscode" / "mcp.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        write_mcp_config(config_path, "servers", {"type": "stdio"}, "copilot")
        data = json.loads(config_path.read_text())
        assert data["servers"]["lat"]["type"] == "stdio"

    def test_creates_parent_dirs(self, tmp_path):
        config_path = tmp_path / "nested" / "dir" / "mcp.json"
        write_mcp_config(config_path, "mcpServers", {}, "cursor-agent")
        assert config_path.exists()
