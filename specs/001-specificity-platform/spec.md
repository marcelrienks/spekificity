# feature specification: spekificity platform — core project foundation

**feature branch**: `001-spekificity-platform`  
**created**: 2026-04-29  
**status**: complete  

## overview

**spekificity** is a platform that improves ai-assisted development by combining four existing tools — graphify, obsidian, github speckit (via specify), and the caveman skill — into a single workflow. it produces no executable application code; instead it produces markdown skills, workflow descriptions, setup guides, and ai agent instructions that enable any developer to initialise, configure, and operate a persistent ai development environment on any project. the initialisation mechanism is an ai-executed setup guide, not a compiled binary — every setup step is a terminal command or ai instruction that can be followed without human interpretation.

---

## user scenarios & testing *(mandatory)*

### user story 1 — first-time project initialisation (priority: p1)

a developer runs a single command (or follows a short ai-guided script) inside an empty or pre-existing project folder. the command detects what is already installed, installs or links the required third-party tools (graphify, obsidian, speckit/specify) according to their install mode (local vs global prerequisite), and then installs the spekificity custom skills and workflow guides locally. after the command completes the developer can immediately begin using the full ai-assisted workflow.

**why this priority**: this is the entry point of the entire system. nothing else is usable until initialisation succeeds.

**independent test**: follow `workflows/init-workflow.md` on a fresh folder; verify all tools are reachable, all custom skills are present in `.github/agents/` (github copilot) or `.claude/commands/` (claude code), and an ai agent can invoke `/speckit.specify` without errors.

**acceptance scenarios**:

1. **given** an empty project folder with none of the tools installed, **when** the init workflow is followed, **then** all required tools are installed/linked and all custom skills are available locally within 10 minutes of tool installation completing.
2. **given** a project folder where speckit is already globally installed, **when** the init command is run, **then** the existing global installation is reused (not duplicated) and custom skills are layered on top.
3. **given** an already-initialised project folder, **when** the init command is run again, **then** the command is idempotent — it updates without destroying existing configuration.

---

### user story 2 — ai-guided codebase & documentation mapping (priority: p2)

after initialisation, a developer invokes a skill command that directs the ai agent to build or refresh a graph-based map of the codebase and documentation using graphify and store it as an obsidian vault. subsequent ai queries consult the graph map rather than recursively reading every file, dramatically reducing token consumption.

**why this priority**: this is the primary token-efficiency mechanism — the core differentiator of spekificity over vanilla speckit usage.

**independent test**: on a project with at least 20 files, invoke the mapping skill, then ask the ai a cross-cutting question; verify the ai answers using the graph map without exhaustively re-reading all source files.

**acceptance scenarios**:

1. **given** an initialised project, **when** the mapping skill is invoked, **then** a graphify graph of all source files and docs is generated and stored as an obsidian vault within the project.
2. **given** an existing map, **when** new files are added and the mapping skill is re-invoked, **then** only changed/new nodes are updated (incremental refresh).
3. **given** a mapped project, **when** the ai receives a context request, **then** the ai uses the obsidian vault graph to answer without loading files that are not relevant.

---

### user story 3 — enriched speckit feature lifecycle (priority: p2)

a developer uses the spekificity-extended speckit workflow (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) where each step is enriched by graph context from obsidian, caveman-compressed prompts, and persisted lessons learnt. the ai produces richer specs, more accurate plans, and more reliable implementations compared to vanilla speckit.

**why this priority**: this is the main day-to-day value proposition — improving the quality and reliability of ai-generated work.

**independent test**: run a full speckit feature lifecycle on a test project with spekificity active; compare spec detail, plan accuracy, and implementation correctness against a baseline vanilla speckit run on the same feature.

**acceptance scenarios**:

1. **given** an initialised and mapped project, **when** `/speckit.specify` is invoked, **then** the spec includes cross-referenced context from the obsidian map (e.g., related existing components are cited).
2. **given** a spec, **when** `/speckit.plan` is invoked, **then** the plan references existing graph nodes that will be impacted, without the ai having to re-read all source files.
3. **given** an implementation is complete, **when** the lessons-learnt skill is invoked, **then** a structured lessons entry is appended to the obsidian vault and referenced in future ai sessions.

---

### user story 4 — token-efficient ai interactions via caveman (priority: p3)

throughout the entire workflow, the caveman skill is automatically or easily invokable to compress ai responses and prompts, reducing the verbosity of context and keeping token budgets low without sacrificing technical accuracy.

**why this priority**: important for cost efficiency but not a blocker for core functionality.

**independent test**: toggle caveman mode on; verify that ai output is measurably shorter (by character count) while retaining all technically required information for subsequent workflow steps.

**acceptance scenarios**:

1. **given** any spekificity workflow step, **when** caveman mode is active, **then** all ai responses are compressed using the caveman skill conventions.
2. **given** caveman mode is active, **when** the ai must reference graph nodes, **then** node references are expressed in compressed notation without losing traceability.

---

### user story 5 — independent component updates (priority: p3)

a developer updates one third-party tool (e.g., a new version of speckit/specify is released globally) without needing to re-initialise the entire spekificity stack. the modular structure allows each component (graphify, obsidian, speckit, spekificity custom skills) to be updated independently.

**why this priority**: ensures long-term maintainability and reduces friction of keeping the stack current.

**independent test**: update the global speckit installation; verify spekificity custom skills still function correctly and no configuration files need manual merging.

**acceptance scenarios**:

1. **given** speckit is updated globally, **when** a developer runs the spekificity update check, **then** the custom skills layer adapts to the new speckit version without manual intervention.
2. **given** graphify releases a new version, **when** the graphify component is updated, **then** obsidian vault structure and existing maps remain intact.

---

### edge cases

- what happens when a required third-party tool (graphify, obsidian) is not installable in the target environment?
- how does the system behave when the obsidian vault is very large (>10,000 nodes)?
- what happens if an ai agent does not support a specific skill format (e.g., `.agent.md` vs `.instructions.md`)?
- how does lessons-learnt deduplication work when the same lesson is encountered across multiple features?
- what happens if the init command is interrupted mid-way?

---

## requirements *(mandatory)*

### functional requirements

- **fr-001**: the initialisation mechanism must install or link graphify and speckit/specify to the target project (each as a global prerequisite via `uv tool install`), and must create the obsidian vault directory structure locally. the obsidian desktop app is optional and not required for ai agent read/write operations — the vault is plain markdown on the filesystem.
- **fr-002**: the initialisation mechanism must install spekificity's custom skills and workflow documents locally within the project, in a structure consistent with how specify installs speckit.
- **fr-003**: the system must support idempotent initialisation — running the init command multiple times must not corrupt or duplicate configuration.
- **fr-004**: spekificity must install standard speckit globally (or guide the user to do so) so that upstream speckit updates can be applied without modifying spekificity's custom layer.
- **fr-005**: the mapping skill must direct the ai to build a graphify-based graph of the codebase and store it as an obsidian vault accessible by subsequent ai sessions.
- **fr-006**: the mapping skill must support incremental refresh, updating only changed nodes rather than regenerating the entire graph.
- **fr-007**: all spekificity-extended speckit skills must decorate (not replace) the vanilla speckit commands, following a decorator pattern.
- **fr-008**: lessons-learnt entries must be structured, versioned, and stored in the obsidian vault, and referenced in ai agent context for future sessions.
- **fr-009**: the caveman skill must be integrated into the spekificity workflow and invokable at any point to compress ai context.
- **fr-010**: each component (graphify, obsidian, speckit, spekificity custom layer) must be independently updatable without requiring full re-initialisation.
- **fr-011**: the system must support at minimum two ai agents: github copilot and claude code.
- **fr-012**: all setup steps that cannot be automated must be documented as clear, ai-executable step-by-step guides.

### key entities

- **skill**: a markdown file containing instructions that an ai agent can read and execute; analogous to an agent plugin.
- **workflow**: a documented sequence of skill invocations with expected inputs, outputs, and ordering.
- **graph map**: a graphify-generated dependency/relationship graph of source files and documentation nodes.
- **obsidian vault**: a local obsidian-format directory (markdown + metadata) that stores the graph map, lessons learnt, and persistent context.
- **lessons learnt entry**: a structured record capturing what was discovered, changed, or decided during a speckit feature lifecycle.
- **persistent context**: ai-accessible memory that survives across sessions, stored in the obsidian vault and referenced in ai agent instructions.

---

## success criteria *(mandatory)*

### measurable outcomes

- **sc-001**: a developer with no prior knowledge of the tool stack can complete tool installation in under 10 minutes and complete first-time initialisation (including spekificity skill deployment and first `/speckit.specify` invocation) in under 30 minutes total.
- **sc-002**: ai token consumption for cross-cutting queries on a mapped project is reduced by at least 40% compared to an unmapped project of equivalent size.
- **sc-003**: the caveman skill reduces ai response verbosity by at least 60% (by character count) without omitting technical content required for the next workflow step.
- **sc-004**: 100% of speckit lifecycle steps (specify, plan, tasks, implement) are enriched with graph context when a map is available.
- **sc-005**: updating any single third-party component takes less than 5 minutes of developer effort and requires zero changes to the other components.
- **sc-006**: the `context-load` skill must load the vault index and most recent lessons entry in a single session step, without requiring multiple back-and-forth turns with the developer.
- **sc-007**: the system is operational on both macos and linux environments.

---

## assumptions

- graphify and obsidian can be installed locally within a project folder, or if they require global installation, the documentation clearly identifies them as prerequisites and provides install instructions.
- github copilot reads skills from `.github/agents/` and claude code reads skills from `.claude/commands/` — both conventions are supported by speckit/specify and used by spekificity.
- the target developer has basic familiarity with a terminal and git.
- speckit/specify is installed globally (or the init command handles its installation) and is available on the system path.
- the caveman skill is already installed in the developer's global agent skills directory and does not need to be installed by spekificity.
- obsidian vaults in markdown format are compatible with direct file-system reads by ai agents.
- no backend server or cloud service is required; all components run locally or are accessed via existing cloud ai services.

---

## out of scope

- building graphify, obsidian, or speckit functionality from scratch.
- providing a gui or web-based interface for any workflow step.
- supporting ai agents other than github copilot and claude code in the initial version.
- automatic conflict resolution between speckit upstream changes and spekificity custom skills.
- multi-user or team-shared obsidian vault synchronisation.
