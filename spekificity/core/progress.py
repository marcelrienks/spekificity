"""Task progress tracking and logging.

Manages progress log lifecycle: creation, updates, completion, rollback.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json


class ProgressLogger:
    """Task progress tracking with idempotent operations."""

    def __init__(self, logs_dir: str = ".specify/logs"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def get_log_path(self, task_id: str) -> Path:
        """Get path for task log file.

        Args:
            task_id: Task ID

        Returns:
            Path to log file
        """
        return self.logs_dir / f"{task_id}.md"

    def start_task(
        self,
        task_id: str,
        task_description: str,
        priority: str = "P2",
        estimated_hours: float = 2.0
    ) -> Path:
        """Start task and create progress log.

        Args:
            task_id: Task ID
            task_description: Task description
            priority: Priority level
            estimated_hours: Estimated hours to complete

        Returns:
            Path to log file
        """
        log_path = self.get_log_path(task_id)

        if log_path.exists():
            return log_path  # Idempotent: return existing

        # Create frontmatter
        frontmatter = {
            "task_id": task_id,
            "description": task_description,
            "priority": priority,
            "estimated_hours": estimated_hours,
            "status": "in-progress",
            "started_at": datetime.now().isoformat(),
            "ended_at": None,
            "completed": False
        }

        # Format as Markdown frontmatter
        content = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, str):
                content += f'{key}: "{value}"\n'
            else:
                content += f"{key}: {value}\n"
        content += "---\n\n"
        content += f"# {task_id}: {task_description}\n\n"
        content += "## Progress Log\n\n"

        log_path.write_text(content)
        return log_path

    def log_progress(
        self,
        task_id: str,
        message: str,
        level: str = "info"
    ) -> bool:
        """Log progress entry.

        Args:
            task_id: Task ID
            message: Progress message
            level: Log level (info, warning, error, decision)

        Returns:
            True if logged successfully
        """
        log_path = self.get_log_path(task_id)

        if not log_path.exists():
            # Create if doesn't exist
            self.start_task(task_id, "Task")

        # Append entry
        timestamp = datetime.now().isoformat()
        entry = f"- **{timestamp}** [{level.upper()}] {message}\n"

        current = log_path.read_text()
        log_path.write_text(current + entry)

        return True

    def log_decision(self, task_id: str, decision: str, rationale: str = "") -> bool:
        """Log decision made during task.

        Args:
            task_id: Task ID
            decision: Decision text
            rationale: Rationale for decision

        Returns:
            True if logged
        """
        message = decision
        if rationale:
            message += f" (rationale: {rationale})"

        return self.log_progress(task_id, message, level="decision")

    def mark_complete(self, task_id: str, summary: str = "") -> bool:
        """Mark task complete.

        Args:
            task_id: Task ID
            summary: Completion summary

        Returns:
            True if marked
        """
        log_path = self.get_log_path(task_id)

        if not log_path.exists():
            return False

        # Update frontmatter
        content = log_path.read_text()
        lines = content.split("\n")

        # Find end of frontmatter
        fm_end = next((i for i, line in enumerate(lines) if line.startswith("---") and i > 0), -1)

        if fm_end == -1:
            return False

        # Update frontmatter fields
        new_lines = []
        for i, line in enumerate(lines):
            if i <= fm_end:
                if line.startswith("status:"):
                    new_lines.append('status: "completed"')
                elif line.startswith("completed:"):
                    new_lines.append("completed: true")
                elif line.startswith("ended_at:"):
                    new_lines.append(f'ended_at: "{datetime.now().isoformat()}"')
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Add completion entry
        completion_entry = f"\n## Completion\n\n- **{datetime.now().isoformat()}** Task completed\n"
        if summary:
            completion_entry += f"\n**Summary:**\n{summary}\n"

        new_lines.append(completion_entry)

        log_path.write_text("\n".join(new_lines))

        return True

    def mark_rollback(self, task_id: str, reason: str = "") -> Path:
        """Mark task as rolled back.

        Args:
            task_id: Task ID
            reason: Rollback reason

        Returns:
            Path to rolled back log
        """
        log_path = self.get_log_path(task_id)

        if not log_path.exists():
            return log_path

        # Append rollback note
        rollback_entry = f"\n## Rollback\n\n- **{datetime.now().isoformat()}** Task rolled back"
        if reason:
            rollback_entry += f": {reason}"
        rollback_entry += "\n"

        current = log_path.read_text()
        log_path.write_text(current + rollback_entry)

        # Archive log
        archived_path = self.logs_dir / f"{task_id}.rolled-back.md"
        archived_path.write_text(current)

        return archived_path

    def get_log_content(self, task_id: str) -> Optional[str]:
        """Get full log content.

        Args:
            task_id: Task ID

        Returns:
            Log content or None
        """
        log_path = self.get_log_path(task_id)
        if log_path.exists():
            return log_path.read_text()
        return None

    def list_logs(self) -> Dict[str, Path]:
        """List all progress logs.

        Returns:
            Dict mapping task_id to log path
        """
        logs = {}
        for log_file in self.logs_dir.glob("*.md"):
            if not ".rolled-back" in log_file.name:
                task_id = log_file.stem
                logs[task_id] = log_file
        return logs
