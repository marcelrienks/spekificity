# Module Contracts: Planned Features

## `spekificity/vault/backprop.py`

### Public API

```python
def backprop_reflex(test_output: str, vault_path: Path) -> BackpropResult:
    """Parse test failure output and append warnings to vault.

    Args:
        test_output: Raw stdout/stderr from test runner (pytest, jest, mocha).
        vault_path:  Path to .spek/vault/ directory.

    Returns:
        BackpropResult with warnings_added count and parsed failure keys.

    Side effects:
        - Appends `> ⚠ Backprop warning ...` blockquote to vault_path/patterns.md
        - Creates/updates .spek/memory/backprop-seen.yaml (relative to vault_path parent)
        - Calls print_status("[OK]"/"[SKIP]") to stdout

    Errors:
        - Never raises; returns BackpropResult(skipped=True) on parse failure
        - Creates vault_path/patterns.md if absent
    """
```

### Internal Functions (not exported)

```python
def _parse_failures(test_output: str) -> list[dict]:
    """Extract failure records from test output. Returns [] on no failures."""

def _infer_failure_type(message: str) -> str:
    """Map failure message keywords to canonical type string."""

def _dedup_key(failure: dict) -> str:
    """Return composite key: f"{test_path}::{failure_type}"."""

def _load_seen(seen_path: Path) -> dict[str, dict]:
    """Load backprop-seen.yaml. Returns {} if absent or malformed."""

def _save_seen(seen_path: Path, seen: dict[str, dict]) -> None:
    """Write backprop-seen.yaml. Creates parent dirs."""

def _append_vault_warning(patterns_path: Path, failure: dict) -> None:
    """Append blockquote warning to patterns.md."""
```

### Vault Warning Format

Appended to `.spek/vault/patterns.md`:

```markdown
> ⚠ Backprop warning [assertion_failure]: `tests/unit/vault/test_init.py::TestInitVault::test_calls_open_vault` failed.
> Review for: assertion_failure patterns in related code.
```

---

## `spekificity/vault/antisycophancy.py`

### Public API

```python
def validate_spec(spec_text: str, vault_path: Path, config: dict) -> ValidationResult:
    """Validate spec text against vault for AI drift patterns.

    Args:
        spec_text:  Raw markdown text of the feature spec.
        vault_path: Path to .spek/vault/ directory.
        config:     Parsed .spek/config.yaml dict.

    Returns:
        ValidationResult with violations list and skipped flag.

    Side effects:
        - Appends to .spek/memory/violations.md (relative to vault_path parent)
        - Calls print_status for each violation and summary
        - Does NOT halt execution (caller decides what to do with result)

    Errors:
        - Never raises; returns ValidationResult(skipped=True) on vault read failure
        - Creates violations.md if absent
    """
```

### Internal Functions (not exported)

```python
def _load_vault_text(vault_path: Path, filename: str) -> str:
    """Read vault/<filename>. Returns "" if absent."""

def _rule_contradiction(spec_text: str, decisions_text: str, extra_pairs: list) -> list[Violation]:
    """Rule 1: bidirectional contradiction detection against _CONTRADICTION_PAIRS."""

def _rule_complexity(spec_text: str, vault_path: Path, threshold: float) -> list[Violation]:
    """Rule 2: spec word count vs avg of prior specs in vault/specs/."""

def _rule_pattern_consistency(spec_text: str, patterns_text: str) -> list[Violation]:
    """Rule 3: recent pattern reuse check (LOW severity)."""

def _rule_stack_drift(spec_text: str, patterns_text: str) -> list[Violation]:
    """Rule 4: CamelCase + version string extraction vs vault pattern techs."""

def _write_violations(violations: list[Violation], memory_path: Path) -> None:
    """Append violation entries to violations.md. Creates if absent."""
```

### Default Contradiction Pairs

```python
_CONTRADICTION_PAIRS = [
    ("dependency injection", "service locator"),
    ("observer pattern", "direct subscription"),
    ("layered architecture", "monolithic"),
    ("api-first", "implementation-first"),
    ("synchronous", "asynchronous"),
    ("singleton", "factory"),
    ("immutable", "mutable state"),
]
```

---

## `spekificity/speckit/config.py` additions

`_CONFIG_TEMPLATE` gains two new blocks (appended after `autolink:` block):

```python
token_budget:
  per_feature: null
  alert_thresholds: []
antisycophancy:
  enabled: true
  complexity_threshold: 2.0
  contradiction_pairs: []
```

No new functions; `write_spek_config()` signature unchanged.

---

## Skill File Contracts

### `spek-rarv.md`

- **Location in package**: `spekificity/skills/spek-rarv.md`
- **Distributed as**: flat `.md` for `claude`/`copilot`/`generic`; `spek-rarv/SKILL.md` for subfolder integrations
- **Required sections** (in order): `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`
- **Heading**: `# /spek.rarv`
- **No agent-specific syntax**: no `@workspace`, `#file:`, `[[wikilink]]`
- **Steps**: imperative mood; numbered; reference vault paths and lat.md commands

### `spek-blind-review.md`

- **Location in package**: `spekificity/skills/spek-blind-review.md`
- **Distributed as**: same rules as above
- **Required sections** (in order): `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`
- **Heading**: `# /spek.blind-review`
- **No agent-specific syntax**: no `@workspace`, `#file:`, `[[wikilink]]`
- **Anonymization step**: explicitly states "operate on working memory only; never modify original files"

---

## Updated Skill File Touch Points

| Skill File | Change |
|-----------|--------|
| `spek-conclude.md` | Add optional RARV hint + optional blind-review hint at end of Steps |
| `spek-plan.md` | Add anti-sycophancy validation step before user review |
| `spek-prepare.md` | Add token budget check step (skip if not configured) |
| `spek-implement.md` | Add token budget phase tracking step |
| `spek-conclude.md` | Add backprop reflex step (Step 3) + token budget summary |
| `spek-lessons.md` | Add token budget note (already has autolink from 003) |
