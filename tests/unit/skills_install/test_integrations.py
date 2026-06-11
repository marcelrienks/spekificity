"""Unit tests for spekificity.skills_install.integrations."""

from __future__ import annotations
import pytest
from spekificity.skills_install.integrations import (
    get_skills_config,
    FLAT_INTEGRATIONS,
    INTEGRATION_SKILLS_DIR,
    INTEGRATION_MCP_CONFIG,
)


class TestGetSkillsConfig:
    def test_claude_returns_flat(self):
        skills_dir, use_subfolder = get_skills_config("claude")
        assert skills_dir == ".claude/commands"
        assert use_subfolder is False

    def test_cursor_agent_returns_subfolder(self):
        skills_dir, use_subfolder = get_skills_config("cursor-agent")
        assert skills_dir == ".cursor/skills"
        assert use_subfolder is True

    def test_copilot_returns_flat(self):
        skills_dir, use_subfolder = get_skills_config("copilot")
        assert use_subfolder is False

    def test_generic_returns_flat(self):
        skills_dir, use_subfolder = get_skills_config("generic")
        assert use_subfolder is False

    def test_unknown_returns_fallback_with_subfolder(self):
        skills_dir, use_subfolder = get_skills_config("unknown-integration")
        assert skills_dir == ".agents/skills"
        assert use_subfolder is True

    def test_all_11_known_integrations_present(self):
        known = ["claude", "copilot", "generic", "gemini", "cursor-agent",
                 "windsurf", "cline", "codex", "kiro-cli", "amp", "qwen"]
        for integration in known:
            skills_dir, _ = get_skills_config(integration)
            assert skills_dir != ""

    def test_flat_integrations_membership(self):
        assert "claude" in FLAT_INTEGRATIONS
        assert "copilot" in FLAT_INTEGRATIONS
        assert "generic" in FLAT_INTEGRATIONS
        assert "gemini" not in FLAT_INTEGRATIONS
        assert "cursor-agent" not in FLAT_INTEGRATIONS
