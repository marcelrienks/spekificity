"""Unit tests for spekificity.lat_md.index."""

from __future__ import annotations
from pathlib import Path
from unittest.mock import patch, call
import pytest
from spekificity.lat_md.index import run_lat_index


class TestRunLatIndex:
    def test_lat_init_called(self, tmp_path):
        with patch("spekificity.lat_md.index.run_command") as mock_run:
            run_lat_index(tmp_path)
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0][:2] == ["lat", "init"]

    def test_idempotent_when_lat_md_dir_exists(self, tmp_path):
        lat_md_dir = tmp_path / ".spek" / "lat.md"
        lat_md_dir.mkdir(parents=True)
        with patch("spekificity.lat_md.index.run_command") as mock_run:
            run_lat_index(tmp_path)
        mock_run.assert_not_called()
