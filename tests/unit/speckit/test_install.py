"""Unit tests for spekificity.speckit.install."""

from __future__ import annotations
from unittest.mock import patch
import pytest
from spekificity.speckit.install import install_speckit


class TestInstallSpeckit:
    def test_already_present(self):
        with patch("shutil.which", return_value="/usr/local/bin/specify"):
            result = install_speckit()
        assert result.status == "already_present"

    def test_absent_runs_uv_tool_install(self):
        with patch("shutil.which", return_value=None), \
             patch("spekificity.utils.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = install_speckit()
        assert result.status == "installed"
        call_args = mock_run.call_args[0][0]
        assert "uv" in call_args
        assert "specify-cli" in call_args
