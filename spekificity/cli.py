"""spek CLI — entry point for `spek init`."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from spekificity import __version__
from spekificity.utils import print_status, progress_start, progress_ok, progress_error


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Spekificity — spec-driven agent development framework."""


@main.command()
@click.argument("path", default=".", type=click.Path(file_okay=False))
@click.option("--integration", default=None, help="Agent integration type (e.g. claude, copilot, gemini).")
@click.option("--script", "script_type", default=None, type=click.Choice(["sh", "ps"]), help="Script type.")
@click.option("--no-git-hooks", is_flag=True, default=False, help="Skip git hook installation.")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Show detailed output for debugging.")
def init(
    path: str,
    integration: str | None,
    script_type: str | None,
    no_git_hooks: bool,
    verbose: bool,
) -> None:
    """Initialize Spekificity in a project directory."""
    try:
        _init_impl(path, integration, script_type, no_git_hooks, verbose)
    except KeyboardInterrupt:
        sys.exit(130)


def _init_impl(
    path: str,
    integration: str | None,
    script_type: str | None,
    no_git_hooks: bool,
    verbose: bool = False,
) -> None:
    """Implementation of init command."""
    # Store verbose flag in a global so run_command and print_status can access it
    import spekificity.utils
    spekificity.utils.VERBOSE = verbose
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

    # --- Step 1: Prerequisites (fail-fast on missing tool) ---
    progress_start("Verifying prerequisites")
    check_prerequisites()
    progress_ok()

    # --- Step 2: lat.md ---
    progress_start("Installing code analysis")
    install_lat()
    run_lat_index(project_path)
    progress_ok()

    # --- Step 3: Obsidian + vault scaffold ---
    progress_start("Setting up vault")
    obsidian_result = install_obsidian()
    scaffold_vault(project_path)
    needs_exit_2 = False
    if obsidian_result.status == "needs_user_action":
        needs_exit_2 = True
        progress_ok()
        print_status("SKIP", "Obsidian CLI not registered — register CLI and re-run spek init")
    elif obsidian_result.status == "skipped":
        progress_ok()
        print_status("SKIP", "Obsidian skipped (Linux)")
    else:
        init_vault(project_path)
        progress_ok()

    # --- Step 4: SpecKit ---
    progress_start("Installing spec workflow")
    install_speckit()
    run_specify_init(project_path, integration)
    write_spek_config(project_path, options)
    progress_ok()

    # --- Step 5: MCP config ---
    progress_start("Configuring AI agent integration")
    if integration in INTEGRATION_MCP_CONFIG:
        config_file_str, servers_key, extra_fields, flat_key = INTEGRATION_MCP_CONFIG[integration]
        config_path = project_path / config_file_str
        write_mcp_config(config_path, servers_key, extra_fields, integration, flat_key=flat_key)
    else:
        print_mcp_instructions()
    progress_ok()

    # --- Step 6: Git hook ---
    progress_start("Installing git hooks")
    write_git_hook(project_path, skip=no_git_hooks)
    progress_ok()

    # --- Step 7: Skills ---
    progress_start("Installing agent skills")
    copy_skills(project_path, integration)
    progress_ok()

    # --- Step 8: Caveman ---
    progress_start("Enabling Caveman compression")
    from spekificity.caveman.install import install_caveman
    install_caveman(project_path, integration)
    progress_ok()

    print("")
    print_status("OK", "Setup complete!")

    if needs_exit_2:
        sys.exit(2)
