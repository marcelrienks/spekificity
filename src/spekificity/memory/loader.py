"""Memory loading: 3-layer architecture (user, session, repo)."""

from pathlib import Path
from datetime import datetime
import yaml
import json
from loguru import logger
from typing import Optional, Dict, Any

from ..utils.models import UserMemory, SessionMemory, RepoMemory, Context
from ..utils.config import (
    get_user_memories_dir,
    get_session_memories_dir,
    get_repo_memories_dir,
    get_wiki_dir,
    get_cel_dir,
)


def load_user_memory() -> Optional[UserMemory]:
    """Load user-level persistent memory from ~/.memories/."""
    try:
        user_dir = get_user_memories_dir()
        if not user_dir.exists():
            logger.debug("User memory directory not found, skipping")
            return None
        
        prefs_file = user_dir / "preferences.md"
        user_mem = UserMemory(
            source_path=user_dir,
            preferences={},
            skills=[],
            patterns={}
        )
        
        # Parse preferences.md (basic YAML front matter)
        if prefs_file.exists():
            content = prefs_file.read_text()
            if content.startswith("---"):
                # Extract front matter
                parts = content.split("---")
                if len(parts) >= 2:
                    try:
                        front_matter = yaml.safe_load(parts[1].strip())
                        if front_matter:
                            user_mem.preferences = front_matter
                    except yaml.YAMLError:
                        pass
        
        logger.info(f"Loaded user memory from {user_dir}")
        return user_mem
    
    except Exception as e:
        logger.error(f"Error loading user memory: {e}")
        return None


def load_session_memory(feature_name: Optional[str] = None) -> Optional[SessionMemory]:
    """Load session-scoped memory from .memories/session/."""
    try:
        session_dir = get_session_memories_dir()
        if not session_dir.exists():
            logger.debug("Session memory directory not found, skipping")
            return None
        
        session_mem = SessionMemory(
            source_path=session_dir,
            feature_state=None,
            decisions_made=[],
            progress=None
        )
        
        # Load current session context if it exists
        context_file = session_dir / "context-loaded.md"
        if context_file.exists():
            session_mem.progress = context_file.read_text()
        
        # Load feature state if specified
        if feature_name:
            state_file = session_dir / f"{feature_name}-state.yaml"
            if state_file.exists():
                session_mem.feature_state = yaml.safe_load(state_file.read_text())
        
        # Load decisions if they exist
        decisions_file = session_dir / "decisions.yaml"
        if decisions_file.exists():
            decisions = yaml.safe_load(decisions_file.read_text())
            if isinstance(decisions, list):
                session_mem.decisions_made = decisions
        
        logger.info(f"Loaded session memory from {session_dir}")
        return session_mem
    
    except Exception as e:
        logger.error(f"Error loading session memory: {e}")
        return None


def load_repo_memory() -> Optional[RepoMemory]:
    """Load repository-scoped memory from .cel/ and wiki/."""
    try:
        repo_mem = RepoMemory(
            source_path=get_repo_memories_dir(),
            architectural_decisions={},
            patterns_index={},
            vault_specs={},
            lessons={}
        )
        
        # Load repo memory files if they exist
        repo_dir = get_repo_memories_dir()
        if repo_dir.exists():
            # Architectural decisions
            ad_file = repo_dir / "architectural-decisions.md"
            if ad_file.exists():
                repo_mem.architectural_decisions = {"source": ad_file.read_text()[:500]}
            
            # Patterns index
            patterns_file = repo_dir / "patterns-index.md"
            if patterns_file.exists():
                repo_mem.patterns_index = {"source": patterns_file.read_text()[:500]}
        
        # Load wiki specs metadata
        wiki_dir = get_wiki_dir()
        specs_dir = wiki_dir / "specs"
        if specs_dir.exists():
            spec_count = len(list(specs_dir.glob("*.md")))
            repo_mem.metadata["spec_count"] = spec_count
            repo_mem.metadata["specs_dir"] = str(specs_dir)
        
        logger.info(f"Loaded repo memory from .cel/ and wiki/")
        return repo_mem
    
    except Exception as e:
        logger.error(f"Error loading repo memory: {e}")
        return None


def load_context(feature_name: Optional[str] = None, layers: str = "all") -> Context:
    """Load full context with 3-layer architecture."""
    logger.info(f"Loading context (layers={layers}, feature={feature_name})")
    
    context = Context(feature_name=feature_name)
    
    if layers in ("user", "all"):
        context.user_memory = load_user_memory()
    
    if layers in ("session", "all"):
        context.session_memory = load_session_memory(feature_name)
    
    if layers in ("repo", "all"):
        context.repo_memory = load_repo_memory()
    
    logger.info(f"Context loaded: user={context.user_memory is not None}, session={context.session_memory is not None}, repo={context.repo_memory is not None}")
    
    return context


def save_session_context(context: Context) -> None:
    """Save session context to disk for persistence."""
    try:
        session_dir = get_session_memories_dir()
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Save context loaded indicator
        context_file = session_dir / "context-loaded.md"
        context_file.write_text(
            f"# Session Context Loaded\n\n"
            f"**Time:** {context.loaded_at.isoformat()}\n"
            f"**Feature:** {context.feature_name or 'none'}\n\n"
            f"Context layers loaded:\n"
            f"- User: {context.user_memory is not None}\n"
            f"- Session: {context.session_memory is not None}\n"
            f"- Repo: {context.repo_memory is not None}\n"
        )
        
        logger.info(f"Session context saved to {context_file}")
    
    except Exception as e:
        logger.error(f"Error saving session context: {e}")


def save_feature_state(feature_name: str, state: Dict[str, Any]) -> None:
    """Save feature state to session memory."""
    try:
        session_dir = get_session_memories_dir()
        session_dir.mkdir(parents=True, exist_ok=True)
        
        state_file = session_dir / f"{feature_name}-state.yaml"
        state_file.write_text(yaml.dump(state, default_flow_style=False))
        
        logger.info(f"Feature state saved to {state_file}")
    
    except Exception as e:
        logger.error(f"Error saving feature state: {e}")


def get_cached_context() -> Optional[Context]:
    """Get cached context from session memory (if available)."""
    try:
        session_dir = get_session_memories_dir()
        context_file = session_dir / "context-loaded.md"
        
        if context_file.exists():
            logger.info("Using cached context from session")
            return load_context()  # Reload from files
        
        return None
    
    except Exception as e:
        logger.error(f"Error getting cached context: {e}")
        return None
