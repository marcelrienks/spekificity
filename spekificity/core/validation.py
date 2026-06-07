"""Validation logic for specifications and plans.

Checks testability, measurability, and task dependencies.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from spekificity.core.types import Specification, Plan, Task


@dataclass
class ValidationError:
    """Validation error with severity and remediation hint."""
    severity: str  # "error", "warning"
    field: str  # spec, plan, task
    message: str
    remediation: Optional[str] = None
    line_number: Optional[int] = None


class SpecValidator:
    """Validate specification quality and completeness."""

    VAGUE_WORDS = {
        "should", "maybe", "might", "could", "try", "attempt",
        "possibly", "perhaps", "apparently", "seemingly"
    }

    MEASURABLE_KEYWORDS = {
        "<", ">", "<=", ">=", "==", "!=", "%", "seconds", "minutes",
        "hours", "days", "count", "number", "at least", "no more than",
        "maximum", "minimum", "threshold"
    }

    @staticmethod
    def check_requirement_testability(requirement: str) -> Tuple[bool, Optional[str]]:
        """Check if requirement is testable (not vague).

        Args:
            requirement: Requirement text

        Returns:
            Tuple of (is_testable, issue_message)
        """
        lower = requirement.lower()

        # Check for vague language
        for vague in SpecValidator.VAGUE_WORDS:
            if re.search(rf'\b{vague}\b', lower):
                return False, f"Vague word '{vague}' found"

        # Check it's not just "this" or "it"
        if requirement.strip() in ["this", "it", "these", "those"]:
            return False, "Requirement is empty/incomplete"

        # Positive signal: has action verb + object
        if len(requirement.split()) < 3:
            return False, "Requirement too short to be testable"

        return True, None

    @staticmethod
    def check_success_criteria_measurable(criteria: str) -> Tuple[bool, Optional[str]]:
        """Check if success criterion is measurable.

        Args:
            criteria: Success criteria text

        Returns:
            Tuple of (is_measurable, issue_message)
        """
        # Check for numeric/measurable keywords
        has_measurable = any(
            keyword in criteria.lower()
            for keyword in SpecValidator.MEASURABLE_KEYWORDS
        )

        if not has_measurable:
            # Check for pass/fail or yes/no
            criteria_lower = criteria.lower()
            if not any(kw in criteria_lower for kw in ["pass", "fail", "yes", "no", "valid", "invalid"]):
                return False, "No measurable target found (e.g., < 5s, 80%, pass/fail)"

        return True, None

    @staticmethod
    def validate_spec(spec_data: Dict[str, Any]) -> List[ValidationError]:
        """Validate specification completeness and quality.

        Args:
            spec_data: Spec dict from parser

        Returns:
            List of ValidationError objects (empty if valid)
        """
        errors = []

        # Check required fields
        if not spec_data.get("title"):
            errors.append(ValidationError("error", "spec", "Title is required"))

        # Check user stories exist
        if not spec_data.get("user_stories"):
            errors.append(ValidationError("warning", "spec", "No user stories defined"))

        # Check requirements testability
        for i, req in enumerate(spec_data.get("requirements", [])):
            is_testable, issue = SpecValidator.check_requirement_testability(req)
            if not is_testable:
                errors.append(ValidationError(
                    "warning", "spec", f"Requirement {i+1} may not be testable: {issue}",
                    remediation="Rewrite requirement with clear action and measurable outcome"
                ))

        # Check success criteria measurability
        for i, criteria in enumerate(spec_data.get("success_criteria", [])):
            is_measurable, issue = SpecValidator.check_success_criteria_measurable(criteria)
            if not is_measurable:
                errors.append(ValidationError(
                    "warning", "spec", f"Criterion {i+1} may not be measurable: {issue}",
                    remediation="Add quantifiable targets (e.g., < 30 seconds, > 80%)"
                ))

        # Check assumptions exist for ambiguities
        if not spec_data.get("assumptions"):
            errors.append(ValidationError(
                "warning", "spec", "No assumptions documented",
                remediation="Document assumptions about dependencies, scope, and constraints"
            ))

        return errors


class PlanValidator:
    """Validate plan quality and task organization."""

    @staticmethod
    def check_task_dependencies(tasks: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
        """Check for circular task dependencies.

        Args:
            tasks: List of task dicts with 'id' and 'dependencies' fields

        Returns:
            Tuple of (no_cycles, issue_message)
        """
        # Build dependency graph
        graph = {}
        for task in tasks:
            task_id = task.get("id", "")
            deps = task.get("dependencies", [])
            graph[task_id] = deps

        # DFS for cycles
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for task_id in graph:
            if task_id not in visited:
                if has_cycle(task_id):
                    return False, "Circular dependency detected"

        return True, None

    @staticmethod
    def validate_plan(plan_data: Dict[str, Any], tasks: List[Dict[str, Any]]) -> List[ValidationError]:
        """Validate plan and task organization.

        Args:
            plan_data: Plan dict
            tasks: List of task dicts

        Returns:
            List of ValidationError objects
        """
        errors = []

        # Check required fields
        if not plan_data.get("architecture"):
            errors.append(ValidationError("warning", "plan", "No architecture section"))

        if not plan_data.get("tech_stack"):
            errors.append(ValidationError("warning", "plan", "Technology stack not defined"))

        # Check tasks exist
        if not tasks:
            errors.append(ValidationError("error", "plan", "No tasks defined"))
            return errors

        # Check for circular dependencies
        no_cycles, cycle_msg = PlanValidator.check_task_dependencies(tasks)
        if not no_cycles:
            errors.append(ValidationError("error", "plan", cycle_msg))

        # Check task scope (hours and tokens)
        for task in tasks:
            hours = task.get("estimated_hours", 0)
            if hours > 4:
                errors.append(ValidationError(
                    "warning", "plan",
                    f"Task {task.get('id')} estimated at {hours}h (consider breaking down)",
                    remediation="Split large tasks into smaller, independently testable units"
                ))

            tokens = task.get("estimated_tokens", 0)
            if tokens > 10000:
                errors.append(ValidationError(
                    "warning", "plan",
                    f"Task {task.get('id')} estimated at {tokens} tokens (may be too large)"
                ))

        # Check task count reasonable
        if len(tasks) < 3:
            errors.append(ValidationError("warning", "plan", "Plan has very few tasks (< 3)"))
        if len(tasks) > 50:
            errors.append(ValidationError("warning", "plan", "Plan has many tasks (> 50); consider consolidation"))

        return errors


def validate_spec(spec_data: Dict[str, Any]) -> List[ValidationError]:
    """Validate specification (convenience function).

    Args:
        spec_data: Spec dict from parser

    Returns:
        List of ValidationError objects
    """
    return SpecValidator.validate_spec(spec_data)


def validate_plan(plan_data: Dict[str, Any], tasks: List[Dict[str, Any]] = None) -> List[ValidationError]:
    """Validate plan (convenience function).

    Args:
        plan_data: Plan dict
        tasks: Optional list of task dicts

    Returns:
        List of ValidationError objects
    """
    tasks = tasks or []
    return PlanValidator.validate_plan(plan_data, tasks)


def summarize_validation(errors: List[ValidationError]) -> Dict[str, Any]:
    """Summarize validation results.

    Args:
        errors: List of ValidationError objects

    Returns:
        Dict with counts, severity breakdown, and summary
    """
    severity_counts = {"error": 0, "warning": 0}
    for error in errors:
        severity_counts[error.severity] += 1

    return {
        "total_issues": len(errors),
        "errors": severity_counts["error"],
        "warnings": severity_counts["warning"],
        "can_proceed": severity_counts["error"] == 0,
        "errors_list": errors
    }
