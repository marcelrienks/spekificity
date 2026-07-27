"""Integration → skills directory and MCP config mappings."""

from __future__ import annotations

from typing import Any

FLAT_INTEGRATIONS: set[str] = {"claude", "generic"}

INTEGRATION_SKILLS_DIR: dict[str, str] = {
    "claude": ".claude/commands",
    "copilot": ".github/skills",
    "generic": ".agents/skills",
    "gemini": ".gemini/skills",
    "cursor-agent": ".cursor/skills",
    "windsurf": ".windsurf/skills",
    "cline": ".cline/skills",
    "codex": ".codex/skills",
    "kiro-cli": ".kiro/skills",
    "amp": ".amp/skills",
    "qwen": ".qwen/skills",
}

# (config_file, servers_key, extra_fields, flat_key)
# flat_key=True: servers_key is a literal JSON key (e.g. VS Code "cline.mcpServers"),
#                NOT a dot-separated path into nested objects.
INTEGRATION_MCP_CONFIG: dict[str, tuple[str, str, dict[str, Any], bool]] = {
    "claude": (".mcp.json", "mcpServers", {}, False),
    "cursor-agent": (".cursor/mcp.json", "mcpServers", {}, False),
    "copilot": (".vscode/mcp.json", "servers", {"type": "stdio"}, False),
    "windsurf": (".windsurf/mcp.json", "mcpServers", {}, False),
    "cline": (".vscode/settings.json", "cline.mcpServers", {}, True),
    "gemini": (".gemini/settings.json", "mcpServers", {}, False),
    "codex": (".codex/mcp.json", "mcpServers", {}, False),
    "kiro-cli": (".kiro/mcp.json", "mcpServers", {}, False),
    "amp": (".amp/mcp.json", "mcpServers", {}, False),
    "qwen": (".qwen/mcp.json", "mcpServers", {}, False),
}

_FALLBACK_DIR = ".agents/skills"


def get_skills_config(integration: str) -> tuple[str, bool]:
    """Return (skills_dir, use_subfolder) for the given integration.

    use_subfolder=True means copy to <skills_dir>/spek-NAME/SKILL.md
    use_subfolder=False means copy to <skills_dir>/spek-NAME.md
    """
    skills_dir = INTEGRATION_SKILLS_DIR.get(integration, _FALLBACK_DIR)
    use_subfolder = integration not in FLAT_INTEGRATIONS
    return skills_dir, use_subfolder
