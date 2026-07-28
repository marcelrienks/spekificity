---
name: spek-implement
description: 'Execute approved tasks via SpecKit. Accepts optional --steps N to jump to task N (resume from a specific task).'
---

# /spek.implement

Execute approved tasks via SpecKit. Accepts optional `--steps N` to jump to task N (resume from a specific task).

## Prerequisites

- `/spek.plan` completed (spec, plan, tasks approved and archived)
- `/spek.prepare` completed (lat.md indexes current, vault context loaded)
- All artifact files exist: `spec.md`, `plan.md`, `tasks.md` in `.spek/vault/`

## Steps

0. **Caveman activation check**: Ensure Caveman compression is active. If not active in this session, run `/caveman full` to enable ~75% token reduction (valuable for implementation-heavy phase).

0.5. **Validation**: Check git initialized (`.git/` directory exists). If not, halt with error. Check all prerequisite files exist in `.spek/vault/` — `spec.md`, `plan.md`, `tasks.md`; fail fast with error if missing. Validate lat.md symlink: check `./lat.md` exists and points to `.spek/lat.md/` (required for lat.md symbol tracking during implementation). If symlink missing, halt with error (symlink should be created by prepare; contact user to run `/spek.prepare` if missing). If `--steps N` provided, validate N is positive integer and task N exists in tasks list; fail fast with error if invalid.
0.6. **Approval Validation**: Check YAML frontmatter in each of spec.md, plan.md, tasks.md. Verify all three have `status: approved`. If any show `status: draft`, halt with error and report which file(s) need approval. Verify `approved_by` and `approved_date` populated in all three. If missing, prompt user to update frontmatter via spek-plan and rerun.
0.7. **Token Budget Advisory**: Read `token_budget.per_feature` from `.spek/config.yaml` (if exists). Print `[INFO] Token budget: X remaining for this feature. Caveman enabled for ~75% token reduction.`; skip if not configured.
1. Check working directory clean: run `git status --porcelain`; if uncommitted changes exist, print `[WARN] uncommitted changes exist — stash or commit before continuing`. Continue only after user confirms.
2. Load context from `.spek/vault/` (spec + plan + tasks).
3. Run `/speckit-implement` (optionally with `--steps N`). SpecKit executes all tasks in dependency order and owns per-task execution, code generation, and step tracking.
4. Per-task checklist:
   - Load task context from plan
   - Read Success Criteria for this task
   - **Query lat.md for this task's affected symbols/files**:
     - List all symbols (functions, classes, methods) that this task modifies or creates
     - Check each symbol exists in lat.md code index; if not found, document as "new symbol" (implementation adds code not yet indexed)
     - Record symbol locations in `.spek/memory/task-X-symbols.md` for later drift detection
   - Write implementation code
   - Write or extend tests
   - Run tests locally (must pass before committing)
   - **Validate symbols post-implementation**:
     - After tests pass, re-query lat.md for any new symbols added (not in pre-implementation list)
     - Record "symbol additions" for later drift analysis in spek-conclude
   - Capture test output to `.spek/memory/last-test-output.log` (append each run, not overwrite)
   - Validate against Success Criteria (including: are implementation symbols consistent with lat.md definitions?)
   - Commit with message `[Task X] description`
   - Update plan document: mark task complete and document outcome
   - Document any lessons learned or blockers
5. Track token cost for implementation phase per task; print `[WARN] token budget: implementation phase threshold reached` if configured threshold exceeded. If token cost trending high, note that Caveman is already enabled for ~75% token reduction; execution continues.

## Output

- Implemented code committed with task references (`[Task X] description`)
- Tests passing locally, output captured to `.spek/memory/last-test-output.log`
- Plan updated with task completion status

## Git Commit Strategy

- **Per-task commits**: Each completed task → one commit with message `[Task X] description`
- **Rationale**: Chronological history per feature; enables `git bisect` or rollback of specific tasks
- **Feature branch commits**: Should total N commits for N tasks (plus any fix commits if tests failed then passed)
- **Do NOT squash**: Spek.conclude will commit vault changes separately, keeping feature task history distinct


## Exit Criteria

- All tasks completed in dependency order
- All tests passing locally
- Success Criteria validated for each task (including: symbol consistency with lat.md)
- Code committed with task references
- Plan marked as "Implementation Complete"
- Symbol addition/removal per-task documented in `.spek/memory/task-X-symbols.md` files
