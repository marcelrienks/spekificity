# Spekificity

> **Status:** Active development. Full documentation and specifications in `/wiki` and `/specs`.

## What is Spekificity?

Spekificity is a **specification-driven framework for rapid AI agent development**. It solves four critical problems:

| Problem | Solution |
|---------|----------|
| **Token bloat** | Indexed code analysis (CodeGraph) + scoped context loading |
| **Shallow planning** | Spec-first workflow with enriched validation layers |
| **Context loss** | Persistent knowledge vault (Git-backed Obsidian) |
| **Low autonomy** | Reusable agent skills with deterministic sequencing |

**Value Proposition:** Build features **10x faster** with deterministic specs, persistent memory, and zero context loss between sessions.

---

## Quick Start (5 minutes)

### Prerequisites

- Python 3.11+
- Git (initialized project)
- `uv` package manager

### Installation & Setup

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd spekificity

# 2. Install SpecKit globally
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 3. Initialize Spekificity in your project
specify init .

# 4. Set up knowledge vault (Obsidian-compatible)
# → Read: wiki/quickstart.md for step-by-step guide

# 5. Start your first feature
/spek.prepare
```

**Next:** Read [wiki/quickstart.md](wiki/quickstart.md) for full walkthrough (30 min).

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
- **CodeGraph** — Code intelligence & impact analysis (replaces Graphify)
- **Obsidian Vault** — Knowledge store for specs, decisions, patterns, lessons
- **Caveman Mode** — Response compression for token control

Spekificity defines how these tools work together—it doesn't replace them.

---

## Core Workflow

```
FEATURE START
    ↓
/spek.prepare (git clean, vault fresh, CodeGraph synced)
    ↓
/spek.automate --phase=specify (enriched spec generation)
    ↓
/spek.automate --phase=plan (task breakdown with impact analysis)
    ↓
/spek.implement (execute with full context)
    ↓
/spek.post (archive lessons, refresh state)
    ↓
FEATURE COMPLETE
```

---

## Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [wiki/quickstart.md](wiki/quickstart.md) | Step-by-step guide for first feature | 30 min |
| [wiki/workflow.md](wiki/workflow.md) | Detailed 5-phase workflow | 15 min |
| [wiki/intention.md](wiki/intention.md) | Project vision & philosophy | 10 min |
| [wiki/decision.md](wiki/decision.md) | Architectural decisions (why CodeGraph, etc.) | 10 min |
| [wiki/faq.md](wiki/faq.md) | Common questions & troubleshooting | 20 min |
| [.spekificity/skill-index.md](.spekificity/skill-index.md) | Complete command reference | 15 min |

---

## Next Steps

**New to Spekificity?** Start here:

1. Read [wiki/quickstart.md](wiki/quickstart.md) (30 min)
2. Run `/spek.prepare` to initialize your workspace
3. Create your first feature spec with `/spek.automate --phase=specify`

**Questions?** See [wiki/faq.md](wiki/faq.md).

---

## Contributing

Contributions welcome! Please:

1. Create a feature branch from `main`
2. Submit specs and documentation following [wiki/naming-conventions.md](wiki/naming-conventions.md)
3. Link decisions to [wiki/decision.md](wiki/decision.md)
4. Include test cases and lessons learned

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Marcel Rienks**

---

## Platform Model (Detailed)

The intended Spekificity workflow is:

1. Run `/spek.automate` to load project context and orchestrate spec generation.
2. Let `/spek.automate` drive the upstream SpecKit flow through specify, clarify (if needed), plan, tasks, analyze, and remediation.
3. Review resulting artifacts.
4. Run `/spek.implement` to execute against approved spec, plan, tasks, and code context.
5. Capture lessons and refresh durable project memory.

Canonical user-facing command surface is:

- `/spek.prepare` — initialize workspace, git state, graph freshness, and feature state
- `/spek.context` — load or reload project context into session
- `/spek.map` — build or refresh code/document graph
- `/spek.automate` — orchestrate spec-first flow through task generation
- `/spek.implement` — execute implementation after automation has prepared artifacts
- `/spek.post` — archive feature outcomes, lessons, vault updates, and graph refresh
- `/spek.lessons` — extract structured lessons explicitly when needed

Primary workflow commands are `/spek.automate` and `/spek.implement`. Support commands remain user-facing and may also be called internally when orchestration needs them.

Vanilla SpecKit commands remain part of the underlying model:

- `/speckit.specify`
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.analyze`
- `/speckit.tasks`
- `/speckit.implement`

Use the `/spek.*` surface when following the Spekificity workflow. **Enrichment** means context injection: `/spek.automate` loads decisions and patterns from the knowledge vault before calling `/speckit.specify`, `/speckit.plan`, etc., so those commands operate with project-specific constraints already in scope. This guides spec and plan generation toward existing patterns without requiring manual context setup.

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
- [wiki/decision.md](wiki/decision.md) — major tool and architecture decisions
- [wiki/naming-conventions.md](wiki/naming-conventions.md) — current command names and directory conventions
- [wiki/speckit-workflow.md](wiki/speckit-workflow.md) — canonical SpecKit flow and Spekificity integration points
- [wiki/todo.md](wiki/todo.md) — roadmap and implementation status

## Documentation Map

### Core docs

- [wiki/vision.md](wiki/vision.md)
- [wiki/decision.md](wiki/decision.md)
- [wiki/llm-wiki.md](wiki/llm-wiki.md)
- [wiki/research.md](wiki/research.md)
- [wiki/naming-conventions.md](wiki/naming-conventions.md)
- [wiki/speckit-workflow.md](wiki/speckit-workflow.md)
- [wiki/todo.md](wiki/todo.md)

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
├── wiki/
│   ├── architecture.md
│   ├── decision.md
│   ├── intention.md
│   ├── llm-wiki.md
│   ├── naming-conventions.md
│   ├── research.md
│   ├── speckit-workflow.md
│   ├── todo.md
│   ├── setup/
│   ├── specs/
│   └── raw/
├── .github/
├── .specify/
└── .cel/
```

Practical reading order:

1. README
2. `wiki/intention.md`
3. `wiki/decision.md`
4. `wiki/naming-conventions.md`
5. `wiki/speckit-workflow.md`
6. relevant files in `wiki/specs/`

## Working Assumptions

The docs in this repository consistently assume:

- the enriched command surface uses `spek.*`
- Spekificity wraps SpecKit rather than forking it
- durable knowledge lives in markdown, not opaque runtime state
- code intelligence should come from indexed graph tooling rather than repeated file scans
- post-feature lessons are part of the system, not optional afterthoughts

## Constitution

Project principles are governed by [.specify/memory/constitution.md](.specify/memory/constitution.md).
