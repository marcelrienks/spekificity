"""Skill: /spek.conclude — Analyze outcomes and capture lessons.

Concludes feature work by extracting lessons, updating vault, and refreshing project state.
"""

import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from spekificity.core.vault import Vault
from spekificity.core.parser import SpecParser, PlanParser, TaskParser
from spekificity.core.types import Lesson, Decision, Pattern


class FeatureConcluder:
    """Analyzes feature outcomes and updates vault."""

    def __init__(self, project_path: str = ".", vault_path: str = "vault", specs_dir: str = "specs"):
        self.project_path = Path(project_path)
        self.vault_path = vault_path
        self.specs_dir = Path(specs_dir)
        self.vault = Vault(vault_path)

    def load_feature_artifacts(self, feature_name: str) -> Dict[str, Any]:
        """Load spec, plan, tasks, and progress logs for feature.

        Args:
            feature_name: Feature name/directory

        Returns:
            Dict with artifact contents
        """
        feature_path = self.specs_dir / feature_name
        artifacts = {
            "spec": None,
            "plan": None,
            "tasks": None,
            "progress_logs": []
        }

        # Load spec
        spec_file = feature_path / "spec.md"
        if spec_file.exists():
            artifacts["spec"] = {
                "content": spec_file.read_text(),
                "parsed": SpecParser.parse(spec_file.read_text())
            }

        # Load plan
        plan_file = feature_path / "plan.md"
        if plan_file.exists():
            artifacts["plan"] = {
                "content": plan_file.read_text(),
                "parsed": PlanParser.parse(plan_file.read_text())
            }

        # Load tasks
        tasks_file = feature_path / "tasks.md"
        if tasks_file.exists():
            artifacts["tasks"] = {
                "content": tasks_file.read_text(),
                "parsed": TaskParser.parse_all(tasks_file.read_text())
            }

        # Load progress logs
        logs_dir = self.project_path / ".specify" / "logs"
        if logs_dir.exists():
            for log_file in logs_dir.glob("*.md"):
                artifacts["progress_logs"].append({
                    "file": str(log_file),
                    "content": log_file.read_text()
                })

        return artifacts

    def compare_outcomes(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        """Compare actual outcomes vs success criteria.

        Args:
            artifacts: Feature artifacts

        Returns:
            Dict with comparison results
        """
        comparison = {
            "success_criteria": [],
            "completed_tasks": 0,
            "total_tasks": 0,
            "outcomes": {}
        }

        # Extract success criteria
        if artifacts["spec"]:
            parsed_spec = artifacts["spec"]["parsed"]
            criteria = parsed_spec.get("success_criteria", [])
            comparison["success_criteria"] = criteria

        # Count completed tasks
        if artifacts["progress_logs"]:
            comparison["completed_tasks"] = len(artifacts["progress_logs"])

        if artifacts["tasks"]:
            comparison["total_tasks"] = len(artifacts["tasks"]["parsed"])

        # Calculate completion rate
        total = comparison["total_tasks"]
        if total > 0:
            completion_rate = comparison["completed_tasks"] / total
            comparison["completion_rate"] = completion_rate
            comparison["status"] = "completed" if completion_rate >= 0.8 else "partial"

        return comparison

    def extract_lessons(self, feature_name: str, artifacts: Dict[str, Any], comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Extract lessons learned from feature work.

        Args:
            feature_name: Feature name
            artifacts: Feature artifacts
            comparison: Outcome comparison

        Returns:
            Dict with lesson data
        """
        lessons_data = {
            "feature": feature_name,
            "outcomes": f"Completed {comparison['completed_tasks']}/{comparison['total_tasks']} tasks",
            "lessons": [],
            "patterns": [],
            "decisions": []
        }

        # Extract from progress logs
        if artifacts["progress_logs"]:
            for log in artifacts["progress_logs"]:
                content = log["content"]
                # Simple extraction: look for decision annotations
                lines = content.split("\n")
                for line in lines:
                    if "@decision" in line or "decision:" in line.lower():
                        lessons_data["decisions"].append(line.strip())

        # Basic lessons
        if comparison.get("completion_rate", 0) >= 0.8:
            lessons_data["lessons"].append("High task completion rate indicates well-scoped feature")
        else:
            lessons_data["lessons"].append("Partial completion suggests feature scope underestimation")

        return lessons_data

    def write_lessons_to_vault(self, lessons_data: Dict[str, Any]) -> Path:
        """Write lessons to vault.

        Args:
            lessons_data: Lesson data dict

        Returns:
            Path to lesson file written
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        feature = lessons_data["feature"].replace("/", "_")
        lesson_file = Path(self.vault_path) / "lessons" / f"{timestamp}-{feature}.md"

        lesson_file.parent.mkdir(parents=True, exist_ok=True)

        # Format as Markdown
        content = f"# Lessons: {lessons_data['feature']}\n\n"
        content += f"**Date:** {datetime.now().isoformat()}\n\n"
        content += f"## Outcomes\n\n{lessons_data['outcomes']}\n\n"

        if lessons_data["lessons"]:
            content += "## Lessons Learned\n\n"
            for lesson in lessons_data["lessons"]:
                content += f"- {lesson}\n"
            content += "\n"

        if lessons_data["patterns"]:
            content += "## Patterns Identified\n\n"
            for pattern in lessons_data["patterns"]:
                content += f"- {pattern}\n"
            content += "\n"

        if lessons_data["decisions"]:
            content += "## Decisions Made\n\n"
            for decision in lessons_data["decisions"]:
                content += f"- {decision}\n"

        lesson_file.write_text(content)

        # Also append to main lessons index
        lessons_index = Path(self.vault_path) / "lessons.md"
        if lessons_index.exists():
            current = lessons_index.read_text()
            entry = f"- [{feature}]({lesson_file.name}) — {datetime.now().strftime('%Y-%m-%d')}\n"
            lessons_index.write_text(current + entry)

        return lesson_file

    def generate_summary(self, feature_name: str, artifacts: Dict[str, Any], comparison: Dict[str, Any]) -> str:
        """Generate feature completion summary.

        Args:
            feature_name: Feature name
            artifacts: Feature artifacts
            comparison: Outcome comparison

        Returns:
            Summary Markdown
        """
        summary = f"# Feature Completion Summary: {feature_name}\n\n"
        summary += f"**Date:** {datetime.now().isoformat()}\n\n"

        # Overview
        summary += "## Overview\n\n"
        summary += f"- Tasks Completed: {comparison['completed_tasks']}/{comparison['total_tasks']}\n"
        if "completion_rate" in comparison:
            summary += f"- Completion Rate: {comparison['completion_rate']:.0%}\n"
        summary += f"- Status: {comparison.get('status', 'unknown')}\n\n"

        # Success Criteria
        if comparison["success_criteria"]:
            summary += "## Success Criteria\n\n"
            for criteria in comparison["success_criteria"][:5]:
                summary += f"- {criteria}\n"
            summary += "\n"

        # Outcomes
        summary += "## Outcomes\n\n"
        summary += f"{comparison['outcomes']}\n\n"

        return summary


def conclude(
    feature_name: str,
    project_path: str = ".",
    vault_path: str = "vault",
    specs_dir: str = "specs",
    interactive: bool = False
) -> Dict[str, Any]:
    """Conclude feature work and capture lessons.

    Args:
        feature_name: Feature name/directory
        project_path: Project root path
        vault_path: Path to vault directory
        specs_dir: Path to specs directory
        interactive: Prompt developer for additional lessons

    Returns:
        Dict with completion summary, lessons, and updated vault state
    """
    start = time.time()

    concluder = FeatureConcluder(project_path, vault_path, specs_dir)

    # Load artifacts
    artifacts = concluder.load_feature_artifacts(feature_name)

    # Compare outcomes
    comparison = concluder.compare_outcomes(artifacts)

    # Extract lessons
    lessons_data = concluder.extract_lessons(feature_name, artifacts, comparison)

    # Write to vault
    lesson_file = concluder.write_lessons_to_vault(lessons_data)

    # Generate summary
    summary = concluder.generate_summary(feature_name, artifacts, comparison)

    elapsed = time.time() - start

    return {
        "success": True,
        "feature": feature_name,
        "summary": summary,
        "lessons_written": str(lesson_file),
        "completion_rate": comparison.get("completion_rate", 0),
        "elapsed_seconds": elapsed,
        "meets_sla": elapsed < 300,  # 5 minutes
        "next_step": f"Feature complete. Lessons available for next feature via /spek.prepare"
    }
