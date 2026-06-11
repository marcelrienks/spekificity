"""Write .spek/config.yaml from InitOptions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from spekificity.utils import print_status


@dataclass
class InitOptions:
    path: Path
    integration: str
    script_type: Literal["sh", "ps"]
    no_git_hooks: bool = False


_CONFIG_TEMPLATE = """integration: {integration}
script_type: {script_type}
tools:
  speckit:
    enabled: true
  lat_md:
    enabled: true
    index_path: .spek/lat/
  vault:
    enabled: true
    path: .spek/vault/
    obsidian_vault_name: vault
context_loading:
  cache_expiry_minutes: 60
token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000
"""


def write_spek_config(project_path: Path, options: InitOptions) -> None:
    """Write .spek/config.yaml. Idempotent (skip if exists)."""
    config_path = project_path / ".spek" / "config.yaml"
    if config_path.exists():
        print_status("SKIP", ".spek/config.yaml already exists")
        return
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        _CONFIG_TEMPLATE.format(
            integration=options.integration,
            script_type=options.script_type,
        )
    )
    print_status("OK", ".spek/config.yaml written")
