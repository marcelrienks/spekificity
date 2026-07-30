"""Run specify init to initialize SpecKit in the project."""

from __future__ import annotations

import json
import os
from pathlib import Path

from spekificity.utils import run_command, print_status


def _configure_speckit_output_path(project_path: Path) -> None:
    """Configure SpecKit to write artifacts to .spek/vault/ instead of project root.
    
    This ensures that spec.md, plan.md, and tasks.md are stored directly in
    .spek/vault/ (vault-native design) rather than in project root and then
    moved. This configuration is idempotent — it only creates/updates the
    config if it doesn't already have the setting.
    """
    vault_path = project_path / ".spek" / "vault"
    specify_config_path = project_path / ".specify" / "config.json"
    
    # Ensure vault directory exists
    vault_path.mkdir(parents=True, exist_ok=True)
    specs_dir = vault_path / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    
    # Load or initialize config
    if specify_config_path.exists():
        try:
            with specify_config_path.open("r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = {}
    else:
        config = {}
    
    # Configure artifact output path if not already set
    # Key path may vary by SpecKit version; we set a reasonable default
    if "artifact_output_dir" not in config:
        config["artifact_output_dir"] = str(specs_dir.relative_to(project_path))
        try:
            specify_config_path.parent.mkdir(parents=True, exist_ok=True)
            with specify_config_path.open("w") as f:
                json.dump(config, f, indent=2)
            print_status("OK", f"SpecKit configured to write to .spek/vault/specs/")
        except IOError as e:
            print_status("WARN", f"Could not write SpecKit config: {e}")


def run_specify_init(project_path: Path, integration: str) -> None:
    """Run specify init if .specify/ dir does not exist (idempotent).
    
    After SpecKit initialization, configures it to write artifacts to
    .spek/vault/specs/ to ensure vault-native artifact storage.
    """
    specify_dir = project_path / ".specify"
    if specify_dir.exists():
        print_status("SKIP", ".specify/ already exists — skipping specify init")
        return

    # Change to project directory so --here works, then restore after
    old_cwd = os.getcwd()
    try:
        os.chdir(project_path)
        run_command(
            ["specify", "init", "--here", "--force", "--integration", integration],
            "specify init",
        )
    finally:
        os.chdir(old_cwd)

    print_status("OK", "SpecKit initialized (.specify/)")
    
    # Configure SpecKit to write artifacts to vault
    _configure_speckit_output_path(project_path)
