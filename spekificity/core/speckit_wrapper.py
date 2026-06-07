"""SpecKit orchestration wrapper with context enrichment.

Wraps SpecKit specify/plan/implement commands and injects vault context.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import tempfile

from spekificity.integrations.speckit import (
    invoke_specify,
    invoke_plan,
    invoke_analyze,
    SpecKitError,
    check_speckit_version
)
from spekificity.core.context import ContextLoader, format_context_for_agent
from spekificity.core.types import Decision, Pattern, Task


def create_enrichment_preamble(
    decisions: List[Decision],
    patterns: List[Pattern],
    max_tokens: int = 1000
) -> str:
    """Create preamble of prior decisions and patterns for SpecKit input.

    Args:
        decisions: List of relevant decisions from vault
        patterns: List of relevant design patterns
        max_tokens: Maximum tokens for preamble

    Returns:
        Formatted preamble text for enrichment
    """
    if not decisions and not patterns:
        return ""

    preamble = "## Prior Context\n\n"

    if decisions:
        preamble += "### Prior Decisions\n\n"
        for decision in decisions[:5]:
            preamble += f"- **{decision.title}** ({decision.id}): {decision.decision}\n"
        preamble += "\n"

    if patterns:
        preamble += "### Design Patterns\n\n"
        for pattern in patterns[:5]:
            preamble += f"- **{pattern.title}** ({pattern.category}): {pattern.solution}\n"
        preamble += "\n"

    return preamble


def run_specify(
    feature_intent: str,
    project_path: str = ".",
    vault_path: str = "vault",
    output_dir: Optional[str] = None,
    use_context: bool = True,
    timeout: int = 300
) -> Dict[str, Any]:
    """Generate specification from feature intent with optional vault context.

    Args:
        feature_intent: Feature description/intent
        project_path: Project root path
        vault_path: Path to vault directory
        output_dir: Output directory for spec.md (defaults to temp dir)
        use_context: Inject vault context
        timeout: Command timeout in seconds

    Returns:
        Dict with 'spec', 'valid', 'metadata'

    Raises:
        SpecKitError: if SpecKit command fails
    """
    # Check SpecKit availability
    check_speckit_version()

    # Load vault context if requested
    enriched_intent = feature_intent
    if use_context:
        try:
            loader = ContextLoader(project_path, vault_path)
            decisions = loader.load_relevant_decisions(feature_intent, limit=5)
            patterns = loader.load_relevant_patterns(feature_intent, limit=5)

            preamble = create_enrichment_preamble(decisions, patterns)
            enriched_intent = preamble + "\n" + feature_intent
        except Exception as e:
            # Fallback to unenriched intent
            enriched_intent = feature_intent

    # Use temp dir if not specified
    if output_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="spek_specify_")
        output_dir = temp_dir

    # Invoke SpecKit
    result = invoke_specify(
        enriched_intent,
        output_dir=output_dir,
        timeout=timeout
    )

    # Validate spec if requested
    spec_file = Path(output_dir) / "spec.md"
    valid = spec_file.exists()

    return {
        "spec": result["spec"],
        "valid": valid,
        "output_dir": output_dir,
        "metadata": result.get("metadata", {})
    }


def run_plan(
    spec_content: str,
    project_path: str = ".",
    vault_path: str = "vault",
    output_dir: Optional[str] = None,
    use_context: bool = True,
    timeout: int = 300
) -> Dict[str, Any]:
    """Generate plan and tasks from specification with optional vault context.

    Args:
        spec_content: Specification Markdown content
        project_path: Project root path
        vault_path: Path to vault directory
        output_dir: Output directory for plan.md and tasks.md
        use_context: Inject vault context
        timeout: Command timeout in seconds

    Returns:
        Dict with 'plan', 'tasks', 'valid', 'metadata'

    Raises:
        SpecKitError: if SpecKit command fails
    """
    # Check SpecKit availability
    check_speckit_version()

    # Use temp dir if not specified
    if output_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="spek_plan_")
        output_dir = temp_dir

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write spec to temp file
    spec_file = output_path / "spec.md"
    spec_file.write_text(spec_content)

    # Invoke SpecKit
    result = invoke_plan(
        str(spec_file),
        output_dir=output_dir,
        timeout=timeout
    )

    # Validate output
    plan_file = output_path / "plan.md"
    tasks_file = output_path / "tasks.md"
    valid = plan_file.exists()

    return {
        "plan": result.get("plan", ""),
        "tasks": result.get("tasks", ""),
        "valid": valid,
        "output_dir": output_dir,
        "metadata": result.get("metadata", {})
    }


def run_implement(
    plan_content: str,
    project_path: str = ".",
    vault_path: str = "vault",
    task_id: str = "",
    timeout: int = 60
) -> Dict[str, Any]:
    """Get context for task implementation with vault enrichment.

    This is a reference function; actual task execution happens in /spek.implement skill.

    Args:
        plan_content: Plan Markdown content
        project_path: Project root path
        vault_path: Path to vault directory
        task_id: Task identifier
        timeout: Query timeout in seconds

    Returns:
        Dict with context for task execution

    Raises:
        ValueError: if task_id not provided
    """
    if not task_id:
        raise ValueError("task_id required for implement")

    # Load context for task
    try:
        loader = ContextLoader(project_path, vault_path)
        context = loader.load_task_context(
            task_id=task_id,
            task_description=plan_content[:500],  # Use plan summary
            max_decisions=3,
            max_patterns=3,
            max_code=3,
            working_dir=project_path
        )

        return {
            "context": format_context_for_agent(context),
            "task_id": task_id,
            "decisions": [d.dict() if hasattr(d, 'dict') else d for d in context.decisions],
            "patterns": [p.dict() if hasattr(p, 'dict') else p for p in context.patterns],
        }
    except Exception as e:
        return {
            "context": "",
            "task_id": task_id,
            "error": str(e)
        }


def validate_spec(spec_content: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Validate specification using SpecKit analyze.

    Args:
        spec_content: Specification Markdown content
        output_dir: Working directory for validation (defaults to temp)

    Returns:
        Dict with 'valid', 'analysis', 'issues' list

    Raises:
        SpecKitError: if SpecKit command fails
    """
    check_speckit_version()

    if output_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="spek_validate_")
        output_dir = temp_dir

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    spec_file = output_path / "spec.md"
    spec_file.write_text(spec_content)

    result = invoke_analyze(str(spec_file))

    return {
        "valid": result["valid"],
        "analysis": result.get("analysis", ""),
        "issues": [],  # Parse from analysis if needed
        "spec_file": str(spec_file)
    }
