# /spek.rarv

Detect and resolve spec drift via four-phase Reason-Act-Reflect-Verify cycle.

## Prerequisites

- `/spek.conclude` completed for current feature
- `.spek/vault/specs/` contains original feature spec
- `lat.md` code index current (`lat init` run after last commit)
- Obsidian vault accessible at `.spek/vault/`

## Steps

1. REASON: Load original spec from `.spek/vault/specs/`; query lat.md for all implemented symbols and files changed this feature; build a side-by-side map of spec requirements vs implemented artifacts.
2. REASON: Identify deviations — additions (code has X, spec does not mention it), omissions (spec requires Y, code lacks it), architecture changes (different pattern used than specified).
3. ACT: For each deviation, prompt user to choose: Option A (fix code to match spec — revert or add code), Option B (update spec and vault with new rationale — spec was wrong or evolved), Option C (defer as tech debt — note and move on).
4. REFLECT: If Option B chosen, update relevant `.spek/vault/decisions.md` or `.spek/vault/patterns.md` with justification; mark deviation as `justified` in vault notes.
5. REFLECT: If Option C chosen, append tech debt item to `.spek/vault/patterns.md` with context: feature name, deviation description, date deferred.
6. VERIFY: Re-read updated vault decisions; confirm no new contradictions introduced by vault changes; print alignment summary listing resolved/deferred/fixed counts.

## Output

- Deviation report listing all spec vs implementation gaps
- Updated vault files where Option B chosen
- Tech debt entries in `.spek/vault/patterns.md` where Option C chosen
- Alignment summary: `N resolved (A), N justified (B), N deferred (C)`

## Exit Criteria

- All deviations have recorded resolution (A, B, or C)
- Vault updated where Option B chosen
- No new vault contradictions introduced
- Alignment summary printed to output
