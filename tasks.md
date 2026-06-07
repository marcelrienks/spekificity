# Spekificity Framework: Comprehensive Task List

**Status:** Ready for Phase 1 Execution  
**Generated:** 2026-06-07  
**Total Tasks:** 48 tasks across 5 phases  
**Estimated Effort:** 260-330K tokens (40-50 engineering hours)  
**Critical Path:** 7-8 weeks with parallelization

---

## Executive Summary

This task list implements the complete Spekificity framework from specification (in `specs/001-complete-framework/spec.md`) through production deployment. Tasks are:

- **Dependency-ordered**: Prerequisites always precede dependent tasks
- **Atomically scoped**: Each task completable in 1-4 hours, < 50 lines of code typically
- **Independently testable**: Acceptance criteria define verification strategy
- **Categorized**: [ARCH], [CODE], [TEST], [DOC], [CONFIG] for clarity
- **Prioritized**: P0 (blockers), P1 (critical path), P2 (unblocks others), P3 (polish)
- **Estimated**: Token usage for implementation provided

**Key Insights:**
- **Phase 1** (Core Infrastructure) is the foundation; no parallelization possible
- **Phases 2-3** can partially overlap after Phase 1 completion
- **Phase 4** requires Decision Point 1-3 validation before starting
- **Phase 5** testing can begin during Phase 4 implementation
- **Critical path** tasks (marked P0/P1) gate all downstream work

---

## Dependency & Execution Rules

### Task ID Format
```
[PHASE].[SEQUENCE] — T1.1, T1.2, ..., T2.1, T2.2, etc.
```

### Priority Definitions

- **P0 (Blocker)**: Task must complete before ANY other work can proceed; gates entire phase(s)
- **P1 (Critical Path)**: Task is in the longest dependency chain; delays here delay entire project
- **P2 (Unblocks)**: Task enables parallelization of subsequent tasks
- **P3 (Polish)**: Task improves UX, documentation, or code quality but doesn't block progress

### Parallelization Rules

Tasks with the same phase and no interdependencies can execute in parallel. See "Parallel Execution Examples" section for timing optimization.

---

## PHASE 1: CORE INFRASTRUCTURE (Weeks 1-2)

**Objective:** Build foundation: installation system, CLI, vault engine, type models  
**Deliverables:** Installable `spekificity` package with CLI and vault engine  
**Token Estimate:** 40-50K tokens  
**Completion Gate:** Installation works; `spek init` creates valid `.specify/` structure  
**No External Dependencies:** Phase 1 is independent (only verifies external tool availability)

---

### T1.1 [ARCH] [CONFIG] Design & Create Package Structure

**Priority:** P0 (blocker)  
**Depends On:** None  
**Estimated Tokens:** 2-3K  
**Estimated Hours:** 1-1.5

**Description:**
Create the root `spekificity/` Python package with all directories, `__init__.py` files, and module structure per IMPL_PLAN Part 2.1.

**Acceptance Criteria:**
- [ ] Directory structure matches Part 2.1 of IMPL_PLAN exactly
- [ ] All `__init__.py` files exist and are importable
- [ ] No circular imports; modules load without errors
- [ ] `pyproject.toml` exists with valid Python 3.11+ metadata

**Subtasks:**
1. Create `spekificity/` root and all subdirectories (cli/, core/, skills/, templates/, integrations/, tests/)
2. Create `__init__.py` files in each directory
3. Create `pyproject.toml` with basic metadata (no dependencies yet)
4. Create `spekificity/__main__.py` for CLI entry point
5. Verify package structure: `python -c "import spekificity; print(spekificity.__file__)"`

**References:**
- IMPL_PLAN Part 2.1: Package Structure
- wiki/architecture.md: Component layout

---

### T1.2 [CODE] [CONFIG] Implement `pyproject.toml` with Dependencies & Entry Points

**Priority:** P0 (blocker)  
**Depends On:** T1.1  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Define all project metadata, dependencies, and CLI entry points in `pyproject.toml`. This enables installation via `uv tool install`.

**Acceptance Criteria:**
- [ ] `pyproject.toml` contains all dependencies from IMPL_PLAN (SpecKit, lat.md, Obsidian CLI, Caveman, Pydantic, GitPython, markdown-hero)
- [ ] Dependencies are pinned to minimum compatible versions (no `>=` wildcards for critical tools)
- [ ] `[project.scripts]` entry point: `spek = spekificity.cli.main:main`
- [ ] `[project.optional-dependencies]` includes `dev` group (pytest, black, mypy)
- [ ] `python -m build` succeeds without errors
- [ ] `pip install -e .` installs the package in editable mode

**Subtasks:**
1. Define all dependencies with version pins (see IMPL_PLAN Part 1.3)
2. Create entry point: `spek` command → `spekificity.cli.main:main`
3. Add `[project.optional-dependencies]` for development
4. Test local installation: `pip install -e .`
5. Verify `spek --version` can be invoked

**References:**
- IMPL_PLAN Part 1.3: Dependency Analysis
- IMPL_PLAN Part 3.1: Installation & Dependency Resolution

---

### T1.3 [CODE] Implement `cli/main.py` — CLI Router & Help

**Priority:** P1 (critical path)  
**Depends On:** T1.2  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Create the main CLI entry point with command routing, `--help`, `--version`, and global options.

**Acceptance Criteria:**
- [ ] `spek --version` outputs semantic version string
- [ ] `spek --help` lists all available commands (install, init, prepare, plan, implement, conclude)
- [ ] Unknown commands produce helpful error messages
- [ ] Global flags (`--verbose`, `--color`) work across all commands
- [ ] Command routing dispatches to correct submodule (e.g., `spek init` → `cli/init.py`)

**Subtasks:**
1. Create Click/Typer CLI framework setup
2. Implement `--version` flag (read from `__version__` in `__init__.py`)
3. Implement `--help` and command listing
4. Create command dispatch logic
5. Test all commands show up in help

**References:**
- IMPL_PLAN Part 3.1: Installation & Dependency Resolution
- wiki/patterns.md: CLI design patterns (if documented)

---

### T1.4 [CODE] Implement `cli/install.py` — Dependency Verification & Auto-Install

**Priority:** P1 (critical path)  
**Depends On:** T1.3  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Verify system prerequisites (Python 3.11+, git, uv) and auto-install SpecKit, lat.md, Obsidian CLI if missing.

**Acceptance Criteria:**
- [ ] `spek install` checks Python version and fails gracefully if < 3.11
- [ ] `spek install` checks for git and uv; exits with install instructions if missing
- [ ] If SpecKit not found: runs `pip install speckit==0.9.6+` and verifies installation
- [ ] If lat.md not found: runs `pip install lat-md` and verifies installation
- [ ] Obsidian CLI check: warns if missing (non-blocking) with installation link
- [ ] Prints colored status report (✓ Python 3.11, ✓ git, ✓ SpecKit, etc.)
- [ ] Exit code 0 if all critical tools installed; non-zero if missing critical tool

**Subtasks:**
1. Implement Python version check (sys.version_info)
2. Implement `which` checks for git and uv
3. Implement auto-install logic for SpecKit (run `pip install`, check exit code)
4. Implement auto-install logic for lat.md
5. Implement Obsidian CLI warning (don't auto-install; provide link)
6. Implement colored output for status report
7. Test on clean system (or mock system state)

**References:**
- IMPL_PLAN Part 1.3: Dependency Analysis
- IMPL_PLAN Part 3.1: Installation & Dependency Resolution
- FR-002, FR-003, FR-004 from spec.md

---

### T1.5 [CODE] Implement `cli/init.py` — Per-Project Initialization

**Priority:** P1 (critical path)  
**Depends On:** T1.4  
**Estimated Tokens:** 6-7K  
**Estimated Hours:** 2-2.5

**Description:**
Create the `spek init` command that initializes `.specify/` structure in a Git-managed project directory.

**Acceptance Criteria:**
- [ ] `spek init` validates current directory is a Git repo (has `.git/`)
- [ ] Creates `.specify/` directory with subdirs: extensions/, integrations/, memory/, scripts/
- [ ] Creates `specs/` directory at project root
- [ ] Runs `speckit init .` to set up SpecKit in project (verifies SpecKit CLI works)
- [ ] Creates vault structure: `wiki/decisions.md`, `wiki/patterns.md`, `wiki/lessons.md`, `wiki/lessons/` dir
- [ ] Initializes lat.md index (runs `lat init`, creates `.lat/` directory)
- [ ] Creates skill definition files in `.github/agents/skills/spek-{prepare,plan,implement,conclude}/`
- [ ] Registers skills in `.github/copilot-instructions.md`
- [ ] Prints completion message: "✓ Initialized Spekificity in PROJECT_DIR; run `/spek.prepare FEATURE` to start"
- [ ] All created files are readable and valid (vault Markdown, YAML frontmatter, etc.)

**Subtasks:**
1. Check for `.git/` directory; exit if not a Git repo
2. Create `.specify/` with subdirectories
3. Create `specs/` directory
4. Run `speckit init .` and handle errors
5. Create vault skeleton (decisions.md, patterns.md, lessons.md)
6. Run `lat init` for lat.md indexing
7. Create `.github/agents/skills/` structure
8. Register skills in copilot-instructions.md
9. Verify all created files are valid
10. Test: `cd /tmp/test-project && git init && spek init && ls -la .specify/`

**References:**
- IMPL_PLAN Part 3.2: Per-Project Initialization
- IMPL_PLAN Part 2.2: Agent Skills Registration
- IMPL_PLAN Part 2.3: Vault Structure
- FR-005, FR-006, FR-007 from spec.md

---

### T1.6 [CODE] Create Vault Initialization Templates

**Priority:** P2 (unblocks vault operations)  
**Depends On:** T1.1  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Create Markdown templates for vault structure, constitution, spec, plan, and task generation. These are embedded in `spekificity/templates/` and used by `spek init` and `/spek.plan`.

**Acceptance Criteria:**
- [ ] `templates/vault_init.md` contains skeleton vault structure with YAML frontmatter examples
- [ ] `templates/constitution.md` is a default project constitution with sections: Vision, Principles, Governance, Constraints
- [ ] `templates/spec_template.md` has sections for: title, branch, user stories, requirements (FR-xxx), entities, success criteria, assumptions
- [ ] `templates/plan_template.md` has sections for: architecture, tech stack, sequencing, risks/mitigations, dependencies
- [ ] `templates/task_template.md` has format: [TaskID] [P?] [Story?] Description with file path, acceptance criteria, estimated tokens
- [ ] All templates are valid Markdown with proper frontmatter structure
- [ ] Templates are loadable by Python code (read as strings)

**Subtasks:**
1. Create `templates/vault_init.md` with example entries and structure
2. Create `templates/constitution.md` with default content (link to wiki/vision.md)
3. Create `templates/spec_template.md` with all sections from spec.md requirements
4. Create `templates/plan_template.md` with architecture, stack, sequencing, risks
5. Create `templates/task_template.md` with atomic task format
6. Test: verify all templates are loadable and render correctly

**References:**
- IMPL_PLAN Part 2.3: Vault Structure (Specification)
- IMPL_PLAN Part 3.2: Per-Project Initialization
- wiki/vault.md (if documented)

---

### T1.7 [CODE] Implement `core/types.py` — Pydantic Models for Spec, Plan, Task, Decision, Lesson

**Priority:** P1 (critical path)  
**Depends On:** T1.1  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2-3

**Description:**
Create Pydantic v2 data models for all artifact types (Spec, Plan, Task, Decision, Lesson). These models validate and serialize data across the framework.

**Acceptance Criteria:**
- [ ] `Spec` model has fields: title, branch, created, user_stories[], requirements[], entities[], success_criteria[], assumptions[]
- [ ] `Task` model has fields: id, title, description, priority (P0-P3), dependencies[], success_criteria[], estimated_tokens, estimated_hours, phase
- [ ] `Plan` model has fields: spec_branch, spec_file, tasks[], architecture, tech_stack[], risks[], sequencing
- [ ] `Decision` model has fields: id, title, status, date, rationale, implications[], alternatives[]
- [ ] `Lesson` model has fields: feature, date, outcomes, lessons[], patterns[], decisions[]
- [ ] All models have optional fields marked as Optional[...]
- [ ] Pydantic v2 validators where needed (e.g., priority must be P0-P3)
- [ ] Models can be serialized to/from JSON and Markdown
- [ ] `UserStory` model supports: priority, scenarios[], acceptance_criteria[], status
- [ ] `Entity` model supports: name, description, fields[], relationships[]

**Subtasks:**
1. Create base model imports and setup
2. Define `Entity` model (name, description, fields, relationships)
3. Define `SuccessCriteria` model (id, description, measurable)
4. Define `Assumption` model (id, description)
5. Define `UserStory` model (priority, scenarios, acceptance_criteria, status)
6. Define `Spec` model with all user story/requirement fields
7. Define `Task` model with priority, dependencies, tokens
8. Define `Plan` model with architecture, sequencing
9. Define `Decision` model with status, rationale, implications
10. Define `Lesson` model with feature, outcomes, lessons
11. Add validation tests: priority enum, task dependencies valid, etc.
12. Test serialization: Spec to JSON, Task to Markdown, etc.

**References:**
- IMPL_PLAN Part 2.4: Data Model & Type Contracts
- wiki/patterns.md: Type design patterns (if documented)

---

### T1.8 [CODE] Implement `core/vault.py` — Vault Engine (Load/Write/Query)

**Priority:** P1 (critical path)  
**Depends On:** T1.7  
**Estimated Tokens:** 7-9K  
**Estimated Hours:** 2.5-3

**Description:**
Create the vault engine: functions to load decisions, patterns, lessons from Markdown files; write new entries; update existing entries; query by intent (fallback to simple text match for now, lat.md search added in Phase 2).

**Acceptance Criteria:**
- [ ] `load_decisions()` reads `vault/decisions.md`, parses frontmatter, returns List[Decision]
- [ ] `load_patterns()` reads `vault/patterns.md`, parses frontmatter, returns List[Pattern]
- [ ] `load_lessons()` reads `vault/lessons/` directory and `lessons.md`, returns List[Lesson]
- [ ] `write_lesson(feature, outcomes, lessons)` appends to `vault/lessons.md` and creates timestamped lesson file
- [ ] `update_decision(id, status, rationale)` updates existing decision entry (idempotent)
- [ ] `query_decisions_text(keyword)` returns decisions matching keyword (simple text search for now)
- [ ] `export_vault()` returns complete vault as structured dict (for JSON export)
- [ ] All vault operations are idempotent (safe to call multiple times)
- [ ] Vault parsing handles frontmatter correctly (YAML block at top of file)
- [ ] Files created with consistent formatting (line endings, spacing)

**Subtasks:**
1. Create Markdown parser for frontmatter (YAML → Python dict)
2. Implement `load_decisions()` with frontmatter parsing
3. Implement `load_patterns()` with frontmatter parsing
4. Implement `load_lessons()` for both lessons.md and lessons/ directory
5. Implement `write_lesson()` with timestamp generation
6. Implement `update_decision()` with idempotency checks
7. Implement `query_decisions_text()` (keyword matching on title/rationale)
8. Implement `export_vault()` for structured export
9. Create tests: load/write cycle, frontmatter preservation, idempotency
10. Test with sample vault entries

**References:**
- IMPL_PLAN Part 2.3: Vault Structure (Specification)
- IMPL_PLAN Part 3.3: Vault Engine
- FR-050, FR-051, FR-053, FR-054 from spec.md

---

### T1.9 [TEST] Comprehensive Unit Tests for Phase 1 Components

**Priority:** P2 (unblocks verification)  
**Depends On:** T1.8  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2-3

**Description:**
Write comprehensive unit tests for CLI, package structure, vault engine, and type models.

**Acceptance Criteria:**
- [ ] Test file: `tests/test_cli.py` with tests for CLI routing, help, version
- [ ] Test file: `tests/test_vault.py` with tests for load/write operations
- [ ] Test file: `tests/test_types.py` with tests for model validation and serialization
- [ ] At least 80% code coverage for Phase 1 modules
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Fixtures created: sample vault structure, mock projects in `tests/fixtures/`
- [ ] Tests include edge cases: empty vault, invalid frontmatter, missing files

**Subtasks:**
1. Create `tests/fixtures/` with sample vault and project structures
2. Write `test_cli.py`: test version, help, command dispatch
3. Write `test_vault.py`: test load/write, frontmatter parsing, idempotency
4. Write `test_types.py`: test model validation, serialization, enums
5. Add coverage measurement: `pytest --cov=spekificity tests/`
6. Fix any coverage gaps
7. Test error cases: invalid input, missing files, malformed data

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- wiki/patterns.md: Testing patterns (if documented)

---

### T1.10 [DOC] Document Installation & Quick-Start in README

**Priority:** P3 (polish)  
**Depends On:** T1.4, T1.5  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Create user-facing README.md with feature overview, prerequisites, installation steps, and quick-start example.

**Acceptance Criteria:**
- [ ] README has sections: Features, Prerequisites, Installation, Quick-Start
- [ ] Installation section covers: `uv tool install spekificity`, global vs per-project
- [ ] Quick-Start shows: create test project, `git init`, `spek init`, `/spek.prepare`
- [ ] Prerequisites clearly list: Python 3.11+, git, uv, Obsidian CLI (optional)
- [ ] README distinguishes: end-state docs (what Spekificity will be) vs development docs (how to build it)
- [ ] Links to detailed documentation (when created in Phase 4-5)
- [ ] Code examples are valid and tested

**Subtasks:**
1. Write Features section (overview, 4 core components)
2. Write Prerequisites section (Python, git, uv, optional tools)
3. Write Installation section (global + per-project steps)
4. Write Quick-Start (walkthrough: init project, run /spek.prepare)
5. Add Contributing section (link to CONTRIBUTE.md, placeholder for now)
6. Add License section (link to LICENSE file)
7. Test: verify install instructions work on clean system

**References:**
- IMPL_PLAN Part 9: Documentation Plan
- FR-080, FR-081, FR-082, FR-083 from spec.md
- Existing README.md (if present)

---

## PHASE 2: VAULT + CODE INDEXING (Weeks 2-3)

**Objective:** Build vault querying, lat.md integration, context injection  
**Deliverables:** Vault semantic search, lat.md BM25 retrieval, context loading for tasks  
**Token Estimate:** 50-60K tokens  
**Completion Gate:** Context injection works; `load_feature_context()` returns relevant code + decisions + patterns  
**Dependencies:** All Phase 1 tasks complete; Decision Point 2 validation  
**Parallelization:** T2.1-T2.4 can run in parallel after T1.8 complete

---

### T2.1 [CODE] Implement `integrations/lat_md.py` — lat.md Index Integration

**Priority:** P1 (critical path)  
**Depends On:** T1.8  
**Estimated Tokens:** 7-8K  
**Estimated Hours:** 2.5-3

**Description:**
Create wrapper functions for lat.md MCP tools: index sync, BM25 file search, function search, impact analysis.

**Acceptance Criteria:**
- [x] `index_codebase()` runs `lat sync` to rebuild/update code index
- [x] `query_relevant_files(intent, scope)` returns List[filepath, relevance_score] via BM25 search
- [x] `query_functions(intent, scope)` returns List[function_name, file, signature] matching intent
- [x] `query_impact(file_path)` returns callers, dependencies, impact scope
- [x] `search_patterns(pattern_name)` finds code matching design pattern
- [x] All queries are scoped: can search "backend/" only, or "all" for full codebase
- [x] Queries timeout gracefully (fallback to semantic_search if lat.md takes > 5s)
- [x] Results are deduplicated and ranked by relevance
- [x] Integration with lat.md MCP tools confirmed (lat_files, lat_callers, lat_impact tools available)

**Subtasks:**
1. Verify lat.md MCP interface (check available tools, test simple query)
2. Implement `index_codebase()` — runs `lat sync`
3. Implement `query_relevant_files()` — calls lat_files MCP tool
4. Implement `query_functions()` — searches function definitions
5. Implement `query_impact()` — calls lat_impact MCP tool
6. Implement `search_patterns()` — pattern-based search
7. Add timeout handling with fallback to semantic_search
8. Add result deduplication and ranking
9. Test queries on sample codebase
10. Benchmark: measure query latency, ensure < 1s per query

**References:**
- IMPL_PLAN Part 1.4: Unknowns & Clarification Needed (lat.md MCP interface)
- IMPL_PLAN Part 3.4: Code Indexing (lat.md Integration)
- FR-060, FR-061, FR-062, FR-063, FR-064 from spec.md

---

### T2.2 [CODE] Implement `integrations/semantic_search.py` — Fallback Search

**Priority:** P2 (unblocks fallback)  
**Depends On:** T1.1  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Create fallback semantic search for when lat.md is unavailable or times out. Uses workspace semantic_search tool or simple grep-based matching.

**Acceptance Criteria:**
- [x] `semantic_search(query, scope)` uses workspace semantic_search tool if available
- [x] Falls back to grep-based keyword search if semantic_search unavailable
- [x] Returns List[filepath, line_number, context] of matches
- [x] Queries are scoped (by file pattern, directory)
- [x] Performance acceptable for typical codebases (< 10s for keyword search on 100K+ files)
- [x] Clearly marked as fallback (logging indicates lat.md unavailable, using fallback)

**Subtasks:**
1. Implement workspace semantic_search wrapper
2. Implement grep-based fallback (subprocess call with proper escaping)
3. Add scope filtering (by directory, file extension)
4. Add result deduplication
5. Add logging for fallback usage
6. Test both paths: with semantic_search available, without (fallback)

**References:**
- IMPL_PLAN Part 3.4: Code Indexing (lat.md Integration)
- FR-062 from spec.md

---

### T2.3 [CODE] Implement `core/context.py` — Feature Context Loading & Injection

**Priority:** P1 (critical path)  
**Depends On:** T1.8, T2.1  
**Estimated Tokens:** 8-10K  
**Estimated Hours:** 3-4

**Description:**
Create context injection engine: load relevant decisions, patterns, code files, and function signatures for a task. This is the heart of the "deterministic context" feature.

**Acceptance Criteria:**
- [x] `load_feature_context(feature_intent, scope)` returns FeatureContext object with:
  - relevant_decisions: List[Decision] from vault (top 5 most relevant)
  - relevant_patterns: List[Pattern] from vault
  - relevant_files: List[FileRef] from lat.md search
  - relevant_functions: List[FunctionRef] with signatures
  - impact_map: Dict[file] → callers, dependencies
- [x] `inject_context(context, format)` returns formatted context string (Markdown) for agent consumption
- [x] `compress_context(context)` uses Caveman skill to reduce token usage (optional compression)
- [x] Context ranking by relevance: decisions > patterns > code files > functions
- [x] Total injected context ≤ 50K tokens (or configurable limit)
- [x] All decisions include rationale and implications (not just titles)
- [x] Code snippets include line numbers and function signatures

**Subtasks:**
1. Define `FeatureContext` Pydantic model (decisions, patterns, files, functions, impact)
2. Implement `load_feature_context()` orchestration
3. Call vault.query_decisions_text() for relevant decisions
4. Call vault.load_patterns() and filter by relevance
5. Call index.query_relevant_files() for code context
6. Call index.query_functions() for function signatures
7. Call index.query_impact() to build impact map
8. Implement `inject_context()` — format as Markdown with sections
9. Implement `compress_context()` — call Caveman skill if enabled
10. Add token counting to verify context size < 50K

**References:**
- IMPL_PLAN Part 3.6: Context Injection
- wiki/patterns.md: Context design patterns (if documented)
- FR-030 from spec.md (context injection requirement)

---

### T2.4 [CODE] Implement Context Compression with Caveman Skill

**Priority:** P3 (polish, reduces token overhead)  
**Depends On:** T2.3  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Integrate Caveman skill for optional context compression to reduce token usage when context is large.

**Acceptance Criteria:**
- [x] `compress_context(context, intensity)` calls Caveman skill with appropriate intensity level
- [x] Intensity levels: lite, full (default), ultra correspond to Caveman modes
- [x] Compressed output is 40-60% of original token size (typical compression ratio)
- [x] Caveman-compressed context remains actionable (no loss of critical information)
- [x] Compression is optional (configurable via flag or environment variable)
- [x] Fallback to uncompressed context if Caveman unavailable (non-blocking)

**Subtasks:**
1. Implement Caveman skill invocation wrapper
2. Map intensity levels to Caveman modes
3. Implement token counting before/after compression
4. Add configuration flag for compression enable/disable
5. Add logging for compression statistics
6. Test compression on sample context

**References:**
- Skills: caveman (compression mode documentation)
- IMPL_PLAN Part 3.6: Context Injection

---

### T2.5 [TEST] Test lat.md Integration & Context Loading

**Priority:** P2 (unblocks Phase 3)  
**Depends On:** T2.1, T2.3  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Write comprehensive tests for lat.md queries, context loading, and injection.

**Acceptance Criteria:**
- [x] Test file: `tests/test_index.py` for lat.md queries
- [x] Test file: `tests/test_context.py` for context loading and injection
- [x] Tests for all query types: query_relevant_files, query_functions, query_impact
- [x] Tests for context loading: relevant decisions, patterns, files loaded correctly
- [x] Tests for context injection: Markdown format correct, no broken links
- [x] Tests for context compression: token reduction verified
- [x] At least 80% coverage for lat.md and context modules
- [x] Sample projects in fixtures with known code structure

**Subtasks:**
1. Create sample project fixture with known code structure
2. Create sample vault fixture with test decisions/patterns
3. Write tests for lat.md queries (with mocked lat.md if needed)
4. Write tests for context loading orchestration
5. Write tests for Markdown injection format
6. Write tests for compression (mock Caveman skill)
7. Write integration tests: index + context + vault
8. Measure coverage and fix gaps

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases

---

### T2.6 [TEST] Benchmark Vault & Index Performance

**Priority:** P2 (gating Phase 3 start)  
**Depends On:** T1.8, T2.1, T2.5  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Benchmark vault loading and lat.md queries to validate Decision Point 2 criteria: vault < 2s for 100+ entries, lat.md < 5s rebuild, < 1s query.

**Acceptance Criteria:**
- [ ] Vault loading test: 100 decision entries load in < 2 seconds
- [ ] lat.md sync (full rebuild) completes in < 5 seconds for typical codebase
- [ ] lat.md query (single intent) completes in < 1 second
- [ ] `/spek.prepare` end-to-end (load vault + index sync + navigation) completes in < 30 seconds
- [ ] Benchmark results logged: timings, bottlenecks identified
- [ ] If any benchmark fails: document mitigation plan (optimization, caching, etc.)

**Subtasks:**
1. Create benchmark harness: time vault loading with 100+ entries
2. Create benchmark: time lat.md full sync on sample codebase
3. Create benchmark: time lat.md query on various intents
4. Create benchmark: time `/spek.prepare` end-to-end
5. Log results to file (for trend tracking)
6. Analyze bottlenecks and document findings
7. If any fail SLA: propose optimization (caching, lazy loading, etc.)

**References:**
- IMPL_PLAN Part 6: Risk Assessment & Mitigation (vault/lat.md performance)
- Decision Point 2

---

### T2.7 [DOC] Document Code Indexing & Context in wiki/

**Priority:** P3 (polish)  
**Depends On:** T2.3  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Create documentation for code indexing strategy and context injection mechanism.

**Acceptance Criteria:**
- [ ] `wiki/indexing.md` documents: lat.md BM25 search, fallback semantic_search, scoped queries
- [ ] `wiki/context.md` documents: context loading flow, decision/pattern/code ranking, compression
- [ ] Both docs include examples and expected output
- [ ] Links to IMPL_PLAN and spec.md where applicable

**Subtasks:**
1. Write `wiki/indexing.md` with diagrams (ASCII or Mermaid)
2. Write `wiki/context.md` with flow and examples
3. Add references to decision points and patterns
4. Review for clarity and completeness

**References:**
- IMPL_PLAN Part 2: Implementation Architecture

---

## PHASE 3: SPECKIT ORCHESTRATION (Weeks 3-4)

**Objective:** Wrap SpecKit to inject context and generate specs, plans, tasks  
**Deliverables:** Spec/plan/task generation with enriched vault context  
**Token Estimate:** 50-60K tokens  
**Completion Gate:** `/spek.plan FEATURE_DESCRIPTION` generates valid spec + plan + tasks  
**Dependencies:** Phases 1-2 complete; Decision Point 1 validation (SpecKit API stability)  
**Parallelization:** T3.1-T3.4 can run in parallel after T2.3 complete

---

### T3.1 [CODE] Implement `core/speckit_wrapper.py` — SpecKit Command Orchestration

**Priority:** P1 (critical path)  
**Depends On:** T1.8, T2.3  
**Estimated Tokens:** 8-10K  
**Estimated Hours:** 3-4

**Description:**
Create wrapper functions for SpecKit commands: `run_specify()`, `run_plan()`, `run_implement()` with context enrichment injection.

**Acceptance Criteria:**
- [x] `run_specify(feature_intent, context)` calls `speckit specify` with enriched context (decisions, patterns from vault)
- [x] `run_plan(spec, context)` calls `speckit plan` with architecture context
- [x] `run_implement(plan, context)` calls `speckit implement` with task context
- [x] Enrichment injected via environment variables or input file (depends on SpecKit API)
- [x] Output parsed correctly: spec.md, plan.md, tasks.md extracted from SpecKit output
- [x] Error handling: if SpecKit call fails, returns clear error message with remediation
- [x] All SpecKit outputs validated for structure (required sections, frontmatter, etc.)

**Subtasks:**
1. Implement `run_specify()` — call SpecKit with feature intent + vault context
2. Implement `run_plan()` — call SpecKit with spec + architecture context
3. Implement `run_implement()` — call SpecKit with plan + task context (for reference)
4. Add context injection via environment variables
5. Add output parsing: extract spec.md, plan.md, tasks from SpecKit output
6. Add error handling with clear error messages
7. Test with sample feature descriptions
8. Verify SpecKit version compatibility (test with v0.9.6+)

**References:**
- IMPL_PLAN Part 3.5: SpecKit Orchestration
- Decision Point 1: SpecKit API stability

---

### T3.2 [CODE] Implement `integrations/speckit.py` — SpecKit Command Runners

**Priority:** P1 (critical path)  
**Depends On:** T1.4  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Create low-level SpecKit command runners: invoke `speckit specify`, `speckit plan`, `speckit analyze` commands.

**Acceptance Criteria:**
- [x] `invoke_specify(feature_intent, output_dir)` runs `speckit specify` in subprocess with args
- [x] `invoke_plan(spec_file, output_dir)` runs `speckit plan` with spec.md as input
- [x] `invoke_analyze(spec_file, output_dir)` runs `speckit analyze` for validation
- [x] All commands run in specified output directory (isolated from project root)
- [x] Environment variables can be passed to SpecKit (for context enrichment)
- [x] Return codes and stderr captured and raised as exceptions if non-zero
- [x] SpecKit CLI version checked before running commands (fail early if version wrong)

**Subtasks:**
1. Add SpecKit version check function
2. Implement `invoke_specify()` with subprocess.run
3. Implement `invoke_plan()` with subprocess.run
4. Implement `invoke_analyze()` with subprocess.run
5. Add environment variable passing
6. Add return code checking
7. Add stderr capture for error messages
8. Test all commands with sample inputs

**References:**
- IMPL_PLAN Part 3.5: SpecKit Orchestration
- IMPL_PLAN Part 1.3: Dependency Analysis (SpecKit version pinning)

---

### T3.3 [CODE] Implement Enrichment Layer — Inject Decisions & Patterns into SpecKit

**Priority:** P1 (critical path)  
**Depends On:** T2.3, T3.1  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Create enrichment layer that injects vault decisions and patterns as context input to SpecKit commands. This is critical for spec/plan generation to leverage prior knowledge.

**Acceptance Criteria:**
- [x] `enrich_specify_input(feature_intent, vault_context)` formats decisions, patterns as preamble to feature description
- [x] `enrich_plan_input(spec, decisions, patterns)` injects relevant decisions and patterns as architecture hints
- [x] Injected context does not change spec/plan structure (only augments content)
- [x] Enrichment data passed to SpecKit via environment variables or input file
- [x] All enriched inputs remain valid YAML/Markdown per SpecKit spec
- [x] Enrichment is optional: framework works without vault context (fallback)

**Subtasks:**
1. Design enrichment format (how to inject decisions into SpecKit input)
2. Implement `enrich_specify_input()` — prepend decisions summary to feature intent
3. Implement `enrich_plan_input()` — add architecture notes as context
4. Test enrichment: verify SpecKit accepts enriched input
5. Test fallback: verify SpecKit works with empty/minimal enrichment

**References:**
- IMPL_PLAN Part 3.5: SpecKit Orchestration
- IMPL_PLAN Part 3.6: Context Injection

---

### T3.4 [CODE] Implement Output Parsing — Extract Spec, Plan, Tasks from SpecKit

**Priority:** P1 (critical path)  
**Depends On:** T1.7, T3.1  
**Estimated Tokens:** 6-7K  
**Estimated Hours:** 2-2.5

**Description:**
Create output parser for SpecKit-generated spec.md, plan.md, and tasks from stdout/files. Parse Markdown and frontmatter into typed models.

**Acceptance Criteria:**
- [x] `parse_spec(markdown_text)` extracts Spec model from spec.md
- [x] `parse_plan(markdown_text)` extracts Plan model from plan.md
- [x] `parse_tasks(markdown_text)` extracts List[Task] from tasks list
- [x] Frontmatter YAML parsed into model fields correctly
- [x] All required fields present; error if missing with clear message
- [x] Markdown sections mapped to model fields (User Stories → user_stories[], etc.)
- [x] Parsed models can be re-serialized to Markdown identically (round-trip)

**Subtasks:**
1. Create Markdown parser for frontmatter and sections
2. Implement `parse_spec()` — extract user stories, requirements, entities, criteria, assumptions
3. Implement `parse_plan()` — extract architecture, stack, sequencing, risks
4. Implement `parse_tasks()` — extract task list with IDs, descriptions, dependencies
5. Add validation: all required fields present, enums valid
6. Test round-trip: parse + re-serialize = identical output
7. Test error cases: missing sections, invalid frontmatter

**References:**
- IMPL_PLAN Part 2.4: Data Model & Type Contracts
- IMPL_PLAN Part 3.5: SpecKit Orchestration

---

### T3.5 [CODE] Implement Validation Logic — Testability & Measurable Criteria Checks

**Priority:** P2 (unblocks downstream)  
**Depends On:** T1.7, T3.4  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Create validation functions to ensure specs and plans meet quality gates: testable requirements, measurable success criteria, clear task dependencies.

**Acceptance Criteria:**
- [x] `validate_spec(spec)` checks:
  - All requirements (FR-xxx) are testable (not vague, have measurable criteria)
  - Success criteria (SC-xxx) are measurable (quantifiable, observable)
  - User stories have clear acceptance scenarios
  - Assumptions documented for ambiguities
- [x] `validate_plan(plan)` checks:
  - All tasks are independent or dependencies clearly marked
  - Task ordering respects dependencies (no cycles)
  - Estimated hours/tokens reasonable (< 4 hours per task typically)
  - All requirements mapped to at least one task
- [x] Validation returns List[ValidationError] with clear messages and remediation hints
- [x] Framework can proceed with warnings but not errors

**Subtasks:**
1. Implement `validate_spec()` with individual checks (testability, measurable, etc.)
2. Add requirement testability check (regex for vague words: "should", "maybe", etc.)
3. Add success criteria measurability check (numeric thresholds, pass/fail criteria)
4. Implement `validate_plan()` with dependency checks
5. Add dependency cycle detection (DFS/topological sort)
6. Add task scope validation (hours/tokens)
7. Add requirement-to-task mapping validation
8. Test with sample specs and plans (valid and invalid)

**References:**
- IMPL_PLAN Part 3.5: SpecKit Orchestration
- spec.md: Requirements definitions (FR-020, FR-025, FR-026)

---

### T3.6 [TEST] Test SpecKit Wrapper & Enrichment Layer

**Priority:** P2 (unblocks Phase 4)  
**Depends On:** T3.1-T3.5  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Write comprehensive tests for SpecKit wrapper, enrichment, output parsing, and validation.

**Acceptance Criteria:**
- [x] Test file: `tests/test_speckit_wrapper.py` for wrapper orchestration
- [x] Test file: `tests/test_enrichment.py` for enrichment layer
- [x] Test file: `tests/test_output_parsing.py` for Markdown parsing
- [x] Test file: `tests/test_validation.py` for spec/plan validation
- [x] Tests include: happy path (valid spec generated), error handling (SpecKit fails), enrichment injection
- [x] Tests verify output is parsed into correct models
- [x] Tests for validation: spec with testable requirements passes, vague requirements fail
- [x] At least 80% code coverage
- [x] All tests pass: `pytest tests/test_speckit* -v`

**Subtasks:**
1. Create fixtures: sample feature descriptions, valid specs/plans, invalid specs
2. Write tests for `run_specify()` (mock SpecKit CLI)
3. Write tests for `run_plan()`
4. Write tests for enrichment injection
5. Write tests for output parsing (frontmatter, sections, round-trip)
6. Write tests for validation (testability checks, measurable criteria)
7. Write integration tests: feature → enrichment → SpecKit → parsing → validation
8. Measure and fix coverage gaps

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases

---

### T3.7 [TEST] Integration Test: Full Spec → Plan Workflow

**Priority:** P2 (gating Phase 4 start)  
**Depends On:** T3.6  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Write end-to-end integration test for complete spec → plan workflow: feature description through task list generation.

**Acceptance Criteria:**
- [x] Test file: `tests/test_e2e_spec_plan.py`
- [x] Test case: provide feature description → generate spec → generate plan → get tasks
- [x] Verify spec is valid Markdown with all required sections
- [x] Verify plan references spec and has architecture + sequencing
- [x] Verify tasks are independent, ordered by dependency, have IDs and descriptions
- [x] Verify vault decisions are consulted during generation (decisions appear in enrichment)
- [x] Full workflow completes in < 3 minutes (per SC-003 requirement)

**Subtasks:**
1. Create end-to-end test harness
2. Provide sample feature description
3. Run full workflow: specify → plan → task extraction
4. Verify outputs match expected structure
5. Verify timing < 3 minutes
6. Test with multiple feature descriptions to validate generalization

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- FR-020 through FR-026 from spec.md

---

## PHASE 4: AGENT SKILLS & WORKFLOW (Weeks 4-5)

**Objective:** Implement 4 core agent skills: prepare, plan, implement, conclude  
**Deliverables:** `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude` commands fully functional  
**Token Estimate:** 60-80K tokens  
**Completion Gate:** Full workflow (prepare → plan → implement → conclude) executable end-to-end  
**Dependencies:** Phases 1-3 complete; Decision Points 1-3 resolved  
**Parallelization:** T4.1-T4.4 can run in parallel after T3.6 complete

---

### T4.1 [CODE] Implement `skills/prepare.py` — /spek.prepare Skill

**Priority:** P1 (critical path)  
**Depends On:** T1.8, T2.3, T2.6  
**Estimated Tokens:** 7-8K  
**Estimated Hours:** 2.5-3

**Description:**
Implement `/spek.prepare` skill: loads vault context, indexes codebase, generates navigation guide for feature work.

**Acceptance Criteria:**
- [x] `/spek.prepare FEATURE_NAME` or `/spek.prepare --intent "description"` is the entry point
- [x] Validates git working directory is clean (or prompts for commit)
- [x] Loads vault decisions, patterns, lessons relevant to feature
- [x] Runs lat.md index sync (or uses cached index if recent)
- [x] Generates navigation guide: relevant files, prior decisions, patterns, file locations
- [x] Output is structured report (Markdown) with sections: Decisions, Patterns, Code Guide, Token Estimate
- [x] Completes in < 30 seconds (per SC-002)
- [x] Returns at least 3 actionable items (relevant context, file locations, patterns)
- [x] Estimates context token overhead for subsequent tasks

**Subtasks:**
1. Create entry point function `prepare(feature_name_or_intent, ...)`
2. Check git status (clean working directory)
3. Load vault decisions, patterns, lessons
4. Filter vault context by feature relevance (use semantic matching)
5. Run lat.md sync or load cached index
6. Generate navigation guide: code files, functions, patterns
7. Estimate token usage (count vault entries + code snippets)
8. Format report as Markdown
9. Test: verify < 30s execution, > 3 items returned

**References:**
- IMPL_PLAN Part 3.8: Agent Skills (`prepare.py`)
- FR-010 through FR-014 from spec.md
- SC-002 from spec.md (30s SLA)

---

### T4.2 [CODE] Implement `skills/plan.py` — /spek.plan Skill

**Priority:** P1 (critical path)  
**Depends On:** T3.1-T3.5  
**Estimated Tokens:** 8-10K  
**Estimated Hours:** 3-4

**Description:**
Implement `/spek.plan` skill: orchestrates SpecKit to generate spec, plan, tasks from feature description.

**Acceptance Criteria:**
- [x] `/spek.plan FEATURE_DESCRIPTION` is the entry point (or reference spec)
- [x] Accepts feature description as argument or reads from file
- [x] Calls SpecKit specify with enriched vault context (decisions, patterns)
- [x] Identifies ambiguities (max 3) and prompts developer for clarification (interactive)
- [x] Fills unambiguous gaps with documented assumptions
- [x] Generates spec.md with: user stories, requirements, entities, success criteria, assumptions
- [x] Calls SpecKit plan to generate plan.md with architecture, sequencing, risks
- [x] Validates spec and plan (testability, measurable criteria)
- [x] Generates tasks.md with independent, prioritized tasks
- [x] Output files written to `specs/` directory (feature branch)
- [x] Completes in < 3 minutes (per SC-003)
- [x] Developers can clarify ambiguities without re-running (interactive mode)

**Subtasks:**
1. Create entry point function `plan(feature_description, ...)`
2. Load enrichment context (vault decisions, patterns, code context)
3. Call SpecKit specify with enriched input
4. Parse spec output
5. Detect ambiguities (extract from SpecKit output or analyze programmatically)
6. Prompt for clarification (max 3 ambiguities)
7. Update spec with clarifications and assumptions
8. Call SpecKit plan with spec + architecture context
9. Parse plan output (architecture, sequencing, risks)
10. Validate spec and plan
11. Generate tasks from plan
12. Write outputs to `specs/feature_name/` (spec.md, plan.md, tasks.md)
13. Test: verify < 3 minutes, ambiguity prompts work, outputs valid

**References:**
- IMPL_PLAN Part 3.8: Agent Skills (`plan.py`)
- FR-020 through FR-026 from spec.md
- SC-003, SC-004 from spec.md

---

### T4.3 [CODE] Implement `skills/implement.py` — /spek.implement Skill

**Priority:** P1 (critical path)  
**Depends On:** T2.3, T4.4  
**Estimated Tokens:** 9-11K  
**Estimated Hours:** 3.5-4

**Description:**
Implement `/spek.implement` skill: executes a single task with context injection, progress tracking, and decision logging.

**Acceptance Criteria:**
- [x] `/spek.implement --task TASK_ID` is the entry point
- [x] Loads task from tasks.md (parses task definition)
- [x] Loads feature context: relevant decisions, patterns, code files, functions
- [x] Injects context into agent session (formatted as Markdown preamble)
- [x] Starts progress tracking (log created in `.specify/logs/TASK_ID.md`)
- [x] Executes task with agent (LLM generates code based on injected context)
- [x] Logs progress: task start, subtasks, decisions made, code changes
- [x] Captures decision annotations (e.g., `@decision "use pattern X because..."`)
- [x] Marks task complete when developer confirms
- [x] Generates task summary: changes made, decisions logged, estimated tokens used
- [x] Context injection completes in < 10s (per SC-005)
- [x] Full task cycle (start → implement → decide → log → mark complete) < 30 minutes (per SC-006, assuming well-scoped task)
- [ ] Progress visible in `.specify/logs/` with timestamps

**Subtasks:**
1. Create entry point function `implement(task_id, ...)`
2. Load task definition from tasks.md (parse task structure)
3. Load feature context via `context.load_feature_context(task_intent)`
4. Start progress log (create `.specify/logs/TASK_ID.md`)
5. Format context as Markdown preamble for agent
6. Inject context into agent session
7. Execute task (run agent with injected context + task description)
8. Log progress: task start, execution steps, decisions
9. Extract decision annotations from agent output
10. Mark task complete when developer confirms
11. Generate summary: code changes, decisions, token usage
12. Benchmark: context injection < 10s, full cycle < 30 min (with good task scope)

**References:**
- IMPL_PLAN Part 3.8: Agent Skills (`implement.py`)
- FR-030 through FR-036 from spec.md
- SC-005, SC-006 from spec.md

---

### T4.4 [CODE] Implement `skills/conclude.py` — /spek.conclude Skill

**Priority:** P1 (critical path)  
**Depends On:** T1.8, T4.3  
**Estimated Tokens:** 8-10K  
**Estimated Hours:** 3-4

**Description:**
Implement `/spek.conclude` skill: analyzes outcomes, extracts lessons, updates vault, refreshes project state.

**Acceptance Criteria:**
- [x] `/spek.conclude --feature FEATURE_NAME` is the entry point
- [x] Loads feature spec, plan, tasks, progress logs
- [x] Compares actual outcomes (completed tasks, code changes) vs success criteria
- [x] Extracts lessons learned: what went well, what to improve, patterns identified
- [x] Prompts developer to document lessons (interactive)
- [x] Writes lessons to vault: `vault/lessons/TIMESTAMP-feature.md` and `vault/lessons.md`
- [x] Updates vault decisions: new decisions or refinements based on implementation
- [x] Updates vault patterns: new or refined patterns identified
- [x] Exports feature summary: spec + plan + outcomes + lessons (Markdown)
- [x] Refreshes lat.md index (sync codebase after implementation)
- [x] Refreshes project state (update README references if needed)
- [x] Requires Obsidian CLI for vault export; graceful fallback if unavailable
- [x] Completes in < 5 minutes (per SC-007)
- [x] Second feature's `/spek.prepare` retrieves lessons from first feature (SC-008)

**Subtasks:**
1. Create entry point function `conclude(feature_name, ...)`
2. Load feature spec, plan, tasks, progress logs
3. Load success criteria from spec
4. Compare success criteria vs actual outcomes (completed tasks, code changes)
5. Extract lessons: call agent to analyze outcomes and generate lessons
6. Prompt developer for lesson documentation (interactive)
7. Write lessons to vault (timestamped file + lessons.md)
8. Update decisions in vault (new or refined)
9. Update patterns in vault (new or refined)
10. Export feature summary as Markdown
11. Call Obsidian CLI to export vault (if available)
12. Refresh lat.md index
13. Update project state (README, architecture docs)
14. Test: verify < 5 minutes, lessons written to vault, subsequent /spek.prepare retrieves lessons

**References:**
- IMPL_PLAN Part 3.8: Agent Skills (`conclude.py`)
- FR-040 through FR-045 from spec.md
- SC-007, SC-008 from spec.md

---

### T4.5 [CODE] Implement `core/progress.py` — Task Progress Tracking

**Priority:** P2 (unblocks implement skill)  
**Depends On:** T1.7  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Implement progress tracking for task execution: log creation, progress updates, rollback, completion.

**Acceptance Criteria:**
- [x] `start_task(task_id, task_description)` creates `.specify/logs/TASK_ID.md` with frontmatter
- [x] `log_progress(task_id, message, level)` appends timestamped progress entry to log
- [x] `mark_complete(task_id, summary)` adds completion entry with changes summary
- [x] `mark_rollback(task_id, reason)` rolls back task (archives log, restores previous state)
- [x] Progress logs have clear structure: frontmatter, progress entries with timestamps, decisions, final summary
- [x] All progress operations are idempotent (safe to call multiple times)

**Subtasks:**
1. Define progress log structure (frontmatter: task_id, start_time, status, etc.)
2. Implement `start_task()` — create log file with frontmatter
3. Implement `log_progress()` — append timestamped entries
4. Implement `mark_complete()` — add completion summary
5. Implement `mark_rollback()` — archive log, flag as rolled back
6. Add idempotency checks
7. Test: full progress cycle (start → log → complete)

**References:**
- IMPL_PLAN Part 3.7: Progress Tracking & Decision Logging

---

### T4.6 [CODE] Implement `core/decisions.py` — Decision Logging & Extraction

**Priority:** P2 (unblocks implement skill)  
**Depends On:** T1.7  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Implement decision logging and extraction: parse decision annotations from agent output, write to vault.

**Acceptance Criteria:**
- [x] `log_decision(task_id, title, rationale, implications)` creates Decision model and appends to vault
- [x] `extract_decisions(agent_output)` parses decision annotations (format: `@decision "..."` or `## Decision:` sections)
- [x] `write_decisions_to_vault(decisions)` appends to `vault/decisions.md` with frontmatter
- [x] Decisions are idempotent: same decision logged twice doesn't create duplicates
- [x] Decisions are traceable: reference task_id, date, author (from context)
- [ ] Extracted decisions are validated: status, rationale, implications present

**Subtasks:**
1. Implement `log_decision()` — create Decision model
2. Implement decision annotation parser (regex for `@decision` patterns)
3. Implement `extract_decisions()` — parse agent output for decisions
4. Implement `write_decisions_to_vault()` — append to decisions.md
5. Add idempotency check (avoid duplicate decisions)
6. Add validation (status enum, required fields)
7. Test: extract decisions from sample agent output, write to vault

**References:**
- IMPL_PLAN Part 3.7: Progress Tracking & Decision Logging
- FR-032 from spec.md

---

### T4.7 [CONFIG] Register Skills in Agent Context

**Priority:** P1 (critical path)  
**Depends On:** T1.5, T4.1-T4.4  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Register `/spek.*` skills in `.github/copilot-instructions.md` so they're available as agent commands in the IDE.

**Acceptance Criteria:**
- [ ] `.github/copilot-instructions.md` includes skill registrations for: /spek.prepare, /spek.plan, /spek.implement, /spek.conclude
- [ ] Each skill registration includes: command name, brief description, example usage
- [ ] Skills are discoverable: `/spek.` autocomplete suggests all 4 skills
- [ ] Skills are invocable: `/spek.prepare FEATURE` launches skill correctly
- [ ] Agent context includes skill input/output specifications (from skill definition files)

**Subtasks:**
1. Create skill registration syntax in copilot-instructions.md
2. Register /spek.prepare with input/output specs
3. Register /spek.plan with input/output specs
4. Register /spek.implement with input/output specs
5. Register /spek.conclude with input/output specs
6. Test: verify skills are discoverable and invocable in IDE

**References:**
- IMPL_PLAN Part 2.2: Agent Skills Registration
- `.github/copilot-instructions.md` (existing file)

---

### T4.8 [CONFIG] Create Skill Definition Files in .github/agents/skills/

**Priority:** P2 (documentation)  
**Depends On:** T4.1-T4.4  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Create skill definition files for each `/spek.*` command: input specification, output format, examples.

**Acceptance Criteria:**
- [ ] `.github/agents/skills/spek-prepare/_skill.md` defines: inputs (feature name), outputs (onboarding report), example
- [ ] `.github/agents/skills/spek-prepare/instructions.md` provides detailed agent instructions
- [ ] Same for spek-plan, spek-implement, spek-conclude
- [ ] All skill definitions follow consistent format
- [ ] Examples are concrete and runnable (walkthrough scenarios)
- [ ] Output specifications match actual skill outputs

**Subtasks:**
1. Create `.github/agents/skills/spek-prepare/_skill.md` with input/output/example
2. Create `.github/agents/skills/spek-prepare/instructions.md` with detailed steps
3. Repeat for spek-plan, spek-implement, spek-conclude
4. Review for consistency and accuracy
5. Test: verify instructions guide agent correctly

**References:**
- IMPL_PLAN Part 2.2: Agent Skills Registration
- `.github/agents/skills/` directory structure

---

### T4.9 [TEST] Manual End-to-End Workflow Test

**Priority:** P2 (validation)  
**Depends On:** T4.1-T4.8  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Manually test complete workflow: prepare → plan → implement → conclude on a sample feature.

**Acceptance Criteria:**
- [ ] Create sample project (git repo, .specify/ initialized)
- [ ] Run `/spek.prepare SAMPLE_FEATURE` — verify navigation guide generated, < 30s
- [ ] Run `/spek.plan FEATURE_DESCRIPTION` — verify spec + plan + tasks generated, < 3 min
- [ ] Select one task and run `/spek.implement --task T1` — verify context injected, task executes
- [ ] Implement task successfully (code changes made)
- [ ] Run `/spek.conclude --feature SAMPLE_FEATURE` — verify lessons extracted, vault updated, < 5 min
- [ ] Second feature's `/spek.prepare` retrieves lessons from first feature
- [ ] Entire workflow (start to finish) completes < 2 hours wall-clock time

**Subtasks:**
1. Create sample project with git repo
2. Run `spek init` in sample project
3. Manually run `/spek.prepare` and verify output
4. Manually run `/spek.plan` with test feature description
5. Manually run `/spek.implement` with test task
6. Implement task (write code)
7. Manually run `/spek.conclude` and verify vault updates
8. Verify second feature reuses lessons
9. Document any issues or refinements needed

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- SC-001 through SC-012 from spec.md

---

### T4.10 [TEST] Automated Integration Tests for Full Workflow

**Priority:** P2 (gating Phase 5)  
**Depends On:** T4.9  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Write automated integration tests for complete workflow: prepare → plan → implement → conclude.

**Acceptance Criteria:**
- [ ] Test file: `tests/test_e2e_workflow.py`
- [ ] Test case: create sample project, run full workflow, verify outputs
- [ ] Tests verify: spec generated, plan generated, tasks generated, context injected, lessons extracted
- [ ] Tests verify timing SLAs: < 30s prepare, < 3 min plan, < 30 min implement (mocked), < 5 min conclude
- [ ] Tests verify knowledge reuse: second feature reuses lessons from first
- [ ] All tests pass: `pytest tests/test_e2e_workflow.py -v`
- [ ] At least 90% code coverage for skills modules

**Subtasks:**
1. Create test fixture: sample project with .specify/ initialized
2. Write test case: /spek.prepare
3. Write test case: /spek.plan with feature description
4. Write test case: /spek.implement (mock agent, verify context injected)
5. Write test case: /spek.conclude
6. Write test case: knowledge reuse (second feature retrieves lessons)
7. Mock agent execution (don't require LLM) but verify context is passed
8. Measure coverage and fix gaps
9. Optimize test speed (use caching, fixtures)

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases

---

### T4.11 [DOC] Document Skills Usage & Examples in wiki/

**Priority:** P3 (polish)  
**Depends On:** T4.1-T4.8  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Create comprehensive documentation for `/spek.*` skills with usage examples, input/output specifications, troubleshooting.

**Acceptance Criteria:**
- [ ] `wiki/skills.md` documents all 4 skills: `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`
- [ ] Each skill has: description, inputs, outputs, example usage, expected timing
- [ ] `wiki/workflow.md` documents complete feature workflow with diagrams
- [ ] `wiki/troubleshooting.md` documents common issues and fixes
- [ ] All examples are concrete and runnable

**Subtasks:**
1. Write `wiki/skills.md` with all 4 skill descriptions and examples
2. Write `wiki/workflow.md` with workflow diagram (ASCII or Mermaid)
3. Write `wiki/troubleshooting.md` with common issues
4. Add links from README to skill documentation
5. Review for accuracy and clarity

**References:**
- IMPL_PLAN Part 9: Documentation Plan

---

## PHASE 5: INTEGRATION, POLISH, TESTING (Weeks 5-6)

**Objective:** Integrate all components, comprehensive testing, documentation, production readiness  
**Deliverables:** Production-ready Spekificity package with full documentation  
**Token Estimate:** 60-80K tokens  
**Completion Gate:** `uv tool install spekificity` works; full workflow executable on production projects  
**Dependencies:** All Phases 1-4 complete  
**Parallelization:** T5.1-T5.8 can run in parallel; T5.9-T5.13 sequential with validation gates

---

### T5.1 [CODE] Integrate Obsidian CLI Operations

**Priority:** P2 (unblocks vault export)  
**Depends On:** T1.4  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Create Obsidian CLI integration: vault export, graph generation, markdown validation.

**Acceptance Criteria:**
- [ ] `export_vault_obsidian(vault_path)` runs `obsidian export` command
- [ ] `generate_graph(vault_path)` generates project graph from vault files
- [ ] `validate_vault_markdown(vault_path)` validates vault structure (frontmatter, links, sections)
- [ ] All operations handle missing Obsidian CLI gracefully (warn, don't block)
- [ ] Exported vault is valid Markdown with correct link references

**Subtasks:**
1. Implement Obsidian CLI version check
2. Implement `export_vault_obsidian()` — runs obsidian export command
3. Implement `generate_graph()` — calls obsidian graph generation
4. Implement `validate_vault_markdown()` — validate frontmatter, links, sections
5. Add graceful fallback if Obsidian CLI missing
6. Test: verify exported vault is valid, links correct

**References:**
- IMPL_PLAN Part 3.9: Git Integration
- FR-044, FR-045 from spec.md

---

### T5.2 [CODE] Implement Git Integration

**Priority:** P2 (unblocks git workflow)  
**Depends On:** T1.4  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Create git integration: branch creation, auto-commit, merge, conflict handling.

**Acceptance Criteria:**
- [ ] `create_feature_branch(feature_name)` creates new branch with naming convention
- [ ] `auto_commit(message, scope)` stages and commits changes before major transitions
- [ ] `merge_feature(branch, strategy)` merges completed feature back to main (squash or standard)
- [ ] `view_commit_history(feature_name)` shows commits for feature
- [ ] `handle_merge_conflicts()` provides guidance for conflict resolution (doesn't auto-resolve)
- [ ] All git operations are safe: check for uncommitted changes before branching

**Subtasks:**
1. Implement `create_feature_branch()` with naming convention
2. Implement `auto_commit()` — stage and commit with message
3. Implement `merge_feature()` — merge with strategy option
4. Implement `view_commit_history()` — show commits for range
5. Implement merge conflict detection and guidance
6. Add safety checks: uncommitted changes before branch
7. Test: full git workflow on sample repo

**References:**
- IMPL_PLAN Part 3.9: Git Integration
- FR-070, FR-071, FR-072, FR-073 from spec.md

---

### T5.3 [CODE] Implement Comprehensive Error Handling Across All Components

**Priority:** P2 (unblocks user experience)  
**Depends On:** All Phase 1-4 code tasks  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Add comprehensive error handling to all components: informative error messages, remediation suggestions, no silent failures.

**Acceptance Criteria:**
- [ ] All exceptions are caught and re-raised with user-friendly messages
- [ ] Error messages include: what went wrong, why it happened, how to fix it
- [ ] Exit codes are meaningful: 0 for success, 1 for user error, 2 for system error
- [ ] CLI provides `--debug` flag for verbose error output (stack traces)
- [ ] Common errors documented: missing dependencies, git conflicts, invalid specs, etc.
- [ ] No silent failures: all errors are reported to user

**Subtasks:**
1. Create custom exception hierarchy (SpekificityError, ConfigError, VaultError, etc.)
2. Add error handling to CLI commands (try/except with user-friendly messages)
3. Add error handling to core modules (vault, index, context, etc.)
4. Add error handling to skills (prepare, plan, implement, conclude)
5. Add remediation suggestions to error messages
6. Add `--debug` flag for verbose output
7. Test: trigger common errors and verify messages are clear

**References:**
- IMPL_PLAN Part 5: Integration & Polish

---

### T5.4 [CODE] Add Comprehensive Logging Across All Components

**Priority:** P2 (unblocks debugging)  
**Depends On:** T5.3  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Add structured logging with configurable levels (debug, info, warning, error) throughout the codebase.

**Acceptance Criteria:**
- [ ] All modules use `logging` module with consistent format
- [ ] Default log level: info (important events, user-facing messages)
- [ ] Debug level: detailed execution flow, variable values, API calls
- [ ] Warning level: deprecated APIs, recoverable errors, fallbacks
- [ ] Error level: failures, exceptions, recovery attempts
- [ ] Logs written to `.specify/logs/spekificity.log` (with rotation)
- [ ] CLI supports `--verbose` and `--debug` flags to control logging
- [ ] Log format: `[TIMESTAMP] [LEVEL] [MODULE] MESSAGE`

**Subtasks:**
1. Set up logging configuration (logger, handlers, formatters)
2. Add logging to CLI commands (execution flow)
3. Add logging to core modules (vault, index, context, SpecKit calls)
4. Add logging to skills (prepare, plan, implement, conclude)
5. Add logging to integrations (lat.md, git, Obsidian CLI)
6. Implement log rotation (max file size, archive old logs)
7. Test: verify logs written correctly, levels controlled by flags

**References:**
- IMPL_PLAN Part 5: Integration & Polish

---

### T5.5 [TEST] Test Complete Installation Flow

**Priority:** P1 (gating Phase 5)  
**Depends On:** T1.4, T1.5, T5.3  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Test the complete installation flow: `uv tool install spekificity` on clean system.

**Acceptance Criteria:**
- [ ] Test on clean macOS system (or in Docker container)
- [ ] `uv tool install spekificity` completes without errors
- [ ] All dependencies auto-installed: SpecKit, lat.md, Obsidian CLI (with fallback)
- [ ] `spek --version` works
- [ ] `spek --help` lists all commands
- [ ] `spek install` verifies dependencies
- [ ] Installation < 5 minutes (per SC-001)

**Subtasks:**
1. Create clean test environment (VM or Docker)
2. Run `uv tool install spekificity` from repo
3. Verify all dependencies installed
4. Run `spek --version` and `spek --help`
5. Run `spek install` to verify setup
6. Time the entire installation flow
7. Document any issues or manual steps required

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- SC-001 from spec.md

---

### T5.6 [TEST] Test Per-Project Initialization Flow

**Priority:** P1 (gating Phase 5)  
**Depends On:** T1.5, T5.5  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Test the per-project initialization: `spek init` creates valid `.specify/` structure.

**Acceptance Criteria:**
- [ ] Create test project with git repo
- [ ] Run `spek init` in project directory
- [ ] Verify `.specify/` structure created correctly
- [ ] Verify vault files created (decisions.md, patterns.md, lessons.md)
- [ ] Verify lat.md index initialized
- [ ] Verify skill files created in `.github/agents/skills/`
- [ ] Verify `.github/copilot-instructions.md` updated
- [ ] Initialization < 2 minutes (part of SC-001 5-minute SLA)

**Subtasks:**
1. Create test project
2. Run `spek init` and capture output
3. Verify all directory structures
4. Verify all required files created
5. Verify file contents are valid (Markdown, YAML, etc.)
6. Time the initialization
7. Test multiple times to ensure idempotency

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- SC-001 from spec.md

---

### T5.7 [TEST] End-to-End Test: Feature from Prepare → Conclude

**Priority:** P1 (validation)  
**Depends On:** T4.10, T5.5, T5.6  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Comprehensive end-to-end test on production-like project: complete feature development from start to finish.

**Acceptance Criteria:**
- [ ] Test file: `tests/test_e2e_production.py`
- [ ] Create test project (similar to real project: multiple files, modules, tests)
- [ ] Run full workflow: init → prepare → plan → implement → conclude
- [ ] Verify all SLAs met:
  - SC-001: Installation + init < 5 min ✓
  - SC-002: /spek.prepare < 30s, 3+ items ✓
  - SC-003: /spek.plan spec + plan < 3 min ✓
  - SC-005: /spek.implement context < 10s ✓
  - SC-006: Full task cycle < 30 min ✓
  - SC-007: /spek.conclude < 5 min ✓
  - SC-008: Second feature reuses lessons ✓
  - SC-009: Generated docs valid Markdown ✓
- [ ] All outputs are valid, no errors

**Subtasks:**
1. Create realistic test project (Python package with modules, tests, docs)
2. Install Spekificity in test environment
3. Run `spek init` and verify success
4. Run `/spek.prepare` with feature name
5. Run `/spek.plan` with feature description
6. Select task and run `/spek.implement`
7. Implement task (write code)
8. Run `/spek.conclude`
9. Verify second feature reuses lessons
10. Document timing and any issues

**References:**
- IMPL_PLAN Part 4: Sequenced Implementation Phases
- SC-001 through SC-008 from spec.md

---

### T5.8 [TEST] Test Error Cases & Edge Conditions

**Priority:** P2 (robustness)  
**Depends On:** T5.3, T5.4  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Test error cases and edge conditions to ensure graceful handling and recovery.

**Acceptance Criteria:**
- [ ] Test missing dependencies: Python < 3.11, no git, no uv → clear error message
- [ ] Test missing SpecKit/lat.md → graceful fallback or clear install instruction
- [ ] Test git conflicts: feature branch conflicts with main → guidance provided
- [ ] Test invalid specs: vague requirements, unmeasurable criteria → validation error
- [ ] Test broken vault: malformed Markdown, missing frontmatter → error with remediation
- [ ] Test very large codebase: 100K+ files → /spek.prepare still < 30s (or documented timeout)
- [ ] Test offline mode: network unavailable → fallback to cached data
- [ ] All errors have clear messages and remediation steps

**Subtasks:**
1. Create test cases for each error condition
2. Test missing dependencies on clean system
3. Test invalid spec/plan/task inputs
4. Test git workflow edge cases (conflicts, uncommitted changes)
5. Test vault errors (malformed files, missing sections)
6. Test performance on large codebase (use sample large project)
7. Test offline scenarios
8. Document all error messages and remediation steps

**References:**
- IMPL_PLAN Part 5: Integration & Polish

---

### T5.9 [TEST] Performance Testing: Validate SLAs

**Priority:** P1 (gating Phase 5)  
**Depends On:** T2.6, T4.9, T5.7  
**Estimated Tokens:** 5-6K  
**Estimated Hours:** 2-2.5

**Description:**
Comprehensive performance testing to validate all SLA requirements from SC-002 through SC-007.

**Acceptance Criteria:**
- [ ] Benchmark: /spek.prepare < 30 seconds (SC-002)
- [ ] Benchmark: /spek.plan < 3 minutes (SC-003)
- [ ] Benchmark: /spek.implement context injection < 10 seconds (SC-005)
- [ ] Benchmark: Full task cycle < 30 minutes (SC-006, with well-scoped task)
- [ ] Benchmark: /spek.conclude < 5 minutes (SC-007)
- [ ] Benchmark: Full feature workflow < 2 hours wall-clock (prepare → conclude)
- [ ] Test on multiple project sizes: small (10K lines), medium (100K lines), large (1M+ lines)
- [ ] Document bottlenecks and optimization opportunities

**Subtasks:**
1. Create benchmark harness for each skill
2. Benchmark /spek.prepare on projects of various sizes
3. Benchmark /spek.plan on different feature descriptions
4. Benchmark /spek.implement context injection
5. Benchmark /spek.conclude on different project sizes
6. Benchmark full workflow end-to-end
7. Document results and identify bottlenecks
8. If any SLA fails: propose optimization (caching, lazy loading, etc.)

**References:**
- IMPL_PLAN Part 8: Success Criteria & Validation
- SC-002, SC-003, SC-005, SC-006, SC-007 from spec.md

---

### T5.10 [DOC] Write Comprehensive README

**Priority:** P2 (user documentation)  
**Depends On:** T5.5-T5.7  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Comprehensive, user-focused README documenting features, prerequisites, installation, quick-start, and examples.

**Acceptance Criteria:**
- [ ] README has clear sections:
  - What is Spekificity? (1-2 paragraphs)
  - Key Features (with benefits)
  - Prerequisites (Python, git, uv, optional tools)
  - Installation (global + per-project)
  - Quick-Start (walkthrough with `spek init` and `/spek.prepare`)
  - Workflow (4-stage prepare → plan → implement → conclude)
  - Examples (sample project walkthrough)
  - Documentation Links (to wiki/, skill reference, troubleshooting)
  - Contributing (link to CONTRIBUTE.md)
  - License (link to LICENSE)
- [ ] Distinguishes: end-state documentation (what Spekificity will be) vs development documentation (how to build it)
- [ ] Code examples are concrete, tested, and runnable

**Subtasks:**
1. Write introduction and value proposition
2. Write features list with benefits
3. Write prerequisites section
4. Write installation section (step-by-step)
5. Write quick-start (sample project walkthrough)
6. Write workflow diagram (ASCII or Mermaid)
7. Write example (sample feature through completion)
8. Add links to detailed docs
9. Review for clarity and completeness

**References:**
- IMPL_PLAN Part 9: Documentation Plan
- Existing README.md (if present)

---

### T5.11 [DOC] Write Skill Reference Documentation

**Priority:** P2 (user documentation)  
**Depends On:** T4.1-T4.11  
**Estimated Tokens:** 4-5K  
**Estimated Hours:** 1.5-2

**Description:**
Detailed documentation for each skill: input specification, output format, examples, expected timing, troubleshooting.

**Acceptance Criteria:**
- [ ] `wiki/skill-reference.md` or separate files for each skill:
  - `/spek.prepare`: inputs, outputs, examples, timing, troubleshooting
  - `/spek.plan`: inputs, outputs, examples, timing, troubleshooting
  - `/spek.implement`: inputs, outputs, examples, timing, troubleshooting
  - `/spek.conclude`: inputs, outputs, examples, timing, troubleshooting
- [ ] Each skill documentation includes:
  - Brief description (1-2 sentences)
  - Input specification (arguments, options)
  - Output specification (format, files created)
  - Expected timing (typical range, SLA)
  - Step-by-step example (walkthrough)
  - Common issues and solutions
- [ ] Examples are concrete and tested

**Subtasks:**
1. Write comprehensive documentation for /spek.prepare
2. Write comprehensive documentation for /spek.plan
3. Write comprehensive documentation for /spek.implement
4. Write comprehensive documentation for /spek.conclude
5. Create diagrams for skill inputs/outputs
6. Write troubleshooting section for each skill
7. Review for accuracy and completeness

**References:**
- IMPL_PLAN Part 9: Documentation Plan
- `.github/agents/skills/spek-*/`

---

### T5.12 [DOC] Create Example Project Walkthrough

**Priority:** P3 (polish)  
**Depends On:** T5.10, T5.11  
**Estimated Tokens:** 3-4K  
**Estimated Hours:** 1-1.5

**Description:**
Create detailed walkthrough of building a sample feature from scratch using Spekificity.

**Acceptance Criteria:**
- [ ] `docs/EXAMPLE.md` (or similar) contains:
  - Sample feature description (e.g., "Add user authentication")
  - Step-by-step walkthrough: init → prepare → plan → implement → conclude
  - Screenshots or output excerpts at each step
  - Explanations of what's happening and why
  - Links to detailed documentation for deeper learning
- [ ] Example is realistic and demonstrates all 4 skills
- [ ] Walkthrough completes in < 30 minutes of reading

**Subtasks:**
1. Choose realistic sample feature
2. Document initial project setup
3. Document /spek.prepare execution and output
4. Document /spek.plan execution and output
5. Document /spek.implement execution and output
6. Document /spek.conclude execution and output
7. Add explanations and insights at each step
8. Add screenshots or output excerpts
9. Review for clarity and completeness

**References:**
- IMPL_PLAN Part 9: Documentation Plan

---

### T5.13 [CODE] Refactor for Code Quality & Maintainability

**Priority:** P3 (polish)  
**Depends On:** T4.10, T5.4  
**Estimated Tokens:** 6-8K  
**Estimated Hours:** 2.5-3

**Description:**
Refactor code for clarity, consistency, maintainability: naming, docstrings, type hints, organization, style.

**Acceptance Criteria:**
- [ ] All functions have docstrings (description, args, returns, raises)
- [ ] All functions have type hints (input and output types)
- [ ] Code follows PEP 8 style (checked by black formatter)
- [ ] Type checking passes (mypy with strict mode)
- [ ] No cyclic imports or circular dependencies
- [ ] Code is DRY: no significant duplication
- [ ] Functions are focused: single responsibility
- [ ] Modules are organized: related functions grouped
- [ ] Constants are named and documented
- [ ] Code coverage remains > 80%

**Subtasks:**
1. Add comprehensive docstrings to all public functions
2. Add type hints to all functions (including internal)
3. Run black formatter and fix style issues
4. Run mypy and fix type errors
5. Check for circular imports (import order)
6. Refactor duplicated code into shared functions
7. Review function sizes (refactor long functions)
8. Review module organization (move related code together)
9. Document constants and configuration
10. Re-run tests and verify coverage

**References:**
- IMPL_PLAN Part 5: Integration & Polish

---

## PARALLEL EXECUTION EXAMPLES

### Phase 1 Parallelization

**Independent Tasks (can run in parallel):**
- T1.1 (Package structure) — prerequisite for all
- After T1.1: T1.2 (pyproject.toml), T1.6 (Templates), T1.7 (Types), T1.8 (Vault engine) can run in parallel
- T1.3 (CLI main) — requires T1.2
- T1.4 (Install verification) — requires T1.3
- T1.5 (spek init) — requires T1.4, T1.6, T1.7, T1.8
- T1.9 (Tests) — requires T1.8
- T1.10 (README) — requires T1.4, T1.5

**Critical Path (longest chain):** T1.1 → T1.2 → T1.3 → T1.4 → T1.5 (5 tasks, ~1 week)

**Recommended Schedule:**
- Day 1: T1.1 (4 hours)
- Day 2: T1.2, T1.6, T1.7 in parallel (3-4 hours each, can overlap)
- Day 3: T1.3 (2 hours), then T1.8 (2-3 hours parallel with T1.4)
- Day 4: T1.4 (2-3 hours), T1.5 (2-3 hours)
- Day 5: T1.9 (2-3 hours), T1.10 (1-2 hours)

### Phase 2 Parallelization

**Independent Tasks (after T1.8 complete):**
- T2.1 (lat.md), T2.2 (Semantic search), T2.4 (Caveman compression) can run in parallel
- T2.3 (Context loading) — requires T2.1, uses T2.2 as fallback
- T2.5 (Testing) — requires T2.1-T2.3
- T2.6 (Benchmarking) — requires T2.1, T2.5
- T2.7 (Documentation) — requires T2.3

**Recommended Schedule:**
- Days 1-2: T2.1, T2.2 in parallel (3-4 hours each)
- Day 2-3: T2.3 (3-4 hours, depends on T2.1 complete)
- Day 3-4: T2.4 (1-2 hours), T2.5 (2.5-3 hours) in parallel
- Day 4-5: T2.6 (2-2.5 hours), T2.7 (1.5-2 hours) in parallel

### Phases 2 & 3 Overlap

**After Phase 1 & T2.3 complete:**
- Phase 3 can begin (T3.1-T3.5 depend on Phase 2 context loading)
- Phase 2 testing/benchmarking can continue in parallel with Phase 3 implementation

---

## CRITICAL PATH ANALYSIS

**Longest sequential chain (gates the project):**

```
T1.1 → T1.2 → T1.3 → T1.4 → T1.5 → T1.8 → T2.1 → T2.3 → T3.1 → T4.1 → T5.7
(4h)    (1.5h)  (2h)  (2.5h) (2.5h) (3h)   (2.5h)  (3h)   (3h)   (2.5h)  (2.5h)
```

**Total Critical Path:** ~32 hours (4 weeks with 8-hour work days)

**Parallelizable Opportunities:**
- Phase 1: T1.6, T1.7 run parallel with T1.2-T1.4 → saves ~6 hours
- Phase 2: T2.1, T2.2 run parallel → saves ~2.5 hours
- Phase 3: T3.1-T3.5 can run in parallel (after T2.3) → saves ~4 hours
- Phase 4: T4.1-T4.4 can run in parallel (after T3.6) → saves ~4 hours
- Phase 5: T5.1-T5.8 can run in parallel → saves ~10 hours

**Total with Parallelization:** ~15-18 weeks actual elapsed time (vs 32 weeks pure sequential)

---

## SUCCESS METRICS & VALIDATION

### Phase Completion Criteria

**Phase 1 Complete When:**
- [ ] Package installs via `uv tool install spekificity` ✓
- [ ] `spek --version` and `spek --help` work ✓
- [ ] `spek init` creates valid `.specify/` structure ✓
- [ ] Vault engine (load/write) works ✓
- [ ] Phase 1 tests pass (80%+ coverage) ✓

**Phase 2 Complete When:**
- [ ] lat.md integration works (queries return results) ✓
- [ ] Context loading works (decisions + patterns + code injected) ✓
- [ ] Performance SLAs met (vault < 2s, lat.md < 1s query) ✓
- [ ] Phase 2 tests pass (80%+ coverage) ✓

**Phase 3 Complete When:**
- [ ] `/spek.plan FEATURE` generates valid spec + plan + tasks ✓
- [ ] Output parsing works (Markdown → typed models) ✓
- [ ] Validation works (testability checks pass) ✓
- [ ] Phase 3 tests pass (80%+ coverage) ✓

**Phase 4 Complete When:**
- [ ] All 4 skills implemented (`/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`) ✓
- [ ] Skills registered and discoverable in agent context ✓
- [ ] Full workflow (prepare → conclude) executes end-to-end ✓
- [ ] Phase 4 tests pass (90%+ coverage) ✓

**Phase 5 Complete When:**
- [ ] All SLAs validated (SC-001 through SC-012) ✓
- [ ] All error cases handled gracefully ✓
- [ ] Comprehensive documentation complete (README, skills, examples) ✓
- [ ] All tests pass (90%+ coverage) ✓
- [ ] Code quality standards met (PEP 8, type hints, docstrings) ✓

---

## RISK MITIGATION & CONTINGENCY

### High-Risk Items & Mitigations

**Risk: SpecKit API Instability**
- **Probability:** Medium | **Impact:** High
- **Mitigation:** Pin version in pyproject.toml; add version checks before using API; test early in Phase 3
- **Contingency:** If API breaks, implement lighter wrapper or fork SpecKit locally
- **Decision Point:** Before Phase 3 starts (Decision Point 1)

**Risk: lat.md MCP Interface Unavailable**
- **Probability:** Medium | **Impact:** High
- **Mitigation:** Verify MCP tools available before Phase 2; implement fallback semantic_search
- **Contingency:** If lat.md unavailable, disable code indexing or use grep-based search (slower)
- **Decision Point:** Before Phase 2 starts (Decision Point 2)

**Risk: Agent Skill Invocation Fails**
- **Probability:** Medium | **Impact:** High
- **Mitigation:** Test skill registration early in Phase 4; coordinate with agent team
- **Contingency:** If skills don't work, implement CLI entry points instead (no IDE integration)
- **Decision Point:** Before Phase 4 starts (Decision Point 3)

**Risk: Performance at Scale**
- **Probability:** Low | **Impact:** Medium
- **Mitigation:** Benchmark in Phase 2; optimize if needed (caching, lazy loading)
- **Contingency:** If /spek.prepare exceeds 30s, implement incremental indexing or project scoping
- **Decision Point:** After Phase 2 benchmark (Decision Point 2)

---

## DECISION POINTS & GATES

### Decision Point 1: Dependency Verification (Pre-Phase 1)

**Required Actions:**
1. Verify SpecKit v0.9.6+ is stable and supports wrapper injection
2. Verify lat.md MCP tools available (lat_files, lat_callers, lat_impact)
3. Verify Obsidian CLI export functionality works
4. Confirm agent skill registration mechanism

**Blockers:**
- If SpecKit API unstable → Phase 3 plan changes
- If lat.md unavailable → fallback semantic_search only
- If Obsidian CLI non-functional → manual vault export only
- If skill registration fails → CLI-only interface

**Decision Owner:** Architect  
**Timeline:** Before Phase 1 implementation starts  
**Impact:** May affect scope of Phases 2-4

---

### Decision Point 2: Performance Validation (Phase 1→2 Boundary)

**Required Actions:**
1. Measure vault loading time (target: < 2s for 100+ entries)
2. Measure lat.md sync time (target: < 5s for full rebuild)
3. Measure lat.md query time (target: < 1s per query)
4. Measure /spek.prepare end-to-end (target: < 30s)

**Blockers:**
- If vault > 2s → may need caching or optimization
- If lat.md > 5s → may need incremental sync
- If /spek.prepare > 30s → may need scoping or parallelization

**Decision Owner:** Tech Lead  
**Timeline:** After Phase 1 complete  
**Impact:** May affect Phase 2 design (caching, optimization)

---

### Decision Point 3: Workflow Validation (Phase 4→5 Boundary)

**Required Actions:**
1. Validate agent skill invocation works (register /spek.* commands)
2. Test context injection into agent session
3. Confirm full workflow (prepare → plan → implement → conclude) end-to-end

**Blockers:**
- If skill invocation fails → may need CLI-only interface
- If context injection fails → agent won't have proper context
- If workflow fails end-to-end → may need redesign of skill orchestration

**Decision Owner:** Integrations Lead  
**Timeline:** After Phase 4 implementation  
**Impact:** May affect Phase 5 scope (user experience improvements needed)

---

## TRACKING & PROGRESS REPORTING

### How to Use This Task List

1. **For Execution:** Work through tasks in order, respecting dependencies
2. **For Parallelization:** Group independent tasks and execute simultaneously
3. **For Tracking:** Mark tasks complete as work finishes; update "Progress Summary" section
4. **For Reporting:** Generate weekly status: # tasks complete, # in progress, # blocked, SLAs met

### Progress Summary Template

```
## Weekly Progress (Week X)

**Completed:** T1.1, T1.2, T1.3 (3 tasks)
**In Progress:** T1.4, T1.6, T1.7 (3 tasks, 50% complete)
**Blocked:** None
**Total Complete:** 3/48 (6%)
**Completion Rate:** 3 tasks/week (on track for 8+ weeks)

**SLA Status:**
- SC-001: Not yet validated (gated on Phase 1 completion)
- SC-002: Not yet validated (gated on Phase 2 completion)
... (more SLAs)

**Risks & Mitigations:**
- SpecKit API stability: TBD (Decision Point 1 pending)
- lat.md availability: Verified ✓

**Next Week's Goals:**
- Complete T1.4-T1.10 (core infrastructure)
- Begin Phase 2 (vault querying, lat.md integration)
- Resolve Decision Point 1 (dependency verification)
```

---

## APPENDIX: TASK SUMMARY BY PHASE

| Phase | Count | Tokens | Weeks | Critical Path | Gate |
|-------|-------|--------|-------|---|---|
| **Phase 1** | 10 | 40-50K | 1-2 | T1.1→T1.2→T1.3→T1.4→T1.5 | `spek init` works |
| **Phase 2** | 7 | 50-60K | 1-2 | T2.1→T2.3→(Phase 3) | Context loading works |
| **Phase 3** | 7 | 50-60K | 1-2 | T3.1→(Phase 4) | `/spek.plan` works |
| **Phase 4** | 11 | 60-80K | 1.5-2 | T4.1-T4.4→T4.9-T4.10 | Full workflow works |
| **Phase 5** | 13 | 60-80K | 1-2 | T5.9→T5.13 | Production ready |
| **TOTAL** | **48** | **260-330K** | **5.5-8** | ~32h sequential, ~15-18w parallel | SC-001 through SC-012 ✓ |

---

**End of Task List**

Generated: 2026-06-07  
Last Updated: 2026-06-07  
Version: 1.0

