"""Decision logging and extraction during task execution.

Captures architectural decisions made during task implementation.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import re


class DecisionLogger:
    """Logs and extracts decisions from task execution."""

    DECISION_PATTERN = r"@decision\s+(.+?)(?:\n|$)"
    PATTERN_PATTERN = r"@pattern\s+(.+?)(?:\n|$)"

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.decisions_log = self.project_path / ".specify" / "decisions-session.md"
        self.decisions_log.parent.mkdir(parents=True, exist_ok=True)

    def initialize_session(self, feature_name: str) -> None:
        """Initialize decision logging session.

        Args:
            feature_name: Feature name
        """
        header = f"# Decisions: {feature_name}\n\n"
        header += f"**Session Started:** {datetime.now().isoformat()}\n\n"

        if not self.decisions_log.exists():
            self.decisions_log.write_text(header)

    def log_decision(
        self,
        task_id: str,
        decision: str,
        rationale: str,
        alternatives: List[str] = None,
        implications: List[str] = None
    ) -> str:
        """Log architectural decision.

        Args:
            task_id: Task ID where decision was made
            decision: Decision text
            rationale: Why this decision
            alternatives: Alternative options considered
            implications: Consequences of decision

        Returns:
            Decision ID generated
        """
        # Generate decision ID based on timestamp
        dec_id = f"D{datetime.now().strftime('%Y%m%d%H%M%S')}"

        entry = f"\n## Decision: {dec_id}\n\n"
        entry += f"**Task:** {task_id}\n\n"
        entry += f"**Decision:** {decision}\n\n"
        entry += f"**Rationale:** {rationale}\n\n"

        if alternatives:
            entry += "**Alternatives Considered:**\n\n"
            for alt in alternatives:
                entry += f"- {alt}\n"
            entry += "\n"

        if implications:
            entry += "**Implications:**\n\n"
            for imp in implications:
                entry += f"- {imp}\n"
            entry += "\n"

        entry += f"**Date:** {datetime.now().isoformat()}\n"

        current = self.decisions_log.read_text()
        self.decisions_log.write_text(current + entry)

        return dec_id

    def log_pattern_usage(
        self,
        task_id: str,
        pattern_name: str,
        context: str = "",
        modifications: List[str] = None
    ) -> str:
        """Log use of design pattern.

        Args:
            task_id: Task ID
            pattern_name: Pattern name
            context: Where/how pattern was used
            modifications: Any modifications to standard pattern

        Returns:
            Pattern usage ID
        """
        pattern_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"

        entry = f"\n## Pattern Usage: {pattern_id}\n\n"
        entry += f"**Task:** {task_id}\n\n"
        entry += f"**Pattern:** {pattern_name}\n\n"

        if context:
            entry += f"**Context:** {context}\n\n"

        if modifications:
            entry += "**Modifications:**\n\n"
            for mod in modifications:
                entry += f"- {mod}\n"
            entry += "\n"

        entry += f"**Date:** {datetime.now().isoformat()}\n"

        current = self.decisions_log.read_text()
        self.decisions_log.write_text(current + entry)

        return pattern_id

    def extract_decisions(self) -> List[Dict[str, Any]]:
        """Extract all logged decisions.

        Returns:
            List of decision dicts
        """
        if not self.decisions_log.exists():
            return []

        content = self.decisions_log.read_text()
        decisions = []

        # Split by decision header
        sections = re.split(r"## Decision: ", content)

        for section in sections[1:]:  # Skip header
            lines = section.split("\n")
            if not lines:
                continue

            decision_id = lines[0].strip()
            decision_dict = {"id": decision_id, "raw": section}

            # Extract fields
            for i, line in enumerate(lines):
                if line.startswith("**Decision:**"):
                    decision_dict["decision"] = line.replace("**Decision:**", "").strip()
                elif line.startswith("**Rationale:**"):
                    decision_dict["rationale"] = line.replace("**Rationale:**", "").strip()
                elif line.startswith("**Task:**"):
                    decision_dict["task_id"] = line.replace("**Task:**", "").strip()

            decisions.append(decision_dict)

        return decisions

    def extract_patterns(self) -> List[Dict[str, Any]]:
        """Extract all logged pattern uses.

        Returns:
            List of pattern usage dicts
        """
        if not self.decisions_log.exists():
            return []

        content = self.decisions_log.read_text()
        patterns = []

        # Split by pattern header
        sections = re.split(r"## Pattern Usage: ", content)

        for section in sections[1:]:  # Skip header
            lines = section.split("\n")
            if not lines:
                continue

            pattern_id = lines[0].strip()
            pattern_dict = {"id": pattern_id, "raw": section}

            # Extract fields
            for line in lines:
                if line.startswith("**Pattern:**"):
                    pattern_dict["pattern"] = line.replace("**Pattern:**", "").strip()
                elif line.startswith("**Task:**"):
                    pattern_dict["task_id"] = line.replace("**Task:**", "").strip()
                elif line.startswith("**Context:**"):
                    pattern_dict["context"] = line.replace("**Context:**", "").strip()

            patterns.append(pattern_dict)

        return patterns

    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of session decisions and patterns.

        Returns:
            Dict with counts and lists
        """
        decisions = self.extract_decisions()
        patterns = self.extract_patterns()

        return {
            "decisions_count": len(decisions),
            "patterns_count": len(patterns),
            "decisions": decisions,
            "patterns": patterns,
            "total_artifacts": len(decisions) + len(patterns)
        }

    def close_session(self) -> Path:
        """Close decision logging session.

        Returns:
            Path to closed log
        """
        if not self.decisions_log.exists():
            return self.decisions_log

        # Append session end marker
        current = self.decisions_log.read_text()
        footer = f"\n---\n\n**Session Ended:** {datetime.now().isoformat()}\n"

        self.decisions_log.write_text(current + footer)

        return self.decisions_log
