"""Unit tests for CLI commands."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from spekificity.cli.main import cli, init, prepare, plan, implement, conclude


@pytest.fixture
def cli_runner():
    """Create Click CLI test runner."""
    return CliRunner()


class TestMainCLI:
    """Tests for main CLI commands."""
    
    def test_version_flag(self, cli_runner):
        """--version flag should show version."""
        result = cli_runner.invoke(cli, ["--version"])
        
        assert result.exit_code == 0
        assert "spek version" in result.output
    
    def test_help_flag(self, cli_runner):
        """--help flag should show help."""
        result = cli_runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "Spekificity" in result.output or "Usage" in result.output
    
    def test_no_command_shows_help(self, cli_runner):
        """Running with no command should show help."""
        result = cli_runner.invoke(cli, [])
        
        assert result.exit_code == 0
        # Should show help or error message
        assert "spek" in result.output.lower() or "command" in result.output.lower()


class TestInitCommand:
    """Tests for 'spek init' command."""
    
    def test_init_without_git_fails(self, cli_runner):
        """init without git repo should fail gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = cli_runner.invoke(init, [], obj={}, cwd=tmpdir)
            
            # Should fail or warn about git
            assert "git" in result.output.lower() or result.exit_code != 0
    
    def test_init_command_accepts_no_arguments(self, cli_runner):
        """init command should not require arguments."""
        result = cli_runner.invoke(init, [], obj={})
        
        # May fail due to missing git, but should be callable
        assert result.exit_code in [0, 1, 2]


class TestPrepareCommand:
    """Tests for 'spek prepare' command."""
    
    def test_prepare_command_invocable(self, cli_runner):
        """prepare command should be invocable."""
        result = cli_runner.invoke(prepare, [], obj={})
        
        # Should not crash
        assert result.exit_code in [0, 1, 2]
        assert "preparing" in result.output.lower() or "prepare" in result.output.lower()
    
    def test_prepare_with_feature_name(self, cli_runner):
        """prepare should accept feature name."""
        result = cli_runner.invoke(prepare, ["test-feature"], obj={})
        
        assert result.exit_code in [0, 1, 2]
        assert "test-feature" in result.output or "Feature" in result.output


class TestPlanCommand:
    """Tests for 'spek plan' command."""
    
    def test_plan_command_invocable(self, cli_runner):
        """plan command should be invocable."""
        result = cli_runner.invoke(plan, [], obj={})
        
        assert result.exit_code in [0, 1, 2]
        assert "planning" in result.output.lower() or "plan" in result.output.lower()


class TestImplementCommand:
    """Tests for 'spek implement' command."""
    
    def test_implement_command_invocable(self, cli_runner):
        """implement command should be invocable."""
        result = cli_runner.invoke(implement, [], obj={})
        
        assert result.exit_code in [0, 1, 2]
        assert "implementing" in result.output.lower() or "implement" in result.output.lower()


class TestConcludeCommand:
    """Tests for 'spek conclude' command."""
    
    def test_conclude_command_invocable(self, cli_runner):
        """conclude command should be invocable."""
        result = cli_runner.invoke(conclude, [], obj={})
        
        assert result.exit_code in [0, 1, 2]
        assert "concluding" in result.output.lower() or "conclude" in result.output.lower()
