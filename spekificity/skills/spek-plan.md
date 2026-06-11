# /spek.plan

Orchestrate SpecKit planning pipeline with user review and remediation at each step.

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded, constitution present)

## Steps

1. Run `/speckit-specify`. Query lat.md doc index for related decisions and patterns; include in session context. Present output to user for approval. If remediation needed, apply fixes and re-run.
2. Run `/speckit-plan`. Query lat.md code index for affected code areas; include in session context. Present output to user for approval. If remediation needed, fix and re-run (or return to step 1 if spec was wrong).
3. Run `/speckit-tasks`. Present to user for approval. If remediation needed, fix and re-run from affected step.
4. Archive `spec.md`, `plan.md`, and `tasks.md` to `.spek/vault/` via Obsidian.

## Output

- `spec.md` — Feature specification with success criteria
- `plan.md` — Architecture, tech choices, affected code areas
- `tasks.md` — Dependency-ordered tasks with IDs
- All artifacts archived to `.spek/vault/`

## Exit Criteria

- Spec approved by user
- Plan approved by user
- Task list approved by user
- All artifacts archived to `.spek/vault/` via Obsidian
