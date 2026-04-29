# SpecKit Enrich — Implement

## Description

Decorator for `/speckit.implement`. Loads graph context at session start, cross-references the vault before each task to avoid inconsistencies with existing code, and after all tasks complete automatically invokes `/lessons-learnt` and `/map-codebase` to update the vault with the results of the feature.

**Decorator pattern**: This skill wraps `/speckit.implement` without replacing it. SpecKit remains the authoritative implementation engine.

## Trigger

Invoked by the developer in the AI chat session:
```
/speckit-enrich-implement
```

## Prerequisites

- `tasks.md` exists for the current feature (created by `/speckit.tasks`)
- `plan.md` exists for the current feature
- Vault exists with a current graph (`vault/graph/index.md`)
- SpecKit initialised (`.specify/` exists)

## Inputs

No explicit inputs required. The skill reads `tasks.md` and the vault automatically.

## Steps

1. **Load full context**:
   ```
   /context-load full
   ```
   Load graph, decisions, patterns, and any prior lessons for this feature. This is the only context-load needed for the entire implementation session.

2. **For each task** in `tasks.md` (before implementing):
   - Check the vault graph for nodes related to that task's file path or component name
   - If a related node exists, note its current state (e.g., "this file already exists as node X — implementation should modify, not recreate")
   - Proceed with the task as defined by `/speckit.implement`

3. **Invoke `/speckit.implement`**: Run the standard SpecKit implement command. The vault context loaded in step 1 is available in working memory throughout.

4. **Post-completion — invoke `/lessons-learnt`** automatically:
   ```
   /lessons-learnt
   ```
   Capture structured lessons for this feature before the context is lost.

5. **Post-completion — run incremental map refresh**:
   ```
   /map-codebase
   ```
   Update the vault graph with any new or modified files created during implementation.

6. **Report completion**: "Feature implementation complete. Lessons written to vault. Graph updated."

## Outputs

Passthrough to `/speckit.implement` outputs (all tasks completed), plus:

| Output | Path | Description |
|--------|------|-------------|
| Completed tasks | Per `tasks.md` | All tasks marked `[X]` by SpecKit |
| Lessons entry | `vault/lessons/<date>-<slug>.md` | Written by `/lessons-learnt` |
| Updated vault graph | `vault/graph/` | Refreshed by `/map-codebase` incremental |

## Error Handling

- **Vault missing / graph empty**: Proceed with unenriched `/speckit.implement`. Note: "No vault graph available — graph cross-check skipped."
- **`tasks.md` missing**: Halt and inform developer: "No tasks.md found. Run /speckit.tasks first."
- **`/speckit.implement` fails mid-way**: Do not invoke `/lessons-learnt` or `/map-codebase` automatically. Inform developer: "Implementation halted at task [X]. Resolve the failure, then re-run. When complete, manually invoke /lessons-learnt and /map-codebase."
- **`/lessons-learnt` fails**: Report the error and provide the manual invocation command. Do not block or undo completed work.
- **`/map-codebase` fails**: Report the error. Implementation is complete — only the vault update failed. Developer can re-run `/map-codebase` manually.

## Notes

- Activate `/caveman` (full mode) before this skill — implementation sessions benefit from maximum compression to keep tasks focused.
- If the implementation session is interrupted and restarted, re-run `/context-load` at the top of the new session before continuing.
- Related: [skills/lessons-learnt/SKILL.md](../lessons-learnt/SKILL.md), [skills/map-codebase/SKILL.md](../map-codebase/SKILL.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
