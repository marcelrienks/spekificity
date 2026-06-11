# Quickstart & Validation Guide: Planned Features

## Prerequisites

- Spec 003 fully implemented (all 56 tasks complete, 102 tests pass)
- `.spek/vault/` initialized with `decisions.md`, `patterns.md`, `lessons/`
- `.spek/config.yaml` present

Run from project root: `/Users/marcel.rienks/WorkSpace/personal/spekificity/`

---

## Scenario 1: Token Budget Config Written on Init

**Validates**: FR-001, SC-001

```bash
# 1. Create a clean project and run spek init
cd /tmp/test-004-token-budget
git init
uv run spek init --integration claude --script sh

# 2. Verify token_budget block in config
grep -A 3 "token_budget:" .spek/config.yaml
```

**Expected output**:
```
token_budget:
  per_feature: null
  alert_thresholds: []
```

**Also verify `antisycophancy:` block**:
```bash
grep -A 3 "antisycophancy:" .spek/config.yaml
```
Expected:
```
antisycophancy:
  enabled: true
  complexity_threshold: 2.0
  contradiction_pairs: []
```

---

## Scenario 2: Backprop Reflex — Pytest Failure Captured

**Validates**: FR-005, FR-006, FR-007, SC-002

```python
# Run from Python REPL or test:
from pathlib import Path
from spekificity.vault.backprop import backprop_reflex

vault_path = Path(".spek/vault")
test_output = """
FAILED tests/unit/vault/test_init.py::TestInitVault::test_calls_open_vault - AssertionError: mock not called
FAILED tests/unit/speckit/test_config.py::TestWriteSpekConfig::test_creates_config_yaml - AssertionError
"""

result = backprop_reflex(test_output, vault_path)
print(result)
```

**Expected**:
- `result.warnings_added == 2`
- `.spek/vault/patterns.md` contains two `> ⚠ Backprop warning` blockquotes
- `.spek/memory/backprop-seen.yaml` contains two entries

```bash
grep "Backprop warning" .spek/vault/patterns.md
cat .spek/memory/backprop-seen.yaml
```

---

## Scenario 3: Backprop Reflex — Idempotency

**Validates**: FR-008, SC-009

```python
# Re-run with same output:
result2 = backprop_reflex(test_output, vault_path)
print(result2.warnings_added)  # Expected: 0 (no new warnings added)

# Verify patterns.md still has only 2 warnings (not 4):
import subprocess
subprocess.run(["grep", "-c", "Backprop warning", ".spek/vault/patterns.md"])
# Expected: 2
```

---

## Scenario 4: Backprop Reflex — No Failures

**Validates**: FR-007 (skip path)

```python
result = backprop_reflex("All tests passed.", vault_path)
assert result.skipped is True
assert result.warnings_added == 0
# [SKIP] printed to stdout
```

---

## Scenario 5: Anti-Sycophancy — Contradiction Detected

**Validates**: FR-010, FR-011, SC-003, SC-008

```python
from spekificity.vault.antisycophancy import validate_spec

# Set up a vault with a conflicting decision
vault = Path(".spek/vault")
(vault / "decisions.md").write_text("# Decisions\n\nUse dependency injection for all services.")

spec_with_conflict = """
## Architecture
Use service locator pattern for auth service discovery.
"""

result = validate_spec(spec_with_conflict, vault, {})
print(result.violations)
```

**Expected**:
- `result.violations[0].rule == "CONTRADICTION"`
- `result.violations[0].severity == "HIGH"`
- Message references "dependency injection" and "service locator"
- `.spek/memory/violations.md` created with entry

```bash
cat .spek/memory/violations.md
```

---

## Scenario 6: Anti-Sycophancy — Disabled

**Validates**: FR-016, SC-008

```python
result = validate_spec("any spec text", vault, {"antisycophancy": {"enabled": False}})
assert result.skipped is True
# [SKIP] printed; violations.md unchanged
```

---

## Scenario 7: RARV Skill File Valid

**Validates**: FR-018, FR-019, SC-004

```bash
# Confirm file exists and has correct structure
cat spekificity/skills/spek-rarv.md
```

**Expected**: File starts with `# /spek.rarv`, contains all four H2 sections in order:
```
## Prerequisites
## Steps
## Output
## Exit Criteria
```

No occurrences of `@workspace`, `#file:`, or `[[wikilink]]` (agent syntax):
```bash
grep -E "@workspace|#file:|\[\[" spekificity/skills/spek-rarv.md
# Expected: no output
```

---

## Scenario 8: Blind Review Skill File Valid

**Validates**: FR-023, FR-024, SC-005

```bash
cat spekificity/skills/spek-blind-review.md
grep "never modify original" spekificity/skills/spek-blind-review.md
# Expected: line found confirming anonymization is in-memory only
```

---

## Scenario 9: Skill Files Distributed to Integration Paths

**Validates**: FR-022, FR-027, SC-006

```bash
# spek init in a clean project (integration=claude)
ls .claude/commands/ | grep spek
```

**Expected**: 9 files (7 original + spek-rarv.md + spek-blind-review.md):
```
spek-blind-review.md
spek-conclude.md
spek-context.md
spek-implement.md
spek-lessons.md
spek-map.md
spek-plan.md
spek-prepare.md
spek-rarv.md
```

---

## Scenario 10: Full Test Suite Green

**Validates**: SC-007

```bash
uv run pytest --tb=short -q
```

**Expected**: All tests pass. Minimum count: 102 existing + new tests for backprop and antisycophancy.
No regressions in existing 102 tests.

---

## Edge Cases to Validate Manually

| Case | How to Test |
|------|------------|
| Backprop with empty vault (no patterns.md) | Run `backprop_reflex()` before vault init; confirm patterns.md created |
| Anti-sycophancy with empty vault | Run `validate_spec()` with no decisions.md; confirm Rule 1 skips, returns empty violations |
| Token budget null (unconfigured) | Confirm all skill files run without budget warnings |
| Both new skill files in cursor-agent subfolder format | `spek init --integration cursor-agent` → check `.cursor/skills/spek-rarv/SKILL.md` |
