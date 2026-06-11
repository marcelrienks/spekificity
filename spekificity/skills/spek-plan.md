# /spek.plan

Orchestrate SpecKit planning pipeline with user review and remediation at each step.

## Workflow

1. **Specify**: Run `/speckit-specify`. Before invoking, query lat.md doc index for related decisions and patterns; include in session context. Present output to user for approval. If remediation needed, apply fixes and re-run step 1.
2. **Plan**: Run `/speckit-plan`. Query lat.md code index for affected code areas; include in session context. Present output to user for approval. If remediation needed, fix and re-run (or return to step 1 if spec was wrong).
3. **Tasks**: Run `/speckit-tasks`. Present to user for approval. If remediation needed, fix and re-run from affected step.

After all three steps approved: archive `spec.md`, `plan.md`, and `tasks.md` to `.spek/vault/` via Obsidian.

## Output Artifacts

- `spec.md` — Feature specification with success criteria (SpecKit manages path; archived to `.spek/vault/`)
- `plan.md` — Architecture, tech choices, affected code areas (archived to `.spek/vault/`)
- `tasks.md` — Dependency-ordered tasks with IDs (archived to `.spek/vault/`)

## Exit Criteria

- Spec approved by user
- Plan approved by user
- Task list approved by user
- All artifacts archived to `.spek/vault/` via Obsidian
