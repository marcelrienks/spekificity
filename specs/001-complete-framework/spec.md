# Feature Specification: Complete Spekificity Framework

**Feature Branch**: `001-complete-framework`

**Created**: 2026-06-07

**Status**: Draft

**Input**: Comprehensive system architecture and requirements documented in user request

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Onboard to Feature & Load Prior Context (Priority: P1)

A developer starts work on a new feature. They run `/spek.prepare` to onboard themselves. The command loads prior architectural decisions, design patterns, and lessons learned from the project vault, indexes the current codebase state via lat.md, and generates a navigation guide tailored to the feature intent.

**Why this priority**: This is the foundation of the entire framework. Without context loading and code indexing, all downstream workflows are ineffective. Enabling developers to resume work without re-reading the codebase is the primary value proposition.

**Independent Test**: Can be tested independently by running `/spek.prepare` on a feature description and verifying that:
  - Prior decisions from vault are loaded and presented
  - Codebase is indexed via lat.md with BM25 retrieval
  - Navigation guide is generated with file paths and rationales

**Acceptance Scenarios**:

1. **Given** a developer on a new feature branch, **When** they run `/spek.prepare FEATURE_NAME`, **Then** they receive:
   - A structured onboarding report listing prior decisions, patterns, and relevant codebase sections
   - An indexed context map showing the current code state
   - A navigation guide for files they'll likely need

2. **Given** a developer who has worked on this project before, **When** they run `/spek.prepare`, **Then** the vault-loaded prior decisions help them avoid repeating mistakes or second-guessing earlier architectural choices

---

### User Story 2 - Generate Specification, Clarify Ambiguities, Plan Implementation (Priority: P1)

A developer has a feature intent (narrative description). They run `/spek.plan` to convert that intent into a formal specification, clarify ambiguities, and generate a high-level implementation plan with task breakdown. The command produces a spec.md, a plan.md, and a tasks.md that can be executed sequentially.

**Why this priority**: Deterministic planning is the second pillar of Spekificity. Without a clear spec and plan, implementation is ad hoc. This workflow enforces clarity before coding.

**Independent Test**: Can be tested independently by providing a feature description and verifying that:
  - A testable, unambiguous spec.md is generated
  - Ambiguities are flagged for clarification or resolved with documented assumptions
  - A plan.md with architecture and sequencing is generated
  - A tasks.md with independent, prioritized tasks is generated

**Acceptance Scenarios**:

1. **Given** a feature description with ambiguities, **When** `/spek.plan` runs, **Then** it:
   - Identifies ambiguities (max 3) and asks the developer to clarify
   - Fills unambiguous gaps with reasonable defaults documented in Assumptions
   - Produces a spec.md ready for implementation

2. **Given** an approved spec.md, **When** `/spek.plan` continues, **Then** it:
   - Generates a plan.md with architecture, tech stack, and sequencing
   - Produces a tasks.md with independently testable tasks
   - Each task can be developed, tested, and deployed without waiting for others

---

### User Story 3 - Execute Tasks with Persistent Progress Tracking (Priority: P1)

A developer begins implementation. They run `/spek.implement --task TASK_ID` to execute a single task from the task list. The command injects relevant context (vault decisions, prior patterns, code examples) directly into the agent session, tracks progress, logs decisions made, and updates the vault upon task completion.

**Why this priority**: Implementation is where the framework delivers value. Without persistent tracking and decision logging, the developer loses context between sessions and the vault stagnates. This workflow ensures no decision is lost.

**Independent Test**: Can be tested independently by executing a single task and verifying that:
  - Relevant context is injected (decisions, patterns, code examples)
  - Progress is tracked and visible
  - Decisions made during implementation are logged to vault
  - Task can be marked complete or rolled back consistently

**Acceptance Scenarios**:

1. **Given** a task from the task list, **When** `/spek.implement --task TASK_ID` runs, **Then**:
   - Relevant files, decisions, and patterns are loaded into context
   - The developer can execute the task with minimal context switching
   - Progress is tracked in a persistent log

2. **Given** a developer who encounters a design decision during implementation, **When** they log it (e.g., `@decision ...`), **Then**:
   - The decision is captured in the vault
   - It becomes available to future `/spek.prepare` runs
   - It prevents future contributors from reconsidering the same trade-off

---

### User Story 4 - Analyze Outcomes, Extract Lessons, Update Vault (Priority: P2)

After implementation is complete, a developer runs `/spek.conclude` to analyze what was built, extract lessons learned, update the vault with new patterns or decisions, and refresh the project state for the next feature. This ensures knowledge compounds over time.

**Why this priority**: P2 because it's critical for long-term project health but not required for a single feature to be complete. It prevents knowledge loss and enables future features to benefit from what was learned.

**Independent Test**: Can be tested independently by running `/spek.conclude` after a task and verifying that:
  - Outcomes are analyzed against success criteria
  - Lessons are extracted and written to vault
  - New patterns are identified and catalogued
  - Project state is refreshed for the next feature

**Acceptance Scenarios**:

1. **Given** completed implementation, **When** `/spek.conclude` runs, **Then**:
   - Actual outcomes are compared to success criteria
   - Lessons are written to vault as decision updates or new patterns
   - Project graph is refreshed for future reference

2. **Given** a second feature built after the first, **When** `/spek.prepare` runs for the second feature, **Then**:
   - Lessons from the first feature are available and consulted
   - The developer benefits from prior experience without re-learning

---

### User Story 5 - Install Spekificity Globally & Initialize Per-Project (Priority: P1)

A new user wants to adopt Spekificity for their project. They run `uv tool install spekificity` to install globally (which auto-installs SpecKit and lat.md), then `spek init` in their project directory to initialize the `.specify/` folder structure. Upon completion, all `/spek.*` commands are available and functional in their project.

**Why this priority**: Without installation and initialization, users can't use the framework. This is the entry point.

**Independent Test**: Can be tested independently by:
  - Installing on a clean system with Python 3.11+, uv, and git
  - Running `uv tool install spekificity`
  - Verifying all dependencies are auto-installed
  - Running `spek init` in a test project
  - Verifying `/spek.*` commands are available

**Acceptance Scenarios**:

1. **Given** a developer with Python 3.11+, uv, and git, **When** they run `uv tool install spekificity`, **Then**:
   - Spekificity is installed globally
   - SpecKit and lat.md are auto-installed if not present
   - Obsidian CLI requirement is noted with installation link
   - All tools are available in PATH

2. **Given** an initialized project, **When** a developer runs `spek prepare FEATURE`, **Then**:
   - `/spek.prepare` executes with full context loading and code indexing
   - The framework is immediately productive

---

### Edge Cases

- What happens when lat.md indexing times out or fails? (Fall back to semantic_search or direct code navigation)
- How does the framework handle very large codebases (100K+ files)? (Scoped indexing by feature-specific file patterns)
- What happens if the Obsidian CLI is not installed when `/spek.conclude` runs? (Alert user, offer manual fallback or skip vault export)
- What happens when a developer runs `/spek.implement` without a completed plan? (Require plan completion first, prompt user to run `/spek.plan`)
- How does the framework handle merge conflicts or branch conflicts during task execution? (Provide conflict resolution guidance, allow user to resolve manually, resume task)

## Requirements *(mandatory)*

### Functional Requirements

#### Installation & Initialization
- **FR-001**: `spekificity` MUST be installable via `uv tool install` from the public GitHub repository
- **FR-002**: Installation MUST auto-install SpecKit (v0.9.6+) and lat.md globally if not already present
- **FR-003**: Installation MUST verify Python 3.11+, git, and uv are available
- **FR-004**: Installation MUST warn if Obsidian CLI is not found (required for `/spek.conclude`)
- **FR-005**: `spek init` MUST initialize the `.specify/` folder structure in the target project directory with templates, extensions, integrations, and memory subdirectories
- **FR-006**: `spek init` MUST create a default constitution.md and init-options.json with reasonable defaults
- **FR-007**: `spek init` MUST configure git integration hooks for branch creation, commits, and feature workflow

#### /spek.prepare Command
- **FR-010**: `/spek.prepare` MUST load prior decisions, patterns, and lessons from the vault (wiki/ directory)
- **FR-011**: `/spek.prepare` MUST index the codebase via lat.md (or fallback to semantic_search if lat.md unavailable)
- **FR-012**: `/spek.prepare` MUST generate a structured onboarding report with:
  - Relevant prior decisions from vault
  - Current codebase structure and key file locations
  - Navigation guide for the feature
  - Estimated context requirements (token overhead)
- **FR-013**: `/spek.prepare` MUST support feature name or description as input
- **FR-014**: `/spek.prepare` MUST be completable in under 30 seconds for typical projects (< 100K files)

#### /spek.plan Command
- **FR-020**: `/spek.plan` MUST accept a feature description or reference an existing spec
- **FR-021**: `/spek.plan` MUST generate or refine a spec.md with:
  - User scenarios with priorities (P1-P3)
  - Functional requirements (FR-xxx)
  - Success criteria (SC-xxx)
  - Key entities (if data-focused)
  - Assumptions documented
- **FR-022**: `/spek.plan` MUST identify ambiguities in the feature description (max 3) and prompt for clarification
- **FR-023**: `/spek.plan` MUST fill unambiguous gaps with reasonable defaults and document assumptions
- **FR-024**: `/spek.plan` MUST generate a plan.md with:
  - Architecture overview (no code, concepts only)
  - Technology stack and tools
  - Sequence and dependencies
  - Risk assessment and mitigations
- **FR-025**: `/spek.plan` MUST generate a tasks.md with independent, prioritized, testable tasks
- **FR-026**: `/spek.plan` MUST validate all requirements are testable and success criteria are measurable

#### /spek.implement Command
- **FR-030**: `/spek.implement --task TASK_ID` MUST inject relevant context into the agent session:
  - Relevant code files (from lat.md BM25 search or code references in plan)
  - Prior decisions affecting this task
  - Patterns and examples from vault
  - Function signatures and type definitions
- **FR-031**: `/spek.implement` MUST execute a single task with progress tracking
- **FR-032**: `/spek.implement` MUST allow developers to log decisions via a command or annotation (e.g., `@decision "...rationale..."`), which are captured to vault
- **FR-033**: `/spek.implement` MUST support sequential task execution (one task at a time, in priority order)
- **FR-034**: `/spek.implement` MUST track progress and allow tasks to be marked complete, rolled back, or paused
- **FR-035**: `/spek.implement` MUST generate a progress log visible in `.specify/logs/` with timestamps and decisions
- **FR-036**: `/spek.implement` MUST provide a summary upon task completion showing changes made and decisions logged

#### /spek.conclude Command
- **FR-040**: `/spek.conclude` MUST analyze actual outcomes against success criteria
- **FR-041**: `/spek.conclude` MUST extract lessons learned and ask the developer to document them
- **FR-042**: `/spek.conclude` MUST write new patterns, decisions, or insights to the vault (wiki/ directory)
- **FR-043**: `/spek.conclude` MUST export a feature summary (spec, plan, tasks, outcomes, lessons) as markdown
- **FR-044**: `/spek.conclude` MUST refresh the project state (e.g., generate or update project graph, update README references)
- **FR-045**: `/spek.conclude` MUST require Obsidian CLI for vault operations; if unavailable, offer manual fallback

#### Vault & Knowledge Management
- **FR-050**: The vault (wiki/ directory) MUST be Git-backed and support version control
- **FR-051**: The vault MUST include standard sections:
  - `decisions.md` — Architectural decisions made
  - `patterns.md` — Reusable patterns and conventions
  - `lessons.md` — Lessons learned from past features
  - `architecture.md` — High-level system architecture
  - `setup.md` — Project setup and dependencies
  - `conventions.md` — Coding conventions and standards
- **FR-052**: The vault MUST support Obsidian markdown syntax with frontmatter for categorization and linking
- **FR-053**: The vault MUST be queryable via `/spek.prepare` to load prior context
- **FR-054**: The vault MUST be updateable via `/spek.conclude` to persist new decisions and lessons

#### Code Indexing via lat.md
- **FR-060**: The framework MUST use lat.md as the sole code analysis tool for BM25-based lexical retrieval
- **FR-061**: lat.md integration MUST support querying for relevant files, functions, classes, and types by semantic intent
- **FR-062**: lat.md integration MUST support fallback to semantic_search if lat.md is unavailable or query times out
- **FR-063**: lat.md integration MUST support scoped searches (e.g., "all API endpoints in backend/", "all test files")
- **FR-064**: lat.md results MUST be deduplicated and ranked by relevance

#### Git Integration
- **FR-070**: Git integration MUST support automatic branch creation on `/spek.prepare` or manual branch naming
- **FR-071**: Git integration MUST support auto-committing staged changes before major transitions (plan, implement, conclude)
- **FR-072**: Git integration MUST allow developers to view commit history for a feature
- **FR-073**: Git integration MUST support merging completed features back to main with squash or standard merge options

#### Documentation & Help
- **FR-080**: `spek --help` MUST list all available commands with descriptions
- **FR-081**: `spek COMMAND --help` MUST provide command-specific documentation and examples
- **FR-082**: The project README MUST distinguish between end-state documentation (what Spekificity will be) and development documentation (how to build it)
- **FR-083**: README MUST include quick-start guide, prerequisites, installation, and per-project initialization steps

### Key Entities

- **Feature**: A discrete piece of user-facing or internal functionality defined by a spec and implemented via a plan and tasks
- **Specification**: A document defining user scenarios, requirements, success criteria, and assumptions for a feature (spec.md)
- **Plan**: A document defining architecture, technology stack, sequencing, and risk for feature implementation (plan.md)
- **Task**: An independent, testable, prioritized unit of work derived from a plan (task list in tasks.md)
- **Decision**: A record of an architectural, design, or technical choice made during implementation, with rationale and implications
- **Pattern**: A reusable solution or convention documented in the vault for future reference
- **Lesson**: An insight or corrective action extracted from a completed feature, stored in the vault
- **Vault**: A Git-backed Obsidian markdown directory (wiki/) containing decisions, patterns, lessons, and conventions
- **Context**: Relevant code, decisions, patterns, and documentation loaded into an agent session for task execution

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can install Spekificity globally via `uv tool install` and initialize a project via `spek init` in under 5 minutes, with all dependencies auto-installed
- **SC-002**: The `/spek.prepare` command completes in under 30 seconds and returns a structured onboarding report with at least 3 actionable items (relevant decisions, code locations, patterns)
- **SC-003**: The `/spek.plan` command generates a complete, testable specification (spec.md) and sequenced plan (plan.md) within 3 minutes
- **SC-004**: Developers can clarify up to 3 ambiguities during `/spek.plan` interactively without re-running the command
- **SC-005**: The `/spek.implement` command injects contextual information (code files, decisions, patterns) within 10 seconds of task start
- **SC-006**: A developer can complete a task (implement, test, log decision) and mark it complete within 30 minutes, assuming the task scope is well-defined and context is preloaded
- **SC-007**: The `/spek.conclude` command extracts lessons, updates the vault, and produces a feature summary in under 5 minutes
- **SC-008**: Across two sequential features, the second feature's `/spek.prepare` retrieves at least 3 relevant lessons or decisions from the vault that help guide implementation
- **SC-009**: All generated documentation (spec, plan, tasks, lessons) is valid Markdown with correct structure, no broken links, and parseable frontmatter
- **SC-010**: The framework integrates seamlessly with existing projects without requiring changes to codebase structure, build system, or CI/CD pipeline
- **SC-011**: Developers using Spekificity report token efficiency gains of 40-60% compared to traditional iterative AI-assisted development (reduced re-reading, precise context injection)
- **SC-012**: At least 80% of features successfully complete all 4 stages (prepare → plan → implement → conclude) on the first attempt without major re-work

## Assumptions

- **Assumption 1**: Python 3.11+ will be available on users' systems; no support for earlier Python versions is required.
- **Assumption 2**: git will be initialized and available on users' systems; Spekificity operates within Git-managed projects.
- **Assumption 3**: Users have a stable internet connection for initial installation; subsequent work can be offline.
- **Assumption 4**: SpecKit (v0.9.6+) is the primary specification and planning tool; Spekificity wraps and orchestrates it rather than reimplementing it.
- **Assumption 5**: lat.md will be available for code indexing; if unavailable, fallback to semantic_search is acceptable for MVP (though slower).
- **Assumption 6**: The Obsidian desktop app or CLI will be available for vault operations in `/spek.conclude`; if unavailable, manual markdown editing is an acceptable fallback.
- **Assumption 7**: Developers are familiar with Git workflows (branching, committing, merging); no Git training is in scope.
- **Assumption 8**: The vault (wiki/) uses standard Markdown with Obsidian-style links (`[[ref]]`) for cross-referencing; no custom wiki syntax is required.
- **Assumption 9**: Features follow the 4-stage workflow (prepare → plan → implement → conclude); ad hoc work outside this workflow is not in scope.
- **Assumption 10**: Token efficiency improvements come from reduced context re-reading; absolute token cost depends on LLM model and task complexity, which are outside Spekificity's control.
- **Assumption 11**: The project is initially built, tested, and documented with Spekificity itself (dog-fooding); this is expected and acceptable.
- **Assumption 12**: Users have read and agreed to the Spekificity constitution before using the framework; it governs project decision-making and feature prioritization.
- **Assumption 13**: Mobile app support and browser-based interfaces are out of scope for v1; CLI is the primary interface.
- **Assumption 14**: Multi-user collaboration features (real-time sync, concurrent editing) are out of scope for v1; Git manages concurrency.
