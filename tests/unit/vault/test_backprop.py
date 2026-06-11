"""Unit tests for spekificity.vault.backprop."""

from __future__ import annotations

from pathlib import Path

import pytest

from spekificity.vault.backprop import (
    BackpropResult,
    _append_vault_warning,
    _dedup_key,
    _infer_failure_type,
    _load_seen,
    _parse_failures,
    _save_seen,
    backprop_reflex,
)


PYTEST_OUTPUT = """
FAILED tests/unit/vault/test_init.py::TestInitVault::test_calls_open_vault - AssertionError: mock not called
FAILED tests/unit/speckit/test_config.py::TestWriteSpekConfig::test_creates_config_yaml - AssertionError
"""

EMPTY_OUTPUT = "All tests passed."

JEST_OUTPUT = """
  ● AuthService › login should return token

    Expected: "token123"
    Received: undefined
"""


class TestParseFailures:
    def test_pytest_extracts_test_path_and_name(self):
        failures = _parse_failures(PYTEST_OUTPUT)
        paths = [f["test_path"] for f in failures]
        assert "tests/unit/vault/test_init.py" in paths

    def test_pytest_two_failures(self):
        failures = _parse_failures(PYTEST_OUTPUT)
        assert len(failures) == 2

    def test_empty_output_returns_empty_list(self):
        assert _parse_failures(EMPTY_OUTPUT) == []

    def test_blank_string_returns_empty_list(self):
        assert _parse_failures("") == []

    def test_non_failure_output_returns_empty(self):
        assert _parse_failures("1 passed, 0 failed in 0.3s") == []

    def test_failure_dict_has_required_keys(self):
        failures = _parse_failures(PYTEST_OUTPUT)
        for f in failures:
            assert "test_path" in f
            assert "test_name" in f
            assert "failure_type" in f

    def test_jest_output_parsed(self):
        failures = _parse_failures(JEST_OUTPUT)
        assert len(failures) >= 1


class TestInferFailureType:
    def test_assertion_error_maps_correctly(self):
        assert _infer_failure_type("AssertionError: mock not called") == "assertion_failure"

    def test_type_error(self):
        assert _infer_failure_type("TypeError: expected int got str") == "type_error"

    def test_import_error(self):
        assert _infer_failure_type("ImportError: cannot import name X") == "import_error"

    def test_timeout(self):
        assert _infer_failure_type("Timeout after 5000ms") == "timeout"

    def test_unknown_message_returns_unknown(self):
        assert _infer_failure_type("something completely unrecognized xyz") == "unknown"

    def test_case_insensitive(self):
        assert _infer_failure_type("ASSERT failed") == "assertion_failure"


class TestDedupKey:
    def test_consistent_format(self):
        failure = {"test_path": "tests/foo.py", "failure_type": "assertion_failure"}
        assert _dedup_key(failure) == "tests/foo.py::assertion_failure"

    def test_different_paths_different_keys(self):
        a = {"test_path": "tests/a.py", "failure_type": "timeout"}
        b = {"test_path": "tests/b.py", "failure_type": "timeout"}
        assert _dedup_key(a) != _dedup_key(b)


class TestLoadSeen:
    def test_returns_empty_when_file_absent(self, tmp_path):
        result = _load_seen(tmp_path / "nonexistent.yaml")
        assert result == {}

    def test_returns_dict_with_correct_keys(self, tmp_path):
        yaml_content = (
            "seen_failures:\n"
            '  - test_path: "tests/foo.py"\n'
            '    failure_type: "assertion_failure"\n'
            '    first_seen: "2026-06-11"\n'
            "    count: 1\n"
        )
        seen_path = tmp_path / "backprop-seen.yaml"
        seen_path.write_text(yaml_content)
        result = _load_seen(seen_path)
        assert "tests/foo.py::assertion_failure" in result

    def test_returns_empty_on_malformed_yaml(self, tmp_path):
        seen_path = tmp_path / "bad.yaml"
        seen_path.write_text("{{{invalid yaml")
        result = _load_seen(seen_path)
        assert isinstance(result, dict)


class TestSaveSeen:
    def test_creates_file_with_correct_format(self, tmp_path):
        seen_path = tmp_path / "memory" / "backprop-seen.yaml"
        seen = {
            "tests/foo.py::assertion_failure": {
                "test_path": "tests/foo.py",
                "failure_type": "assertion_failure",
                "first_seen": "2026-06-11",
                "count": 1,
            }
        }
        _save_seen(seen_path, seen)
        assert seen_path.exists()
        content = seen_path.read_text()
        assert "tests/foo.py" in content
        assert "assertion_failure" in content


class TestAppendVaultWarning:
    def test_appends_blockquote_to_existing_patterns_md(self, tmp_path):
        patterns = tmp_path / "patterns.md"
        patterns.write_text("# Patterns\n")
        failure = {
            "test_path": "tests/foo.py",
            "test_name": "TestFoo::test_bar",
            "failure_type": "assertion_failure",
        }
        _append_vault_warning(patterns, failure)
        content = patterns.read_text()
        assert "> ⚠ Backprop warning" in content
        assert "assertion_failure" in content

    def test_creates_patterns_md_if_absent(self, tmp_path):
        patterns = tmp_path / "patterns.md"
        failure = {
            "test_path": "tests/foo.py",
            "test_name": "TestFoo::test_bar",
            "failure_type": "timeout",
        }
        _append_vault_warning(patterns, failure)
        assert patterns.exists()
        assert "> ⚠ Backprop warning" in patterns.read_text()

    def test_correct_blockquote_format(self, tmp_path):
        patterns = tmp_path / "patterns.md"
        failure = {
            "test_path": "tests/unit/foo.py",
            "test_name": "TestFoo::test_x",
            "failure_type": "type_error",
        }
        _append_vault_warning(patterns, failure)
        content = patterns.read_text()
        assert "> ⚠ Backprop warning [type_error]" in content
        assert "`tests/unit/foo.py::TestFoo::test_x` failed." in content


class TestBackpropReflex:
    def _make_vault(self, tmp_path: Path) -> Path:
        vault = tmp_path / ".spek" / "vault"
        vault.mkdir(parents=True)
        (tmp_path / ".spek" / "memory").mkdir(parents=True)
        return vault

    def test_pytest_failure_adds_warning(self, tmp_path):
        vault = self._make_vault(tmp_path)
        result = backprop_reflex(PYTEST_OUTPUT, vault)
        assert result.warnings_added == 2
        assert not result.skipped

    def test_idempotency_second_call_adds_zero(self, tmp_path):
        vault = self._make_vault(tmp_path)
        backprop_reflex(PYTEST_OUTPUT, vault)
        result2 = backprop_reflex(PYTEST_OUTPUT, vault)
        assert result2.warnings_added == 0

    def test_empty_input_returns_skipped(self, tmp_path):
        vault = self._make_vault(tmp_path)
        result = backprop_reflex(EMPTY_OUTPUT, vault)
        assert result.skipped is True
        assert result.warnings_added == 0

    def test_single_failure_adds_one_warning(self, tmp_path):
        vault = self._make_vault(tmp_path)
        single = "FAILED tests/unit/foo.py::TestFoo::test_x - AssertionError"
        result = backprop_reflex(single, vault)
        assert result.warnings_added == 1

    def test_patterns_md_contains_warning(self, tmp_path):
        vault = self._make_vault(tmp_path)
        single = "FAILED tests/unit/foo.py::TestFoo::test_x - AssertionError"
        backprop_reflex(single, vault)
        patterns = vault / "patterns.md"
        assert patterns.exists()
        assert "> ⚠ Backprop warning" in patterns.read_text()

    def test_failures_parsed_contains_keys(self, tmp_path):
        vault = self._make_vault(tmp_path)
        result = backprop_reflex(PYTEST_OUTPUT, vault)
        assert len(result.failures_parsed) == 2
