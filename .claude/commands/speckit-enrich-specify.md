# speckit enrich — specify

## description

decorator for `/speckit.specify`. loads graph context from the obsidian vault before spec generation, enriches the feature description with related existing components, and passes the enriched description to `/speckit.specify`. the resulting spec includes cross-references to existing graph nodes, making downstream planning more accurate.

**decorator pattern**: this skill wraps `/speckit.specify` without replacing it. speckit remains the authoritative spec-writing engine.

## trigger

invoked by the developer in the ai chat session:
```
/speckit-enrich-specify
```

## prerequisites

- spekificity initialised (see [workflows/init-workflow.md](../../workflows/init-workflow.md))
- feature description prepared (developer provides this)
- vault exists (`vault/graph/index.md` exists, or at minimum `vault/` is present)

## inputs

| input | description | required |
|-------|-------------|----------|
| feature description | the feature to specify (same text you would pass to `/speckit.specify`) | yes |

## steps

1. **load context** (if not already loaded this session):
   ```
   /context-load graph-only
   ```
   if vault is empty or missing, proceed without graph context and note the limitation.

2. **identify related existing components**: from the loaded graph index, identify any nodes whose path, name, or description is semantically related to the feature description. list them as "related existing components."

3. **annotate the feature description**:
   ```
   original: "add a user authentication module"
   enriched: "add a user authentication module
              related existing components: [src/users.py (user entity), src/api/routes.py (api routing), specs/002-user-model/spec.md (prior user spec)]"
   ```

4. **invoke `/speckit.specify`** with the enriched description as input. let speckit run its standard spec-writing workflow.

5. **post-write**: after `spec.md` is written, review the generated spec's assumptions section. if related graph nodes are not already referenced, add a note:
   ```
   - graph nodes likely impacted: [list from step 2]
   ```

## outputs

passthrough to `/speckit.specify` outputs:

| output | path | description |
|--------|------|-------------|
| feature spec | `specs/<feature-dir>/spec.md` | spec written by speckit, enriched with graph cross-references |

## error handling

- **vault missing / graph empty**: proceed with unenriched `/speckit.specify` call. note in spec assumptions: "no vault graph available — graph enrichment skipped."
- **`/speckit.specify` fails**: report the speckit error directly. this skill does not mask downstream errors.

## notes

- if `/context-load` was already run this session, skip step 1 — the context is already in working memory.
- for maximum enrichment quality, run `/map-codebase` before starting a new feature to ensure the graph is current.
- activate `/caveman lite` before this skill for efficient token use during the spec-writing session.
- related: [skills/context-load/skill.md](../context-load/skill.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
