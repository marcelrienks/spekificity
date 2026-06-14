"""Copy bundled skill files to the integration's skills directory."""

from __future__ import annotations

import importlib.resources as pkg_resources
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from spekificity.skills_install.integrations import get_skills_config
from spekificity.utils import print_status


@dataclass
class SkillInstallResult:
    integration: str
    skills_dir: Path
    installed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def copy_skills(project_path: Path, integration: str) -> SkillInstallResult:
    """Copy skill files from package to integration's skills dir. Always replaces static files."""
    skills_dir_str, use_subfolder = get_skills_config(integration)
    skills_dir = project_path / skills_dir_str
    result = SkillInstallResult(integration=integration, skills_dir=skills_dir)

    skills_src = pkg_resources.files("spekificity") / "skills"
    for skill_resource in skills_src.iterdir():
        name = skill_resource.name
        if not name.endswith(".md") or name.startswith("."):
            continue

        if use_subfolder:
            skill_name = name[:-3]  # strip .md
            dest = skills_dir / skill_name / "SKILL.md"
        else:
            dest = skills_dir / name

        dest.parent.mkdir(parents=True, exist_ok=True)
        was_present = dest.exists()
        with pkg_resources.as_file(skill_resource) as src_path:
            shutil.copy2(src_path, dest)
        result.installed.append(name)
        action = "updated" if was_present else "installed"
        print_status("OK", f"skill {name} {action} at {dest.relative_to(project_path)}")

    return result
