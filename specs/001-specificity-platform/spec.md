# Feature Specification: Spekificity Platform — Core Project Foundation

**Feature Branch**: `001-spekificity-platform`  
**Created**: 2026-04-29  
**Status**: Complete  

## Overview

**Spekificity** is a meta-tooling project that orchestrates and supercharges an AI-assisted development workflow by combining four existing tools — Graphify, Obsidian, GitHub SpecKit (via Specify), and the Caveman skill — into a cohesive, developer-friendly system. It does not produce executable application code; instead, it produces a curated collection of skills, workflow descriptions, setup guides, and AI agent instructions that together enable any developer to initialise, configure, and operate a persistent, context-aware, token-efficient AI development environment on any project. The initialisation mechanism is an AI-executed setup guide, not a compiled binary — every setup step is a terminal command or AI instruction that can be followed without human interpretation.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — First-Time Project Initialisation (Priority: P1)

A developer runs a single command (or follows a short AI-guided script) inside an empty or pre-existing project folder. The command detects what is already installed, installs or links the required third-party tools (Graphify, Obsidian, SpecKit/Specify) according to their install mode (local vs global prerequisite), and then installs the Spekificity custom skills and workflow guides locally. After the command completes the developer can immediately begin using the full AI-assisted workflow.

**Why this priority**: This is the entry point of the entire system. Nothing else is usable until initialisation succeeds.

**Independent Test**: Follow `workflows/init-workflow.md` on a fresh folder; verify all tools are reachable, all custom skills are present in `.github/agents/` (GitHub Copilot) or `.claude/commands/` (Claude Code), and an AI agent can invoke `/speckit.specify` without errors.

**Acceptance Scenarios**:

1. **Given** an empty project folder with none of the tools installed, **When** the init workflow is followed, **Then** all required tools are installed/linked and all custom skills are available locally within 10 minutes of tool installation completing.
2. **Given** a project folder where SpecKit is already globally installed, **When** the init command is run, **Then** the existing global installation is reused (not duplicated) and custom skills are layered on top.
3. **Given** an already-initialised project folder, **When** the init command is run again, **Then** the command is idempotent — it updates without destroying existing configuration.

---

### User Story 2 — AI-Guided Codebase & Documentation Mapping (Priority: P2)

After initialisation, a developer invokes a skill command that directs the AI agent to build or refresh a graph-based map of the codebase and documentation using Graphify and store it as an Obsidian vault. Subsequent AI queries consult the graph map rather than recursively reading every file, dramatically reducing token consumption.

**Why this priority**: This is the primary token-efficiency mechanism — the core differentiator of Spekificity over vanilla SpecKit usage.

**Independent Test**: On a project with at least 20 files, invoke the mapping skill, then ask the AI a cross-cutting question; verify the AI answers using the graph map without exhaustively re-reading all source files.

**Acceptance Scenarios**:

1. **Given** an initialised project, **When** the mapping skill is invoked, **Then** a Graphify graph of all source files and docs is generated and stored as an Obsidian vault within the project.
2. **Given** an existing map, **When** new files are added and the mapping skill is re-invoked, **Then** only changed/new nodes are updated (incremental refresh).
3. **Given** a mapped project, **When** the AI receives a context request, **Then** the AI uses the Obsidian vault graph to answer without loading files that are not relevant.

---

### User Story 3 — Supercharged SpecKit Feature Lifecycle (Priority: P2)

A developer uses the Spekificity-extended SpecKit workflow (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) where each step is enriched by graph context from Obsidian, caveman-compressed prompts, and persisted lessons learnt. The AI produces richer specs, more accurate plans, and more reliable implementations compared to vanilla SpecKit.

**Why this priority**: This is the main day-to-day value proposition — improving the quality and reliability of AI-generated work.

**Independent Test**: Run a full speckit feature lifecycle on a test project with Spekificity active; compare spec detail, plan accuracy, and implementation correctness against a baseline vanilla SpecKit run on the same feature.

**Acceptance Scenarios**:

1. **Given** an initialised and mapped project, **When** `/speckit.specify` is invoked, **Then** the spec includes cross-referenced context from the Obsidian map (e.g., related existing components are cited).
2. **Given** a spec, **When** `/speckit.plan` is invoked, **Then** the plan references existing graph nodes that will be impacted, without the AI having to re-read all source files.
3. **Given** an implementation is complete, **When** the lessons-learnt skill is invoked, **Then** a structured lessons entry is appended to the Obsidian vault and referenced in future AI sessions.

---

### User Story 4 — Token-Efficient AI Interactions via Caveman (Priority: P3)

Throughout the entire workflow, the Caveman skill is automatically or easily invokable to compress AI responses and prompts, reducing the verbosity of context and keeping token budgets low without sacrificing technical accuracy.

**Why this priority**: Important for cost efficiency but not a blocker for core functionality.

**Independent Test**: Toggle Caveman mode on; verify that AI output is measurably shorter (by character count) while retaining all technically required information for subsequent workflow steps.

**Acceptance Scenarios**:

1. **Given** any Spekificity workflow step, **When** Caveman mode is active, **Then** all AI responses are compressed using the Caveman skill conventions.
2. **Given** Caveman mode is active, **When** the AI must reference graph nodes, **Then** node references are expressed in compressed notation without losing traceability.

---

### User Story 5 — Independent Component Updates (Priority: P3)

A developer updates one third-party tool (e.g., a new version of SpecKit/Specify is released globally) without needing to re-initialise the entire Spekificity stack. The modular structure allows each component (Graphify, Obsidian, SpecKit, Spekificity custom skills) to be updated independently.

**Why this priority**: Ensures long-term maintainability and reduces friction of keeping the stack current.

**Independent Test**: Update the global SpecKit installation; verify Spekificity custom skills still function correctly and no configuration files need manual merging.

**Acceptance Scenarios**:

1. **Given** SpecKit is updated globally, **When** a developer runs the Spekificity update check, **Then** the custom skills layer adapts to the new SpecKit version without manual intervention.
2. **Given** Graphify releases a new version, **When** the Graphify component is updated, **Then** Obsidian vault structure and existing maps remain intact.

---

### Edge Cases

- What happens when a required third-party tool (Graphify, Obsidian) is not installable in the target environment?
- How does the system behave when the Obsidian vault is very large (>10,000 nodes)?
- What happens if an AI agent does not support a specific skill format (e.g., `.agent.md` vs `.instructions.md`)?
- How does lessons-learnt deduplication work when the same lesson is encountered across multiple features?
- What happens if the init command is interrupted mid-way?

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The initialisation mechanism MUST install or link Graphify and SpecKit/Specify to the target project (each as a global prerequisite via `uv tool install`), and MUST create the Obsidian vault directory structure locally. The Obsidian desktop app is optional and NOT required for AI agent read/write operations — the vault is plain markdown on the filesystem.
- **FR-002**: The initialisation mechanism MUST install Spekificity's custom skills and workflow documents locally within the project, in a structure consistent with how Specify installs SpecKit.
- **FR-003**: The system MUST support idempotent initialisation — running the init command multiple times MUST NOT corrupt or duplicate configuration.
- **FR-004**: Spekificity MUST install standard SpecKit globally (or guide the user to do so) so that upstream SpecKit updates can be applied without modifying Spekificity's custom layer.
- **FR-005**: The mapping skill MUST direct the AI to build a Graphify-based graph of the codebase and store it as an Obsidian vault accessible by subsequent AI sessions.
- **FR-006**: The mapping skill MUST support incremental refresh, updating only changed nodes rather than regenerating the entire graph.
- **FR-007**: All Spekificity-extended SpecKit skills MUST decorate (not replace) the vanilla SpecKit commands, following a decorator pattern.
- **FR-008**: Lessons-learnt entries MUST be structured, versioned, and stored in the Obsidian vault, and referenced in AI agent context for future sessions.
- **FR-009**: The Caveman skill MUST be integrated into the Spekificity workflow and invokable at any point to compress AI context.
- **FR-010**: Each component (Graphify, Obsidian, SpecKit, Spekificity custom layer) MUST be independently updatable without requiring full re-initialisation.
- **FR-011**: The system MUST support at minimum two AI agents: GitHub Copilot and Claude Code.
- **FR-012**: All setup steps that cannot be automated MUST be documented as clear, AI-executable step-by-step guides.

### Key Entities

- **Skill**: A markdown file containing instructions that an AI agent can read and execute; analogous to an agent plugin.
- **Workflow**: A documented sequence of skill invocations with expected inputs, outputs, and ordering.
- **Graph Map**: A Graphify-generated dependency/relationship graph of source files and documentation nodes.
- **Obsidian Vault**: A local Obsidian-format directory (markdown + metadata) that stores the graph map, lessons learnt, and persistent context.
- **Lessons Learnt Entry**: A structured record capturing what was discovered, changed, or decided during a SpecKit feature lifecycle.
- **Persistent Context**: AI-accessible memory that survives across sessions, stored in the Obsidian vault and referenced in AI agent instructions.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer with no prior knowledge of the tool stack can complete tool installation in under 10 minutes and complete first-time initialisation (including Spekificity skill deployment and first `/speckit.specify` invocation) in under 30 minutes total.
- **SC-002**: AI token consumption for cross-cutting queries on a mapped project is reduced by at least 40% compared to an unmapped project of equivalent size.
- **SC-003**: The Caveman skill reduces AI response verbosity by at least 60% (by character count) without omitting technical content required for the next workflow step.
- **SC-004**: 100% of SpecKit lifecycle steps (specify, plan, tasks, implement) are enriched with graph context when a map is available.
- **SC-005**: Updating any single third-party component takes less than 5 minutes of developer effort and requires zero changes to the other components.
- **SC-006**: The `context-load` skill MUST load the vault index and most recent lessons entry in a single session step, without requiring multiple back-and-forth turns with the developer.
- **SC-007**: The system is operational on both macOS and Linux environments.

---

## Assumptions

- Graphify and Obsidian can be installed locally within a project folder, or if they require global installation, the documentation clearly identifies them as prerequisites and provides install instructions.
- GitHub Copilot reads skills from `.github/agents/` and Claude Code reads skills from `.claude/commands/` — both conventions are supported by SpecKit/Specify and used by Spekificity.
- The target developer has basic familiarity with a terminal and git.
- SpecKit/Specify is installed globally (or the init command handles its installation) and is available on the system PATH.
- The Caveman skill is already installed in the developer's global agent skills directory and does not need to be installed by Spekificity.
- Obsidian vaults in markdown format are compatible with direct file-system reads by AI agents.
- No backend server or cloud service is required; all components run locally or are accessed via existing cloud AI services.

---

## Out of Scope

- Building Graphify, Obsidian, or SpecKit functionality from scratch.
- Providing a GUI or web-based interface for any workflow step.
- Supporting AI agents other than GitHub Copilot and Claude Code in the initial version.
- Automatic conflict resolution between SpecKit upstream changes and Spekificity custom skills.
- Multi-user or team-shared Obsidian vault synchronisation.
