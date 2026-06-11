# /spek.conclude

All post-implementation: analysis, lessons extraction, vault archive, state refresh, and commit.

## Prerequisites

- `/spek.implement` completed (all tasks done, tests passing)

## Steps

1. Run `/speckit-analyze`. Compare Success Criteria vs actual outcomes. Flag spec drift or deviations.
2. Run `/spek.lessons` as sub-step. Prompt for retrospective. Extract patterns and decisions. Write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`. (autolink enrichment runs automatically inside `/spek.lessons` — wikilinks and tags added to lesson file)
3. Archive spec, plan, and tasks to `.spek/vault/`. Update `.spek/vault/patterns.md` with newly discovered patterns. Update `.spek/vault/decisions.md` with new architectural decisions.
4. Run `lat init` to refresh the lat.md index (reflects newly committed code). Sync repo memory to `.spek/memory/`.
5. Run `git add .spek/vault/ .spek/memory/` then `git commit`.

## Output

- Analysis report (spec drift documented)
- Lessons file at `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`
- Updated `.spek/vault/patterns.md` and `.spek/vault/decisions.md`
- lat.md indexes refreshed
- `.spek/memory/` updated and committed

## Exit Criteria

- Analysis complete (spec drift documented)
- Lessons extracted and committed to vault
- Feature artifacts archived to `.spek/vault/`
- lat.md code and doc indexes refreshed
- Repo memory updated at `.spek/memory/`
