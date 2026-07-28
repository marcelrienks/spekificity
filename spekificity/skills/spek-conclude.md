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

0. **Pre-check**: Validate git initialized (`.git/` exists). Validate both `.spek/vault/` and `.spek/memory/` exist and are writable. Validate plan document shows "Implementation Complete" or all tasks marked done. Validate `/speckit-analyze` command available. Validate lat.md symlink at `./lat.md` exists (should be created by prepare). If any pre-check fails, halt with error.

1. Run `/speckit-analyze`. Validate command exists before running; if not found, halt with error. Compare Success Criteria vs actual outcomes. Flag spec drift or deviations. **Token efficiency tip**: Analysis phase often requires reading multiple spec/code artifacts; if Caveman not active, consider `/caveman full` for analysis output compression (~75% token reduction).
2. Run `/spek.lessons` as sub-step. Prompt for retrospective. Extract patterns and decisions. Write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`. (autolink enrichment runs automatically inside `/spek.lessons` — wikilinks and tags added to lesson file; see spek-lessons skill for details).
3. Run Backprop Reflex: Validate `backprop_reflex()` function exists and callable. Parse test failure output from last test run; call `backprop_reflex()` with vault path; append `> ⚠ Backprop warning` blockquotes to `.spek/vault/patterns.md` for each new failure pattern; skip if no test failures in output or function unavailable.
4. Archive spec, plan, and tasks to `.spek/vault/`. Update `.spek/vault/patterns.md` with newly discovered patterns. Update `.spek/vault/decisions.md` with new architectural decisions.
5. Summarize total token usage for feature; compare against `token_budget.per_feature`; print `[WARN] token budget: feature exceeded budget` if over; skip if `per_feature: null`.
6. Run `lat init` to refresh the lat.md index (reflects newly committed code). Sync repo memory to `.spek/memory/`.
6.5. **lat.md Drift Report**: Aggregate symbol additions/removals from `.spek/memory/task-X-symbols.md` files (populated during implement). Generate `.spek/memory/lat-drift-report.md`:
   - **New Symbols**: List all symbols (functions, classes, methods) added during implementation but not in pre-task lat.md snapshots. For each, note: file location, symbol name, task introduced in, purpose from commit message.
   - **Removed Symbols**: List symbols deleted or refactored away. Note file location and task that removed them.
   - **Spec Alignment**: For each symbol addition, check against original `spec.md` Success Criteria. Mark as "justified" (mentioned in spec) or "unplanned" (spec didn't mention this code). Link to relevant Success Criteria line number if justified.
   - **Drift Severity**: Flag any additions marked "unplanned" that significantly increase scope or complexity (e.g., new API endpoints, new database tables). These indicate spec drift and should be reviewed.
   - **Recommendations**: If drift detected, note whether it should be addressed now (Option A in rarv: fix code) or justified/deferred (Options B/C).
   - Example structure:
   ```
   ## New Symbols (Implementation Phase)
   
   ### Added Functions
   - `helpers.format_timestamp()` [task-2, utils.py:45] — Justified (spec: "timestamps formatted per spec")
   - `auth.validate_token_expiry()` [task-3, auth.py:120] — Unplanned (spec says "validate token" but not specific implementation details)
   
   ### Severity Assessment
   - Unplanned additions: 2 (validate_token_expiry, middleware_retry_handler)
   - Scope change: +2 functions, +1 class, +0 breaking changes
   - Recommendation: Review Option A (fix) or Option B (justify new design) before merging
   ```
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
