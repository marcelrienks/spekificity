"""Unit tests for spekificity.prerequisites."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from spekificity.prerequisites import PrerequisiteResult, check_prerequisites


class TestCheckPrerequisites:
    def test_all_present_returns_list(self):
        def run_side(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = "Python 3.11.0" if cmd[0] == "python" else "v22.0.0" if cmd[0] == "node" else "tool 1.0.0"
            return R()

        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run", side_effect=run_side):
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

    def test_python_version_too_low_exits_1(self):
        with patch("shutil.which", return_value="/usr/bin/python"), \
             patch("subprocess.run") as mock_run, \
             pytest.raises(SystemExit) as exc_info:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Python 3.10.0"
            check_prerequisites()
        assert exc_info.value.code == 1

    def test_node_version_too_low_exits_1(self):
        def which_side(cmd):
            return f"/usr/bin/{cmd}"

        def run_side(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = "v18.0.0" if cmd[0] == "node" else "tool 1.0.0"
            return R()

        with patch("shutil.which", side_effect=which_side), \
             patch("subprocess.run", side_effect=run_side), \
             pytest.raises(SystemExit) as exc_info:
            check_prerequisites()
        assert exc_info.value.code == 1

    def test_python_version_ok_passes(self):
        def run_side(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = "Python 3.11.0" if cmd[0] == "python" else "v22.0.0" if cmd[0] == "node" else "tool 1.0.0"
            return R()

        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run", side_effect=run_side):
            results = check_prerequisites()
        assert all(r.present for r in results)

    def test_node_version_ok_passes(self):
        def run_side(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = "v22.0.0" if cmd[0] == "node" else "Python 3.11.0" if cmd[0] == "python" else "tool 1.0.0"
            return R()

        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run", side_effect=run_side):
            results = check_prerequisites()
        assert all(r.present for r in results)

    def test_not_in_git_repo_exits_1(self):
        def run_side(cmd, **kwargs):
            class R:
                pass
            r = R()
            if cmd[0] == "git" and len(cmd) > 1 and cmd[1] == "rev-parse":
                r.returncode = 1
                r.stdout = ""
            elif cmd[0] == "python":
                r.returncode = 0
                r.stdout = "Python 3.11.0"
            elif cmd[0] == "node":
                r.returncode = 0
                r.stdout = "v22.0.0"
            else:
                r.returncode = 0
                r.stdout = "tool 1.0.0"
            return r

        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run", side_effect=run_side), \
             pytest.raises(SystemExit) as exc_info:
            check_prerequisites()
        assert exc_info.value.code == 1

    def test_valid_git_repo_passes(self):
        def run_side(cmd, **kwargs):
            class R:
                returncode = 0
                stdout = "Python 3.11.0" if cmd[0] == "python" else "v22.0.0" if cmd[0] == "node" else ".git"
            return R()

        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch("subprocess.run", side_effect=run_side):
            results = check_prerequisites()
        assert len(results) == 4
