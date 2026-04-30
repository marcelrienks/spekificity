# tasks: spekificity platform — core project foundation

**feature branch**: `001-spekificity-platform`  
**input**: design documents from `specs/001-spekificity-platform/`  
**date**: 2026-04-29

**prerequisites used**: plan.md ✓ | spec.md ✓ | research.md ✓ | data-model.md ✓ | contracts/skill-contracts.md ✓ | quickstart.md ✓

---

## format: `[id] [p?] [story?] description with file path`

- **[p]**: parallelisable — different files, no dependency on in-progress tasks
- **[us#]**: user story this task belongs to
- no tests — not requested in spec; this is a documentation project with manual validation

---

## phase 1: setup (project scaffolding)

**purpose**: create the directory structure required by all subsequent phases.

- [x] t001 create top-level directory structure: `skills/`, `workflows/`, `setup-guides/`, `vault/`
- [x] t002 create vault subdirectory scaffold: `vault/graph/nodes/`, `vault/lessons/`, `vault/context/`
- [x] t003 [p] create `vault/context/decisions.md` with schema header placeholder
- [x] t004 [p] create `vault/context/patterns.md` with schema header placeholder

---

## phase 2: foundational (blocking prerequisites)

**purpose**: root-level project files that all user stories reference.

**⚠️ critical**: setup guides and workflows cannot be finalized until these exist.

- [x] t005 create root `readme.md` with project overview, prerequisite list, quickstart link, and component update table
- [x] t006 create `.gitignore` entries for `vault/graph/` (opt-out on large repos), `.obsidian/workspace.json`, and standard os/editor files

**checkpoint**: root scaffolding complete — user story work can begin.

---

## phase 3: user story 1 — first-time project initialisation (priority: p1) 🎯 mvp

**goal**: a developer can follow the init workflow to install all tools and have all spekificity custom skills active in under 30 minutes on a fresh macos or linux machine.

**independent test**: follow `workflows/init-workflow.md` step by step on a fresh machine; verify `graphify --version` and `specify --version` succeed, all skill files exist in `.github/agents/` and `.claude/commands/`, and `/speckit.specify` can be invoked without errors.

- [x] t007 [p] [us1] create `setup-guides/graphify-setup.md` — overview, install via `uv tool install graphifyy`, verify command, `--obsidian` flag explanation, troubleshooting
- [x] t008 [p] [us1] create `setup-guides/speckit-setup.md` — overview, install via `uv tool install specify-cli`, verify command, `specify init .` workflow, version compatibility table
- [x] t009 [p] [us1] create `setup-guides/obsidian-setup.md` — overview (optional app), vault-as-filesystem explanation, app install steps, vault open instructions, note it is not required for ai workflow
- [x] t010 [us1] create `workflows/init-workflow.md` — ordered 8-step init workflow: prerequisite check → install graphify → install speckit → `specify init` → install spekificity skills → run `/map-codebase` → verify → next steps; includes detect-before-install idempotency checks at each step

**checkpoint**: us1 complete — developer can initialise a new project from zero.

---

## phase 4: user story 2 — ai-guided codebase & documentation mapping (priority: p2)

**goal**: a developer can invoke `/map-codebase` to build and refresh a graphify → obsidian graph of the project, enabling ai agents to answer cross-cutting questions without scanning all source files.

**independent test**: invoke `/map-codebase` per `skills/map-codebase/skill.md` on a project with ≥20 files; verify `vault/graph/index.md` exists, contains node entries, and an ai agent can answer a cross-cutting question citing vault nodes.

- [x] t011 [us2] create `skills/map-codebase/skill.md` — full skill file: description, trigger (`/map-codebase`), prerequisites (graphify installed, project root), inputs (`--full` flag, optional `claude_api_key`), steps (run `graphify . --obsidian --output vault/graph/`, verify outputs, report diff), outputs table, error handling (missing graphify → print install instructions, write failure → halt without partial write), notes
- [x] t012 [p] [us2] create `vault/graph/index.md` as a human-readable schema template — header with last-updated metadata, node count placeholder, section structure for god nodes, full node list table; this is the template the `/map-codebase` skill overwrites at runtime
- [x] t013 [us2] create `workflows/map-refresh.md` — when to refresh (after file adds/deletes, before `/speckit.plan`, start of new feature), how to refresh (invoke `/map-codebase`), incremental vs full flag guidance, vault size guidance (gitignore `vault/graph/` if >500 nodes)

**checkpoint**: us2 complete — ai can map any project and use vault for context.

---

## phase 5: user story 3 — supercharged speckit feature lifecycle (priority: p2)

**goal**: a developer can run the enriched speckit lifecycle where each step (`/speckit.specify`, `/speckit.plan`, `/speckit.implement`) is decorated with graph-aware context, and lessons learnt are persisted to the vault at feature completion.

**independent test**: in a mapped project, invoke `/context-load` then `/speckit-enrich-specify`; verify the spec output includes cross-references to existing graph nodes. after a completed feature, invoke `/lessons-learnt`; verify `vault/lessons/<date>-<slug>.md` exists with all schema sections populated.

- [x] t014 [p] [us3] create `skills/context-load/skill.md` — description, trigger (`/context-load`), prerequisite (vault exists), inputs (scope: `full`/`graph-only`/`lessons-only`, optional feature filter), steps (read `vault/graph/index.md`, read `vault/context/decisions.md`, read `vault/context/patterns.md`, load relevant lessons entry, summarise in ≤5 bullets with caveman if active, confirm "context loaded"), outputs (ai working memory), postconditions
- [x] t015 [p] [us3] create `skills/lessons-learnt/skill.md` — description, trigger (`/lessons-learnt`), prerequisites (feature complete, `vault/lessons/` exists), inputs (branch auto-detected, date auto-detected, ai model name), steps (detect branch, ai reflection on what worked / harder than expected / decisions / patterns, write `vault/lessons/<date>-<slug>.md` per data-model schema, append to `vault/context/patterns.md`, append to `vault/context/decisions.md`, report path), outputs table, error handling
- [x] t016 [p] [us3] create `skills/speckit-enrich/specify-enrich.md` — decorator for `/speckit.specify`: run `/context-load` if not already run, identify related graph nodes for feature description, annotate description with "related existing components: [list]", invoke `/speckit.specify` with enriched input, post-write: note impacted nodes in spec assumptions
- [x] t017 [p] [us3] create `skills/speckit-enrich/plan-enrich.md` — decorator for `/speckit.plan`: run `/context-load graph-only`, identify graph nodes referenced in `spec.md`, annotate plan's technical context with "impacted graph nodes: [list]", invoke `/speckit.plan`, post-write: verify impacted nodes are present in plan's project structure
- [x] t018 [p] [us3] create `skills/speckit-enrich/implement-enrich.md` — decorator for `/speckit.implement`: run `/context-load` at session start, check graph for related nodes before each task, invoke `/speckit.implement`, post-complete: auto-invoke `/lessons-learnt` then `/map-codebase` incremental
- [x] t019 [us3] create `workflows/feature-lifecycle.md` — enriched speckit lifecycle: 7-step sequence (`/context-load` → `/speckit-enrich-specify` → `/speckit-enrich-plan` → `/speckit.tasks` → `/speckit-enrich-implement` → `/lessons-learnt` → `/map-codebase` incremental), decision points (if vault not mapped: run `/map-codebase` first), expected state at each checkpoint, recovery instructions for partial failures

**checkpoint**: us3 complete — full enriched feature lifecycle is operational.

---

## phase 6: user story 4 — token-efficient ai interactions via caveman (priority: p3)

**goal**: caveman mode is explicitly integrated at every workflow step, with clear guidance on when to invoke it and which intensity level to use.

**independent test**: activate `/caveman lite` then run through `workflows/feature-lifecycle.md`; verify ai responses are compressed throughout without omitting technical content needed for the next step.

- [x] t020 [us4] update `workflows/feature-lifecycle.md` to add explicit caveman invocation checkpoints — add a "token efficiency" section: recommend `/caveman lite` at session start before spec/plan steps (structured output), `/caveman` (full) for implementation steps, `/caveman ultra` for research/exploration; add a note to `workflows/init-workflow.md` and `workflows/map-refresh.md` recommending caveman activation

**checkpoint**: us4 complete — token efficiency guidance is embedded throughout all workflow documents.

---

## phase 7: user story 5 — independent component updates (priority: p3)

**goal**: each third-party component (graphify, obsidian, speckit, spekificity custom layer) can be updated independently without re-initialising the stack.

**independent test**: follow the graphify update section of `workflows/component-update.md`; verify no other spekificity files require changes.

- [x] t021 [us5] create `workflows/component-update.md` — four-section update guide: (1) speckit update (`uv tool upgrade specify-cli`, no spekificity changes unless command interface changed, how to detect breaking changes), (2) graphify update (`uv tool upgrade graphifyy`, update only `skills/map-codebase/skill.md` if cli args change), (3) obsidian update (download new app, no spekificity changes, vault format is stable markdown), (4) spekificity custom layer update (`git pull` from spekificity repo, re-copy skills to `.github/agents/` and `.claude/commands/`); include version compatibility table per component; add token-efficiency note at top recommending `/caveman lite` before reading update docs (constitution principle vi)

**checkpoint**: us5 complete — maintenance workflow is documented.

---

## final phase: polish & cross-cutting concerns

**purpose**: agent-specific skill distribution, context file updates, and final accuracy verification.

- [x] t022 [p] distribute all skills to `.github/agents/` for github copilot — copy: `skills/map-codebase/skill.md` → `.github/agents/map-codebase.agent.md`, `skills/lessons-learnt/skill.md` → `.github/agents/lessons-learnt.agent.md`, `skills/context-load/skill.md` → `.github/agents/context-load.agent.md`, `skills/speckit-enrich/specify-enrich.md` → `.github/agents/speckit-enrich-specify.agent.md`, `skills/speckit-enrich/plan-enrich.md` → `.github/agents/speckit-enrich-plan.agent.md`, `skills/speckit-enrich/implement-enrich.md` → `.github/agents/speckit-enrich-implement.agent.md`
- [x] t023 [p] distribute all skills to `.claude/commands/` for claude code — create `.claude/commands/` directory and copy each skill file with `.md` extension (matching filenames used in t022)
- [x] t024 update `.github/copilot-instructions.md` to include the spekificity skill index and session-start guidance: "at session start, run `/context-load` to load vault context before any work"
- [x] t025 cross-verify `specs/001-spekificity-platform/quickstart.md` against all created skill and workflow files — update any file paths, command names, or step numbers that have diverged from final implementations
- [x] t026 [p] create `docs/validation.md` — measurement methodology for sc-002 (token reduction ≥40%: procedure to record token counts for 5 representative cross-cutting queries on a mapped vs unmapped project, log results, compute reduction %) and sc-003 (caveman verbosity reduction ≥60%: procedure to record character counts of 3 representative ai responses with and without caveman active, compute reduction %); include example log table for each metric
- [x] t027 [p] create root `agents.md` — claude code skill discovery index: list all 6 spekificity skills with their command name, trigger, file path in `.claude/commands/`, and one-line description; add session-start guidance ("run `/context-load` before any feature work"); ensures fr-011 and fr-012 compliance for claude code users

---

## dependencies

```
t001 → t002 → t003, t004
t001 → t005, t006

t007, t008, t009 (parallel) → t010   [us1]

t010 → t011 → t012, t013             [us2]

t013 → t014, t015, t016, t017, t018 (parallel) → t019  [us3]

t019 → t020                           [us4]

t020 → t021                           [us5]

t021 → t022, t023 (parallel) → t024 → t025
t024 → t026, t027 (parallel)
```

---

## parallel execution examples

### us1 — setup guides (after t001):
```
t007 (graphify-setup.md)  ─┐
t008 (speckit-setup.md)   ─┤── all complete → t010 (init-workflow.md)
t009 (obsidian-setup.md)  ─┘
```

### us3 — skill files (after t013):
```
t014 (context-load)          ─┐
t015 (lessons-learnt)        ─┤
t016 (specify-enrich)        ─┤── all complete → t019 (feature-lifecycle.md)
t017 (plan-enrich)           ─┤
t018 (implement-enrich)      ─┘
```

### polish — agent distribution (after t021):
```
t022 (.github/agents/)  ─┐
t023 (.claude/commands/) ─┘── both complete → t024 → t025
```

---

## implementation strategy

**mvp scope (us1 only — t001–t010)**: delivers a working initialisation workflow. a developer can get all tools installed and spekificity scaffolded without any mapping or enrichment features.

**increment 2 (add us2 — t011–t013)**: adds codebase mapping. ai sessions can now load graph context instead of scanning files.

**increment 3 (add us3 — t014–t019)**: full enriched speckit lifecycle. this is the primary daily-use value.

**increment 4 (add us4+us5+polish — t020–t027)**: caveman integration guidance, component update procedures, agent distribution, and validation methodology — hardening and polish.

---

## summary

| phase | user story | tasks | parallel opportunities |
|-------|-----------|-------|----------------------|
| setup | — | t001–t004 (4) | t003, t004 |
| foundational | — | t005–t006 (2) | — |
| phase 3 | us1 (p1) | t007–t010 (4) | t007, t008, t009 |
| phase 4 | us2 (p2) | t011–t013 (3) | t012 |
| phase 5 | us3 (p2) | t014–t019 (6) | t014, t015, t016, t017, t018 |
| phase 6 | us4 (p3) | t020 (1) | — |
| phase 7 | us5 (p3) | t021 (1) | — |
| polish | — | t022–t027 (6) | t022, t023, t026, t027 |
| **total** | | **27 tasks** | **15 parallelisable** |
