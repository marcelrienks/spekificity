# implementation tasks: spekificity platform lifecycle

**feature**: spekificity platform lifecycle — setup, init, update | **branch**: `002-spek-platform-lifecycle`  
**spec**: [spec.md](spec.md) | **plan**: [plan.md](plan.md)  
**generated**: 2026-05-03 | **total tasks**: 48 (45 original + 3 remediations)

---

## implementation strategy

**MVP Scope** (US1 + US2): Complete `spek setup` and `spek init` orchestration on primary platform (macOS/Linux). Delivers single unified entry point for all developer tooling. Estimated delivery: 6-8 weeks.

**Phase 2** (US3-US5): Independent updates, namespace consistency, configuration persistence. Estimated: 2-3 weeks.

**Execution Model**: Tasks organized by user story (P1 first, then P2) to enable incremental delivery. Parallel execution possible within phase (e.g., research tasks 1-6 can run in parallel; shell script tasks can parallelize).

**Remediations Applied**:
- ✅ Added T0X0 (spek status command) — FR-016 implementation
- ✅ Added T0X1 (US3 acceptance test) — US3 dedicated acceptance testing
- ✅ Added T0X3 (early platform validation) — catch platform bugs earlier than Polish phase
- ✅ Added D0X (manual setup guide) — AI-executable step-by-step documentation
- ✅ Added D0X2 (migration guide) — moved from Polish to Design phase for early clarity
- ✅ Updated Constitution to clarify shell scripts allowed for orchestration
- ✅ Clarified FR-005 (idempotency rules explicit), FR-003 (skill locations explicit), FR-009 (update source specified), edge cases expanded

**Success Criteria**:
- ✅ `spek setup` detects/installs all prerequisites on clean machine
- ✅ `spek init` orchestrates all tool initialization in sequence
- ✅ `spek status` reports initialization status and tool integration
- ✅ All skills (spekificity, speckit, caveman) installed to default locations
- ✅ `.spekificity/config.json` created with full orchestration state
- ✅ Idempotent re-runs update state without destroying configuration
- ✅ All tasks complete in <2 min with prerequisites installed

---

## task dependency graph

```
Phase 1 (Research)        Phase 2 (Design)        Phase 3 (Implementation)
├─ R1-R6 (parallel)  →   D1-5 + D0X + D0X2   →   T001-T045 + T0X0 + T0X1 + T0X3 (by story)
                         (sequential)             ├─ Setup/Infrastructure (T001-T005)
                                                  ├─ US1: spek setup (T006-T010)
                                                  ├─ Early platform check (T0X3)
                                                  ├─ US2: spek init (T011-T020)
                                                  ├─ US2: spek status (T0X0)
                                                  ├─ US3: spek update (T021-T025)
                                                  ├─ US3: acceptance test (T0X1)
                                                  ├─ US4: Namespace (T026-T030)
                                                  ├─ US5: Config (T031-T035)
                                                  └─ Polish (T036-T045)
```

**Critical Path**: Research (2w) → Design (1w including D0X/D0X2) → Implementation (6-8w) = 9-11 weeks total

**Note**: Early platform validation (T0X3) runs after T010 to catch bugs earlier than Polish phase.

---

## phase 1: research — resolve technical unknowns

### research completion tasks

- [ ] R001 [p] research shell script orchestration patterns
  - **investigation scope**: Study specify init workflow; analyze graphify/obsidian/caveman setup; document error handling
  - **deliverable**: Flow diagram, conditional paths, rollback strategy
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 1)
  - **time estimate**: 2-3 days

- [ ] R002 [p] research skill installation and discovery strategy
  - **investigation scope**: AI agent skill discovery mechanisms; manifest format; namespace isolation
  - **deliverable**: Unified discovery architecture; config format; AI integration points
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 2)
  - **time estimate**: 2-3 days

- [ ] R003 [p] research configuration schema and state tracking
  - **investigation scope**: Config versioning; idempotency rules; migration strategy
  - **deliverable**: `.spekificity/config.json` schema v1.0; idempotency semantics
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 3)
  - **time estimate**: 2-3 days

- [ ] R004 [p] research update strategy for spekificity custom layer
  - **investigation scope**: Diff-merge; conflict detection; rollback; changelog generation
  - **deliverable**: Update architecture; conflict resolution; rollback procedure
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 4)
  - **time estimate**: 1-2 days

- [ ] R005 [p] research multi-platform support (macOS/Linux/Windows)
  - **investigation scope**: Bash vs. zsh; platform detection; package managers; installer availability
  - **deliverable**: Platform detection strategy; prerequisite paths; testing plan
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 5)
  - **time estimate**: 2-3 days

- [ ] R006 [p] research prerequisite availability and fallback behavior
  - **investigation scope**: Hard-required vs. optional; graceful degradation; error messaging
  - **deliverable**: Prerequisite tiers; fallback behavior; error messages; offline testing
  - **file**: `specs/002-spek-platform-lifecycle/research.md` (section 6)
  - **time estimate**: 1-2 days

---

## phase 2: design — create implementation artifacts

### design document creation tasks

- [ ] D001 → R001-R006 research tasks completed
  - **file**: research.md fully documented

- [ ] D002 [us1] [us2] create data-model.md with entity definitions and config schema
  - **deliverables**: 
    - Orchestration State entity (fields, relationships)
    - Setup Prerequisite entity (tool metadata)
    - Skill Layer entity (namespace, directory, availability)
    - Orchestration Step entity (workflow actions)
    - `.spekificity/config.json` schema v1.0 with JSON examples
  - **file**: `specs/002-spek-platform-lifecycle/data-model.md`
  - **time estimate**: 2-3 days
  - **blocks**: T001 (config implementation), T003 (schema validation)

- [ ] D003 [us1] [us2] create three interface contracts
  - **deliverables**:
    - `specs/002-spek-platform-lifecycle/contracts/orchestration-contract.md` — how spek init calls underlying tools
    - `specs/002-spek-platform-lifecycle/contracts/skill-installation-contract.md` — skill discovery, namespace isolation
    - `specs/002-spek-platform-lifecycle/contracts/idempotency-contract.md` — safe re-run guarantees
  - **files**: 3 contract files
  - **time estimate**: 2-3 days
  - **blocks**: T002 (skill index), T004 (idempotency test)

- [ ] D004 [us1] [us2] create quickstart.md user guide
  - **deliverables**: 5-min overview, installation steps, init workflow, first feature dev, troubleshooting basics
  - **file**: `specs/002-spek-platform-lifecycle/quickstart.md`
  - **time estimate**: 2 days

- [ ] D005 [us1] [us2] update .github/copilot-instructions.md for spekificity platform
  - **deliverables**: Clarify spek as primary entry point; document skill index; link orchestration docs; reference skill dev guide
  - **file**: `.github/copilot-instructions.md` (add spekificity section)
  - **time estimate**: 1 day

- [ ] D0X [p] create manual setup guide for AI agents and offline environments
  - **deliverables**:
    - Create markdown guide: `.spekificity/guides/manual-setup.md`
    - Step-by-step instructions for running `spek setup` manually if shell scripts not directly executable by AI agents
    - Instructions for each platform (macOS, Linux, Windows/WSL)
    - Commands for each prerequisite check and installation step
    - Error recovery guidance for each failure scenario
    - Offline setup instructions for restricted network environments
  - **file**: `.spekificity/guides/manual-setup.md`
  - **time estimate**: 1-2 days
  - **blocks**: T036 (end-to-end testing can verify manual path)
  - **note**: Ensures Constitution Principle VII (AI-executable setup) compliance

- [ ] D0X2 [p] create migration guide for existing users
  - **deliverables**:
    - Create guide: `specs/002-spek-platform-lifecycle/guides/migration.md`
    - Instructions for users already using speckit, graphify, obsidian independently
    - How to adopt spekificity without breaking existing setup
    - Backward compatibility guarantees: existing projects continue working without modification
    - Gradual adoption strategy: opt-in to spekificity features
    - Examples: converting manual speckit init to `spek init`, reusing existing .github/agents, etc.
  - **file**: `specs/002-spek-platform-lifecycle/guides/migration.md`
  - **time estimate**: 1-2 days
  - **note**: Moved from Polish phase (T041) to Design phase for early clarity

- [ ] D0X [p] create manual setup guide for AI agents and offline environments
  - **deliverables**:
    - Create markdown guide: `.spekificity/guides/manual-setup.md`
    - Step-by-step instructions for running `spek setup` manually if shell scripts not directly executable by AI agents
    - Instructions for each platform (macOS, Linux, Windows/WSL)
    - Commands for each prerequisite check and installation step
    - Error recovery guidance for each failure scenario
    - Offline setup instructions for restricted network environments
  - **file**: `.spekificity/guides/manual-setup.md`
  - **time estimate**: 1-2 days
  - **blocks**: T036 (end-to-end testing can verify manual path)

- [ ] D0X2 [p] create migration guide for existing users
  - **deliverables**:
    - Create guide: `specs/002-spek-platform-lifecycle/guides/migration.md`
    - Instructions for users already using speckit, graphify, obsidian independently
    - How to adopt spekificity without breaking existing setup
    - Backward compatibility guarantees: existing projects continue working without modification
    - Gradual adoption strategy: opt-in to spekificity features
    - Examples: converting manual speckit init to `spek init`, reusing existing .github/agents, etc.
  - **file**: `specs/002-spek-platform-lifecycle/guides/migration.md`
  - **time estimate**: 1-2 days
  - **blocks**: T041 (no need to duplicate in Polish phase)

---

## phase 3: implementation — core infrastructure setup

### shared infrastructure tasks

- [ ] T001 [p] create .spekificity/ directory structure and version tracking
  - **deliverables**:
    - Create `.spekificity/` root directory (local per-project)
    - Create subdirectories: `setup-scripts/`, `skills/`, `workflows/`, `guides/`
    - Create `.spekificity/version.txt` (current: 1.0.0)
    - Create `.spekificity/README.md` explaining directory structure
  - **file**: `.spekificity/` (all subdirectories)
  - **blocks**: All subsequent implementation tasks
  - **time estimate**: 1 day

- [ ] T002 [p] [us2] implement .spekificity/config.json schema and handler
  - **deliverables**:
    - JSON schema file (`.spekificity/config-schema.json`)
    - Bash function `initialize_config()` to create default config
    - Bash function `update_config()` to modify tracked fields
    - Bash function `read_config()` to load and parse config
    - Config versioning and migration support
  - **file**: `.spekificity/config.json` template; shell functions in `.spekificity/setup-scripts/config-handler.sh`
  - **time estimate**: 2-3 days
  - **dependencies**: D002, T001

- [ ] T003 [p] [us2] implement .spekificity/skill-index.md unified skill discovery
  - **deliverables**:
    - Skill index template with sections: spekificity skills, speckit skills, caveman skills
    - Bash function `update_skill_index()` to auto-generate from discovered skills
    - Index includes skill name, namespace, description, location, version
    - Index is updateable and version-controllable
  - **file**: `.spekificity/skill-index.md`; shell functions in `.spekificity/setup-scripts/skill-discovery.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: D003 (skill-installation-contract)

- [ ] T004 [p] [us2] implement idempotency tracking and state validation
  - **deliverables**:
    - Bash function `is_already_initialized()` using config state
    - Bash function `detect_partial_failure()` to identify interrupted setups
    - Bash function `validate_prerequisites()` to check tool versions
    - Recovery guidance for each partial failure scenario
  - **file**: `.spekificity/setup-scripts/idempotency.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: D001 (idempotency-contract), T002

- [ ] T005 [p] [us1] [us2] create shared logging and status output system
  - **deliverables**:
    - Bash functions: `log_step()`, `log_success()`, `log_error()`, `log_warning()`
    - Structured output showing spekificity component vs. third-party tool steps
    - Color coding for different message types (info, success, error, warning)
    - Verbose mode flag `--verbose` for debugging
  - **file**: `.spekificity/setup-scripts/logging.sh`
  - **time estimate**: 1 day

---

## phase 4: implementation — user story 1 (P1) setup orchestration

### US1: Single-command project setup — spek setup

- [ ] T006 [p] [us1] implement prerequisite detection for Python 3.11+
  - **deliverables**:
    - Bash function `check_python()` — detect Python version, locate executable
    - Fallback to `python`, `python3`, or system PATH
    - Error message with installation instructions
    - Handle version checking (3.11+ required)
  - **file**: `.spekificity/setup-scripts/prerequisites.sh`
  - **time estimate**: 1 day

- [ ] T007 [p] [us1] implement prerequisite detection for uv and git
  - **deliverables**:
    - Bash functions: `check_uv()`, `check_git()`
    - Detect versions; locate executables; error handling with install instructions
    - Uv installation via curl/pip if missing
    - Git detection (usually pre-installed on dev machines)
  - **file**: `.spekificity/setup-scripts/prerequisites.sh`
  - **time estimate**: 1 day

- [ ] T008 [p] [us1] implement prerequisite detection for speckit, graphify, obsidian
  - **deliverables**:
    - Bash function `check_speckit()` — detect global speckit; provide install guidance
    - Bash function `check_graphify()` — detect graphify; installation options
    - Bash function `check_obsidian()` — detect Obsidian desktop app; mark as optional
    - Graceful handling of missing optional tools
  - **file**: `.spekificity/setup-scripts/prerequisites.sh`
  - **time estimate**: 1-2 days

- [ ] T009 [p] [us1] implement platform detection and conditional prerequisite installation
  - **deliverables**:
    - Bash function `detect_platform()` — identify OS (macOS, Linux, Windows/WSL)
    - Bash function `install_prerequisites()` — conditional installation by platform
    - Platform-specific package manager logic (brew for macOS, apt for Ubuntu, etc.)
    - Error handling and user guidance for restricted environments
  - **file**: `.spekificity/setup-scripts/platform.sh`
  - **time estimate**: 2 days
  - **dependencies**: T006, T007, T008, R005 (multi-platform research)

- [ ] T010 [us1] implement spek setup command (main entry point)
  - **deliverables**:
    - Main script: `.spekificity/setup-scripts/setup.sh`
    - Orchestrates: platform detection → prerequisite checking → installation
    - Status reporting at each step
    - Error recovery and retry guidance
    - Summary report showing what was installed/verified
    - Exit code 0 if all prerequisites ready, non-zero if failures
  - **file**: `.spekificity/setup-scripts/setup.sh`
  - **blocks**: T011 (spek init requires setup to complete)
  - **time estimate**: 2 days
  - **dependencies**: T001-T009, T005 (logging system)

---

## phase 5: implementation — user story 2 (P1) unified init orchestration

### US2: Unified spekificity initialization — spek init

- [ ] T011 [p] [us2] implement specify init orchestration in spek init
  - **deliverables**:
    - Bash function `orchestrate_specify_init()` — call `specify init` with correct flags
    - Capture speckit initialization status
    - Error handling if specify init fails
    - Idempotency check: skip if already initialized
    - Update config with speckit initialization status
  - **file**: `.spekificity/setup-scripts/init.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: T010 (setup completes), T002 (config handler), D001 (orchestration-contract)

- [ ] T012 [p] [us2] implement graphify setup orchestration in spek init
  - **deliverables**:
    - Bash function `orchestrate_graphify()` — initialize graphify for project
    - Generate initial project graph if needed
    - Detect existing graphify state; skip if already initialized
    - Update config with graphify initialization status
  - **file**: `.spekificity/setup-scripts/init.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: T011, R001 (orchestration patterns)

- [ ] T013 [p] [us2] implement obsidian vault setup orchestration in spek init
  - **deliverables**:
    - Bash function `orchestrate_obsidian()` — configure Obsidian vault location
    - Optional: handle case where Obsidian is not installed (graceful fallback)
    - Set up vault in `.obsidian/` or user-specified location
    - Update config with obsidian initialization status
  - **file**: `.spekificity/setup-scripts/init.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: T012, R006 (fallback behavior)

- [ ] T014 [p] [us2] implement caveman skill integration in spek init
  - **deliverables**:
    - Bash function `orchestrate_caveman()` — detect and integrate caveman skill
    - Check if caveman available in environment
    - Create caveman integration marker if available
    - Update config with caveman integration status
  - **file**: `.spekificity/setup-scripts/init.sh`
  - **time estimate**: 1 day
  - **dependencies**: T013

- [ ] T015 [p] [us2] implement spekificity custom skill installation in spek init
  - **deliverables**:
    - Bash function `install_spek_skills()` — populate `.spekificity/skills/` directory
    - Copy skill files: spek.context-load.md, spek.map-codebase.md, spek.lessons-learnt.md, etc.
    - Create skill templates for future extensibility
    - Register skills in skill-index.md
  - **file**: `.spekificity/setup-scripts/init.sh`; skill files in `.spekificity/skills/`
  - **time estimate**: 1-2 days
  - **dependencies**: T014, T003 (skill index)

- [ ] T016 [p] [us2] implement workflow documentation installation in spek init
  - **deliverables**:
    - Create workflow files: `setup-workflow.md`, `init-workflow.md`, `update-workflow.md`, `integration-guide.md`
    - Copy to `.spekificity/workflows/`
    - Define integration patterns showing how skills invoke underlying tools
  - **file**: `.spekificity/workflows/` (4 workflow files)
  - **time estimate**: 2 days
  - **dependencies**: T015

- [ ] T017 [p] [us2] implement guides and documentation installation in spek init
  - **deliverables**:
    - Create guides: `architecture.md`, `orchestration-model.md`, `skill-development.md`, `troubleshooting.md`
    - Copy to `.spekificity/guides/`
    - Make documentation discoverable and readable from project root
  - **file**: `.spekificity/guides/` (4 guide files)
  - **time estimate**: 2 days
  - **dependencies**: D005 (architecture documented)

- [ ] T018 [us2] implement spek init command (main orchestration entry point)
  - **deliverables**:
    - Main script: `.spekificity/setup-scripts/init.sh` (orchestration sequence)
    - Validate setup has completed (check if prerequisites installed)
    - Execute orchestration steps in sequence: specify init → graphify → obsidian → caveman → skills install → workflows → guides
    - Track each step in config with timestamps
    - Error handling: detailed messages showing which step failed
    - Rollback or recovery guidance
    - Summary report showing all tools initialized, all skills installed, project ready
  - **file**: `.spekificity/setup-scripts/init.sh`
  - **time estimate**: 2 days
  - **dependencies**: T011-T017, T005 (logging)

- [ ] T019 [us2] create shell alias/wrapper for spek commands (spek setup, spek init, spek update)
  - **deliverables**:
    - Main `spek` script or shell function that dispatches: `spek setup`, `spek init`, `spek update`, `spek status`
    - Add to project root or `.spekificity/bin/spek`
    - Integration guidance for users: add to PATH or create shell alias
    - Cross-platform support (bash/zsh on macOS/Linux; batch script for Windows optional)
  - **file**: `.spekificity/bin/spek` (or equivalent)
  - **time estimate**: 1 day
  - **dependencies**: T010, T018

- [ ] T0X0 [p] [us1] [us2] implement spek status command (main entry point)
  - **deliverables**:
    - Main script: `.spekificity/setup-scripts/status.sh`
    - Output: initialization status, installed version, list of available spekificity skills, integration status with each third-party tool
    - Status shows: speckit (installed/not-installed), graphify (installed/not-installed), obsidian (installed/optional), caveman (available/not-available)
    - Human-readable format; machine-readable JSON output with `--json` flag
    - Exit code 0 if initialized, 1 if not
  - **file**: `.spekificity/setup-scripts/status.sh`
  - **time estimate**: 1 day
  - **dependencies**: T002 (config handler), T003 (skill index)

- [ ] T020 [us2] [p] acceptance testing: US2 setup and init workflow
  - **deliverables**:
    - Create test scenario document: clean machine setup test (or VM/docker)
    - Run `spek setup` → verify all prerequisites detected
    - Run `spek init` → verify all tools initialized, all skills installed, config created
    - Run `/spek.context-load` → verify custom skill works
    - Run `/speckit.specify` → verify speckit skill works
    - Run `spek init` again → verify idempotency (state updated, not reset)
    - Document test results and any issues
  - **file**: `specs/002-spek-platform-lifecycle/acceptance-tests/US2-unified-init.md`
  - **time estimate**: 2-3 days
  - **dependencies**: T018, T004 (idempotency)

---

## phase 6: implementation — user story 3 (P2) independent updates

### US3: Independent spekificity updates — spek update

- [ ] T021 [us3] implement version checking for spekificity
  - **deliverables**:
    - Bash function `get_current_version()` — read `.spekificity/version.txt`
    - Bash function `get_latest_version()` — query remote (GitHub releases or equivalent)
    - Version comparison logic
  - **file**: `.spekificity/setup-scripts/update.sh`
  - **time estimate**: 1 day
  - **dependencies**: T001

- [ ] T022 [us3] implement skill and workflow update mechanism
  - **deliverables**:
    - Bash function `download_skill_files()` — fetch updated skills from remote
    - Bash function `merge_skill_files()` — diff-merge to preserve user customizations
    - Conflict detection and user notification
    - Backup previous versions before update
  - **file**: `.spekificity/setup-scripts/update.sh`
  - **time estimate**: 2 days
  - **dependencies**: R004 (update strategy research)

- [ ] T023 [us3] implement changelog generation and display
  - **deliverables**:
    - Bash function `generate_changelog()` — extract change info from remote
    - Bash function `display_changelog()` — show changes to user before applying
    - Changelog includes: new skills, updated workflows, bug fixes, breaking changes
  - **file**: `.spekificity/setup-scripts/update.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: T022, R004

- [ ] T024 [us3] implement rollback mechanism for failed updates
  - **deliverables**:
    - Bash function `backup_current_state()` — save skill files before update
    - Bash function `rollback_update()` — restore previous version if update fails
    - User guidance: how to manually rollback if needed
  - **file**: `.spekificity/setup-scripts/update.sh`
  - **time estimate**: 1 day
  - **dependencies**: T022

- [ ] T025 [us3] implement spek update command (main entry point)
  - **deliverables**:
    - Main script: `.spekificity/setup-scripts/update.sh`
    - Orchestrates: version check → changelog display → user confirmation → skill download → merge → update config → success/error reporting
    - Ensures third-party tools (graphify, obsidian, speckit) are NOT modified
    - Preserve project customizations
    - Update skill-index.md with new skills
  - **file**: `.spekificity/setup-scripts/update.sh`
  - **time estimate**: 2 days
  - **dependencies**: T021-T024, T002 (config update)

- [ ] T0X1 [us3] [p] acceptance testing: US3 independent update workflow
  - **deliverables**:
    - Create test scenario document detailing update acceptance tests
    - Scenario 1: Run `spek update` when new version available; verify changelog displayed; verify skills updated; verify config version incremented
    - Scenario 2: Verify third-party tools (graphify, obsidian, speckit) are NOT modified by update
    - Scenario 3: Modify a custom spekificity skill file; run `spek update`; verify custom modifications preserved (diff-merge)
    - Scenario 4: Run `spek update` with conflicts; verify user notification and conflict resolution guidance
    - Scenario 5: Run `spek update` and fail mid-way; run again; verify recovery without corruption
    - Document all test results and any issues
  - **file**: `specs/002-spek-platform-lifecycle/acceptance-tests/US3-independent-update.md`
  - **time estimate**: 2 days
  - **dependencies**: T025, T022 (diff-merge), T024 (rollback)

---

## phase 7: implementation — user story 4 (P2) namespace consistency

### US4: Spekificity namespace and abbreviation consistency

- [ ] T026 [us4] validate all spekificity skills use spek.* prefix
  - **deliverables**:
    - Audit all skill files in `.spekificity/skills/` — verify naming: spek.context-load.md, spek.map-codebase.md, etc.
    - Create linting script to validate namespace adherence
    - Document naming standard in skill-development.md
  - **file**: `.spekificity/guides/skill-development.md`; `.spekificity/setup-scripts/validate-namespace.sh`
  - **time estimate**: 1 day
  - **dependencies**: D005 (skill-development guide)

- [ ] T027 [us4] validate configuration keys use spek_ or spek. prefix
  - **deliverables**:
    - Audit `.spekificity/config.json` schema — verify all keys use spek_ or spek. prefix
    - Document namespace standards for config in architecture.md
    - Create validation function to check config conformance
  - **file**: `.spekificity/guides/architecture.md`; `.spekificity/setup-scripts/validate-config-namespace.sh`
  - **time estimate**: 1 day
  - **dependencies**: T002 (config handler), D002 (data-model)

- [ ] T028 [us4] [p] document namespace distinction in copilot-instructions.md
  - **deliverables**:
    - Extend `.github/copilot-instructions.md` with namespace clarity section
    - Explain: `/spek.*` for spekificity, `/speckit.*` for speckit, caveman skill access
    - Provide command discovery instructions for AI agents
  - **file**: `.github/copilot-instructions.md`
  - **time estimate**: 1 day
  - **dependencies**: D005 (copilot-instructions update)

- [ ] T029 [us4] [p] create namespace consistency checklist and validation guide
  - **deliverables**:
    - Comprehensive checklist: skills naming, config keys, documentation references, command invocations
    - Validation script to check entire project for namespace violations
    - Troubleshooting guide: how to identify and fix namespace issues
  - **file**: `specs/002-spek-platform-lifecycle/checklists/namespace-consistency.md`; `.spekificity/setup-scripts/validate-all-namespaces.sh`
  - **time estimate**: 1-2 days

- [ ] T030 [us4] acceptance testing: namespace consistency verification
  - **deliverables**:
    - Run namespace validation scripts on initialized project
    - Verify AI agent recognizes all spekificity commands with `/spek.*` prefix
    - Verify no namespace collisions between spekificity and speckit commands
    - Document test results
  - **file**: `specs/002-spek-platform-lifecycle/acceptance-tests/US4-namespace.md`
  - **time estimate**: 1 day
  - **dependencies**: T026-T029

---

## phase 8: implementation — user story 5 (P2) configuration persistence

### US5: Spekificity configuration persistence

- [ ] T031 [us5] implement configuration schema versioning and migration
  - **deliverables**:
    - Add schema version field to config (current: 1.0)
    - Create migration framework to handle future schema changes
    - Bash function `migrate_config()` to upgrade old schema versions
    - Backward compatibility: handle configs from v0.9 in future
  - **file**: `.spekificity/setup-scripts/config-handler.sh`
  - **time estimate**: 1-2 days
  - **dependencies**: T002 (config handler), D002 (data-model)

- [ ] T032 [us5] implement project configuration customization framework
  - **deliverables**:
    - Bash function `set_config_preference()` — allow per-project customization
    - Document customizable fields: skill activation, tool preferences, update frequency, etc.
    - Configuration file readable and editable by users
    - Preserve user customizations across updates
  - **file**: `.spekificity/setup-scripts/config-handler.sh`; `.spekificity/guides/configuration.md`
  - **time estimate**: 1-2 days
  - **dependencies**: T031

- [ ] T033 [us5] implement orchestration history tracking
  - **deliverables**:
    - Add orchestration_history array to config.json
    - Bash function `record_orchestration_step()` — log each init/setup/update step
    - Track: step name, status (success/failure), timestamp, error message (if failure)
    - Enable audit trail and debugging
  - **file**: `.spekificity/setup-scripts/config-handler.sh`
  - **time estimate**: 1 day
  - **dependencies**: T002

- [ ] T034 [us5] implement configuration validation and repair
  - **deliverables**:
    - Bash function `validate_config()` — check config.json schema compliance
    - Bash function `repair_config()` — add missing fields with defaults
    - Error messages: what's wrong, how to fix it
    - Recovery guidance for corrupted config
  - **file**: `.spekificity/setup-scripts/config-handler.sh`
  - **time estimate**: 1 day
  - **dependencies**: T031, T032

- [ ] T035 [us5] acceptance testing: configuration persistence and reproducibility
  - **deliverables**:
    - Create two test scenarios: (1) local team setup, (2) CI/CD environment
    - Run `spek init` on machine A; commit config; pull on machine B; run `spek init` again
    - Verify config is valid, no conflicts, project is initialized correctly
    - Test configuration customization: modify config, re-run `spek init`, verify customizations preserved
    - Document test results and any edge cases
  - **file**: `specs/002-spek-platform-lifecycle/acceptance-tests/US5-config-persistence.md`
  - **time estimate**: 2 days
  - **dependencies**: T031-T034

---

## phase 9: polish and finalization

### comprehensive testing and documentation

- [ ] T036 [p] [p] end-to-end acceptance test: full workflow (setup → init → use)
  - **deliverables**:
    - Clean machine (VM or container) test: `spek setup` → `spek init` → run `/spek.context-load` → run `/speckit.specify` → verify all working
    - Document full test scenario with screenshots/logs
    - Performance metrics: setup time, init time, first command latency
    - Success criteria: all tasks complete, no errors, reproducible across platforms
  - **file**: `specs/002-spek-platform-lifecycle/acceptance-tests/e2e-workflow.md`
  - **time estimate**: 3-4 days
  - **dependencies**: T020, T0X1 (US3 test), T035

- [ ] T0X3 [p] multi-platform validation (macOS, Linux, early smoke test)
  - **deliverables**:
    - Quick smoke test after T010 completes to catch platform-specific bugs early
    - Test on macOS (primary): `spek setup` detection phase on at least 2 macOS versions (if available)
    - Test on Ubuntu Linux VM: `spek setup` detection phase
    - Document any platform-specific prerequisite detection issues
    - Document bash vs zsh compatibility issues (if any)
    - Full end-to-end test deferred to T037 in Polish phase
  - **file**: `specs/002-spek-platform-lifecycle/validation/early-platform-check.md`
  - **time estimate**: 1-2 days (quick validation only)
  - **dependencies**: T010

- [ ] T037 [p] comprehensive multi-platform validation (macOS, Linux, Windows/WSL optional)
  - **deliverables**:
    - Full end-to-end test on macOS (primary): `spek setup` and `spek init` complete workflow
    - Full end-to-end test on Ubuntu Linux: `spek setup` and `spek init` complete workflow
    - Document any platform-specific differences or workarounds discovered
    - Verify all commands (`spek setup`, `spek init`, `spek update`, `spek status`, `/spek.*` skills) work correctly on both platforms
    - Windows support (optional for MVP): assess feasibility or plan for Phase 2
  - **file**: `specs/002-spek-platform-lifecycle/validation/comprehensive-platform-matrix.md`
  - **time estimate**: 2-3 days
  - **dependencies**: T0X3 (early check done), T018, T0X0, T025, T036

- [ ] T038 [p] idempotency and recovery testing
  - **deliverables**:
    - Test 1: Run `spek init` twice → verify second run updates state without destroying config
    - Test 2: Interrupt `spek init` mid-way → run again → verify recovery
    - Test 3: Corrupt config → run `spek init` → verify repair/recovery
    - Document all scenarios and outcomes
  - **file**: `specs/002-spek-platform-lifecycle/validation/idempotency-testing.md`
  - **time estimate**: 2-3 days
  - **dependencies**: T004 (idempotency), T020

- [ ] T039 [p] complete quickstart guide with real examples
  - **deliverables**:
    - Extend `quickstart.md` with: actual commands to run, expected output, troubleshooting tips
    - Step-by-step walkthroughs for: new developer, existing project, updates
    - Links to detailed documentation (guides, contracts, architecture)
    - Real console output examples
  - **file**: `specs/002-spek-platform-lifecycle/quickstart.md`
  - **time estimate**: 2 days
  - **dependencies**: D004 (quickstart template)

- [ ] T040 [p] create troubleshooting guide and error messages
  - **deliverables**:
    - Common errors: missing prerequisite, network failure, permission denied, etc.
    - For each error: explanation, cause, solution, recovery steps
    - Error messages in shell scripts improved to reference troubleshooting guide
    - FAQ section addressing likely user questions
  - **file**: `.spekificity/guides/troubleshooting.md`
  - **time estimate**: 2 days

- [ ] T042 [p] create developer guide for skill extension and customization
  - **deliverables**:
    - Template for creating new `/spek.*` skills
    - Guidelines for skill documentation, namespace, integration testing
    - Examples: extending existing skills, creating new skill layer
    - Contribution guidelines for spekificity maintenance
  - **file**: `.spekificity/guides/skill-development.md`
  - **time estimate**: 2 days

- [ ] T043 [p] documentation review and cross-linking
  - **deliverables**:
    - Audit all documentation: architecture.md, orchestration-model.md, contracts, guides
    - Add cross-links between related documents
    - Ensure terminology consistency
    - Update table of contents and documentation index
    - Create documentation site structure (if applicable)
  - **file**: multiple docs updated; new `.spekificity/docs/index.md` created
  - **time estimate**: 2 days
  - **dependencies**: T017, T040-T042

- [ ] T044 [p] update project README and top-level docs
  - **deliverables**:
    - Update main `/README.md` to reference spekificity platform
    - Add quick links: `spek setup`, `spek init`, quickstart guide
    - Update `.github/copilot-instructions.md` with finalized spekificity references
    - Add spekificity to `/docs/architecture.md` if exists
  - **files**: `/README.md`, `.github/copilot-instructions.md`, `/docs/`
  - **time estimate**: 1 day
  - **dependencies**: T043

- [ ] T045 [p] final git commit and PR preparation
  - **deliverables**:
    - Commit all implementation changes to feature branch `002-spek-platform-lifecycle`
    - Create PR description summarizing: requirements met, user stories completed, testing results, remediations applied (FR-016, idempotency clarification, fallback format, update source, early platform testing, migration guide moved to Design phase)
    - Verification: all tasks complete, all acceptance tests pass, documentation reviewed
    - Ready for code review and merge
  - **file**: Git PR body; feature branch contains all deliverables
  - **time estimate**: 1-2 days
  - **dependencies**: All preceding tasks (T001-T044, T0X0, T0X1, T0X3)

---

## task execution model

### parallel execution opportunities

**Research Phase** (R001-R006): All research tasks can run in parallel. Estimated delivery: 2 weeks

**Design Phase** (D001-D005): Sequential dependency: research → design. Estimated delivery: 1 week

**Implementation Phase** (T001-T045):
- **Infrastructure** (T001-T005): Run first, sequential
- **US1 Setup** (T006-T010): Parallel after infrastructure, ~2 weeks
- **US2 Init** (T011-T020): Parallel after setup complete, ~2 weeks
- **US3 Update** (T021-T025): Parallel after init complete, ~1 week
- **US4 Namespace** (T026-T030): Can overlap with other US tasks, ~1 week
- **US5 Config** (T031-T035): Can overlap with other US tasks, ~1 week
- **Polish** (T036-T045): After all US tasks complete, ~2 weeks

**Estimated Total**: 9-11 weeks

### success verification

**Per User Story**:
- ✅ US1: `spek setup` completes successfully on clean machine; all prerequisites detected
- ✅ US2: `spek init` orchestrates all tools; all skills installed; config created; idempotent
- ✅ US3: `spek update` updates custom layer without touching third-party tools
- ✅ US4: All commands follow namespace conventions; no collisions
- ✅ US5: Config.json created and maintained; team reproducibility verified

**End-to-End**:
- ✅ Feature branch merged to main
- ✅ All acceptance tests pass
- ✅ Documentation complete and reviewable
- ✅ No regressions to existing spekificity workflows
- ✅ Underlying tools (speckit, graphify, obsidian, caveman) fully functional through both `spek` and direct invocation

---

## dependencies & blockers

| Task | Depends On | Blocks |
|------|-----------|--------|
| T001 | None | All infrastructure tasks |
| T002 | D002, T001 | T004, T018, T031 |
| T003 | D003, T001 | T015, T019 |
| T004 | D001, T002 | T020 (acceptance testing) |
| T005 | T001 | T010, T018 (logging in all scripts) |
| T006-T008 | T001 | T009 |
| T009 | T006-T008, R005 | T010 |
| T010 | T001-T009, T005 | T011 (setup must complete before init) |
| T011-T017 | T010, T002, T003 | T018 |
| T018 | T011-T017, T005 | T019, T020 |
| T019 | T010, T018 | User accessibility of spek commands |
| T020 | T018, T004 | MVP validation |
| T021-T025 | T002 | Spek update capability |
| T026-T030 | D005 | Namespace validation |
| T031-T035 | T002, D002 | Configuration persistence |
| T036-T045 | T020, T030, T035 | Release/merge readiness |

---

## checklist by delivery phase

### Phase 1: MVP (US1 + US2) — Weeks 1-8

- [ ] R001-R006 completed (2 weeks, parallel)
- [ ] D001-D005 completed (1 week, sequential after research)
- [ ] D0X + D0X2 completed (Design phase enhancements)
- [ ] T001-T005 completed (1 week)
- [ ] T006-T010 completed (2 weeks)
- [ ] T0X3 (early platform check) completed (1-2 days after T010)
- [ ] T011-T020 completed (2 weeks)
- [ ] T0X0 (spek status) completed (1 day)
- [ ] All acceptance tests pass (T020 + T036 partial)
- [ ] MVP ready for team review and merge

### Phase 2: Completeness (US3-US5) — Weeks 9-10

- [ ] T021-T035 completed (2 weeks)
- [ ] T0X1 (US3 acceptance test) completed (2 days)
- [ ] All user story acceptance tests pass
- [ ] Namespace and config validation complete

### Phase 3: Polish (T036-T045) — Weeks 11+

- [ ] End-to-end testing complete (T036)
- [ ] Comprehensive multi-platform validation complete (T037)
- [ ] All documentation finalized
- [ ] PR ready for merge
- [ ] Feature branch merged to main

---

## remediations applied

✅ **Constitution Principle I Clarification**: Updated to explicitly permit shell scripts for orchestration automation when paired with markdown documentation

✅ **FR-016 Added**: New requirement for `spek status` command with full specification

✅ **FR-005 Clarified**: Explicit idempotency rules documented (skip vs. re-run vs. version-check semantics)

✅ **FR-003 Clarified**: Explicit skill installation locations documented (`.spekificity/skills/`, `.github/agents/`, etc.)

✅ **FR-009 Clarified**: Update source specified (GitHub releases)

✅ **Edge Cases Expanded**: Fallback storage format (.spekificity/graph.json), offline scenarios, namespace collision handling, interrupted setup recovery, major version handling, existing speckit coexistence

✅ **Tasks Added**:
- T0X0: spek status command implementation
- T0X1: US3 acceptance testing
- T0X3: Early platform validation (moved from Polish)
- D0X: Manual setup guide for AI agents
- D0X2: Migration guide (moved from Polish to Design phase)

✅ **Task Reordering**: Multi-platform validation split into early check (T0X3 after T010) + comprehensive check (T037 in Polish phase)

✅ **Documentation Enhanced**: All ambiguities clarified, terminology standardized, redundant sections consolidated

---

## post-implementation: graduation criteria

✅ **Feature Complete**: All 5 user stories implemented and tested  
✅ **Constitution Compliant**: All 8 constitution principles maintained throughout  
✅ **Acceptance Tested**: All scenarios from spec.md validated  
✅ **Documentation Complete**: Quickstart, guides, contracts, troubleshooting all available  
✅ **Team Reproducible**: Config-based setup works for multiple developers  
✅ **No Regressions**: Existing spekificity skills work; underlying tools fully functional  
✅ **PR Approved**: Code review passed; ready to merge to main  

**Next Steps After Merge**:
1. Tag release as v1.0.0 with release notes
2. Update main README to reference `spek` platform
3. Announce platform launch to team
4. Monitor feedback and schedule Phase 2 improvements (advanced features, extended platform support, etc.)
