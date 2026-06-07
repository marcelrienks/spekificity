# Spekificity: Complete Framework Implementation Plan

**Plan Version:** 1.0  
**Created:** 2026-06-07  
**Feature Branch:** `001-complete-framework`  
**Scope:** Full Spekificity framework from specification to production-ready tool

---

## Executive Summary

This plan defines the complete implementation roadmap for Spekificity, a spec-driven agent development framework. The project requires building 5 major components across 5 implementation phases, with careful sequencing to ensure each phase builds on prior work. Total estimated effort: 40-50 engineering hours (200K-300K tokens), organized as 25-30 independent, prioritized tasks.

**Success Definition:** Users can run `spek init` on any Python 3.11+ project, then use the full `/spek.*` workflow (prepare → plan → implement → conclude) to manage feature development with deterministic planning and persistent knowledge.

---

## Part 1: Technical Context & Analysis

### 1.1 Specification Overview

The feature specification (in `specs/001-complete-framework/spec.md`) defines:

- **4 Core Components:**
  1. Installation system (global + per-project)
  2. Knowledge vault (Obsidian-backed, git-stored)
  3. Code indexing (lat.md-based BM25 retrieval)
  4. Workflow orchestration (SpecKit-wrapped agent skills)

- **5 User-Facing Commands:**
  - `/spek.prepare` — Load prior context, index codebase, generate navigation guide
  - `/spek.plan` — Convert feature intent to spec + plan + tasks
  - `/spek.implement` — Execute tasks with persistent progress, decision logging
  - `/spek.conclude` — Analyze outcomes, extract lessons, update vault
  - `spek init` — One-time per-project initialization

- **Functional Scope (14 FR blocks):**
  - Installation & verification (FR-001–FR-007)
  - /spek.prepare (FR-010–FR-014)
  - /spek.plan (FR-020–FR-026)
  - /spek.implement (FR-030–FR-036)
  - /spek.conclude (FR-040–FR-045)
  - Vault & knowledge mgmt (FR-050–FR-054)
  - Code indexing (FR-060–FR-064)
  - Git integration (FR-070–FR-073)
  - Documentation (FR-080–FR-083)

### 1.2 Architectural Constraints & Design Principles

**Mandatory Integration Points:**
- SpecKit (v0.9.6+) — Spec → plan → implement orchestration (required)
- lat.md — Sole code analysis tool; BM25 retrieval (required, no fallback in production)
- Obsidian CLI — Vault operations and exports (required for /spek.conclude)
- Caveman skill — Token compression (required for terse outputs)

**Design Pillars (Non-Negotiable):**
1. **Token Efficiency** — Pre-indexed context; no file scans; Caveman compression available
2. **Determinism** — Spec → plan → implement → conclude; reproducible; auditable
3. **Persistence** — Git-backed vault; knowledge compounds across features
4. **Autonomy** — Agents operate with minimal hand-holding; human gates on plan approval

**Architectural Patterns:**
- **Programmatic Pipeline** — Deterministic outputs, typed contracts (Pydantic), idempotent runs
- **Dual-System Architecture** — Vault (slow-changing knowledge) + Code Index (fast-changing analysis)
- **Decorator Pattern** — Spekificity wraps SpecKit without modifying it
- **Modular Independence** — Each component (vault, index, spec engine) independently upgradeable

### 1.3 Dependency Analysis

| Dependency | Version | Type | Status | Notes |
|------------|---------|------|--------|-------|
| Python | 3.11+ | Runtime | External | Verified in installer |
| uv | Latest | Package Manager | External | Verified in installer |
| git | Latest | VCS | External | Verified in installer |
| SpecKit | v0.9.6+ | Spec/Plan Engine | Auto-installed | Core orchestration tool |
| lat.md | Latest | Code Index | Auto-installed | Canonical code analysis |
| Obsidian CLI | Latest | Vault Operations | Auto-installed | Required for /spek.conclude |
| Caveman | Latest | Compression | Auto-installed | Optional, for token savings |
| Pydantic | 2.0+ | Type Contracts | Internal | Data validation for artifacts |
| markdown-hero | Latest | Markdown Linting | Internal | Structural hygiene for vault |
| GitPython | 3.1.0+ | Git Integration | Internal | Branch/commit operations |

**Critical Decision Point 1:** All dependencies must be auto-installed by the Spekificity installer. If SpecKit, lat.md, or Obsidian CLI are unavailable, installation fails with clear guidance.

### 1.4 Unknowns & Clarification Needed

| Item | Current State | Resolution | Impact |
|------|---------------|-----------|--------|
| SpecKit API Stability | Assumption: stable v0.9.6+ | Verify SpecKit accepts wrapper commands; test enrichment injection points | High: if SpecKit API unstable, wrapper approach fails |
| lat.md MCP Interface | Assumption: available as MCP tools | Confirm lat.md query tools (lat_files, lat_callers, lat_impact) exposed via MCP | High: /spek.implement context injection depends on this |
| Obsidian CLI Export Format | Assumption: exports valid Markdown | Test `obsidian export` command; verify output structure | Medium: affects vault export in /spek.conclude |
| Agent Skill Invocation | Assumption: can wrap SpecKit via agent skills | Confirm `/spek.*` commands can be registered as agent skills with access to SpecKit; test invocation from Copilot Chat | High: entire workflow depends on skill availability |
| Vault Performance at Scale | Assumption: vault fast at 100+ lessons | Benchmark vault loading with 50-100 decision/pattern/lesson files | Medium: affects /spek.prepare speed |
| lat.md Sync Performance | Assumption: incremental sync < 5s | Measure full index rebuild + incremental sync time on sample codebases | Medium: affects /spek.prepare speed requirement (30s SLA) |

**Critical Decision Point 2:** Before implementation begins, resolve unknowns 1-4 (high-impact dependencies). Unknowns 5-6 can be addressed during Phase 1.

---

## Part 2: Implementation Architecture

### 2.1 Package Structure

**Root-level package:** `spekificity/` (Python package, installable via `uv tool install`)

```
spekificity/
├── __init__.py                 # Package entry point
├── __main__.py                 # CLI entry: python -m spekificity
├── cli/                        # CLI commands (entry point: spek command)
│   ├── __init__.py
│   ├── main.py                 # Main CLI router (spek --help, spek --version)
│   ├── install.py              # Installation & dependency verification
│   ├── init.py                 # Per-project initialization (spek init)
│   └── helpers.py              # CLI utilities (colors, prompts, path resolution)
│
├── core/                       # Core logic (no CLI, testable)
│   ├── __init__.py
│   ├── vault.py                # Vault loading, writing, querying
│   ├── index.py                # lat.md integration (query wrapper)
│   ├── speckit_wrapper.py      # SpecKit orchestration (specify → plan → implement)
│   ├── context.py              # Context injection (decisions, patterns, code)
│   ├── progress.py             # Task progress tracking
│   ├── decisions.py            # Decision logging & extraction
│   └── types.py                # Pydantic models (Spec, Plan, Task, Decision, etc.)
│
├── skills/                     # Agent skills (registered as /spek.* commands)
│   ├── __init__.py
│   ├── prepare.py              # /spek.prepare skill
│   ├── plan.py                 # /spek.plan skill
│   ├── implement.py            # /spek.implement skill
│   ├── conclude.py             # /spek.conclude skill
│   ├── context_loader.py       # /spek.context skill (utility)
│   └── helpers.py              # Skill utilities
│
├── templates/                  # Default templates (vault structure, specs, plans)
│   ├── vault_init.md           # Initial vault skeleton
│   ├── constitution.md         # Default constitution (project principles)
│   ├── spec_template.md        # Spec.md generation template
│   ├── plan_template.md        # Plan.md generation template
│   └── task_template.md        # Task entry generation template
│
├── integrations/               # External tool integrations
│   ├── __init__.py
│   ├── speckit.py              # SpecKit command runners
│   ├── lat_md.py               # lat.md MCP query interface
│   ├── obsidian.py             # Obsidian CLI operations
│   ├── git.py                  # Git operations (branch, commit, etc.)
│   └── semantic_search.py      # Fallback semantic search (if lat.md unavailable)
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_vault.py
│   ├── test_index.py
│   ├── test_speckit_wrapper.py
│   ├── test_context.py
│   ├── test_skills.py
│   └── fixtures/               # Test data, mock projects
│
├── pyproject.toml              # Package metadata, dependencies, entry points
└── README.md                   # User-facing documentation

```

### 2.2 Agent Skills Registration

Skills are registered as `/spek.*` commands in the agent context. Implementation approach:

**Skills Directory in Project (.github/agents/skills/):**
```
.github/agents/skills/
├── spek-prepare/
│   ├── _skill.md               # Skill definition (input, output, example)
│   └── instructions.md         # Detailed instructions for agent
├── spek-plan/
│   ├── _skill.md
│   └── instructions.md
├── spek-implement/
│   ├── _skill.md
│   └── instructions.md
└── spek-conclude/
    ├── _skill.md
    └── instructions.md
```

**Agent Context Registration:** Skills are automatically registered in `.github/copilot-instructions.md` during `spek init`.

**Skill Invocation Model:**
- Each skill wraps a Python CLI entry point (e.g., `/spek.prepare` → `python -m spekificity prepare`)
- Skills accept feature names, descriptions, and options as arguments
- Output is returned as structured markdown (spec, plan, summary, etc.)

### 2.3 Vault Structure (Specification)

```
vault/
├── decisions.md                # Append-only log of architectural decisions
├── patterns.md                 # Reusable patterns, conventions, examples
├── lessons.md                  # Lessons learned from completed features
├── vision.md                   # Project vision, principles, governance
└── lessons/                    # Timestamped lesson files (auto-created)
    ├── 2026-06-07-feature-abc.md
    ├── 2026-06-14-feature-def.md
    └── [more lesson files]
```

**Vault File Format:** Standard Markdown with YAML frontmatter for metadata.

Example `decisions.md` entry:
```yaml
---
id: dec-001
title: Use SpecKit for Spec-Driven Workflows
status: approved
date: 2026-06-07
author: architect
---

## Decision

Use SpecKit (v0.9.6+) as the canonical specification and planning tool for all features.

## Rationale

- Mature, actively maintained GitHub project
- Wide community adoption
- Native YAML workflow (spec → plan → tasks)
- Integrates with agent workflows

## Implications

- Developers must learn SpecKit conventions
- Some features may need Spekificity wrapper logic
- Long-term dependency on SpecKit team

## Alternatives Considered

- Custom in-house spec engine (rejected: too much maintenance)
- SDD Pilot (rejected: less mature, narrower adoption)
```

### 2.4 Data Model & Type Contracts

All artifacts use Pydantic v2 models for validation and serialization.

```python
# spekificity/core/types.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Entity(BaseModel):
    name: str
    description: str
    fields: List[str]

class SuccessCriteria(BaseModel):
    id: str  # SC-001, SC-002, etc.
    description: str
    measurable: bool

class Assumption(BaseModel):
    id: str  # Assumption-1, etc.
    description: str

class Spec(BaseModel):
    title: str
    branch: str
    created: datetime
    user_stories: List[dict]  # Priority, scenarios, acceptance criteria
    requirements: List[dict]   # FR-001, FR-002, etc.
    entities: List[Entity]
    success_criteria: List[SuccessCriteria]
    assumptions: List[Assumption]

class Task(BaseModel):
    id: str
    title: str
    description: str
    priority: str  # P0, P1, P2
    dependencies: List[str]  # Task IDs this depends on
    success_criteria: List[str]
    estimated_tokens: int
    estimated_hours: float

class Plan(BaseModel):
    spec_branch: str
    spec_file: str
    tasks: List[Task]
    architecture: str  # Architecture overview (no code)
    tech_stack: List[str]
    risks: List[dict]  # risk, mitigation, probability
    sequencing: str  # Dependency graph, critical path

class Decision(BaseModel):
    id: str
    title: str
    status: str  # approved, proposed, rejected, superseded
    date: datetime
    rationale: str
    implications: List[str]
    alternatives: List[str]

class Lesson(BaseModel):
    feature: str
    date: datetime
    outcomes: str  # What was actually built
    lessons: List[str]  # Key learnings
    patterns: List[str]  # New or refined patterns
    decisions: List[str]  # New decisions made
```

---

## Part 3: Code Sections to Create/Modify

### 3.1 Installation & Dependency Resolution

**File: `spekificity/pyproject.toml`**
- Define all dependencies (SpecKit, lat.md, Obsidian CLI, Caveman, etc.)
- Configure entry points: `[project.scripts]` with `spek = spekificity.cli.main:main`
- Ensure dependencies are pinned to compatible versions

**File: `spekificity/cli/install.py`**
- Dependency check function: verify Python 3.11+, git, uv
- Auto-install logic: if SpecKit/lat.md missing, run `pip install`
- Obsidian CLI check: warn if missing (non-blocking)
- Status report: list installed tools and versions

### 3.2 Per-Project Initialization

**File: `spekificity/cli/init.py`**
- Validate git repo (must be in a git-initialized directory)
- Create vault structure (decisions.md, patterns.md, lessons.md, lessons/)
- Run `specify init .` for SpecKit per-project setup
- Initialize lat.md index (`.lat/` directory)
- Create `.spek/` with skill definitions
- Create `specs/` directory
- Write `.github/copilot-instructions.md` with skill registrations

**Templates (spekificity/templates/):**
- `vault_init.md` — Vault skeleton (frontmatter format, structure)
- `constitution.md` — Default project constitution
- `spec_template.md` — Template for spec.md generation
- `plan_template.md` — Template for plan.md generation

### 3.3 Vault Engine

**File: `spekificity/core/vault.py`**
- `load_decisions()` — Load all entries from vault/decisions.md
- `load_patterns()` — Load all entries from vault/patterns.md
- `load_lessons()` — Load all entries from vault/lessons/ and lessons.md
- `write_lesson()` — Append new lesson to vault/lessons/ (with timestamp)
- `update_decision()` — Add/update decision entry
- `query_decisions(intent)` — Semantic search on decisions (lat.md or fallback)
- `export_vault()` — Export vault for Obsidian CLI or version control

### 3.4 Code Indexing (lat.md Integration)

**File: `spekificity/integrations/lat_md.py`**
- `index_codebase()` — Run lat.md init and sync
- `query_relevant_files(intent)` — BM25 search for files by feature intent
- `query_functions(intent)` — Search for functions/methods by name or intent
- `query_impact(file_path)` — Callers, dependencies of a file
- `fallback_search()` — If lat.md unavailable, use semantic_search or grep

**File: `spekificity/integrations/semantic_search.py`**
- Fallback semantic search (if lat.md timeout or missing)
- Use workspace semantic search capability to find relevant code

### 3.5 SpecKit Orchestration

**File: `spekificity/core/speckit_wrapper.py`**
- `run_specify()` — Invoke `speckit specify` with enriched context (vault decisions, patterns)
- `run_plan()` — Invoke `speckit plan` with architecture context
- `run_implement()` — Invoke `speckit implement` with task context
- `validate_spec()` — Check spec for testability, measurable criteria
- `validate_plan()` — Check plan for task independence, clear dependencies

**File: `spekificity/integrations/speckit.py`**
- Command runners for `speckit specify`, `speckit plan`, `speckit implement`, `speckit analyze`
- Environment setup (pass vault context, code index paths to SpecKit)
- Output parsing (extract spec.md, plan.md, tasks.md from SpecKit output)

### 3.6 Context Injection

**File: `spekificity/core/context.py`**
- `load_feature_context()` — Load relevant decisions, patterns, code for a task
  - Call `vault.query_decisions(task_intent)`
  - Call `index.query_relevant_files(task_intent)`
  - Call `index.query_functions(task_intent)`
  - Return structured context object
- `inject_context()` — Format context for agent consumption (code snippets, decision summaries, patterns)
- `compress_context()` — Use Caveman skill to compress context if needed

**File: `spekificity/integrations/semantic_search.py`**
- Wrapper around workspace semantic_search tool
- Cache results to avoid repeated queries

### 3.7 Progress Tracking & Decision Logging

**File: `spekificity/core/progress.py`**
- `start_task()` — Initialize progress log for a task
- `log_progress()` — Append progress entry to log
- `mark_complete()` — Mark task complete with summary
- `mark_rollback()` — Rollback task, restore previous state
- Progress log location: `.specify/logs/TASK_ID.md`

**File: `spekificity/core/decisions.py`**
- `log_decision()` — Parse decision annotation (e.g., `@decision "use pattern X because..."`)
- `extract_decisions()` — Extract all decisions from task implementation session
- `write_decisions_to_vault()` — Write extracted decisions to vault

### 3.8 Agent Skills

**File: `spekificity/skills/prepare.py`**
- Input: feature name or branch name
- Actions:
  1. Check git state (clean working directory)
  2. Load vault (decisions, patterns, lessons)
  3. Index codebase (lat.md sync)
  4. Generate navigation guide (relevant files, patterns, prior decisions)
  5. Estimate token overhead
- Output: structured onboarding report

**File: `spekificity/skills/plan.py`**
- Input: feature description (or reference spec)
- Actions:
  1. Call `speckit specify` with context enrichment (vault decisions, patterns)
  2. Identify ambiguities; prompt for clarification
  3. Fill unambiguous gaps with defaults
  4. Call `speckit plan` to generate tasks
  5. Validate all requirements testable
  6. Generate spec.md, plan.md, tasks.md
- Output: complete spec, plan, and task list

**File: `spekificity/skills/implement.py`**
- Input: task ID (from tasks.md)
- Actions:
  1. Load task context (code, decisions, patterns)
  2. Inject context into agent session
  3. Execute task with progress tracking
  4. Log decisions made during implementation
  5. Mark task complete
- Output: implementation summary, decision log, updated task status

**File: `spekificity/skills/conclude.py`**
- Input: feature branch name or spec reference
- Actions:
  1. Analyze actual outcomes vs success criteria
  2. Extract lessons learned from implementation log
  3. Identify new patterns or refined patterns
  4. Write lessons to vault/lessons/
  5. Update vault/decisions.md and patterns.md
  6. Export feature summary (spec + plan + outcomes + lessons)
  7. Refresh lat.md index
- Output: lessons document, vault updates, feature archive

### 3.9 Git Integration

**File: `spekificity/integrations/git.py`**
- `create_feature_branch()` — Create branch from feature name (or use existing)
- `auto_commit()` — Stage and commit changes before major transitions
- `merge_feature()` — Merge completed feature back to main (squash or standard)
- `view_commit_history()` — Show commits for feature
- `handle_merge_conflicts()` — Provide guidance for conflict resolution

### 3.10 Tests

**File: `spekificity/tests/test_*.py`**
- Unit tests for vault loading/writing
- Unit tests for lat.md query interface
- Unit tests for SpecKit wrapper commands
- Integration tests for full workflow (prepare → plan → implement → conclude)
- Fixtures: sample projects with known vault/code structures

---

## Part 4: Sequenced Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-2, 60-80 hours)

**Objective:** Build the foundation: installation, CLI, vault engine, and basic context loading.

**Deliverables:**
1. Package structure (`spekificity/` with all directories)
2. Installation system (`spek` CLI, dependency verification, auto-install)
3. Per-project initialization (`spek init` command)
4. Vault engine (load/write decisions, patterns, lessons)
5. Unit tests for vault and CLI

**Tasks:**
- T1.1: Set up Python package structure, pyproject.toml, entry points
- T1.2: Implement `spek --version` and `spek --help` commands
- T1.3: Implement dependency verification (Python 3.11+, git, uv)
- T1.4: Implement auto-install for SpecKit, lat.md, Obsidian CLI
- T1.5: Create vault initialization templates (decisions.md, patterns.md, lessons.md)
- T1.6: Implement `spek init` command (create vault structure, .spek/, specs/)
- T1.7: Implement vault.py (load/write operations, Markdown parsing)
- T1.8: Implement types.py (Pydantic models for Spec, Plan, Task, Decision, Lesson)
- T1.9: Write unit tests for vault and CLI
- T1.10: Document installation process in README

**Dependencies:**
- None (Phase 1 is independent)

**Risks:**
- Dependency version compatibility (SpecKit, lat.md API changes)
  - Mitigation: Pin versions in pyproject.toml; test with target versions before release

**Token Estimate:** 40-50K tokens (code generation, testing, documentation)

---

### Phase 2: Vault Engine & Code Indexing (Weeks 2-3, 50-70 hours)

**Objective:** Build vault querying, lat.md integration, and context injection.

**Deliverables:**
1. Vault querying (semantic search on decisions, patterns)
2. lat.md integration (index sync, BM25 search)
3. Context injection (load relevant code, decisions, patterns for a task)
4. Fallback semantic search (if lat.md unavailable)
5. Unit tests for index and context

**Tasks:**
- T2.1: Implement lat_md.py (index sync, query interface)
- T2.2: Implement fallback semantic_search.py (if lat.md unavailable)
- T2.3: Implement context.py (load_feature_context, inject_context)
- T2.4: Implement context compression (using Caveman skill)
- T2.5: Test lat.md integration (query for files, functions, impact)
- T2.6: Test context injection with sample project
- T2.7: Benchmark vault loading and lat.md queries
- T2.8: Write integration tests for index + context
- T2.9: Document context loading in wiki/

**Dependencies:**
- Phase 1 (vault engine must exist before querying)
- SpecKit and lat.md must be installed (verified in Phase 1)

**Risks:**
- lat.md API changes or missing MCP interface
  - Mitigation: Confirm MCP tools available before Phase 2 start (Decision Point 2)
- Context window overflow (too much context injected)
  - Mitigation: Implement context compression with Caveman; limit context size

**Token Estimate:** 50-60K tokens (integration code, testing, benchmarking)

---

### Phase 3: SpecKit Orchestration (Weeks 3-4, 40-60 hours)

**Objective:** Wrap SpecKit commands to inject context and generate specs, plans, and tasks.

**Deliverables:**
1. SpecKit wrapper (specify, plan, implement, analyze commands)
2. Enrichment layer (inject vault context, code context into SpecKit)
3. Output parsing (extract spec.md, plan.md, tasks.md)
4. Validation logic (testability, measurable criteria)
5. Unit tests for SpecKit wrapper

**Tasks:**
- T3.1: Implement speckit_wrapper.py (run_specify, run_plan, run_implement)
- T3.2: Implement speckit.py (command runners, environment setup)
- T3.3: Implement enrichment layer (inject decisions, patterns, code into SpecKit)
- T3.4: Implement output parsing (extract and validate spec.md, plan.md)
- T3.5: Implement validation logic (testability checks, measurable criteria)
- T3.6: Test SpecKit wrapper with sample feature
- T3.7: Test enrichment injection (verify context is passed to SpecKit)
- T3.8: Write integration tests for full spec → plan workflow
- T3.9: Document SpecKit integration in wiki/

**Dependencies:**
- Phase 1 (vault engine)
- Phase 2 (context injection)
- SpecKit installation (Phase 1)

**Risks:**
- SpecKit API stability (command signature changes, output format changes)
  - Mitigation: Pin SpecKit version; add version check in wrapper; test with target version
- Enrichment layer complexity (too much context confuses SpecKit)
  - Mitigation: Implement incremental enrichment; start minimal, expand based on testing

**Token Estimate:** 50-60K tokens (wrapper code, enrichment, testing)

---

### Phase 4: Agent Skills & Workflow (Weeks 4-5, 50-70 hours)

**Objective:** Implement the 4 core agent skills: prepare, plan, implement, conclude.

**Deliverables:**
1. `/spek.prepare` skill (context loading, codebase indexing, navigation guide)
2. `/spek.plan` skill (spec generation, ambiguity resolution, plan creation)
3. `/spek.implement` skill (task execution, progress tracking, decision logging)
4. `/spek.conclude` skill (outcome analysis, lesson extraction, vault updates)
5. Skill registration in agent context
6. Integration tests for full workflow

**Tasks:**
- T4.1: Implement prepare.py skill (workspace check, vault load, index sync, navigation guide)
- T4.2: Implement plan.py skill (orchestrate SpecKit specify → plan, validate outputs)
- T4.3: Implement implement.py skill (task context loading, progress tracking, decision logging)
- T4.4: Implement conclude.py skill (outcome analysis, lesson extraction, vault updates)
- T4.5: Implement progress.py (task logging, rollback, completion)
- T4.6: Implement decisions.py (decision extraction, parsing, vault writing)
- T4.7: Register skills in agent context (.github/copilot-instructions.md)
- T4.8: Create skill definition files (.github/agents/skills/spek-*/[_skill.md, instructions.md])
- T4.9: Test full workflow: prepare → plan → implement → conclude (manually)
- T4.10: Write end-to-end integration tests
- T4.11: Document skill usage in wiki/

**Dependencies:**
- Phase 1 (vault engine)
- Phase 2 (context injection)
- Phase 3 (SpecKit wrapper)

**Risks:**
- Agent skill invocation not working (registration or context injection issues)
  - Mitigation: Test skill invocation early; work with agent team if needed
- Task scope too large or too small
  - Mitigation: Validate task independence and scope during plan validation

**Token Estimate:** 60-80K tokens (4 skills, workflow orchestration, testing)

---

### Phase 5: Integration, Polish, Testing (Weeks 5-6, 40-60 hours)

**Objective:** Integrate all components, polish user experience, comprehensive testing, and documentation.

**Deliverables:**
1. Complete installation flow (global + per-project)
2. Obsidian CLI integration (vault exports, graph generation)
3. Git integration (branch creation, auto-commit, merge)
4. Comprehensive test suite (unit, integration, end-to-end)
5. Complete user documentation (README, setup guide, skill reference)
6. Production-ready error handling and logging

**Tasks:**
- T5.1: Integrate Obsidian CLI operations (export, graph generation)
- T5.2: Implement git.py (branch creation, commit, merge, conflict handling)
- T5.3: Implement complete error handling across all components
- T5.4: Add comprehensive logging (debug, info, error levels)
- T5.5: Test full installation flow (uv tool install spekificity)
- T5.6: Test per-project initialization (spek init)
- T5.7: End-to-end test: feature from prepare → conclude
- T5.8: Test error cases (missing dependencies, git conflicts, invalid specs)
- T5.9: Performance testing (vault loading, lat.md queries, /spek.prepare 30s SLA)
- T5.10: Write comprehensive README (features, prerequisites, installation, quick-start)
- T5.11: Write skill reference documentation
- T5.12: Create example project walk-through
- T5.13: Refactor code for clarity, consistency, maintainability

**Dependencies:**
- Phase 1-4 (all core components)

**Risks:**
- Documentation may lag implementation (mitigated by continuous documentation)
- User experience issues discovered during testing
  - Mitigation: Usability testing with sample users; iterate on UX

**Token Estimate:** 60-80K tokens (integration, testing, documentation, refinement)

---

## Part 5: Token Usage Estimates

| Phase | Component | Estimate | Notes |
|-------|-----------|----------|-------|
| **Phase 1** | Core Infrastructure | 40-50K | Package, CLI, vault, types, tests |
| **Phase 2** | Vault + Index | 50-60K | lat.md integration, context, compression |
| **Phase 3** | SpecKit Wrapper | 50-60K | Orchestration, enrichment, validation |
| **Phase 4** | Agent Skills | 60-80K | 4 skills, workflow, integration tests |
| **Phase 5** | Integration & Polish | 60-80K | Obsidian, git, testing, documentation |
| **TOTAL** | **Complete Framework** | **260-330K** | Full project with tests & docs |

**Token Usage Breakdown:**
- Code generation: 130-160K (35-40% of total)
- Testing & debugging: 70-100K (25-30% of total)
- Documentation: 40-50K (15-20% of total)
- Refinement & polish: 20-30K (5-10% of total)

**Caveats:**
- Estimates assume straightforward implementation (no major API instability)
- Actual usage may vary by ±20% based on complexity encountered
- Token efficiency can be improved using Caveman skill for terse code generation

---

## Part 6: Risk Assessment & Mitigation

### High-Risk Factors

| Risk | Probability | Impact | Mitigation | Decision Point |
|------|-------------|--------|-----------|---|
| **SpecKit API instability** | Medium | High | Pin version; add version checks; test early | Decision 2 |
| **lat.md MCP interface missing/unstable** | Medium | High | Verify MCP tools before Phase 2; implement fallback | Decision 2 |
| **Obsidian CLI unavailable** | Low | Medium | Provide manual vault export; document fallback | Phase 5 |
| **Agent skill registration fails** | Medium | High | Test skill invocation in Phase 4; coordinate with agent team | Phase 4 |
| **Token overhead exceeds expectations** | Low | Medium | Implement Caveman compression; optimize context injection | Phase 2 |
| **Vault/lat.md performance at scale** | Low | Medium | Benchmark in Phase 2; optimize queries if needed | Phase 2 |
| **Git merge conflicts during feature work** | Low | Low | Provide conflict resolution guidance; allow manual resolution | Phase 5 |
| **User experience confusion** | Medium | Medium | Usability testing; clear error messages; comprehensive docs | Phase 5 |

### Critical Decision Points

**Decision 1 (Pre-Planning):**
- Confirm SpecKit v0.9.6+ is stable and supports wrapper command injection
- Confirm lat.md MCP tools are available (lat_files, lat_callers, lat_impact)
- Confirm Obsidian CLI export functionality works
- Decision Owner: Architect; Timeline: Before Phase 1 start; Blocker: YES

**Decision 2 (Phase 1-2 Boundary):**
- Verify vault loading performance (< 2s for 100+ entries)
- Verify lat.md query performance (< 5s for full index rebuild, < 1s for queries)
- Confirm /spek.prepare can meet 30s SLA
- Adjust Phase 2 scope if performance issues discovered
- Decision Owner: Tech Lead; Timeline: After Phase 1; Blocker: YES

**Decision 3 (Phase 4-5 Boundary):**
- Validate agent skill invocation works (register /spek.* commands)
- Test context injection into agent session
- Confirm full workflow (prepare → plan → implement → conclude) executes end-to-end
- Decision Owner: Integrations Lead; Timeline: After Phase 4; Blocker: YES

---

## Part 7: Dependencies & Sequencing

### Dependency Graph

```
Phase 1: Core Infrastructure
  ├─ Package structure, CLI, vault engine, types
  └─ No external dependencies (only SpecKit/lat.md verification)

Phase 2: Vault + Index
  ├─ Depends on: Phase 1 (vault engine)
  ├─ Decision 2: Performance verification
  └─ Delivers: context injection layer

Phase 3: SpecKit Wrapper
  ├─ Depends on: Phase 1 (vault), Phase 2 (context)
  ├─ Parallel work: speckit integration, enrichment layer
  └─ Delivers: spec/plan/task generation

Phase 4: Agent Skills
  ├─ Depends on: Phase 1-3 (all core components)
  ├─ Decision 3: Agent skill invocation
  └─ Delivers: user-facing /spek.* commands

Phase 5: Integration & Polish
  ├─ Depends on: Phase 1-4 (all components)
  ├─ Parallel work: Obsidian, git, comprehensive testing
  └─ Delivers: production-ready framework
```

### Critical Path

**Longest sequential path (critical path):**
1. Phase 1 (2 weeks) → Phase 2 (1 week, after Decision 2) → Phase 3 (1.5 weeks) → Phase 4 (1.5 weeks, after Decision 3) → Phase 5 (1 week)
2. **Total Critical Path:** ~7-8 weeks (with overlapping work)

**Parallelizable Work:**
- Phase 2 and Phase 3 can overlap (after Phase 1 complete)
- Phase 5 testing can start during Phase 4 (write tests as skills are completed)
- Documentation can be written continuously (not blocking other work)

---

## Part 8: Success Criteria & Validation

### Success Metrics (from Spec)

| Metric | Target | Validation Method | Phase |
|--------|--------|-------------------|-------|
| SC-001: Installation & init < 5 min | 5 minutes | Manual walkthrough | Phase 1 |
| SC-002: /spek.prepare < 30s, 3+ items | 30s | Benchmark on sample project | Phase 2 |
| SC-003: /spek.plan spec + plan < 3 min | 3 minutes | Benchmark on sample feature | Phase 3 |
| SC-004: Ambiguity clarification interactive | 3 ambiguities max | Manual testing | Phase 3 |
| SC-005: /spek.implement context < 10s | 10s | Benchmark | Phase 4 |
| SC-006: Full task cycle < 30 min | 30 minutes | End-to-end test | Phase 4 |
| SC-007: /spek.conclude < 5 min | 5 minutes | Benchmark | Phase 4 |
| SC-008: Second feature reuses lessons | 3+ lessons | Integration test with 2 features | Phase 4-5 |
| SC-009: Generated docs valid Markdown | 100% valid | Automated lint check | Phase 5 |
| SC-010: No codebase structure changes | Zero changes | Validation during /spek.init | Phase 1 |
| SC-011: 40-60% token efficiency | Measured | Comparison test (with/without vault) | Phase 5 |
| SC-012: 80% feature completion rate | 80% | Validation with sample features | Phase 5 |

### Test Plan

**Unit Tests (Phase 1-4):**
- Vault load/write operations
- lat.md query interface
- SpecKit wrapper commands
- Context injection
- Decision parsing
- Progress tracking

**Integration Tests (Phase 4-5):**
- Vault + context integration
- SpecKit wrapper + context enrichment
- Full workflow: prepare → plan → implement → conclude
- Skills registration and invocation

**End-to-End Tests (Phase 5):**
- Complete project setup (spek init)
- Feature development (full 4-stage workflow)
- Multiple features (knowledge reuse across features)
- Error handling (missing dependencies, invalid specs, merge conflicts)

**Performance Tests (Phase 2, 5):**
- Vault loading (< 2s for 100+ entries)
- lat.md queries (< 1s per query)
- /spek.prepare execution (< 30s)
- Full workflow (< 2 hours wall-clock time)

**User Experience Tests (Phase 5):**
- Install flow (new user walkthrough)
- Error messages (clarity, actionability)
- Documentation completeness

---

## Part 9: Documentation Plan

### User-Facing Documentation

| Doc | Phase | Content | Audience |
|-----|-------|---------|----------|
| README.md | Phase 1 | Features, prerequisites, quick-start | End users |
| INSTALL.md | Phase 1 | Global + per-project installation | End users |
| WORKFLOW.md | Phase 4 | /spek.* command reference, examples | End users |
| VAULT.md | Phase 2 | Vault structure, format, querying | Maintainers |
| ARCHITECTURE.md | Phase 3 | System design, component interactions | Contributors |
| TROUBLESHOOTING.md | Phase 5 | Common issues, debug steps | End users |
| CONTRIBUTE.md | Phase 5 | Development setup, testing, contribution guidelines | Contributors |

### Developer Documentation

| Doc | Phase | Content |
|-----|-------|---------|
| Skill Reference (.github/agents/skills/spek-*/) | Phase 4 | Input, output, example for each skill |
| API Reference (docstrings in code) | Continuous | Class/function contracts, examples |
| Integration Guide (wiki/) | Phase 5 | How to integrate with other tools |

---

## Part 10: Known Unknowns & Clarification Checklist

**Before Phase 1 Starts (Decision Point 1):**

- [ ] **SpecKit API Stability** — Confirm SpecKit v0.9.6+ is stable; test wrapper command injection
- [ ] **lat.md MCP Interface** — Confirm MCP tools available (lat_files, lat_callers, lat_impact)
- [ ] **Obsidian CLI Export** — Test `obsidian export` command; verify output format
- [ ] **Agent Skill Invocation** — Confirm `/spek.*` can be registered as agent skills

**After Phase 1, Before Phase 2 (Decision Point 2):**

- [ ] **Vault Performance** — Measure vault load time with 100+ entries; must be < 2s
- [ ] **lat.md Performance** — Measure index build and query time; must be < 5s rebuild, < 1s query

**After Phase 4, Before Phase 5 (Decision Point 3):**

- [ ] **Agent Skill Registration** — Confirm `/spek.*` commands work in agent context
- [ ] **Context Injection** — Verify context reaches agent session correctly
- [ ] **Full Workflow** — Test prepare → plan → implement → conclude end-to-end

---

## Part 11: Handoff & Continuation

### Artifacts Created by This Plan

1. **IMPL_PLAN.md** — This document (detailed implementation roadmap)
2. **Task List** — 25-30 independent, prioritized tasks (Phase 1-5)
3. **Git Branch** — `001-complete-framework` (contains this plan and spec)
4. **Wiki Updates** — Architecture, decisions, patterns documented during execution

### Continuation Process

1. **Phase 1 Kickoff:** Resolve Decision Point 1 checklist; begin implementation
2. **Phase 1 → 2 Transition:** Resolve Decision Point 2 checklist; adjust scope if needed
3. **Phase 4 → 5 Transition:** Resolve Decision Point 3 checklist; confirm integration
4. **Phase 5 Completion:** All success metrics validated; framework ready for user adoption

### Success Definition

**Framework is complete when:**
- ✅ All 5 phases completed
- ✅ All 12 success criteria (SC-001 through SC-012) validated
- ✅ All functional requirements (FR-001 through FR-083) implemented
- ✅ All unit, integration, and end-to-end tests passing
- ✅ User documentation (README, INSTALL, WORKFLOW) complete and accurate
- ✅ Example project walk-through completed successfully
- ✅ Framework tested by sample users (internal team)
- ✅ Ready for public GitHub release

---

## Appendix: Reference Materials

### Related Documents

- **Feature Specification:** `specs/001-complete-framework/spec.md` (defining requirements, scenarios, acceptance criteria)
- **Architecture Document:** `wiki/architecture.md` (design pillars, component responsibilities, layering)
- **Decision Log:** `wiki/decision.md` (tooling choices: SpecKit, lat.md, Obsidian, Caveman)
- **Vision Document:** `wiki/vision.md` (problem statement, core solution, philosophy)
- **Setup Guide:** `wiki/setup.md` (installation & per-project initialization spec)

### External Tool Documentation

- **SpecKit:** https://github.com/github/speckit (specification & planning tool)
- **lat.md:** https://github.com/lat-md/lat-md (code indexing via MCP)
- **Obsidian CLI:** https://obsidian.md/help/cli (vault operations)
- **Caveman Skill:** Compression notation for agent outputs

### Glossary

- **Vault** — Git-backed Obsidian-style markdown directory storing decisions, patterns, lessons
- **Specification (Spec)** — Document defining feature user scenarios, requirements, success criteria
- **Plan** — Document defining architecture, technology stack, tasks, and dependencies
- **Task** — Independent, prioritized, testable unit of work from a plan
- **Decision** — Record of architectural/design choice with rationale and implications
- **Pattern** — Reusable solution or convention documented for future reference
- **Lesson** — Insight extracted from completed feature, stored in vault
- **Context** — Relevant code, decisions, patterns, docs loaded into agent session for task execution
- **Enrichment** — Adding vault context to SpecKit commands (decisions, patterns, code examples)
- **SpecKit Wrapper** — Spekificity layer that decorates SpecKit with context enrichment

---

**End of Implementation Plan**

*This plan is ready for task generation and implementation. All phases, dependencies, and success criteria are defined. Proceed to Phase 1 upon resolution of Decision Point 1.*
