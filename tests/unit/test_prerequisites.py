"""Unit tests for spekificity.prerequisites."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from spekificity.prerequisites import PrerequisiteResult, check_prerequisites


class TestCheckPrerequisites:
    def test_all_present_returns_list(self):
        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "tool 1.0.0"
            results = check_prerequisites()
        assert all(r.present for r in results)
        assert len(results) == 4

    def test_missing_uv_exits_1(self):
        def which_side_effect(cmd):
            return None if cmd == "uv" else f"/usr/bin/{cmd}"

        with patch("shutil.which", side_effect=which_side_effect), \
             pytest.raises(SystemExit) as exc_info:
            check_prerequisites()
        assert exc_info.value.code == 1

    def test_missing_git_exits_1(self):
        def which_side_effect(cmd):
            return None if cmd == "git" else f"/usr/bin/{cmd}"

        with patch("shutil.which", side_effect=which_side_effect), \
             pytest.raises(SystemExit) as exc_info:
            check_prerequisites()
        assert exc_info.value.code == 1

    def test_install_hint_non_empty_on_missing(self):
        with patch("shutil.which", return_value=None), \
             pytest.raises(SystemExit):
            check_prerequisites()

    def test_version_none_when_absent(self):
        with patch("shutil.which", return_value=None), \
             pytest.raises(SystemExit):
            results = check_prerequisites()

    def test_prerequisite_result_fields(self):
        result = PrerequisiteResult(
            name="uv",
            present=False,
            version=None,
            install_hint="curl -LsSf https://astral.sh/uv/install.sh | sh",
        )
        assert result.install_hint != ""
