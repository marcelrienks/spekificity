# implementation plan: spek — full workflow cli

**branch**: `003-spek-full-workflow-cli` | **date**: 2026-05-03 | **spec**: [spec.md](spec.md)

---

## summary

**primary requirement**: deliver `spek` as a two-layer platform: (1) a bash cli for machine operations (`setup`, `init`, `status`, `update`) that installs prerequisites and orchestrates underlying tool initialisation, and (2) a set of ai agent skills (`/spek.prepare`, `/spek.automate`, `/spek.post`) that drive the speckit feature lifecycle with vault context integration, automated step sequencing, and interactive developer prompting — all without replacing or modifying any underlying tool.

**technical approach**:
1. `spek` bash cli entry point with sub-commands routing to dedicated shell scripts in `bin/`
2. `/spek.prepare`, `/spek.automate`, `/spek.post` as markdown ai agent skills following the established spekificity skill format
3. workflow state persistence via `.spekificity/workflow-state.json` for automate interruption recovery
4. pattern-based speckit step completion detection (output markers or file existence checks)
5. pr creation via `gh` cli with terminal fallback if `gh` unavailable
6. graph staleness detection via last-modified timestamp comparison against git HEAD

---

## technical context

**language/version**: bash (cli scripts, macos + linux); markdown (ai agent skills)
**primary dependencies**: speckit/specify (global), graphify (global), gh cli (optional, for pr creation), git (required)
**storage**: `.spekificity/config.json` (platform config), `.spekificity/workflow-state.json` (automate session state), `vault/` (obsidian vault — plain markdown)
**testing**: acceptance scenario validation on clean macos/linux; ai agent skill execution tests against both copilot and claude code; idempotency re-run tests
**target platform**: macos, linux (bash)
**project type**: platform cli + ai agent skill collection
**performance goals**: `spek setup` < 20 min (tool install time varies); `spek init` < 5 min with prerequisites; `spek prepare` < 60 sec with fresh graph; `spek status` < 5 sec
**constraints**: no compiled binaries; no gui; all operations terminal-safe; must be ai-executable as skills; no assumptions about internet availability for vault operations
**scale/scope**: 1 cli entry point; 7 sub-commands; 3 new ai skills; 3 updated existing skills; 1 config schema; 1 workflow state schema

---

## constitution check

*gate: must pass before phase 0 research. re-check after phase 1 design.*

| principle | status | rationale |
|-----------|--------|-----------|
| **i. skills and workflows — not application code** | ✅ pass | cli layer is bash orchestration scripts (explicitly permitted by constitution). ai functionality is markdown skills. no custom business logic or stateful services beyond shell scripts. |
| **ii. decorator pattern — never replace, always extend** | ✅ pass | `spek init` calls `specify init` internally; `spek automate` wraps speckit workflow steps; no speckit code is forked or modified. |
| **iii. modular independence** | ✅ pass | each tool (speckit, graphify, obsidian, caveman) is invoked by name only via cli. if a tool changes its cli interface, only the relevant adapter script changes. |
| **iv. global speckit, local customisation** | ✅ pass | speckit remains global. all spek scripts and skills are local per-project under `.spekificity/` and `bin/`. |
| **v. graph-first context loading** | ✅ pass | `spek prepare` loads vault graph before any speckit step. `/spek.automate` passes vault context to spec and plan steps. |
| **vi. token efficiency by design** | ✅ pass | skills use vault graph to avoid file scanning. caveman mode available throughout. workflow state minimises re-doing completed steps. |
| **vii. ai-executable setup** | ✅ pass | all setup steps are bash commands or explicit step-by-step guides. no ambiguous instructions. |
| **viii. idempotent initialisation** | ✅ pass | `spek init` checks existing state before each action (fr-006); `spek setup` skips already-installed tools (fr-002). workflow state file enables safe re-entry. |

**gate result**: ✅ **pass** — all 8 constitution principles satisfied. proceed to phase 0 research.

**post-design re-check**: ✅ pass — design decisions in research.md confirm no constitution violations introduced.

---

## project structure

### documentation (this feature)

```text
specs/003-spek-full-workflow-cli/
├── plan.md              ← this file
├── research.md          ← phase 0: resolved decisions and alternatives
├── data-model.md        ← phase 1: entity definitions (config, state, skill-index, etc.)
├── quickstart.md        ← phase 1: first-time setup walkthrough
├── contracts/
│   ├── cli-contract.md          ← spek cli sub-command interface contract
│   ├── automate-contract.md     ← /spek.automate skill input/output contract
│   └── vault-integration-contract.md  ← how spek reads/writes vault
└── tasks.md             ← phase 2 (/speckit.tasks — not created by this plan)
```

### runtime structure (repository root)

```text
bin/
└── spek                         ← bash cli entry point (executable)
    # routes to:
    # setup    → .spekificity/bin/setup.sh
    # init     → .spekificity/bin/init.sh
    # prepare  → .spekificity/bin/prepare.sh  (orchestrates /spek.prepare skill)
    # automate → .spekificity/bin/automate.sh (orchestrates /spek.automate skill)
    # post     → .spekificity/bin/post.sh     (orchestrates /spek.post skill)
    # status   → .spekificity/bin/status.sh
    # update   → .spekificity/bin/update.sh

.spekificity/
├── bin/                         ← internal command implementations
│   ├── setup.sh
│   ├── init.sh
│   ├── prepare.sh
│   ├── automate.sh
│   ├── post.sh
│   ├── status.sh
│   └── update.sh
├── config.json                  ← platform config (schema v1.0 — see data-model.md)
├── workflow-state.json          ← automate session state (see data-model.md)
├── skill-index.md               ← unified skill registry (/spek.* + /speckit.* + caveman)
├── version.txt                  ← installed spekificity version
└── skills/                      ← ai agent skill files
    ├── spek.prepare.md          ← NEW: preparation phase skill
    ├── spek.automate.md         ← NEW: automated speckit lifecycle skill
    ├── spek.post.md             ← NEW: post-implementation tasks skill
    ├── spek.context-load.md     ← UPDATE: existing skill, integrate with workflow state
    ├── spek.map-codebase.md     ← UPDATE: existing skill, add staleness check
    └── spek.lessons-learnt.md   ← UPDATE: existing skill, align with post workflow

vault/
├── graph/index.md               ← graphify graph (read by spek prepare, updated by spek post)
├── lessons/                     ← written by /spek.lessons-learnt (called from spek post)
└── context/                     ← decisions + patterns (read by spek automate)
```

**structure decision**: single project (bash cli + markdown skills). no sub-packages or language runtimes beyond bash. all state is json files in `.spekificity/`. ai skill files are in `.spekificity/skills/` for local per-project installation.

---

## complexity tracking

no constitution violations. no complexity justification required.

---

## phase 0: research

*see [research.md](research.md) for full findings. decisions summarised here.*

### r-001: spek cli distribution and installation
**decision**: ship `spek` as a single bash entry-point script. install via `curl | bash` installer script or manual `chmod +x && cp bin/spek /usr/local/bin/spek`. no package manager dependency.
**rationale**: zero runtime dependencies; users already have bash; consistent with constitution preference for shell scripts. avoids python/node dependency management.
**alternatives rejected**: python cli (adds runtime dependency); npm package (requires node); compiled binary (requires build step).

### r-002: speckit programmatic invocation
**decision**: speckit is driven by the ai agent reading the `/spek.automate` skill. the skill instructs the ai to invoke each speckit command in sequence. "programmatic" means the ai follows the skill step by step — not a separate process calling speckit cli.
**rationale**: speckit is an ai skill system, not a traditional cli. the ai agent is the runtime. `spek automate` triggers the ai to execute `/spek.automate` skill which drives speckit commands.
**alternatives rejected**: subprocess call to speckit cli (speckit is not designed for piped automation); parsing speckit stdout (fragile, format-dependent).

### r-003: speckit step completion detection
**decision**: completion is detected by the ai agent via two methods: (1) existence of the expected output file (e.g., `spec.md` exists in feature dir → spec step complete); (2) explicit "step complete" marker in the skill instruction that the ai checks before proceeding.
**rationale**: file-based detection is robust and ai-readable. no output parsing required.
**alternatives rejected**: exit code parsing (speckit is ai-driven, not a subprocess); speckit internal api (not available externally).

### r-004: graph staleness detection
**decision**: compare `vault/graph/index.md` last-modified timestamp against git HEAD timestamp. if graph is older than HEAD, mark stale. threshold: graph is "stale" if HEAD has commits newer than the graph timestamp.
**rationale**: git is already required; `git log -1 --format=%ct HEAD` gives epoch; `stat -f %m vault/graph/index.md` (macos) / `stat -c %Y` (linux) gives epoch. simple, no additional dependencies.
**alternatives rejected**: file count comparison (misses content changes); md5 of all source files (expensive for large codebases).

### r-005: pr creation
**decision**: use `gh pr create` if `gh` cli is installed and authenticated. fall back to printing a formatted pr description to the terminal with copy-paste instructions if `gh` is unavailable.
**rationale**: `gh` is the official github cli, widely used. terminal fallback ensures the step never blocks completion of the workflow.
**alternatives rejected**: direct github api calls (requires auth token management in shell); git push + browser (not ai-executable).

### r-006: workflow state serialization
**decision**: persist automate session state as `.spekificity/workflow-state.json`. schema: `{ feature_branch, feature_dir, current_step, completed_steps[], pending_questions[], started_at, last_updated }`. ai reads this file at resume to determine next step.
**rationale**: json is human-readable and ai-readable. file-based state survives session restarts and process interruptions. simple schema, no database required.
**alternatives rejected**: environment variables (lost on session end); separate database (overkill for a single-feature state).

---

## phase 1: design

*full artifacts in linked files. key decisions summarised here.*

### data model
see [data-model.md](data-model.md).

key entities:
- **`SpekConfig`** (`.spekificity/config.json`): platform version, init state, tool integration status, skill registry
- **`WorkflowState`** (`.spekificity/workflow-state.json`): active automate session — branch, step tracking, pending questions, resume checkpoint
- **`GraphState`**: derived state from vault/graph/index.md timestamp vs git HEAD — fresh / stale / absent
- **`SkillIndex`** (`.spekificity/skill-index.md`): registry of all `/spek.*`, `/speckit.*`, and caveman commands

### contracts
see `contracts/` directory:
- [cli-contract.md](contracts/cli-contract.md): `spek` sub-command interface — inputs, outputs, exit codes for each sub-command
- [automate-contract.md](contracts/automate-contract.md): `/spek.automate` skill — required inputs, step sequence, question interface, completion criteria
- [vault-integration-contract.md](contracts/vault-integration-contract.md): how `spek` reads from and writes to vault — file paths, formats, update conditions

### quickstart
see [quickstart.md](quickstart.md) — complete first-time setup walkthrough: install spek → setup → init → prepare → automate.

---

## implementation phases

### phase a — cli foundation (fr-001, fr-002, fr-003, fr-019, fr-020)
*prerequisite for all other phases*

deliverables:
- `bin/spek` entry point script
- `.spekificity/bin/setup.sh` — prerequisite detection and installation
- `.spekificity/bin/status.sh` — platform status report
- `.spekificity/config.json` schema + initial write on first run
- `[spek]` / `[speckit]` / `[graphify]` output prefix conventions

### phase b — init and skill installation (fr-004, fr-005, fr-006)
*requires: phase a*

deliverables:
- `.spekificity/bin/init.sh` — orchestrates `specify init`, graphify setup, obsidian vault creation, skill installation
- `.spekificity/skill-index.md` — auto-generated on init
- `.spekificity/bin/update.sh` — spekificity custom layer update

### phase c — prepare skill (fr-007, fr-008)
*requires: phase b*

deliverables:
- `.spekificity/skills/spek.prepare.md` — new skill: context load, graph staleness check, lessons surfacing
- `.spekificity/bin/prepare.sh` — triggers ai to read spek.prepare skill
- graph staleness detection logic (r-004)

### phase d — automate skill (fr-009 through fr-016)
*requires: phase c*

deliverables:
- `.spekificity/skills/spek.automate.md` — new skill: full speckit lifecycle automation, interactive qa, vault context injection
- `.spekificity/workflow-state.json` schema + read/write
- `.spekificity/bin/automate.sh` — entry point, preflight checks, feature branch creation
- resume logic (`spek automate --resume`)
- pr creation via `gh` with fallback

### phase e — post skill (fr-017, fr-018)
*requires: phase b*

deliverables:
- `.spekificity/skills/spek.post.md` — new skill: lessons learnt, incremental graph refresh
- `.spekificity/bin/post.sh` — post-implementation entry point
- update existing skills: `spek.context-load.md`, `spek.map-codebase.md`, `spek.lessons-learnt.md`

### phase f — validation
*requires: phases a–e*

deliverables:
- clean-machine acceptance test: setup → init → prepare → automate → post
- idempotency test: re-run setup and init
- vault integration test: spec and plan reference vault graph nodes
- resume test: interrupt automate, verify resume from correct step
