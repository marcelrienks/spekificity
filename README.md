# Spekificity

> **Status:** Init-first wrapper model. Spekificity is intended to be installed globally via `uv`, then initialized per-project with `spek init` which scaffolds `.spek` skills/functions and configures dependent tools.
>
> **Documentation Structure:** `/wiki/` contains philosophy, architecture, and workflow guidance. `/specs/` contains detailed specifications and implementation contracts.

## What is Spekificity?

Spekificity is a **specification-driven framework for rapid AI agent development**. It solves four critical problems:

| Problem | Solution |
|---------|----------|
| **Token bloat** | Indexed code analysis (lat.md) + scoped context loading |
| **Shallow planning** | Spec-first workflow with enriched validation layers |
| **Context loss** | Persistent knowledge vault (Git-backed Obsidian vault/) |
| **Low autonomy** | Reusable agent skills with deterministic sequencing |

**Value Proposition:** Build features **faster** with deterministic specs, persistent memory, and zero context loss between sessions.

---

## Quick Start


### Prerequisites

- Python 3.11+
- `uv` package manager ([install](https://docs.astral.sh/uv/))
-- **Obsidian CLI** (required) — primary integration for vault automation: syncs, exports, and scripted operations that enable context loading, graph generation, and lesson extraction.
+    - Why: Spekificity performs scripted vault operations (pull/push, heading/frontmatter export, and JSON/graph exports). Having the `obsidian` CLI in PATH simplifies reliable automation in developer workflows and CI.
+    - Install / enable CLI: Register the `obsidian` command in your PATH. The CLI is typically provided by the Obsidian desktop app, but the CLI is the primary required integration point — the desktop app is optional (used for visualization and interactive workflows). See https://obsidian.md/help/cli and https://obsidian.md/help/headless for platform-specific guidance.

### Installation & Setup (Recommended)

```bash
# 1. Install Spekificity as a tool (installs all dependencies)
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# 2. Initialize your project (sets up infrastructure and runs specify init)
spek init

# 3. Verify installation
spek --help
spek --version
spek tools --list
```


Planned automatic steps:
- Install Spekificity CLI and configured dependencies (SpecKit, lat.md, etc.)
- Create project directories (`.spek/`, `vault/`, `wiki/`)
- Initialize lat.md index and invoke SpecKit initialization
- Verify `obsidian` CLI availability (the automation described here requires the `obsidian` CLI to be installed and registered in PATH)

### Alternative: Manual Installation

```bash
# Clone repository
git clone <repo-url>
cd spekificity

# Install in development mode
pip install -e .

# Initialize project
spek init
```

**Full guide:** See [wiki/install.md](wiki/install.md) for detailed setup options.

**Testing local branch code before merge:** See [wiki/local.md](wiki/local.md) for a local-only pre-merge workflow using editable installs.

---

## Key Features

✅ **Spec-Driven Workflow** — All work starts with a structured specification  
✅ **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault  
✅ **Token Efficiency** — Pre-indexed indexing (lat.md) + Caveman compression  
✅ **Deterministic Sequencing** — 4-stage workflow (Prepare → Specify & Plan → Implement → Close)  
✅ **Composable Skills** — `/spek.*` commands can be chained or run independently  

---

## Platform Model

Spekificity is built around four pillars:

| Pillar | Goal | Mechanism |
|---|---|---|
| **Token efficiency** | Spend tokens on reasoning, not file rediscovery | indexed graph queries, scoped context loading, Caveman compression |
| **Determinism** | Keep feature work on a repeatable track | SpecKit workflow: specify → plan → tasks → implement |
| **Persistence** | Preserve architectural context across sessions | knowledge vault (markdown store for decisions, patterns, lessons) |
| **Autonomy** | Reduce developer hand-holding | reusable project memory + graph-grounded context injection |

---


## Target Tool Stack

- **SpecKit / Specify** — Spec-driven workflow engine
- **lat.md** — Indexing and doc-code linkage (preferred)
- **Obsidian Vault (with Obsidian CLI)** — Required knowledge store and runtime interface for specs, decisions, patterns, and lessons. The automation described in these documents depends on the `obsidian` CLI being available and registered in PATH.
- **Obsidian Vault (with Obsidian CLI)** — Required knowledge store and runtime interface for specs, decisions, patterns, and lessons. The automation described here depends on the `obsidian` CLI being available and registered in PATH. The Obsidian CLI is the required integration; the desktop app is optional and used primarily for visualization and interactive workflows.
- **Caveman Mode** — Response compression for token control

Spekificity defines how these tools work together—it doesn't replace them. **The toolset described (SpecKit, lat.md, Obsidian + Obsidian CLI, Caveman) is required for the intended automation and behavior described in this documentation.**

---

## Core Workflow

```
GLOBAL INSTALL
    ↓
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
    ↓
PROJECT INIT
    ↓
spek init [target-dir]
    ↓
INIT ACTIONS
    ├─ scaffold .spek skills/functions/prompts
    ├─ install/verify dependencies (specify, obsidian CLI, lat.md, caveman)
    ├─ run specify init under the covers
    └─ link workflow between all tools
    ↓
AGENT EXECUTION
    ↓
Use generated /spek.* skills from .spek (or direct underlying tools when needed)
```

---

## Documentation Roadmap

### **For First-Time Users**

Start with this reading order—each doc builds on the previous:

1. **[wiki/intention.md](wiki/intention.md)** — Why Spekificity exists and core philosophy (vision, principles, tenets)
2. **[wiki/architecture.md](wiki/architecture.md)** — How components fit together (technical architecture and data flow)
3. **[wiki/quickstart.md](wiki/quickstart.md)** — Hands-on walkthrough of your first feature

### **For Daily Work (Reference)**

| Document | Purpose |
|----------|---------|
| [wiki/workflow.md](wiki/workflow.md) | staged workflow details (reference during development) |
| [wiki/conventions.md](wiki/conventions.md) | Command naming and skill invocation |
| [.spek/skill-index.md](.spek/skill-index.md) | Complete `/spek.*` command reference |


### **Documentation Structure**

- **`/wiki/`** — Conceptual guidance (vision, philosophy, architecture, workflow, naming)
- **`/specs/`** — Detailed specifications and implementation contracts
- **`/vault/`** — Project memory (decisions, patterns, lessons captured during development)

### **Wiki File Scope Guide**

| File | Scope | When to Read |
|------|-------|--------------|
| **vision.md** | Vision statement, problem/solution, four pillars, design principles | Understand *why* Spekificity exists |
| **intention.md** | Philosophy, core principles, project tenets, constraints, target users | Understand Spekificity *philosophy* and design intent |
| **architecture.md** | Technical components, data flow, responsibilities (Vault, lat.md, SpecKit, Skills), integration | Understand *how* components fit together technically |
| **workflow.md** | 5-phase feature development workflow with entry/exit criteria, artifacts, detailed steps | Reference during *active development* |
| **quickstart.md** | Hands-on walkthrough for first feature | *Get started* with your first feature |
| **conventions.md** | `/spek.*` and `/speckit.*` command naming patterns and invocation | Know *which command to use* |



### **Terminology Guide**

| Term | Canonical Usage | Aliases | Definition |
|------|-----------------|---------|-----------|
| **Stage** | "Prepare", "Specify & Plan", etc. | "phase", "step" | One of the deterministic workflow stages in feature development |
| **Closeout** | "Post-Feature Closeout" | "Close", "post-processing", "archive phase" | Final phase where artifacts are archived and lessons extracted |
| **Lessons Learned** | "lessons learned", "lessons" (in context of `/spek.conclude` output) | "reflection", "retrospective", "what we learned" | Structured insights captured at feature end (what worked, what didn't, patterns) |
| **lat.md** | "lat.md" (indexer for docs and source) | "indexing tool", "doc-code linkage" | Markdown-native index + source metadata; primary source for context injection |
| **Enrichment Layer** | "enrichment layers" (plural when multiple) | "context layers", "structured context" | Context-specific information added to specs/plans (Success Criteria, Assumptions, Risk Assessment, etc.) |
| **SpecKit** | "SpecKit" or "/speckit.*" commands | "spec framework", "specification tool" | Underlying spec-driven workflow engine (upstream tool, not Spekificity-specific) |

---

## Next Steps

**New to Spekificity?** Start here:

1. Read [wiki/quickstart.md](wiki/quickstart.md)
2. Install globally via `uv tool install ... --from git+...`
3. Run `spek init` in your project directory to scaffold `.spek`
4. Run generated skills through your agent workflow

**Questions?** See [wiki/faq.md](wiki/faq.md).

---

## Contributing

Contributions welcome! Please:

1. Create a feature branch from `main`
2. Submit specs and documentation following [wiki/conventions.md](wiki/conventions.md)
3. Include test cases and lessons learned

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Marcel Rienks**

---

## Platform Model (Detailed)

The intended Spekificity workflow is:

1. Install Spekificity globally via `uv tool install ... --from git+...`.
2. Run `spek init` in a target directory.
3. Let `spek init` scaffold `.spek` skills/functions and initialize SpecKit (`specify init`) under the covers.
4. Execute the generated `/spek.*` skills from your agent (or call underlying tools directly when needed).
5. Capture lessons and refresh durable project memory through the generated workflow.

Canonical user-facing command surface is:

- `spek init` — per-project bootstrap command (primary runtime CLI command)
- `spek doctor` / `spek tools` (optional helpers) — dependency checks/status
- Generated `/spek.*` skills in `.spek/` — primary execution interface for agents

Primary workflow is skill-first (agent execution), not direct CLI-phase execution.

Vanilla SpecKit commands remain part of the underlying model:

- `/speckit.specify`
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.analyze`
- `/speckit.tasks`
- `/speckit.implement`

Use the generated `/spek.*` skills when following the Spekificity workflow. **Enrichment** means context injection and tool coordination: skills load decisions/patterns from Obsidian + lat.md and then call `/speckit.*` phases with project-specific constraints already in scope.

Note on notation: `/spek.*` denotes generated agent skills placed in `.spek/` by `spek init`. The user-facing setup CLI is `spek` (primarily `spek init`).

Vanilla SpecKit commands remain the execution layer; Spekificity adds context loading, orchestration, and post-processing around them.

## Current Repository State

This repository is ahead on architectural definition and behind on implementation.

Current state, based on the docs in `wiki/`:

- architecture and workflow intent are documented
- naming conventions for the new command surface are defined
- memory, graph, orchestration, and post-processing behavior are specified in atomic docs
- implementation of agent skills, CLI orchestration, and end-to-end validation is the next major phase

If you are evaluating the project today, treat this repository as the source for design contracts and planned behavior, not as a finished installable product.

## Start Here

Use these documents first:

- [wiki/vision.md](wiki/vision.md) — project vision, philosophy, architecture, and lifecycle framing
- [wiki/conventions.md](wiki/conventions.md) — current command names and directory conventions
- [wiki/workflow.md](wiki/workflow.md) — canonical workflow and Spekificity integration points

## Documentation Map

### Core docs

- [wiki/vision.md](wiki/vision.md)
- [wiki/intention.md](wiki/intention.md)
- [wiki/architecture.md](wiki/architecture.md)
- [wiki/workflow.md](wiki/workflow.md)
- [wiki/llm-wiki.md](wiki/llm-wiki.md)
- [wiki/conventions.md](wiki/conventions.md)

### Setup notes

- [wiki/setup.md](wiki/setup.md)

### Key specifications

- [wiki/specs/context-load-lifecycle.md](wiki/specs/context-load-lifecycle.md)
- [wiki/specs/session-memory.md](wiki/specs/session-memory.md)
- [wiki/specs/persistent-memories-and-lessons.md](wiki/specs/persistent-memories-and-lessons.md)
- [wiki/specs/decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md)
- [wiki/specs/cli-orchestration.md](wiki/specs/cli-orchestration.md)
- [wiki/specs/100-prepare-command.md](wiki/specs/100-prepare-command.md)
- [wiki/specs/102-conclude-command.md](wiki/specs/102-conclude-command.md)
- [wiki/specs/specify-enrichment.md](wiki/specs/specify-enrichment.md)
- [wiki/specs/plan-enrichment.md](wiki/specs/plan-enrichment.md)
- [wiki/specs/implement-enrichment.md](wiki/specs/implement-enrichment.md)
- [wiki/specs/050-latmd-setup-and-integration.md](wiki/specs/050-latmd-setup-and-integration.md)
- [wiki/specs/integration-validation-and-testing.md](wiki/specs/integration-validation-and-testing.md)

## Repository Layout

Current top-level layout:

```text
spekificity/
├── README.md
├── LICENSE
├── wiki/
│   ├── architecture.md
│   ├── conventions.md
│   ├── goal.md
│   ├── intention.md
│   ├── llm-wiki.md
│   ├── quickstart.md
│   ├── setup.md
│   ├── skill-index.md
│   ├── speckit.md
│   ├── vision.md
│   ├── workflow.md
│   ├── specs/
│   └── raw/
├── .git/
└── .gitignore
```

Practical reading order:

1. README
2. `wiki/intention.md`
3. `wiki/architecture.md`
4. `wiki/quickstart.md`
5. `wiki/conventions.md`
6. relevant files in `wiki/specs/`


## Working Assumptions

The docs in this repository consistently assume:

- the enriched command surface uses `spek.*`
- Spekificity wraps SpecKit rather than forking it
- durable knowledge lives in markdown, not opaque runtime state
- **Obsidian CLI is required:** The `obsidian` command must be available in PATH and enabled in Obsidian Settings → General → Command line interface. The Obsidian CLI is the primary integration point for core automation (vault syncs, metadata exports, lesson extraction, and graph exports); the desktop app is optional. Fallback alternatives are not supported.
- code intelligence should come from indexed graph tooling rather than repeated file scans
- post-feature lessons are part of the system, not optional afterthoughts

## Constitution

Project principles are governed by [.specify/memory/constitution.md](.specify/memory/constitution.md).
