"""Unit tests for spekificity.lat_md.index."""

from __future__ import annotations
from pathlib import Path
from unittest.mock import patch, call
import pytest
from spekificity.lat_md.index import run_lat_index


class TestRunLatIndex:
    def test_both_commands_called(self, tmp_path):
        with patch("spekificity.lat_md.index.run_command") as mock_run:
            run_lat_index(tmp_path)
        calls = [c[0][0] for c in mock_run.call_args_list]
        assert ["lat", "init"] in calls
        assert ["lat", "init", "--docs"] in calls

    def test_idempotent_when_lat_dir_exists(self, tmp_path):
        lat_dir = tmp_path / ".spek" / "lat"
        lat_dir.mkdir(parents=True)
        with patch("spekificity.lat_md.index.run_command") as mock_run:
            run_lat_index(tmp_path)
        mock_run.assert_not_called()
