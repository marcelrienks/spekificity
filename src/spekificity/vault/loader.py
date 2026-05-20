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
        "obsidian_vault": load_obsidian_vault_summary(),
    }


# ============================================================================
# Obsidian Vault Functions (vault/ directory as persistent memory)
# ============================================================================


def get_obsidian_vault_dir() -> Path:
    """Get Obsidian vault directory path."""
    return Path.cwd() / "vault"


def load_obsidian_lessons() -> Dict[str, str]:
    """Load all lessons from vault/lessons/."""
    try:
        vault_dir = get_obsidian_vault_dir()
        lessons_dir = vault_dir / "lessons"
        
        if not lessons_dir.exists():
            return {}
        
        lessons = {}
        for lesson_file in lessons_dir.glob("*.md"):
            try:
                lessons[lesson_file.stem] = lesson_file.read_text()
            except Exception as e:
                logger.warning(f"Error reading lesson {lesson_file}: {e}")
        
        logger.info(f"Loaded {len(lessons)} lessons from vault/lessons/")
        return lessons
    
    except Exception as e:
        logger.error(f"Error loading obsidian lessons: {e}")
        return {}


def load_obsidian_patterns() -> Dict[str, str]:
    """Load patterns library from vault/patterns.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        patterns_file = vault_dir / "patterns.md"
        
        if not patterns_file.exists():
            return {}
        
        content = patterns_file.read_text()
        patterns = {}
        
        # Split by ## (pattern headers)
        sections = re.split(r'^## ', content, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip first split (before any ##)
            lines = section.split('\n')
            if lines:
                pattern_name = lines[0].strip()
                patterns[pattern_name] = section
        
        logger.info(f"Loaded {len(patterns)} patterns from vault/patterns.md")
        return patterns
    
    except Exception as e:
        logger.error(f"Error loading obsidian patterns: {e}")
        return {}


def load_obsidian_decisions() -> Dict[str, str]:
    """Load architectural decisions from vault/decision.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        decisions_file = vault_dir / "decision.md"
        
        if not decisions_file.exists():
            return {}
        
        content = decisions_file.read_text()
        decisions = {}
        
        # Split by ## (decision headers)
        sections = re.split(r'^## ', content, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip first split
            lines = section.split('\n')
            if lines:
                decision_name = lines[0].strip()
                decisions[decision_name] = section
        
        logger.info(f"Loaded {len(decisions)} decisions from vault/decision.md")
        return decisions
    
    except Exception as e:
        logger.error(f"Error loading obsidian decisions: {e}")
        return {}


def load_obsidian_intention() -> str:
    """Load project intention/vision from vault/intention.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        intention_file = vault_dir / "intention.md"
        
        if not intention_file.exists():
            return ""
        
        content = intention_file.read_text()
        logger.info("Loaded project intention from vault/intention.md")
        return content
    
    except Exception as e:
        logger.error(f"Error loading obsidian intention: {e}")
        return ""


def save_lesson_to_obsidian(feature_name: str, lesson_content: str) -> bool:
    """Save lesson to vault/lessons/<date>-<feature>.md."""
    try:
        from datetime import datetime
        vault_dir = get_obsidian_vault_dir()
        lessons_dir = vault_dir / "lessons"
        lessons_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename: YYYY-MM-DD-<feature>.md
        date_str = datetime.now().strftime("%Y-%m-%d")
        lesson_file = lessons_dir / f"{date_str}-{feature_name}.md"
        
        lesson_file.write_text(lesson_content)
        logger.info(f"Saved lesson to {lesson_file}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving lesson to obsidian: {e}")
        return False


def append_pattern_to_obsidian(pattern_name: str, pattern_content: str) -> bool:
    """Append pattern to vault/patterns.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        patterns_file = vault_dir / "patterns.md"
        
        if not patterns_file.exists():
            logger.warning("vault/patterns.md not found")
            return False
        
        # Append new pattern
        current_content = patterns_file.read_text()
        
        # Add pattern if not already present
        if f"## {pattern_name}" not in current_content:
            new_content = current_content + f"\n## {pattern_name}\n\n{pattern_content}\n\n---\n"
            patterns_file.write_text(new_content)
            logger.info(f"Appended pattern '{pattern_name}' to vault/patterns.md")
            return True
        else:
            logger.info(f"Pattern '{pattern_name}' already exists in vault/patterns.md")
            return False
    
    except Exception as e:
        logger.error(f"Error appending pattern to obsidian: {e}")
        return False


def append_decision_to_obsidian(decision_name: str, decision_content: str) -> bool:
    """Append decision to vault/decision.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        decisions_file = vault_dir / "decision.md"
        
        if not decisions_file.exists():
            logger.warning("vault/decision.md not found")
            return False
        
        # Append new decision
        current_content = decisions_file.read_text()
        
        # Add decision if not already present
        if f"## {decision_name}" not in current_content:
            new_content = current_content + f"\n## {decision_name}\n\n{decision_content}\n\n---\n"
            decisions_file.write_text(new_content)
            logger.info(f"Appended decision '{decision_name}' to vault/decision.md")
            return True
        else:
            logger.info(f"Decision '{decision_name}' already exists in vault/decision.md")
            return False
    
    except Exception as e:
        logger.error(f"Error appending decision to obsidian: {e}")
        return False


def update_intention_obsidian(intention_content: str) -> bool:
    """Update vault/intention.md."""
    try:
        vault_dir = get_obsidian_vault_dir()
        intention_file = vault_dir / "intention.md"
        
        intention_file.write_text(intention_content)
        logger.info("Updated vault/intention.md")
        return True
    
    except Exception as e:
        logger.error(f"Error updating intention in obsidian: {e}")
        return False


# ============================================================================
# Wikilink Support: Extract and Validate [[...]] References
# ============================================================================

def extract_wikilinks(content: str) -> List[str]:
    """Extract [[wikilink]] style references from markdown content."""
    wikilinks = []
    # Find all [[...]] style links
    matches = re.findall(r'\[\[([^\]]+)\]\]', content)
    for match in matches:
        # Extract just the link target (before |)
        target = match.split("|")[0].strip()
        wikilinks.append(target)
    return wikilinks


def get_wikilinks_from_vault() -> Dict[str, List[str]]:
    """Get all wikilinks found in vault files."""
    wikilinks = {}
    
    try:
        vault_dir = get_obsidian_vault_dir()
        if not vault_dir.exists():
            return wikilinks
        
        # Check all vault markdown files
        for md_file in vault_dir.rglob("*.md"):
            try:
                content = md_file.read_text()
                links = extract_wikilinks(content)
                if links:
                    rel_path = md_file.relative_to(vault_dir)
                    wikilinks[str(rel_path)] = links
            except Exception as e:
                logger.warning(f"Error extracting wikilinks from {md_file}: {e}")
        
        logger.info(f"Extracted wikilinks from {len(wikilinks)} vault files")
        return wikilinks
    
    except Exception as e:
        logger.error(f"Error getting wikilinks from vault: {e}")
        return {}


def validate_wikilinks(wikilinks: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Validate wikilinks - identify broken references."""
    broken = {}
    vault_dir = get_obsidian_vault_dir()
    
    try:
        # Build map of available files in vault
        available_files = set()
        for md_file in vault_dir.rglob("*.md"):
            # Store file names without extensions
            available_files.add(md_file.stem)
            # Also store relative paths
            available_files.add(str(md_file.relative_to(vault_dir)).replace("\\", "/"))
        
        # Check each wikilink
        for source_file, links in wikilinks.items():
            broken_links = []
            for link in links:
                # Remove file extension from link if present
                link_target = link.rsplit(".", 1)[0]
                
                # Check if target exists (as filename or path)
                if link_target not in available_files and link not in available_files:
                    broken_links.append(link)
            
            if broken_links:
                broken[source_file] = broken_links
        
        if broken:
            logger.warning(f"Found {sum(len(v) for v in broken.values())} broken wikilinks")
        else:
            logger.info("All wikilinks validated successfully")
        
        return broken
    
    except Exception as e:
        logger.error(f"Error validating wikilinks: {e}")
        return {}


def load_obsidian_vault_summary() -> Dict[str, int]:
    """Get summary of Obsidian vault contents."""
    return {
        "lessons": len(load_obsidian_lessons()),
        "patterns": len(load_obsidian_patterns()),
        "decisions": len(load_obsidian_decisions()),
        "has_intention": bool(load_obsidian_intention()),
    }
