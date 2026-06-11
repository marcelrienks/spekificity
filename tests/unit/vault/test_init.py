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
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "obsidian" in args
        assert "open-vault" in args

    def test_vault_path_passed_correctly(self, tmp_path):
        with patch("spekificity.vault.init.run_command") as mock_run:
            init_vault(tmp_path)
        args = mock_run.call_args[0][0]
        expected_vault = str(tmp_path / ".spek" / "vault")
        assert expected_vault in args
