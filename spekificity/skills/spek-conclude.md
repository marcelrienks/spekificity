# /spek.conclude

All post-implementation: analysis, lessons extraction, vault archive, state refresh, and commit.

## Prerequisites

- `/spek.implement` completed (all tasks done, tests passing)

## Steps

1. Run `/speckit-analyze`. Compare Success Criteria vs actual outcomes. Flag spec drift or deviations.
2. Run `/spek.lessons` as sub-step. Prompt for retrospective. Extract patterns and decisions. Write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`. (autolink enrichment runs automatically inside `/spek.lessons` — wikilinks and tags added to lesson file)
3. Run Backprop Reflex: parse test failure output from last test run; call `backprop_reflex()` with vault path; append `> ⚠ Backprop warning` blockquotes to `.spek/vault/patterns.md` for each new failure pattern; skip if no test failures in output.
4. Archive spec, plan, and tasks to `.spek/vault/`. Update `.spek/vault/patterns.md` with newly discovered patterns. Update `.spek/vault/decisions.md` with new architectural decisions.
5. Summarize total token usage for feature; compare against `token_budget.per_feature`; print `[WARN] token budget: feature exceeded budget` if over; skip if `per_feature: null`.
6. Run `lat init` to refresh the lat.md index (reflects newly committed code). Sync repo memory to `.spek/memory/`.
7. Run `git add .spek/vault/ .spek/memory/` then `git commit`.
8. Optional: run `/spek.blind-review` for a context-free quality pass before archiving (strips AI markers, runs linter and complexity checks independently).
9. Optional: run `/spek.rarv` to detect and resolve spec drift (recommended for features with architectural changes or complex deviations).

## Output

- Analysis report (spec drift documented)
- Lessons file at `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`
- Updated `.spek/vault/patterns.md` and `.spek/vault/decisions.md`
- lat.md indexes refreshed
- `.spek/memory/` updated and committed

## Exit Criteria

- Analysis complete (spec drift documented)
- Lessons extracted and committed to vault
- Failure patterns from this feature captured in vault (or none found)
- Feature artifacts archived to `.spek/vault/`
- Token usage summarized
- lat.md code and doc indexes refreshed
- Repo memory updated at `.spek/memory/`
- Spec drift check completed (optional)
- Blind review completed (optional)
