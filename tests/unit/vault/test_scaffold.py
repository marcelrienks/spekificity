"""Unit tests for spekificity.vault.scaffold."""

from __future__ import annotations
from pathlib import Path
import pytest
from spekificity.vault.scaffold import scaffold_vault


class TestScaffoldVault:
    def test_creates_all_dirs(self, tmp_path):
        result = scaffold_vault(tmp_path)
        assert (tmp_path / ".spek" / "vault" / "lessons").is_dir()
        assert (tmp_path / ".spek" / "memory").is_dir()
        assert (tmp_path / ".spek" / "lat").is_dir()

    def test_does_not_create_content_files(self, tmp_path):
        scaffold_vault(tmp_path)
        assert not (tmp_path / ".spek" / "vault" / "decisions.md").exists()
        assert not (tmp_path / ".spek" / "vault" / "patterns.md").exists()

    def test_idempotent_existing_dirs_skipped(self, tmp_path):
        scaffold_vault(tmp_path)
        result2 = scaffold_vault(tmp_path)
        assert len(result2.created_dirs) == 0
        assert len(result2.skipped_dirs) == 3

    def test_returns_scaffold_result(self, tmp_path):
        result = scaffold_vault(tmp_path)
        assert hasattr(result, "created_dirs")
        assert hasattr(result, "skipped_dirs")
        assert len(result.created_dirs) == 3
