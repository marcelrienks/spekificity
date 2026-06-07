"""Context loading and injection for task execution.

Loads relevant decisions, patterns, code examples, and injects into agent session.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from spekificity.core.types import TaskContext, CodeContext, Decision, Pattern
from spekificity.core.vault import Vault
from spekificity.integrations.lat_md import LatMdIndex, query_relevant_context as lat_query
from spekificity.integrations.semantic_search import SemanticSearcher, search_relevant_context as fallback_query


class ContextLoader:
    """Load and manage context for task execution."""
    
    def __init__(self, project_path: str = ".", vault_path: str = "vault"):
        self.project_path = Path(project_path)
        self.vault = Vault(vault_path)
        self.lat_index = LatMdIndex(project_path)
        self.searcher = SemanticSearcher(project_path)
    
    def load_relevant_decisions(self, intent: str, limit: int = 3) -> List[Decision]:
        """Load decisions relevant to task intent.
        
        Args:
            intent: Task description
            limit: Maximum decisions to load
        
        Returns:
            List of relevant Decision objects
        """
        all_decisions = self.vault.load_decisions()
        
        # Simple matching: decisions whose title or content matches intent terms
        relevant = []
        intent_terms = set(intent.lower().split())
        
        for decision_dict in all_decisions:
            title = decision_dict.get("title", "").lower()
            content = " ".join([
                decision_dict.get("decision", ""),
                decision_dict.get("rationale", "")
            ]).lower()
            
            # Count matching terms
            matches = len(intent_terms & set(content.split()))
            if matches > 0:
                decision = Decision(**decision_dict)
                relevant.append((decision, matches))
        
        # Sort by relevance (match count)
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [d for d, _ in relevant[:limit]]
    
    def load_relevant_patterns(self, intent: str, limit: int = 3) -> List[Pattern]:
        """Load design patterns relevant to task intent.
        
        Args:
            intent: Task description
            limit: Maximum patterns to load
        
        Returns:
            List of relevant Pattern objects
        """
        all_patterns = self.vault.load_patterns()
        
        # Simple matching: patterns whose title matches intent terms
        relevant = []
        intent_terms = set(intent.lower().split())
        
        for pattern_dict in all_patterns:
            title = pattern_dict.get("title", "").lower()
            category = pattern_dict.get("category", "").lower()
            
            # Check for term matches
            matches = len(intent_terms & set((title + " " + category).split()))
            if matches > 0:
                pattern = Pattern(**pattern_dict)
                relevant.append((pattern, matches))
        
        # Sort by relevance
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [p for p, _ in relevant[:limit]]
    
    def load_relevant_code(self, intent: str, limit: int = 3, use_fallback: bool = True) -> List[CodeContext]:
        """Load relevant code sections for task intent.
        
        Args:
            intent: Task description
            limit: Maximum code sections
            use_fallback: Use semantic search if lat.md unavailable
        
        Returns:
            List of CodeContext objects with file paths and snippets
        """
        code_contexts = []
        
        try:
            # Try lat.md first
            lat_results = lat_query(intent, project_path=str(self.project_path), max_files=limit)
            
            for file_result in lat_results.get("files", []):
                file_path = file_result.get("path", "")
                if file_path:
                    try:
                        file_obj = Path(file_path)
                        if file_obj.exists():
                            snippet = file_obj.read_text()[:500]  # First 500 chars
                            code_contexts.append(CodeContext(
                                file_path=file_path,
                                snippet=snippet,
                                relevance=file_result.get("relevance", "medium")
                            ))
                    except Exception:
                        pass
        except Exception as e:
            # lat.md unavailable, try fallback
            if use_fallback:
                code_contexts = self._load_with_fallback(intent, limit)
        
        return code_contexts[:limit]
    
    def _load_with_fallback(self, intent: str, limit: int) -> List[CodeContext]:
        """Load code using fallback semantic search."""
        code_contexts = []
        
        try:
            results = fallback_query(intent, project_path=str(self.project_path), max_files=limit)
            
            for file_result in results.get("files", []):
                file_path = file_result.get("path", "")
                if file_path:
                    try:
                        file_obj = Path(file_path)
                        if file_obj.exists():
                            snippet = file_obj.read_text()[:500]
                            code_contexts.append(CodeContext(
                                file_path=file_path,
                                snippet=snippet,
                                relevance="fallback"
                            ))
                    except Exception:
                        pass
        except Exception as e:
            pass
        
        return code_contexts[:limit]
    
    def load_task_context(
        self,
        task_id: str,
        task_description: str,
        max_decisions: int = 3,
        max_patterns: int = 3,
        max_code: int = 3,
        working_dir: str = ""
    ) -> TaskContext:
        """Load complete context for a task.
        
        Args:
            task_id: Task identifier
            task_description: Task description
            max_decisions: Maximum decisions to load
            max_patterns: Maximum patterns to load
            max_code: Maximum code sections to load
            working_dir: Working directory for task
        
        Returns:
            TaskContext with all relevant information
        """
        decisions = self.load_relevant_decisions(task_description, limit=max_decisions)
        patterns = self.load_relevant_patterns(task_description, limit=max_patterns)
        code = self.load_relevant_code(task_description, limit=max_code)
        
        return TaskContext(
            task_id=task_id,
            task_description=task_description,
            decisions=decisions,
            patterns=patterns,
            code=code,
            working_directory=working_dir or str(self.project_path),
        )


def format_context_for_agent(context: TaskContext, compressed: bool = False) -> str:
    """Format TaskContext as markdown for agent consumption.
    
    Args:
        context: TaskContext to format
        compressed: Use minimal format (Caveman-style)
    
    Returns:
        Formatted markdown string
    """
    if compressed:
        return _format_compressed(context)
    
    output = f"# Context for {context.task_id}\n\n"
    output += f"**Task:** {context.task_description}\n\n"
    
    if context.decisions:
        output += "## Relevant Decisions\n\n"
        for decision in context.decisions:
            output += f"- **{decision.title}** ({decision.id}, {decision.status}): {decision.decision[:100]}...\n"
        output += "\n"
    
    if context.patterns:
        output += "## Relevant Patterns\n\n"
        for pattern in context.patterns:
            output += f"- **{pattern.title}** ({pattern.category}): {pattern.solution[:100]}...\n"
        output += "\n"
    
    if context.code:
        output += "## Relevant Code\n\n"
        for code in context.code:
            output += f"### {code.file_path}\n\n```\n{code.snippet}\n```\n\n"
    
    return output


def _format_compressed(context: TaskContext) -> str:
    """Minimal format for context (Caveman mode)."""
    output = f"# {context.task_id}\n\n"
    
    if context.decisions:
        output += "**Decisions:**\n"
        for d in context.decisions[:2]:
            output += f"- {d.title}\n"
        output += "\n"
    
    if context.patterns:
        output += "**Patterns:**\n"
        for p in context.patterns[:2]:
            output += f"- {p.title}\n"
        output += "\n"
    
    if context.code:
        output += "**Code:**\n"
        for c in context.code[:2]:
            output += f"- {c.file_path}\n"
    
    return output


def load_context_for_task(
    task_id: str,
    task_description: str,
    project_path: str = ".",
    vault_path: str = "vault",
    compressed: bool = False
) -> str:
    """Load and format context for a task (convenience function).
    
    Args:
        task_id: Task identifier
        task_description: Task description
        project_path: Project root path
        vault_path: Vault directory path
        compressed: Use compressed format
    
    Returns:
        Formatted context string ready for agent
    """
    loader = ContextLoader(project_path, vault_path)
    context = loader.load_task_context(
        task_id=task_id,
        task_description=task_description,
    )
    
    return format_context_for_agent(context, compressed=compressed)
