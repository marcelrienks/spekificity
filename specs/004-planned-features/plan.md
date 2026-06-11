# Implementation Plan: Planned Features Implementation

**Branch**: `004-planned-features` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-planned-features/spec.md`

## Summary

Implement five features deferred from spec 003. Phased by dependency order — Token Budget first (independent), then Backprop (foundation), then Anti-Sycophancy (foundation), then RARV (needs Backprop), then Blind Review (independent, lower priority).

| Phase | What | Deliverable |
|-------|------|-------------|
| **P1: Token Budget** | Config schema + skill file updates | Updated `speckit/config.py`, updated 4 skill files |
| **P2: Backprop Reflex** | Python module + conclude integration | `vault/backprop.py`, updated `spek-conclude.md` |
| **P3: Anti-Sycophancy** | Python module + plan integration | `vault/antisycophancy.py`, updated `spek-plan.md` |
| **P4: RARV** | New skill file + conclude hint | `skills/spek-rarv.md`, updated `spek-conclude.md` |
| **P5: Blind Review** | New skill file + conclude hint | `skills/spek-blind-review.md`, updated `spek-conclude.md` |

P1 has no dependencies — start immediately. P2 and P3 are independent of each other, both depend on foundation only. P4 depends on P2 being settled (references Backprop in RARV steps). P5 is independent of P2/P3/P4.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: stdlib only (`re`, `difflib`, `hashlib`, `pathlib`, `subprocess`) — no new external packages

**Storage**: `.spek/memory/backprop-seen.yaml` (dedup store), `.spek/memory/violations.md` (violation log)

**Testing**: pytest; `tmp_path` for filesystem tests; `unittest.mock.patch` for subprocess

**Target Platform**: macOS, Windows, Linux (same as spec 003)

**Constraints**: No external NLP deps; no network calls; all analysis must work offline

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Development | ✅ PASS | Spec reviewed and approved |
| II. Token Efficiency | ✅ PASS | Token budget itself enforces this; backprop feeds loop |
| III. Deterministic 4-Stage Workflow | ✅ PASS | All new features slot into existing stages |
| IV. Persistent Memory | ✅ PASS | Backprop writes to vault; violations logged to memory |
| V. Simplicity & Composability | ✅ PASS | Each feature is one module; skill files are independent |

## Project Structure

### New Files

```text
spekificity/
├── vault/
│   ├── backprop.py                 # P2: test failure → vault warning pipeline
│   └── antisycophancy.py           # P3: spec validation against vault decisions
│
└── skills/
    ├── spek-rarv.md                # P4: RARV reflection cycle skill
    └── spek-blind-review.md        # P5: blind code review skill

tests/
└── unit/
    └── vault/
        ├── test_backprop.py        # P2
        └── test_antisycophancy.py  # P3
```

### Modified Files

```text
spekificity/
├── speckit/
│   └── config.py                   # P1: add token_budget block to YAML template
└── skills/
    ├── spek-prepare.md             # P1: add token budget step reference
    ├── spek-plan.md                # P1+P3: token budget + anti-sycophancy validation step
    ├── spek-implement.md           # P1: token budget step reference
    ├── spek-conclude.md            # P1+P2+P4+P5: token budget + backprop step + RARV/blind hints
    ├── spek-lessons.md             # P1: token budget step reference (already has autolink from P8)
    └── spek-context.md             # (no changes)

tests/
└── unit/
    └── speckit/
        └── test_config.py          # P1: assert token_budget block present
```

---

## P1: Token Budget Model

Config-only change + skill file updates. No new Python module. No runtime enforcement — soft warnings only.

### `speckit/config.py` addition

Add `token_budget:` block after `autolink:` in the YAML template:

```yaml
token_budget:
  per_feature: null           # Team-defined; null = no budget tracking
  alert_thresholds: []        # Configure warning thresholds as needed
```

When `per_feature` is `null`, all budget tracking steps in skill files skip silently.

### Skill file updates (4 files)

Each skill file gets one line added to `## Steps` referencing token awareness:

- `spek-prepare.md`: "Check token budget remaining for this feature (skip if `token_budget.per_feature` not set)"
- `spek-plan.md`: "Track token cost for spec/plan generation phase against configured threshold"
- `spek-implement.md`: "Track token cost for implementation phase; print `[WARN]` if threshold exceeded"
- `spek-conclude.md`: "Summarize total token usage for feature; compare against `token_budget.per_feature`"

No enforcement logic in Python — agent reads config and emits `[WARN]` per skill instructions.

---

## P2: Backprop Reflex

New module `spekificity/vault/backprop.py`. Called from `spek-conclude.md` Step 3.

### Module Design

```python
@dataclass
class BackpropResult:
    warnings_added: int = 0
    skipped: bool = False
    failures_parsed: list[str] = field(default_factory=list)

_FAILURE_PATTERNS = [
    # pytest: "FAILED tests/path.py::test_name - ErrorType: message"
    re.compile(r"FAILED\s+([\w/]+\.py)::(\w+)"),
    # jest/mocha: "✕ test name (Xms)"  or  "× test name"
    re.compile(r"[✕×]\s+(.+?)(?:\s+\(\d+ms\))?$", re.MULTILINE),
]

_FAILURE_TYPE_MAP = {
    "race": "race_condition",
    "timeout": "timeout",
    "assert": "assertion_failure",
    "import": "import_error",
    "attribute": "attribute_error",
    # ... extensible
}

def _parse_failures(test_output: str) -> list[dict]:
    # apply each pattern; extract test_path, test_name, infer failure_type
    # return list of {test_path, test_name, failure_type}

def _dedup_key(failure: dict) -> str:
    return hashlib.sha256(
        f"{failure['test_path']}::{failure['failure_type']}".encode()
    ).hexdigest()[:16]

def _load_seen(seen_path: Path) -> set[str]:
    # read .spek/memory/backprop-seen.yaml; return set of seen keys
    # return empty set if file absent

def _save_seen(seen_path: Path, seen: set[str]) -> None:
    # write updated seen set to YAML file; create parent dirs

def _append_vault_warning(vault_path: Path, failure: dict) -> None:
    # append to .spek/vault/patterns.md:
    # > ⚠ Backprop warning [{failure_type}]: `{test_path}::{test_name}` failed.
    # > Review for: {failure_type} patterns in related code.

def backprop_reflex(test_output: str, vault_path: Path) -> BackpropResult:
    # orchestrate: parse → dedup check → append → save seen → return result
```

**No subprocess calls** — pure string parsing. Idempotent via SHA-256 content hash stored in `.spek/memory/backprop-seen.yaml`.

---

## P3: Anti-Sycophancy Validation

New module `spekificity/vault/antisycophancy.py`. Called from `spek-plan.md` before user review.

### Module Design

```python
@dataclass
class Violation:
    rule: str       # "CONTRADICTION" | "COMPLEXITY" | "PATTERN" | "STACK_DRIFT"
    severity: str   # "HIGH" | "MEDIUM" | "LOW"
    message: str
    spec_excerpt: str = ""

@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)
    skipped: bool = False

def _load_vault_text(vault_path: Path, filename: str) -> str:
    # read .spek/vault/<filename> text; return "" if absent

def _rule_contradiction(spec_text: str, decisions_text: str) -> list[Violation]:
    # extract "Use X" / "Prefer X" directives from decisions_text
    # check if spec_text contains opposing directives ("service locator" vs "dependency injection")
    # simple keyword matching; configurable opposing-pairs dict

def _rule_complexity(spec_text: str, vault_path: Path, threshold: float) -> list[Violation]:
    # scan .spek/vault/specs/ for prior spec files; compute avg word count
    # if len(spec_text.split()) > avg * threshold → flag MEDIUM

def _rule_pattern_consistency(spec_text: str, patterns_text: str) -> list[Violation]:
    # extract recent pattern names from patterns.md
    # if spec deviates → flag LOW (informational only)

def _rule_stack_drift(spec_text: str, patterns_text: str) -> list[Violation]:
    # extract tech names from spec (capitalized proper nouns, version strings)
    # check against patterns_text; flag if not found

def _write_violations(violations: list[Violation], memory_path: Path) -> None:
    # append to .spek/memory/violations.md; create if absent
    # format: date, rule, severity, message per entry; append-only

def validate_spec(spec_text: str, vault_path: Path, config: dict) -> ValidationResult:
    cfg = config.get("antisycophancy", {})
    if not cfg.get("enabled", True):
        print_status("SKIP", "anti-sycophancy validation disabled")
        return ValidationResult(skipped=True)
    # run all 4 rules; collect violations; write if any; print per violation
```

**Configuration additions to `.spek/config.yaml`:**
```yaml
antisycophancy:
  enabled: true
  complexity_threshold: 2.0    # flag if spec > 2x avg vault spec word count
```

---

## P4: RARV Reflection Cycles

New skill file only. No new Python module — agent performs comparison using lat.md + vault context. Called as optional standalone skill after `/spek.conclude`.

### `spekificity/skills/spek-rarv.md` structure

```markdown
# /spek.rarv

## Prerequisites
- `/spek.conclude` completed for current feature
- `.spek/vault/specs/` contains the original spec for this feature
- `lat.md` code index current (`lat init` run after last commit)

## Steps
1. REASON: Load original spec from `.spek/vault/specs/`; query lat.md for implemented symbols; compare
2. REASON: Identify deviations — additions (code has X, spec does not), omissions (spec requires Y, code lacks it), architecture changes
3. ACT: For each deviation, prompt user: Option A (fix code), Option B (update spec + vault), Option C (defer to tech debt)
4. REFLECT: If Option B chosen, update relevant vault decision file with new rationale and mark deviation `justified`
5. REFLECT: If Option C chosen, append tech debt item to `.spek/vault/patterns.md`
6. VERIFY: Re-read updated vault decisions; confirm no contradictions introduced; print alignment summary

## Output
- Deviation report: list of additions, omissions, architecture changes with user-chosen resolution
- Updated vault decision files (if Option B chosen)
- Tech debt entries in patterns.md (if Option C chosen)
- Alignment summary: `spec and code aligned after RARV` or `N deviations deferred`

## Exit Criteria
- All deviations have a recorded resolution (A, B, or C)
- Vault updated where Option B was chosen
- No new contradictions in vault decisions
- Alignment summary printed
```

### Update `spek-conclude.md`

Add at end of Steps: `Optional: run /spek.rarv to detect and resolve spec drift (recommended for features with architectural changes)`

---

## P5: Blind Code Review

New skill file only. No new Python module — agent performs anonymization in working memory; linting invoked via existing `run_command` pattern through agent tool use.

### `spekificity/skills/spek-blind-review.md` structure

```markdown
# /spek.blind-review

## Prerequisites
- Feature implementation complete
- Test suite passes (run before anonymization)
- Linter configured (pylint, eslint, or equivalent)

## Steps
1. Anonymize source files in working memory: strip comments containing vendor/agent names
   (`claude`, `copilot`, `chatgpt`, `openai`, `anthropic`); replace service class names with
   generic aliases (AuthService → ServiceA) for review; NEVER modify original files
2. Run linter on anonymized copy; capture output; report findings with severity
3. Confirm all tests pass (`pytest` or configured runner); report failures as CRITICAL
4. Check function complexity: flag functions exceeding 20 lines or cyclomatic complexity > 10
5. Report all findings: `CRITICAL` (blocks merge), `WARNING` (should fix), `INFO` (informational)

## Output
- Anonymized review report: findings by severity with file:line references
- Summary: total CRITICAL / WARNING / INFO counts
- Remediation hints per finding

## Exit Criteria
- All CRITICAL findings reviewed (fixed or explicitly accepted)
- Findings report written to `.spek/memory/blind-review-YYYY-MM-DD.md`
- Original source files confirmed unchanged (hash check)
```

### Update `spek-conclude.md`

Add at end of Steps (after RARV hint): `Optional: run /spek.blind-review for a context-free quality pass before archiving`

---

## Complexity Tracking

> No constitution violations to justify.
> Token Budget, Backprop, Anti-Sycophancy are self-contained modules with no cross-feature state.
> RARV and Blind Review are skill-file-only; no new Python modules introduced.
> Total new Python code: ~2 modules, ~200 LOC each. Scope bounded.
