"""Unit tests for spekificity.lat_md.git_hook."""

from __future__ import annotations
import stat
from pathlib import Path
import pytest
from spekificity.lat_md.git_hook import write_git_hook


class TestWriteGitHook:
    def test_hook_written_with_correct_content(self, tmp_path):
        (tmp_path / ".git" / "hooks").mkdir(parents=True)
        write_git_hook(tmp_path)
        hook_path = tmp_path / ".git" / "hooks" / "post-commit"
        assert hook_path.exists()
        content = hook_path.read_text()
        assert "lat update" in content
        assert content.startswith("#!/bin/sh")

    def test_hook_is_executable(self, tmp_path):
        (tmp_path / ".git" / "hooks").mkdir(parents=True)
        write_git_hook(tmp_path)
        hook_path = tmp_path / ".git" / "hooks" / "post-commit"
        mode = hook_path.stat().st_mode
        assert mode & stat.S_IXUSR

    def test_skip_when_disable_file_exists(self, tmp_path):
        (tmp_path / ".git" / "hooks").mkdir(parents=True)
        disable = tmp_path / ".spek" / ".disable-git-hooks"
        disable.parent.mkdir(parents=True, exist_ok=True)
        disable.touch()
        write_git_hook(tmp_path)
        assert not (tmp_path / ".git" / "hooks" / "post-commit").exists()

    def test_skip_when_skip_flag_true(self, tmp_path):
        (tmp_path / ".git" / "hooks").mkdir(parents=True)
        write_git_hook(tmp_path, skip=True)
        assert not (tmp_path / ".git" / "hooks" / "post-commit").exists()

    def test_idempotent_when_already_present(self, tmp_path):
        (tmp_path / ".git" / "hooks").mkdir(parents=True)
        hook_path = tmp_path / ".git" / "hooks" / "post-commit"
        hook_path.write_text("#!/bin/sh\necho existing")
        write_git_hook(tmp_path)
        assert hook_path.read_text() == "#!/bin/sh\necho existing"
