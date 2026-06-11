"""Create .spek/ directory structure."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from spekificity.utils import print_status


@dataclass
class ScaffoldResult:
    created_dirs: list[Path] = field(default_factory=list)
    skipped_dirs: list[Path] = field(default_factory=list)


def scaffold_vault(project_path: Path) -> ScaffoldResult:
    """Create .spek/ dirs and initial files. Idempotent."""
    result = ScaffoldResult()

    dirs = [
        project_path / ".spek" / "vault" / "lessons",
        project_path / ".spek" / "memory",
        project_path / ".spek" / "lat",
    ]
    for d in dirs:
        if d.exists():
            result.skipped_dirs.append(d)
        else:
            d.mkdir(parents=True, exist_ok=True)
            result.created_dirs.append(d)
            print_status("OK", f"created {d.relative_to(project_path)}")

    files = {
        project_path / ".spek" / "vault" / "decisions.md": "# Decisions\n",
        project_path / ".spek" / "vault" / "patterns.md": "# Patterns\n",
        project_path / ".spek" / "vault" / "lessons" / ".keep": "",
    }
    for path, content in files.items():
        if path.exists():
            print_status("SKIP", f"{path.relative_to(project_path)} already exists")
        else:
            path.write_text(content)
            print_status("OK", f"created {path.relative_to(project_path)}")

    return result
