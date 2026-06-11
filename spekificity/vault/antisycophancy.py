"""Anti-sycophancy validation: detect AI drift patterns in spec text."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from spekificity.utils import print_status


@dataclass
class Violation:
    rule: str
    severity: str
    message: str
    spec_excerpt: str = ""


@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)
    skipped: bool = False


_CONTRADICTION_PAIRS: list[tuple[str, str]] = [
    ("dependency injection", "service locator"),
    ("observer pattern", "direct subscription"),
    ("layered architecture", "monolithic"),
    ("api-first", "implementation-first"),
    ("synchronous", "asynchronous"),
    ("singleton", "factory"),
    ("immutable", "mutable state"),
]

_CAMELCASE_PATTERN = re.compile(r"\b[A-Z][a-zA-Z0-9]{2,}\b")
_VERSION_PATTERN = re.compile(r"v?\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9]+)?")

_COMMON_ENGLISH = frozenset({
    "The", "This", "That", "These", "Those", "When", "Where", "Which",
    "What", "How", "Why", "Who", "All", "Each", "Every", "Some", "Any",
    "Both", "Few", "More", "Most", "Other", "Such", "Into", "Per",
    "Run", "Use", "Add", "Get", "Set", "New", "Old", "One", "Two",
    "For", "Not", "But", "And", "Via", "See", "May", "Can", "Has",
    "Are", "Was", "Had", "Did", "Let", "Its",
    "True", "False", "None", "List", "Dict", "Path", "File",
})


def _load_vault_text(vault_path: Path, filename: str) -> str:
    """Read vault/<filename>. Returns '' if absent."""
    try:
        return (vault_path / filename).read_text()
    except (FileNotFoundError, OSError):
        return ""


def _rule_contradiction(
    spec_text: str,
    decisions_text: str,
    extra_pairs: list,
) -> list[Violation]:
    """Rule 1: bidirectional contradiction detection."""
    violations: list[Violation] = []
    spec_lower = spec_text.lower()
    decisions_lower = decisions_text.lower()

    all_pairs = list(_CONTRADICTION_PAIRS) + list(extra_pairs)
    for term_a, term_b in all_pairs:
        a_lower = term_a.lower()
        b_lower = term_b.lower()
        if a_lower in decisions_lower and b_lower in spec_lower:
            excerpt = _find_excerpt(spec_text, term_b)
            violations.append(Violation(
                rule="CONTRADICTION",
                severity="HIGH",
                message=(
                    f'spec contradicts vault: vault uses "{term_a}" '
                    f'but spec proposes "{term_b}"'
                ),
                spec_excerpt=excerpt,
            ))
        elif b_lower in decisions_lower and a_lower in spec_lower:
            excerpt = _find_excerpt(spec_text, term_a)
            violations.append(Violation(
                rule="CONTRADICTION",
                severity="HIGH",
                message=(
                    f'spec contradicts vault: vault uses "{term_b}" '
                    f'but spec proposes "{term_a}"'
                ),
                spec_excerpt=excerpt,
            ))
    return violations


def _find_excerpt(text: str, term: str) -> str:
    """Return up to 80 chars of context around term."""
    idx = text.lower().find(term.lower())
    if idx == -1:
        return ""
    start = max(0, idx - 20)
    end = min(len(text), idx + len(term) + 40)
    return text[start:end].replace("\n", " ")[:80]


def _rule_complexity(
    spec_text: str,
    vault_path: Path,
    threshold: float,
) -> list[Violation]:
    """Rule 2: flag if spec word count > threshold × avg of prior specs."""
    specs_dir = vault_path / "specs"
    if not specs_dir.exists():
        return []
    prior_specs = list(specs_dir.glob("*.md"))
    if not prior_specs:
        return []
    word_counts = [
        len(p.read_text().split())
        for p in prior_specs
    ]
    avg = sum(word_counts) / len(word_counts)
    if avg == 0:
        return []
    spec_words = len(spec_text.split())
    if spec_words > avg * threshold:
        return [Violation(
            rule="COMPLEXITY",
            severity="MEDIUM",
            message=(
                f"spec is {spec_words} words, {threshold}× avg of "
                f"{avg:.0f} words across {len(prior_specs)} prior specs"
            ),
        )]
    return []


def _rule_pattern_consistency(
    spec_text: str,
    patterns_text: str,
) -> list[Violation]:
    """Rule 3: check if spec references recent patterns."""
    if not patterns_text.strip():
        return []
    pattern_names: list[str] = []
    for line in patterns_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            name = stripped[2:].split(":")[0].strip().lower()
            if len(name) > 3:
                pattern_names.append(name)

    if len(pattern_names) < 3:
        return []

    from collections import Counter
    word_counts: Counter = Counter()
    for name in pattern_names:
        for word in name.split():
            if len(word) > 3:
                word_counts[word] += 1

    spec_lower = spec_text.lower()
    deviations = [
        word for word, count in word_counts.most_common(3)
        if count >= 2 and word not in spec_lower
    ]
    if deviations:
        return [Violation(
            rule="PATTERN",
            severity="LOW",
            message=(
                f"spec may deviate from vault patterns; "
                f"recurring pattern terms not found: {', '.join(deviations)}"
            ),
        )]
    return []


def _rule_stack_drift(
    spec_text: str,
    patterns_text: str,
) -> list[Violation]:
    """Rule 4: flag CamelCase tech names/versions in spec not in patterns."""
    violations: list[Violation] = []
    camel_terms = set(_CAMELCASE_PATTERN.findall(spec_text))
    tech_terms = camel_terms - _COMMON_ENGLISH
    version_terms = set(_VERSION_PATTERN.findall(spec_text))
    patterns_lower = patterns_text.lower()

    unknown_techs = [
        t for t in sorted(tech_terms)
        if t.lower() not in patterns_lower
    ]
    unknown_versions = [
        v for v in sorted(version_terms)
        if v not in patterns_text
    ]

    if unknown_techs:
        violations.append(Violation(
            rule="STACK_DRIFT",
            severity="MEDIUM",
            message=(
                f"tech names in spec not found in vault patterns: "
                f"{', '.join(unknown_techs[:5])}"
            ),
        ))
    if unknown_versions:
        violations.append(Violation(
            rule="STACK_DRIFT",
            severity="MEDIUM",
            message=(
                f"version strings in spec not in vault patterns: "
                f"{', '.join(unknown_versions[:5])}"
            ),
        ))
    return violations


def _write_violations(violations: list[Violation], memory_path: Path) -> None:
    """Append violation entries to violations.md. Creates if absent."""
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    lines: list[str] = []
    for v in violations:
        lines.append(f"\n## {today} | {v.rule} | {v.severity}\n")
        if v.spec_excerpt:
            lines.append(f"\n**Spec excerpt**: \"{v.spec_excerpt}\"\n")
        lines.append(f"\n**Message**: {v.message}\n")
        lines.append("\n---\n")
    text = "".join(lines)
    if memory_path.exists():
        memory_path.write_text(memory_path.read_text() + text)
    else:
        memory_path.write_text(text.lstrip("\n"))


def validate_spec(
    spec_text: str,
    vault_path: Path,
    config: dict,
) -> ValidationResult:
    """Validate spec text against vault for AI drift patterns.

    Never raises. Returns ValidationResult(skipped=True) if disabled.
    Does NOT halt execution — caller reads result and decides.
    """
    antisyco_cfg = config.get("antisycophancy", {})
    if not antisyco_cfg.get("enabled", True):
        print_status("SKIP", "anti-sycophancy validation disabled in config")
        return ValidationResult(skipped=True)

    threshold = float(antisyco_cfg.get("complexity_threshold", 2.0))
    extra_pairs = antisyco_cfg.get("contradiction_pairs", [])

    try:
        decisions_text = _load_vault_text(vault_path, "decisions.md")
        patterns_text = _load_vault_text(vault_path, "patterns.md")

        violations: list[Violation] = []
        violations.extend(_rule_contradiction(spec_text, decisions_text, extra_pairs))
        violations.extend(_rule_complexity(spec_text, vault_path, threshold))
        violations.extend(_rule_pattern_consistency(spec_text, patterns_text))
        violations.extend(_rule_stack_drift(spec_text, patterns_text))

        if violations:
            memory_path = vault_path.parent / "memory" / "violations.md"
            _write_violations(violations, memory_path)
            for v in violations:
                print_status("WARN", f"[{v.rule}:{v.severity}] {v.message}")
        else:
            print_status("OK", "anti-sycophancy checks passed")

        return ValidationResult(violations=violations)

    except Exception as exc:
        print_status("SKIP", f"anti-sycophancy: vault read error — {exc}")
        return ValidationResult(skipped=True)
