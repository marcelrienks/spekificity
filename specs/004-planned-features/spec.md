# Feature Specification: Planned Features Implementation

**Feature Branch**: `004-planned-features`

**Created**: 2026-06-11

**Status**: Draft

**Input**: Five features documented in `wiki/decision.md` under "Planned Features (Not Yet Implemented)" — Backprop Reflex, RARV Reflection Cycles, Anti-Sycophancy Validation, Blind Code Review, Token Budget Model.

**Prerequisite**: Spec 003 fully complete (auto-tagging included). All five features build on the foundation decisions implemented in 003.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Token Budget Model (Priority: P1)

A developer wants visibility into token costs per workflow phase so they can optimize expensive phases without blocking progress. They configure soft warning thresholds in `.spek/config.yaml`; when a phase exceeds the threshold, a `[WARN]` message is printed — but execution continues.

**Why this priority**: Independent of all other planned features. Config-only change + skill file updates. Provides foundation data for future Backprop/RARV optimization decisions.

**Independent Test**: Add `token_budget` block to `.spek/config.yaml`. Run any skill. Confirm `[WARN]` appears when simulated phase cost exceeds configured threshold. Confirm execution continues (soft limit).

**Acceptance Scenarios**:

1. **Given** `token_budget.per_feature` is set and a phase exceeds its threshold, **When** any `/spek.*` skill runs, **Then** a `[WARN] token budget: phase X at Y% of threshold` message is printed; execution is not halted.

2. **Given** `token_budget` block is absent from config, **When** any skill runs, **Then** no token warnings appear and behavior is identical to current.

3. **Given** `spek init` runs on a new project, **When** `.spek/config.yaml` is written, **Then** it includes `token_budget:` block with commented placeholder fields (per `wiki/decision.md` schema).

---

### User Story 2 - Backprop Reflex (Priority: P2)

After feature implementation completes and tests are run, failed test patterns are automatically captured and appended to relevant vault decision/pattern files as warnings — preventing the same mistake in future features.

**Why this priority**: Requires foundation from spec 003. Builds on vault file structure. No dependency on other planned features except foundation. RARV (US4) depends on this.

**Independent Test**: Simulate a test failure output (pytest stderr). Run `backprop_reflex()`. Confirm a warning note is appended to the matching vault file. Confirm idempotency (same failure not appended twice).

**Acceptance Scenarios**:

1. **Given** pytest output contains `"FAILED tests/test_auth.py::test_race_condition"`, **When** `backprop_reflex()` runs, **Then** a warning note is appended to `.spek/vault/patterns.md` referencing `race_condition` and the affected test path.

2. **Given** no test failures in output, **When** `backprop_reflex()` runs, **Then** no vault files are modified and `[SKIP]` is printed.

3. **Given** same failure already appended to vault, **When** `backprop_reflex()` runs again with same output, **Then** duplicate warning is not added (idempotent via content hash check).

4. **Given** `/spek.conclude` runs, **When** Step 3 reaches backprop, **Then** `backprop_reflex()` is called automatically and its results printed.

---

### User Story 3 - Anti-Sycophancy Validation (Priority: P3)

During `/spek.plan`, the generated spec is automatically checked against vault decisions and patterns. Contradictions, significant complexity increases, and technology stack drift are flagged as `[WARN]` violations before the plan proceeds — requiring documented override or alignment.

**Why this priority**: Runs during `/spek.plan`. Independent of Backprop and RARV. Requires vault to have populated decisions/patterns (foundation from spec 003).

**Independent Test**: Create a vault with `decisions.md` containing "Use dependency injection". Generate a spec proposing "service locator". Run `validate_spec()`. Confirm violation flagged with rule name and conflicting decision.

**Acceptance Scenarios**:

1. **Given** vault `decisions.md` contains "Use dependency injection" and new spec proposes "service locator", **When** `validate_spec()` runs (Rule 1: Contradiction), **Then** violation logged to `.spek/memory/violations.md` with `[WARN] CONTRADICTION: spec contradicts vault decision`.

2. **Given** spec complexity is substantially above the average of prior specs in vault, **When** `validate_spec()` runs (Rule 2: Complexity), **Then** `[WARN] COMPLEXITY: spec N% above baseline` is printed.

3. **Given** spec introduces a technology not present in vault patterns, **When** `validate_spec()` runs (Rule 4: Stack Drift), **Then** `[WARN] STACK DRIFT: <tech> not in vault patterns` is printed.

4. **Given** no violations found, **When** `validate_spec()` runs, **Then** `[OK] anti-sycophancy checks passed` is printed; no violations file written.

5. **Given** `antisycophancy.enabled: false` in config, **When** `/spek.plan` runs, **Then** validation step is skipped with `[SKIP]`.

---

### User Story 4 - RARV Reflection Cycles (Priority: P4)

After `/spek.conclude` completes, the developer optionally triggers a RARV cycle to detect spec drift. Code vs. spec deviations are surfaced, the developer chooses to fix code, update spec, or defer to tech debt — and the vault is updated with the outcome.

**Why this priority**: Depends on Backprop Reflex (US2) for failure context. Optional step; no blocking of existing workflow. Implemented as a new skill file `/spek.rarv`.

**Independent Test**: With a completed feature where code deviates from spec (known case), run `/spek.rarv`. Confirm each deviation is reported with category (addition/omission/architecture). Confirm each outcome written to vault decision.

**Acceptance Scenarios**:

1. **Given** original spec requires "singleton auth service" and code implements "factory pattern", **When** `/spek.rarv` runs, **Then** deviation is reported as `ARCHITECTURE: singleton → factory` with user prompted to choose Option A (fix code), B (update spec), or C (defer).

2. **Given** developer chooses Option B (update spec), **When** RARV records outcome, **Then** vault decision file updated with new rationale; deviation marked `justified`.

3. **Given** no deviations found, **When** `/spek.rarv` runs, **Then** `[OK] spec and code aligned — no deviations detected` is printed.

4. **Given** `/spek.rarv` is not invoked, **When** `/spek.conclude` runs, **Then** conclude completes normally with a reminder hint: `Optional: run /spek.rarv to check spec alignment`.

---

### User Story 5 - Blind Code Review (Priority: P5)

Before archiving a feature, the developer optionally runs `/spek.blind-review` to get an independent, context-free quality pass. AI-generation markers are stripped, linters and static analysis run, and issues are reported with severity and remediation hints.

**Why this priority**: Optional, post-implementation step. No dependencies on other planned features. Builds on test infrastructure already present. Lowest implementation complexity of the five features.

**Independent Test**: Run `/spek.blind-review` on a directory with a known linting issue. Confirm issue reported at correct severity. Confirm AI-vendor comments stripped from anonymized copy. Confirm original files unchanged.

**Acceptance Scenarios**:

1. **Given** a source file with a comment `# Generated by Claude`, **When** `/spek.blind-review` anonymizes the file, **Then** the comment is removed from the review copy; original file is unchanged.

2. **Given** linting is configured and a lint error exists, **When** `/spek.blind-review` runs, **Then** the error is reported as `CRITICAL` or `WARNING` with file, line, and remediation hint.

3. **Given** all checks pass, **When** `/spek.blind-review` runs, **Then** `[OK] blind review passed — no issues found` is printed.

4. **Given** `/spek.blind-review` is not invoked, **When** `/spek.conclude` runs, **Then** conclude completes normally with a reminder hint: `Optional: run /spek.blind-review before archiving`.

---

### Edge Cases

- Vault empty (no decisions/patterns written yet) → anti-sycophancy returns `[SKIP]`; backprop writes new note, does not error.
- Test output format varies (pytest, jest, mocha) → backprop parser handles each; unknown format logs `[WARN] unrecognized test output format`.
- RARV run on feature with no spec file → error with actionable message: `spec not found at .spek/vault/specs/`; suggest re-running `/spek.plan`.
- Token budget not configured → all token-budget-related steps silently skip.
- Blind review run on non-Python project → use generic linter fallback (shellcheck, eslint); if none available, skip linting step and report `[WARN] no linter found`.

---

## Requirements *(mandatory)*

### Functional Requirements

**P1 — Token Budget Model**
- **FR-001**: `.spek/config.yaml` MUST include `token_budget:` block with `per_feature` and `alert_thresholds` placeholder fields (schema from `wiki/decision.md`)
- **FR-002**: Token budget tracking MUST be soft-limit only — warnings printed, execution never halted
- **FR-003**: Skill files that span multiple phases MUST include a `[token budget]` step referencing the configured threshold
- **FR-004**: When `token_budget` absent from config, all budget steps MUST skip silently

**P2 — Backprop Reflex**
- **FR-005**: `spekificity/vault/backprop.py` MUST expose `backprop_reflex(test_output: str, vault_path: Path) -> BackpropResult`
- **FR-006**: Parser MUST support pytest output format (`FAILED <path>::<test>` lines); extensible for other formats
- **FR-007**: Each failure pattern MUST be appended to relevant vault file as a `> ⚠ Backprop warning:` blockquote; pattern type and affected test noted
- **FR-008**: Deduplication MUST prevent same failure appended twice — use content hash of `(test_path, failure_type)` stored in `.spek/memory/backprop-seen.yaml`
- **FR-009**: `spekificity/skills/spek-conclude.md` MUST include Backprop Reflex as Step 3

**P3 — Anti-Sycophancy Validation**
- **FR-010**: `spekificity/vault/antisycophancy.py` MUST expose `validate_spec(spec_text: str, vault_path: Path, config: dict) -> ValidationResult`
- **FR-011**: Rule 1 (Contradiction): scan vault decisions for opposing directives; flag HIGH if found
- **FR-012**: Rule 2 (Complexity): compute word-count ratio of new spec vs. average of vault specs; flag if ratio > `antisycophancy.complexity_threshold` (default: 2.0)
- **FR-013**: Rule 3 (Pattern Consistency): if vault patterns show N recent uses of a pattern and spec deviates, flag LOW
- **FR-014**: Rule 4 (Stack Drift): extract technology names from spec; flag any not present in vault patterns
- **FR-015**: All violations MUST be written to `.spek/memory/violations.md` (append, not overwrite); each entry includes rule, severity, and spec line reference
- **FR-016**: `antisycophancy.enabled` config flag (default: `true`); when false, skip all checks
- **FR-017**: `spekificity/skills/spek-plan.md` MUST include Anti-Sycophancy validation as a step before user review

**P4 — RARV Reflection Cycles**
- **FR-018**: New skill file `spekificity/skills/spek-rarv.md` MUST be created with H2 structure (`## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`)
- **FR-019**: Steps MUST implement the 4-phase cycle: REASON (code vs. spec diff), ACT (user choice A/B/C), REFLECT (vault update if B), VERIFY (re-check alignment)
- **FR-020**: `/spek.rarv` MUST be callable standalone (after `/spek.conclude`) AND as optional sub-step within conclude
- **FR-021**: `spekificity/skills/spek-conclude.md` MUST add optional RARV hint at end (not a mandatory step)
- **FR-022**: `spek-rarv.md` MUST be included in the skills distribution (copied to agent skills dir by `skills_install/`)

**P5 — Blind Code Review**
- **FR-023**: New skill file `spekificity/skills/spek-blind-review.md` MUST be created with H2 structure
- **FR-024**: Anonymization step MUST strip AI vendor name comments (regex for `claude`, `copilot`, `chatgpt`, `openai`, `anthropic` in comments); operate on temp copy; never modify originals
- **FR-025**: Review checks: (1) linting — run configured linter via `run_command`, capture output; (2) test pass check — confirm `pytest` or equivalent passes; (3) complexity — flag functions with cyclomatic complexity > threshold
- **FR-026**: All findings reported with severity (`CRITICAL`, `WARNING`, `INFO`) and file:line reference
- **FR-027**: `spek-blind-review.md` MUST be included in skills distribution
- **FR-028**: `spekificity/skills/spek-conclude.md` MUST add optional blind-review hint (not a mandatory step)

### Key Entities

- **`spekificity/vault/backprop.py`**: test failure → vault warning pipeline
- **`spekificity/vault/antisycophancy.py`**: spec validation against vault
- **`spekificity/skills/spek-rarv.md`**: RARV reflection cycle skill
- **`spekificity/skills/spek-blind-review.md`**: blind code review skill
- **`.spek/memory/backprop-seen.yaml`**: deduplication store for backprop
- **`.spek/memory/violations.md`**: anti-sycophancy violation log

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `token_budget:` block present in `.spek/config.yaml` output after `spek init`
- **SC-002**: `backprop_reflex()` unit tests pass for pytest format; idempotency confirmed (no duplicate warnings on re-run)
- **SC-003**: `validate_spec()` unit tests pass for all 4 rules; violations written to `.spek/memory/violations.md`
- **SC-004**: `spek-rarv.md` skill file passes format check (correct H2 sections, no agent syntax, imperative mood)
- **SC-005**: `spek-blind-review.md` skill file passes format check
- **SC-006**: Both new skill files distributed to correct integration paths by `skills_install/copy.py` (no code changes needed — copy logic is generic)
- **SC-007**: All new unit tests pass; no changes to existing 74 tests
- **SC-008**: `antisycophancy.enabled: false` causes validation step to skip; `[SKIP]` printed
- **SC-009**: Backprop deduplication confirmed: same failure in same test output → single vault warning entry across multiple runs
- **SC-010**: Blind review anonymization leaves original source files unchanged; confirms via hash comparison before/after

---

## Assumptions

- Test infrastructure (pytest) is present in projects using Backprop Reflex; Backprop gracefully skips if test runner not found
- RARV is agent-side (skill file only); no Python code required for spec-vs-code comparison — agent performs the comparison using lat.md + spec text
- Blind review anonymization operates on an in-memory temp copy; no temp files written to disk for anonymization step
- Token budget thresholds are team-defined; no default numeric values in code per `wiki/decision.md`
- Anti-Sycophancy complexity threshold defaults to 2.0× average vault spec word count; configurable per project
- `spek-rarv.md` and `spek-blind-review.md` are copied by existing `skills_install/copy.py` logic without code changes (generic copy)
- Violation log at `.spek/memory/violations.md` is append-only; never truncated or overwritten by tools
