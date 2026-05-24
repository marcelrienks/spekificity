# Implementation Roadmap


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Date:** 2026-05-20 | ---


## Dependencies & Blockers


## Hard Dependencies
- Python 3.11+
- SpecKit CLI (GitHub: github/spec-kit)
- Git (initialized project)
- `uv` package manager


## Soft Dependencies
- Obsidian (for vault editing; not required for CLI to work)
- lat.md MCP (can implement with simpler indexer first)


## References

- [Spekificity Vision](../vision.md)
- [Spekificity Architecture](../architecture.md)
- [Feature Development Workflow](../workflow.md)
- [SpecKit Integration Contract](110-speckit-integration-contract.md)
- [Test Suite Specification](141-test-suite-specification.md)

## Executive Summary

Spekificity specification is **COMPLETE AND READY FOR IMPLEMENTATION**. All architectural decisions, integration contracts, and workflow specifications have been documented and validated. Implementation can begin immediately following this roadmap.


## Readiness Checklist
Component | Status | Reference | -----------|--------|----------- | **Vision & Philosophy** | ✓ Complete | [vision.md](../vision.md), [intention.md](../intention.md) | **Architectural Design** | ✓ Complete | [architecture.md](../architecture.md) | **Workflow Definition** | ✓ Complete | [workflow.md](../workflow.md) | **Integration Contracts** | ✓ Complete | [110-speckit-integration-contract.md](110-speckit-integration-contract.md) | **Memory Architecture** | ✓ Complete | [030-memory-architecture.md](030-memory-architecture.md) through [032-enrichment-layer.md](032-enrichment-layer.md) | **Memory Architecture** | ✓ Complete | [030-memory-architecture.md](030-memory-architecture.md) through [032-enrichment-layer.md](032-enrichment-layer.md) — `Obsidian` + `obsidian` CLI are required for the vault operations described in this roadmap. | **lat.md Specification** | ✓ Complete | [050-latmd-setup-and-integration.md](050-latmd-setup-and-integration.md) through [057-graph-merge-integration.md](057-graph-merge-integration.md) | **Skill Specifications** | ✓ Complete | [100-prepare-command.md](100-prepare-command.md) through [105-spek-implement-workflow.md](105-spek-implement-workflow.md) | **Automation Workflow** | ✓ Complete | [120-spek-automate-workflow.md](120-spek-automate-workflow.md), [121-cli-orchestration.md](121-cli-orchestration.md) | **Testing & Validation** | ✓ Complete | [140-integration-validation-and-testing.md](140-integration-validation-and-testing.md), [141-test-suite-specification.md](141-test-suite-specification.md)
---


## Technology Stack Decision


## Language: Python 3.11+


**Rationale:**
- **SpecKit Ecosystem:** SpecKit CLI is Python-native; deep integration with `uv` package manager
- **Code Analysis:** AST-based parsing for lat.md support (ast, Pygments libraries mature)
- **CLI Framework:** Click or Typer for deterministic SpecKit orchestration
- **Obsidian CLI:** `Obsidian` and the `obsidian` CLI are required for the automated vault operations (sync/export/metadata extraction) described in this roadmap. The `setup.sh` installer verifies that the `obsidian` command is available in PATH and will print guidance to register the CLI if it is missing.
- **Performance:** Fast startup is a target; precise numeric performance targets are defined in implementation artifacts.
- **Dependency Management:** `uv` provides fast, reproducible environments
- **Observability:** Structured logging (loguru/structlog) for debugging agent handoffs

**Required Packages:**
```
uv, speckit, pygments, click, pydantic, sqlalchemy, gitpython, loguru
```


## Directory Structure


> Example moved to [Example: 200-implementation-roadmap-code-1.md](./examples/200-implementation-roadmap-code-1.md)


---


## Step-by-Step Implementation Plan


## Step 1: Project Scaffolding
**Deliverable:** Python project structure + `pyproject.toml` + entry point

**Tasks:**
- Create `pyproject.toml` with dependencies (SpecKit, Click, SQLAlchemy, etc.)
- Create `src/spekificity/` package structure
- Create `src/spekificity/cli/main.py` entry point
- Create `tests/` directory with initial test structure

**Success Criteria:**
- `uv pip install -e .` succeeds
- `spek --help` displays core commands (`prepare`, `context`, `plan`, `map`, `implement`, `post`, `lessons`)
- All imports resolve

**Spec Reference:** None (standard scaffolding)

---


## Step 2: Language Selection & Environment Setup
**Deliverable:** Confirmed Python 3.11+ with `uv` configured

**Tasks:**
- Verify Python 3.11+ installed
- Initialize `uv` in project
- Create `.python-version` pinning 3.11+
- Document setup in [setup.md](../setup.md) (update)
- Create `uv.lock` with reproducible dependencies

**Success Criteria:**
- `uv python --version` shows 3.11+
- `uv pip list` shows SpecKit, Click, SQLAlchemy
- `uv.lock` committed to repo

**Spec Reference:** None (environment setup)

---


## Step 3: CLI Scaffolding
**Deliverable:** 7 CLI commands wired to placeholder implementations

**Tasks:**
- Create `src/spekificity/cli/main.py` with Click CLI group
- Create 7 skill commands: `prepare`, `context`, `plan`, `map`, `implement`, `post`, `lessons`
- Each command has help text + placeholder implementation (prints status)
- Wire commands to their modules (`cli/prepare.py`, `cli/context.py`, etc.)
- Add `--help`, `--verbose`, `--dry-run` flags where applicable
- Test all commands display help + exit cleanly

**Success Criteria:**
- `spek prepare --help` shows help text
- `spek plan --help` shows help text
- All 7 commands callable and return ✓ status
- Error messages are user-friendly

**Spec Reference:** [121-cli-orchestration.md](121-cli-orchestration.md)

---


## Step 4: Core Skills Implementation (Phase 1–7)


## 4a. /spek.prepare (Workspace Setup)
**Deliverable:** multi-step workspace initialization

**Tasks:**
- Implement git verification (clean working tree, feature branch check)
- Implement feature name extraction/prompting
-- Implement lat.md freshness check
-- Implement conditional lat.md refresh (async call placeholder)
- Implement context loading via `/spek.context`
- Implement feature state tracking (create `.spek/current-feature.md`)
- Report ready status

**Success Criteria:**
- `spek prepare` validates git state ✓
- Feature name extracted from branch or prompted ✓
- Context loaded and session memory initialized ✓
- Returns ✓ quickly

**Spec Reference:** [100-prepare-command.md](100-prepare-command.md)


## 4b. /spek.context (Context Layer)
**Deliverable:** 3-layer context loading (user, session, repo)

**Tasks:**
- Load user memory from `vault/user/` (if exists)
- Load session memory from `vault/session/` (if exists)
- Load repo memory from `vault/repo/` + `vault/` + `wiki/`
- Load vault specs, decisions, lessons from `wiki/`
- Construct 3-layer context object (user → session → repo, precedence)
- Cache context for session (avoid re-reading)
- Expose context to downstream commands

**Success Criteria:**
- Context object contains user, session, repo layers ✓
- Vault specs loaded and deduplicated ✓
- Cache prevents redundant I/O ✓

**Spec Reference:** [030-memory-architecture.md](030-memory-architecture.md), [031-context-layer.md](031-context-layer.md), [032-enrichment-layer.md](032-enrichment-layer.md)


## 4c. /spek.plan (SpecKit Orchestration)
**Deliverable:** Orchestrated SpecKit workflow (specify → clarify → plan → analyze → tasks)

**Tasks:**
- Accept feature intent (natural language description)
- Call SpecKit `specify` → capture spec.md
- Optional: Call SpecKit `clarify` → enrich spec.md
- Call SpecKit `plan` → capture plan.md, data-model.md, contracts/
- Optional: Call SpecKit `analyze` → validate cross-artifact consistency
- Optional: Call SpecKit `remediate` → fix issues in-place
- Call SpecKit `tasks` → generate tasks.md
- Commit all artifacts to repo
- Return link to spec + plan

**Success Criteria:**
- Feature branch created with auto-numbering ✓
- spec.md generated with enrichment layers ✓
- plan.md with technical architecture ✓
- tasks.md with executable task list ✓
- All artifacts committed ✓

**Spec Reference:** [110-speckit-integration-contract.md](110-speckit-integration-contract.md), [102-post-command.md](102-post-command.md)

-#### 4d. /spek.map (lat.md Wrapper)
**Deliverable:** lat.md query interface + impact analysis

**Tasks:**
- Expose lat.md query tools: `symbols()`, `references()`, `definition()`, `impact()`
- Implement dependency graph visualization (ASCII/JSON output)
- Implement cross-file impact analysis (what breaks if this file changes?)
- Cache graph queries for session duration
- Support JSON + Markdown output formats

**Success Criteria:**
- `spek map --symbol MyClass` returns definition + references ✓
- `spek map --impact src/core.py` returns affected files ✓
- Output includes file:line + context ✓

**Spec Reference:** [050-latmd-setup-and-integration.md](050-latmd-setup-and-integration.md) through [057-graph-merge-integration.md](057-graph-merge-integration.md)


## 4e. /spek.implement (Execution Coordinator)
**Deliverable:** Context-aware implementation execution

**Tasks:**
- Load full context (vault, graph, memory)
- Read tasks.md from current feature branch
- Execute each task sequentially or in batches (configurable)
- Provide full context to each execution step (no context re-loading)
- Update feature state tracker after each task
- Capture implementation outputs (files modified, tests run, etc.)
- Return summary of completed tasks

**Success Criteria:**
- Context fully loaded before execution ✓
- Tasks executed with access to full context ✓
- Feature state tracker updated ✓
- Summary report generated ✓

**Spec Reference:** [105-spek-implement-workflow.md](105-spek-implement-workflow.md)


## 4f. /spek.conclude (Outcome Archival)
**Deliverable:** Feature completion + lesson extraction

**Tasks:**
- Verify feature is complete (all tasks done, tests pass)
- Extract lessons learned (decisions, patterns, anti-patterns)
- Commit lessons to vault (`wiki/lessons/`)
-- Update lat.md index (final refresh)
- Merge feature branch to main (or prompt user)
- Archive feature state to repo memory (`.spek/features/[feature-name]/`)
- Sync vault to origin (Obsidian git plugin)

**Success Criteria:**
- Lessons captured in vault ✓
- Feature state archived ✓
- Vault synced to origin ✓
- Branch merged or marked for merge ✓

**Spec Reference:** [102-post-command.md](102-post-command.md)


## 4g. /spek.lessons (Retrospective)
**Deliverable:** Pattern extraction + recommendation system

**Tasks:**
- Scan completed features in `.spek/features/` + `wiki/lessons/`
- Extract patterns (common decisions, libraries, anti-patterns)
- Identify reusable skill opportunities
- Generate recommendations for future features
- Output: Lessons summary (Markdown)

**Success Criteria:**
- Patterns extracted from ≥1 completed feature ✓
- Recommendations generated ✓
- Markdown report generated ✓

**Spec Reference:** [104-spek-lessons-command.md](104-spek-lessons-command.md)

---


## Step 5: lat.md MCP Setup
**Deliverable:** Indexed code analysis + real-time sync

**Tasks:**
- Design SQLite schema for code graph (nodes: symbols, files; edges: references, dependencies)
- Implement file indexer (AST-based for Python, regex-based for other languages)
- Implement graph sync (incremental update on file changes)
- Implement query engine (symbols, references, impact analysis)
- Wire MCP tools: `lat_symbols()`, `lat_references()`, `lat_impact()`, `lat_definition()`
- Setup auto-refresh on `/spek.prepare` or on-demand
- Add `--force-graph-refresh` flag to `/spek.prepare`

**Success Criteria:**
- SQLite schema defined ✓
- Indexer processes Python files (AST) ✓
- Queries return correct results ✓
- Graph refreshes within acceptable time ✓
- MCP tools callable from agent context ✓

**Spec Reference:** [050-latmd-setup-and-integration.md](050-latmd-setup-and-integration.md), [051-graph-storage-structure.md](051-graph-storage-structure.md), [052-node-schema-design.md](052-node-schema-design.md), [053-graph-refresh-strategy.md](053-graph-refresh-strategy.md), [054-graph-query-patterns.md](054-graph-query-patterns.md)

---


## Integration Validation & Testing


## Test Phases
Phase | What | Where | Success Criteria | -------|------|-------|------------------ | **Unit Tests** | Individual components (CLI, graph, vault, memory) | `tests/unit/` | Coverage adequate per module | **Integration Tests** | Multi-step workflows (prepare → context → plan) | `tests/integration/` | Full workflow succeeds ✓ | **E2E Tests** | Complete feature from intent → lessons | `tests/e2e/` | Feature completes end-to-end ✓

## Validation Checklist

- [ ] All CLI commands callable with `--help`
- [ ] Context loads without errors (user, session, repo layers)
- [ ] SpecKit orchestration produces artifacts (spec, plan, tasks)
- [ ] lat.md indexes code correctly
- [ ] `/spek.prepare` completes and returns ready status
- [ ] `/spek.implement` context includes full vault + graph
- [ ] Lessons extraction identifies multiple patterns
- [ ] Full feature workflow completes end-to-end

**Spec Reference:** [140-integration-validation-and-testing.md](140-integration-validation-and-testing.md), [141-test-suite-specification.md](141-test-suite-specification.md)

---


## Potential Blockers
- SpecKit API changes (mitigate: pin version in `pyproject.toml`)
- Large codebase indexing performance (mitigate: incremental indexing, caching)

---


## Success Metrics

Success criteria and numeric targets are defined in implementation artifacts and CI configuration. This roadmap avoids prescriptive numeric targets; implementation teams should define precise metrics (startup time, prepare execution, index refresh, end-to-end workflow duration, test thresholds) in their project CI/specs as appropriate.

---


## Timeline

Timeline and effort estimates are omitted from this specification. Implementation teams should create task-level estimates in their project management tooling.

---

## Next Steps

1. ✓ Confirm readiness (this document)
2. Start Step 2 → language + environment setup
3. Commit `pyproject.toml` + `uv.lock` to repo
4. Create PR: "feat: initialize Python project structure"

---

