# contracts: spekificity platform — skill interface specifications

**phase**: 1 — design  
**date**: 2026-04-29  
**feature**: 001-spekificity-platform

this document defines the invocation contracts for all spekificity custom skills. each contract specifies:
- command name (how the developer/ai invokes it)
- preconditions (what must be true before it runs)
- inputs (what the skill needs)
- outputs (what it produces and where)
- postconditions (what is true after it succeeds)

---

## skill: `/map-codebase`

**skill file**: `skills/map-codebase/skill.md`  
**purpose**: build or refresh the graphify → obsidian graph map of the current project.

### preconditions
- spekificity has been initialised in the project (init workflow complete)
- `graphifyy` is installed globally (`graphify --version` succeeds)
- current directory is the project root

### inputs
| input | type | required | description |
|-------|------|----------|-------------|
| `--full` flag | optional flag | no | force full regeneration instead of incremental refresh |
| `claude_api_key` | env var | no | required only if semantic extraction of markdown docs is desired (beyond code ast) |

### steps (contract, not implementation)
1. run `graphify . --obsidian --output vault/graph/` from project root
2. verify `vault/graph/index.md` exists
3. update `vault/graph/index.md` with timestamp of last refresh
4. if vault did not previously exist, create `vault/lessons/` and `vault/context/` directories
5. report: number of nodes added, updated, removed

### outputs
| output | path | description |
|--------|------|-------------|
| graph index | `vault/graph/index.md` | master entry point listing all nodes |
| node files | `vault/graph/nodes/*.md` | one file per code/doc node |
| raw graph | `vault/graph/graph.json` | graphify networkx json (machine-readable) |
| report | `vault/graph/graph_report.md` | human/ai-readable summary of god nodes and surprising connections |
| graph visual | `vault/graph/graph.html` | interactive browser visualization (optional) |

### postconditions
- `vault/graph/index.md` is current (timestamp matches current run)
- all source files and docs are represented as nodes
- ai agents can load `vault/graph/index.md` to navigate the graph without scanning source files

### error handling
- if `graphify` is not installed → print install instructions from `setup-guides/graphify-setup.md` and halt
- if `vault/graph/` write fails (permissions) → report error with path and halt; do not partially write

---

## skill: `/lessons-learnt`

**skill file**: `skills/lessons-learnt/skill.md`  
**purpose**: capture structured lessons at the end of a speckit feature lifecycle and write them to the obsidian vault.

### preconditions
- a speckit feature implementation is complete (or at a meaningful checkpoint)
- `vault/lessons/` directory exists (created by `/map-codebase` or init)
- current feature branch name is known

### inputs
| input | type | required | description |
|-------|------|----------|-------------|
| feature branch name | string | yes | used as slug in filename (auto-detected from git) |
| date | string | yes | iso 8601 date (auto-detected) |
| ai model name | string | yes | name of ai agent and model used (e.g., "github copilot / claude sonnet 4.6") |

### steps (contract)
1. detect current git branch name
2. prompt ai to reflect on: what worked, what was harder than expected, decisions made, patterns identified
3. write entry to `vault/lessons/<yyyy-mm-dd>-<feature-slug>.md` using the lessons learnt schema (see data-model.md)
4. append a summary line to `vault/context/patterns.md` for any new patterns
5. append decisions to `vault/context/decisions.md`
6. report: file path written

### outputs
| output | path | description |
|--------|------|-------------|
| lessons entry | `vault/lessons/<date>-<slug>.md` | full structured lessons record |
| updated patterns | `vault/context/patterns.md` | appended with new patterns |
| updated decisions | `vault/context/decisions.md` | appended with new decisions |

### postconditions
- a lessons entry exists for the completed feature
- `vault/context/` is updated with reusable knowledge
- future `/context-load` calls will surface this entry

---

## skill: `/context-load`

**skill file**: `skills/context-load/skill.md`  
**purpose**: load persistent context from the obsidian vault at the start of an ai session to orient the agent without scanning source files.

### preconditions
- `vault/` directory exists
- `vault/graph/index.md` exists (at minimum)

### inputs
| input | type | required | description |
|-------|------|----------|-------------|
| scope | string | no | `full` (default) or `graph-only` or `lessons-only` |
| feature context | string | no | a feature name or branch to filter lessons context |

### steps (contract)
1. read `vault/graph/index.md` — load node list and key relationships
2. read `vault/context/decisions.md` — load architectural decisions
3. read `vault/context/patterns.md` — load identified patterns
4. if `vault/lessons/` contains entries for the current branch, read the most recent one
5. summarise loaded context in a brief header (≤5 bullet points) using caveman format if caveman mode is active
6. confirm to the developer: "context loaded. [n] graph nodes, [m] decisions, [k] patterns. ready."

### outputs
| output | location | description |
|--------|----------|-------------|
| active context | ai working memory | vault summary held in session context |

### postconditions
- ai agent holds current graph structure, decisions, and patterns in session context
- subsequent ai responses reference vault entries rather than scanning files

---

## skill: `/speckit-enrich-specify`

**skill file**: `skills/speckit-enrich/specify-enrich.md`  
**purpose**: decorator for `/speckit.specify` — loads graph context before spec generation to produce a context-aware spec.

### preconditions
- `/context-load` has been run this session (or vault exists)
- user has a feature description ready

### inputs
| input | type | required | description |
|-------|------|----------|-------------|
| feature description | string | yes | the feature to specify (passed through to `/speckit.specify`) |

### steps (contract)
1. run `/context-load` (if not already run this session)
2. identify from graph any existing components related to the feature description
3. annotate the feature description with: "related existing components: [list from graph]"
4. invoke `/speckit.specify` with the enriched description
5. after spec is written, note any graph nodes that will likely be impacted in the spec's assumptions section

### outputs
passthrough to `/speckit.specify` outputs (`spec.md`), enriched with graph cross-references.

---

## skill: `/speckit-enrich-plan`

**skill file**: `skills/speckit-enrich/plan-enrich.md`  
**purpose**: decorator for `/speckit.plan` — ensures the plan references existing graph nodes that will be affected.

### preconditions
- `spec.md` exists for the current feature
- vault graph is current (recent `/map-codebase` run)

### steps (contract)
1. run `/context-load graph-only` (refresh graph context)
2. identify graph nodes referenced in `spec.md` (by name or path)
3. annotate the plan's technical context section with: "impacted graph nodes: [list]"
4. invoke `/speckit.plan`
5. after plan is written, verify that no impacted nodes are missing from the plan's project structure section

### outputs
passthrough to `/speckit.plan` outputs (`plan.md`), enriched with impacted node references.

---

## skill: `/speckit-enrich-implement`

**skill file**: `skills/speckit-enrich/implement-enrich.md`  
**purpose**: decorator for `/speckit.implement` — loads graph context during implementation to avoid inconsistencies with existing code.

### preconditions
- `tasks.md` exists for the current feature
- vault graph is current

### steps (contract)
1. run `/context-load` at session start
2. for each task in `tasks.md`, check graph for related nodes before implementing
3. after all tasks complete, invoke `/lessons-learnt` automatically
4. invoke `/map-codebase` (incremental) to update the graph with new nodes

### outputs
passthrough to `/speckit.implement` outputs, plus:
- updated vault graph (`/map-codebase` incremental run)
- lessons learnt entry (`/lessons-learnt`)
