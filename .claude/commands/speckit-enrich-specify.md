# SpecKit Enrich — Specify

## Description

Decorator for `/speckit.specify`. Loads graph context from the Obsidian vault before spec generation, enriches the feature description with related existing components, and passes the enriched description to `/speckit.specify`. The resulting spec includes cross-references to existing graph nodes, making downstream planning more accurate.

**Decorator pattern**: This skill wraps `/speckit.specify` without replacing it. SpecKit remains the authoritative spec-writing engine.

## Trigger

Invoked by the developer in the AI chat session:
```
/speckit-enrich-specify
```

## Prerequisites

- Spekificity initialised (see [workflows/init-workflow.md](../../workflows/init-workflow.md))
- Feature description prepared (developer provides this)
- Vault exists (`vault/graph/index.md` exists, or at minimum `vault/` is present)

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| Feature description | The feature to specify (same text you would pass to `/speckit.specify`) | Yes |

## Steps

1. **Load context** (if not already loaded this session):
   ```
   /context-load graph-only
   ```
   If vault is empty or missing, proceed without graph context and note the limitation.

2. **Identify related existing components**: From the loaded graph index, identify any nodes whose path, name, or description is semantically related to the feature description. List them as "Related existing components."

3. **Annotate the feature description**:
   ```
   Original: "Add a user authentication module"
   Enriched: "Add a user authentication module
              Related existing components: [src/users.py (User entity), src/api/routes.py (API routing), specs/002-user-model/spec.md (prior user spec)]"
   ```

4. **Invoke `/speckit.specify`** with the enriched description as input. Let SpecKit run its standard spec-writing workflow.

5. **Post-write**: After `spec.md` is written, review the generated spec's Assumptions section. If related graph nodes are not already referenced, add a note:
   ```
   - Graph nodes likely impacted: [list from step 2]
   ```

## Outputs

Passthrough to `/speckit.specify` outputs:

| Output | Path | Description |
|--------|------|-------------|
| Feature spec | `specs/<feature-dir>/spec.md` | Spec written by SpecKit, enriched with graph cross-references |

## Error Handling

- **Vault missing / graph empty**: Proceed with unenriched `/speckit.specify` call. Note in spec Assumptions: "No vault graph available — graph enrichment skipped."
- **`/speckit.specify` fails**: Report the SpecKit error directly. This skill does not mask downstream errors.

## Notes

- If `/context-load` was already run this session, skip step 1 — the context is already in working memory.
- For maximum enrichment quality, run `/map-codebase` before starting a new feature to ensure the graph is current.
- Activate `/caveman lite` before this skill for efficient token use during the spec-writing session.
- Related: [skills/context-load/SKILL.md](../context-load/SKILL.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
