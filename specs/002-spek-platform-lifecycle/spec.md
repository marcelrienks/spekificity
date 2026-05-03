# feature specification: spekificity as a complete platform — setup, init, and update lifecycle

**feature branch**: `002-spek-platform-lifecycle`  
**created**: 2026-05-03  
**status**: draft  

## overview

Transform spekificity from a collection of custom skills and workflows into a complete, self-contained platform that consolidates and automates setup, initialization, and maintenance of a multi-tool development stack. Spekificity is a **consolidation and automation layer**, not a replacement for underlying tools.

### architectural philosophy

Spekificity operates on four core principles:

1. **Primary orchestration entry point**: `spek` is the primary, intended entry point for users (analogous to how `specify` is for speckit). When a user runs `spek init`, it internally orchestrates and calls the initialization functions of all consolidated tools (`specify init`, graphify setup, obsidian setup, caveman setup, etc.). This provides a unified developer experience while preserving the independence of underlying tools.

2. **Consolidation without replacement**: Spekificity groups and orchestrates existing tools (speckit, graphify, obsidian, caveman) into a cohesive workflow, but does NOT replace their functionality. All underlying tools remain fully functional and can be used directly if needed (e.g., `graphify` CLI, `specify` CLI work independently). However, the primary intended workflow is through `spek` commands, which orchestrate these tools internally.

3. **Automation of setup and initialization**: Spekificity automates the friction points of multi-tool setup — prerequisite detection, installation, configuration, skill discovery, and orchestrated initialization of all components. The `spek setup` and `spek init` commands eliminate manual file copying, configuration, and environment verification by calling underlying tool initialization functions as needed.

4. **Unified skill installation across all layers**: When `spek init` runs, it installs skills from all layers (spekificity custom skills, speckit skills via `specify init`, caveman skills) to their default project locations. Users interact with a unified command namespace (`/spek.*` for spekificity, `/speckit.*` for speckit, caveman skill access) without manual skill copying or configuration. This creates a seamless multi-tool development environment.

### platform components

See **Functional Requirements** section (FR-001 through FR-018) for complete component specifications and architecture details.

---

## user scenarios & testing *(mandatory)*

### user story 1 — single-command project setup (priority: p1)

A developer runs a single `spek setup` command in a new or existing project folder. This is the primary entry point for setting up the entire development stack. The command detects what is already installed, installs missing prerequisites (Python 3.11+, uv, git, speckit, graphify, obsidian), and prepares the environment for `spek init`. The setup process is automated and requires no manual prerequisite installation or configuration. After setup, the developer runs `spek init` (the primary initialization entry point, analogous to `specify init` for speckit) which orchestrates the complete initialization of all consolidated tools in a single operation. Within minutes, the project is ready to use the full spekificity workflow through `spek` commands and has all skills (spekificity, speckit, caveman) installed and available. While underlying tools remain accessible for direct use, the intended primary workflow is through `spek`.

**why this priority**: This is the primary entry point to the entire platform. `spek` is the user-facing orchestration interface that consolidates multi-tool setup into a seamless, single-command experience. Removing friction from first-time adoption while maintaining the independence of underlying tools is critical.

**independent test**: On a clean machine or fresh project folder, run `spek setup` then `spek init`. Verify all prerequisites are installed or reachable, all spekificity custom skills are available at `.spekificity/skills/spek.*`, all speckit skills are available at `.github/agents/`, project configuration is created, a subsequent `/spek.context-load` command executes without errors, AND verify that underlying tools can still be invoked directly if needed (though the primary workflow is through `spek`).

**acceptance scenarios**:

1. **given** an empty project folder with no tools installed, **when** `spek setup` is run followed by `spek init`, **then** all required prerequisites are installed/verified, all custom and third-party skills are installed to their default locations, and all spekificity files are initialized within 15 minutes (excluding long install times for obsidian/graphify).
2. **given** a project with speckit already globally installed, **when** `spek setup` and `spek init` are run, **then** the existing global speckit installation is reused and `specify init` is called internally to install speckit skills alongside spekificity skills.
3. **given** a project where `spek setup` and `spek init` previously ran successfully, **when** these commands are run again, **then** the operation is idempotent — it updates or verifies state without destroying existing project configuration or custom modifications.
4. **given** a developer chooses to skip obsidian installation (optional), **when** `spek init` completes, **then** the project remains fully functional with spekificity and all third-party tools working with fallback graph storage formats.
5. **given** `spek init` has completed, **when** a developer runs spekificity commands (e.g., `/spek.context-load`), speckit commands (e.g., `/speckit.specify`), or third-party tool CLIs directly, **then** all commands function correctly, demonstrating that all skills and tools are properly installed and integrated.

---

### user story 2 — unified spekificity initialization (priority: p1)

After prerequisites are installed via `spek setup`, a developer runs `spek init` — the primary initialization entry point that orchestrates all component initialization in a single command. `spek init` internally calls `specify init` to initialize speckit, sets up graphify, configures obsidian, integrates caveman, and installs all custom spekificity skills. This is the core value of spekificity: a single command replaces what would otherwise be multiple sequential manual steps (run specify init, copy skills to .github/agents/, copy spekificity skills to .spekificity/, configure graphify, etc.). All skills — spekificity custom skills, speckit skills, and caveman — are installed to their default project locations and are immediately discoverable and available to AI agents. `spek init` is analogous to how `specify init` is the primary entry point for speckit workflows.

**why this priority**: This is the core value proposition of spekificity as a consolidation and automation platform. By making `spek init` the primary entry point that orchestrates all tool initialization, spekificity eliminates the cognitive load and manual effort of multi-tool setup. Users experience a unified initialization process, not a series of independent tool setup steps.

**independent test**: After prerequisites are installed, run `spek init` in a test project. Verify that `.spekificity/` directory structure is created, all spekificity custom skills are present under `.spekificity/skills/spek.*`, all speckit skills are installed (via internal `specify init` call) to their default location (`.github/agents/`), all caveman skills are installed, project configuration file is created (`.spekificity/config.json`), all custom skills (spekificity, speckit, caveman) are discoverable and available immediately, and subsequent `/spek.context-load`, `/speckit.specify`, and caveman commands all work without errors.

**acceptance scenarios**:

1. **given** all prerequisites are installed, **when** `spek init` is run, **then** `specify init` is called internally and all tool initialization steps (graphify, obsidian, caveman) are orchestrated in sequence without user intervention.
2. **given** `spek init` runs, **when** it completes successfully, **then** all custom skill commands (`/spek.context-load`, `/spek.map-codebase`, `/spek.lessons-learnt`, etc.) are available and discoverable by the AI agent under the spekificity namespace, AND all speckit skills are available under the speckit namespace.
3. **given** `spek init` has completed, **when** a developer inspects the project structure, **then** skills are installed to their expected default locations: spekificity skills in `.spekificity/skills/`, speckit skills in `.github/agents/`, caveman skills in their default location, and all are discoverable without additional configuration.
4. **given** a project where `spek init` previously ran, **when** `spek init` is run again, **then** existing project configuration is updated (not reset), custom modifications to skill files are preserved, and `specify init` is re-run cleanly without destroying speckit configuration.
5. **given** spekificity has been initialized via `spek init`, **when** a developer invokes `/spek.context-load` (spekificity skill), `/speckit.specify` (speckit skill), or other commands, **then** all commands function correctly, demonstrating that spekificity's orchestration successfully installed all skills and initialized all tools.

---

### user story 3 — independent spekificity updates (priority: p2)

A developer runs an update command that checks for new versions of spekificity custom skills, workflows, and documentation, and updates only the spekificity layer without touching third-party tools (graphify, obsidian, speckit). This allows teams to maintain their custom skill library independently from global tool updates.

**why this priority**: Long-term platform maintainability and cost efficiency. Teams need to adopt improvements in spekificity custom skills without waiting for or managing third-party tool updates.

**independent test**: After a new version of spekificity is released, a developer runs `spek update`. Verify that custom skills are updated to latest versions, changelog is displayed, no third-party tools are touched, and the update process preserves project-specific customizations.

**acceptance scenarios**:

1. **given** a project with spekificity already initialized, **when** `spek update` is run, **then** only spekificity custom skills, workflows, and documentation are updated — third-party tools (graphify, obsidian, speckit) are not modified.
2. **given** spekificity is updated, **when** the update completes, **then** a changelog is displayed showing what changed, and the AI can immediately invoke updated skill commands without restarting the session.
3. **given** a project with custom modifications to a spekificity skill file, **when** `spek update` runs, **then** the custom modifications are preserved (diff merge) or flagged for manual review if conflicts exist.
4. **given** spekificity is updated and introduces a new skill command, **when** the AI agent consults the skill index, **then** the new command is discoverable and available immediately.

---

### user story 4 — spekificity namespace and abbreviation consistency (priority: p2)

All custom skills, workflows, setup guides, and configuration files created or managed by spekificity use the `spek.` abbreviation and live under the spekificity namespace. This distinguishes spekificity-owned artifacts from speckit-owned artifacts (which use `speckit.` or no prefix), prevents namespace collisions, and makes discoverability clear to users and AI agents.

**why this priority**: Clarity and maintainability. As the platform grows, namespace collision and confusion between third-party and custom tools becomes a significant friction point. Establishing clear naming conventions from the start prevents future refactoring.

**independent test**: On an initialized project, inspect the `.spekificity/skills/` directory and verify all files follow `spek.*` naming pattern. Check `.spekificity/config.json` for configuration schema using spek-prefixed keys. Verify that AI agent command discovery lists all spekificity commands with `/spek.*` prefix and all speckit commands with `/speckit.*` prefix.

**acceptance scenarios**:

1. **given** spekificity is initialized, **when** AI agent lists available commands, **then** all spekificity custom commands are prefixed with `/spek.` (e.g., `/spek.context-load`, `/spek.map-codebase`, `/spek.init-project`, `/spek.update-skills`).
2. **given** spekificity configuration files, **when** they are read or written, **then** all configuration keys use `spek_` or `spek.` prefix (e.g., `spek_initialized`, `spek.version`, `spek.custom_skills`).
3. **given** spekificity skills or workflows are created, **when** they reference each other or third-party commands, **then** the references use proper namespacing: spekificity commands use `/spek.*`, speckit commands use `/speckit.*` or `/specify.*`.
4. **given** documentation for spekificity, **when** users read setup guides or workflow docs, **then** the documentation consistently uses `spek.` abbreviation and explains the namespace distinction clearly.

---

### user story 5 — spekificity configuration persistence (priority: p2)

Spekificity maintains a project-level configuration file that tracks the platform version, installed skills, initialization status, custom preferences, and integration with third-party tools. This configuration is human-readable, version-controllable, and allows teams to define spekificity settings per-project.

**why this priority**: Configuration persistence enables reproducible setups across team members, audit trails for platform changes, and the ability to customize platform behavior per-project.

**independent test**: After `spek init` completes, verify that `.spekificity/config.json` (or equivalent) exists, contains all necessary metadata (version, initialized flag, list of installed skills, speckit integration status), can be version-controlled without conflicts, and is updated correctly by `spek update`.

**acceptance scenarios**:

1. **given** spekificity is initialized, **when** a developer inspects `.spekificity/config.json`, **then** the file contains: spekificity version, initialization timestamp, list of installed skills with versions, speckit integration status, custom preferences, and a schema version for forward compatibility.
2. **given** a project configuration exists, **when** the configuration is committed to git and pulled by another team member, **then** the configuration is valid and the second developer can run `spek init` (or a check command) without errors.
3. **given** spekificity is updated, **when** the update completes, **then** the configuration file is updated with new version info and any new fields are added with sensible defaults.

---

### edge cases

- **Offline/restricted network**: If prerequisite tools cannot be installed, `spek setup` classifies them as hard-required (python, uv, git, speckit) or optional (graphify, obsidian, caveman), provides clear error messaging with manual installation instructions, and allows partial initialization with available tools.
- **Fallback storage if obsidian unavailable**: If obsidian cannot be installed, graph context defaults to JSON format stored in `.spekificity/graph.json` with a markdown-rendered summary in `.spekificity/graph.md` for readability.
- **Namespace collisions**: If a user manually creates a `/spek.*` command that conflicts with spekificity command, `spek status` detects the collision and warns the user. Spekificity command takes precedence; user must rename their custom command.
- **Interrupted setup**: If `spek setup` or `spek init` is interrupted (network failure, user abort), the process can be resumed by re-running the same command. Config state tracks partial failures and recovery guidance is provided.
- **Major version changes**: `spek update` detects breaking changes (new config schema, major skill API changes), displays warnings before applying, and provides rollback guidance if needed. Backward compatibility is maintained via config versioning (schema_version field).
- **Existing speckit initialization**: If a project has both `.spekificity/config.json` and `.github/` from prior speckit initialization, `spek init` detects the existing speckit and reuses it, avoiding conflicts. No files are overwritten without user confirmation.

---

## requirements *(mandatory)*

### functional requirements

- **fr-001**: `spek setup` command must detect and verify all prerequisites (Python 3.11+, uv, git, graphify, obsidian, speckit); install missing tools or provide clear instructions for manual installation. Does NOT replace the original installation or configuration of these tools.
- **fr-002**: `spek init` command must orchestrate and call the initialization functions of all consolidated tools (`specify init`, graphify, obsidian, caveman) in sequence to achieve unified initialization.
- **fr-003**: `spek init` must install all skills to their default project locations automatically, eliminating manual skill copying: (1) Spekificity custom skills install to `.spekificity/skills/spek.*`; (2) Speckit skills install to `.github/agents/speckit.*` (via internal `specify init` call); (3) Caveman skills install to global or project-local location depending on availability. All skills registered in `.spekificity/skill-index.md` for unified discovery.
- **fr-004**: `spek init` must create and populate `.spekificity/config.json` with spekificity version, initialization metadata, list of installed skills, and orchestration history tracking which tool initialization functions were called.
- **fr-005**: `spek init` must be idempotent — running it multiple times updates state without destroying existing configuration or custom modifications. Idempotency rules: (1) Skip prerequisite reinstallation if already verified to correct version; (2) Re-run `specify init` cleanly if speckit version changed or not yet initialized; (3) Update config timestamp and orchestration history; (4) Preserve all user-created files and custom modifications to `.spekificity/` skill files; (5) Enable recovery from partial failures using config state tracking.
- **fr-006**: `spek init` is the primary initialization entry point (analogous to `specify init` for speckit). The intended workflow is to run `spek init` once, which orchestrates all component initialization, rather than manually running separate tool initialization commands.
- **fr-007**: Spekificity must not replace, proxy, or intercept third-party tool functionality. All underlying tools (graphify, obsidian, speckit) must remain directly accessible and functional without spekificity involvement (e.g., `graphify` CLI, `specify` CLI work independently).
- **fr-008**: Spekificity custom skills must explicitly document how they leverage underlying tools (e.g., "/spek.map-codebase internally invokes graphify to generate graphs, then stores them in obsidian format").
- **fr-009**: `spek update` command must check for new versions of spekificity from GitHub releases (https://github.com/marcelrienks/spekificity/releases), download updates, and refresh all custom skills, workflows, and documentation under `.spekificity/`.
- **fr-010**: `spek update` must not modify third-party tool installations (graphify, obsidian, speckit) and must preserve project-specific customizations to spekificity skills.
- **fr-011**: `spek update` must display a changelog summarizing what changed and provide rollback guidance if updates introduce conflicts.
- **fr-012**: All spekificity custom commands must be prefixed with `/spek.` (e.g., `/spek.context-load`, `/spek.map-codebase`, `/spek.lessons-learnt`, `/spek.init-project`, `/spek.update-skills`). Third-party tool commands retain their original namespaces (`/speckit.*`, graphify CLI, etc.).
- **fr-013**: Spekificity configuration keys must use `spek_` or `spek.` prefix in all configuration files and documentation. MUST NOT use or override third-party tool configuration namespaces.
- **fr-014**: `spek setup` and `spek init` must provide clear, step-by-step output so users understand what is happening and can troubleshoot failures. Output must clearly distinguish between spekificity components and third-party tool installation steps.
- **fr-015**: All spekificity documentation, setup guides, and workflow files must reside under `.spekificity/` (or symlinked within the project) and use `spek.` naming convention.
- **fr-016**: Spekificity must provide a `spek status` command that reports: (1) initialization status (initialized/not-initialized), (2) installed version (from `.spekificity/version.txt`), (3) list of available spekificity skills (from `.spekificity/skill-index.md`), (4) integration status with each third-party tool (speckit/graphify/obsidian/caveman: installed/not-installed/optional). This command must NOT intrude on third-party tool status reporting.
- **fr-017**: Spekificity skills must clearly document their namespace (`spek.`), dependencies on underlying tools, and how they integrate with speckit workflows. Documentation must be transparent about which third-party tool is being invoked by each spekificity skill.
- **fr-018**: Spekificity must maintain strict separation between its custom functionality and third-party tool functionality. Configuration, commands, and file structure must clearly indicate ownership (spekificity vs. third-party).

### architectural model: orchestration and consolidation

Spekificity is explicitly designed as a **primary orchestration and consolidation platform** that unifies the initialization and interaction with multiple development tools. While underlying tools retain full independence and can be used directly if needed, the primary intended workflow is through spekificity. The architecture is defined as follows:

**Primary Entry Point (`spek`)**:
- `spek setup` and `spek init` are the primary entry points for users, analogous to how `specify` is the primary entry point for speckit workflows.
- `spek init` internally orchestrates and calls the initialization functions of all consolidated tools: `specify init` (for speckit), graphify setup, obsidian configuration, and caveman integration.
- Users run `spek init` once and all tools are set up, configured, and skills are installed — this is the primary intended interaction model.

**Unified Skill Installation**:
- When `spek init` completes, all skills from all layers are installed and available: spekificity custom skills (under `/spek.*` namespace), speckit skills (under `/speckit.*` namespace via `specify init`), and caveman skills.
- All skills are installed to their default project locations (e.g., `.spekificity/skills/` for spekificity, `.github/agents/` for speckit).
- No manual skill copying or configuration is required — the orchestration handles all installation steps.

**Orchestration without Replacement**:
- Spekificity does NOT replace third-party tools; it orchestrates their initialization and surfaces their capabilities through the unified `spek` interface.
- Third-party tools (speckit, graphify, obsidian, caveman) retain 100% of their original functionality and CAN be used directly if needed, but the primary intended workflow is through `spek` commands.
- Spekificity provides NO proxying, wrapping, or interception of third-party tool behavior — `spek init` simply calls the underlying initialization functions in sequence.

**Custom Skills as Orchestration Agents**:
- Spekificity custom skills (prefixed `/spek.*`) are orchestration commands that combine multiple underlying tools to provide higher-level automation and value.
- Each custom skill clearly documents which third-party tools it invokes and how (e.g., `/spek.map-codebase` calls graphify, then stores results in obsidian vault format).
- Custom skills are purely additive and orchestration-focused — they never shadow or replace third-party tool commands.

**Consolidation Benefits**:
- **Unified entry point**: Users interact with `spek` as the primary platform, not multiple separate tools.
- **Orchestrated initialization**: `spek init` handles calling `specify init`, graphify setup, obsidian config, caveman integration, and custom skill installation in one operation.
- **Skill installation consolidation**: All skills (spekificity, speckit, caveman) are installed automatically to their default locations without manual copying.
- **Configuration consolidation**: `.spekificity/config.json` tracks the state of the entire platform and orchestration history.
- **Namespace consolidation**: Spekificity's `/spek.*` namespace for custom skills keeps orchestration commands distinct from third-party namespaces.

**Automation Benefits**:
- Eliminates manual multi-step initialization (run specify init, copy skills, configure graphify, etc.) — replaced by single `spek init` command.
- Enables reproducible multi-developer setups through orchestrated initialization and `.spekificity/config.json`.
- Provides independent update path for spekificity custom orchestration without affecting third-party tool versions.
- Reduces cognitive load by providing a single, unified platform experience while preserving underlying tool independence.

### key entities

- **Spekificity Config (`.spekificity/config.json`)**: Core metadata file containing version, initialization status, installed skills, speckit integration status, and custom preferences.
- **Spekificity Skills**: Custom AI agent skills under `.spekificity/skills/spek.*` that extend speckit workflows with graph context and token efficiency.
- **Spekificity Workflows**: Workflow documentation under `.spekificity/workflows/` describing feature lifecycle steps and integration patterns.
- **Setup Metadata**: Installation history, prerequisite verification results, and environment information captured during `spek setup`.
- **Project Configuration**: Per-project spekificity settings that allow teams to customize platform behavior, skill activation, and integration preferences.

---

## success criteria *(mandatory)*

### measurable outcomes

- **sc-001**: First-time setup can be completed in under 20 minutes on a clean machine (including tool installation time for graphify and obsidian).
- **sc-002**: `spek init` command executes in under 2 minutes on a project with prerequisites already installed and successfully orchestrates initialization of all consolidated tools.
- **sc-003**: Setup and init commands display clear, actionable output that allows non-technical users to understand status and troubleshoot failures, with explicit indication of which tool initialization steps are being executed.
- **sc-004**: `spek init` installs all skills (spekificity custom skills, speckit skills via orchestrated `specify init`, caveman skills) to their default project locations automatically with zero manual skill copying required.
- **sc-005**: After `spek init` completes, all custom skills are discoverable by AI agents (e.g., `/spek.*` commands, `/speckit.*` commands, caveman skills) within the first session without manual command registration.
- **sc-006**: `spek` is usable as the primary entry point for the entire multi-tool stack, with users running `spek setup` followed by `spek init` as their complete initialization workflow.
- **sc-007**: `spek update` command can refresh all custom skills without breaking existing project configuration, maintaining 100% backward compatibility for configuration files.
- **sc-008**: Documentation for spekificity platform lifecycle (setup, init, update, orchestration model) is clear enough that a new developer can follow it independently without requiring expert guidance.
- **sc-009**: Project configuration (`.spekificity/config.json`) tracks orchestration history and remains stable across major versions of third-party tools and is safely version-controllable across team members.

---

## assumptions

- **Python 3.11+** is available or installable on target systems (used by graphify and spekificity tooling).
- **`uv` package manager** will be the standard installation tool for global prerequisites (speckit, graphify).
- **Git** is already installed in developer environments (prerequisite for version control and spekificity updates).
- **Obsidian** installation is optional for MVP; fallback storage format (JSON or plain files) is acceptable for graph storage if obsidian is unavailable.
- **Third-party tools (speckit, graphify)** follow semantic versioning and maintain backward compatibility; major breaking changes are rare.
- **Project developers have write permissions** to their project directories to create `.spekificity/` and configuration files.
- **Setup script will use shell scripting** (bash/zsh) for Unix-like systems and will provide batch script equivalent or alternative for Windows.
- **Spekificity version is tracked via version file** (e.g., `.spekificity/version.txt` or in `config.json`), not by git tag alone.
- **Custom skill modifications** by users are isolated in specific sections of skill files to minimize conflicts during `spek update`.
- **Configuration schema** is versioned to support forward compatibility and graceful upgrades when new configuration fields are added.
- **No breaking changes to speckit API** will occur during spekificity MVP; spekificity will layer on top without replacing speckit.
- **Spekificity is NOT a replacement layer** — all third-party tools remain fully functional and directly accessible independent of spekificity involvement. Spekificity provides consolidation and orchestration, not proxying or interception.
- **Spekificity is the primary entry point** — while underlying tools CAN be used independently, the intended and primary workflow is through `spek` commands, which orchestrate underlying tools. `spek init` is analogous to `specify init` for speckit — it is the primary initialization command.
- **Orchestration via internal tool invocation** — `spek init` internally calls and orchestrates the initialization functions of consolidated tools (`specify init`, graphify setup, obsidian config, caveman integration) in sequence. This is explicit orchestration, not wrapping or proxying.
- **Unified skill installation** — `spek init` automatically installs all skills (spekificity, speckit, caveman) to their default project locations in a single operation. Users do not manually copy skills or run separate tool init commands.
- **Third-party tool independence** — spekificity setup and initialization do not modify, wrap, or shadow any third-party tool. Each tool retains its original CLI, configuration format, and namespace. However, the primary workflow is through spekificity's orchestration.
- **Custom skills are purely additive orchestration** — spekificity custom skills (prefixed `/spek.*`) add new orchestration commands that invoke underlying tools, but never replace or shadow third-party tool commands.
- **Transparent orchestration** — each spekificity custom skill and the orchestration workflow clearly documents which underlying tools are invoked and how, allowing users to understand the relationship between spekificity and third-party tools.
- **Coexistence of initialization** — `spek init` orchestrates underlying tool initialization (calling `specify init` internally) in a coordinated manner, with zero configuration conflicts or namespace collisions.

---

## dependencies & external integrations

- **Speckit/Specify** (global installation): Primary third-party tool for spec-driven development; spekificity decorates and extends, not replaces. Spekificity custom skills may invoke speckit but do not replace its functionality.
- **Graphify**: Graph generation tool for codebase and documentation mapping; invoked by `/spek.map-codebase` custom skill. Remains independently usable via its own CLI.
- **Obsidian**: Vault storage for persistent graph context; optional for MVP with fallback storage formats. Remains independently usable as a desktop app or CLI tool.
- **Caveman skill**: Token efficiency skill that can be used standalone or integrated into spekificity custom skills for compressed output.
- **GitHub Copilot / Claude Code**: AI agent platforms that execute spekificity commands; requires `.instructions.md` or equivalent discovery mechanism. Spekificity does not interfere with direct use of speckit or other third-party skills on these platforms.
- **Git**: Version control for tracking changes, branching, and storing spekificity configuration. Spekificity does not replace git operations.
- **Python 3.11+**: Runtime for graphify and any custom spekificity tooling.
- **`uv` package manager**: Tool for installing global Python-based prerequisites. Spekificity uses `uv` for prerequisite installation but does not replace or constrain its direct use.



