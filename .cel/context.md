---
last_deep_read: 2026-05-03t15:04:00z
version: 2.1
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

## documentation map (consolidated & reorganized)

| document | location | purpose | status |
|----------|----------|---------|--------|
| **readme** | `docs/readme.md` | quick start, core problems, value proposition, target users | ✓ consolidated |
| **guide** | `docs/guide.md` | feature lifecycle workflows, enriched speckit operations, token efficiency | ✓ consolidated |
| **architecture** | `docs/architecture.md` | design principles, component roles, data flows, directory structure, vault design | ✓ consolidated |
| **glossary** | `docs/glossary.md` | term definitions (caveman, decorator, graphify, obsidian, speckit, etc.) | unchanged |
| **faq** | `docs/faq.md` | troubleshooting, setup issues, vault operations | unchanged |
| **validation** | `docs/validation.md` | success criteria measurement methodology | unchanged |

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

## document inventory & hash validation (scanned 2026-05-03 15:04)

**primary docs/ (active):**

| file | lines | hash | status |
|------|-------|------|--------|
| docs/readme.md | 116 | e4a2eed40f1b1dc6a196cdaed91d7f5c | ✓ new (consolidated) |
| docs/guide.md | 146 | ff07fcbe4d2f03b4a083fbb2fd54a310 | ✓ new (consolidated) |
| docs/architecture.md | 218 | 9da1179f6ac0557e3930437658110ef5 | ✓ updated |
| docs/glossary.md | 53 | 55a2a95a9527193d4343fd512805b5e1 | ✓ unchanged |
| docs/faq.md | 308 | 420471d15759fca6d3612c4605e1964f | ✓ unchanged |
| docs/validation.md | 96 | 98b7f62546bb5cef1a08478df6fc7eaa | ✓ unchanged |

**removed files:**
- docs/INIT.md (consolidated into readme.md + architecture.md)
- docs/PRD.md (consolidated into readme.md + guide.md + architecture.md)

**naming standardization:**
- ARCHITECTURE.md → architecture.md (case)
- GLOSSARY.md → glossary.md (case)

**cross-reference updates:**
- README.md (root) → updated links to docs/readme.md, docs/guide.md
- .cel/context.md → this file (updated doc map)
- all workflows/specs maintained (no changes)

**scanned**: 14 active files. 2 consolidated. 2 renamed. context refreshed.
