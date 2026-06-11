# /spek.conclude

All post-implementation: analysis, lessons extraction, vault archive, state refresh, and commit.

## Workflow

1. **Analysis**: Run `/speckit-analyze`. Compare Success Criteria vs actual outcomes. Flag spec drift or deviations.
2. **Lessons**: Run `/spek.lessons` as sub-step. Prompt for retrospective. Extract patterns and decisions. Write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`.
3. **Vault Archive**:
   - Archive spec + plan + tasks to `.spek/vault/`.
   - Update `.spek/vault/patterns.md` with newly discovered patterns.
   - Update `.spek/vault/decisions.md` with new architectural decisions.
4. **State Refresh**:
   - Run `lat init` to refresh the lat.md index (reflects newly committed code).
   - Sync repo memory to `.spek/memory/`.
5. **Commit**: `git add .spek/vault/ .spek/memory/` then `git commit`.

## Exit Criteria

- Analysis complete (spec drift documented)
- Lessons extracted and committed to vault
- Feature artifacts archived to `.spek/vault/`
- lat.md code and doc indexes refreshed
- Repo memory updated at `.spek/memory/`
