"""Unit tests for spekificity.vault.install."""

from __future__ import annotations
from unittest.mock import patch
import pytest
from spekificity.vault.install import install_obsidian


class TestInstallObsidian:
    def test_already_in_path(self):
        with patch("shutil.which", return_value="/usr/local/bin/obsidian"):
            result = install_obsidian()
        assert result.status == "already_present"

    def test_darwin_installs_via_brew_then_present(self):
        call_count = {"n": 0}
        def which_side(cmd):
            call_count["n"] += 1
            if cmd == "obsidian" and call_count["n"] == 1:
                return None
            return "/usr/local/bin/obsidian"

        with patch("shutil.which", side_effect=which_side), \
             patch("sys.platform", "darwin"), \
             patch("spekificity.utils.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = install_obsidian()
        assert result.status == "installed"

    def test_darwin_needs_user_action_when_cli_not_registered(self):
        with patch("shutil.which", return_value=None), \
             patch("sys.platform", "darwin"), \
             patch("spekificity.utils.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = install_obsidian()
        assert result.status == "needs_user_action"
        assert result.exit_code == 2

    def test_linux_returns_skipped(self):
        with patch("shutil.which", return_value=None), \
             patch("sys.platform", "linux"):
            result = install_obsidian()
        assert result.status == "skipped"

    def test_win32_installs_via_winget(self):
        call_count = {"n": 0}
        def which_side(cmd):
            call_count["n"] += 1
            if cmd == "obsidian" and call_count["n"] == 1:
                return None
            return "C:\\obsidian.exe"

        with patch("shutil.which", side_effect=which_side), \
             patch("sys.platform", "win32"), \
             patch("spekificity.utils.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            result = install_obsidian()
        assert result.status == "installed"
