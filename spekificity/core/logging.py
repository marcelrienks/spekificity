"""Comprehensive logging across Spekificity components.

Structured logging for debugging and audit trail.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json


class SpekLogger:
    """Structured logging for Spekificity."""

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    def __init__(self, name: str, log_dir: str = ".specify/logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Console logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # File handler
        log_file = self.log_dir / f"{name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str, **context):
        """Log debug message.

        Args:
            message: Message
            context: Additional context dict
        """
        if context:
            self.logger.debug(f"{message} | {json.dumps(context)}")
        else:
            self.logger.debug(message)

    def info(self, message: str, **context):
        """Log info message."""
        if context:
            self.logger.info(f"{message} | {json.dumps(context)}")
        else:
            self.logger.info(message)

    def warning(self, message: str, **context):
        """Log warning message."""
        if context:
            self.logger.warning(f"{message} | {json.dumps(context)}")
        else:
            self.logger.warning(message)

    def error(self, message: str, exception: Exception = None, **context):
        """Log error message."""
        if exception:
            self.logger.error(f"{message}: {exception}", exc_info=True)
        elif context:
            self.logger.error(f"{message} | {json.dumps(context)}")
        else:
            self.logger.error(message)

    def event(self, event_type: str, details: Dict[str, Any]):
        """Log structured event.

        Args:
            event_type: Event type (prepare_start, plan_complete, etc.)
            details: Event details dict
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details
        }
        self.logger.info(f"EVENT: {json.dumps(event)}")

    def get_logs(self) -> str:
        """Get all logs for this logger.

        Returns:
            Log file contents
        """
        log_file = self.log_dir / f"{self.name}.log"
        if log_file.exists():
            return log_file.read_text()
        return ""


# Global logger instances
_loggers: Dict[str, SpekLogger] = {}


def get_logger(name: str) -> SpekLogger:
    """Get or create logger instance.

    Args:
        name: Logger name

    Returns:
        SpekLogger instance
    """
    if name not in _loggers:
        _loggers[name] = SpekLogger(name)
    return _loggers[name]


def log_workflow_start(feature_name: str, stage: str):
    """Log workflow stage start.

    Args:
        feature_name: Feature name
        stage: Stage name (prepare, plan, implement, conclude)
    """
    logger = get_logger("workflow")
    logger.event(f"{stage}_start", {
        "feature": feature_name,
        "stage": stage,
        "timestamp": datetime.now().isoformat()
    })


def log_workflow_complete(feature_name: str, stage: str, duration_seconds: float):
    """Log workflow stage completion.

    Args:
        feature_name: Feature name
        stage: Stage name
        duration_seconds: Duration in seconds
    """
    logger = get_logger("workflow")
    logger.event(f"{stage}_complete", {
        "feature": feature_name,
        "stage": stage,
        "duration_seconds": duration_seconds,
        "timestamp": datetime.now().isoformat()
    })


def log_task_start(task_id: str):
    """Log task start.

    Args:
        task_id: Task ID
    """
    logger = get_logger("tasks")
    logger.event("task_start", {
        "task_id": task_id,
        "timestamp": datetime.now().isoformat()
    })


def log_task_complete(task_id: str, duration_seconds: float, decision_count: int = 0):
    """Log task completion.

    Args:
        task_id: Task ID
        duration_seconds: Duration
        decision_count: Number of decisions logged
    """
    logger = get_logger("tasks")
    logger.event("task_complete", {
        "task_id": task_id,
        "duration_seconds": duration_seconds,
        "decisions_logged": decision_count,
        "timestamp": datetime.now().isoformat()
    })


def log_context_injection(task_id: str, context_size_tokens: int, duration_seconds: float):
    """Log context injection.

    Args:
        task_id: Task ID
        context_size_tokens: Context size in tokens
        duration_seconds: Injection duration
    """
    logger = get_logger("context")
    logger.event("context_injected", {
        "task_id": task_id,
        "tokens": context_size_tokens,
        "duration_seconds": duration_seconds,
        "sla_met": duration_seconds < 10,
        "timestamp": datetime.now().isoformat()
    })


def log_vault_update(operation: str, item_count: int):
    """Log vault update.

    Args:
        operation: Operation type (add_decision, add_lesson, etc.)
        item_count: Number of items added/updated
    """
    logger = get_logger("vault")
    logger.event("vault_updated", {
        "operation": operation,
        "items": item_count,
        "timestamp": datetime.now().isoformat()
    })
