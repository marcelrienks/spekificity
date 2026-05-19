# Spekificity

> Status: active development. Repository currently contains documentation, architectural decisions, and implementation specs for the Spekificity platform. CLI and skill implementation are planned; this repo is not yet a packaged runtime.

Spekificity is an agentic consolidation platform aimed at four recurring LLM agent failures:

- token bloat
- shallow planning
- context loss
- low autonomy

Core idea: combine spec-driven workflow, indexed code context, persistent project memory, and aggressive output compression so an AI agent can move from feature request to implementation with less rescanning, less drift, and less manual steering.

## What This Repository Is

This repository is the design and specification surface for Spekificity.

It currently contains:

- project intention and architecture documents
- workflow definitions for enriched SpecKit usage
- atomic specifications for context loading, orchestration, memory, graph integration, and post-processing
- setup notes for supporting tools
- roadmap and design decisions

It does not currently contain a complete shipped `spek` CLI, installed skill bundle, or runnable platform distribution in this tree.

## Platform Model

Spekificity is built around four pillars:

| Pillar | Goal | Mechanism |
|---|---|---|
| Token efficiency | Spend tokens on reasoning, not file rediscovery | indexed graph queries, scoped context loading, Caveman compression |
| Determinism | Keep feature work on a repeatable track | SpecKit workflow: specify -> plan -> tasks -> implement |
| Persistence | Preserve architectural context across sessions | vault-style markdown knowledge store for decisions, patterns, lessons |
| Autonomy | Reduce developer hand-holding | reusable project memory + graph-grounded context injection |

## Target Tool Stack

Current design direction across the wiki is:

- SpecKit / Specify for spec-first workflow generation
- CodeGraph as the recommended code intelligence layer for agent workflows
- Obsidian-compatible markdown vault for durable project knowledge
- Caveman mode for response compression and token control

Spekificity does not try to replace those systems. It defines how they should work together.

## Target Workflow

The intended Spekificity workflow is:

1. Load project context.
2. Enrich specification generation with prior decisions and patterns.
3. Enrich planning with code-graph and impact context.
4. Generate ordered tasks.
5. Implement against spec, plan, and code context.
6. Capture lessons and refresh durable project memory.

Canonical command surface for that workflow is:

- `/spek.context`
- `/spek.specify`
- `/spek.plan`
- `/speckit.tasks`
- `/speckit.analyze` (optional)
- `/spek.implement`
- `/spek.lessons`
- `/spek.post`
- `/spek.map`
- `/spek.automate`

Vanilla SpecKit commands remain part of the model where appropriate:

- `/speckit.specify`
- `/speckit.plan`
- `/speckit.tasks`
- `/speckit.implement`

Use the `spek.*` surface when following the Spekificity-enriched workflow.

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

- [wiki/intention.md](wiki/intention.md) — project vision, philosophy, and lifecycle framing
- [wiki/architecture.md](wiki/architecture.md) — system structure, component boundaries, update model
- [wiki/decision.md](wiki/decision.md) — major tool and architecture decisions
- [wiki/naming-conventions.md](wiki/naming-conventions.md) — current command names and directory conventions
- [wiki/speckit-workflow.md](wiki/speckit-workflow.md) — canonical SpecKit flow and Spekificity integration points
- [wiki/todo.md](wiki/todo.md) — roadmap and implementation status

## Documentation Map

### Core docs

- [wiki/intention.md](wiki/intention.md)
- [wiki/architecture.md](wiki/architecture.md)
- [wiki/decision.md](wiki/decision.md)
- [wiki/llm-wiki.md](wiki/llm-wiki.md)
- [wiki/research.md](wiki/research.md)
- [wiki/naming-conventions.md](wiki/naming-conventions.md)
- [wiki/speckit-workflow.md](wiki/speckit-workflow.md)
- [wiki/todo.md](wiki/todo.md)

### Setup notes

- [wiki/setup/speckit-setup.md](wiki/setup/speckit-setup.md)
- [wiki/setup/obsidian-setup.md](wiki/setup/obsidian-setup.md)
- [wiki/setup/graphify-setup.md](wiki/setup/graphify-setup.md)

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
