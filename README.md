# Spekificity

> **Status:** Active development. Full documentation and specifications in `/wiki` and `/specs`.
>
> **Documentation Structure:** `/wiki/` contains philosophy, architecture, and workflow guidance. `/specs/` contains detailed specifications and implementation contracts.

## What is Spekificity?

Spekificity is a **specification-driven framework for rapid AI agent development**. It solves four critical problems:

| Problem | Solution |
|---------|----------|
| **Token bloat** | Indexed code analysis (CodeGraph) + scoped context loading |
| **Shallow planning** | Spec-first workflow with enriched validation layers |
| **Context loss** | Persistent knowledge vault (Git-backed Obsidian vault/) |
| **Low autonomy** | Reusable agent skills with deterministic sequencing |

**Value Proposition:** Build features **faster** with deterministic specs, persistent memory, and zero context loss between sessions.

---

## Quick Start


### Prerequisites

- Python 3.11+
- `uv` package manager ([install](https://docs.astral.sh/uv/))
- **Obsidian** (required) — for persistent memory management and vault operations
    - [Download Obsidian](https://obsidian.md/download)
    - macOS: `brew install obsidian`
    - Windows: `choco install obsidian`
- **Obsidian CLI** (required) — all vault operations and persistent memory management are performed via the Obsidian CLI
    - Install: `npm install -g @obsidianmd/obsidian-cli`
    - See [Obsidian CLI documentation](https://github.com/obsidianmd/obsidian-cli) for usage

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


This automatically:
- ✅ Installs Spekificity CLI
- ✅ Installs all dependencies (SpecKit, CodeGraph, etc.)
- ✅ Creates project directories (`.spek/`, `vault/`, `wiki/`)
- ✅ Initializes CodeGraph database
- ✅ Runs `specify init .` to initialize SpecKit
- ✅ **Requires Obsidian CLI for all persistent memory and vault operations**

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

---

## Key Features

✅ **Spec-Driven Workflow** — All work starts with a structured specification  
✅ **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault  
✅ **Token Efficiency** — Pre-indexed code analysis (CodeGraph) + Caveman compression  
✅ **Deterministic Sequencing** — 5-phase workflow (Prepare → Specify → Plan → Implement → Close)  
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
- **CodeGraph** — Code intelligence & impact analysis
- **Obsidian Vault (with Obsidian CLI)** — Mandatory knowledge store and runtime interface for specs, decisions, patterns, lessons. **All persistent memory operations require Obsidian CLI.**
- **Caveman Mode** — Response compression for token control

Spekificity defines how these tools work together—it doesn't replace them. **Obsidian CLI is a required runtime dependency for all vault and persistent memory management.**

---

## Core Workflow

```
FEATURE START
    ↓
/spek.prepare (workspace ready)
    ↓
/spek.plan --phase=specify (spec generation)
    ↓
/spek.plan --phase=plan (planning + task breakdown)
    ↓
/spek.implement (execute)
    ↓
/spek.conclude (archive lessons, refresh state)
    ↓
FEATURE COMPLETE
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
| [wiki/workflow.md](wiki/workflow.md) | 5-phase workflow details (reference during development) |
| [wiki/naming-conventions.md](wiki/naming-conventions.md) | Command naming and skill invocation |
| [.spekificity/skill-index.md](.spekificity/skill-index.md) | Complete `/spek.*` command reference |


### **Documentation Structure**

- **`/wiki/`** — Conceptual guidance (vision, philosophy, architecture, workflow, naming)
- **`/specs/`** — Detailed specifications and implementation contracts
- **`/vault/`** — Project memory (decisions, patterns, lessons captured during development)

### **Wiki File Scope Guide**

| File | Scope | When to Read |
|------|-------|--------------|
| **vision.md** | Vision statement, problem/solution, four pillars, design principles | Understand *why* Spekificity exists |
| **intention.md** | Philosophy, core principles, project tenets, constraints, target users | Understand Spekificity *philosophy* and design intent |
| **architecture.md** | Technical components, data flow, responsibilities (Vault, CodeGraph, SpecKit, Skills), integration | Understand *how* components fit together technically |
| **workflow.md** | 5-phase feature development workflow with entry/exit criteria, artifacts, detailed steps | Reference during *active development* |
| **quickstart.md** | Hands-on walkthrough for first feature | *Get started* with your first feature |
| **naming-conventions.md** | `/spek.*` and `/speckit.*` command naming patterns and invocation | Know *which command to use* |



### **Terminology Guide**

| Term | Canonical Usage | Aliases | Definition |
|------|-----------------|---------|-----------|
| **Phase** | "Phase 1: Prepare", "Phase 2: Specify", etc. (5 total) | "stage", "step" | One of five deterministic workflow stages in feature development |
| **Closeout** | "Phase 5: Post-Feature Closeout" | "Close", "post-processing", "archive phase" | Final phase where artifacts are archived and lessons extracted |
| **Lessons Learned** | "lessons learned", "lessons" (in context of `/spek.conclude` output) | "reflection", "retrospective", "what we learned" | Structured insights captured at feature end (what worked, what didn't, patterns) |
| **CodeGraph** | "CodeGraph" (always capitalized, never "code graph") | "code intelligence tool", "code analysis" | Pre-indexed SQLite code analysis tool; primary source of code intelligence |
| **Enrichment Layer** | "enrichment layers" (plural when multiple) | "context layers", "structured context" | Context-specific information added to specs/plans (Success Criteria, Assumptions, Risk Assessment, etc.) |
| **SpecKit** | "SpecKit" or "/speckit.*" commands | "spec framework", "specification tool" | Underlying spec-driven workflow engine (upstream tool, not Spekificity-specific) |

---

## Next Steps

**New to Spekificity?** Start here:

1. Read [wiki/quickstart.md](wiki/quickstart.md) (30 min)
2. Run `/spek.prepare` to initialize your workspace
3. Create your first feature spec with `/spek.plan --phase=specify`

**Questions?** See [wiki/faq.md](wiki/faq.md).

---

## Contributing

Contributions welcome! Please:

1. Create a feature branch from `main`
2. Submit specs and documentation following [wiki/naming-conventions.md](wiki/naming-conventions.md)
3. Include test cases and lessons learned

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Marcel Rienks**

---

## Platform Model (Detailed)

The intended Spekificity workflow is:

1. Run `/spek.plan` to load project context and orchestrate spec generation.
2. Let `/spek.plan` drive the upstream SpecKit flow through specify, clarify (if needed), plan, tasks, analyze, and remediation.
3. Review resulting artifacts.
4. Run `/spek.implement` to execute against approved spec, plan, tasks, and code context.
5. Capture lessons and refresh durable project memory.

Canonical user-facing command surface is:

- `/spek.prepare` — initialize workspace, git state, graph freshness, and feature state
- `/spek.context` — load or reload project context into session
- `/spek.map` — build or refresh code/document graph
- `/spek.plan` — orchestrate spec-first flow through task generation
- `/spek.implement` — execute implementation after automation has prepared artifacts
- `/spek.conclude` — archive feature outcomes, lessons, vault updates, and graph refresh
- `/spek.lessons` — extract structured lessons explicitly when needed

Primary workflow commands are `/spek.plan` and `/spek.implement`. Support commands remain user-facing and may also be called internally when orchestration needs them.

Vanilla SpecKit commands remain part of the underlying model:

- `/speckit.specify`
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.analyze`
- `/speckit.tasks`
- `/speckit.implement`

Use the `/spek.*` surface when following the Spekificity workflow. **Enrichment** means context injection: `/spek.plan` loads decisions and patterns from the knowledge vault before calling `/speckit.specify`, `/speckit.plan`, etc., so those commands operate with project-specific constraints already in scope. This guides spec and plan generation toward existing patterns without requiring manual context setup.

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
- [wiki/naming-conventions.md](wiki/naming-conventions.md) — current command names and directory conventions
- [wiki/workflow.md](wiki/workflow.md) — canonical workflow and Spekificity integration points

## Documentation Map

### Core docs

- [wiki/vision.md](wiki/vision.md)
- [wiki/intention.md](wiki/intention.md)
- [wiki/architecture.md](wiki/architecture.md)
- [wiki/workflow.md](wiki/workflow.md)
- [wiki/llm-wiki.md](wiki/llm-wiki.md)
- [wiki/naming-conventions.md](wiki/naming-conventions.md)

### Setup notes

- [wiki/setup.md](wiki/setup.md)

### Key specifications

- [wiki/specs/context-load-lifecycle.md](wiki/specs/context-load-lifecycle.md)
- [wiki/specs/session-memory.md](wiki/specs/session-memory.md)
- [wiki/specs/persistent-memories-and-lessons.md](wiki/specs/persistent-memories-and-lessons.md)
- [wiki/specs/decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md)
- [wiki/specs/cli-orchestration.md](wiki/specs/cli-orchestration.md)
- [wiki/specs/prepare-command.md](wiki/specs/prepare-command.md)
- [wiki/specs/post-command.md](wiki/specs/post-command.md)
- [wiki/specs/specify-enrichment.md](wiki/specs/specify-enrichment.md)
- [wiki/specs/plan-enrichment.md](wiki/specs/plan-enrichment.md)
- [wiki/specs/implement-enrichment.md](wiki/specs/implement-enrichment.md)
- [wiki/specs/codegraph-setup-and-integration.md](wiki/specs/codegraph-setup-and-integration.md)
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
5. `wiki/naming-conventions.md`
6. relevant files in `wiki/specs/`


## Working Assumptions

The docs in this repository consistently assume:

- the enriched command surface uses `spek.*`
- Spekificity wraps SpecKit rather than forking it
- durable knowledge lives in markdown, not opaque runtime state
- **all persistent memory and vault operations are performed via Obsidian CLI (required, not optional)**
- code intelligence should come from indexed graph tooling rather than repeated file scans
- post-feature lessons are part of the system, not optional afterthoughts

## Constitution

Project principles are governed by [.specify/memory/constitution.md](.specify/memory/constitution.md).
