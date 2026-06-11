# Research: Planned Features Implementation

## Q1: Test Output Parsing

**Decision**: Regex-based per-format parser; stdlib only (`re` module); pytest is primary (project uses pytest with `testpaths = ["tests"]` in `pyproject.toml`); jest/mocha as secondary.

**Patterns**:

| Runner | Pattern | Captures |
|--------|---------|---------|
| pytest | `r"FAILED\s+([\w/]+\.py)::([\w:]+)"` | test_path, test_name |
| pytest error | `r"ERROR\s+([\w/]+\.py)::([\w:]+)"` | test_path, test_name |
| jest | `r"●\s+(.+?)\s+›\s+(.+)"` | suite, test_name |
| mocha | `r"^\s+\d+\)\s+(.+)$"` (MULTILINE) | test_name |

**Failure type inference** (all formats): scan failure message line for keywords: `race`, `timeout`, `assert`, `import`, `attribute`, `key`, `type`, `value`, `io`, `connection`. Map to canonical type string.

**Alternatives considered**: `pytest-json-report` plugin for structured output — rejected (adds external dep; not all projects use pytest; regex works offline).

---

## Q2: Technology Name Extraction

**Decision**: Two-pass regex extraction after markdown stripping (reuse `_strip_markdown` approach from `vault/autolink.py`).

**Pass 1 — CamelCase proper nouns**: `r"\b[A-Z][a-zA-Z0-9]{2,}\b"` — matches `React`, `PostgreSQL`, `TypeScript`, `FastAPI`. Filter against expanded stopword set.

**Pass 2 — Version strings**: `r"v?\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9]+)?"` — matches `v1.2`, `3.11`, `22.0.0-beta`. Associate with the preceding proper noun.

**Filter**: Drop words already in vault patterns (known techs are fine; unknowns trigger alert).

**Alternatives considered**: spaCy NER — rejected (external dep; overkill for this use case).

---

## Q3: Anti-Sycophancy Contradiction Pairs

**Decision**: Hardcoded bidirectional pairs in `antisycophancy.py`; configurable override via `antisycophancy.contradiction_pairs` in `.spek/config.yaml`.

**Default pairs** (from `wiki/decision.md` examples):

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

Check both directions: if vault says "use X" and spec proposes "Y" (where X↔Y is a pair) → flag.

**Alternatives considered**: Embedding-based semantic contradiction detection — rejected (requires external model; must work offline; overkill for deterministic rules).

---

## Q4: backprop-seen.yaml Dedup Schema

**Decision**: Simple composite key (human-readable); no SHA-256 hashing. Format:

```yaml
seen_failures:
  - test_path: "tests/unit/vault/test_autolink.py::TestBuildVaultIndex::test_empty_vault"
    failure_type: "assertion_failure"
    first_seen: "2026-06-11"
    count: 1
```

**Dedup key** (in-memory): `f"{test_path}::{failure_type}"` — string comparison, no hashing.

**Rationale**: Human-readable for debugging; composite key is unique enough for test failure dedup; `count` enables trend analysis; `first_seen` enables age-based cleanup. Matches project's YAML-first memory conventions.

**Alternatives considered**: SHA-256 hash — rejected (opaque; harder to inspect/debug; no benefit given low collision risk for test path strings).

---

## Summary: All NEEDS CLARIFICATION Resolved

| Unknown | Resolution |
|---------|-----------|
| Test output parser format | Regex per format; pytest primary; jest/mocha secondary |
| Tech name extraction | CamelCase + version regex; two-pass; stdlib only |
| Contradiction detection | Bidirectional keyword pair matching; 7 default pairs; configurable |
| Dedup schema | Composite key YAML; human-readable; count tracking |
| Code anonymization approach | Agent in-memory only; no temp files (per spec assumption) |
| RARV comparison engine | Agent-driven via lat.md + spec text; no Python code needed |
| Token tracking mechanism | Agent-side from response metadata; config thresholds only |
