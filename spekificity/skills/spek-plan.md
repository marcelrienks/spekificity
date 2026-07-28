---
name: spek-plan
description: 'Orchestrate SpecKit planning pipeline with user review and remediation at each step.'
---

# /spek.plan

Orchestrate SpecKit planning pipeline with user review and remediation at each step.

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded, constitution present)

## Steps

0. **Pre-check**: Validate all three SpecKit commands available — `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`. Check each command callable before proceeding. Validate lat.md indexes exist in `.spek/lat.md/` (both code and doc indexes from prepare step). Validate lat.md symlink at `./lat.md` points to `.spek/lat.md/` (required for `lat mcp` server). If any pre-check fails, halt with error.
0.5. **Freshness Check**: Compare `.spek/lat.md/` file modification time against latest git commit timestamp. If lat.md older than most recent commit, print `[WARN] lat.md stale (last commit: X hours ago). Run 'lat init' to refresh? (Y/n)`. If user confirms Y, auto-run `lat init` and `lat init --docs` before continuing. If N, proceed with stale data (user accepts risk).
0.6. **Vault Integrity Check**: Load `.spek/vault/decisions.md` and `.spek/vault/patterns.md`. Run internal contradiction validator (pseudocode: `for each decision, check if any other decision directly conflicts`). If contradictions exist, print `[WARN] vault contradictions detected: [list]`. Continue with warning but mark violations in session context for remediation later (user can fix via `/speckit-constitution` if needed).
1. Run `/speckit-specify`. Query lat.md **doc index** for related decisions and patterns using keywords from the feature description; include in session context. **Also query vault decisions systematically**:
   - Load `.spek/vault/decisions.md` and search for `## Decision:` entries matching feature keywords
   - Extract `Impact:` and `Alternatives:` sections — identify architectural constraints (decisions that affect this feature's design space)
   - Extract `Tags:` and `Related Decisions:` — flag any decisions that narrow design choices for this feature
   - Include decision context in spec output for user review
   - Present spec output to user for approval. If remediation needed, apply fixes and re-run.
2. Run `/speckit-plan`. Query lat.md **code index** for affected code areas (symbols, call graphs, definitions) and include in session context. Query lat.md **doc index** again for architectural patterns and prior design solutions. **Also query vault patterns systematically**:
   - Load `.spek/vault/patterns.md` and search for `## Pattern:` entries using feature keywords and tags
   - Extract `Example Files:` — reference prior implementations
   - Extract `Trade-offs:` and `Anti-patterns:` — learn from what didn't work before
   - Check if any existing patterns apply to this feature's tasks (e.g., "error handling via Result type" pattern)
   - Include pattern recommendations and tradeoffs in plan output for author consideration
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

- `spec.md` — Feature specification with success criteria, linked to vault decisions
- `plan.md` — Architecture, tech choices, affected code areas from lat.md code index, pattern recommendations from vault
- `tasks.md` — Dependency-ordered tasks with IDs, constrained by vault decisions
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
