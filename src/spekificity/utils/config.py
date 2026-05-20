"""Configuration and path utilities."""

from pathlib import Path
import os


def get_project_root() -> Path:
    """Get project root directory (where pyproject.toml is)."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "pyproject.toml").exists() and "spekificity" in (current / "pyproject.toml").read_text():
            return current
        current = current.parent
    return Path.cwd()


def get_memories_dir() -> Path:
    """Get .memories/ directory (project root)."""
    return get_project_root() / ".memories"


def get_user_memories_dir() -> Path:
    """Get /memories/ directory (user-level, outside project)."""
    home = Path.home()
    return home / ".memories"


def get_session_memories_dir() -> Path:
    """Get /memories/session/ directory."""
    return get_memories_dir() / "session"


def get_repo_memories_dir() -> Path:
    """Get .memories/repo/ directory (project-scoped)."""
    return get_memories_dir() / "repo"


def get_cel_dir() -> Path:
    """Get .cel/ directory (cache + state)."""
    return get_project_root() / ".cel"


def get_wiki_dir() -> Path:
    """Get wiki/ directory."""
    return get_project_root() / "wiki"


def get_wiki_specs_dir() -> Path:
    """Get wiki/specs/ directory."""
    return get_wiki_dir() / "specs"


def get_vault_dir() -> Path:
    """Get vault/ directory (if exists in wiki/)."""
    vault = get_project_root() / "vault"
    if vault.exists():
        return vault
    return get_wiki_dir() / "vault"


def get_src_dir() -> Path:
    """Get src/ directory."""
    return get_project_root() / "src"


def get_codegraph_db_path() -> Path:
    """Get CodeGraph SQLite database path."""
    return get_cel_dir() / "codegraph.db"


def get_feature_state_path(feature_name: str) -> Path:
    """Get feature state file path."""
    session_dir = get_session_memories_dir()
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir / f"{feature_name}-state.yaml"


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    dirs = [
        get_memories_dir(),
        get_session_memories_dir(),
        get_repo_memories_dir(),
        get_cel_dir(),
        get_wiki_dir(),
        get_wiki_specs_dir(),
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


# Global configuration
PROJECT_ROOT = get_project_root()
MEMORIES_DIR = get_memories_dir()
USER_MEMORIES_DIR = get_user_memories_dir()
SESSION_MEMORIES_DIR = get_session_memories_dir()
REPO_MEMORIES_DIR = get_repo_memories_dir()
CEL_DIR = get_cel_dir()
WIKI_DIR = get_wiki_dir()
WIKI_SPECS_DIR = get_wiki_specs_dir()
VAULT_DIR = get_vault_dir()
SRC_DIR = get_src_dir()
CODEGRAPH_DB = get_codegraph_db_path()

# Ensure directories on import
ensure_directories()
