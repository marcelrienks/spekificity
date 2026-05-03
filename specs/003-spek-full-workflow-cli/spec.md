# feature specification: spek — full workflow cli

**feature branch**: `003-spek-full-workflow-cli`
**created**: 2026-05-03
**status**: draft

## overview

`spek` is a terminal-based cli tool that serves as the unified entry point for the entire spekificity platform. it orchestrates setup, initialisation, and operation of all underlying tools (graphify, obsidian, speckit/specify, caveman) and provides two distinct operational modes for driving software feature development:

1. **manual mode**: `spek prepare` readies the environment and context, then the developer drives the speckit workflow step by step (spec, plan, tasks, implement) using standard commands.

2. **automated mode**: `spek automate` accepts a feature description from the developer and autonomously drives the full speckit lifecycle (spec → plan → tasks → analyse → remediation → implement) to completion, surfacing questions to the user when needed, handling interruptions, and completing preflight and post-flight operations automatically.

after any development flow, `spek post` executes post-implementation tasks (to be specified) that persist knowledge and clean up the session.

`spek` does not replace any underlying tool. it orchestrates them. all tools remain independently callable.

---

## user scenarios & testing *(mandatory)*

### user story 1 — first-time install and tool setup (priority: p1)

a developer installs the `spek` cli on their machine and runs `spek setup`. the command guides them through verifying and installing all required third-party tools (python 3.11+, uv, graphify, obsidian, speckit/specify, caveman), detecting what is already present and only installing what is missing. the developer ends the setup phase with all prerequisites satisfied and confirmation of what is ready.

**why this priority**: nothing else is possible without prerequisites in place. this is the mandatory gateway to all other functionality.

**independent test**: on a clean machine, run `spek setup`. verify each tool is detected or installed, the developer receives clear pass/fail status per tool, and the session ends with a clear "ready for `spek init`" confirmation.

**acceptance scenarios**:

1. **given** a clean machine with no tools installed, **when** `spek setup` is run, **then** it detects all missing prerequisites, installs them (or provides manual instructions for any it cannot install automatically), and ends with all tools confirmed present.
2. **given** a machine where some tools are already installed, **when** `spek setup` is run, **then** it detects existing tools, skips reinstallation, and confirms only the delta of what was installed.
3. **given** a tool that cannot be auto-installed (e.g., obsidian gui app), **when** `spek setup` runs, **then** it provides step-by-step instructions for manual installation and marks that tool as pending until confirmed.
4. **given** `spek setup` is re-run on a fully set-up machine, **when** it completes, **then** the result is idempotent — no tools are reinstalled, no configuration is overwritten, and a confirmation of readiness is displayed.

---

### user story 2 — project initialisation with `spek init` (priority: p1)

a developer runs `spek init` inside a project folder (empty or existing). this single command orchestrates the complete initialisation of all underlying tools: internally calls `specify init` to set up speckit, configures graphify, sets up the obsidian vault structure, integrates caveman, and installs all spekificity custom skills. after completion, the project is ready for both manual and automated speckit workflows.

**why this priority**: `spek init` is the primary entry point to the operational platform. without it, neither preparation, manual flow, nor automation can run.

**independent test**: in an empty project folder, run `spek init`. verify `.spekificity/` structure is created, all skills are installed and discoverable, speckit initialisation has run, graphify and obsidian vault are configured, and an ai agent can immediately invoke any `/spek.*` or `/speckit.*` command.

**acceptance scenarios**:

1. **given** an empty project folder with all prerequisites installed, **when** `spek init` is run, **then** it orchestrates `specify init`, graphify setup, obsidian vault creation, and skill installation in sequence without user intervention, completing within 5 minutes.
2. **given** a project where speckit is already initialised, **when** `spek init` is run, **then** `specify init` is re-run cleanly (idempotent), existing speckit configuration is preserved, and spekificity skills are added without collision.
3. **given** an already-initialised project, **when** `spek init` is run again, **then** the operation is idempotent — all tools are re-verified, config is updated, and no existing files are overwritten.
4. **given** `spek init` completes, **when** the developer inspects the project, **then** the skill index lists all `/spek.*` and `/speckit.*` commands, and a status summary confirms all tool integrations are active.

---

### user story 3 — preparation phase with `spek prepare` (priority: p2)

before beginning any feature development, a developer runs `spek prepare`. this command executes a defined set of preparation tasks that prime the ai session with current project context. preparation tasks include (but are not limited to): loading vault context (`/spek.context-load`), verifying or refreshing the graphify graph if stale, and surfacing recent lessons learnt. after `spek prepare`, the developer is ready to begin the manual or automated speckit workflow with full context in place.

**why this priority**: preparation ensures that all downstream speckit workflows (manual or automated) benefit from up-to-date codebase context and historical decisions. without preparation, specs and plans lack grounding in the actual project state.

**independent test**: run `spek prepare` on a project with an existing obsidian vault. verify vault context is loaded into the session, graph is verified as current (or refreshed if stale), and recent lessons are surfaced. then run `/speckit.specify` and verify the spec produced references existing codebase context.

**acceptance scenarios**:

1. **given** an initialised project with a vault, **when** `spek prepare` is run, **then** vault context is loaded, graph staleness is checked (and refreshed if stale), and recent lessons learnt are surfaced to the ai session.
2. **given** an initialised project where no vault exists yet, **when** `spek prepare` is run, **then** it detects the missing graph, runs `/spek.map-codebase` to build it, and then loads the context.
3. **given** preparation completes, **when** the developer runs any subsequent speckit command, **then** the ai session has full codebase context and does not need to re-read files to answer cross-cutting questions.
4. **given** `spek prepare` is run in a project with a recently-built graph (within threshold), **when** it completes, **then** the graph rebuild is skipped and a "context loaded from cache" confirmation is displayed.

---

### user story 4 — automated speckit lifecycle with `spek automate` (priority: p1)

a developer runs `spek automate` with a feature description. spek executes the full speckit lifecycle — spec → plan → tasks → analyse → remediation → implement — entirely autonomously. at any point where speckit needs clarification, spek surfaces the question to the developer. where speckit can proceed without input, it does so automatically. speckit stopping mid-flow is treated as an interruption to be resumed, not a terminal failure. the workflow drives to full completion: a merged feature branch or open PR.

**why this priority**: this is the primary differentiator of `spek` over manual speckit usage. autonomous, completion-guaranteed feature development is the core value proposition.

**independent test**: run `spek automate "add a user login form"` on an initialised and prepared project. verify a feature branch is created, all speckit lifecycle steps are executed in sequence, any questions are surfaced to the developer interactively, implementation reaches completion, and a PR is opened.

**acceptance scenarios**:

1. **given** an initialised and prepared project, **when** `spek automate "<feature description>"` is run, **then** a preflight check verifies no unstaged changes exist, a feature branch is created, and the speckit spec step is invoked with the provided description.
2. **given** the spec step produces clarification questions, **when** speckit requests input, **then** spek surfaces each question to the developer in a clear interactive prompt, collects answers, and injects them back into the speckit flow without the developer having to understand speckit internals.
3. **given** spec is complete, **when** spec step ends, **then** spek automatically invokes the plan step without developer intervention, passing the spec as input.
4. **given** plan is complete, **when** plan step ends, **then** spek automatically invokes tasks step, then analyse step in sequence.
5. **given** the analyse step identifies remediation items, **when** remediation is recommended, **then** spek surfaces the remediation items to the developer for review, suggests remediation implementations, collects any developer input, and proceeds with remediation before advancing to implementation.
6. **given** the implementation step starts, **when** implementation runs, **then** spek monitors for speckit stopping mid-flow and automatically instructs speckit to continue until all tasks are marked complete.
7. **given** implementation is complete, **when** the final task is done, **then** spek performs post-flight operations: marks the spec as complete, runs `/spek.post` (post-implementation tasks), and opens a pull request targeting the default branch.
8. **given** any step fails with an unrecoverable error, **when** spek cannot proceed, **then** it halts, displays the error clearly, saves the current workflow state, and provides the developer with instructions to resume with `spek automate --resume`.

---

### user story 5 — post-implementation tasks with `spek post` (priority: p2)

after any feature implementation (manual or automated), a developer runs `spek post`. this command executes a defined set of post-implementation tasks that capture knowledge and clean up the session. post tasks include (but are not limited to): running `/spek.lessons-learnt` to append a structured lessons entry to the obsidian vault, and running `/spek.map-codebase` to update the graph with newly created or modified files.

**why this priority**: knowledge capture at feature completion is what makes the obsidian vault grow in value over time. without post tasks, the system loses its memory advantage on each completed feature.

**independent test**: complete a feature implementation manually, then run `spek post`. verify a lessons learnt entry is appended to `vault/lessons/`, the graphify graph is refreshed to include new files, and the ai session confirms the vault is updated.

**acceptance scenarios**:

1. **given** a completed feature implementation, **when** `spek post` is run, **then** the lessons-learnt skill is invoked, the developer is prompted for key decisions and patterns from the feature, and a structured entry is written to `vault/lessons/`.
2. **given** new files were created during implementation, **when** `spek post` runs, **then** `/spek.map-codebase` is invoked in incremental mode to update the graph with the new nodes.
3. **given** `spek automate` runs to completion, **when** the automated post-flight phase starts, **then** `spek post` is invoked automatically without requiring the developer to trigger it manually.
4. **given** `spek post` is run after a manual workflow, **when** lessons are captured, **then** the next `/spek.context-load` in a future session surfaces the new lessons entry.

---

### user story 6 — graphify and obsidian integration throughout the workflow (priority: p2)

graphify and obsidian are not merely setup artefacts — they actively participate in every spek workflow. the obsidian vault provides context for spec and plan steps, graphify graph is consulted when resolving cross-cutting questions during automation, and the vault is updated after implementation. this integration ensures each feature is grounded in the actual codebase state.

**why this priority**: without active graphify/obsidian integration, spek automate reduces to vanilla speckit automation with no codebase awareness. the vault is what differentiates spek from a simple speckit wrapper.

**independent test**: run `spek automate` on a project with a populated obsidian vault. inspect the generated spec and plan; verify they reference existing codebase components from the vault graph. inspect the vault after completion; verify new lessons and graph updates are present.

**acceptance scenarios**:

1. **given** a project with an obsidian vault, **when** `spek automate` runs the spec step, **then** the vault graph is consulted and related existing components are referenced in the generated spec.
2. **given** a project with a populated vault, **when** `spek automate` runs the plan step, **then** impacted graph nodes are identified and referenced in the plan without the ai re-reading all source files.
3. **given** implementation completes, **when** post-flight runs, **then** the graph is updated incrementally with new or modified files, and the vault contains a new lessons entry for the completed feature.
4. **given** vault context is loaded via `spek prepare`, **when** `spek automate` asks for clarifications, **then** questions are informed by existing patterns and decisions from the vault (reducing the number of questions asked of the developer).

---

### edge cases

- **interrupted automation**: if `spek automate` is interrupted (network failure, session timeout, user ctrl-c), workflow state is saved and can be resumed with `spek automate --resume`. the resume command re-reads the last completed speckit step and continues from the next step.
- **speckit stops mid-implementation**: if speckit halts mid-task (e.g., tool exits early, context window limit reached), spek detects the halt condition, surfaces any pending questions to the developer, and instructs speckit to continue. this repeats until all tasks are marked complete.
- **conflicting feature branch**: if a branch for the feature already exists when `spek automate` starts, spek asks the developer whether to reuse the existing branch or create a new one with a suffix.
- **analyse step identifies high-risk remediation**: if remediation impacts a large portion of the codebase or introduces breaking changes, spek prompts the developer for explicit approval before proceeding, displaying the impact scope.
- **pr creation fails**: if the pr creation step fails (no remote, auth issue, branch protection), spek does not fail silently — it reports the failure, outputs the pr description to the terminal, and provides instructions for manual pr creation.
- **empty vault on first use**: if `spek prepare` is run before any codebase mapping, the graph is built from scratch rather than refreshed. the developer is informed that the first prepare will take longer.
- **vault context absent during automate**: if `vault/context/decisions.md` or `vault/context/patterns.md` are missing or empty when `spek automate` reaches the spec or plan step, vault context injection is skipped and the skill proceeds with a warning. this is the no-vault fallback defined in contracts/vault-integration-contract.md.

---

## requirements *(mandatory)*

### functional requirements

- **fr-001**: `spek` must be installable as a cli tool from a terminal on macos and linux without requiring a gui or browser interaction.
- **fr-002**: `spek setup` must detect all required and optional prerequisites (python 3.11+, uv, git, graphify, obsidian, speckit/specify, caveman), auto-install those that can be installed programmatically, and provide step-by-step instructions for those that require manual installation.
- **fr-003**: `spek setup` must classify tools as required (python, uv, git, speckit) or optional (graphify, obsidian, caveman) and allow partial setup completion where optional tools are deferred.
- **fr-004**: `spek init` must orchestrate initialisation of all underlying tools in a single command by internally calling `specify init`, graphify setup, obsidian vault creation, and caveman skill installation.
- **fr-005**: `spek init` must install all spekificity custom skills (`/spek.*`), speckit skills (`/speckit.*`), and caveman skills to their default project locations, and register them in a unified skill index at `.spekificity/skill-index.md`.
- **fr-006**: `spek init` must be idempotent — multiple runs must not destroy existing project configuration, overwrite custom modifications, or re-initialise tools that are already initialised to the correct version.
- **fr-007**: `spek prepare` must execute the following preparation tasks before any feature workflow: (a) verify graph currency — building or refreshing the graph if stale or absent (trigger mechanism defined in fr-008), (b) load vault context (decisions, patterns), and (c) surface recent lessons to the ai session.
- **fr-008**: `spek prepare` must detect a missing or stale graph and automatically trigger `/spek.map-codebase` to build or refresh it before loading context.
- **fr-009**: `spek automate "<feature description>"` must accept a natural-language feature description as input and pass it to the speckit spec step to begin the lifecycle.
- **fr-010**: `spek automate` must automatically sequence all speckit lifecycle steps (spec → plan → tasks → analyse → remediation → implement) in order, without requiring developer intervention between steps unless questions arise.
- **fr-011**: `spek automate` must surface any clarification questions generated by speckit to the developer via interactive prompt, collect answers, and inject them back into the speckit flow — the developer must never need to interact directly with speckit internals. the injection mechanism and question lifecycle are defined in contracts/automate-contract.md.
- **fr-012**: `spek automate` must monitor each speckit step for premature halts and automatically instruct speckit to continue until each step reaches a defined completion state.
- **fr-013**: `spek automate` must perform preflight checks before starting: verify no uncommitted changes block branch creation, create a feature branch named after the feature, and confirm the branch is active before invoking speckit.
- **fr-014**: `spek automate` must perform post-flight operations on completion: mark the spec status as complete, invoke `spek post`, and open a pull request targeting the default branch with an auto-generated description.
- **fr-015**: `spek automate` must save workflow state after each completed speckit step so that `spek automate --resume` can recover from interruptions without restarting from the beginning.
- **fr-016**: `spek automate` must leverage the obsidian vault at spec and plan steps, passing relevant vault context to inform the feature spec and plan with existing codebase knowledge.
- **fr-017**: `spek post` must execute a defined set of post-implementation tasks (to be specified separately), including at minimum: invoking `/spek.lessons-learnt` and running `/spek.map-codebase` in incremental mode.
- **fr-018**: `spek post` must be invokable both manually (after a manual workflow) and automatically (as part of `spek automate` post-flight).
- **fr-019**: `spek status` must report the current state of: initialisation, installed skills, third-party tool versions, and vault currency (last graph refresh timestamp).
- **fr-020**: all `spek` commands must produce clear, human-readable terminal output distinguishing spekificity actions from underlying tool actions (e.g., prefixing spek actions with `[spek]` and underlying tool actions with `[speckit]`, `[graphify]`, etc.).
- **fr-021**: `spek update` must update the spekificity custom layer (scripts, skills, and workflows) to the latest version without modifying underlying tool configuration (speckit, graphify, etc.), and must be idempotent — running `spek update` on an already-current installation produces no changes and exits 0.

### key entities

- **spek cli**: the terminal-executable command. has sub-commands: `setup`, `init`, `prepare`, `automate`, `post`, `status`, `update`.
- **workflow state**: persisted state file (`.spekificity/workflow-state.json`) that tracks the current automate session: active feature branch, last completed speckit step, pending questions, and resume checkpoint.
- **skill index**: `.spekificity/skill-index.md` — unified registry of all available commands (`/spek.*`, `/speckit.*`, caveman) and their locations.
- **vault**: the obsidian vault at `vault/` — graph nodes, lessons, decisions, patterns. consulted at spec/plan steps, updated at post step.
- **graph**: the graphify-generated dependency graph stored under `vault/graph/`. has a currency state (fresh / stale / absent) that determines whether `spek prepare` triggers a refresh.

---

## success criteria *(mandatory)*

### measurable outcomes

- **sc-001**: a developer on a clean machine can run `spek setup` followed by `spek init` and be fully operational within 15 minutes (excluding obsidian gui installation time if required).
- **sc-002**: `spek automate` drives the complete speckit lifecycle (spec through implementation) to completion for a feature with no more than 5 developer interactions (questions answered) for a well-described feature request.
- **sc-003**: `spek automate` resumes from an interruption point without data loss and without re-executing already-completed speckit steps.
- **sc-004**: a feature spec and plan produced by `spek automate` references at least 2 existing codebase components from the obsidian vault graph (demonstrating active vault integration).
- **sc-005**: `spek post` captures a lessons learnt entry and updates the graph within 3 minutes of being invoked on a completed feature.
- **sc-006**: `spek prepare` loads vault context and completes readiness checks in under 60 seconds on a project with a current (non-stale) graph.
- **sc-007**: all `spek` commands are idempotent — running any command twice in sequence produces the same end state as running it once.

---

## assumptions

- **prepare tasks**: `spek prepare` performs at minimum: vault context load, graph currency check (with auto-refresh if stale or absent), and surfacing recent lessons to the ai session. additional preparation tasks may be added in future enhancements without breaking existing behaviour.
- **post tasks**: `spek post` performs at minimum: invoking `/spek.lessons-learnt` and running `/spek.map-codebase` in incremental mode. additional post-implementation tasks may be added in future enhancements.
- **speckit api stability**: the automated workflow assumes that speckit lifecycle commands (`/speckit.specify`, `/speckit.plan`, etc.) accept programmatic invocation and produce machine-readable output or clearly delimited output that spek can detect as complete or halted. if speckit does not support this natively, spek will implement pattern-based detection of completion states.
- **pr creation**: pr creation assumes a git remote is configured and the developer has authentication credentials. spek uses the git cli or github cli (`gh`) to create prs. if neither is available, spek outputs the pr description to the terminal for manual submission.
- **obsidian vault format stability**: vault reads and writes assume the obsidian vault format is plain markdown, as established in prior specs. no obsidian app api is assumed.
- **single active feature**: `spek automate` assumes one active feature workflow per project at a time. concurrent workflows in the same directory are not supported in v1.
- **feature branch naming**: branch names are auto-generated from the feature description using the same `NNN-kebab-case-name` pattern established in prior specs.
- **caveman integration**: caveman mode is available and invokable throughout all workflows. `spek automate` may activate caveman mode automatically during implementation to reduce token consumption.
