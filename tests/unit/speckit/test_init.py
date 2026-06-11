"""Unit tests for spekificity.speckit.init."""

from __future__ import annotations
from pathlib import Path
from unittest.mock import patch
import pytest
from spekificity.speckit.init import run_specify_init


class TestRunSpecifyInit:
    def test_skips_when_specify_dir_exists(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        with patch("spekificity.speckit.init.run_command") as mock_run:
            run_specify_init(tmp_path, "claude")
        mock_run.assert_not_called()

    def test_runs_specify_init_when_dir_absent(self, tmp_path):
        with patch("spekificity.speckit.init.run_command") as mock_run:
            run_specify_init(tmp_path, "claude")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "specify" in args
        assert "init" in args

    def test_passes_integration_flag(self, tmp_path):
        with patch("spekificity.speckit.init.run_command") as mock_run:
            run_specify_init(tmp_path, "cursor-agent")
        args = mock_run.call_args[0][0]
        assert "--integration" in args
        assert "cursor-agent" in args
