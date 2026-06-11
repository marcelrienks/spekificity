"""Unit tests for spekificity.speckit.config."""

from __future__ import annotations
from pathlib import Path
import pytest
from spekificity.speckit.config import write_spek_config, InitOptions


class TestWriteSpekConfig:
    def _make_options(self, tmp_path, integration="claude", script_type="sh"):
        return InitOptions(path=tmp_path, integration=integration, script_type=script_type)

    def test_creates_config_yaml(self, tmp_path):
        (tmp_path / ".spek").mkdir()
        opts = self._make_options(tmp_path)
        write_spek_config(tmp_path, opts)
        config_path = tmp_path / ".spek" / "config.yaml"
        assert config_path.exists()

    def test_config_contains_all_required_fields(self, tmp_path):
        (tmp_path / ".spek").mkdir()
        opts = self._make_options(tmp_path)
        write_spek_config(tmp_path, opts)
        content = (tmp_path / ".spek" / "config.yaml").read_text()
        assert "integration: claude" in content
        assert "script_type: sh" in content
        assert "speckit:" in content
        assert "lat_md:" in content
        assert "vault:" in content
        assert "context_loading:" in content
        assert "token_limits:" in content
        assert "autolink:" in content
        assert "enabled: true" in content
        assert "threshold: 0.8" in content

    def test_idempotent_skips_existing(self, tmp_path):
        (tmp_path / ".spek").mkdir()
        opts = self._make_options(tmp_path)
        write_spek_config(tmp_path, opts)
        original = (tmp_path / ".spek" / "config.yaml").read_text()
        # Second write with different options — file should not change
        opts2 = self._make_options(tmp_path, integration="gemini")
        write_spek_config(tmp_path, opts2)
        assert (tmp_path / ".spek" / "config.yaml").read_text() == original

    def test_creates_parent_dirs_if_missing(self, tmp_path):
        opts = self._make_options(tmp_path)
        write_spek_config(tmp_path, opts)
        assert (tmp_path / ".spek" / "config.yaml").exists()
