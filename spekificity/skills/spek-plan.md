---
name: spek-plan
description: 'Orchestrate SpecKit planning pipeline with user review and remediation at each step.'
---

# /spek.plan

Orchestrate SpecKit planning pipeline with user review and remediation at each step.

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded, constitution present)

## Steps

1. Run `/speckit-specify`. Query lat.md doc index for related decisions and patterns; include in session context. Present output to user for approval. If remediation needed, apply fixes and re-run.
2. Run `/speckit-plan`. Query lat.md code index for affected code areas; include in session context. Present output to user for approval. If remediation needed, fix and re-run (or return to step 1 if spec was wrong).
3. Run `/speckit-tasks`. Present to user for approval. If remediation needed, fix and re-run from affected step.
4. Run anti-sycophancy validation: check spec against vault decisions (Rule 1: contradiction), word-count baseline (Rule 2: complexity), pattern history (Rule 3: consistency), tech names (Rule 4: stack drift); print `[WARN]` per violation; violations logged to `.spek/memory/violations.md`; execution continues regardless of violations.
5. Track token cost for spec/plan generation phase; print `[WARN] token budget: plan phase cost high` if cost approaches configured `alert_thresholds`; non-blocking.
6. Archive `spec.md`, `plan.md`, and `tasks.md` to `.spek/vault/` via Obsidian.

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
- Anti-sycophancy check run; violations documented if any
- Token cost within budget or warning issued
