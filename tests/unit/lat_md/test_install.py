"""Unit tests for spekificity.lat_md.install."""

from __future__ import annotations
from unittest.mock import patch, MagicMock
import pytest
from spekificity.lat_md.install import install_lat


class TestInstallLat:
    def test_already_present(self):
        with patch("shutil.which", return_value="/usr/local/bin/lat"):
            result = install_lat()
        assert result.status == "already_present"

    def test_absent_runs_npm_install(self):
        with patch("shutil.which", return_value=None), \
             patch("spekificity.utils.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = install_lat()
        assert result.status == "installed"
        call_args = mock_run.call_args[0][0]
        assert "npm" in call_args
        assert "lat.md" in call_args
