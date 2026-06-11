# Data Model: Planned Features Implementation

## Entities

### BackpropResult

Returned by `backprop_reflex()`.

| Field | Type | Description |
|-------|------|-------------|
| `warnings_added` | `int` | Count of vault warnings written this run |
| `skipped` | `bool` | True when no failures in input |
| `failures_parsed` | `list[str]` | Canonical keys of parsed failures |

### Failure (internal)

Internal structure used during backprop processing.

| Field | Type | Description |
|-------|------|-------------|
| `test_path` | `str` | e.g. `"tests/unit/vault/test_init.py"` |
| `test_name` | `str` | e.g. `"TestInitVault::test_calls_open_vault"` |
| `failure_type` | `str` | Canonical type: `"assertion_failure"`, `"race_condition"`, `"timeout"`, `"import_error"`, `"attribute_error"`, `"key_error"`, `"type_error"`, `"value_error"`, `"io_error"`, `"connection_error"`, `"unknown"` |
| `dedup_key` | `str` | `f"{test_path}::{failure_type}"` |

### Violation

One entry in anti-sycophancy validation output.

| Field | Type | Description |
|-------|------|-------------|
| `rule` | `str` | `"CONTRADICTION"`, `"COMPLEXITY"`, `"PATTERN"`, `"STACK_DRIFT"` |
| `severity` | `str` | `"HIGH"`, `"MEDIUM"`, `"LOW"` |
| `message` | `str` | Human-readable description with specifics |
| `spec_excerpt` | `str` | Relevant snippet from spec text (≤80 chars) |

### ValidationResult

Returned by `validate_spec()`.

| Field | Type | Description |
|-------|------|-------------|
| `violations` | `list[Violation]` | All violations found (empty = pass) |
| `skipped` | `bool` | True when `antisycophancy.enabled: false` |

---

## Persistent Storage Schemas

### `.spek/memory/backprop-seen.yaml`

```yaml
seen_failures:
  - test_path: "tests/unit/vault/test_init.py::TestInitVault::test_calls_open_vault"
    failure_type: "assertion_failure"
    first_seen: "2026-06-11"
    count: 1
```

**Rules**:
- Created on first backprop run; never truncated; entries append-only
- `count` incremented if same key seen again (but vault warning NOT re-appended)
- `first_seen` is ISO date string (`YYYY-MM-DD`); no timezone

### `.spek/memory/violations.md`

```markdown
## 2026-06-11 | CONTRADICTION | HIGH

**Spec excerpt**: "use service locator for auth"
**Vault decision**: "Use dependency injection (decisions.md)"
**Message**: spec contradicts vault: "dependency injection" vs "service locator"

---
```

**Rules**:
- Append-only; never overwritten
- One `##` section per violation per run
- Separator `---` between entries

### `.spek/config.yaml` additions

```yaml
token_budget:
  per_feature: null           # Team-defined; null disables tracking
  alert_thresholds: []        # List of {phase: name, pct: 80} objects

antisycophancy:
  enabled: true
  complexity_threshold: 2.0   # Flag if spec > 2× avg vault spec word count
  contradiction_pairs: []     # Add custom pairs; merged with defaults
```

---

## Config Schema State After 004

Full `.spek/config.yaml` schema produced by `speckit/config.py` after this feature:

```yaml
integration: {integration}
script_type: {script_type}
tools:
  speckit:
    enabled: true
  lat_md:
    enabled: true
    index_path: .spek/lat/
  vault:
    enabled: true
    path: .spek/vault/
    obsidian_vault_name: vault
context_loading:
  cache_expiry_minutes: 60
token_limits:
  standard: 3500
  lite: 2000
  ultra: 1000
autolink:
  enabled: true
  threshold: 0.8
  keyword_tags: {}
token_budget:
  per_feature: null
  alert_thresholds: []
antisycophancy:
  enabled: true
  complexity_threshold: 2.0
  contradiction_pairs: []
```

---

## New Skill File Inventory

| Skill | Path | Triggers |
|-------|------|---------|
| `/spek.rarv` | `spekificity/skills/spek-rarv.md` | Optional after `/spek.conclude` |
| `/spek.blind-review` | `spekificity/skills/spek-blind-review.md` | Optional before `/spek.conclude` archival |

Both are distributed by existing `skills_install/copy.py` (no code changes).

---

## Module Responsibilities

| Module | Owns | Does NOT own |
|--------|------|-------------|
| `vault/backprop.py` | Parse test output, dedup, append vault warning | Deciding which vault file to update (always `patterns.md`) |
| `vault/antisycophancy.py` | 4 validation rules, violation logging | Halting execution (caller reads result) |
| `spek-rarv.md` | RARV 4-phase cycle instructions | Code comparison engine (agent + lat.md do it) |
| `spek-blind-review.md` | Anonymization + review steps | Actual linter invocation (agent tool-calls linter) |

---

## State Transitions

### Backprop Lifecycle

```
test output (string)
  → parse failures → list[Failure]
  → dedup check vs backprop-seen.yaml → list[Failure] (new only)
  → append vault warning per failure → updated patterns.md
  → update backprop-seen.yaml
  → return BackpropResult
```

### Anti-Sycophancy Lifecycle

```
spec text + vault_path + config
  → load vault (decisions.md, patterns.md, prior specs)
  → run Rule 1 (contradiction) → list[Violation]
  → run Rule 2 (complexity) → list[Violation]
  → run Rule 3 (pattern) → list[Violation]
  → run Rule 4 (stack drift) → list[Violation]
  → if violations: append violations.md, print each
  → return ValidationResult
```
