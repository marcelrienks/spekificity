"""Run obsidian open-vault to register the .spek/vault."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


def init_vault(project_path: Path) -> None:
    """Run obsidian open-vault. Sentinel prevents redundant re-runs."""
    vault_path = project_path / ".spek" / "vault"
    sentinel = vault_path / ".initialized"
    if sentinel.exists():
        print_status("SKIP", "Obsidian vault already initialized")
        return
    run_command(["obsidian", "open-vault", str(vault_path)], "obsidian open-vault")
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.touch()
    print_status("OK", "Obsidian vault initialized")
