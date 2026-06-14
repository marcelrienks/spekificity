"""Populate agent config files (CLAUDE.md, etc.) from constitution principles."""

from __future__ import annotations

import re
from pathlib import Path

from spekificity.utils import print_status


def _extract_principles(constitution_path: Path) -> list[tuple[str, str]]:
    """Extract Core Principles from constitution.md.

    Returns list of (name, description) tuples.
    """
    if not constitution_path.exists():
        return []

    content = constitution_path.read_text()

    # Find "## Core Principles" section
    match = re.search(r"## Core Principles\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if not match:
        return []

    principles_section = match.group(1)
    principles = []

    # Extract ### [NAME] followed by description (first non-comment line)
    principle_blocks = re.findall(
        r"### ([^\n]+)\n(?:<!--.*?-->\n)?([^\n]+)",
        principles_section,
        re.DOTALL
    )

    for name, desc in principle_blocks:
        name = name.strip()
        desc = desc.strip()
        if name and desc and not desc.startswith("<!--"):
            principles.append((name, desc))

    return principles


def _generate_claude_md(principles: list[tuple[str, str]]) -> str:
    """Generate CLAUDE.md content from principles."""
    if not principles:
        return ""

    lines = ["# Project Constitution — Claude Agent Rules\n"]
    lines.append("Derived from `.specify/memory/constitution.md` core principles.\n")

    for name, desc in principles:
        lines.append(f"## {name}\n")
        lines.append(f"{desc}\n")

    return "\n".join(lines)


def populate_agent_configs(project_path: Path) -> None:
    """Populate agent config files from constitution.

    Updates CLAUDE.md, .cursor/rules.md, .windsurf/rules.md based on
    Core Principles extracted from .specify/memory/constitution.md.
    """
    constitution_path = project_path / ".specify" / "memory" / "constitution.md"
    principles = _extract_principles(constitution_path)

    if not principles:
        print_status("SKIP", "No principles found in constitution")
        return

    # Generate and write CLAUDE.md
    claude_content = _generate_claude_md(principles)
    claude_path = project_path / "CLAUDE.md"
    claude_path.write_text(claude_content)
    print_status("OK", f"CLAUDE.md populated ({len(principles)} principles)")

    # Generate and write .cursor/rules.md if .cursor exists
    cursor_dir = project_path / ".cursor"
    if cursor_dir.exists():
        cursor_rules_path = cursor_dir / "rules.md"
        cursor_rules_path.write_text(claude_content.replace("Claude Agent", "Cursor Agent"))
        print_status("OK", f".cursor/rules.md populated ({len(principles)} principles)")

    # Generate and write .windsurf/rules.md if .windsurf exists
    windsurf_dir = project_path / ".windsurf"
    if windsurf_dir.exists():
        windsurf_rules_path = windsurf_dir / "rules.md"
        windsurf_rules_path.write_text(claude_content.replace("Claude Agent", "Windsurf Agent"))
        print_status("OK", f".windsurf/rules.md populated ({len(principles)} principles)")
