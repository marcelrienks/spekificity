"""Write .git/hooks/post-commit for lat update."""

from __future__ import annotations

import os
import stat
from pathlib import Path

from spekificity.utils import print_status

_HOOK_CONTENT = "#!/bin/sh\nlat update\n"


def write_git_hook(project_path: Path, skip: bool = False) -> None:
    """Write post-commit hook. Skipped if skip=True, --no-git-hooks used, or .spek/.disable-git-hooks exists."""
    disable_file = project_path / ".spek" / ".disable-git-hooks"
    if skip or disable_file.exists():
        print_status("SKIP", "git hook installation skipped (--no-git-hooks or .disable-git-hooks)")
        return

    hook_path = project_path / ".git" / "hooks" / "post-commit"
    if hook_path.exists():
        print_status("SKIP", "post-commit hook already present")
        return

    hook_path.parent.mkdir(parents=True, exist_ok=True)
    hook_path.write_text(_HOOK_CONTENT)
    current_mode = os.stat(hook_path).st_mode
    os.chmod(hook_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print_status("OK", f"post-commit hook written to {hook_path}")
