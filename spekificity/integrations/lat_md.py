"""Integration with lat.md for code indexing and analysis.

lat.md provides BM25 lexical retrieval for code search via MCP interface.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

import click


class LatMdIndex:
    """Interface for lat.md code indexing and queries."""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.index_dir = self.project_path / ".lat"
    
    def ensure_index(self) -> bool:
        """Initialize lat.md index if not exists.
        
        Returns:
            True if index initialized successfully
        """
        if self.index_dir.exists():
            return True
        
        try:
            # Try to run lat init
            result = subprocess.run(
                ["lat", "init", str(self.project_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            click.echo(f"⚠ lat init failed: {e}", err=True)
            return False
    
    def sync_index(self, full: bool = False) -> bool:
        """Sync lat.md index with current codebase.
        
        Args:
            full: Run full rebuild instead of incremental sync
        
        Returns:
            True if sync successful
        """
        try:
            cmd = ["lat", "sync", str(self.project_path)]
            if full:
                cmd.append("--full")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            click.echo(f"⚠ lat sync failed: {e}", err=True)
            return False
    
    def query_files(self, intent: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query for relevant files by feature intent.
        
        Args:
            intent: Feature description or search query
            limit: Maximum results to return
        
        Returns:
            List of files with path, relevance score, and content summary
        """
        try:
            # Try lat query command (if available via MCP)
            result = subprocess.run(
                ["lat", "query", "files", intent, "--limit", str(limit)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Fallback: parse as newline-delimited results
                    files = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            files.append({"path": line, "relevance": "unknown"})
                    return files
            
            return []
        except Exception as e:
            click.echo(f"⚠ lat files query failed: {e}", err=True)
            return []
    
    def query_functions(self, intent: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query for relevant functions/methods.
        
        Args:
            intent: Function name or search query
            limit: Maximum results to return
        
        Returns:
            List of functions with file, line, and signature
        """
        try:
            result = subprocess.run(
                ["lat", "query", "functions", intent, "--limit", str(limit)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    functions = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            functions.append({"signature": line, "file": "unknown"})
                    return functions
            
            return []
        except Exception as e:
            click.echo(f"⚠ lat functions query failed: {e}", err=True)
            return []
    
    def query_impact(self, file_path: str) -> Dict[str, Any]:
        """Query impact of changes to a file.
        
        Args:
            file_path: Path to file
        
        Returns:
            Dict with callers, dependencies, references
        """
        try:
            result = subprocess.run(
                ["lat", "query", "impact", file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {
                        "file": file_path,
                        "callers": [],
                        "dependencies": [],
                        "impact": "unknown"
                    }
            
            return {}
        except Exception as e:
            click.echo(f"⚠ lat impact query failed: {e}", err=True)
            return {}
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of indexed codebase.
        
        Returns:
            Dict with file count, function count, and last sync time
        """
        try:
            result = subprocess.run(
                ["lat", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"status": result.stdout.strip()}
            
            return {"status": "unavailable"}
        except Exception as e:
            return {"status": f"error: {e}"}


def load_index(project_path: str = ".") -> LatMdIndex:
    """Load or initialize lat.md index.
    
    Args:
        project_path: Path to project root
    
    Returns:
        LatMdIndex instance
    """
    index = LatMdIndex(project_path)
    index.ensure_index()
    return index


def query_relevant_context(
    intent: str,
    project_path: str = ".",
    max_files: int = 3,
    max_functions: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """Query for all relevant context (files, functions) for an intent.
    
    Args:
        intent: Feature description or task description
        project_path: Path to project root
        max_files: Maximum files to return
        max_functions: Maximum functions to return
    
    Returns:
        Dict with 'files' and 'functions' keys, each containing list of results
    """
    index = load_index(project_path)
    
    return {
        "files": index.query_files(intent, limit=max_files),
        "functions": index.query_functions(intent, limit=max_functions),
    }
