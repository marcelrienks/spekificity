"""Integration tests for spek init end-to-end flow."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from spekificity.cli import main


def _make_subprocess_mock():
    """Return a mock subprocess.run that always succeeds."""
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = ""
    mock.stderr = ""
    return mock


def _version_run_side(cmd, **kwargs):
    """Version-aware subprocess.run mock for prerequisites._get_version calls."""
    class R:
        returncode = 0
        stdout = (
            "Python 3.11.0" if cmd[0] == "python"
            else "v22.0.0" if cmd[0] == "node"
            else "tool 1.0.0"
        )
    return R()


def _mock_which(present_tools=("python", "uv", "node", "git", "lat", "obsidian", "specify")):
    def which_side(cmd):
        return f"/usr/bin/{cmd}" if cmd in present_tools else None
    return which_side


def _specify_init_side_effect(project_path: Path):
    """Return a run_command side effect that creates .specify/ when specify init is called."""
    def side_effect(cmd, description):
        if cmd == ["specify", "init"]:
            (project_path / ".specify").mkdir(exist_ok=True)
    return side_effect


def _run_invoke(runner, project, integration="claude", script="sh"):
    return runner.invoke(
        main,
        ["init", str(project), "--integration", integration, "--script", script],
    )


class TestInitFlow:
    def test_clean_install_creates_all_artifacts(self, tmp_path):
        runner = CliRunner()
        project = tmp_path / "project"
        project.mkdir()
        (project / ".git" / "hooks").mkdir(parents=True)

        with patch("shutil.which", side_effect=_mock_which()), \
             patch("spekificity.utils.subprocess.run", return_value=_make_subprocess_mock()), \
             patch("spekificity.prerequisites.subprocess.run", side_effect=_version_run_side), \
             patch("spekificity.lat_md.index.run_command"), \
             patch("spekificity.vault.init.run_command"), \
             patch("spekificity.speckit.init.run_command", side_effect=_specify_init_side_effect(project)):
            result = _run_invoke(runner, project)

        assert result.exit_code == 0, result.output
        assert (project / ".spek" / "vault").is_dir()
        assert (project / ".spek" / "memory").is_dir()
        assert (project / ".spek" / "lat").is_dir()
        assert (project / ".spek" / "config.yaml").exists()
        assert (project / ".mcp.json").exists()
        assert (project / ".git" / "hooks" / "post-commit").exists()
        assert (project / ".claude" / "commands").is_dir()
        skill_files = list((project / ".claude" / "commands").glob("spek-*.md"))
        assert len(skill_files) == 7

    def test_idempotent_rerun_exits_0(self, tmp_path):
        runner = CliRunner()
        project = tmp_path / "project2"
        project.mkdir()
        (project / ".git" / "hooks").mkdir(parents=True)

        # First run — creates all artifacts
        with patch("shutil.which", side_effect=_mock_which()), \
             patch("spekificity.utils.subprocess.run", return_value=_make_subprocess_mock()), \
             patch("spekificity.prerequisites.subprocess.run", side_effect=_version_run_side), \
             patch("spekificity.lat_md.index.run_command"), \
             patch("spekificity.vault.init.run_command"), \
             patch("spekificity.speckit.init.run_command", side_effect=_specify_init_side_effect(project)):
            runner.invoke(main, ["init", str(project), "--integration", "claude", "--script", "sh"])

        # Second run — everything should already exist → all [SKIP]
        with patch("shutil.which", side_effect=_mock_which()), \
             patch("spekificity.utils.subprocess.run", return_value=_make_subprocess_mock()), \
             patch("spekificity.prerequisites.subprocess.run", side_effect=_version_run_side), \
             patch("spekificity.lat_md.index.run_command"), \
             patch("spekificity.vault.init.run_command"), \
             patch("spekificity.speckit.init.run_command", side_effect=_specify_init_side_effect(project)):
            result = runner.invoke(main, ["init", str(project), "--integration", "claude", "--script", "sh"])

        assert result.exit_code == 0, result.output
        for line in result.output.strip().splitlines():
            if line.strip():
                assert "[SKIP]" in line, f"Expected [SKIP] but got: {line!r}"

    def test_non_default_path_artifacts_land_under_that_path(self, tmp_path):
        runner = CliRunner()
        project_a = tmp_path / "projectA"
        project_b = tmp_path / "projectB"
        project_a.mkdir()
        project_b.mkdir()
        (project_b / ".git" / "hooks").mkdir(parents=True)

        with patch("shutil.which", side_effect=_mock_which()), \
             patch("spekificity.utils.subprocess.run", return_value=_make_subprocess_mock()), \
             patch("spekificity.prerequisites.subprocess.run", side_effect=_version_run_side), \
             patch("spekificity.lat_md.index.run_command"), \
             patch("spekificity.vault.init.run_command"), \
             patch("spekificity.speckit.init.run_command", side_effect=_specify_init_side_effect(project_b)):
            result = _run_invoke(runner, project_b)

        assert result.exit_code == 0, result.output
        assert (project_b / ".spek" / "config.yaml").exists()
        assert not (project_a / ".spek").exists()
