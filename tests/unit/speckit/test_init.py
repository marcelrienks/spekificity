"""Unit tests for spekificity.speckit.init."""

from __future__ import annotations
from pathlib import Path
from unittest.mock import patch
import json
import pytest
from spekificity.speckit.init import run_specify_init, _configure_speckit_output_path


class TestConfigureSpeckitOutputPath:
    def test_creates_vault_directory(self, tmp_path):
        """Verify vault directory is created if missing."""
        _configure_speckit_output_path(tmp_path)
        assert (tmp_path / ".spek" / "vault" / "specs").exists()

    def test_creates_config_with_artifact_path(self, tmp_path):
        """Verify .specify/config.json is created with artifact_output_dir."""
        _configure_speckit_output_path(tmp_path)
        config_path = tmp_path / ".specify" / "config.json"
        assert config_path.exists()
        
        with config_path.open() as f:
            config = json.load(f)
        
        assert "artifact_output_dir" in config
        assert ".spek/vault/specs" in config["artifact_output_dir"]

    def test_idempotent_preserves_existing_config(self, tmp_path):
        """Verify existing config is preserved when called multiple times."""
        # First call
        _configure_speckit_output_path(tmp_path)
        config_path = tmp_path / ".specify" / "config.json"
        
        # Add custom setting
        with config_path.open() as f:
            config = json.load(f)
        config["custom_setting"] = "test_value"
        
        with config_path.open("w") as f:
            json.dump(config, f)
        
        # Second call should not overwrite custom_setting
        _configure_speckit_output_path(tmp_path)
        
        with config_path.open() as f:
            config = json.load(f)
        
        assert config["custom_setting"] == "test_value"
        assert "artifact_output_dir" in config


class TestRunSpecifyInit:
    def test_skips_when_specify_dir_exists(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        with patch("spekificity.speckit.init.run_command") as mock_run:
            with patch("spekificity.speckit.init._configure_speckit_output_path"):
                run_specify_init(tmp_path, "claude")
        mock_run.assert_not_called()

    def test_runs_specify_init_when_dir_absent(self, tmp_path):
        with patch("spekificity.speckit.init.run_command") as mock_run:
            with patch("spekificity.speckit.init._configure_speckit_output_path"):
                run_specify_init(tmp_path, "claude")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "specify" in args
        assert "init" in args

    def test_passes_integration_flag(self, tmp_path):
        with patch("spekificity.speckit.init.run_command") as mock_run:
            with patch("spekificity.speckit.init._configure_speckit_output_path"):
                run_specify_init(tmp_path, "cursor-agent")
        args = mock_run.call_args[0][0]
        assert "--integration" in args
        assert "cursor-agent" in args
    
    def test_calls_configure_output_path_after_init(self, tmp_path):
        """Verify output path configuration is called after specify init."""
        with patch("spekificity.speckit.init.run_command"):
            with patch("spekificity.speckit.init._configure_speckit_output_path") as mock_config:
                run_specify_init(tmp_path, "claude")
        mock_config.assert_called_once_with(tmp_path)

