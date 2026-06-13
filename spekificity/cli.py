"""spek CLI — entry point for `spek init`."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from spekificity import __version__
from spekificity.utils import print_status


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Spekificity — spec-driven agent development framework."""


@main.command()
@click.argument("path", default=".", type=click.Path(file_okay=False))
@click.option("--integration", default=None, help="Agent integration type (e.g. claude, copilot, gemini).")
@click.option("--script", "script_type", default=None, type=click.Choice(["sh", "ps"]), help="Script type.")
@click.option("--no-git-hooks", is_flag=True, default=False, help="Skip git hook installation.")
def init(path: str, integration: str | None, script_type: str | None, no_git_hooks: bool) -> None:
    """Initialize Spekificity in a project directory."""
    from spekificity.prerequisites import check_prerequisites
    from spekificity.lat_md.install import install_lat
    from spekificity.lat_md.index import run_lat_index
    from spekificity.lat_md.mcp_config import write_mcp_config, print_mcp_instructions
    from spekificity.lat_md.git_hook import write_git_hook
    from spekificity.vault.install import install_obsidian
    from spekificity.vault.scaffold import scaffold_vault
    from spekificity.vault.init import init_vault
    from spekificity.speckit.install import install_speckit
    from spekificity.speckit.init import run_specify_init
    from spekificity.speckit.config import write_spek_config, InitOptions
    from spekificity.skills_install.copy import copy_skills
    from spekificity.skills_install.integrations import INTEGRATION_MCP_CONFIG

    project_path = Path(path).resolve()

    if not integration:
        integration = click.prompt(
            "Agent integration type",
            default="claude",
        )
    if not script_type:
        script_type = click.prompt(
            "Script type",
            default="sh",
            type=click.Choice(["sh", "ps"]),
        )

    options = InitOptions(
        path=project_path,
        integration=integration,
        script_type=script_type,
        no_git_hooks=no_git_hooks,
    )

    # --- Step 1/8: Prerequisites (fail-fast on missing tool) ---
    print_status("INIT", "Step 1/8: Verifying prerequisites")
    check_prerequisites()

    # --- Step 2/8: lat.md ---
    print_status("INIT", "Step 2/8: Installing code analysis (lat.md)")
    install_lat()
    run_lat_index(project_path)

    # --- Step 3/8: Obsidian + vault scaffold ---
    print_status("INIT", "Step 3/8: Setting up vault (Obsidian)")
    obsidian_result = install_obsidian()
    scaffold_vault(project_path)
    needs_exit_2 = False
    if obsidian_result.status == "needs_user_action":
        needs_exit_2 = True
        print_status("SKIP", "Obsidian CLI not registered — skipping vault init; register CLI and re-run spek init")
    elif obsidian_result.status == "skipped":
        print_status("SKIP", "vault init skipped (Linux — Obsidian not available)")
    else:
        init_vault(project_path)

    # --- Step 4/8: SpecKit ---
    print_status("INIT", "Step 4/8: Installing spec workflow (SpecKit)")
    install_speckit()
    run_specify_init(project_path, integration)
    write_spek_config(project_path, options)

    # --- Step 5/8: MCP config ---
    print_status("INIT", "Step 5/8: Configuring AI agent integration")
    if integration in INTEGRATION_MCP_CONFIG:
        config_file_str, servers_key, extra_fields, flat_key = INTEGRATION_MCP_CONFIG[integration]
        config_path = project_path / config_file_str
        write_mcp_config(config_path, servers_key, extra_fields, integration, flat_key=flat_key)
    else:
        print_mcp_instructions()

    # --- Step 6/8: Git hook ---
    print_status("INIT", "Step 6/8: Installing git hooks")
    write_git_hook(project_path, skip=no_git_hooks)

    # --- Step 7/8: Skills ---
    print_status("INIT", "Step 7/8: Installing agent skills")
    copy_skills(project_path, integration)

    # --- Step 8/8: Caveman ---
    print_status("INIT", "Step 8/8: Enabling Caveman compression")
    from spekificity.caveman.install import install_caveman
    install_caveman(project_path, integration)

    print_status("OK", "Setup complete!")

    if needs_exit_2:
        sys.exit(2)
