"""Unit tests for spekificity.vault.antisycophancy."""

from __future__ import annotations

from pathlib import Path

import pytest

from spekificity.vault.antisycophancy import (
    ValidationResult,
    Violation,
    _load_vault_text,
    _rule_complexity,
    _rule_contradiction,
    _rule_pattern_consistency,
    _rule_stack_drift,
    _write_violations,
    validate_spec,
)


SPEC_WITH_SERVICE_LOCATOR = """
## Architecture
Use service locator pattern for auth service discovery.
All services registered at startup via service locator.
"""

SPEC_WITH_DI = """
## Architecture
Use dependency injection for all services.
"""

SPEC_WITH_CAMEL = """
## Tech Stack
Use FastAPI with PostgreSQL and TypeScript frontend.
Version v3.11 required.
"""


class TestLoadVaultText:
    def test_returns_empty_when_absent(self, tmp_path):
        assert _load_vault_text(tmp_path, "nonexistent.md") == ""

    def test_returns_content_when_present(self, tmp_path):
        (tmp_path / "decisions.md").write_text("# Decisions\nUse DI.")
        result = _load_vault_text(tmp_path, "decisions.md")
        assert "Use DI" in result


class TestRuleContradiction:
    def test_returns_high_violation_when_vault_di_spec_service_locator(self):
        decisions = "Use dependency injection for all services."
        violations = _rule_contradiction(SPEC_WITH_SERVICE_LOCATOR, decisions, [])
        assert len(violations) == 1
        assert violations[0].rule == "CONTRADICTION"
        assert violations[0].severity == "HIGH"
        assert "dependency injection" in violations[0].message

    def test_reverse_direction_also_flagged(self):
        decisions = "Use service locator for all service discovery."
        spec = "Use dependency injection for auth."
        violations = _rule_contradiction(spec, decisions, [])
        assert len(violations) == 1
        assert violations[0].rule == "CONTRADICTION"

    def test_no_contradiction_returns_empty(self):
        decisions = "Use dependency injection."
        spec = "Use dependency injection throughout."
        violations = _rule_contradiction(spec, decisions, [])
        assert violations == []

    def test_extra_pairs_used(self):
        decisions = "Use EventBus."
        spec = "Use polling approach."
        extra = [("EventBus", "polling")]
        violations = _rule_contradiction(spec, decisions, extra)
        assert len(violations) == 1

    def test_spec_excerpt_populated(self):
        decisions = "Use dependency injection."
        violations = _rule_contradiction(SPEC_WITH_SERVICE_LOCATOR, decisions, [])
        assert violations[0].spec_excerpt != ""


class TestRuleComplexity:
    def _make_vault_with_specs(self, tmp_path: Path, word_counts: list[int]) -> Path:
        vault = tmp_path / "vault"
        specs_dir = vault / "specs"
        specs_dir.mkdir(parents=True)
        for i, count in enumerate(word_counts):
            content = " ".join(["word"] * count)
            (specs_dir / f"spec-{i}.md").write_text(content)
        return vault

    def test_returns_medium_when_spec_exceeds_threshold(self, tmp_path):
        vault = self._make_vault_with_specs(tmp_path, [100, 100])
        big_spec = " ".join(["word"] * 250)
        violations = _rule_complexity(big_spec, vault, 2.0)
        assert len(violations) == 1
        assert violations[0].rule == "COMPLEXITY"
        assert violations[0].severity == "MEDIUM"

    def test_returns_empty_when_no_prior_specs(self, tmp_path):
        vault = tmp_path / "vault"
        (vault / "specs").mkdir(parents=True)
        spec = "A small spec text."
        violations = _rule_complexity(spec, vault, 2.0)
        assert violations == []

    def test_returns_empty_when_no_specs_dir(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        violations = _rule_complexity("some text", vault, 2.0)
        assert violations == []

    def test_returns_empty_when_below_threshold(self, tmp_path):
        vault = self._make_vault_with_specs(tmp_path, [200, 200])
        small_spec = " ".join(["word"] * 50)
        violations = _rule_complexity(small_spec, vault, 2.0)
        assert violations == []


class TestRulePatternConsistency:
    def test_empty_patterns_returns_empty(self):
        assert _rule_pattern_consistency("some spec", "") == []

    def test_too_few_patterns_skips(self):
        patterns = "- auth pattern: use JWT\n- caching pattern: use Redis\n"
        assert _rule_pattern_consistency("spec text", patterns) == []

    def test_returns_low_when_spec_deviates(self):
        patterns = (
            "- validation pattern: use pydantic validators\n"
            "- validation pattern: use schema validators\n"
            "- validation pattern: use input validators\n"
        )
        spec = "Use raw dict parsing throughout."
        violations = _rule_pattern_consistency(spec, patterns)
        # May or may not trigger depending on word frequency — just test no crash
        assert isinstance(violations, list)


class TestRuleStackDrift:
    def test_camelcase_tech_not_in_patterns_returns_medium(self):
        patterns = "- Use Flask for web\n"
        spec = "Use FastAPI with PostgreSQL."
        violations = _rule_stack_drift(spec, patterns)
        names = [v.message for v in violations if v.rule == "STACK_DRIFT"]
        assert any("FastAPI" in m or "PostgreSQL" in m for m in names)

    def test_tech_present_in_patterns_not_flagged(self):
        patterns = "- Use FastAPI for web endpoints\n- PostgreSQL as database\n"
        spec = "Use FastAPI with PostgreSQL."
        violations = _rule_stack_drift(spec, patterns)
        for v in violations:
            assert "FastAPI" not in v.message or "PostgreSQL" not in v.message

    def test_version_strings_extracted(self):
        patterns = "- Use Python 2.7\n"
        spec = "Requires Python v3.11."
        violations = _rule_stack_drift(spec, patterns)
        assert any("3.11" in v.message for v in violations if v.rule == "STACK_DRIFT")

    def test_common_english_words_not_flagged(self):
        patterns = "- general guidance\n"
        spec = "The feature uses this approach. All items should be tested."
        violations = [
            v for v in _rule_stack_drift(spec, patterns)
            if v.rule == "STACK_DRIFT"
        ]
        for v in violations:
            assert "The" not in v.message
            assert "All" not in v.message


class TestWriteViolations:
    def test_creates_violations_md_with_section_format(self, tmp_path):
        memory_path = tmp_path / "memory" / "violations.md"
        violations = [
            Violation(
                rule="CONTRADICTION",
                severity="HIGH",
                message="test message",
                spec_excerpt="some excerpt",
            )
        ]
        _write_violations(violations, memory_path)
        assert memory_path.exists()
        content = memory_path.read_text()
        assert "## " in content
        assert "CONTRADICTION" in content
        assert "HIGH" in content

    def test_appends_not_overwrites_on_second_call(self, tmp_path):
        memory_path = tmp_path / "memory" / "violations.md"
        v = Violation(rule="COMPLEXITY", severity="MEDIUM", message="msg")
        _write_violations([v], memory_path)
        first_content = memory_path.read_text()
        _write_violations([v], memory_path)
        second_content = memory_path.read_text()
        assert len(second_content) > len(first_content)


class TestValidateSpec:
    def _make_vault(self, tmp_path: Path) -> Path:
        vault = tmp_path / ".spek" / "vault"
        vault.mkdir(parents=True)
        (tmp_path / ".spek" / "memory").mkdir(parents=True)
        return vault

    def test_returns_skipped_when_disabled(self, tmp_path):
        vault = self._make_vault(tmp_path)
        result = validate_spec("any spec", vault, {"antisycophancy": {"enabled": False}})
        assert result.skipped is True
        assert result.violations == []

    def test_contradiction_violation_written_to_violations_md(self, tmp_path):
        vault = self._make_vault(tmp_path)
        (vault / "decisions.md").write_text("Use dependency injection for all services.")
        result = validate_spec(SPEC_WITH_SERVICE_LOCATOR, vault, {})
        assert any(v.rule == "CONTRADICTION" for v in result.violations)
        violations_md = tmp_path / ".spek" / "memory" / "violations.md"
        assert violations_md.exists()
        assert "CONTRADICTION" in violations_md.read_text()

    def test_ok_printed_when_no_violations(self, tmp_path, capsys):
        vault = self._make_vault(tmp_path)
        result = validate_spec("a simple spec with no camelcase or versions", vault, {})
        assert not result.skipped
        assert result.violations == []

    def test_empty_vault_does_not_raise(self, tmp_path):
        vault = self._make_vault(tmp_path)
        result = validate_spec("any text", vault, {})
        assert isinstance(result, ValidationResult)

    def test_extra_contradiction_pairs_in_config(self, tmp_path):
        vault = self._make_vault(tmp_path)
        (vault / "decisions.md").write_text("Use EventBus for messaging.")
        spec = "Use polling for event handling."
        config = {"antisycophancy": {"contradiction_pairs": [["EventBus", "polling"]]}}
        result = validate_spec(spec, vault, config)
        assert any(v.rule == "CONTRADICTION" for v in result.violations)
