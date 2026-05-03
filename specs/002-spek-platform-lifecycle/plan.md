# implementation plan: spekificity platform lifecycle — setup, init, and update

**branch**: `002-spek-platform-lifecycle` | **date**: 2026-05-03 | **spec**: [spec.md](spec.md)

**note**: This plan transforms spekificity into a primary orchestration platform with unified entry points that consolidate multi-tool initialization and maintenance.

---

## summary

**Primary Requirement**: Transform spekificity into a primary orchestration platform that provides a unified entry point (`spek`) analogous to `specify` for speckit. Users run `spek setup` then `spek init` to automatically install all prerequisites, orchestrate initialization of all consolidated tools (speckit, graphify, obsidian, caveman), and install all skills (spekificity custom, speckit, caveman) to their default project locations in a single operation.

**Technical Approach**: 
1. Create shell scripts for `spek setup` and `spek init` commands that orchestrate prerequisite detection/installation and call underlying tool initialization functions in sequence
2. Design project structure (`.spekificity/` directory tree) with unified skill installation layer
3. Build configuration system (`.spekificity/config.json`) to track orchestration state and enable idempotent re-runs
4. Establish integration documentation defining how spekificity skills invoke underlying tools
5. Create setup guides for users and developers on the orchestration model and skill development patterns
6. Implement `spek update` capability for independent spekificity custom layer updates

---

## technical context

**Language/Version**: Bash/Zsh shell scripting (cross-platform with fallback for Windows batch); YAML for orchestration config; Markdown for skills and workflows  
**Primary Dependencies**: speckit/specify (global), graphify (global), obsidian (optional), caveman skill (optional)  
**Storage**: Project-local configuration files (`.spekificity/config.json`), project structure metadata (`.spekificity/version.txt`)  
**Testing**: Acceptance scenario validation on clean machines; AI agent skill discovery verification; idempotency testing (re-running setup/init)  
**Target Platform**: macOS, Linux (primary); Windows batch script equivalent (optional for MVP)  
**Project Type**: Platform/tools orchestration (shell scripts, markdown skills, configuration system)  
**Performance Goals**: `spek setup` <20 min (including long tool installs), `spek init` <2 min (with prerequisites installed), idempotent re-runs complete in <30 sec  
**Constraints**: Zero manual file copying by users; all skills installed to default locations automatically; setup/init must provide clear status output; no GUI required  
**Scale/Scope**: Orchestrates 4 main tools (speckit, graphify, obsidian, caveman); installs 3 layers of skills (spekificity, speckit, caveman); manages multi-developer team setup reproducibility

---

## constitution check

*Gate: Must pass before phase 0 research. Re-check after phase 1 design.*

| Principle | Status | Rationale |
|-----------|--------|-----------|
| **I. Skills and workflows — not application code** | ✅ PASS | Feature delivers shell setup scripts (CLI tools), markdown skill files, YAML configuration, setup guides. No application code; all execution is via CLI commands and skill definitions. |
| **II. Decorator pattern — never replace, always extend** | ✅ PASS | Spekificity orchestrates existing tools (`spek init` calls `specify init`, graphify setup, etc.) without modifying or forking them. `spek` decorates and extends speckit's workflow without replacing it. |
| **III. Modular independence** | ✅ PASS | Each tool (speckit, graphify, obsidian, caveman) is independently updatable. Spekificity orchestration calls their public initialization interfaces, adapting only to those interfaces, not internal structure. |
| **IV. Global speckit, local customization** | ✅ PASS | Speckit/specify remains globally installed and independently updatable. Spekificity's custom skills/config live locally in `.spekificity/` per-project. Separation is clean. |
| **V. Graph-first context loading** | ✅ PASS | Spekificity integrates graphify → obsidian workflow via `/spek.map-codebase` skill and graph-first context loading in other skills. Supports constitution principle. |
| **VI. Token efficiency by design** | ✅ PASS | Spekificity orchestrates caveman skill integration; custom skills document token-efficient practices; setup guides minimize verbose context. Caveman mode available throughout. |
| **VII. AI-executable setup** | ✅ PASS | All setup steps (prerequisite detection, tool installation, skill setup) are documented as bash commands or step-by-step guides that AI agents can execute without ambiguity. No hand-wavy instructions. |
| **VIII. Idempotent initialization** | ✅ PASS | Feature spec (fr-005) requires idempotent `spek init` — running multiple times updates state without destroying config or custom modifications. Configuration tracking enables recovery from partial failures. |

**Gate Result**: ✅ **PASS** — Feature aligns with all 8 constitution principles. Proceed to phase 0 research.

## project structure

### documentation (this feature)

```text
specs/002-spek-platform-lifecycle/
├── plan.md              # this file — implementation plan
├── research.md          # phase 0 research deliverable (6 research tasks)
├── data-model.md        # phase 1 design: entity definitions
├── quickstart.md        # phase 1 design: user onboarding guide
├── contracts/
│   ├── orchestration-contract.md    # how spek init orchestrates tools
│   ├── skill-installation-contract.md    # skill installation and discovery
│   └── idempotency-contract.md      # idempotent re-run guarantees
└── tasks.md             # phase 2 — implementation task breakdown (/speckit.tasks)
```

### runtime structure (repository root)

```text
.spekificity/                    # Primary spekificity platform directory (local per-project)
├── config.json                  # Orchestration state and config (schema v1.0)
├── version.txt                  # Spekificity platform version
├── skill-index.md               # Unified skill discovery index for all layers
├── setup-scripts/
│   ├── setup.sh                 # spek setup command (prerequisite detection/installation)
│   ├── init.sh                  # spek init command (orchestration)
│   └── update.sh                # spek update command (custom layer updates)
├── skills/
│   ├── spek.context-load.md
│   ├── spek.map-codebase.md
│   ├── spek.lessons-learnt.md
│   └── [other spek.* custom skills]
├── workflows/
│   ├── setup-workflow.md
│   ├── init-workflow.md
│   ├── update-workflow.md
│   └── integration-guide.md
└── guides/
    ├── architecture.md
    ├── orchestration-model.md
    ├── skill-development.md
    └── troubleshooting.md

.github/
├── agents/                       # Speckit skills (installed via specify init)
│   └── [speckit.* skill files]

[project-root]/
├── [source code and other project files unchanged]
```

**Structure Decision**: The spekificity platform uses a three-layered skill model:
1. **Spekificity custom skills** — stored in `.spekificity/skills/spek.*` (local)
2. **Speckit skills** — stored in `.github/agents/speckit.*` (installed by `specify init` called from `spek init`)
3. **Caveman skills** — available globally or per-project (integrated by `spek init`)

All skills are registered in `.spekificity/skill-index.md` for unified discovery by AI agents.

---

## phase 0: research — resolve technical unknowns

**Objective**: Identify and document technical decisions needed before detailed design can proceed.

### research task 1: shell script orchestration patterns

**Unknown**: How should `spek setup` and `spek init` orchestrate multiple tools with different initialization interfaces and error conditions?

**Investigation**:
- Study how `specify` implements its init workflow and prerequisite checking
- Analyze graphify installation and setup requirements
- Document obsidian configuration approach (desktop app vs. CLI)
- Determine caveman skill integration point in orchestration
- Research error handling and recovery patterns for multi-step orchestration

**Research Deliverable**: Document in `research.md`:
- Orchestration flow diagram: prerequisites → `spek setup` → error handling → `spek init` → tool initialization sequence
- Conditional initialization paths (e.g., obsidian optional, fallback storage)
- Rollback and recovery strategy for interrupted setup
- Idempotency implementation (state tracking via config file)

---

### research task 2: skill installation and discovery strategy

**Unknown**: How should skills from all layers (spekificity, speckit, caveman) be discovered and made available to AI agents in a unified namespace?

**Investigation**:
- Determine how `.github/agents/` (speckit skills) and `.spekificity/skills/spek.*` (spekificity) should be organized
- Research AI agent skill discovery mechanisms (Copilot `.instructions.md`, Claude Code skill auto-discovery)
- Define strategy for caveman skill availability (included in spekificity or separate?)
- Determine `.spekificity/skill-index.md` or equivalent discovery manifest format
- Analyze how to make skills discoverable WITHOUT modifying third-party tool configurations

**Research Deliverable**: Document in `research.md`:
- Unified skill discovery architecture (how spekificity aggregates and surfaces all skills)
- Configuration format for skill registration (manifest file format)
- AI agent integration points (copilot-instructions.md vs. SKILL.md vs. .instructions.md)
- Namespace clarity (how users distinguish `/spek.*` from `/speckit.*` from caveman)

---

### research task 3: configuration schema and state tracking

**Unknown**: How should `.spekificity/config.json` track orchestration state, tool versions, and enable idempotent re-runs?

**Investigation**:
- Design config schema: version tracking, initialization status, installed tools/skills, orchestration history
- Determine config versioning strategy for forward/backward compatibility
- Research migration path for schema changes (e.g., new fields added in future versions)
- Analyze how config enables idempotent re-runs: detecting already-initialized state, skipping certain steps, updating others
- Define config semantics: when does `spek init` re-run `specify init` vs. skipping it?

**Research Deliverable**: Document in `research.md`:
- Config schema version 1.0 (JSON structure with all tracked fields)
- Idempotency rules: which orchestration steps are re-run, which are skipped/updated, which are flagged for review
- Config versioning and migration strategy
- Troubleshooting guide: how to recover from partial failures using config state

---

### research task 4: update strategy for spekificity custom layer

**Unknown**: How should `spek update` independently update spekificity custom skills without affecting third-party tools or breaking user modifications?

**Investigation**:
- Research diff-merge strategy for updating skill files while preserving user customizations
- Determine rollback mechanism (save previous skill versions? git history?)
- Analyze conflict detection and resolution for updated skills
- Evaluate whether update should be triggered automatically or manually
- Research changelog generation and display strategy

**Research Deliverable**: Document in `research.md`:
- Update architecture: how spekificity tracks versions, downloads updates, applies changes
- Conflict detection and user notification strategy
- Rollback procedure if update introduces breaking changes
- Changelog format and user communication approach

---

### research task 5: multi-platform support (macOS/Linux/Windows)

**Unknown**: How should setup scripts be portable across macOS, Linux, and Windows while maintaining consistent behavior?

**Investigation**:
- Analyze bash vs. zsh differences on macOS and Linux
- Determine Windows support approach (batch script, WSL, PowerShell, or out-of-scope?)
- Research prerequisite detection on each platform (e.g., which package manager? brew on macOS, apt on Ubuntu)
- Analyze installer tool availability (`uv`, `pip`, Homebrew, apt, etc.)

**Research Deliverable**: Document in `research.md`:
- Platform detection strategy (OS type, shell, available tools)
- Prerequisite installation paths by platform
- Testing plan: validation on clean macOS, Ubuntu, (Windows optional)
- Documentation of platform-specific behavior differences

---

### research task 6: prerequisite availability and fallback behavior

**Unknown**: What should happen when prerequisites cannot be installed (offline environment, restricted network, permission issues)?

**Investigation**:
- Define which prerequisites are hard-required vs. optional (e.g., obsidian optional, graphify required)
- Determine error messaging: clear explanation of missing tools + manual installation instructions
- Analyze graceful degradation: if tool cannot be installed, how should spekificity adapt?
- Research fallback storage formats if obsidian is unavailable (JSON files? plain markdown?)

**Research Deliverable**: Document in `research.md`:
- Prerequisite tiers: hard-required, optional, soft-required (warn but proceed)
- Fallback behavior for each optional component
- Error messaging and recovery instructions for users
- Testing strategy for offline/restricted network scenarios

---

## phase 1: design — architecture and integration

### design task 1: project structure and configuration schema

**Deliverable**: Define in `data-model.md`:

#### Configuration schema (`.spekificity/config.json`):

```json
{
  "spek_version": "1.0.0",
  "project_initialized": true,
  "initialized_timestamp": "2026-05-03T12:00:00Z",
  "prerequisites": {
    "python": "3.11.2",
    "uv": "0.1.42",
    "git": "2.43.0",
    "speckit": "1.0.0",
    "graphify": "0.5.0",
    "obsidian": "installed"
  },
  "tools_initialized": {
    "speckit": true,
    "graphify": true,
    "obsidian": true,
    "caveman": true
  },
  "installed_skills": {
    "spekificity": ["spek.context-load", "spek.map-codebase", "spek.lessons-learnt"],
    "speckit": ["speckit.specify", "speckit.plan", "speckit.implement"],
    "caveman": "available"
  },
  "orchestration_history": [
    {"step": "verify_prerequisites", "status": "success", "timestamp": "2026-05-03T12:00:01Z"},
    {"step": "specify_init", "status": "success", "timestamp": "2026-05-03T12:00:05Z"}
  ],
  "config_schema_version": "1.0"
}
```

---

### design task 2: core data entities

**Deliverable**: In `data-model.md`, define key entities:

- **Orchestration State**: Tracks initialization status, prerequisites, tools, skills, history
- **Setup Prerequisite**: Tool metadata (name, version, installer command, priority, fallback)
- **Skill Layer**: Layer metadata (name, namespace, directory, skills, installed status)
- **Orchestration Step**: Single action in workflow (name, status, error, timestamp, recoverable)

---

### design task 3: interface contracts

**Deliverable**: Create `contracts/` directory with three interface definitions:

1. **orchestration-contract.md**: How `spek init` calls `specify init`, graphify, obsidian, caveman
2. **skill-installation-contract.md**: Skill installation locations, discovery, namespace isolation
3. **idempotency-contract.md**: Guarantees for safe re-running `spek init`

---

### design task 4: quickstart and user guide

**Deliverable**: `quickstart.md` with:
- Five-minute overview of spekificity
- Installation: `spek setup`
- Initialization: `spek init`
- First feature development workflow
- Troubleshooting basics
- Reference to orchestration model and tool independence

---

### design task 5: update copilot-instructions.md

**Deliverable**: Update `.github/copilot-instructions.md` to:
- Clarify `spek` as primary entry point
- Document new skill index structure
- Link to orchestration documentation
- Reference skill development guide

---

## phase 1 design summary

**Architecture**: `.spekificity/` directory contains all orchestration components, configuration, and spekificity-custom skills. Shell scripts implement `spek setup`, `spek init`, `spek update`. Configuration (`.spekificity/config.json`) tracks state and enables idempotency. Unified skill index aggregates all skills (spekificity, speckit, caveman) for AI agent discovery.

**Constraints Met**: ✅ Zero manual file copying, ✅ All skills auto-installed, ✅ Clear status output, ✅ Idempotent operations, ✅ Platform-aware, ✅ Fallback behavior

---

## next phase: implementation

**Phase 2** (`/speckit.tasks` → `/speckit.implement`) will generate task breakdown covering:
1. Shell script implementation (setup.sh, init.sh, update.sh)
2. Directory structure and templates
3. Configuration schema and handling
4. All documentation (guides, workflows, skill templates)
5. Testing and validation
6. End-to-end acceptance testing
7. Migration guide for existing users

**Constitution**: ✅ Re-checked after phase 1 design. All 8 principles maintained throughout implementation plan.
