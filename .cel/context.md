---
last_deep_read: 2026-05-20T16:45:00Z
version: 5.4
scan_status: full refresh (implementation scaffolding complete)
changes_detected: ✅ Major update (design → implementation phase); implementation roadmap, goal, todo, skill-index added; Python CLI scaffolding with 7 commands; pyproject.toml configured; File count 49→54 (5 new docs)
tracked_files: 62
tracked_wiki_files: 54
python_src_files: 12
---

# spekificity technical brief (implementation scaffolding phase)

## project purpose

Spekificity = specification-driven AI agent development framework solving four critical problems:

| problem | mechanism |
|---|---|
| token bloat | CodeGraph (indexed queries) + aggressive caveman compression (output reduced 75-90%) |
| shallow planning | canonical spec→plan→tasks→implement workflow enforced; SpecKit integration |
| context loss | 3-layer memory model (user/session/repo) + git-backed vault for specs, patterns, lessons |
| low autonomy | pre-indexed code analysis + reusable skills allow agents to work independently overnight |

Core promise: raw code + docs → feature idea → spec → implementation → lessons, all with AI agent as copilot, all tracked in vault, minimal token waste.

**MAJOR MILESTONE (May 20, 2026):** Transitioned from design-only to **implementation scaffolding complete**. Python CLI structure deployed with 7 commands (prepare, context, plan, map, implement, post, lessons). All dependencies configured (pyproject.toml). Ready for skill development and CodeGraph integration.

---

## architecture and tech stack

### implementation status

**Phase:** 1–3 of 5 COMPLETE ✓

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | Implementation readiness documented | ✓ Complete |
| 2 | Python 3.11+ environment + scaffolding | ✓ Complete |
| 3 | CLI structure (7 commands, placeholders) | ✓ Complete |
| 4 | Core skills full implementation | ⧖ In Progress |
| 5 | CodeGraph MCP integration | ⧖ Queued |

### core stack (NOW IN PYTHON)

- **SpecKit/Specify:** spec-driven workflow engine (global install, wrapped by spekificity CLI)
- **Spekificity Python CLI:** 7 commands decorating SpecKit
  - Entry point: `spek` (via pyproject.toml `[project.scripts]`)
  - Module: `spekificity.cli.main:cli` (Click-based)
  - 7 skills: prepare, context, plan, map, implement, post, lessons
- **CodeGraph:** Planned indexed code analysis (SQLAlchemy + Pygments backend)
  - Storage: SQLite database (incremental updates)
  - Languages: Python (via AST), with extensibility for others
  - Tools: `codegraph_symbols()`, `codegraph_references()`, `codegraph_impact()`, `codegraph_definition()`
- **Vault:** Git-backed Obsidian vault for knowledge
  - Specs, decisions, patterns, lessons, session memory
  - Format: plain markdown, human-readable, version-controlled
- **Caveman Mode:** Token compression (75-90% reduction)
  - Active throughout all phases
- **Session Memory:** 3-layer model
  - User memory (`/memories/`) — permanent across projects
  - Session memory (`/memories/session/`) — current conversation
  - Repo memory (`/memories/repo/`) — project-scoped

### project structure (NEW)

```
spekificity/
├── src/spekificity/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py              # CLI entry point (Click)
│   │   ├── prepare.py           # /spek.prepare skill
│   │   ├── context.py           # /spek.context skill
│   │   ├── plan.py              # /spek.plan skill
│   │   ├── map_.py              # /spek.map skill (CodeGraph refresh)
│   │   ├── implement.py         # /spek.implement skill
│   │   ├── post.py              # /spek.post skill (archival)
│   │   └── lessons.py           # /spek.lessons skill
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── codegraph.py         # (placeholder)
│   │   ├── indexer.py           # (placeholder)
│   │   ├── query.py             # (placeholder)
│   │   └── schema.py            # (placeholder)
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── context.py           # (placeholder)
│   │   └── enrichment.py        # (placeholder)
│   ├── vault/
│   │   └── __init__.py          # (placeholder)
│   ├── orchestration/
│   │   └── __init__.py          # (placeholder)
│   └── utils/
│       └── __init__.py          # (placeholder)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_cli.py
│   ├── integration/
│   │   └── __init__.py
│   └── e2e/
│       └── __init__.py
├── wiki/                        # Documentation + specifications
│   ├── [8 root docs]            # vision, workflow, architecture, conventions, intention, llm-wiki, quickstart, speckit
│   ├── setup.md                 # Unified setup guide
│   ├── goal.md                  # NEW: Complete goal statement
│   ├── todo.md                  # NEW: Implementation status report
│   ├── skill-index.md           # NEW: CLI skills reference
│   └── specs/                   # 41 atomic specifications
│       ├── [memory]             # 030-memory-architecture, 031-context-layer, 032-enrichment-layer
│       ├── [graph]              # 050-codegraph-*, 051-graph-storage, 052-node-schema, etc.
│       ├── [skills]             # 100-prepare, 102-post, 104-lessons, etc.
│       ├── [workflow]           # 120-spek-automate, 121-cli-orchestration
│       ├── [patterns]           # 170-backprop-reflex, 171-rarv-reflection, 172-anti-sycophancy, etc.
│       └── [validation]         # 140-integration-validation, 141-test-suite
├── pyproject.toml               # NEW: Hatchling build, 7 core dependencies, dev optional deps
└── .cel/context.md              # THIS FILE (cache + state)
```

### design principles

- Decorate, not fork; integrate SpecKit without replacement
- Token efficiency is first-class (not cleanup)
- Components remain independently updateable
- Deterministic, repeatable workflows
- AI-executable step-by-step guides where CLI impractical
- Modular independence across all layers

---

## key workflows

### workflow stages (deterministic 4-phase model)

**Stage 0: Init (one-time)**
- `spekificity init` → auto-detect tools, install missing, deploy skills, initialize vault, set up code mapping
- Output: `.spekificity/` config, `.agents/skills/` local skills, Obsidian vault ready

**Stage 1: Prepare** (`/spek.prepare`)
- Load vault context (3-layer memory)
- Index code state via CodeGraph (incremental refresh)
- List available specs for feature selection
- Load prior decisions + patterns relevant to feature
- Output: Feature context + related specs, dependency map, related patterns

**Stage 2: Specify & Plan** (`/spek.plan --phase=specify`, then `/speckit.specify`, then `/speckit.plan`)
- Generate feature spec with enrichment layers (Success Criteria, Assumptions, Risk Assessment)
- Parse spec; generate task list (granular, implementable)
- Identify code sections to modify (CodeGraph impact analysis)
- Estimate token budget per task
- Suggest related patterns + decision references
- Output: Detailed implementation plan with code sections, line ranges, token estimates

**Stage 3: Implement** (`/spek.implement`)
- Execute tasks with full context (vault + CodeGraph)
- Apply code changes
- Capture execution trace
- Auto-sync CodeGraph
- Output: Code changes, execution trace

**Stage 4: Post** (`/spek.post`)
- Analyze execution trace
- Extract lessons learned
- Update vault with insights
- Refresh CodeGraph (incremental)
- Archive feature state
- Output: Lesson artifacts, updated vault

Next feature starts at Stage 1 (Prepare) with richer context.

### enrichment pattern (PRE → CORE → POST)

All three enrichment phases follow same pattern:

1. **PRE**: Load context (vault decisions, patterns, code graph state)
2. **CORE**: Call SpecKit command with enriched input
3. **POST**: Validate output, update memory, check alignment

Consolidated into single spec: **enrichment-layer.md** (covering specify, plan, implement).

### 3-layer memory model

**Layer 1: Vault** (permanent, authoritative)
- `vault/decision.md` — architectural decisions
- `vault/patterns.md` — proven patterns + when to use
- `vault/lessons/` — per-feature lessons learned
- Format: plain markdown, git-backed, human-readable

**Layer 2: Repo Memory** (compressed cache)
- `.memories/repo/architectural-decisions.md` — decision index
- `.memories/repo/patterns-index.md` — pattern index for fast lookup

**Layer 3: Session Memory** (ephemeral)
- `.memories/session/context-loaded.md` — what was loaded at session start
- `.memories/session/current-feature.md` — current feature state, progress, blockers

---

## documentation map (54 wiki files)

### root docs (8 files)

- **README.md** — Project overview, platform model, quick start
- **vision.md** — Vision statement, philosophy, design principles (NEW core doc)
- **intention.md** — Principles and intent (kept)
- **architecture.md** — Technical architecture (kept)
- **workflow.md** — Feature development workflow, 4-stage model
- **conventions.md** — Naming conventions, command prefixes, style guide
- **llm-wiki.md** — LLM wiki pattern reference (Andrej Karpathy approach)
- **speckit.md** — SpecKit integration points

### setup and goals (3 files)

- **setup.md** — Unified tool installation guide (SpecKit, Vault, CodeGraph)
- **goal.md** — NEW: Complete goal statement; problems solved and end state
- **todo.md** — NEW: Implementation status report (phases 1-5 progress)

### reference and indexing (2 files)

- **quickstart.md** — Step-by-step getting-started guide
- **skill-index.md** — NEW: CLI skills reference; `/spek.*` command catalog

### atomic specifications (41 files in wiki/specs/)

**Memory & Context (3 specs):**
- **030-memory-architecture.md** — 3-layer model, load lifecycle
- **031-context-layer.md** — Context composition, injection patterns
- **032-enrichment-layer.md** — PRE→CORE→POST pattern for enrichment

**CodeGraph & Indexing (8 specs):**
- **050-codegraph-setup-and-integration.md** — CodeGraph integration contract
- **051-graph-storage-structure.md** — SQLite storage design
- **052-node-schema-design.md** — Node structure, metadata, ID format
- **053-graph-refresh-strategy.md** — Incremental refresh on file changes
- **054-graph-query-patterns.md** — Query patterns for context retrieval
- **055-3layer-query-rule.md** — Query rule for 3-layer retrieval
- **056-code-and-document-maps.md** — Cross-file linking strategy
- **057-graph-merge-integration.md** — Merging multiple graph sources

**Core Skills (7 specs):**
- **100-prepare-command.md** — `/spek.prepare` specification
- **102-post-command.md** — `/spek.post` specification
- **101-post-processing.md** — Detailed post-feature workflow
- **103-spek-map-command.md** — `/spek.map` (CodeGraph refresh)
- **104-spek-lessons-command.md** — `/spek.lessons` (lesson archival)
- **105-spek-implement-workflow.md** — `/spek.implement` workflow
- **110-speckit-integration-contract.md** — Integration contract with SpecKit

**Automation & Orchestration (4 specs):**
- **120-spek-automate-workflow.md** — `/spek.automate` orchestration (optional)
- **121-cli-orchestration.md** — Command orchestration, entry points
- **200-implementation-roadmap.md** — NEW: Implementation readiness + technology stack + timeline
- **130-token-budget.md** — Token budget tracking and optimization

**Patterns & Lessons (4 specs):**
- **020-zettelkasten-conventions.md** — Zettelkasten markdown format
- **021-lessons-format.md** — Lesson document template, archival
- **022-architectural-decisions.md** — Decision tracking, archival
- **023-patterns-library.md** — Proven patterns, tagging, discovery

**Error Handling & Validation (6 specs):**
- **010-error-handling-and-recovery.md** — Error scenarios, recovery procedures
- **011-decorator-wrapper-pattern.md** — Decorator implementation pattern
- **012-git-verification.md** — Git state validation
- **140-integration-validation-and-testing.md** — Integration test patterns
- **141-test-suite-specification.md** — Test structure and coverage
- **142-validation-patterns-archive.md** — Validation patterns reference

**Advanced Topics (9 specs):**
- **060-auto-tagging-wikilinks.md** — Auto-tagging and wikilink generation
- **061-obsidian-graph-export.md** — Graph export format from Obsidian
- **131-session-continuation-strategy.md** — Session state recovery
- **160-multi-developer-coordination.md** — Team coordination patterns
- **170-backprop-reflex.md** — Backprop reflex agent pattern
- **171-rarv-reflection.md** — RARV reflection agent pattern
- **172-anti-sycophancy.md** — Anti-sycophancy measures
- **173-blind-code-review.md** — Blind review process
- **174-caveman-integration.md** — Caveman compression integration

---

## current project state (implementation phase)

**Repository Status:** Active implementation scaffolding (May 20, 2026)  
**Phase:** 1–3 of 5 COMPLETE ✓

### Completed (May 20, 2026)

**Phase 1: Implementation Readiness** ✓
- Comprehensive readiness checklist (all components passing)
- Technology stack decision: Python 3.11+ with Click, Pydantic, SQLAlchemy
- Detailed breakdown of 7 core skills
- CodeGraph MCP specification
- Testing & validation phases
- Timeline estimate (~63h, 2-3 weeks)

**Phase 2: Language & Environment Setup** ✓
- Python 3.11+ selected and configured
- `pyproject.toml` created with all dependencies
- Hatchling build system configured
- 7 core dependencies installed: click, pydantic, sqlalchemy, gitpython, pygments, loguru, pyyaml
- Dev optional dependencies: pytest, pytest-cov, black, ruff, mypy, pytest-mock

**Phase 3: CLI Scaffolding** ✓
- Full directory structure created: `src/spekificity/` with 7 modules
- CLI entry point: `spek` command (Click-based)
- Placeholder implementations for all 7 skills
- Test structure established (unit, integration, e2e)

### In Progress

**Phase 4: Core Skills Full Implementation** ⧖
- `/spek.prepare` — Loading vault context, CodeGraph integration
- `/spek.context` — Context management and injection
- `/spek.plan` — SpecKit orchestration with enrichment
- `/spek.map` — CodeGraph refresh and indexing
- `/spek.implement` — Task execution and code change application
- `/spek.post` — Vault update and lesson archival
- `/spek.lessons` — Lesson discovery and review

**Phase 5: CodeGraph MCP Integration** ⧖
- SQLAlchemy schema implementation
- AST-based Python code indexing
- Graph query engine
- File watch automation

### New Documentation (This Session)

| File | Purpose | Status |
|------|---------|--------|
| goal.md | Complete goal statement; problems + solutions | ✓ Complete |
| todo.md | Implementation status report (5-phase roadmap) | ✓ Complete |
| skill-index.md | CLI skills reference with command catalog | ✓ Complete |
| 200-implementation-roadmap.md | Detailed implementation plan + technology stack | ✓ Complete |
| pyproject.toml | Build config + all dependencies | ✓ Complete |

---

## file inventory and hashes

**Scan Timestamp:** 2026-05-20T16:45:00Z  
**Total Files Tracked:** 54 wiki + 12 source + 2 config + 9 raw = 77 files

### wiki files (54) — current state

**Root docs (8):**
- wiki/README.md (linkage: wiki/README.md → wiki/ subdocs)
- wiki/vision.md
- wiki/intention.md
- wiki/architecture.md
- wiki/workflow.md
- wiki/conventions.md
- wiki/llm-wiki.md
- wiki/speckit.md

**Setup & Goals (3):**
- wiki/setup.md
- wiki/goal.md — NEW
- wiki/todo.md — NEW

**Reference (2):**
- wiki/quickstart.md
- wiki/skill-index.md — NEW

**Specs (41):**
- [All 41 spec files listed above in "documentation map"]

### source files (12)

- src/spekificity/__init__.py
- src/spekificity/cli/main.py
- src/spekificity/cli/prepare.py
- src/spekificity/cli/context.py
- src/spekificity/cli/plan.py
- src/spekificity/cli/map_.py
- src/spekificity/cli/implement.py
- src/spekificity/cli/post.py
- src/spekificity/cli/lessons.py
- src/spekificity/graph/__init__.py
- src/spekificity/memory/__init__.py
- src/spekificity/vault/__init__.py
- [+ 6 placeholder modules: graph/codegraph.py, graph/indexer.py, graph/query.py, graph/schema.py, memory/context.py, memory/enrichment.py, orchestration/*, utils/*]

### config files (2)

- pyproject.toml — NEW: Build config, 7 core + 6 dev dependencies
- README.md — Updated links to wiki structure

### changes from previous scan

**Added (5 new files):**
- wiki/goal.md
- wiki/todo.md
- wiki/skill-index.md
- wiki/specs/200-implementation-roadmap.md
- pyproject.toml

**Modified (cross-reference updates):**
- wiki/setup.md — Updated references
- wiki/workflow.md — Updated references
- README.md — Updated quick start links

**Unchanged (49 files):**
- All other wiki files; all content preserved
- 41 atomic specs in wiki/specs/ — content unchanged (cross-references verified)

---

## next steps

**Immediate (Next Session):**
1. Phase 4 Implementation: Start with `/spek.prepare` (load vault context)
2. CodeGraph schema and storage layer
3. Unit tests for CLI commands

**Within 1 Week:**
1. `/spek.map` CodeGraph refresh command
2. `/spek.context` context injection
3. Integration tests for prepare→plan→implement flow

**Within 2 Weeks:**
1. `/spek.implement` code execution
2. `/spek.post` vault archival
3. Full end-to-end workflow validation

**Context Loading:**
- Loads from Obsidian vault (vault/ - persistent memory)
- Loads from CodeGraph (code index - independent of vault)
- Loads from documentation index (doc graph - separate from code)
- All three layers are atomic and refreshed independently
