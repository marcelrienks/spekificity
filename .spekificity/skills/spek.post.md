# /spek.post — post-implementation lifecycle skill

## description

captures structured lessons from the completed feature, refreshes the obsidian vault graph with the latest codebase state, and prepares a completion summary. invoked automatically at postflight by `/spek.automate`, and usable standalone at the end of any feature.

## trigger

```
/spek.post
```

optional: invoked by `/spek.automate` at postflight step 2. developer can also invoke manually after completing a feature.

## prerequisites

- feature implementation is complete (all tasks in `tasks.md` marked `[x]`)
- `vault/` directory exists
- `.spekificity/config.json` exists (for vault path resolution)
- git repo is accessible

## inputs

| input | source | description |
|-------|--------|-------------|
| `feature_branch` | `workflow-state.json` or `git branch --show-current` | identifies the feature for lesson tagging |
| `feature_dir` | `workflow-state.json` or auto-detect from branch name | spec directory (e.g. `specs/003-add-login/`) |
| `--no-lessons` flag | shell invocation | skip lessons-learnt step |
| `--no-graph` flag | shell invocation | skip map-codebase step |

## steps

### step 1 — read context

1. read `.spekificity/workflow-state.json` if it exists:
   - extract `feature_branch`, `feature_dir`, `feature_description`
   - note `completed_steps` for summary
2. if workflow-state.json is absent: fall back to `git branch --show-current` for branch name

### step 2 — developer reflection

prompt the developer to reflect on the feature. use `[spek] ❓` format:

```
[spek] ❓ post-implementation reflection (feature: <feature_branch>)

Please answer the following questions briefly:
> 1. What decisions were made during this feature? (architectural, design, or process)
> 2. What patterns emerged that could be reused?
> 3. What was harder than expected?
> 4. What worked particularly well?

(type your answers or press Enter to let the AI infer from the session)
```

if the developer presses Enter without answering, the AI infers answers from:
- the feature spec (`<feature_dir>/spec.md`)
- the plan (`<feature_dir>/plan.md`)
- the tasks completed in `tasks.md`

### step 3 — invoke `/spek.lessons-learnt`

invoke `/spek.lessons-learnt` (or `/lessons-learnt` if the spek. namespace is not registered) with:
- the developer's reflection answers (or AI-inferred answers) as context
- `feature_branch` and `feature_dir` explicitly provided

the skill writes:
- `vault/lessons/YYYY-MM-DD-<feature-slug>.md`
- appends new patterns to `vault/context/patterns.md`
- appends new decisions to `vault/context/decisions.md`

if `--no-lessons` flag was set, skip this step and log:
```
[spek] ⚠ --no-lessons set — skipping lesson capture
```

### step 4 — invoke `/spek.map-codebase --incremental`

invoke `/map-codebase --incremental` to refresh the vault graph with files changed during this feature. this ensures the next feature's context-load includes the new components.

if `--no-graph` flag was set, skip this step and log:
```
[spek] ⚠ --no-graph set — skipping graph refresh
```

### step 5 — update workflow-state.json

write to `.spekificity/workflow-state.json`:
```json
{
  "postflight": {
    "lessons_written": true,
    "graph_refreshed": true,
    "pr_created": false,
    "pr_url": null
  }
}
```
(preserve all other fields — merge, do not replace)

### step 6 — print completion summary

```
[spek] ✓ post-implementation complete
  feature:  <feature_description or feature_branch>
  lessons:  vault/lessons/YYYY-MM-DD-<slug>.md
  patterns: vault/context/patterns.md (updated)
  graph:    refreshed (incremental)
```

## outputs

| output | path | description |
|--------|------|-------------|
| lessons entry | `vault/lessons/YYYY-MM-DD-<slug>.md` | structured lessons record |
| updated patterns | `vault/context/patterns.md` | new patterns appended |
| updated decisions | `vault/context/decisions.md` | new decisions appended |
| updated graph | `vault/graph/` | incremental graph refresh |
| updated workflow-state | `.spekificity/workflow-state.json` | postflight flags set |

## error handling

| condition | action |
|-----------|--------|
| workflow-state.json missing | use git to detect branch; continue with defaults |
| vault/lessons/ missing | create directory with `mkdir -p vault/lessons/` |
| `/spek.lessons-learnt` fails | log warning, write raw reflection to `vault/lessons/YYYY-MM-DD-<slug>-raw.md` |
| graphify unavailable | log warning, skip graph refresh, mark `graph_refreshed: false` |
| developer reflection empty | AI infers from spec, plan, and tasks |

## notes

- this skill is invoked automatically by `/spek.automate` at postflight. it can also run standalone.
- PR creation is handled by `automate.sh` (not this skill) — `/spek.post` focuses on knowledge capture
- related: [skills/lessons-learnt/skill.md](../../skills/lessons-learnt/skill.md), [skills/map-codebase/skill.md](../../skills/map-codebase/skill.md)
