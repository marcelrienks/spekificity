"""Vault loading: Extract specs, decisions, patterns, and lessons from wiki."""

from pathlib import Path
import re
from loguru import logger
from typing import Dict, List, Optional, Any

from ..utils.models import VaultSpec, ArchitecturalDecision, Pattern, Lesson
from ..utils.config import get_wiki_dir, get_wiki_specs_dir


def load_specs() -> Dict[str, VaultSpec]:
    """Load all specs from wiki/specs/ directory."""
    specs = {}
    try:
        specs_dir = get_wiki_specs_dir()
        if not specs_dir.exists():
            logger.warning(f"Specs directory not found: {specs_dir}")
            return specs
        
        for spec_file in sorted(specs_dir.glob("*.md")):
            try:
                content = spec_file.read_text()
                # Extract title from first # header
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else spec_file.stem
                
                # Extract tags from front matter or content
                tags = []
                tag_match = re.search(r'tags?:\s*\[(.*?)\]', content, re.IGNORECASE)
                if tag_match:
                    tags = [t.strip() for t in tag_match.group(1).split(",")]
                
                spec = VaultSpec(
                    name=spec_file.stem,
                    path=spec_file,
                    title=title,
                    content=content,
                    tags=tags
                )
                specs[spec_file.stem] = spec
            
            except Exception as e:
                logger.error(f"Error loading spec {spec_file}: {e}")
        
        logger.info(f"Loaded {len(specs)} specs from {specs_dir}")
        return specs
    
    except Exception as e:
        logger.error(f"Error loading specs: {e}")
        return specs


def load_architectural_decisions() -> Dict[str, ArchitecturalDecision]:
    """Load architectural decisions from wiki/specs/022-architectural-decisions.md."""
    decisions = {}
    try:
        spec_file = get_wiki_specs_dir() / "022-architectural-decisions.md"
        if not spec_file.exists():
            logger.debug("Architectural decisions spec not found")
            return decisions
        
        content = spec_file.read_text()
        # Parse decision records (basic pattern matching)
        # Format: ## Decision: <title>
        decision_pattern = r'^##\s+Decision:\s+(.+?)(?=^##\s+|$)'
        
        for match in re.finditer(decision_pattern, content, re.MULTILINE | re.DOTALL):
            decision_text = match.group(1).strip()
            # Extract first line as ID/title
            lines = decision_text.split("\n")
            title = lines[0] if lines else "Unknown"
            
            ad = ArchitecturalDecision(
                id=title[:20],
                title=title,
                status="accepted",  # Default, could be parsed
                context="See architectural-decisions.md",
                decision=decision_text[:200],
                consequences="See specification",
                date_created=spec_file.stat().st_mtime  # type: ignore
            )
            decisions[title[:20]] = ad
        
        logger.info(f"Loaded {len(decisions)} architectural decisions")
        return decisions
    
    except Exception as e:
        logger.error(f"Error loading architectural decisions: {e}")
        return decisions


def load_patterns() -> Dict[str, Pattern]:
    """Load patterns from wiki/specs/023-patterns-library.md."""
    patterns = {}
    try:
        spec_file = get_wiki_specs_dir() / "023-patterns-library.md"
        if not spec_file.exists():
            logger.debug("Patterns library spec not found")
            return patterns
        
        content = spec_file.read_text()
        # Parse pattern entries (basic pattern matching)
        # Format: ### Pattern: <name>
        pattern_pattern = r'^###\s+Pattern:\s+(.+?)(?=^###\s+|$)'
        
        for match in re.finditer(pattern_pattern, content, re.MULTILINE | re.DOTALL):
            pattern_text = match.group(1).strip()
            lines = pattern_text.split("\n")
            name = lines[0] if lines else "Unknown"
            
            p = Pattern(
                name=name,
                category="general",  # Could be parsed
                description=pattern_text[:300],
                when_to_use="See patterns-library.md",
                tags=["from-vault"]
            )
            patterns[name] = p
        
        logger.info(f"Loaded {len(patterns)} patterns")
        return patterns
    
    except Exception as e:
        logger.error(f"Error loading patterns: {e}")
        return patterns


def load_lessons(feature_name: Optional[str] = None) -> Dict[str, Lesson]:
    """Load lessons learned from vault/lessons/ or wiki/lessons/."""
    lessons = {}
    try:
        # Try multiple possible locations
        lesson_dirs = [
            get_wiki_dir() / "lessons",
            get_wiki_dir() / "vault" / "lessons",
            Path.home() / ".vault" / "lessons",
        ]
        
        for lesson_dir in lesson_dirs:
            if not lesson_dir.exists():
                continue
            
            for lesson_file in lesson_dir.glob("*.md"):
                try:
                    # If feature_name specified, only load lessons for that feature
                    if feature_name and feature_name not in lesson_file.stem:
                        continue
                    
                    content = lesson_file.read_text()
                    # Extract title from first # header
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else lesson_file.stem
                    
                    lesson = Lesson(
                        feature_name=feature_name or lesson_file.stem,
                        date=Path(lesson_file).stat().st_mtime,  # type: ignore
                        title=title,
                        insight=content[:500],
                        actionable=False,  # Could be parsed from content
                        related_patterns=[]
                    )
                    lessons[lesson_file.stem] = lesson
                
                except Exception as e:
                    logger.error(f"Error loading lesson {lesson_file}: {e}")
        
        logger.info(f"Loaded {len(lessons)} lessons")
        return lessons
    
    except Exception as e:
        logger.error(f"Error loading lessons: {e}")
        return lessons


def get_spec_by_name(spec_name: str) -> Optional[VaultSpec]:
    """Get a specific spec by name."""
    specs = load_specs()
    return specs.get(spec_name)


def search_specs(query: str) -> List[VaultSpec]:
    """Search specs by title or content."""
    specs = load_specs()
    results = []
    query_lower = query.lower()
    
    for spec in specs.values():
        if query_lower in spec.title.lower() or query_lower in spec.content.lower():
            results.append(spec)
    
    return results


def get_related_specs(feature_name: str) -> List[VaultSpec]:
    """Get specs related to a feature."""
    return search_specs(feature_name)


def get_vault_summary() -> Dict[str, Any]:
    """Get summary of vault contents."""
    return {
        "specs": len(load_specs()),
        "decisions": len(load_architectural_decisions()),
        "patterns": len(load_patterns()),
        "lessons": len(load_lessons()),
    }
