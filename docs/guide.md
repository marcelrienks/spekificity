# guide

step-by-step workflows for common spekificity operations.

---

## full feature lifecycle (enriched speckit workflow)

### before you start

- run `/context-load` to load vault context into your ai session
- run `/map-codebase` if you haven't already built the graph

### step 1: specification

```bash
/speckit.specify
```

ai reads your obsidian vault (codebase graph, past decisions, lessons learnt) and your feature description, then produces a specification that is grounded in your actual codebase structure.

**what you provide**: feature description or user story

**what you get**: `spec.md` with:
- overview and context
- functional and non-functional requirements
- success criteria (measurable outcomes)
- user stories with acceptance criteria
- edge cases and constraints

**see also**: [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md)

---

### step 2: planning

```bash
/speckit.plan
```

ai reads your spec and vault, then produces an implementation plan that references existing components and architectural patterns.

**what you provide**: completed `spec.md`

**what you get**: `plan.md` with:
- architecture or design decisions
- data model (if applicable)
- implementation phases
- technical constraints and dependencies

**output location**: `specs/NNN-feature-name/plan.md`

---

### step 3: task generation

```bash
/speckit.tasks
```

ai generates an actionable, dependency-ordered task list from your spec and plan.

**what you provide**: completed `spec.md` and `plan.md`

**what you get**: `tasks.md` with:
- ordered list of tasks, grouped by phase
- task descriptions with acceptance criteria
- dependencies between tasks (marked with [p] for parallel tasks)
- estimated effort or complexity

**output location**: `specs/NNN-feature-name/tasks.md`

---

### step 4: implementation

```bash
/speckit.implement
```

ai executes the implementation plan by processing and implementing all tasks in order. this step reads from your obsidian vault context to reference existing code patterns and decisions.

**what you provide**: completed `spec.md`, `plan.md`, and `tasks.md`

**what you get**: all code, tests, and documentation changes for the feature

**note**: this step is long-running. ai may ask for clarification or confirmation during implementation.

---

### step 5: lessons learnt

```bash
/lessons-learnt
```

at feature completion, run this skill to capture structured lessons, decisions made, problems encountered, and recommendations for future features.

**what this does**:
- prompts you for key decisions, patterns, and recommendations
- appends a structured entry to `vault/lessons/`
- entry is indexed in the obsidian vault and available to future sessions

**output location**: `vault/lessons/yyyy-mm-dd-feature-name.md`

---

## mapping an existing codebase

### first time setup

```bash
/map-codebase
```

ai runs graphify against your source files and documentation to generate a dependency graph. the graph is stored as an obsidian vault inside your project.

**what happens**:
1. graphify analyzes source files (python, typescript, javascript, markdown, etc.)
2. generates a relationship graph (imports, references, dependencies)
3. stores graph as markdown nodes in `vault/graph/`
4. creates an index at `vault/graph/index.md`

**future sessions**: load the vault index with `/context-load` instead of scanning files. this saves 40%+ tokens on cross-cutting queries like "where is authentication handled?"

see also: [workflows/map-refresh.md](../workflows/map-refresh.md)

---

## spek cli — automated feature lifecycle

the `spek` cli entry point drives the full feature lifecycle from a single shell command. install it once and run from any project directory.

### install

```bash
# copy to PATH (one-time, global)
cp bin/spek /usr/local/bin/spek
chmod +x /usr/local/bin/spek
```

### workflow: setup → init → prepare → automate → post

| step | command | what it does |
|------|---------|--------------|
| 1. setup | `spek setup` | install prerequisites (graphify, obsidian, speckit) |
| 2. init | `spek init` | create `.spekificity/` config, link vault, scaffold skills |
| 3. prepare | `spek prepare` | check vault graph freshness; rebuild if stale; invoke `/spek.prepare` |
| 4. automate | `spek automate "<description>"` | run full lifecycle: branch → spec → plan → tasks → analyse → implement → postflight |
| 5. post | `spek post` | lessons capture + vault graph refresh (run after manual feature work) |

### quick reference

```bash
# full automated lifecycle
spek automate "add user authentication with JWT"

# resume an interrupted automate session
spek automate --resume

# skip PR creation
spek automate --no-pr "spike: explore graphify modes"

# post-implementation (lessons + graph)
spek post
spek post --no-lessons   # skip lessons capture
spek post --no-graph     # skip graph refresh

# check project status
spek status
```

### links

- [setup guide](../setup-guides/): prerequisites for each component
- [init workflow](../workflows/init-workflow.md): detailed initialisation steps
- [skills reference](.spekificity/skills/): skill definitions invoked by each step

---

## managing components

see [workflows/component-update.md](../workflows/component-update.md) for how to independently update graphify, obsidian, speckit, or spekificity skills without breaking other components.

---

## token efficiency

activate caveman mode at any point to compress responses:

```bash
/caveman lite       ← no filler/hedging, keep professional tone
/caveman full       ← classic caveman: drop articles, use fragments
/caveman ultra      ← maximum compression, abbreviate prose
```

see [glossary.md](glossary.md#caveman-mode--caveman-skill) for details.
