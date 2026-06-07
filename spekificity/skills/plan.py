"""Skill: /spek.plan — Generate spec, plan, and tasks.

Orchestrates SpecKit to generate specification and implementation plan from feature description.
"""

import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from spekificity.core.speckit_wrapper import run_specify, run_plan, validate_spec
from spekificity.core.context import ContextLoader
from spekificity.core.parser import SpecParser, PlanParser, TaskParser
from spekificity.core.enrichment import EnrichmentFormatter


class PlanGenerator:
    """Generates spec and plan from feature description."""

    def __init__(self, project_path: str = ".", vault_path: str = "vault"):
        self.project_path = Path(project_path)
        self.vault_path = vault_path
        self.context_loader = ContextLoader(project_path, vault_path)
        self.enricher = EnrichmentFormatter(max_decisions=3, max_patterns=2)

    def detect_ambiguities(self, spec_content: str) -> List[str]:
        """Detect ambiguities in specification.

        Args:
            spec_content: Specification Markdown

        Returns:
            List of ambiguity descriptions (max 3)
        """
        ambiguities = []

        # Look for placeholder text or vague markers
        vague_markers = [
            "unclear", "ambiguous", "tbd", "to be determined",
            "needs clarification", "uncertain", "possibly", "maybe"
        ]

        lines = spec_content.split("\n")
        for i, line in enumerate(lines):
            lower = line.lower()
            for marker in vague_markers:
                if marker in lower:
                    ambiguities.append(f"Line {i+1}: {line.strip()[:80]}")

        return ambiguities[:3]

    def generate_spec(self, feature_intent: str) -> Dict[str, Any]:
        """Generate specification using SpecKit.

        Args:
            feature_intent: Feature description

        Returns:
            Dict with spec_content, parsed_spec, metadata
        """
        # Load enrichment context
        decisions = self.context_loader.load_relevant_decisions(feature_intent, limit=3)
        patterns = self.context_loader.load_relevant_patterns(feature_intent, limit=2)

        # Generate enriched input
        enriched_intent = self.enricher.enrich_specify_input(
            feature_intent,
            decisions,
            patterns
        )

        # Call SpecKit
        result = run_specify(
            enriched_intent,
            project_path=str(self.project_path),
            vault_path=self.vault_path,
            use_context=False  # Already enriched above
        )

        # Parse spec
        parsed = SpecParser.parse(result["spec"])

        # Detect ambiguities
        ambiguities = self.detect_ambiguities(result["spec"])

        return {
            "spec_content": result["spec"],
            "parsed_spec": parsed,
            "ambiguities": ambiguities,
            "valid": result["valid"]
        }

    def generate_plan(self, spec_content: str) -> Dict[str, Any]:
        """Generate plan and tasks using SpecKit.

        Args:
            spec_content: Specification Markdown

        Returns:
            Dict with plan_content, tasks, metadata
        """
        # Call SpecKit plan
        result = run_plan(
            spec_content,
            project_path=str(self.project_path),
            vault_path=self.vault_path
        )

        # Parse plan and tasks
        parsed_plan = PlanParser.parse(result["plan"])
        parsed_tasks = TaskParser.parse_all(result["tasks"])

        return {
            "plan_content": result["plan"],
            "tasks_content": result["tasks"],
            "parsed_plan": parsed_plan,
            "parsed_tasks": parsed_tasks,
            "valid": result["valid"]
        }

    def generate_full_workflow(self, feature_intent: str) -> Dict[str, Any]:
        """Complete workflow: feature intent → spec → plan → tasks.

        Args:
            feature_intent: Feature description

        Returns:
            Dict with all outputs (spec, plan, tasks)
        """
        start = time.time()

        # Generate spec
        spec_result = self.generate_spec(feature_intent)

        # Generate plan from spec
        plan_result = self.generate_plan(spec_result["spec_content"])

        elapsed = time.time() - start

        return {
            "feature_intent": feature_intent,
            "spec": spec_result,
            "plan": plan_result,
            "elapsed_seconds": elapsed,
            "meets_sla": elapsed < 180,  # 3 minutes
            "actionable_items": len(plan_result["parsed_tasks"])
        }


def plan(
    feature_intent: str,
    project_path: str = ".",
    vault_path: str = "vault",
    output_dir: Optional[str] = None,
    interactive: bool = False
) -> Dict[str, Any]:
    """Generate spec, plan, and tasks from feature description.

    Args:
        feature_intent: Feature description
        project_path: Project root path
        vault_path: Path to vault directory
        output_dir: Directory to write outputs (defaults to specs/feature_name)
        interactive: Prompt for clarifications

    Returns:
        Dict with spec, plan, tasks, and metadata
    """
    generator = PlanGenerator(project_path, vault_path)
    result = generator.generate_full_workflow(feature_intent)

    # Write outputs if directory specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        spec_file = output_path / "spec.md"
        spec_file.write_text(result["spec"]["spec_content"])

        plan_file = output_path / "plan.md"
        plan_file.write_text(result["plan"]["plan_content"])

        tasks_file = output_path / "tasks.md"
        tasks_file.write_text(result["plan"]["tasks_content"])

        result["output_dir"] = str(output_path)
        result["files"] = {
            "spec": str(spec_file),
            "plan": str(plan_file),
            "tasks": str(tasks_file)
        }

    # Handle ambiguities if interactive
    if interactive and result["spec"]["ambiguities"]:
        result["ambiguities_found"] = len(result["spec"]["ambiguities"])
        result["action_needed"] = "Review and clarify ambiguities"

    return result
