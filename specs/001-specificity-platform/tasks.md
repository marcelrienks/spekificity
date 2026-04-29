# Tasks: Specificity Platform — Core Project Foundation

**Feature Branch**: `001-specificity-platform`  
**Input**: Design documents from `specs/001-specificity-platform/`  
**Date**: 2026-04-29

**Prerequisites used**: plan.md ✓ | spec.md ✓ | research.md ✓ | data-model.md ✓ | contracts/skill-contracts.md ✓ | quickstart.md ✓

---

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Parallelisable — different files, no dependency on in-progress tasks
- **[US#]**: User story this task belongs to
- No tests — not requested in spec; this is a documentation project with manual validation

---

## Phase 1: Setup (Project Scaffolding)

**Purpose**: Create the directory structure required by all subsequent phases.

- [ ] T001 Create top-level directory structure: `skills/`, `workflows/`, `setup-guides/`, `vault/`
- [ ] T002 Create vault subdirectory scaffold: `vault/graph/nodes/`, `vault/lessons/`, `vault/context/`
- [ ] T003 [P] Create `vault/context/decisions.md` with schema header placeholder
- [ ] T004 [P] Create `vault/context/patterns.md` with schema header placeholder

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Root-level project files that all user stories reference.

**⚠️ CRITICAL**: Setup guides and workflows cannot be finalized until these exist.

- [ ] T005 Create root `README.md` with project overview, prerequisite list, quickstart link, and component update table
- [ ] T006 Create `.gitignore` entries for `vault/graph/` (opt-out on large repos), `.obsidian/workspace.json`, and standard OS/editor files

**Checkpoint**: Root scaffolding complete — user story work can begin.

---

## Phase 3: User Story 1 — First-Time Project Initialisation (Priority: P1) 🎯 MVP

**Goal**: A developer can follow the init workflow to install all tools and have all Specificity custom skills active in under 30 minutes on a fresh macOS or Linux machine.

**Independent Test**: Follow `workflows/init-workflow.md` step by step on a fresh machine; verify `graphify --version` and `specify --version` succeed, all skill files exist in `.github/agents/` and `.claude/commands/`, and `/speckit.specify` can be invoked without errors.

- [ ] T007 [P] [US1] Create `setup-guides/graphify-setup.md` — overview, install via `uv tool install graphifyy`, verify command, `--obsidian` flag explanation, troubleshooting
- [ ] T008 [P] [US1] Create `setup-guides/speckit-setup.md` — overview, install via `uv tool install specify-cli`, verify command, `specify init .` workflow, version compatibility table
- [ ] T009 [P] [US1] Create `setup-guides/obsidian-setup.md` — overview (optional app), vault-as-filesystem explanation, app install steps, vault open instructions, note it is NOT required for AI workflow
- [ ] T010 [US1] Create `workflows/init-workflow.md` — ordered 8-step init workflow: prerequisite check → install Graphify → install SpecKit → `specify init` → install Specificity skills → run `/map-codebase` → verify → next steps; includes detect-before-install idempotency checks at each step

**Checkpoint**: US1 complete — developer can initialise a new project from zero.

---

## Phase 4: User Story 2 — AI-Guided Codebase & Documentation Mapping (Priority: P2)

**Goal**: A developer can invoke `/map-codebase` to build and refresh a Graphify → Obsidian graph of the project, enabling AI agents to answer cross-cutting questions without scanning all source files.

**Independent Test**: Invoke `/map-codebase` per `skills/map-codebase/SKILL.md` on a project with ≥20 files; verify `vault/graph/index.md` exists, contains node entries, and an AI agent can answer a cross-cutting question citing vault nodes.

- [ ] T011 [US2] Create `skills/map-codebase/SKILL.md` — full skill file: description, trigger (`/map-codebase`), prerequisites (graphify installed, project root), inputs (`--full` flag, optional `CLAUDE_API_KEY`), steps (run `graphify . --obsidian --output vault/graph/`, verify outputs, report diff), outputs table, error handling (missing graphify → print install instructions, write failure → halt without partial write), notes
- [ ] T012 [P] [US2] Create `vault/graph/index.md` as a human-readable schema template — header with last-updated metadata, node count placeholder, section structure for god nodes, full node list table; this is the template the `/map-codebase` skill overwrites at runtime
- [ ] T013 [US2] Create `workflows/map-refresh.md` — when to refresh (after file adds/deletes, before `/speckit.plan`, start of new feature), how to refresh (invoke `/map-codebase`), incremental vs full flag guidance, vault size guidance (gitignore `vault/graph/` if >500 nodes)

**Checkpoint**: US2 complete — AI can map any project and use vault for context.

---

## Phase 5: User Story 3 — Supercharged SpecKit Feature Lifecycle (Priority: P2)

**Goal**: A developer can run the enriched SpecKit lifecycle where each step (`/speckit.specify`, `/speckit.plan`, `/speckit.implement`) is decorated with graph-aware context, and lessons learnt are persisted to the vault at feature completion.

**Independent Test**: In a mapped project, invoke `/context-load` then `/speckit-enrich-specify`; verify the spec output includes cross-references to existing graph nodes. After a completed feature, invoke `/lessons-learnt`; verify `vault/lessons/<date>-<slug>.md` exists with all schema sections populated.

- [ ] T014 [P] [US3] Create `skills/context-load/SKILL.md` — description, trigger (`/context-load`), prerequisite (vault exists), inputs (scope: `full`/`graph-only`/`lessons-only`, optional feature filter), steps (read `vault/graph/index.md`, read `vault/context/decisions.md`, read `vault/context/patterns.md`, load relevant lessons entry, summarise in ≤5 bullets with Caveman if active, confirm "Context loaded"), outputs (AI working memory), postconditions
- [ ] T015 [P] [US3] Create `skills/lessons-learnt/SKILL.md` — description, trigger (`/lessons-learnt`), prerequisites (feature complete, `vault/lessons/` exists), inputs (branch auto-detected, date auto-detected, AI model name), steps (detect branch, AI reflection on what worked / harder than expected / decisions / patterns, write `vault/lessons/<date>-<slug>.md` per data-model schema, append to `vault/context/patterns.md`, append to `vault/context/decisions.md`, report path), outputs table, error handling
- [ ] T016 [P] [US3] Create `skills/speckit-enrich/specify-enrich.md` — decorator for `/speckit.specify`: run `/context-load` if not already run, identify related graph nodes for feature description, annotate description with "Related existing components: [list]", invoke `/speckit.specify` with enriched input, post-write: note impacted nodes in spec Assumptions
- [ ] T017 [P] [US3] Create `skills/speckit-enrich/plan-enrich.md` — decorator for `/speckit.plan`: run `/context-load graph-only`, identify graph nodes referenced in `spec.md`, annotate plan's Technical Context with "Impacted graph nodes: [list]", invoke `/speckit.plan`, post-write: verify impacted nodes are present in plan's Project Structure
- [ ] T018 [P] [US3] Create `skills/speckit-enrich/implement-enrich.md` — decorator for `/speckit.implement`: run `/context-load` at session start, check graph for related nodes before each task, invoke `/speckit.implement`, post-complete: auto-invoke `/lessons-learnt` then `/map-codebase` incremental
- [ ] T019 [US3] Create `workflows/feature-lifecycle.md` — enriched SpecKit lifecycle: 7-step sequence (`/context-load` → `/speckit-enrich-specify` → `/speckit-enrich-plan` → `/speckit.tasks` → `/speckit-enrich-implement` → `/lessons-learnt` → `/map-codebase` incremental), decision points (if vault not mapped: run `/map-codebase` first), expected state at each checkpoint, recovery instructions for partial failures

**Checkpoint**: US3 complete — full enriched feature lifecycle is operational.

---

## Phase 6: User Story 4 — Token-Efficient AI Interactions via Caveman (Priority: P3)

**Goal**: Caveman mode is explicitly integrated at every workflow step, with clear guidance on when to invoke it and which intensity level to use.

**Independent Test**: Activate `/caveman lite` then run through `workflows/feature-lifecycle.md`; verify AI responses are compressed throughout without omitting technical content needed for the next step.

- [ ] T020 [US4] Update `workflows/feature-lifecycle.md` to add explicit Caveman invocation checkpoints — add a "Token Efficiency" section: recommend `/caveman lite` at session start before spec/plan steps (structured output), `/caveman` (full) for implementation steps, `/caveman ultra` for research/exploration; add a note to `workflows/init-workflow.md` and `workflows/map-refresh.md` recommending Caveman activation

**Checkpoint**: US4 complete — token efficiency guidance is embedded throughout all workflow documents.

---

## Phase 7: User Story 5 — Independent Component Updates (Priority: P3)

**Goal**: Each third-party component (Graphify, Obsidian, SpecKit, Specificity custom layer) can be updated independently without re-initialising the stack.

**Independent Test**: Follow the Graphify update section of `workflows/component-update.md`; verify no other Specificity files require changes.

- [ ] T021 [US5] Create `workflows/component-update.md` — four-section update guide: (1) SpecKit update (`uv tool upgrade specify-cli`, no Specificity changes unless command interface changed, how to detect breaking changes), (2) Graphify update (`uv tool upgrade graphifyy`, update only `skills/map-codebase/SKILL.md` if CLI args change), (3) Obsidian update (download new app, no Specificity changes, vault format is stable markdown), (4) Specificity custom layer update (`git pull` from Specificity repo, re-copy skills to `.github/agents/` and `.claude/commands/`); include version compatibility table per component; add token-efficiency note at top recommending `/caveman lite` before reading update docs (Constitution Principle VI)

**Checkpoint**: US5 complete — maintenance workflow is documented.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Agent-specific skill distribution, context file updates, and final accuracy verification.

- [ ] T022 [P] Distribute all skills to `.github/agents/` for GitHub Copilot — copy: `skills/map-codebase/SKILL.md` → `.github/agents/map-codebase.agent.md`, `skills/lessons-learnt/SKILL.md` → `.github/agents/lessons-learnt.agent.md`, `skills/context-load/SKILL.md` → `.github/agents/context-load.agent.md`, `skills/speckit-enrich/specify-enrich.md` → `.github/agents/speckit-enrich-specify.agent.md`, `skills/speckit-enrich/plan-enrich.md` → `.github/agents/speckit-enrich-plan.agent.md`, `skills/speckit-enrich/implement-enrich.md` → `.github/agents/speckit-enrich-implement.agent.md`
- [ ] T023 [P] Distribute all skills to `.claude/commands/` for Claude Code — create `.claude/commands/` directory and copy each skill file with `.md` extension (matching filenames used in T022)
- [ ] T024 Update `.github/copilot-instructions.md` to include the Specificity skill index and session-start guidance: "At session start, run `/context-load` to load vault context before any work"
- [ ] T025 Cross-verify `specs/001-specificity-platform/quickstart.md` against all created skill and workflow files — update any file paths, command names, or step numbers that have diverged from final implementations
- [ ] T026 [P] Create `docs/VALIDATION.md` — measurement methodology for SC-002 (token reduction ≥40%: procedure to record token counts for 5 representative cross-cutting queries on a mapped vs unmapped project, log results, compute reduction %) and SC-003 (Caveman verbosity reduction ≥60%: procedure to record character counts of 3 representative AI responses with and without Caveman active, compute reduction %); include example log table for each metric
- [ ] T027 [P] Create root `AGENTS.md` — Claude Code skill discovery index: list all 6 Specificity skills with their command name, trigger, file path in `.claude/commands/`, and one-line description; add session-start guidance ("Run `/context-load` before any feature work"); ensures FR-011 and FR-012 compliance for Claude Code users

---

## Dependencies

```
T001 → T002 → T003, T004
T001 → T005, T006

T007, T008, T009 (parallel) → T010   [US1]

T010 → T011 → T012, T013             [US2]

T013 → T014, T015, T016, T017, T018 (parallel) → T019  [US3]

T019 → T020                           [US4]

T020 → T021                           [US5]

T021 → T022, T023 (parallel) → T024 → T025
T024 → T026, T027 (parallel)
```

---

## Parallel Execution Examples

### US1 — Setup guides (after T001):
```
T007 (graphify-setup.md)  ─┐
T008 (speckit-setup.md)   ─┤── all complete → T010 (init-workflow.md)
T009 (obsidian-setup.md)  ─┘
```

### US3 — Skill files (after T013):
```
T014 (context-load)          ─┐
T015 (lessons-learnt)        ─┤
T016 (specify-enrich)        ─┤── all complete → T019 (feature-lifecycle.md)
T017 (plan-enrich)           ─┤
T018 (implement-enrich)      ─┘
```

### Polish — Agent distribution (after T021):
```
T022 (.github/agents/)  ─┐
T023 (.claude/commands/) ─┘── both complete → T024 → T025
```

---

## Implementation Strategy

**MVP Scope (US1 only — T001–T010)**: Delivers a working initialisation workflow. A developer can get all tools installed and Specificity scaffolded without any mapping or enrichment features.

**Increment 2 (add US2 — T011–T013)**: Adds codebase mapping. AI sessions can now load graph context instead of scanning files.

**Increment 3 (add US3 — T014–T019)**: Full enriched SpecKit lifecycle. This is the primary daily-use value.

**Increment 4 (add US4+US5+Polish — T020–T027)**: Caveman integration guidance, component update procedures, agent distribution, and validation methodology — hardening and polish.

---

## Summary

| Phase | User Story | Tasks | Parallel Opportunities |
|-------|-----------|-------|----------------------|
| Setup | — | T001–T004 (4) | T003, T004 |
| Foundational | — | T005–T006 (2) | — |
| Phase 3 | US1 (P1) | T007–T010 (4) | T007, T008, T009 |
| Phase 4 | US2 (P2) | T011–T013 (3) | T012 |
| Phase 5 | US3 (P2) | T014–T019 (6) | T014, T015, T016, T017, T018 |
| Phase 6 | US4 (P3) | T020 (1) | — |
| Phase 7 | US5 (P3) | T021 (1) | — |
| Polish | — | T022–T027 (6) | T022, T023, T026, T027 |
| **Total** | | **27 tasks** | **15 parallelisable** |
