# architecture

spekificity has no runtime components. its "architecture" is the structure of its files and the contracts between them.

---

## design principles

- **decorator pattern**: spekificity skills wrap, not replace, standard speckit commands. vanilla speckit remains untouched and upgradable.
- **modular independence**: code graphing tool, knowledge vaulting tool, spec driven development tool, and the spekificity custom layer can each be updated independently.
- **global tools, local customisation**: some tools such as spec driven development tools may require global installation, while the intent of speckificity is local (project level) toolsets. speckificity will have a setup tool that automates the installation of global toolsets, and itself have a global functional toolset for initialising speckificity customisation functionality within a given project (as an example using the specify toolset, to setup speckit locally per project)
- **ai-executable setup**: wherever cli automation is impractical, setup is documented as step-by-step guides that an ai agent can follow.
- **token efficiency by default**: caveman mode and graph-based context loading are first-class citizens, not afterthoughts.

---
## Component Roles

### 1 skills (`skills/`)

skills are the primary deliverable of spekificity. each skill is a markdown file that an ai agent reads and executes. a skill file must contain:

- **description**: what this skill does and when to use it
- **trigger**: how it is invoked (command name or condition)
- **inputs**: what the skill expects before executing
- **steps**: ordered, unambiguous instructions the ai follows
- **outputs**: what the skill produces and where it is stored

### 3.2 cli scripts (`.spekificity/bin/` and `bin/`)

`bin/spek` is the globally-installable entry point. copy it to `/usr/local/bin/spek`. it finds the nearest `.spekificity/` directory by walking up the tree and dispatches to the appropriate script.

`.spekificity/bin/*.sh` scripts are the per-project implementations:
- `_lib.sh` — shared utilities: config read/write, atomic JSON writes, graph state computation (fresh/stale/absent), working-tree checks
- `prepare.sh` — checks vault graph staleness via `compute_graph_state()`, rebuilds with graphify if stale/absent, hands off to `/spek.prepare` skill
- `automate.sh` — runs preflight (clean tree check), generates `NNN-kebab-branch`, calls `git checkout -b`, writes `workflow-state.json`, hands off to `/spek.automate` skill
- `post.sh` — detects context from `workflow-state.json`, surfaces `--no-lessons` / `--no-graph` flags to skill

`workflow-state.json` schema (see `data-model.md` in feature spec for full definition):
```json
{
  "status": "in-progress | halted | complete",
  "current_step": "<step name>",
  "next_step": "<step name>",
  "completed_steps": ["preflight", "spec", "..."],
  "preflight": { "branch_created": true, "clean_working_tree": true },
  "postflight": { "lessons_written": false, "graph_refreshed": false, "pr_created": false, "pr_url": null }
}
```

### 3.3 workflows (`workflows/`)

workflows describe how skills compose into multi-step processes. a workflow document specifies:

- the ordered sequence of skill invocations
- decision points (e.g., "if vault does not exist, run `/map-codebase` first")
- expected state at each checkpoint
- how to recover from partial failures

### 3.4 setup guides (`setup-guides/`)

setup guides provide step-by-step, ai-executable installation and configuration instructions for each third-party prerequisite. they assume only that the ai has access to a terminal and internet.

### 3.5 obsidian vault (`vault/` or project-defined location)

the vault is the persistent context store for project documentation, essentially becoming an 'LLM wiki'. its structure is TDB.

The vault uses plain markdown and is compatible with obsidian's format. ai agents can read it directly without requiring the obsidian application to be running.

---

## component isolation and update strategy

spekificity's modular independence principle requires that each component can be updated without affecting the others. this is achieved through:

| component | isolation mechanism |
|-----------|-------------------|
| **speckit** | installed globally; spekificity skills invoke it by command name only (no internal api assumptions) |
| **codegraph** | invoked via cli in the `map-codebase` skill; only the skill file needs updating if the cli changes |
| **obsidian** | vault uses plain markdown; no dependency on obsidian internal format |
| **spekificity custom layer** | local per-project; updated by pulling latest from this repo |

### update procedures

- **speckit update**: `npm update -g specify` — no spekificity changes required unless speckit's command interface changes
- **graphify update**: update locally or globally; update only `skills/map-codebase/skill.md` if cli args change
- **obsidian update**: no action required (vault is plain markdown)
- **spekificity update**: `git pull` in the spekificity repo; copy updated skills to target project

---

## ai agent integration

### github copilot

- skills are placed in `.github/agents/` or referenced from `.github/copilot-instructions.md`
- the `copilot-instructions.md` file points to the active plan and constitution at session start

### claude code

- skills are placed in `.agents/` directory
- `agents.md` at the project root lists available skills and workflow entry points

### shared convention

all skills follow the same markdown structure regardless of ai agent. the `.agents/` directory is the canonical location; agent-specific directories are symlinks or copies.

---

## vault commit strategy

**recommended**: commit the vault to git with the project.

- **rationale**: vault entries (lessons learnt, decisions, patterns) are project artefacts with long-term value. version-controlling them preserves history and enables team sharing.
- **exception**: the `vault/graph/` directory may be gitignored on very large projects where graph size impacts repo performance. in this case, the graph is regenerated on each developer machine.

a `.gitignore` template covering this exception is included in the init workflow.

---

## open architecture decisions

| decision | options | status |
|----------|---------|--------|
| codegraph install mode | local npm package vs global install | open — depends on graphify's packaging |
| obsidian headless write | cli tool vs direct markdown writes | open — affects skills/map-codebase implementation |
| vault location | `vault/` in project root vs `.spekificity/vault/` | open — to be decided in planning phase |
| caveman integration point | always-on vs opt-in per session | open — user preference, configurable |
