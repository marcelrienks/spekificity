# speckit enrich — implement

## description

decorator for `/speckit.implement`. loads graph context at session start, cross-references the vault before each task to avoid inconsistencies with existing code, and after all tasks complete automatically invokes `/lessons-learnt` and `/map-codebase` to update the vault with the results of the feature.

**decorator pattern**: this skill wraps `/speckit.implement` without replacing it. speckit remains the authoritative implementation engine.

## trigger

invoked by the developer in the ai chat session:
```
/speckit-enrich-implement
```

## prerequisites

- `tasks.md` exists for the current feature (created by `/speckit.tasks`)
- `plan.md` exists for the current feature
- vault exists with a current graph (`vault/graph/index.md`)
- speckit initialised (`.specify/` exists)

## inputs

no explicit inputs required. the skill reads `tasks.md` and the vault automatically.

## steps

1. **load full context**:
   ```
   /context-load full
   ```
   load graph, decisions, patterns, and any prior lessons for this feature. this is the only context-load needed for the entire implementation session.

2. **for each task** in `tasks.md` (before implementing):
   - check the vault graph for nodes related to that task's file path or component name
   - if a related node exists, note its current state (e.g., "this file already exists as node x — implementation should modify, not recreate")
   - proceed with the task as defined by `/speckit.implement`

3. **invoke `/speckit.implement`**: run the standard speckit implement command. the vault context loaded in step 1 is available in working memory throughout.

4. **post-completion — invoke `/lessons-learnt`** automatically:
   ```
   /lessons-learnt
   ```
   capture structured lessons for this feature before the context is lost.

5. **post-completion — run incremental map refresh**:
   ```
   /map-codebase
   ```
   update the vault graph with any new or modified files created during implementation.

6. **report completion**: "feature implementation complete. lessons written to vault. graph updated."

## outputs

passthrough to `/speckit.implement` outputs (all tasks completed), plus:

| output | path | description |
|--------|------|-------------|
| completed tasks | per `tasks.md` | all tasks marked `[x]` by speckit |
| lessons entry | `vault/lessons/<date>-<slug>.md` | written by `/lessons-learnt` |
| updated vault graph | `vault/graph/` | refreshed by `/map-codebase` incremental |

## error handling

- **vault missing / graph empty**: proceed with unenriched `/speckit.implement`. note: "no vault graph available — graph cross-check skipped."
- **`tasks.md` missing**: halt and inform developer: "no tasks.md found. run /speckit.tasks first."
- **`/speckit.implement` fails mid-way**: do not invoke `/lessons-learnt` or `/map-codebase` automatically. inform developer: "implementation halted at task [x]. resolve the failure, then re-run. when complete, manually invoke /lessons-learnt and /map-codebase."
- **`/lessons-learnt` fails**: report the error and provide the manual invocation command. do not block or undo completed work.
- **`/map-codebase` fails**: report the error. implementation is complete — only the vault update failed. developer can re-run `/map-codebase` manually.

## notes

- activate `/caveman` (full mode) before this skill — implementation sessions benefit from maximum compression to keep tasks focused.
- if the implementation session is interrupted and restarted, re-run `/context-load` at the top of the new session before continuing.
- related: [skills/lessons-learnt/skill.md](../lessons-learnt/skill.md), [skills/map-codebase/skill.md](../map-codebase/skill.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
