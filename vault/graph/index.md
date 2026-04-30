---
last_updated: yyyy-mm-ddthh:mm:ssz
generated_by: graphifyy
node_count: 0
god_node_count: 0
---

# vault graph index

> **note**: this file is a template. it is overwritten by `/map-codebase` (graphify) at runtime. do not edit manually — changes will be lost on the next map run.
>
> after running `/map-codebase`, this file will contain a live index of all project nodes.

---

## last run

| field | value |
|-------|-------|
| generated | *(timestamp written by graphify)* |
| total nodes | *(count written by graphify)* |
| god nodes | *(count written by graphify)* |
| run mode | incremental / full |

---

## god nodes

god nodes are files with unusually high connectivity — they are the most important files to understand when assessing the impact of any change.

| node id | path | connections |
|---------|------|-------------|
| *(populated by graphify)* | | |

---

## all nodes

| node id | type | path | language | last updated |
|---------|------|------|----------|-------------|
| *(populated by graphify)* | | | | |

---

## how to use this index

**for ai agents**:
1. read this file at session start (or use `/context-load` which reads it automatically)
2. use node ids to navigate to `vault/graph/nodes/<node-id>.md` for detailed information about a specific file
3. reference god nodes first when assessing the blast radius of any change
4. do not scan source directories recursively — use this index instead

**for developers**:
- run `/map-codebase` to refresh this index after adding or deleting files
- run `/map-codebase --full` after large refactors
- see [workflows/map-refresh.md](../../workflows/map-refresh.md) for refresh timing guidance
