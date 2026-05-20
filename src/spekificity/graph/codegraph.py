"""CodeGraph: Indexed code analysis and querying."""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import ast
import json
from loguru import logger

from ..utils.models import CodeGraphNode, CodeGraphEdge, ImpactAnalysis
from ..utils.config import get_codegraph_db_path, get_src_dir


class CodeGraph:
    """Code graph: SQLite-backed indexed code analysis."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize CodeGraph."""
        self.db_path = db_path or get_codegraph_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize or migrate database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Nodes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    node_id TEXT PRIMARY KEY,
                    node_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    file_path TEXT,
                    line_start INTEGER,
                    line_end INTEGER,
                    language TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Edges table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    edge_type TEXT NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES nodes(node_id),
                    FOREIGN KEY (target_id) REFERENCES nodes(node_id)
                )
            """)
            
            # Create indices for fast queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_name ON nodes(name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_file ON nodes(file_path)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)")
            
            # Metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info(f"CodeGraph database initialized at {self.db_path}")
    
    def index_python_file(self, file_path: Path) -> List[CodeGraphNode]:
        """Index a Python file and extract symbols."""
        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            nodes = []
            
            # Extract top-level definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    node_id = f"{file_path.stem}:{node.name}:function"
                    cg_node = CodeGraphNode(
                        node_id=node_id,
                        node_type="function",
                        name=node.name,
                        path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        language="python",
                        metadata={"args": [a.arg for a in node.args.args]}
                    )
                    nodes.append(cg_node)
                    self.add_node(cg_node)
                
                elif isinstance(node, ast.ClassDef):
                    node_id = f"{file_path.stem}:{node.name}:class"
                    cg_node = CodeGraphNode(
                        node_id=node_id,
                        node_type="class",
                        name=node.name,
                        path=file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        language="python",
                        metadata={"bases": [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases]}
                    )
                    nodes.append(cg_node)
                    self.add_node(cg_node)
            
            # Add file node
            file_node = CodeGraphNode(
                node_id=f"{file_path.stem}:file",
                node_type="file",
                name=file_path.name,
                path=file_path,
                language="python"
            )
            nodes.append(file_node)
            self.add_node(file_node)
            
            logger.info(f"Indexed {file_path}: {len(nodes)} symbols")
            return nodes
        
        except Exception as e:
            logger.error(f"Error indexing {file_path}: {e}")
            return []
    
    def index_directory(self, directory: Path, pattern: str = "*.py") -> int:
        """Index all Python files in a directory."""
        count = 0
        for file_path in directory.rglob(pattern):
            if ".venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            nodes = self.index_python_file(file_path)
            count += len(nodes)
        
        logger.info(f"Indexed directory {directory}: {count} total symbols")
        return count
    
    def add_node(self, node: CodeGraphNode) -> None:
        """Add a node to the graph."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO nodes 
                    (node_id, node_type, name, file_path, line_start, line_end, language, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    node.node_id,
                    node.node_type,
                    node.name,
                    str(node.path) if node.path else None,
                    node.line_start,
                    node.line_end,
                    node.language,
                    json.dumps(node.metadata)
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Error adding node {node.node_id}: {e}")
    
    def add_edge(self, edge: CodeGraphEdge) -> None:
        """Add an edge to the graph."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO edges (source_id, target_id, edge_type, metadata)
                    VALUES (?, ?, ?, ?)
                """, (
                    edge.source_id,
                    edge.target_id,
                    edge.edge_type,
                    json.dumps(edge.metadata)
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Error adding edge: {e}")
    
    def get_symbol(self, name: str) -> Optional[CodeGraphNode]:
        """Get a symbol by name."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT node_id, node_type, name, file_path, line_start, line_end, language, metadata
                    FROM nodes WHERE name = ? LIMIT 1
                """, (name,))
                row = cursor.fetchone()
                
                if row:
                    node_id, node_type, name, file_path, line_start, line_end, language, metadata = row
                    return CodeGraphNode(
                        node_id=node_id,
                        node_type=node_type,
                        name=name,
                        path=Path(file_path) if file_path else None,
                        line_start=line_start,
                        line_end=line_end,
                        language=language,
                        metadata=json.loads(metadata) if metadata else {}
                    )
        except Exception as e:
            logger.error(f"Error getting symbol {name}: {e}")
        
        return None
    
    def get_references(self, symbol_name: str) -> List[CodeGraphNode]:
        """Get all nodes that reference a symbol."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get edges targeting the symbol
                cursor.execute("""
                    SELECT source_id FROM edges 
                    WHERE target_id LIKE ? OR target_id IN (
                        SELECT node_id FROM nodes WHERE name = ?
                    )
                """, (f"%:{symbol_name}:%", symbol_name))
                
                references = []
                for (source_id,) in cursor.fetchall():
                    cursor.execute("""
                        SELECT node_id, node_type, name, file_path, line_start, line_end, language, metadata
                        FROM nodes WHERE node_id = ?
                    """, (source_id,))
                    row = cursor.fetchone()
                    if row:
                        node_id, node_type, name, file_path, line_start, line_end, language, metadata = row
                        references.append(CodeGraphNode(
                            node_id=node_id,
                            node_type=node_type,
                            name=name,
                            path=Path(file_path) if file_path else None,
                            line_start=line_start,
                            line_end=line_end,
                            language=language,
                            metadata=json.loads(metadata) if metadata else {}
                        ))
                
                return references
        except Exception as e:
            logger.error(f"Error getting references: {e}")
        
        return []
    
    def analyze_impact(self, symbol_name: str) -> ImpactAnalysis:
        """Analyze impact of changes to a symbol."""
        symbol = self.get_symbol(symbol_name)
        references = self.get_references(symbol_name)
        
        affected_files = set()
        affected_symbols = []
        
        for ref in references:
            if ref.path:
                affected_files.add(ref.path)
            affected_symbols.append(ref.name)
        
        # Determine risk level based on number of references
        risk_level = "low" if len(references) <= 2 else "medium" if len(references) <= 10 else "high"
        
        return ImpactAnalysis(
            symbol=symbol_name,
            affected_files=list(affected_files),
            affected_symbols=affected_symbols,
            risk_level=risk_level,
            recommendations=[
                "Review all references before making changes",
                "Add tests for affected modules",
                "Consider backward compatibility"
            ] if risk_level == "high" else []
        )
    
    def refresh(self, source_dir: Optional[Path] = None) -> int:
        """Refresh the code graph."""
        source_dir = source_dir or get_src_dir()
        if not source_dir.exists():
            logger.warning(f"Source directory not found: {source_dir}")
            return 0
        
        # Clear existing nodes (for now, full refresh)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM edges")
            cursor.execute("DELETE FROM nodes")
            conn.commit()
        
        # Re-index
        count = self.index_directory(source_dir)
        
        # Update metadata
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO metadata (key, value)
                VALUES (?, ?)
            """, ("last_refresh", datetime.now().isoformat()))
            conn.commit()
        
        logger.info(f"CodeGraph refreshed: {count} symbols indexed")
        return count
    
    def is_stale(self, max_age_hours: int = 24) -> bool:
        """Check if code graph is stale."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM metadata WHERE key = 'last_refresh'")
                row = cursor.fetchone()
                
                if not row:
                    return True
                
                last_refresh = datetime.fromisoformat(row[0])
                age_hours = (datetime.now() - last_refresh).total_seconds() / 3600
                return age_hours > max_age_hours
        except Exception as e:
            logger.error(f"Error checking staleness: {e}")
            return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get CodeGraph statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM nodes")
                node_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM edges")
                edge_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT value FROM metadata WHERE key = 'last_refresh'")
                last_refresh = cursor.fetchone()
                
                return {
                    "node_count": node_count,
                    "edge_count": edge_count,
                    "last_refresh": last_refresh[0] if last_refresh else None,
                    "db_path": str(self.db_path),
                    "db_size_mb": self.db_path.stat().st_size / (1024 * 1024)
                }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
