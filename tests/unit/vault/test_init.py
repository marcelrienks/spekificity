"""Unit tests for spekificity.vault.init."""

from __future__ import annotations
from pathlib import Path
from unittest.mock import patch, call
import pytest
from spekificity.vault.init import init_vault


class TestInitVault:
    def test_calls_obsidian_open_vault(self, tmp_path):
        with patch("spekificity.vault.init.run_command") as mock_run:
            init_vault(tmp_path)
        assert mock_run.called
        first_call_args = mock_run.call_args_list[0][0][0]
        assert "obsidian" in first_call_args
        assert "open-vault" in first_call_args

    def test_vault_path_passed_as_named_arg(self, tmp_path):
        with patch("spekificity.vault.init.run_command") as mock_run:
            init_vault(tmp_path)
        first_call_args = mock_run.call_args_list[0][0][0]
        expected_vault = str(tmp_path / ".spek" / "vault")
        assert f"path={expected_vault}" in first_call_args

    def test_creates_vault_files_via_obsidian_cli(self, tmp_path):
        with patch("spekificity.vault.init.run_command") as mock_run:
            init_vault(tmp_path)
        all_cmds = [call[0][0] for call in mock_run.call_args_list]
        create_cmds = [cmd for cmd in all_cmds if "create" in cmd]
        assert len(create_cmds) == 3
        flat = [item for cmd in create_cmds for item in cmd]
        assert "file=decisions" in flat
        assert "file=patterns" in flat
        assert "path=lessons/.keep" in flat
        assert "vault=vault" in flat

    def test_skips_when_sentinel_exists(self, tmp_path):
        vault_path = tmp_path / ".spek" / "vault"
        vault_path.mkdir(parents=True, exist_ok=True)
        (vault_path / ".initialized").touch()
        with patch("spekificity.vault.init.run_command") as mock_run:
            init_vault(tmp_path)
        mock_run.assert_not_called()
