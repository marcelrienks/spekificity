# SpecKit Enrich — Plan

## Description

Decorator for `/speckit.plan`. Loads graph context and identifies existing nodes referenced in the current spec before plan generation, then annotates the plan's Technical Context with impacted graph nodes. Prevents the planner from omitting or duplicating existing components.

**Decorator pattern**: This skill wraps `/speckit.plan` without replacing it. SpecKit remains the authoritative plan-writing engine.

## Trigger

Invoked by the developer in the AI chat session:
```
/speckit-enrich-plan
```

## Prerequisites

- `spec.md` exists for the current feature (created by `/speckit-enrich-specify` or `/speckit.specify`)
- Vault exists with a current graph (`vault/graph/index.md`)
- SpecKit initialised (`.specify/` exists)

## Inputs

No explicit inputs required. The skill reads the current feature's `spec.md` automatically.

## Steps

1. **Load graph context**:
   ```
   /context-load graph-only
   ```
   Focus on graph nodes only (decisions and patterns are not needed for planning enrichment).

2. **Read `spec.md`**: Read the current feature's spec, focusing on: the Overview, Requirements, and Key Entities sections.

3. **Identify impacted graph nodes**: Cross-reference entity names, file paths, and component names from `spec.md` against the loaded graph index. Build a list: "Impacted graph nodes: [node-id → path, relationship]."

4. **Annotate plan Technical Context**: Before invoking `/speckit.plan`, prepare the following annotation to be included in the plan's Technical Context section:
   ```
   Impacted graph nodes:
   - <node-id>: <path> (<relationship: modifies | creates | references>)
   ```

5. **Invoke `/speckit.plan`**: Run the standard SpecKit plan command. Pass the impacted node list as additional context for the Technical Context section.

6. **Post-write verification**: After `plan.md` is written, scan the plan's Project Structure section. Verify that each impacted node from step 3 appears somewhere in the plan (either as an existing file to modify or as a referenced component). If any are missing, add a note to the plan's Assumptions section: "Graph node [X] was identified as potentially impacted but not explicitly addressed in this plan."

## Outputs

Passthrough to `/speckit.plan` outputs:

| Output | Path | Description |
|--------|------|-------------|
| Implementation plan | `specs/<feature-dir>/plan.md` | Plan written by SpecKit, with impacted graph nodes in Technical Context |

## Error Handling

- **Vault missing / graph empty**: Proceed with unenriched `/speckit.plan` call. Note in plan Technical Context: "No vault graph available — impacted node analysis skipped."
- **`spec.md` missing**: Halt and inform developer: "No spec.md found for this feature. Run /speckit-enrich-specify first."
- **`/speckit.plan` fails**: Report the SpecKit error directly.

## Notes

- Activate `/caveman lite` before this skill for efficient token use during the planning session.
- Related: [skills/context-load/SKILL.md](../context-load/SKILL.md), [skills/speckit-enrich/specify-enrich.md](specify-enrich.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
