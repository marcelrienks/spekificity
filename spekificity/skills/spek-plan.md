---
name: spek-plan
description: 'Orchestrate SpecKit planning pipeline with user review and remediation at each step.'
---

# /spek.plan

Orchestrate SpecKit planning pipeline with user review and remediation at each step.

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded, constitution present)

## Steps

0. **Pre-check**: Validate all three SpecKit commands available — `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`. Check each command callable before proceeding. Validate lat.md indexes exist in `.spek/lat.md/` (both code and doc indexes from prepare step). If any pre-check fails, halt with error.
0.5. **Freshness Check**: Compare `.spek/lat.md/` file modification time against latest git commit timestamp. If lat.md older than most recent commit, print `[WARN] lat.md stale (last commit: X hours ago). Run 'lat init' to refresh? (Y/n)`. If user confirms Y, auto-run `lat init` and `lat init --docs` before continuing. If N, proceed with stale data (user accepts risk).
1. Run `/speckit-specify`. Query lat.md doc index for related decisions and patterns; include in session context. **Also query vault decisions**:
   - Load `.spek/vault/decisions.md` to identify architectural constraints (decisions that affect this feature's design space)
   - Note any design decisions that constrain this feature (e.g., "we use async/await, not callbacks" → informs implementation patterns)
   - Include decision context in spec output for user review
   - Present output to user for approval. If remediation needed, apply fixes and re-run.
2. Run `/speckit-plan`. Query lat.md code index for affected code areas; include in session context. **Also query vault patterns**:
   - Load `.spek/vault/patterns.md` to identify reusable patterns from prior features
   - Check if any existing patterns apply to this feature's tasks (e.g., "error handling via Result type" pattern)
   - Include pattern recommendations in plan output for author consideration
   - Present output to user for approval. If remediation needed, fix and re-run (or return to step 1 if spec was wrong).
3. Run `/speckit-tasks`. Present to user for approval. If remediation needed, fix and re-run from affected step.
4. **Approval Update**: After all three artifacts approved by user, update YAML frontmatter in each file:
   - `spec.md` frontmatter: `status: approved`, `approved_by: [name]`, `approved_date: YYYY-MM-DD`, `lat_md_version: [timestamp]`
   - `plan.md` frontmatter: same as above
   - `tasks.md` frontmatter: same as above, plus `task_id_format: numeric (1,2,3...)` documenting task numbering
5. **[Optional]** Validate lat.md architecture sections: check if lat.md sections for affected code areas exist; if present, run lat validation check; if missing, skip gracefully (not all specs require lat.md updates); if validation fails, present remediation options and re-run validation.
6. Run anti-sycophancy validation: check spec against vault decisions (Rule 1: contradiction), word-count baseline (Rule 2: complexity), pattern history (Rule 3: consistency), tech names (Rule 4: stack drift); print `[WARN]` per violation; violations logged to `.spek/memory/violations.md`; execution continues regardless of violations.
7. Track token cost for spec/plan generation phase; print `[WARN] token budget: plan phase cost high` if cost approaches configured `alert_thresholds`; non-blocking.
8. Archive `spec.md`, `plan.md`, and `tasks.md` to `.spek/vault/specs/` directory via git (commits with vault updates in spek-conclude).

## Output

- `spec.md` — Feature specification with success criteria
- `plan.md` — Architecture, tech choices, affected code areas
- `tasks.md` — Dependency-ordered tasks with IDs
- All artifacts archived to `.spek/vault/`

## Exit Criteria

- Spec approved by user
- Plan approved by user
- Task list approved by user
- Lat.md validation run (if applicable); violations documented or skipped if not required
- All artifacts archived to `.spek/vault/`
- Anti-sycophancy check run; violations documented if any
- Token cost within budget or warning issued

## See Also

- `/spek.workflow` — Complete workflow guide with tool integration details
- `/spek.map` — Dependency mapping skill (optional: call before plan to understand blockers)
- `/spek.context` — Vault schema documentation for decisions and patterns format
