# /spek.implement

Execute approved tasks via SpecKit. Accepts optional `--steps N` to jump to task N (resume from a specific task).

## Prerequisites

- `/spek.plan` completed (spec, plan, tasks approved and archived)
- `/spek.prepare` completed (lat.md indexes current, vault context loaded)

## Steps

1. Load context from `.spek/vault/` (spec + plan + tasks).
2. Run `/speckit-implement` (optionally with `--steps N`). SpecKit executes all tasks in dependency order and owns per-task execution, code generation, and step tracking.
3. Per-task checklist:
   - Load task context from plan
   - Read Success Criteria for this task
   - Query lat.md for affected symbols and files
   - Write implementation code
   - Write or extend tests
   - Run tests locally (must pass before committing)
   - Validate against Success Criteria
   - Commit with message `[Task X] description`
   - Update plan document: mark task complete and document outcome
   - Document any lessons learned or blockers
3. Track token cost for implementation phase per task; print `[WARN] token budget: implementation phase threshold reached` if configured threshold exceeded; execution continues.

## Output

- Implemented code committed with task references
- Tests passing locally
- Plan updated with task completion status

## Exit Criteria

- All tasks completed in dependency order
- All tests passing locally
- Success Criteria validated for each task
- Code committed with task references
- Plan marked as "Implementation Complete"
