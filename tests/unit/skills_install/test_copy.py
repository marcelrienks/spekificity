"""Unit tests for spekificity.skills_install.copy."""

from __future__ import annotations
from pathlib import Path
import pytest
from spekificity.skills_install.copy import copy_skills


SKILL_NAMES = [
    "spek-prepare.md",
    "spek-plan.md",
    "spek-implement.md",
    "spek-conclude.md",
    "spek-lessons.md",
    "spek-context.md",
    "spek-map.md",
]


class TestCopySkills:
    def test_flat_copy_produces_md_files_at_root(self, tmp_path):
        result = copy_skills(tmp_path, "claude")
        skills_dir = tmp_path / ".claude" / "commands"
        for name in SKILL_NAMES:
            assert (skills_dir / name).exists(), f"Missing {name}"

    def test_subfolder_copy_produces_skill_md(self, tmp_path):
        result = copy_skills(tmp_path, "cursor-agent")
        skills_dir = tmp_path / ".cursor" / "skills"
        for name in SKILL_NAMES:
            skill_name = name.replace(".md", "")
            assert (skills_dir / skill_name / "SKILL.md").exists(), f"Missing {skill_name}/SKILL.md"

    def test_no_overwrite_when_file_exists(self, tmp_path):
        skills_dir = tmp_path / ".claude" / "commands"
        skills_dir.mkdir(parents=True)
        existing = skills_dir / "spek-prepare.md"
        existing.write_text("existing content")
        copy_skills(tmp_path, "claude")
        assert existing.read_text() == "existing content"

    def test_returns_skill_install_result(self, tmp_path):
        result = copy_skills(tmp_path, "claude")
        assert hasattr(result, "installed")
        assert hasattr(result, "skipped")
        assert hasattr(result, "integration")
