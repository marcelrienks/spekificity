# /spek.implement

Execute approved tasks via SpecKit. Accepts optional `--steps N` to jump to task N (resume from a specific task).

## Workflow

1. Load context from `.spek/vault/` (spec + plan + tasks).
2. Run `/speckit-implement` (optionally with `--steps N`).
   - SpecKit executes all tasks in dependency order.
   - SpecKit owns per-task execution, code generation, and step tracking.

## Per-Task Checklist

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

## Exit Criteria

- All tasks completed in dependency order
- All tests passing locally
- Success Criteria validated for each task
- Code committed with task references
- Plan marked as "Implementation Complete"
