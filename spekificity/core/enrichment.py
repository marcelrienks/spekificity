"""Enrichment layer for injecting vault context into SpecKit inputs.

Formats decisions and patterns as context for SpecKit specification and planning.
"""

from typing import List, Dict, Any, Optional
from spekificity.core.types import Decision, Pattern


class EnrichmentFormatter:
    """Format vault data as enrichment preamble for SpecKit."""

    def __init__(self, max_decisions: int = 5, max_patterns: int = 5):
        self.max_decisions = max_decisions
        self.max_patterns = max_patterns

    def format_decisions(self, decisions: List[Decision], intent: str = "") -> str:
        """Format decisions as context for SpecKit.

        Args:
            decisions: List of relevant decisions
            intent: Feature intent (for context)

        Returns:
            Formatted decisions as Markdown
        """
        if not decisions:
            return ""

        output = "## Prior Architectural Decisions\n\n"
        output += "Based on prior feature work, these decisions should inform the specification:\n\n"

        for i, decision in enumerate(decisions[:self.max_decisions], 1):
            output += f"{i}. **{decision.title}** ({decision.status})\n"
            output += f"   - Decision: {decision.decision}\n"
            output += f"   - Rationale: {decision.rationale}\n"
            if decision.implications:
                output += f"   - Implications: {', '.join(decision.implications)}\n"
            output += "\n"

        return output

    def format_patterns(self, patterns: List[Pattern], intent: str = "") -> str:
        """Format design patterns as context for SpecKit.

        Args:
            patterns: List of relevant design patterns
            intent: Feature intent (for context)

        Returns:
            Formatted patterns as Markdown
        """
        if not patterns:
            return ""

        output = "## Relevant Design Patterns\n\n"
        output += "Apply these patterns to maintain consistency with prior implementations:\n\n"

        for pattern in patterns[:self.max_patterns]:
            output += f"### {pattern.title} ({pattern.category})\n\n"
            if pattern.problem:
                output += f"**Problem:** {pattern.problem}\n\n"
            if pattern.solution:
                output += f"**Solution:** {pattern.solution}\n\n"
            if pattern.when_to_use:
                output += f"**When to Use:** {pattern.when_to_use}\n\n"

        return output

    def enrich_specify_input(
        self,
        feature_intent: str,
        decisions: List[Decision],
        patterns: List[Pattern]
    ) -> str:
        """Create enriched input for `speckit specify` command.

        Args:
            feature_intent: Original feature description
            decisions: Relevant prior decisions
            patterns: Relevant design patterns

        Returns:
            Enriched feature intent with prior context prepended
        """
        enrichment = ""

        if decisions or patterns:
            enrichment += "# Prior Context\n\n"

        if decisions:
            enrichment += self.format_decisions(decisions, feature_intent)

        if patterns:
            enrichment += self.format_patterns(patterns, feature_intent)

        if enrichment:
            enrichment += "---\n\n"

        enrichment += f"# Feature Specification\n\n{feature_intent}"
        return enrichment

    def enrich_plan_input(
        self,
        spec_content: str,
        decisions: List[Decision],
        patterns: List[Pattern],
        architecture_notes: str = ""
    ) -> str:
        """Create enriched input for `speckit plan` command.

        Appends architecture context to specification before planning.

        Args:
            spec_content: Original specification Markdown
            decisions: Relevant architectural decisions
            patterns: Relevant design patterns
            architecture_notes: Additional architecture guidance

        Returns:
            Enriched specification with architecture context
        """
        output = spec_content

        if decisions or patterns or architecture_notes:
            output += "\n\n---\n\n## Architecture Context\n\n"

        if architecture_notes:
            output += f"### Architecture Guidance\n\n{architecture_notes}\n\n"

        if decisions:
            output += "### Relevant Decisions\n\n"
            for decision in decisions[:self.max_decisions]:
                output += f"- **{decision.title}**: {decision.decision}\n"
            output += "\n"

        if patterns:
            output += "### Design Patterns\n\n"
            for pattern in patterns[:self.max_patterns]:
                output += f"- **{pattern.title}** ({pattern.category})\n"
            output += "\n"

        return output


def create_enrichment_context(
    intent: str,
    decisions: List[Decision] = None,
    patterns: List[Pattern] = None
) -> Dict[str, str]:
    """Create enrichment context for SpecKit commands (convenience function).

    Args:
        intent: Feature intent
        decisions: Relevant decisions
        patterns: Relevant patterns

    Returns:
        Dict with 'enriched_intent' and 'is_enriched' flag
    """
    decisions = decisions or []
    patterns = patterns or []

    formatter = EnrichmentFormatter()

    enriched = formatter.enrich_specify_input(intent, decisions, patterns)

    return {
        "enriched_intent": enriched,
        "is_enriched": bool(decisions or patterns),
        "decisions_count": len(decisions),
        "patterns_count": len(patterns)
    }


def format_architecture_guidance(
    tech_stack: List[str] = None,
    constraints: List[str] = None,
    patterns: List[str] = None
) -> str:
    """Format architecture guidance for plan enrichment.

    Args:
        tech_stack: Technology stack items
        constraints: Architectural constraints
        patterns: Design patterns to apply

    Returns:
        Formatted architecture guidance
    """
    guidance = ""

    if tech_stack:
        guidance += "## Technology Stack\n\n"
        for tech in tech_stack:
            guidance += f"- {tech}\n"
        guidance += "\n"

    if constraints:
        guidance += "## Constraints\n\n"
        for constraint in constraints:
            guidance += f"- {constraint}\n"
        guidance += "\n"

    if patterns:
        guidance += "## Design Patterns\n\n"
        for pattern in patterns:
            guidance += f"- {pattern}\n"
        guidance += "\n"

    return guidance
