---
last_deep_read: 2026-05-03t00:00:00z
version: 2.0
scan_status: full
---

# spekificity technical brief

## executive summary

**spekificity** is an agentic focused toolset designed for ai agents (github copilot, claude code) that connects graphify (codebase mapping), obsidian (persistent vault), speckit/specify (spec-first cli), and caveman (token compression). solves persistent ai context loss, excessive token consumption, and shallow feature planning. delivered as executable markdown skills, workflows, and setup guides that agents read and run to automate enriched speckit feature lifecycles with persistent context.

---

## problem space

| problem | spekificity solution |
|---------|---------------------|
| ai agents lose context between sessions | obsidian vault stores graph, decisions, lessons; `/context-load` restores at session start |
| token bloat from re-reading all files | graphify generates graph once; ai queries graph instead of scanning files |
| speckit specs/plans disconnected from codebase | `/speckit-enrich-specify` and `/speckit-enrich-plan` inject graph context |
| verbose ai responses consume tokens | caveman skill compresses outputs while preserving technical accuracy |

---

## target users & journeys

**user personas**:
- solo developer: values speed + cognitive load reduction
- team lead/architect: needs consistent toolchain + easy onboarding
- ai power user: wants maximum roi from every token

**core journeys**:
1. **init**: `spekificity init` → auto-detect tools, install missing, deploy skills (~10 min)
2. **map**: `/map-codebase` → graphify generates graph → stored in obsidian vault
3. **feature**: `/context-load` → `/speckit-enrich-specify` → `/speckit-enrich-plan` → `/speckit.tasks` → `/speckit-enrich-implement` → lessons logged
4. **update**: update single tool (graphify/obsidian/speckit/caveman) independently without re-init

---

## architecture & tech stack

**core components** (markdown-interconnected):
- **graphify** (global): analyzes source + docs → dependency/relationship graph
- **obsidian vault** (local): plain markdown storage (filesystem + optional obsidian app); holds graph index + lessons + decisions/patterns
- **speckit/specify** (global): spec-first cli; vanilla commands unchanged; spekificity wraps via decorator pattern
- **caveman skill** (global or local): response compression for token efficiency
- **ai agents**: github copilot + claude code (native skill/agent support)

**delivery model**: all skills, workflows, docs are **markdown files**. no binaries. ai agents read and execute directly.

**directory structure** (project-scoped):
```
spekificity/
├── docs/                      ← project documentation (prd, architecture, glossary, init, validation)
├── skills/                    ← ai-executable skill files
│   ├── context-load/          ← load vault at session start
│   ├── map-codebase/          ← run graphify → obsidian
│   ├── lessons-learnt/        ← capture end-of-feature lessons
│   └── speckit-enrich/        ← decorator wrappers for /specify, /plan, /implement
├── workflows/                 ← multi-step sequences (init, feature-lifecycle, map-refresh, component-update)
├── setup-guides/              ← ai-executable install guides (graphify, obsidian, speckit)
├── specs/                     ← generated speckit features (spec.md, plan.md, tasks.md)
├── vault/                     ← obsidian vault (graph/, lessons/, context/decisions + patterns)
├── .specify/                  ← speckit config (constitution, templates, extensions)
└── .github/agents/ or .claude/commands/ ← agent-specific skill routing
```

---

## enriched feature lifecycle (token-optimized)

```
step 1: /context-load
  → loads vault/graph/index.md + recent lessons
  → ai primed with component map, past decisions, patterns
  ✓ first time: ~2s; subsequent: cached

step 2: /speckit-enrich-specify
  → decorator wraps /speckit.specify
  → injects graph context (related components)
  → output: specs/<feature>/spec.md with cross-refs

step 3: /speckit-enrich-plan
  → decorator wraps /speckit.plan
  → injects impacted graph nodes
  → output: specs/<feature>/plan.md with component impacts

step 4: /speckit.tasks
  → standard speckit (no enrichment needed)
  → input: spec.md + plan.md
  → output: specs/<feature>/tasks.md (dependency-ordered)

step 5: /speckit-enrich-implement
  → decorator wraps /speckit.implement
  → executes all tasks with graph context
  → auto-writes lessons entry → vault/lessons/<date>-<feature>.md
  → auto-runs graphify → updates vault/graph (incremental)

result: feature complete + knowledge persisted for next session
```

**decorator pattern**: spekificity skills **wrap** vanilla speckit; original cli unchanged, independently upgradable.

---

## token efficiency strategy

**mechanisms**:
1. **graph-based context**: query dependency map instead of reading all files
2. **caveman compression**: terse notation, no fluff, full technical content
3. **persistent memory**: load lessons/decisions at start, not re-explained
4. **incremental mapping**: update only changed nodes, not full regeneration

**invocation**: `/caveman lite` (for spec/plan work) or `/caveman` (for implementation)

---

## functional requirements (core)

| id | requirement | status |
|----|-------------|--------|
| fr-001 | init installs/links graphify, obsidian, speckit/specify | core |
| fr-002 | init deploys spekificity custom skills locally (idempotent) | core |
| fr-003 | mapping skill runs graphify + stores output as obsidian vault | core |
| fr-004 | mapping skill supports incremental refresh | core |
| fr-005 | all speckit-extension skills use decorator pattern | core |
| fr-006 | lessons-learnt entries structured, versioned, vault-stored | core |
| fr-007 | caveman skill integrated + invokable at any workflow step | core |
| fr-008 | each component independently updatable (no re-init required) | core |
| fr-009 | support github copilot + claude code as first-class agents | core |
| fr-010 | non-automatable setup steps documented as ai-executable guides | core |

---

## core outcomes

- **operational**: all tools are installed and connected; ai agents can execute skills
- **enriched**: all speckit lifecycle steps are decorated with graph context
- **persistent**: lessons learnt and decisions are captured and surfaced in future sessions
- **multi-platform**: operational on macos + linux
- **modular**: each component is independently updatable

---

## key workflows at a glance

| workflow | purpose | entry point |
|----------|---------|-------------|
| init-workflow.md | tool detection → installation → skill deployment | `spekificity init` or ai-guided |
| feature-lifecycle.md | full speckit cycle (specify→plan→tasks→implement) + lessons | `/context-load` then `/speckit-enrich-*` |
| map-refresh.md | build or refresh graphify graph; store in obsidian | `/map-codebase` |
| component-update.md | update graphify/obsidian/speckit/caveman independently | per-tool update command |

---

## core design principles

1. **decorator pattern**: wrap, never replace. vanilla speckit untouched, independently upgradable.
2. **global speckit, local customization**: speckit installed globally; spekificity skills deployed locally per-project.
3. **modular independence**: each component (graphify, obsidian, speckit, caveman) updatable without full re-init.
4. **ai-executable setup**: where cli automation impractical, setup documented as step-by-step ai-followable guides.
5. **token efficiency by default**: graph-based queries + caveman compression are first-class, not afterthoughts.
6. **markdown-only delivery**: no binaries. all skills/workflows are `.md` files that ai agents read and execute directly.
7. **persistent context across sessions**: obsidian vault stores graph, lessons, decisions; `/context-load` restores at session start.

---

## documentation map

| document | location | purpose |
|----------|----------|---------|
| **prd (product requirements)** | `docs/prd.md` | goals, non-goals, user journeys, functional/non-functional requirements, personas |
| **architecture** | `docs/architecture.md` | component roles, data flows, directory structure, vault design |
| **glossary** | `docs/glossary.md` | term definitions (caveman, decorator, graphify, obsidian, speckit, etc.) |
| **init guide** | `docs/init.md` | high-level narrative, design principles, tool roles |
| **feature spec** | `specs/001-specificity-platform/spec.md` | detailed user stories, requirements, success criteria, assumptions |
| **quickstart** | `specs/001-specificity-platform/quickstart.md` | step-by-step first-time setup |
| **skills** | `skills/<skill>/skill.md` | triggerable ai tasks (agent-agnostic format) |
| **workflows** | `workflows/*.md` | multi-step sequences (init, feature-lifecycle, map-refresh, component-update) |
| **setup guides** | `setup-guides/*.md` | per-tool installation (graphify, obsidian, speckit) |
| **vault: decisions** | `vault/context/decisions.md` | architectural decisions log |
| **vault: patterns** | `vault/context/patterns.md` | identified patterns & recurring solutions |
| **vault: graph** | `vault/graph/index.md` | graphify-generated dependency graph (runtime) |
| **vault: lessons** | `vault/lessons/*.md` | feature lessons entries (runtime, one per feature) |
| **agent routing** | `agents.md` | claude code slash-command index |

---

## non-goals (v1)

- building graphify, obsidian, or speckit functionality from scratch
- gui or web interface
- support for ai agents beyond copilot + claude code
- cloud sync or multi-user vault sharing
- automatic merge conflict resolution with speckit upstream updates

**v1 scope**: all speckit steps enriched when map available; independent component updates (no cross-breaking changes); macos + linux support; fully local operation (no cloud/server required)

---

## known dependencies

- python 3.11+, `uv` package manager
- speckit installed globally: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- graphify installed globally: `uv tool install graphifyy`
- github copilot or claude code for ai agent
- obsidian (desktop app optional; vault is plain markdown)
- git + basic terminal knowledge

---

## entry points for agent interaction

**at session start:**
```
/context-load
```

**for daily feature work:**
```
/speckit-enrich-specify → /speckit-enrich-plan → /speckit.tasks → /speckit-enrich-implement
```

**for codebase refresh:**
```
/map-codebase
```

**for token efficiency:**
```
/caveman lite     (specs/plans)
/caveman          (implementation)
```

---

**status**: production-ready. zero breaking changes expected for dependent projects. modular: each component can be updated independently.

---

## document inventory (scanned 2026-05-03)

| file | category |
|------|----------|
| README.md | root |
| docs/prd.md | documentation |
| docs/architecture.md | documentation |
| docs/glossary.md | documentation |
| docs/init.md | documentation |
| docs/faq.md | documentation |
| docs/validation.md | documentation |
| workflows/init-workflow.md | workflow |
| workflows/feature-lifecycle.md | workflow |
| workflows/map-refresh.md | workflow |
| workflows/component-update.md | workflow |
| setup-guides/graphify-setup.md | setup |
| setup-guides/obsidian-setup.md | setup |
| setup-guides/speckit-setup.md | setup |

**scanned**: 14 files. no changes from 2026-04-30. context cache valid.
