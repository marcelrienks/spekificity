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

    def test_cline_writes_flat_key(self, tmp_path):
        config_path = tmp_path / ".vscode" / "settings.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        write_mcp_config(config_path, "cline.mcpServers", {}, "cline", flat_key=True)
        data = json.loads(config_path.read_text())
        assert "cline.mcpServers" in data          # literal flat key
        assert "cline" not in data                 # NOT nested {"cline": {...}}
        assert "lat" in data["cline.mcpServers"]
        assert data["cline.mcpServers"]["lat"]["command"] == "lat"

    def test_cline_flat_key_idempotent(self, tmp_path):
        config_path = tmp_path / ".vscode" / "settings.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        write_mcp_config(config_path, "cline.mcpServers", {}, "cline", flat_key=True)
        result = write_mcp_config(config_path, "cline.mcpServers", {}, "cline", flat_key=True)
        assert result.status == "already_present"

    def test_cline_flat_key_preserves_existing_entries(self, tmp_path):
        config_path = tmp_path / ".vscode" / "settings.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {"cline.mcpServers": {"other": {"command": "other"}}, "editor.fontSize": 14}
        config_path.write_text(json.dumps(existing))
        write_mcp_config(config_path, "cline.mcpServers", {}, "cline", flat_key=True)
        data = json.loads(config_path.read_text())
        assert "other" in data["cline.mcpServers"]
        assert "lat" in data["cline.mcpServers"]
        assert data["editor.fontSize"] == 14
