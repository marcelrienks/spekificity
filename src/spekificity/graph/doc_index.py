"""Documentation Index: Index all project documentation independently of code."""

from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger

from ..utils.config import get_vault_dir


@dataclass
class DocNode:
    """Represents a documentation node in the graph."""
    
    id: str  # Unique identifier (e.g., "vault/intention.md" or "specs/feature-x.md")
    path: Path  # Absolute file path
    file_path: str  # Relative path from project root
    title: str  # First H1 or filename
    description: str  # First paragraph or summary
    doc_type: str  # "lesson", "pattern", "decision", "intention", "spec", "guide", etc.
    tags: List[str]  # Tags from frontmatter or content
    wikilinks: List[str]  # [[reference]] style links found in content
    backlinks: List[str]  # Reverse references (computed)
    modified: str  # ISO timestamp
    status: str  # "active", "draft", "archived"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "path": str(self.path),
            "file_path": self.file_path,
            "title": self.title,
            "description": self.description,
            "doc_type": self.doc_type,
            "tags": self.tags,
            "wikilinks": self.wikilinks,
            "backlinks": self.backlinks,
            "modified": self.modified,
            "status": self.status,
        }


class DocIndex:
    """Index all project documentation."""
    
    def __init__(self):
        """Initialize doc index."""
        self.nodes: Dict[str, DocNode] = {}
        self.wikilink_map: Dict[str, List[str]] = {}  # reference -> [node_ids that link to it]
    
    def index_vault(self) -> int:
        """Index Obsidian vault documentation. Returns count of indexed files."""
        count = 0
        vault_dir = Path.cwd() / "vault"
        
        if not vault_dir.exists():
            logger.debug("Vault directory not found, skipping vault indexing")
            return count
        
        logger.info(f"Indexing vault documentation from {vault_dir}")
        
        # Index special files
        intention_file = vault_dir / "intention.md"
        if intention_file.exists():
            count += self._index_file(intention_file, doc_type="intention", relative_base=Path.cwd())
        
        patterns_file = vault_dir / "patterns.md"
        if patterns_file.exists():
            count += self._index_file(patterns_file, doc_type="patterns", relative_base=Path.cwd())
        
        decision_file = vault_dir / "decision.md"
        if decision_file.exists():
            count += self._index_file(decision_file, doc_type="decisions", relative_base=Path.cwd())
        
        # Index lesson files
        lessons_dir = vault_dir / "lessons"
        if lessons_dir.exists():
            for lesson_file in sorted(lessons_dir.glob("*.md")):
                count += self._index_file(lesson_file, doc_type="lesson", relative_base=Path.cwd())
        
        logger.info(f"Indexed {count} vault documentation files")
        return count
    
    def index_wiki(self) -> int:
        """Index wiki/ documentation. Returns count of indexed files."""
        count = 0
        wiki_dir = Path.cwd() / "wiki"
        
        if not wiki_dir.exists():
            logger.debug("Wiki directory not found, skipping wiki indexing")
            return count
        
        logger.info(f"Indexing wiki documentation from {wiki_dir}")
        
        # Index root wiki files
        for doc_file in sorted(wiki_dir.glob("*.md")):
            count += self._index_file(doc_file, doc_type="guide", relative_base=Path.cwd())
        
        # Index specs
        specs_dir = wiki_dir / "specs"
        if specs_dir.exists():
            for spec_file in sorted(specs_dir.glob("*.md")):
                count += self._index_file(spec_file, doc_type="spec", relative_base=Path.cwd())
        
        logger.info(f"Indexed {count} wiki documentation files")
        return count
    
    def _index_file(self, file_path: Path, doc_type: str, relative_base: Path) -> int:
        """Index a single documentation file. Returns 1 if successful, 0 otherwise."""
        try:
            content = file_path.read_text(encoding="utf-8")
            relative_path = file_path.relative_to(relative_base)
            node_id = str(relative_path).replace("\\", "/")  # Normalize to forward slashes
            
            # Extract metadata
            title = self._extract_title(content)
            description = self._extract_description(content)
            tags = self._extract_tags(content)
            wikilinks = self._extract_wikilinks(content)
            status = self._extract_status(content)
            
            # Get modification time
            modified = file_path.stat().st_mtime
            from datetime import datetime
            modified_iso = datetime.fromtimestamp(modified).isoformat()
            
            # Create node
            node = DocNode(
                id=node_id,
                path=file_path,
                file_path=node_id,
                title=title,
                description=description,
                doc_type=doc_type,
                tags=tags,
                wikilinks=wikilinks,
                backlinks=[],
                modified=modified_iso,
                status=status,
            )
            
            self.nodes[node_id] = node
            
            # Track wikilinks
            for wikilink in wikilinks:
                if wikilink not in self.wikilink_map:
                    self.wikilink_map[wikilink] = []
                self.wikilink_map[wikilink].append(node_id)
            
            logger.debug(f"Indexed {node_id}: {title} ({doc_type})")
            return 1
        
        except Exception as e:
            logger.error(f"Error indexing {file_path}: {e}")
            return 0
    
    def _extract_title(self, content: str) -> str:
        """Extract title from first H1 header."""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Untitled"
    
    def _extract_description(self, content: str) -> str:
        """Extract description from first paragraph."""
        # Remove frontmatter
        content_without_fm = re.sub(r'^---.*?---\n', '', content, count=1, flags=re.DOTALL)
        # Get first paragraph
        match = re.search(r'^(?!#)(.+?)(?:\n\n|\Z)', content_without_fm, re.MULTILINE | re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Remove markdown formatting
            text = re.sub(r'[*_`\[\]()]', '', text)
            return text[:200]  # Limit to 200 chars
        return ""
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from frontmatter or content."""
        tags = []
        
        # Check frontmatter
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            tag_match = re.search(r'tags:\s*\[(.*?)\]', fm)
            if tag_match:
                tags = [t.strip().strip("'\"") for t in tag_match.group(1).split(",")]
        
        return tags
    
    def _extract_wikilinks(self, content: str) -> List[str]:
        """Extract [[wikilink]] style references."""
        wikilinks = []
        # Find all [[...]] style links
        matches = re.findall(r'\[\[([^\]]+)\]\]', content)
        for match in matches:
            # Extract just the link target (before |)
            target = match.split("|")[0].strip()
            wikilinks.append(target)
        return wikilinks
    
    def _extract_status(self, content: str) -> str:
        """Extract status from frontmatter or content."""
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            status_match = re.search(r'status:\s*(\w+)', fm)
            if status_match:
                return status_match.group(1).lower()
        return "active"
    
    def build_graph(self) -> None:
        """Build wikilink graph (compute backlinks)."""
        logger.info(f"Building documentation graph with {len(self.nodes)} nodes")
        
        # Compute backlinks
        for node_id, node in self.nodes.items():
            for wikilink in node.wikilinks:
                # Find nodes referenced by this wikilink
                matching_nodes = [n for n in self.nodes.values() if self._wikilink_matches(wikilink, n)]
                for matching_node in matching_nodes:
                    if node_id not in matching_node.backlinks:
                        matching_node.backlinks.append(node_id)
        
        logger.info(f"Documentation graph complete: {len(self.nodes)} nodes with cross-references")
    
    def _wikilink_matches(self, wikilink: str, node: DocNode) -> bool:
        """Check if a wikilink refers to a node."""
        # Remove file extension from wikilink
        wikilink_clean = wikilink.rsplit(".", 1)[0]
        node_clean = node.file_path.rsplit(".", 1)[0]
        
        # Check exact match or filename match
        return wikilink_clean == node_clean or wikilink_clean.endswith(node.title.lower().replace(" ", "-"))
    
    def get_node(self, node_id: str) -> Optional[DocNode]:
        """Get a documentation node by ID."""
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[DocNode]:
        """Get all indexed nodes."""
        return list(self.nodes.values())
    
    def get_by_type(self, doc_type: str) -> List[DocNode]:
        """Get all nodes of a specific type."""
        return [n for n in self.nodes.values() if n.doc_type == doc_type]
    
    def get_by_tag(self, tag: str) -> List[DocNode]:
        """Get all nodes with a specific tag."""
        return [n for n in self.nodes.values() if tag in n.tags]
    
    def get_related(self, node_id: str, depth: int = 1) -> List[DocNode]:
        """Get nodes related to a given node via wikilinks (up to specified depth)."""
        if node_id not in self.nodes:
            return []
        
        related = set()
        to_visit = [node_id]
        visited = set()
        
        for _ in range(depth):
            next_visit = []
            for nid in to_visit:
                if nid in visited:
                    continue
                visited.add(nid)
                
                node = self.nodes.get(nid)
                if not node:
                    continue
                
                # Add wikilink targets
                for wikilink in node.wikilinks:
                    matching = [n for n in self.nodes.values() if self._wikilink_matches(wikilink, n)]
                    for m in matching:
                        if m.id != node_id:  # Don't include the source node itself
                            related.add(m.id)
                            next_visit.append(m.id)
                
                # Add backlinks
                for backlink_id in node.backlinks:
                    if backlink_id != node_id:
                        related.add(backlink_id)
                        next_visit.append(backlink_id)
            
            to_visit = next_visit
        
        return [self.nodes[rid] for rid in related if rid in self.nodes]
    
    def to_dict(self) -> dict:
        """Export entire index as dictionary."""
        return {
            "total_nodes": len(self.nodes),
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "wikilink_map": self.wikilink_map,
        }


def build_documentation_index() -> DocIndex:
    """Build a complete documentation index."""
    index = DocIndex()
    
    # Index all documentation
    vault_count = index.index_vault()
    wiki_count = index.index_wiki()
    
    # Build wikilink graph
    index.build_graph()
    
    logger.info(f"Documentation index complete: {vault_count} vault + {wiki_count} wiki = {len(index.nodes)} total nodes")
    
    return index


def get_documentation_summary(index: DocIndex) -> dict:
    """Get summary statistics about documentation."""
    return {
        "total_files": len(index.nodes),
        "by_type": {doc_type: len(index.get_by_type(doc_type)) for doc_type in set(n.doc_type for n in index.nodes.values())},
        "intentions": len(index.get_by_type("intention")),
        "patterns": len(index.get_by_type("patterns")),
        "decisions": len(index.get_by_type("decisions")),
        "lessons": len(index.get_by_type("lesson")),
        "specs": len(index.get_by_type("spec")),
        "guides": len(index.get_by_type("guide")),
    }
