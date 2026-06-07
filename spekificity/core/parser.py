"""Markdown parsing for SpecKit-generated specs, plans, and tasks.

Parses Markdown output from SpecKit into typed Pydantic models.
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml

from spekificity.core.types import Spec, Plan, Task


class MarkdownParser:
    """Parse Markdown documents into typed models."""

    @staticmethod
    def extract_frontmatter(markdown_text: str) -> tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and body from Markdown.

        Args:
            markdown_text: Markdown content with optional YAML frontmatter

        Returns:
            Tuple of (frontmatter dict, body text)
        """
        if not markdown_text.startswith("---"):
            return {}, markdown_text

        lines = markdown_text.split("\n")
        try:
            end_idx = next(i for i in range(1, len(lines)) if lines[i].startswith("---"))
            frontmatter_text = "\n".join(lines[1:end_idx])
            body = "\n".join(lines[end_idx + 1:])

            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
            except yaml.YAMLError:
                frontmatter = {}

            return frontmatter, body
        except StopIteration:
            return {}, markdown_text

    @staticmethod
    def extract_section(markdown_text: str, section_name: str, level: int = 2) -> str:
        """Extract content of a Markdown section.

        Args:
            markdown_text: Markdown content
            section_name: Section heading to find
            level: Heading level (2 for ##, 3 for ###, etc.)

        Returns:
            Section content (without heading)
        """
        heading = "#" * level + f" {section_name}"
        if heading not in markdown_text:
            return ""

        lines = markdown_text.split("\n")
        start_idx = next(
            (i for i, line in enumerate(lines) if line.strip() == heading),
            -1
        )

        if start_idx == -1:
            return ""

        # Find next heading at same or higher level
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith("#" * level) and not line.startswith("#" * (level + 1)):
                end_idx = i
                break

        content = "\n".join(lines[start_idx + 1:end_idx]).strip()
        return content

    @staticmethod
    def extract_list_items(text: str) -> List[str]:
        """Extract list items from Markdown text.

        Args:
            text: Markdown text with list items

        Returns:
            List of item contents
        """
        items = []
        for line in text.split("\n"):
            if line.strip().startswith("- ") or line.strip().startswith("* "):
                item = line.strip()[2:].strip()
                items.append(item)
        return items


class SpecParser(MarkdownParser):
    """Parse Spec Markdown into Spec model."""

    @staticmethod
    def parse(markdown_text: str) -> Dict[str, Any]:
        """Parse spec.md into Spec model data.

        Args:
            markdown_text: spec.md Markdown content

        Returns:
            Dict matching Spec model fields
        """
        frontmatter, body = SpecParser.extract_frontmatter(markdown_text)

        # Extract sections
        user_stories = SpecParser.extract_section(body, "User Stories", level=2)
        requirements = SpecParser.extract_section(body, "Requirements", level=2)
        entities = SpecParser.extract_section(body, "Entities", level=2)
        success_criteria = SpecParser.extract_section(body, "Success Criteria", level=2)
        assumptions = SpecParser.extract_section(body, "Assumptions", level=2)

        return {
            "title": frontmatter.get("title", "Untitled"),
            "branch": frontmatter.get("branch", ""),
            "created": frontmatter.get("created", ""),
            "user_stories": SpecParser.extract_list_items(user_stories),
            "requirements": SpecParser.extract_list_items(requirements),
            "entities": SpecParser.extract_list_items(entities),
            "success_criteria": SpecParser.extract_list_items(success_criteria),
            "assumptions": SpecParser.extract_list_items(assumptions),
        }


class PlanParser(MarkdownParser):
    """Parse Plan Markdown into Plan model."""

    @staticmethod
    def parse(markdown_text: str) -> Dict[str, Any]:
        """Parse plan.md into Plan model data.

        Args:
            markdown_text: plan.md Markdown content

        Returns:
            Dict matching Plan model fields
        """
        frontmatter, body = PlanParser.extract_frontmatter(markdown_text)

        # Extract sections
        architecture = PlanParser.extract_section(body, "Architecture", level=2)
        tech_stack = PlanParser.extract_section(body, "Technology Stack", level=2)
        sequencing = PlanParser.extract_section(body, "Sequencing", level=2)
        risks = PlanParser.extract_section(body, "Risks & Mitigations", level=2)

        return {
            "spec_branch": frontmatter.get("spec_branch", ""),
            "spec_file": frontmatter.get("spec_file", ""),
            "architecture": architecture,
            "tech_stack": PlanParser.extract_list_items(tech_stack),
            "sequencing": sequencing,
            "risks": PlanParser.extract_list_items(risks),
            "phases": [],  # Parse from sequencing if structured
        }


class TaskParser(MarkdownParser):
    """Parse Task items from tasks.md list."""

    @staticmethod
    def parse_task_item(task_text: str) -> Dict[str, Any]:
        """Parse single task item.

        Args:
            task_text: Task list item text (e.g., "T1.1 [CODE] ...")

        Returns:
            Dict with parsed task fields
        """
        # Match pattern: T1.1 [TAG] Description
        match = re.match(r"T(\d+\.\d+)\s*\[([^\]]+)\]\s*(.*)", task_text)

        if not match:
            return {
                "id": "",
                "tags": [],
                "title": task_text,
                "priority": "P3",
            }

        task_id = f"T{match.group(1)}"
        tags = [t.strip() for t in match.group(2).split(",")]
        title = match.group(3).strip()

        return {
            "id": task_id,
            "tags": tags,
            "title": title,
            "priority": "P3",  # Parse from title if present
        }

    @staticmethod
    def parse_all(tasks_markdown: str) -> List[Dict[str, Any]]:
        """Parse all tasks from tasks.md.

        Args:
            tasks_markdown: tasks.md Markdown content

        Returns:
            List of task dicts
        """
        tasks = []
        items = TaskParser.extract_list_items(tasks_markdown)

        for item in items:
            task = TaskParser.parse_task_item(item)
            if task["id"]:
                tasks.append(task)

        return tasks


def parse_spec(markdown_text: str) -> Dict[str, Any]:
    """Parse spec.md into dict (convenience function).

    Args:
        markdown_text: spec.md Markdown content

    Returns:
        Dict with spec fields
    """
    return SpecParser.parse(markdown_text)


def parse_plan(markdown_text: str) -> Dict[str, Any]:
    """Parse plan.md into dict (convenience function).

    Args:
        markdown_text: plan.md Markdown content

    Returns:
        Dict with plan fields
    """
    return PlanParser.parse(markdown_text)


def parse_tasks(tasks_markdown: str) -> List[Dict[str, Any]]:
    """Parse tasks.md into list of task dicts (convenience function).

    Args:
        tasks_markdown: tasks.md Markdown content

    Returns:
        List of task dicts
    """
    return TaskParser.parse_all(tasks_markdown)
