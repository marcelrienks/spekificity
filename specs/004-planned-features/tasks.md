# Tasks: Planned Features Implementation

**Input**: Design documents from `specs/004-planned-features/`

**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅ quickstart.md ✅

**Tests**: Included for Python modules (backprop.py, antisycophancy.py). Skill files verified by format check only.

**Organization**: Tasks grouped by user story (US1–US5) matching spec.md priorities P1–P5.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable — different files, no incomplete shared dependencies
- **[Story]**: User story label (US1–US5)

---

## Phase 1: Setup

No setup tasks needed — project initialized, no new external dependencies (`re`, `pathlib`, `datetime`, `hashlib` are all stdlib).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update config template and test once for both `token_budget` (US1) and `antisycophancy` (US3) blocks — both live in the same file; updating together avoids two sequential edits to the same file.

**⚠️ CRITICAL**: T001 and T002 must complete before US1 and US3 work begins.

- [X] T001 Update `spekificity/speckit/config.py` — append two YAML blocks to `_CONFIG_TEMPLATE` string after the `autolink:` block: (1) `token_budget:\n  per_feature: null\n  alert_thresholds: []\n` and (2) `antisycophancy:\n  enabled: true\n  complexity_threshold: 2.0\n  contradiction_pairs: []\n`; no format-string escaping needed for these static values
- [X] T002 [P] Update `tests/unit/speckit/test_config.py` — in `test_config_contains_all_required_fields`, add assertions: `assert "token_budget:" in content`, `assert "per_feature: null" in content`, `assert "antisycophancy:" in content`, `assert "complexity_threshold: 2.0" in content`, `assert "contradiction_pairs:" in content`

**Checkpoint**: Config template updated, tests green — US1 and US3 skill file work can now proceed.

---

## Phase 3: User Story 1 - Token Budget Model (Priority: P1) 🎯 MVP

**Goal**: Token budget config block written by `spek init`; all 5 workflow skill files include a token-awareness step that skips silently when `per_feature: null`.

**Independent Test**: Run `spek init` on a clean project, verify `token_budget:` block in `.spek/config.yaml`; inspect each skill file for the budget step.

- [X] T003 [P] [US1] Update `spekificity/skills/spek-prepare.md` — add as final item in `## Steps`: `5. Check token budget: read \`token_budget.per_feature\` from \`.spek/config.yaml\`; print \`[WARN] token budget: check remaining before starting\` if \`per_feature\` is set; skip silently if null`; add to `## Exit Criteria`: `token budget checked (or skipped if not configured)`
- [X] T004 [P] [US1] Update `spekificity/skills/spek-plan.md` — add to `## Steps` before user review gate: `Track token cost for spec/plan generation phase; print \`[WARN] token budget: plan phase cost high\` if cost approaches configured \`alert_thresholds\`; non-blocking`; add to `## Exit Criteria`: `token cost within budget or warning issued`
- [X] T005 [P] [US1] Update `spekificity/skills/spek-implement.md` — add to `## Steps`: `Track token cost for implementation phase per task; print \`[WARN] token budget: implementation phase threshold reached\` if configured threshold exceeded; execution continues`
- [X] T006 [P] [US1] Update `spekificity/skills/spek-lessons.md` — add to `## Steps` after autolink step (step 5): `6. Note token budget: print total estimated token cost for this feature cycle for retrospective context; skip if \`token_budget.per_feature\` not configured`
- [X] T007 [US1] Update `spekificity/skills/spek-conclude.md` — add to `## Steps` before the git commit step: `Summarize total token usage for feature; compare against \`token_budget.per_feature\`; print \`[WARN] token budget: feature exceeded budget\` if over; skip if \`per_feature: null\``; add to `## Exit Criteria`: `token usage summarized`

**Checkpoint**: US1 complete — `spek init` writes `token_budget` config; all skill files reference budget tracking.

---

## Phase 4: User Story 2 - Backprop Reflex (Priority: P2)

**Goal**: `backprop_reflex(test_output, vault_path)` parses test failures, deduplicates via `.spek/memory/backprop-seen.yaml`, and appends `> ⚠ Backprop warning` blockquotes to `.spek/vault/patterns.md`. Called from `/spek.conclude` Step 3.

**Independent Test**: `backprop_reflex(pytest_failure_str, tmp_vault_path)` returns `warnings_added == 1`; re-run returns `warnings_added == 0` (idempotent). See quickstart.md Scenarios 2–4.

- [X] T008 [US2] Implement `spekificity/vault/backprop.py` — `BackpropResult` dataclass (`warnings_added: int = 0`, `skipped: bool = False`, `failures_parsed: list[str] = field(default_factory=list)`); `_FAILURE_PATTERNS: list[re.Pattern]` = three compiled patterns: pytest `r"FAILED\s+([\w/\.]+)::(\w+)"`, jest `r"●\s+(.+?)\s+›\s+(.+)"`, mocha `r"^\s+\d+\)\s+(.+)$"` (re.MULTILINE); `_FAILURE_TYPE_MAP: dict[str, str]` mapping keywords ("race"→"race_condition", "timeout"→"timeout", "assert"→"assertion_failure", "import"→"import_error", "attribute"→"attribute_error", "key"→"key_error", "type"→"type_error", "value"→"value_error", "io"→"io_error", "connection"→"connection_error"); `_parse_failures(test_output: str) -> list[dict]` applies each pattern, returns list of `{"test_path": str, "test_name": str, "failure_type": str}` dicts; `_infer_failure_type(message: str) -> str` scans message for _FAILURE_TYPE_MAP keys, returns "unknown" if none match; `_dedup_key(failure: dict) -> str` returns `f"{failure['test_path']}::{failure['failure_type']}"`; `_load_seen(seen_path: Path) -> dict[str, dict]` reads YAML `seen_failures` list from file (key = dedup_key), returns `{}` if absent or malformed; `_save_seen(seen_path: Path, seen: dict[str, dict]) -> None` writes `seen_failures` list to YAML, creates parent dirs; `_append_vault_warning(patterns_path: Path, failure: dict) -> None` appends `\n> ⚠ Backprop warning [{failure_type}]: \`{test_path}::{test_name}\` failed.\n> Review for: {failure_type} patterns in related code.\n` to patterns_path, creates file if absent; `backprop_reflex(test_output: str, vault_path: Path) -> BackpropResult` orchestrates all steps — parse → dedup check → append warning → update seen → return result; prints `[SKIP]` if no failures, `[OK]` per new warning; imports `print_status` from `spekificity.utils`; stdlib only (`re`, `pathlib`, `datetime`)
- [X] T009 [P] [US2] Write `tests/unit/vault/test_backprop.py` — `TestParseFailures`: test pytest pattern extracts `test_path` and `test_name`; test empty output returns `[]`; test non-failure output returns `[]`; `TestInferFailureType`: test "AssertionError" → "assertion_failure"; test unknown message → "unknown"; `TestDedupKey`: test consistent key format; `TestLoadSeen`: test returns `{}` when file absent; test returns dict with correct keys when YAML present; `TestAppendVaultWarning`: test appends blockquote to existing patterns.md; test creates patterns.md if absent; test correct format (`> ⚠ Backprop warning`); `TestBackpropReflex`: test pytest failure output → `warnings_added == 1`; test idempotency (second call → `warnings_added == 0`); test empty input → `skipped == True`; test two distinct failures → `warnings_added == 2`; use `tmp_path`
- [X] T010 [US2] Update `spekificity/skills/spek-conclude.md` — insert as new numbered step after the current Step 2 (lessons sub-step): `3. Run Backprop Reflex: parse test failure output from last test run; call \`backprop_reflex()\` with vault path; append \`> ⚠ Backprop warning\` blockquotes to \`.spek/vault/patterns.md\` for each new failure pattern; skip if no test failures in output`; renumber subsequent steps; add to `## Exit Criteria`: `failure patterns from this feature captured in vault (or none found)`

**Checkpoint**: US2 complete — `backprop_reflex()` functional; conclude skill updated; tests pass.

---

## Phase 5: User Story 3 - Anti-Sycophancy Validation (Priority: P3)

**Goal**: `validate_spec(spec_text, vault_path, config)` runs 4 rules against vault, returns `ValidationResult` with violations; violations appended to `.spek/memory/violations.md`. Called from `/spek.plan` before user review.

**Independent Test**: `validate_spec(spec_with_conflict, vault_path, {})` returns violation with `rule == "CONTRADICTION"`, `severity == "HIGH"`. `validate_spec` with `antisycophancy.enabled=False` returns `skipped=True`. See quickstart.md Scenarios 5–6.

- [X] T011 [US3] Implement `spekificity/vault/antisycophancy.py` — `Violation` dataclass (`rule: str`, `severity: str`, `message: str`, `spec_excerpt: str = ""`); `ValidationResult` dataclass (`violations: list[Violation] = field(default_factory=list)`, `skipped: bool = False`); `_CONTRADICTION_PAIRS: list[tuple[str, str]]` = 7 bidirectional pairs per research.md: `[("dependency injection", "service locator"), ("observer pattern", "direct subscription"), ("layered architecture", "monolithic"), ("api-first", "implementation-first"), ("synchronous", "asynchronous"), ("singleton", "factory"), ("immutable", "mutable state")]`; `_load_vault_text(vault_path: Path, filename: str) -> str` reads file, returns "" if absent; `_rule_contradiction(spec_text: str, decisions_text: str, extra_pairs: list) -> list[Violation]` — for each pair in `_CONTRADICTION_PAIRS + extra_pairs`: if `pair[0]` in `decisions_text.lower()` and `pair[1]` in `spec_text.lower()` → flag HIGH violation (or reverse); `_rule_complexity(spec_text: str, vault_path: Path, threshold: float) -> list[Violation]` — glob `vault_path / "specs" / "*.md"`, compute avg word count; if `len(spec_text.split()) > avg * threshold` → MEDIUM violation; skip if no prior specs; `_rule_pattern_consistency(spec_text: str, patterns_text: str) -> list[Violation]` — extract lines starting with `-` from patterns_text as pattern names; if 3+ recent patterns share a keyword absent from spec → LOW violation; `_rule_stack_drift(spec_text: str, patterns_text: str) -> list[Violation]` — extract CamelCase words `r"\b[A-Z][a-zA-Z0-9]{2,}\b"` and version strings `r"v?\d+\.\d+"` from spec_text; for each not found in patterns_text → MEDIUM violation; filter common English words (keep only tech-looking names); `_write_violations(violations: list[Violation], memory_path: Path) -> None` — append `## {date} | {rule} | {severity}\n\n**Spec excerpt**: ...\n**Message**: ...\n\n---\n` to violations.md, create if absent; `validate_spec(spec_text: str, vault_path: Path, config: dict) -> ValidationResult` — check `config.get("antisycophancy", {}).get("enabled", True)`, print `[SKIP]` and return if False; get `complexity_threshold` (default 2.0) and `extra_pairs` from config; run all 4 rules; if violations: `_write_violations`, print each via `print_status("WARN", ...)`; print `[OK] anti-sycophancy checks passed` if no violations; return result; stdlib only (`re`, `datetime`, `pathlib`)
- [X] T012 [P] [US3] Write `tests/unit/vault/test_antisycophancy.py` — `TestRuleContradiction`: test returns HIGH violation when vault has "dependency injection" and spec has "service locator"; test reverse direction also flagged; test no contradiction → empty list; `TestRuleComplexity`: test returns MEDIUM when spec word count > 2× avg of vault specs; test returns empty when no prior specs; test returns empty when below threshold; `TestRuleStackDrift`: test CamelCase tech in spec not in patterns → MEDIUM violation; test tech present in patterns → no violation; test version strings extracted; `TestRulePatternConsistency`: test LOW violation when spec deviates from repeated pattern; `TestWriteViolations`: test creates violations.md with correct `##` section format; test appends (does not overwrite) on second call; `TestValidateSpec`: test `skipped=True` when `enabled=False`; test violation written to violations.md; test `[OK]` output when no violations; use `tmp_path`
- [X] T013 [US3] Update `spekificity/skills/spek-plan.md` — add to `## Steps` immediately before the user review gate (before step "surface spec to user for approval"): `Run anti-sycophancy validation: check spec text against vault decisions (Rule 1: contradiction), word-count baseline (Rule 2: complexity), pattern history (Rule 3: consistency), tech names (Rule 4: stack drift); print \`[WARN]\` per violation; violations logged to \`.spek/memory/violations.md\`; execution continues regardless of violations`; add to `## Exit Criteria`: `anti-sycophancy check run; violations documented if any`

**Checkpoint**: US3 complete — `validate_spec()` functional; plan skill updated; tests pass.

---

## Phase 6: User Story 4 - RARV Reflection Cycles (Priority: P4)

**Goal**: New skill file `/spek.rarv` implementing 4-phase RARV cycle (Reason-Act-Reflect-Verify). Optional standalone skill; hinted from `/spek.conclude`.

**Independent Test**: `cat spekificity/skills/spek-rarv.md` — verify H2 structure, 6-step RARV cycle, no agent syntax. See quickstart.md Scenario 7.

- [X] T014 [US4] Create `spekificity/skills/spek-rarv.md` — heading `# /spek.rarv`; `## Prerequisites` section listing: `/spek.conclude` completed for current feature; `.spek/vault/specs/` contains original spec; `lat.md` code index current (`lat init` run after last commit); Obsidian vault accessible; `## Steps` with 6 steps: `1. REASON: Load original spec from \`.spek/vault/specs/\`; query lat.md for all implemented symbols and files changed this feature`; `2. REASON: Identify deviations — additions (code has X, spec does not), omissions (spec requires Y, code lacks it), architecture changes (different pattern used)`; `3. ACT: For each deviation, prompt user to choose: Option A (fix code to match spec), Option B (update spec and vault with new rationale), Option C (defer as tech debt)`; `4. REFLECT: If Option B chosen, update relevant \`.spek/vault/\` decision file with justification; mark deviation as \`justified\``; `5. REFLECT: If Option C chosen, append tech debt item to \`.spek/vault/patterns.md\` with context`; `6. VERIFY: Re-read updated vault decisions; confirm no new contradictions introduced; print alignment summary`; `## Output` listing deviation report, updated vault files (if B), tech debt entries (if C), alignment summary message; `## Exit Criteria`: all deviations have recorded resolution (A/B/C); vault updated where B chosen; no new vault contradictions; alignment summary printed; no agent-specific syntax (`@workspace`, `#file:`, `[[wikilink]]`); imperative mood throughout
- [X] T015 [US4] Update `spekificity/skills/spek-conclude.md` — add at end of `## Steps` (after blind review hint from T017 if already added, else as new final step): `Optional: run /spek.rarv to detect and resolve spec drift (recommended for features with architectural changes or complex deviations)`; add to `## Exit Criteria`: `spec drift check completed (optional)`

**Checkpoint**: US4 complete — `spek-rarv.md` created; conclude skill updated with RARV hint.

---

## Phase 7: User Story 5 - Blind Code Review (Priority: P5)

**Goal**: New skill file `/spek.blind-review` implementing anonymization + independent review pass. Optional pre-archival step; hinted from `/spek.conclude`.

**Independent Test**: `cat spekificity/skills/spek-blind-review.md` — verify H2 structure, anonymization-only-in-memory constraint explicitly stated, no agent syntax. See quickstart.md Scenario 8.

- [X] T016 [US5] Create `spekificity/skills/spek-blind-review.md` — heading `# /spek.blind-review`; `## Prerequisites`: implementation complete; test suite passes (run before blind review); linter installed (pylint, eslint, or equivalent); `## Steps` with 5 steps: `1. Anonymize source files in working memory only: strip comments containing vendor or agent names (\`claude\`, \`copilot\`, \`chatgpt\`, \`openai\`, \`anthropic\`); replace service class names with generic aliases (AuthService → ServiceA); NEVER modify original files — all anonymization in working memory`; `2. Run configured linter on anonymized copy; capture output; classify each finding as CRITICAL (security/error), WARNING (quality), or INFO (style)`; `3. Confirm all tests pass via \`pytest\` or configured runner; report any failures as CRITICAL`; `4. Check function complexity: flag functions exceeding 20 lines or cyclomatic complexity > 10 as WARNING`; `5. Report all findings with file:line references and remediation hints; print summary of CRITICAL / WARNING / INFO counts`; `## Output`: anonymized review report with severity-tagged findings; per-finding remediation hints; summary count line; findings file at `.spek/memory/blind-review-YYYY-MM-DD.md`; `## Exit Criteria`: all CRITICAL findings reviewed (fixed or explicitly accepted with rationale); findings report written to `.spek/memory/`; original source files confirmed unchanged; no agent-specific syntax; imperative mood
- [X] T017 [US5] Update `spekificity/skills/spek-conclude.md` — add as final item in `## Steps` (after RARV hint from T015): `Optional: run /spek.blind-review for a context-free quality pass before archiving (strips AI markers, runs linter and complexity checks independently)`; add to `## Exit Criteria`: `blind review completed (optional)`

**Checkpoint**: US5 complete — `spek-blind-review.md` created; conclude skill updated with blind review hint.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T018 [P] Run full test suite — `uv run pytest --tb=short -q`; confirm all existing 102 tests still pass; confirm new backprop and antisycophancy test suites pass; report total test count; fail this task if any regression
- [X] T019 [P] Verify skill file format compliance — confirm `spekificity/skills/spek-rarv.md` and `spekificity/skills/spek-blind-review.md` each have exactly 4 H2 sections in order (`## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`); confirm zero matches for `grep -E "@workspace|#file:|\[\[" spekificity/skills/spek-rarv.md spekificity/skills/spek-blind-review.md`; confirm steps use imperative mood (start with verb)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — start immediately
- **US1 Token Budget (Phase 3)**: Depends on T001 (config.py updated); T003–T006 fully parallel
- **US2 Backprop (Phase 4)**: Depends on Foundational only; independent of US1
- **US3 Anti-Sycophancy (Phase 5)**: Depends on Foundational only; independent of US1/US2
- **US4 RARV (Phase 6)**: Depends on US2 being settled (references Backprop context in RARV steps); T014 can start once T010 is done
- **US5 Blind Review (Phase 7)**: Independent of US2/US3/US4; depends only on Foundational
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: After T001/T002 — T003, T004, T005, T006 fully parallel; T007 sequential (same file as T010)
- **US2 (P2)**: T008 → T009 parallel → T010 sequential
- **US3 (P3)**: T011 → T012 parallel → T013 sequential
- **US4 (P4)**: After T010 — T014 then T015 sequential (same file)
- **US5 (P5)**: T016 → T017 sequential (same file as T015)

### Within Each User Story

- Python module before its test file (test file can be written in parallel if module structure known)
- Skill file updates sequential when targeting the same file (`spek-conclude.md` updated by T007, T010, T015, T017 — must be sequential)

---

## Parallel Opportunities

```bash
# Phase 2 — parallel:
T001 (config.py)
T002 (test_config.py) ← depends on T001 content being known, but different file

# Phase 3 — parallel after T001:
T003 (spek-prepare.md)
T004 (spek-plan.md)        ← different files, fully parallel
T005 (spek-implement.md)
T006 (spek-lessons.md)
# T007 (spek-conclude.md) ← sequential after T003–T006 to avoid conflict

# Phase 4 + Phase 5 — parallel with each other:
T008 (backprop.py)         ← parallel with T011 (antisycophancy.py)
T009 (test_backprop.py)    ← parallel with T012
T011 (antisycophancy.py)
T012 (test_antisycophancy.py)
```

---

## Implementation Strategy

### MVP First (US1 Only — Token Budget Config)

1. Complete Phase 2: T001 + T002
2. Complete Phase 3: T003–T007
3. **Validate**: `spek init` writes `token_budget:` block; skill files updated
4. Deploy/demo: minimal budget-awareness added

### Incremental Delivery

1. Foundation (T001/T002) → Config updated
2. US1 (T003–T007) → Token awareness in all skills
3. US2 (T008–T010) → Backprop failure capture active
4. US3 (T011–T013) → Anti-sycophancy checks in plan flow
5. US4 (T014–T015) → RARV cycle available
6. US5 (T016–T017) → Blind review available
7. Polish (T018/T019) → All green

---

## Notes

- `spek-conclude.md` updated 4 times (T007, T010, T015, T017) — execute sequentially; read current state before each edit
- `spek-plan.md` updated 2 times (T004, T013) — execute sequentially; read before T013
- No new external dependencies; stdlib only throughout
- Backprop uses `print_status` from `spekificity.utils` — import as in existing vault modules
- `antisycophancy.py` `_rule_complexity` skips gracefully when `.spek/vault/specs/` absent or empty
- Both new skill files distributed automatically by existing `skills_install/copy.py` — no code changes needed to copy logic
- Violation log (`.spek/memory/violations.md`) is append-only; never truncate or overwrite
