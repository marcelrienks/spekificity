---
name: spek-rarv
description: 'Detect and resolve spec drift via four-phase Reason-Act-Reflect-Verify cycle.'
---

# /spek.rarv

Detect and resolve spec drift via four-phase Reason-Act-Reflect-Verify cycle.

## Prerequisites

- `/spek.conclude` completed for current feature
- `.spek/vault/specs/` contains original feature spec
- `lat.md` code index current (`lat init` run after last commit)
- Obsidian vault accessible at `.spek/vault/`

## Steps

0. **Pre-check**: Validate original spec file exists in `.spek/vault/specs/` (check for `spec.md` or matching feature name file). If missing, halt with error — spec required for comparison. Check `.spek/lat.md/` indexes exist and are recent (run timestamp check or compare against last git commit). If lat.md stale, run `lat init` to refresh before continuing.
1. **Vault Contradiction Check**: Before proceeding, load `.spek/vault/decisions.md` and `.spek/vault/patterns.md`. Run internal contradiction validator; report any contradictions found (decisions that conflict with each other or patterns). If contradictions exist, halt and prompt user to resolve via `/speckit-constitution` or manual vault edit before continuing.
2. REASON: Load original spec from `.spek/vault/specs/`; query lat.md for all implemented symbols and files changed this feature; build a side-by-side map of spec requirements vs implemented artifacts.
3. REASON: Identify deviations — additions (code has X, spec does not mention it), omissions (spec requires Y, code lacks it), architecture changes (different pattern used than specified).
4. ACT: For each deviation, prompt user to choose: Option A (fix code to match spec — revert or add code), Option B (update spec and vault with new rationale — spec was wrong or evolved), Option C (defer as tech debt — note and move on).
5. REFLECT: If Option B chosen, update relevant `.spek/vault/decisions.md` or `.spek/vault/patterns.md` with justification; mark deviation as `justified` in vault notes.
6. REFLECT: If Option C chosen, append tech debt item to `.spek/vault/patterns.md` with context: feature name, deviation description, date deferred.
7. VERIFY: Re-read updated vault decisions; confirm no new contradictions introduced by vault changes; print alignment summary listing resolved/deferred/fixed counts.

## Output

- Deviation report listing all spec vs implementation gaps
- Updated vault files where Option B chosen
- Tech debt entries in `.spek/vault/patterns.md` where Option C chosen
- Alignment summary: `N resolved (A), N justified (B), N deferred (C)`

## Post-rarv Workflow

If Option A chosen (fix code):
- Code is already committed from `/spek.implement` phase
- User must return to feature branch and make fixes locally
- Run tests locally
- Commit with message: `[Fix] Task X — resolved spec drift issue`
- Re-run `/spek.rarv` step 6 (VERIFY) to confirm no new contradictions
- Then proceed to post-conclusion workflow (PR, merge, release)

If Option B chosen (justify):
- Update vault files (`.spek/vault/decisions.md` or `.spek/vault/patterns.md`) with new rationale explaining deviation
  - Add new `## Decision:` entry if deviation represents an architectural choice
  - Update `## Pattern:` entry if reusing existing pattern but with different intent
- Mark deviation as `justified` in vault entry (add `Status: justified | date | feature-ref`)
- No code changes needed
- Commit vault updates: `git add .spek/vault/ && git commit -m "[Justify] Feature X deviation: [reason]"` (do not wait for spek-conclude)
- Proceed to post-conclusion workflow (PR, merge, release)

If Option C chosen (defer):
- Append tech debt item to `.spek/vault/patterns.md` with context:
  ```
  ## Tech Debt: [Feature Name] — [Brief Description]
  Feature: [feature name]
  Deviation: [description of what diverged from spec]
  Date Deferred: YYYY-MM-DD
  Justification: [why deferred now vs implemented]
  Suggested Resolution: [how to address in future feature]
  Related Issue: [GitHub issue link if created]
  ```
- Create GitHub issue for future work (if not already created)
- Link issue in tech debt entry
- Commit tech debt entry: `git add .spek/vault/ && git commit -m "[TechDebt] Feature X: [reason] (deferred to GitHub issue #N)"`
- Proceed to post-conclusion workflow (PR, merge, release)
- Next feature team can reference tech debt entry when planning related work


## Exit Criteria

- All deviations have recorded resolution (A, B, or C)
- Vault updated where Option B chosen
- No new vault contradictions introduced
- Alignment summary printed to output
