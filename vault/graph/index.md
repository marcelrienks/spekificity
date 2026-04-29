---
last_updated: YYYY-MM-DDTHH:MM:SSZ
generated_by: graphifyy
node_count: 0
god_node_count: 0
---

# Vault Graph Index

> **Note**: This file is a template. It is overwritten by `/map-codebase` (Graphify) at runtime. Do not edit manually — changes will be lost on the next map run.
>
> After running `/map-codebase`, this file will contain a live index of all project nodes.

---

## Last Run

| Field | Value |
|-------|-------|
| Generated | *(timestamp written by Graphify)* |
| Total nodes | *(count written by Graphify)* |
| God nodes | *(count written by Graphify)* |
| Run mode | incremental / full |

---

## God Nodes

God nodes are files with unusually high connectivity — they are the most important files to understand when assessing the impact of any change.

| Node ID | Path | Connections |
|---------|------|-------------|
| *(populated by Graphify)* | | |

---

## All Nodes

| Node ID | Type | Path | Language | Last Updated |
|---------|------|------|----------|-------------|
| *(populated by Graphify)* | | | | |

---

## How to Use This Index

**For AI agents**:
1. Read this file at session start (or use `/context-load` which reads it automatically)
2. Use node IDs to navigate to `vault/graph/nodes/<node-id>.md` for detailed information about a specific file
3. Reference god nodes first when assessing the blast radius of any change
4. Do not scan source directories recursively — use this index instead

**For developers**:
- Run `/map-codebase` to refresh this index after adding or deleting files
- Run `/map-codebase --full` after large refactors
- See [workflows/map-refresh.md](../../workflows/map-refresh.md) for refresh timing guidance
