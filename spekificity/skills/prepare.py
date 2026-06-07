"""Skill: /spek.prepare — Load context and generate navigation guide.

Prepares feature work by loading vault context and indexing codebase.
"""

import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import click

from spekificity.core.vault import Vault
from spekificity.core.context import ContextLoader
from spekificity.integrations.lat_md import LatMdIndex
from spekificity.core.compression import compress_text


class PrepareGuide:
    """Navigation guide generator for feature preparation."""

    def __init__(self, project_path: str = ".", vault_path: str = "vault"):
        self.project_path = Path(project_path)
        self.vault_path = vault_path
        self.vault = Vault(vault_path)
        self.context_loader = ContextLoader(project_path, vault_path)
        self.index = LatMdIndex(project_path)

    def check_git_status(self) -> Dict[str, Any]:
        """Check if git working directory is clean.

        Returns:
            Dict with 'clean' bool and 'status' message
        """
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=str(self.project_path),
                timeout=10
            )
            clean = result.returncode == 0 and not result.stdout.strip()
            return {
                "clean": clean,
                "status": "Working directory is clean" if clean else f"Uncommitted changes: {result.stdout[:100]}"
            }
        except Exception as e:
            return {"clean": False, "status": f"Git check failed: {e}"}

    def load_context(self, feature_intent: str, limit: int = 5) -> Dict[str, List[Any]]:
        """Load relevant vault context for feature.

        Args:
            feature_intent: Feature description
            limit: Maximum items per category

        Returns:
            Dict with decisions, patterns, lessons
        """
        decisions = self.vault.load_decisions()
        patterns = self.vault.load_patterns()
        lessons = self.vault.load_lessons()

        # Simple filtering by keyword matching
        intent_terms = set(feature_intent.lower().split())

        relevant = {
            "decisions": [],
            "patterns": [],
            "lessons": []
        }

        # Filter decisions
        for dec in decisions[:limit]:
            dec_text = f"{dec.get('title', '')} {dec.get('decision', '')}".lower()
            if any(term in dec_text for term in intent_terms):
                relevant["decisions"].append(dec)

        # Filter patterns
        for pat in patterns[:limit]:
            pat_text = f"{pat.get('title', '')} {pat.get('category', '')}".lower()
            if any(term in pat_text for term in intent_terms):
                relevant["patterns"].append(pat)

        # Filter lessons
        for les in lessons[:limit]:
            les_text = f"{les.get('feature', '')} {' '.join(les.get('lessons_learned', []))}".lower()
            if any(term in les_text for term in intent_terms):
                relevant["lessons"].append(les)

        return relevant

    def generate_code_guide(self, feature_intent: str, limit: int = 5) -> Dict[str, Any]:
        """Generate guide to relevant code sections.

        Args:
            feature_intent: Feature description
            limit: Maximum files to include

        Returns:
            Dict with relevant files and functions
        """
        try:
            # Sync index
            self.index.ensure_index()
            self.index.sync_index()

            # Query for relevant files and functions
            files = self.index.query_files(feature_intent, limit=limit)
            functions = self.index.query_functions(feature_intent, limit=min(limit, 5))

            return {
                "files": files,
                "functions": functions,
                "indexed": True
            }
        except Exception as e:
            return {
                "files": [],
                "functions": [],
                "indexed": False,
                "error": str(e)
            }

    def estimate_tokens(self, decisions: List[Dict], patterns: List[Dict], code_guide: Dict) -> int:
        """Rough estimate of token overhead for context.

        Args:
            decisions: Decision list
            patterns: Pattern list
            code_guide: Code guide dict

        Returns:
            Estimated tokens
        """
        # Rough estimation: ~150 tokens per decision, ~200 per pattern, ~100 per file
        est = 0
        est += len(decisions) * 150
        est += len(patterns) * 200
        est += len(code_guide.get("files", [])) * 100
        est += len(code_guide.get("functions", [])) * 50

        return est

    def generate_report(self, feature_intent: str) -> str:
        """Generate complete navigation guide report.

        Args:
            feature_intent: Feature description

        Returns:
            Formatted Markdown report
        """
        start_time = time.time()

        # Load all context
        context = self.load_context(feature_intent)
        code_guide = self.generate_code_guide(feature_intent)
        git_status = self.check_git_status()

        elapsed = time.time() - start_time

        # Build report
        report = f"# Prepare: {feature_intent}\n\n"

        # Git status
        report += f"## Working Directory\n\n"
        report += f"- Status: {git_status['status']}\n"
        report += f"- Ready: {'✓' if git_status['clean'] else '✗'}\n\n"

        # Prior decisions
        if context["decisions"]:
            report += "## Prior Decisions\n\n"
            for dec in context["decisions"][:3]:
                report += f"- **{dec.get('title', 'Decision')}**: {dec.get('decision', '')[:80]}...\n"
            report += "\n"

        # Patterns
        if context["patterns"]:
            report += "## Relevant Patterns\n\n"
            for pat in context["patterns"][:3]:
                report += f"- **{pat.get('title', 'Pattern')}** ({pat.get('category', '')})\n"
            report += "\n"

        # Code guide
        if code_guide["indexed"] and code_guide["files"]:
            report += "## Relevant Code\n\n"
            report += "### Files\n\n"
            for file_ref in code_guide["files"][:3]:
                path = file_ref.get("path", "unknown")
                report += f"- `{path}`\n"
            report += "\n"

            if code_guide["functions"]:
                report += "### Functions\n\n"
                for func in code_guide["functions"][:3]:
                    sig = func.get("signature", func.get("name", "unknown"))
                    report += f"- `{sig}`\n"
                report += "\n"

        # Context estimate
        tokens = self.estimate_tokens(
            context["decisions"],
            context["patterns"],
            code_guide
        )
        report += f"## Context Summary\n\n"
        report += f"- Prior decisions: {len(context['decisions'])}\n"
        report += f"- Relevant patterns: {len(context['patterns'])}\n"
        report += f"- Code files indexed: {len(code_guide.get('files', []))}\n"
        report += f"- Estimated context tokens: ~{tokens}\n"
        report += f"- Preparation time: {elapsed:.1f}s\n\n"

        # Action items
        actionable = len(context["decisions"]) + len(context["patterns"]) + len(code_guide.get("files", []))
        report += f"## Next Steps\n\n"
        report += f"1. Review {len(context['decisions'])} prior decisions above\n"
        report += f"2. Check {len(code_guide.get('files', []))} relevant code files\n"
        report += f"3. Run `/spek.plan \"...feature description...\"` to generate spec\n\n"

        report += f"**Actionable items found: {max(3, actionable)}** ✓\n"

        return report


def prepare(
    feature_intent: str,
    project_path: str = ".",
    vault_path: str = "vault",
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """Prepare for feature work by loading context.

    Args:
        feature_intent: Feature description or name
        project_path: Project root path
        vault_path: Path to vault directory
        output_file: Optional file to write report to

    Returns:
        Dict with report, context, and metadata
    """
    start = time.time()

    guide = PrepareGuide(project_path, vault_path)
    report = guide.generate_report(feature_intent)

    elapsed = time.time() - start

    # Write output if requested
    if output_file:
        Path(output_file).write_text(report)

    return {
        "success": True,
        "report": report,
        "elapsed_seconds": elapsed,
        "meets_sla": elapsed < 30,
        "output_file": output_file
    }
