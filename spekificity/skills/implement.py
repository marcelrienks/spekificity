"""Skill: /spek.implement — Execute task with context injection and progress tracking.

Executes a single task with injected context, progress logging, and decision capture.
"""

import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from spekificity.core.context import ContextLoader, format_context_for_agent
from spekificity.core.parser import TaskParser
from spekificity.core.types import ProgressLog


class TaskExecutor:
    """Executes a task with context injection and progress tracking."""

    def __init__(self, project_path: str = ".", vault_path: str = "vault"):
        self.project_path = Path(project_path)
        self.vault_path = vault_path
        self.context_loader = ContextLoader(project_path, vault_path)
        self.logs_dir = self.project_path / ".specify" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def load_task_definition(self, task_id: str, tasks_file: str = "tasks.md") -> Optional[Dict[str, Any]]:
        """Load task definition from tasks.md.

        Args:
            task_id: Task ID (e.g., "T1.1")
            tasks_file: Path to tasks.md

        Returns:
            Dict with task details or None if not found
        """
        tasks_path = Path(tasks_file)
        if not tasks_path.exists():
            return None

        content = tasks_path.read_text()
        tasks = TaskParser.parse_all(content)

        for task in tasks:
            if task.get("id") == task_id:
                return task

        return None

    def generate_context_preamble(self, task_id: str, task_description: str) -> str:
        """Generate context preamble for task execution.

        Args:
            task_id: Task ID
            task_description: Task description

        Returns:
            Formatted context Markdown
        """
        start = time.time()

        # Load context
        context = self.context_loader.load_task_context(
            task_id=task_id,
            task_description=task_description,
            max_decisions=3,
            max_patterns=2,
            max_code=3
        )

        elapsed = time.time() - start

        # Format context
        preamble = format_context_for_agent(context, compressed=False)
        preamble += f"\n\n**Context loaded in {elapsed:.1f}s**\n"

        return preamble

    def start_progress_log(self, task_id: str) -> Path:
        """Start progress log for task.

        Args:
            task_id: Task ID

        Returns:
            Path to log file
        """
        log_file = self.logs_dir / f"{task_id}.md"

        # Create or append to log
        header = f"# Progress Log: {task_id}\n\n"
        header += f"**Started:** {datetime.now().isoformat()}\n\n"

        if not log_file.exists():
            log_file.write_text(header)

        return log_file

    def log_progress(self, log_file: Path, action: str, details: str = ""):
        """Log progress to file.

        Args:
            log_file: Path to log file
            action: Action taken (started, progressed, completed, blocked)
            details: Additional details
        """
        timestamp = datetime.now().isoformat()
        entry = f"- **{timestamp}** [{action}]: {details}\n"

        current = log_file.read_text()
        log_file.write_text(current + entry)

    def execute_task(
        self,
        task_id: str,
        task_description: str,
        tasks_file: str = "tasks.md"
    ) -> Dict[str, Any]:
        """Execute task with context injection.

        Args:
            task_id: Task ID
            task_description: Task description
            tasks_file: Path to tasks.md

        Returns:
            Dict with execution result, context, and logs
        """
        start_time = time.time()

        # Load task definition
        task_def = self.load_task_definition(task_id, tasks_file)

        # Start log
        log_file = self.start_progress_log(task_id)
        self.log_progress(log_file, "started", f"Executing {task_id}")

        # Generate context (timed)
        context_start = time.time()
        context_preamble = self.generate_context_preamble(task_id, task_description)
        context_elapsed = time.time() - context_start

        self.log_progress(log_file, "context_loaded", f"Loaded in {context_elapsed:.1f}s")

        # Verify SLA
        context_ok = context_elapsed < 10  # SC-005: < 10s

        elapsed = time.time() - start_time

        return {
            "task_id": task_id,
            "success": True,
            "context_preamble": context_preamble,
            "context_elapsed": context_elapsed,
            "context_ok": context_ok,
            "total_elapsed": elapsed,
            "log_file": str(log_file),
            "task_definition": task_def,
            "next_step": "Review context above and implement task"
        }


def implement(
    task_id: str,
    project_path: str = ".",
    vault_path: str = "vault",
    tasks_file: str = "tasks.md"
) -> Dict[str, Any]:
    """Execute task with context injection and progress tracking.

    Args:
        task_id: Task ID to execute (e.g., "T1.1")
        project_path: Project root path
        vault_path: Path to vault directory
        tasks_file: Path to tasks.md

    Returns:
        Dict with context, execution metadata, and log file path
    """
    executor = TaskExecutor(project_path, vault_path)

    # Load task definition to get description
    task_def = executor.load_task_definition(task_id, tasks_file)
    if not task_def:
        return {
            "success": False,
            "error": f"Task {task_id} not found in {tasks_file}",
            "task_id": task_id
        }

    task_description = task_def.get("title", task_def.get("description", ""))

    # Execute task
    result = executor.execute_task(task_id, task_description, tasks_file)

    return result


def conclude_task(
    task_id: str,
    changes_summary: str,
    decisions_logged: List[str] = None,
    project_path: str = ".",
    vault_path: str = "vault"
) -> Dict[str, Any]:
    """Mark task complete and log summary.

    Args:
        task_id: Task ID
        changes_summary: Summary of changes made
        decisions_logged: List of decision IDs logged
        project_path: Project root path
        vault_path: Path to vault directory

    Returns:
        Dict with completion details
    """
    executor = TaskExecutor(project_path, vault_path)

    log_file = executor.logs_dir / f"{task_id}.md"

    # Log completion
    executor.log_progress(log_file, "completed", f"Task completed")
    executor.log_progress(log_file, "summary", changes_summary)

    if decisions_logged:
        for dec_id in decisions_logged:
            executor.log_progress(log_file, "decision_logged", dec_id)

    # Add completion timestamp
    completion_entry = f"\n**Completed:** {datetime.now().isoformat()}\n"
    current = log_file.read_text()
    log_file.write_text(current + completion_entry)

    return {
        "success": True,
        "task_id": task_id,
        "log_file": str(log_file),
        "changes_summary": changes_summary,
        "decisions_logged_count": len(decisions_logged or [])
    }
