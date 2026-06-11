"""Run obsidian open-vault to register the .spek/vault."""

from __future__ import annotations

from pathlib import Path

from spekificity.utils import run_command, print_status


# Initial vault content created via Obsidian CLI so Obsidian indexes them immediately.
_VAULT_FILES = [
    ("file=decisions", "content=# Decisions"),
    ("file=patterns",  "content=# Patterns"),
    ("path=lessons/.keep", "content="),
]


def init_vault(project_path: Path) -> None:
    """Register vault with Obsidian and create initial content files via CLI."""
    vault_path = project_path / ".spek" / "vault"
    sentinel = vault_path / ".initialized"
    if sentinel.exists():
        print_status("SKIP", "Obsidian vault already initialized")
        return
    run_command(["obsidian", "open-vault", f"path={vault_path}"], "obsidian open-vault")
    for file_arg, content_arg in _VAULT_FILES:
        run_command(
            ["obsidian", "create", file_arg, content_arg, "vault=vault"],
            f"obsidian create {file_arg}",
        )
        print_status("OK", f"vault file created via Obsidian: {file_arg}")
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.touch()
    print_status("OK", "Obsidian vault initialized")
