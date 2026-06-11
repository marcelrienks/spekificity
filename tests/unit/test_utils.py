"""Unit tests for spekificity.utils."""

from __future__ import annotations

import subprocess
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from spekificity.utils import print_status, run_command


class TestRunCommand:
    def test_success_returns_completed_process(self):
        result = run_command(["echo", "hello"], "echo test")
        assert isinstance(result, subprocess.CompletedProcess)
        assert result.returncode == 0

    def test_nonzero_exit_raises_runtime_error(self):
        with pytest.raises(RuntimeError, match="exited"):
            run_command(["false"], "false test")

    def test_missing_binary_raises_runtime_error(self):
        with pytest.raises(RuntimeError, match="command not found"):
            run_command(["__no_such_binary__"], "missing test")

    def test_captures_stderr_on_failure(self):
        with pytest.raises(RuntimeError) as exc_info:
            run_command(["ls", "__nonexistent_path_xyz__"], "ls test")
        assert "ls test" in str(exc_info.value)


class TestPrintStatus:
    def test_ok_tag(self, capsys):
        print_status("OK", "step done")
        out = capsys.readouterr().out
        assert out == "[OK] step done\n"

    def test_skip_tag(self, capsys):
        print_status("SKIP", "already present")
        out = capsys.readouterr().out
        assert out == "[SKIP] already present\n"

    def test_warn_tag(self, capsys):
        print_status("WARN", "non-fatal warning")
        out = capsys.readouterr().out
        assert out == "[WARN] non-fatal warning\n"

    def test_error_tag(self, capsys):
        print_status("ERROR", "something failed")
        out = capsys.readouterr().out
        assert out == "[ERROR] something failed\n"
