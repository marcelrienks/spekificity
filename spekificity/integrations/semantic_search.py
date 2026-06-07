"""Fallback semantic search when lat.md is unavailable.

Uses grep-based search and simple relevance scoring as fallback.
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

import click


class SemanticSearcher:
    """Fallback semantic search using grep and file analysis."""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
    
    def search_files(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for files containing query terms.
        
        Args:
            query: Search query (space-separated terms)
            limit: Maximum results
        
        Returns:
            List of matching files with relevance scores
        """
        files = []
        query_terms = query.lower().split()
        
        try:
            # Use grep to find files containing query terms
            for term in query_terms[:3]:  # Search for first 3 terms
                result = subprocess.run(
                    ["grep", "-r", "-l", "--include=*.py", "--include=*.ts", "--include=*.js", term, str(self.project_path)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    for file_path in result.stdout.strip().split('\n'):
                        if file_path and file_path not in [f["path"] for f in files]:
                            files.append({
                                "path": file_path,
                                "relevance": "medium",
                                "matched_term": term
                            })
        except Exception as e:
            click.echo(f"⚠ Semantic search failed: {e}", err=True)
        
        return files[:limit]
    
    def search_functions(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for function/method definitions.
        
        Args:
            query: Function name or pattern
            limit: Maximum results
        
        Returns:
            List of function definitions with file and line
        """
        functions = []
        
        try:
            # Search for Python functions
            result = subprocess.run(
                ["grep", "-r", "-n", "^def ", str(self.project_path), "--include=*.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if query.lower() in line.lower():
                        parts = line.split(':')
                        if len(parts) >= 3:
                            functions.append({
                                "file": parts[0],
                                "line": int(parts[1]),
                                "signature": ':'.join(parts[2:]),
                                "language": "python"
                            })
        except Exception as e:
            click.echo(f"⚠ Function search failed: {e}", err=True)
        
        return functions[:limit]
    
    def search_by_pattern(self, pattern: str, file_type: str = "*.py") -> List[Dict[str, Any]]:
        """Search using regex pattern.
        
        Args:
            pattern: Regex pattern
            file_type: File type to search (e.g., *.py, *.ts)
        
        Returns:
            List of matches with file and line
        """
        matches = []
        
        try:
            result = subprocess.run(
                ["grep", "-r", "-n", "-E", pattern, str(self.project_path), f"--include={file_type}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n')[:20]:  # Limit to 20 matches
                    if line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            matches.append({
                                "file": parts[0],
                                "line": int(parts[1]) if parts[1].isdigit() else 0,
                                "content": ':'.join(parts[2:])
                            })
        except Exception as e:
            click.echo(f"⚠ Pattern search failed: {e}", err=True)
        
        return matches


def search_relevant_context(
    intent: str,
    project_path: str = ".",
    max_files: int = 3,
    max_functions: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """Fallback search for relevant context.
    
    Args:
        intent: Feature description or task description
        project_path: Path to project root
        max_files: Maximum files to return
        max_functions: Maximum functions to return
    
    Returns:
        Dict with 'files' and 'functions' keys
    """
    searcher = SemanticSearcher(project_path)
    
    return {
        "files": searcher.search_files(intent, limit=max_files),
        "functions": searcher.search_functions(intent, limit=max_functions),
    }


def load_searcher(project_path: str = ".") -> SemanticSearcher:
    """Load semantic searcher instance.
    
    Args:
        project_path: Path to project root
    
    Returns:
        SemanticSearcher instance
    """
    return SemanticSearcher(project_path)
