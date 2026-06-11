"""Parse test failure output and append warnings to vault patterns.md."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from spekificity.utils import print_status

try:
    import yaml  # type: ignore[import]
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


@dataclass
class BackpropResult:
    warnings_added: int = 0
    skipped: bool = False
    failures_parsed: list[str] = field(default_factory=list)


_FAILURE_PATTERNS = [
    re.compile(r"FAILED\s+([\w/\.]+)::(\w[\w:]+)"),
    re.compile(r"ERROR\s+([\w/\.]+)::(\w[\w:]+)"),
    re.compile(r"●\s+(.+?)\s+›\s+(.+)"),
    re.compile(r"^\s+\d+\)\s+(.+)$", re.MULTILINE),
]

_FAILURE_TYPE_MAP: dict[str, str] = {
    "race": "race_condition",
    "timeout": "timeout",
    "assert": "assertion_failure",
    "import": "import_error",
    "attribute": "attribute_error",
    "key": "key_error",
    "type": "type_error",
    "value": "value_error",
    "io": "io_error",
    "connection": "connection_error",
}


def _parse_failures(test_output: str) -> list[dict]:
    """Extract failure records from test output. Returns [] on no failures."""
    results: list[dict] = []
    seen_keys: set[str] = set()
    for pattern in _FAILURE_PATTERNS:
        for match in pattern.finditer(test_output):
            groups = match.groups()
            if len(groups) >= 2:
                test_path = groups[0].strip()
                test_name = groups[1].strip()
            else:
                test_path = groups[0].strip()
                test_name = groups[0].strip()
            key = f"{test_path}::{test_name}"
            if key not in seen_keys:
                seen_keys.add(key)
                failure_type = _infer_failure_type(test_output)
                results.append({
                    "test_path": test_path,
                    "test_name": test_name,
                    "failure_type": failure_type,
                })
    return results


def _infer_failure_type(message: str) -> str:
    """Map failure message keywords to canonical type string."""
    lower = message.lower()
    for keyword, canonical in _FAILURE_TYPE_MAP.items():
        if keyword in lower:
            return canonical
    return "unknown"


def _dedup_key(failure: dict) -> str:
    """Return composite dedup key: test_path::failure_type."""
    return f"{failure['test_path']}::{failure['failure_type']}"


def _load_seen(seen_path: Path) -> dict[str, dict]:
    """Load backprop-seen.yaml. Returns {} if absent or malformed."""
    if not seen_path.exists():
        return {}
    try:
        text = seen_path.read_text()
        if not _YAML_AVAILABLE:
            return _load_seen_simple(text)
        data = yaml.safe_load(text) or {}
        entries = data.get("seen_failures", [])
        result: dict[str, dict] = {}
        for entry in entries:
            key = f"{entry.get('test_path', '')}::{entry.get('failure_type', '')}"
            result[key] = entry
        return result
    except Exception:
        return {}


def _load_seen_simple(text: str) -> dict[str, dict]:
    """Minimal YAML parser for seen_failures list (no external deps)."""
    result: dict[str, dict] = {}
    entry: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- test_path:"):
            if entry and "test_path" in entry and "failure_type" in entry:
                key = f"{entry['test_path']}::{entry['failure_type']}"
                result[key] = dict(entry)
            entry = {"test_path": stripped.split(":", 1)[1].strip().strip('"')}
        elif stripped.startswith("failure_type:") and entry:
            entry["failure_type"] = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("first_seen:") and entry:
            entry["first_seen"] = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("count:") and entry:
            entry["count"] = stripped.split(":", 1)[1].strip()
    if entry and "test_path" in entry and "failure_type" in entry:
        key = f"{entry['test_path']}::{entry['failure_type']}"
        result[key] = dict(entry)
    return result


def _save_seen(seen_path: Path, seen: dict[str, dict]) -> None:
    """Write backprop-seen.yaml. Creates parent dirs."""
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["seen_failures:\n"]
    for entry in seen.values():
        lines.append(f"  - test_path: \"{entry.get('test_path', '')}\"\n")
        lines.append(f"    failure_type: \"{entry.get('failure_type', '')}\"\n")
        lines.append(f"    first_seen: \"{entry.get('first_seen', '')}\"\n")
        lines.append(f"    count: {entry.get('count', 1)}\n")
    seen_path.write_text("".join(lines))


def _append_vault_warning(patterns_path: Path, failure: dict) -> None:
    """Append blockquote warning to patterns.md. Creates file if absent."""
    patterns_path.parent.mkdir(parents=True, exist_ok=True)
    warning = (
        f"\n> ⚠ Backprop warning [{failure['failure_type']}]: "
        f"`{failure['test_path']}::{failure['test_name']}` failed.\n"
        f"> Review for: {failure['failure_type']} patterns in related code.\n"
    )
    if patterns_path.exists():
        patterns_path.write_text(patterns_path.read_text() + warning)
    else:
        patterns_path.write_text(warning.lstrip("\n"))


def backprop_reflex(test_output: str, vault_path: Path) -> BackpropResult:
    """Parse test failure output and append warnings to vault.

    Idempotent: second call with same output adds 0 new warnings.
    Never raises; returns BackpropResult(skipped=True) on empty/no failures.
    """
    failures = _parse_failures(test_output)
    if not failures:
        print_status("SKIP", "backprop: no test failures found")
        return BackpropResult(skipped=True)

    memory_path = vault_path.parent / "memory"
    seen_path = memory_path / "backprop-seen.yaml"
    patterns_path = vault_path / "patterns.md"

    seen = _load_seen(seen_path)
    warnings_added = 0
    parsed_keys: list[str] = []

    for failure in failures:
        key = _dedup_key(failure)
        parsed_keys.append(key)
        if key in seen:
            entry = seen[key]
            entry["count"] = int(entry.get("count", 1)) + 1
        else:
            from datetime import date
            seen[key] = {
                "test_path": failure["test_path"],
                "failure_type": failure["failure_type"],
                "first_seen": date.today().isoformat(),
                "count": 1,
            }
            _append_vault_warning(patterns_path, failure)
            warnings_added += 1
            print_status("OK", f"backprop: warning added for {key}")

    _save_seen(seen_path, seen)
    if warnings_added == 0:
        print_status("SKIP", "backprop: all failures already seen (idempotent)")
    return BackpropResult(
        warnings_added=warnings_added,
        failures_parsed=parsed_keys,
    )
