---
name: spek-conclude
description: 'All post-implementation: analysis, lessons extraction, vault archive, state refresh, and commit.'
---

# /spek.conclude

All post-implementation: analysis, lessons extraction, vault archive, state refresh, and commit.

## Prerequisites

- `/spek.implement` completed (all tasks done, tests passing)
- Git initialized (`.git/` directory exists)
- `.spek/vault/` directory exists and writable
- `.spek/memory/` directory exists and writable

## Steps

0. **Pre-check**: Validate git initialized (`.git/` exists). Validate both `.spek/vault/` and `.spek/memory/` exist and are writable. Validate plan document shows "Implementation Complete" or all tasks marked done. Validate `/speckit-analyze` command available. If any pre-check fails, halt with error.

1. Run `/speckit-analyze`. Validate command exists before running; if not found, halt with error. Compare Success Criteria vs actual outcomes. Flag spec drift or deviations.
2. Run `/spek.lessons` as sub-step. Prompt for retrospective. Extract patterns and decisions. Write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`. (autolink enrichment runs automatically inside `/spek.lessons` — wikilinks and tags added to lesson file)
3. Run Backprop Reflex: Validate `backprop_reflex()` function exists and callable. Parse test failure output from last test run; call `backprop_reflex()` with vault path; append `> ⚠ Backprop warning` blockquotes to `.spek/vault/patterns.md` for each new failure pattern; skip if no test failures in output or function unavailable.
4. Archive spec, plan, and tasks to `.spek/vault/`. Update `.spek/vault/patterns.md` with newly discovered patterns. Update `.spek/vault/decisions.md` with new architectural decisions.
5. Summarize total token usage for feature; compare against `token_budget.per_feature`; print `[WARN] token budget: feature exceeded budget` if over; skip if `per_feature: null`.
6. Run `lat init` to refresh the lat.md index (reflects newly committed code). Sync repo memory to `.spek/memory/`.
6.5. **lat.md Drift Report**: Aggregate symbol additions/removals from `.spek/memory/task-X-symbols.md` files. Generate `.spek/memory/lat-drift-report.md`:
   - Symbols added in implementation but not in pre-task lat.md (new code)
   - Symbols removed (refactored or deleted)
   - Compare against spec: were additions/removals intentional?
   - Link to relevant Success Criteria if drift justified
   - Flag any drift that contradicts spec (escalate as potential bug)
7. Run `git add .spek/vault/ .spek/memory/` then `git commit`.

## Optional Steps

### Option A: /spek.blind-review (Context-Free Quality Pass)

**Prerequisites**: Implementation complete, all tests passing, linter installed and configured
**When**: Use for code quality validation before final archival. Run independently — do not combine with Option B in same conclude call.
**Steps**: Invoke `/spek.blind-review` after step 7. Strips AI markers, runs linter and complexity checks independently. Address all CRITICAL findings before proceeding to vault archival.

### Option B: /spek.rarv (Spec Drift Detection)

**Prerequisites**: Original feature spec exists in `.spek/vault/specs/`, lat.md current, vault accessible
**When**: Use for features with architectural changes or complex deviations from plan. Run independently — do not combine with Option A in same conclude call.
**Steps**: Invoke `/spek.rarv` after step 7. Detects and resolves spec vs implementation gaps. User chooses fix (A), justify (B), or defer (C) for each deviation. Update vault accordingly.

## Output

- Analysis report (spec drift documented)
- Lessons file at `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md` with autolinked wikilinks
- Updated `.spek/vault/patterns.md` and `.spek/vault/decisions.md` (if new patterns/decisions found)
- lat.md drift report at `.spek/memory/lat-drift-report.md` (symbols added/removed during feature)
- lat.md indexes refreshed (reflect newly committed code)
- `.spek/memory/` updated and committed (including per-task symbol files and drift report)

## Exit Criteria

- Analysis complete (spec drift documented)
- Lessons extracted and committed to vault
- Failure patterns from this feature captured in vault (or none found)
- Feature artifacts archived to `.spek/vault/`
- Token usage summarized
- lat.md code and doc indexes refreshed
- Repo memory updated at `.spek/memory/`
- (Optional A) Blind review completed if invoked; all CRITICAL findings addressed
- (Optional B) Spec drift resolved if invoked; deviations have recorded resolutions
