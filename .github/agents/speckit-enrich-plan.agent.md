# speckit enrich — plan

## description

decorator for `/speckit.plan`. loads graph context and identifies existing nodes referenced in the current spec before plan generation, then annotates the plan's technical context with impacted graph nodes. prevents the planner from omitting or duplicating existing components.

**decorator pattern**: this skill wraps `/speckit.plan` without replacing it. speckit remains the authoritative plan-writing engine.

## trigger

invoked by the developer in the ai chat session:
```
/speckit-enrich-plan
```

## prerequisites

- `spec.md` exists for the current feature (created by `/speckit-enrich-specify` or `/speckit.specify`)
- vault exists with a current graph (`vault/graph/index.md`)
- speckit initialised (`.specify/` exists)

## inputs

no explicit inputs required. the skill reads the current feature's `spec.md` automatically.

## steps

1. **load graph context**:
   ```
   /context-load graph-only
   ```
   focus on graph nodes only (decisions and patterns are not needed for planning enrichment).

2. **read `spec.md`**: read the current feature's spec, focusing on: the overview, requirements, and key entities sections.

3. **identify impacted graph nodes**: cross-reference entity names, file paths, and component names from `spec.md` against the loaded graph index. build a list: "impacted graph nodes: [node-id → path, relationship]."

4. **annotate plan technical context**: before invoking `/speckit.plan`, prepare the following annotation to be included in the plan's technical context section:
   ```
   impacted graph nodes:
   - <node-id>: <path> (<relationship: modifies | creates | references>)
   ```

5. **invoke `/speckit.plan`**: run the standard speckit plan command. pass the impacted node list as additional context for the technical context section.

6. **post-write verification**: after `plan.md` is written, scan the plan's project structure section. verify that each impacted node from step 3 appears somewhere in the plan (either as an existing file to modify or as a referenced component). if any are missing, add a note to the plan's assumptions section: "graph node [x] was identified as potentially impacted but not explicitly addressed in this plan."

## outputs

passthrough to `/speckit.plan` outputs:

| output | path | description |
|--------|------|-------------|
| implementation plan | `specs/<feature-dir>/plan.md` | plan written by speckit, with impacted graph nodes in technical context |

## error handling

- **vault missing / graph empty**: proceed with unenriched `/speckit.plan` call. note in plan technical context: "no vault graph available — impacted node analysis skipped."
- **`spec.md` missing**: halt and inform developer: "no spec.md found for this feature. run /speckit-enrich-specify first."
- **`/speckit.plan` fails**: report the speckit error directly.

## notes

- activate `/caveman lite` before this skill for efficient token use during the planning session.
- related: [skills/context-load/skill.md](../context-load/skill.md), [skills/speckit-enrich/specify-enrich.md](specify-enrich.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
