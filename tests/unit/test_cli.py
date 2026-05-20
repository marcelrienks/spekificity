"""Unit tests for CLI module."""

import pytest
from click.testing import CliRunner

from spekificity.cli.main import cli


@pytest.fixture
def cli_runner():
    """CLI runner fixture."""
    return CliRunner()


def test_cli_help(cli_runner):
    """Test CLI help output."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Spekificity" in result.output


def test_cli_version(cli_runner):
    """Test CLI version output."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "Spekificity v" in result.output


def test_prepare_help(cli_runner):
    """Test prepare command help."""
    result = cli_runner.invoke(cli, ["prepare", "--help"])
    assert result.exit_code == 0
    assert "Prepare workspace" in result.output


def test_prepare_basic(cli_runner):
    """Test basic prepare command."""
    result = cli_runner.invoke(cli, ["prepare"])
    assert result.exit_code == 0
    assert "Workspace prepared" in result.output


def test_context_help(cli_runner):
    """Test context command help."""
    result = cli_runner.invoke(cli, ["context", "--help"])
    assert result.exit_code == 0


def test_plan_help(cli_runner):
    """Test plan command help."""
    result = cli_runner.invoke(cli, ["plan", "--help"])
    assert result.exit_code == 0


def test_map_help(cli_runner):
    """Test map command help."""
    result = cli_runner.invoke(cli, ["map", "--help"])
    assert result.exit_code == 0


def test_implement_help(cli_runner):
    """Test implement command help."""
    result = cli_runner.invoke(cli, ["implement", "--help"])
    assert result.exit_code == 0


def test_post_help(cli_runner):
    """Test post command help."""
    result = cli_runner.invoke(cli, ["post", "--help"])
    assert result.exit_code == 0


def test_lessons_help(cli_runner):
    """Test lessons command help."""
    result = cli_runner.invoke(cli, ["lessons", "--help"])
    assert result.exit_code == 0
