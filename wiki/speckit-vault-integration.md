# SpecKit & Vault Integration — Architecture Clarification

## Overview

This document clarifies how SpecKit artifacts (spec.md, plan.md, tasks.md) are created, stored, and accessed throughout the Spekificity workflow.

## Key Discovery: Vault-Native Artifact Storage

**Artifacts are stored directly in `.spek/vault/` (or `.spek/vault/specs/NNNN-feature-name.md` per conventions).** They are NOT created in the project root and then "archived" to vault. This distinction is critical for understanding why the approval gate works.

### Artifact Storage Locations

| Artifact | Location | Naming Convention |
|----------|----------|-------------------|
| Specification | `.spek/vault/specs/` | `NNNN-feature-name.md` (4-digit prefix, kebab-case) |
| Plan | `.spek/vault/specs/` | `NNNN-feature-name-plan.md` (same prefix as spec) |
| Tasks | `.spek/vault/specs/` | `NNNN-feature-name-tasks.md` (same prefix as spec) |

**Convention Detail**: Spec numbering is global across the project, starting at `0001`, and incremented sequentially regardless of feature name or creation date. Examples:
- First feature: `0001-user-auth-api.md`, `0001-user-auth-api-plan.md`, `0001-user-auth-api-tasks.md`
- Second feature: `0002-payment-processing.md`, `0002-payment-processing-plan.md`, `0002-payment-processing-tasks.md`

See [conventions.md](conventions.md) for full naming details.

## How SpecKit Is Configured

During `spek init`, the following configuration is established:

### 1. Spekificity Configuration (`.spek/config.yaml`)

Created by `spekificity/speckit/config.py`, this file sets vault paths for Spekificity tooling:

```yaml
tools:
  vault:
    enabled: true
    path: .spek/vault/
    obsidian_vault_name: vault
```

This **does not** configure SpecKit; it configures Spekificity's understanding of where the vault lives.

### 2. SpecKit Configuration (`.specify/` directory)

When `specify init --here --integration [agent]` runs, SpecKit initializes a `.specify/` directory in the project with its own configuration. This directory contains:

- `.specify/memory/constitution.md` — Project principles (created interactively via `/speckit-constitution` or populated by Spekificity)
- `.specify/config.json` or `.specify/config.yaml` — SpecKit's internal configuration (managed by SpecKit, not Spekificity)
- `.specify/memory/` — SpecKit's internal knowledge base

**Status**: How SpecKit is configured to write spec/plan/tasks to `.spek/vault/` is **not currently documented in Spekificity code**. This should be verified via:
1. SpecKit's own documentation or source code
2. The `.specify/config.*` file after init completes
3. Running a test init in a temporary directory and observing where artifacts are created

## Artifact Lifecycle

### Phase 1: `/spek.plan` — Generation & Approval

1. `/speckit-specify` runs → generates spec
2. User reviews and approves spec
3. `/speckit-plan` runs → generates plan
4. User reviews and approves plan
5. `/speckit-tasks` runs → generates tasks
6. User reviews and approves tasks
7. **Frontmatter Added**: YAML frontmatter is added to each file:
   ```yaml
   ---
   status: approved
   approved_by: [user name]
   approved_date: 2026-07-30
   lat_md_version: [timestamp of lat.md index at approval time]
   ---
   ```
8. **Files Committed**: Artifacts are committed to git (this happens during `/spek.conclude` if plan was run in an earlier session, or can happen separately if needed)

**Location at End of Phase 1**: Artifacts exist in `.spek/vault/specs/NNNN-*.md`

### Phase 2: `/spek.implement` — Execution

1. Validation checks that spec.md, plan.md, tasks.md exist in `.spek/vault/`
2. Approval frontmatter is verified (all three must have `status: approved`)
3. `/speckit-implement` runs against the approved artifacts
4. Tasks are executed in dependency order
5. Code changes are committed with task references (`[Task N] description`)

**Key Constraint**: These artifacts do NOT change during implement. If spec changes are needed, you must:
1. Stop implementation
2. Run `/spek.plan` again (with current context)
3. Get new approval
4. Commit updated artifacts with new approval frontmatter
5. Resume `/spek.implement` with updated context

### Phase 3: `/spek.conclude` — Archival & Persistence

1. `/speckit-analyze` compares implementation against spec
2. Lessons are extracted and written to `.spek/vault/lessons/YYYY-MM-DD-*.md`
3. New patterns and decisions discovered during impl are added to vault
4. **Git Commit**: All vault changes (spec, plan, tasks, lessons, patterns, decisions) are committed:
   ```bash
   git add .spek/vault/ .spek/memory/
   git commit -m "Conclude feature: NNNN-feature-name"
   ```

**Outcome**: Vault now contains the complete feature record — spec, plan, tasks, lessons, and any new patterns/decisions discovered.

## Why This Design

| Aspect | Benefit |
|--------|---------|
| **Vault-Native Artifacts** | Single source of truth; no risk of reading stale root files |
| **Approval Frontmatter** | Gate between planning and execution; prevents mid-implementation spec drift |
| **Immutable During Implement** | Implementation runs against stable, approved spec; predictable outcomes |
| **Git-Persisted Vault** | Complete feature history preserved; enables bisect, rollback, and retrospective analysis |
| **Per-Feature Numbering** | Chronological ordering; easy to reference features across sessions |

## Configuration Resolution ✅

**Resolved during Spekificity initialization.**

During `spek init`, after running `specify init --here --integration [agent]`, Spekificity automatically configures SpecKit's output path via `_configure_speckit_output_path()` in `spekificity/speckit/init.py`:

1. Creates `.specify/config.json` with `artifact_output_dir: .spek/vault/specs`
2. Ensures `.spek/vault/specs/` directory structure exists
3. Is idempotent — only sets config if not already present
4. Skips silently if config cannot be written (non-blocking)

**Result**: All SpecKit artifacts (spec.md, plan.md, tasks.md) are automatically written to `.spek/vault/specs/NNNN-feature-name.md` — no manual intervention required.

## Related Files

- [conventions.md](conventions.md) — Artifact naming and directory structure
- [workflow.md](workflow.md) — Four-stage feature workflow overview
- [spekificity/speckit/](../spekificity/speckit/) — Python code for SpecKit initialization
