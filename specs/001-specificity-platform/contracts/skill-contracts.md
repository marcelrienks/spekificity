# Contracts: Spekificity Platform — Skill Interface Specifications

**Phase**: 1 — Design  
**Date**: 2026-04-29  
**Feature**: 001-spekificity-platform

This document defines the invocation contracts for all Spekificity custom skills. Each contract specifies:
- Command name (how the developer/AI invokes it)
- Preconditions (what must be true before it runs)
- Inputs (what the skill needs)
- Outputs (what it produces and where)
- Postconditions (what is true after it succeeds)

---

## Skill: `/map-codebase`

**Skill file**: `skills/map-codebase/SKILL.md`  
**Purpose**: Build or refresh the Graphify → Obsidian graph map of the current project.

### Preconditions
- Spekificity has been initialised in the project (init workflow complete)
- `graphifyy` is installed globally (`graphify --version` succeeds)
- Current directory is the project root

### Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `--full` flag | optional flag | No | Force full regeneration instead of incremental refresh |
| `CLAUDE_API_KEY` | env var | No | Required only if semantic extraction of markdown docs is desired (beyond code AST) |

### Steps (contract, not implementation)
1. Run `graphify . --obsidian --output vault/graph/` from project root
2. Verify `vault/graph/index.md` exists
3. Update `vault/graph/index.md` with timestamp of last refresh
4. If vault did not previously exist, create `vault/lessons/` and `vault/context/` directories
5. Report: number of nodes added, updated, removed

### Outputs
| Output | Path | Description |
|--------|------|-------------|
| Graph index | `vault/graph/index.md` | Master entry point listing all nodes |
| Node files | `vault/graph/nodes/*.md` | One file per code/doc node |
| Raw graph | `vault/graph/graph.json` | Graphify NetworkX JSON (machine-readable) |
| Report | `vault/graph/GRAPH_REPORT.md` | Human/AI-readable summary of god nodes and surprising connections |
| Graph visual | `vault/graph/graph.html` | Interactive browser visualization (optional) |

### Postconditions
- `vault/graph/index.md` is current (timestamp matches current run)
- All source files and docs are represented as nodes
- AI agents can load `vault/graph/index.md` to navigate the graph without scanning source files

### Error Handling
- If `graphify` is not installed → print install instructions from `setup-guides/graphify-setup.md` and halt
- If `vault/graph/` write fails (permissions) → report error with path and halt; do not partially write

---

## Skill: `/lessons-learnt`

**Skill file**: `skills/lessons-learnt/SKILL.md`  
**Purpose**: Capture structured lessons at the end of a SpecKit feature lifecycle and write them to the Obsidian vault.

### Preconditions
- A SpecKit feature implementation is complete (or at a meaningful checkpoint)
- `vault/lessons/` directory exists (created by `/map-codebase` or init)
- Current feature branch name is known

### Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Feature branch name | string | Yes | Used as slug in filename (auto-detected from git) |
| Date | string | Yes | ISO 8601 date (auto-detected) |
| AI model name | string | Yes | Name of AI agent and model used (e.g., "GitHub Copilot / Claude Sonnet 4.6") |

### Steps (contract)
1. Detect current git branch name
2. Prompt AI to reflect on: what worked, what was harder than expected, decisions made, patterns identified
3. Write entry to `vault/lessons/<YYYY-MM-DD>-<feature-slug>.md` using the lessons learnt schema (see data-model.md)
4. Append a summary line to `vault/context/patterns.md` for any new patterns
5. Append decisions to `vault/context/decisions.md`
6. Report: file path written

### Outputs
| Output | Path | Description |
|--------|------|-------------|
| Lessons entry | `vault/lessons/<date>-<slug>.md` | Full structured lessons record |
| Updated patterns | `vault/context/patterns.md` | Appended with new patterns |
| Updated decisions | `vault/context/decisions.md` | Appended with new decisions |

### Postconditions
- A lessons entry exists for the completed feature
- `vault/context/` is updated with reusable knowledge
- Future `/context-load` calls will surface this entry

---

## Skill: `/context-load`

**Skill file**: `skills/context-load/SKILL.md`  
**Purpose**: Load persistent context from the Obsidian vault at the start of an AI session to orient the agent without scanning source files.

### Preconditions
- `vault/` directory exists
- `vault/graph/index.md` exists (at minimum)

### Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Scope | string | No | `full` (default) or `graph-only` or `lessons-only` |
| Feature context | string | No | A feature name or branch to filter lessons context |

### Steps (contract)
1. Read `vault/graph/index.md` — load node list and key relationships
2. Read `vault/context/decisions.md` — load architectural decisions
3. Read `vault/context/patterns.md` — load identified patterns
4. If `vault/lessons/` contains entries for the current branch, read the most recent one
5. Summarise loaded context in a brief header (≤5 bullet points) using Caveman format if Caveman mode is active
6. Confirm to the developer: "Context loaded. [N] graph nodes, [M] decisions, [K] patterns. Ready."

### Outputs
| Output | Location | Description |
|--------|----------|-------------|
| Active context | AI working memory | Vault summary held in session context |

### Postconditions
- AI agent holds current graph structure, decisions, and patterns in session context
- Subsequent AI responses reference vault entries rather than scanning files

---

## Skill: `/speckit-enrich-specify`

**Skill file**: `skills/speckit-enrich/specify-enrich.md`  
**Purpose**: Decorator for `/speckit.specify` — loads graph context before spec generation to produce a context-aware spec.

### Preconditions
- `/context-load` has been run this session (or vault exists)
- User has a feature description ready

### Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Feature description | string | Yes | The feature to specify (passed through to `/speckit.specify`) |

### Steps (contract)
1. Run `/context-load` (if not already run this session)
2. Identify from graph any existing components related to the feature description
3. Annotate the feature description with: "Related existing components: [list from graph]"
4. Invoke `/speckit.specify` with the enriched description
5. After spec is written, note any graph nodes that will likely be impacted in the spec's Assumptions section

### Outputs
Passthrough to `/speckit.specify` outputs (`spec.md`), enriched with graph cross-references.

---

## Skill: `/speckit-enrich-plan`

**Skill file**: `skills/speckit-enrich/plan-enrich.md`  
**Purpose**: Decorator for `/speckit.plan` — ensures the plan references existing graph nodes that will be affected.

### Preconditions
- `spec.md` exists for the current feature
- Vault graph is current (recent `/map-codebase` run)

### Steps (contract)
1. Run `/context-load graph-only` (refresh graph context)
2. Identify graph nodes referenced in `spec.md` (by name or path)
3. Annotate the plan's Technical Context section with: "Impacted graph nodes: [list]"
4. Invoke `/speckit.plan`
5. After plan is written, verify that no impacted nodes are missing from the plan's Project Structure section

### Outputs
Passthrough to `/speckit.plan` outputs (`plan.md`), enriched with impacted node references.

---

## Skill: `/speckit-enrich-implement`

**Skill file**: `skills/speckit-enrich/implement-enrich.md`  
**Purpose**: Decorator for `/speckit.implement` — loads graph context during implementation to avoid inconsistencies with existing code.

### Preconditions
- `tasks.md` exists for the current feature
- Vault graph is current

### Steps (contract)
1. Run `/context-load` at session start
2. For each task in `tasks.md`, check graph for related nodes before implementing
3. After all tasks complete, invoke `/lessons-learnt` automatically
4. Invoke `/map-codebase` (incremental) to update the graph with new nodes

### Outputs
Passthrough to `/speckit.implement` outputs, plus:
- Updated vault graph (`/map-codebase` incremental run)
- Lessons learnt entry (`/lessons-learnt`)
