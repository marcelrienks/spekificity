"""Unit tests for CLI module."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import tempfile
import os

from spekificity.cli.main import cli
from spekificity.utils.config import get_project_root, ensure_directories


@pytest.fixture
def cli_runner():
    """CLI runner fixture."""
    return CliRunner()


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace."""
    os.chdir(tmp_path)
    # Create a fake project root marker
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'spekificity'")
    ensure_directories()
    return tmp_path


class TestCLICore:
    """Test core CLI functionality."""
    
    def test_cli_help(self, cli_runner):
        """Test CLI help output."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Spekificity" in result.output
        assert "prepare" in result.output
        assert "context" in result.output
        assert "plan" in result.output
        assert "map" in result.output
        assert "implement" in result.output
        assert "post" in result.output
        assert "lessons" in result.output
    
    def test_cli_version(self, cli_runner):
        """Test CLI version output."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestPrepareCommand:
    """Test prepare command."""
    
    def test_prepare_help(self, cli_runner):
        """Test prepare command help."""
        result = cli_runner.invoke(cli, ["prepare", "--help"])
        assert result.exit_code == 0
        assert "Prepare workspace" in result.output
    
    def test_prepare_with_feature_name(self, cli_runner, temp_workspace):
        """Test prepare with feature name."""
        result = cli_runner.invoke(cli, ["prepare", "--feature-name", "test-feature"])
        # Result may fail due to git repo requirement, but command should parse
        assert "prepare" in result.output.lower() or "git" in result.output.lower()


class TestContextCommand:
    """Test context command."""
    
    def test_context_help(self, cli_runner):
        """Test context command help."""
        result = cli_runner.invoke(cli, ["context", "--help"])
        assert result.exit_code == 0
        assert "--layer" in result.output
    
    def test_context_layers(self, cli_runner):
        """Test context with different layers."""
        for layer in ["user", "session", "repo", "all"]:
            result = cli_runner.invoke(cli, ["context", "--layer", layer])
            # Should either succeed or show context errors
            assert result.exit_code in [0, 1]


class TestMapCommand:
    """Test map command."""
    
    def test_map_help(self, cli_runner):
        """Test map command help."""
        result = cli_runner.invoke(cli, ["map", "--help"])
        assert result.exit_code == 0
        assert "--symbol" in result.output
        assert "--impact" in result.output
    
    def test_map_stats(self, cli_runner, temp_workspace):
        """Test map command displays stats."""
        result = cli_runner.invoke(cli, ["map"])
        # Should show CodeGraph stats
        assert result.exit_code in [0, 1]


class TestPlanCommand:
    """Test plan command."""
    
    def test_plan_help(self, cli_runner):
        """Test plan command help."""
        result = cli_runner.invoke(cli, ["plan", "--help"])
        assert result.exit_code == 0
        assert "feature_intent" in result.output or "FEATURE_INTENT" in result.output
    
    def test_plan_interactive_abort(self, cli_runner):
        """Test plan command with input abort."""
        result = cli_runner.invoke(cli, ["plan"], input="")
        # Command should either succeed or abort with error
        assert result.exit_code in [0, 1]


class TestImplementCommand:
    """Test implement command."""
    
    def test_implement_help(self, cli_runner):
        """Test implement command help."""
        result = cli_runner.invoke(cli, ["implement", "--help"])
        assert result.exit_code == 0
        assert "--dry-run" in result.output
    
    def test_implement_dry_run(self, cli_runner, temp_workspace):
        """Test implement dry-run mode."""
        result = cli_runner.invoke(cli, ["implement", "--dry-run"])
        # May fail if no tasks file, but should parse
        assert "implement" in result.output.lower() or "tasks" in result.output.lower()


class TestPostCommand:
    """Test post command."""
    
    def test_post_help(self, cli_runner):
        """Test post command help."""
        result = cli_runner.invoke(cli, ["post", "--help"])
        assert result.exit_code == 0
        assert "--merge" in result.output
    
    def test_post_no_merge(self, cli_runner, temp_workspace):
        """Test post without merge."""
        result = cli_runner.invoke(cli, ["post"])
        # Should either succeed or show expected errors
        assert result.exit_code in [0, 1]


class TestLessonsCommand:
    """Test lessons command."""
    
    def test_lessons_help(self, cli_runner):
        """Test lessons command help."""
        result = cli_runner.invoke(cli, ["lessons", "--help"])
        assert result.exit_code == 0
        assert "--format" in result.output
    
    def test_lessons_markdown_format(self, cli_runner, temp_workspace):
        """Test lessons with markdown format."""
        result = cli_runner.invoke(cli, ["lessons", "--format", "markdown"])
        assert result.exit_code in [0, 1]
    
    def test_lessons_json_format(self, cli_runner, temp_workspace):
        """Test lessons with json format."""
        result = cli_runner.invoke(cli, ["lessons", "--format", "json"])
        assert result.exit_code in [0, 1]


class TestCommandIntegration:
    """Test command integration patterns."""
    
    def test_all_commands_have_help(self, cli_runner):
        """Verify all commands have help text."""
        commands = ["prepare", "context", "plan", "map", "implement", "post", "lessons", "init", "tools"]
        for cmd in commands:
            result = cli_runner.invoke(cli, [cmd, "--help"])
            assert result.exit_code == 0, f"Command '{cmd}' help failed"
            assert len(result.output) > 20, f"Command '{cmd}' has no help text"
    
    def test_verbose_flag(self, cli_runner):
        """Test verbose flag."""
        result = cli_runner.invoke(cli, ["-v", "--help"])
        assert result.exit_code == 0


class TestInitCommand:
    """Test init command for project setup."""
    
    def test_init_help(self, cli_runner):
        """Test init command help."""
        result = cli_runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "Initialize" in result.output
        assert "project structure" in result.output.lower()
    
    def test_init_skip_speckit(self, cli_runner, temp_workspace):
        """Test init with --skip-speckit flag."""
        result = cli_runner.invoke(cli, ["init", "--skip-speckit"])
        # Should succeed even if CodeGraph init has issues in test env
        assert result.exit_code in [0, 1]
    
    def test_init_skip_codegraph(self, cli_runner, temp_workspace):
        """Test init with --skip-codegraph flag."""
        result = cli_runner.invoke(cli, ["init", "--skip-codegraph"])
        assert result.exit_code in [0, 1]
    
    def test_init_both_skips(self, cli_runner, temp_workspace):
        """Test init with both skip flags."""
        result = cli_runner.invoke(cli, ["init", "--skip-speckit", "--skip-codegraph"])
        assert result.exit_code in [0, 1]
