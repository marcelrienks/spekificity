"""Vault engine for loading, writing, and querying project knowledge."""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import yaml


class Vault:
    """Interface for vault operations (decisions, patterns, lessons)."""
    
    def __init__(self, vault_path: str = ".spek/vault"):
        self.path = Path(vault_path)
        self.decisions_file = self.path / "decisions.md"
        self.patterns_file = self.path / "patterns.md"
        self.lessons_dir = self.path / "lessons"
    
    def ensure_structure(self) -> None:
        """Ensure vault directory structure exists."""
        self.path.mkdir(exist_ok=True)
        self.lessons_dir.mkdir(exist_ok=True)
    
    def load_decisions(self) -> List[dict]:
        """Load all decisions from vault/decisions.md.
        
        Returns:
            List of decision dictionaries (parsed from YAML frontmatter)
        """
        if not self.decisions_file.exists():
            return []
        
        decisions = []
        content = self.decisions_file.read_text()
        
        # Simple extraction of YAML frontmatter blocks
        # More robust parsing would use a markdown parser
        blocks = content.split("---")
        for block in blocks[1::2]:  # Skip first empty split, take every other block
            try:
                data = yaml.safe_load(block)
                if isinstance(data, dict) and "id" in data:
                    decisions.append(data)
            except yaml.YAMLError:
                continue
        
        return decisions
    
    def load_patterns(self) -> List[dict]:
        """Load all patterns from vault/patterns.md.
        
        Returns:
            List of pattern dictionaries (parsed from YAML frontmatter)
        """
        if not self.patterns_file.exists():
            return []
        
        patterns = []
        content = self.patterns_file.read_text()
        
        blocks = content.split("---")
        for block in blocks[1::2]:
            try:
                data = yaml.safe_load(block)
                if isinstance(data, dict) and "id" in data:
                    patterns.append(data)
            except yaml.YAMLError:
                continue
        
        return patterns
    
    def load_lessons(self, limit: Optional[int] = None) -> List[dict]:
        """Load lessons from vault/lessons/ directory.
        
        Args:
            limit: Maximum number of lessons to load (most recent first)
        
        Returns:
            List of lesson dictionaries
        """
        lessons = []
        
        if not self.lessons_dir.exists():
            return lessons
        
        # Load individual lesson files
        lesson_files = sorted(
            self.lessons_dir.glob("*.md"),
            reverse=True  # Most recent first
        )
        
        for lesson_file in lesson_files:
            if limit and len(lessons) >= limit:
                break
            
            try:
                content = lesson_file.read_text()
                blocks = content.split("---")
                if len(blocks) > 1:
                    data = yaml.safe_load(blocks[1])
                    if isinstance(data, dict):
                        data["file"] = str(lesson_file)
                        lessons.append(data)
            except Exception:
                continue
        
        return lessons
    
    def write_lesson(self, lesson_data: dict) -> Path:
        """Write a new lesson to vault/lessons/.
        
        Args:
            lesson_data: Dictionary with lesson content
        
        Returns:
            Path to created lesson file
        """
        self.ensure_structure()
        
        # Generate filename: YYYY-MM-DD-feature-name.md
        now = datetime.utcnow().strftime("%Y-%m-%d")
        feature = lesson_data.get("feature", "unnamed")
        feature_slug = feature.lower().replace(" ", "-")[:30]
        
        counter = 0
        while True:
            suffix = f"-{counter}" if counter > 0 else ""
            filename = f"{now}-{feature_slug}{suffix}.md"
            filepath = self.lessons_dir / filename
            if not filepath.exists():
                break
            counter += 1
        
        # Write YAML frontmatter + content
        frontmatter = {
            "feature": lesson_data.get("feature", ""),
            "date": lesson_data.get("date", datetime.utcnow().isoformat()),
            "author": lesson_data.get("author", ""),
        }
        
        content = "---\n"
        content += yaml.dump(frontmatter, default_flow_style=False)
        content += "---\n\n"
        content += f"# {lesson_data.get('feature', 'Lesson')}\n\n"
        
        if "outcomes" in lesson_data:
            content += f"## Outcomes\n\n{lesson_data['outcomes']}\n\n"
        
        if "lessons_learned" in lesson_data:
            content += "## Lessons Learned\n\n"
            for lesson in lesson_data["lessons_learned"]:
                content += f"- {lesson}\n"
            content += "\n"
        
        if "new_patterns" in lesson_data:
            content += "## New Patterns\n\n"
            for pattern in lesson_data["new_patterns"]:
                content += f"- {pattern}\n"
        
        filepath.write_text(content)
        return filepath
    
    def get_summary(self) -> dict:
        """Get a summary of vault contents."""
        return {
            "decisions": len(self.load_decisions()),
            "patterns": len(self.load_patterns()),
            "lessons": len(self.load_lessons()),
            "vault_path": str(self.path),
        }


def create_vault_structure(vault_path: Path) -> None:
    """Create initial vault directory structure with templates.
    
    Args:
        vault_path: Path to vault directory
    """
    vault_path.mkdir(parents=True, exist_ok=True)
    (vault_path / "lessons").mkdir(exist_ok=True)
    
    # Copy template files (if they exist)
    template_dir = Path(__file__).parent.parent / "templates"
    
    for template_file in ["decisions.md", "patterns.md"]:
        template_path = template_dir / template_file
        vault_file = vault_path / template_file
        
        if template_path.exists() and not vault_file.exists():
            vault_file.write_text(template_path.read_text())


def load_vault(vault_path: str = ".spek/vault") -> Vault:
    """Load a vault instance.
    
    Args:
        vault_path: Path to vault directory
    
    Returns:
        Vault instance
    """
    vault = Vault(vault_path)
    vault.ensure_structure()
    return vault
