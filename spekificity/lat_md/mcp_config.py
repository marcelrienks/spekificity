"""Write lat MCP server config entry."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class McpConfigResult:
    integration: str
    config_file: Path | None
    status: str  # "written" | "already_present" | "skipped" | "printed_instructions"


def write_mcp_config(
    config_path: Path,
    servers_key: str,
    extra_fields: dict[str, Any],
    integration: str,
    flat_key: bool = False,
) -> McpConfigResult:
    """Merge lat entry into MCP config. Skip if already present. Create file if missing.

    flat_key=True: servers_key is a literal JSON key (VS Code dot-notation like
    "cline.mcpServers"), not a path into nested objects.
    """
    from spekificity.utils import print_status

    config: dict[str, Any] = {}
    if config_path.exists():
        config = json.loads(config_path.read_text())

    if flat_key:
        servers = config.setdefault(servers_key, {})
    else:
        # Navigate dot-separated path (e.g. "mcpServers" or future nested keys)
        keys = servers_key.split(".")
        node = config
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        servers = node.setdefault(keys[-1], {})

    was_present = "lat" in servers

    entry: dict[str, Any] = {"command": "lat", "args": ["mcp"]}
    entry.update(extra_fields)
    servers["lat"] = entry
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))
    action = "updated" if was_present else "written"
    print_status("OK", f"lat MCP entry {action} to {config_path}")
    return McpConfigResult(integration=integration, config_file=config_path, status="written")


def print_mcp_instructions() -> None:
    """Print manual MCP config instructions for generic/unknown integrations."""
    from spekificity.utils import print_status
    print_status("WARN", "lat.md MCP server not auto-configured for this integration.")
    print("Add the following to your agent's MCP config manually:")
    print()
    print("  server name: lat")
    print("  command:     lat")
    print("  args:        mcp")
    print("  type:        stdio")
