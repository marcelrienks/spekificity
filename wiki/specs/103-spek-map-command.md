# ATOMIC SPECIFICATION: /spek.map Command (C5.3)

**Depends On:** 050-latmd-setup-and-integration.md, graph-storage-structure.md
**Used By:** /spek.prepare (Step 4), /spek.conclude (Step 8)  

---

## Overview

`/spek.map` queries and maintains the project index through `lat.md` MCP (markdown-first indexed code + doc analysis), Obsidian export (doc pass), and merge (unified graph). `lat.md` handles indexing and provides MCP query tools; `/spek.map` focuses on querying and keeping documentation in sync.

---

## Modes

### Mode 1: Full Refresh

```bash
/spek.map --full
```

**Process:**
1. Query lat.md for all symbols (fresh scan, no cache)
2. Doc pass: export Obsidian vault
3. Merge: combine code symbols + doc nodes into unified graph
4. Validate: check schema + node count
5. Write: wiki/vault/graph/nodes.jsonl + edges.jsonl + config.json

**Cost:** 1-3 seconds (lat.md queries include incremental updates; optional file-watcher can provide near-real-time refresh)

**When to use:** After major refactoring, or to refresh cached snapshot

### Mode 2: Incremental Sync (Default)

```bash
/spek.map
```

**Process:**
1. Query lat.md for recently modified symbols (lat.md can be configured to watch files or be refreshed on-demand)
2. Doc pass: check Obsidian vault for new/changed files
3. Merge: update affected nodes + edges incrementally
4. Validate + write

**Cost:** < 500ms (lat.md handles incremental indexing or file-watcher updates; /spek.map only merges + writes)

**When to use:** Normal workflow (after /spek.prepare, end of feature)

### Mode 3: Query-Only (No Sync)

```bash
/spek.map --query [symbol|file]
```

**Process:**
1. Query lat.md for specific symbol or file
2. Return results (no file writes)

**Cost:** < 100ms (lat.md MCP query)

**When to use:** During implementation when you need to explore code structure without updating graph

---

## Command Sequence

```
/spek.map [mode]
├─ Phase 1: Setup
│  ├─ Parse arguments
│  ├─ Validate config.yaml
│  ├─ Verify lat.md is available (MCP tool check)
│  └─ Create wiki/vault/graph/ if missing
├─ Phase 2: Code Pass (lat.md Query)
│  ├─ Call lat_symbols (all | recent-only, based on mode)
│  ├─ Call lat_references + lat_impact for each symbol
│  └─ Output: code symbol nodes with edges
├─ Phase 3: Doc Pass (Obsidian Export)
│  ├─ Export vault via cache.json or plugin
│  └─ Output: doc nodes
├─ Phase 4: Merge
│  ├─ Combine code symbols + doc nodes
│  ├─ Deduplicate (by name + type)
│  ├─ Compute unified edges (code calls + doc links + dependencies)
│  ├─ Output: wiki/vault/graph/nodes.jsonl + edges.jsonl
│  └─ Generate node-index.json
├─ Phase 5: Validate
│  ├─ Check schema compliance
│  ├─ Check node count > threshold
│  ├─ Check edges reference valid nodes
│  └─ Report validation results
└─ Phase 6: Finalize
   ├─ Write wiki/vault/graph/config.json
   ├─ Update refresh-log.md
   └─ Report completion
```

---

## Output

**Files Created/Updated:**
- wiki/vault/graph/nodes.jsonl (MERGED code + doc nodes)
- wiki/vault/graph/edges.jsonl (relationships)
- wiki/vault/graph/config.json (metadata)
- wiki/vault/graph/node-index.json (lookup table)
- wiki/vault/graph/GRAPH_REPORT.md (summary)
- wiki/vault/graph/refresh-log.md (history)

**Report:**
```
✓ Graph updated (incremental)
├─ Code pass: lat.md queried (12 recent symbols)
├─ Doc pass: 2 files changed, 8 nodes updated
├─ Merge: 53 total nodes, 67 edges
├─ Validation: ✓ passed
└─ Duration: 0.4 seconds
```

---

## Success Criteria

✅ Code pass queries lat.md for all symbols (or recent changes)  
✅ Doc pass exports Obsidian nodes  
✅ Merge combines into unified graph  
✅ lat.md optional file-watching enables near-real-time updates  
✅ Validation checks schema compliance  
✅ Graph is queryable (nodes.jsonl, edges.jsonl)  
✅ Query mode can answer "what calls this symbol?" via lat.md

---

## Implementation Checklist

- [ ] Implement Phase 1 (setup + lat.md availability check)
- [ ] Implement Phase 2 (code pass via lat.md MCP queries)
- [ ] Implement Phase 3 (doc pass via Obsidian export)
- [ ] Implement Phase 4 (merge + deduplication)
- [ ] Implement Phase 5 (validation)
- [ ] Implement Phase 6 (finalize + report)
- [ ] Add --full, --query modes
- [ ] Add error handling + recovery
- [ ] Add lat.md timeout handling (graceful fallback)

---

## References

**Related Specs:**
- [050-latmd-setup-and-integration.md](050-latmd-setup-and-integration.md) — lat.md MCP setup + tool contract
- [graph-storage-structure.md](graph-storage-structure.md) — Output formats
- [graph-refresh-strategy.md](graph-refresh-strategy.md) — Refresh strategy (lat.md auto-watches; /spek.map syncs on demand)
- [graph-merge-integration.md](graph-merge-integration.md) — Merge logic

**lat.md MCP Tool Contract:**
- `lat_symbols(file: str | None)` — Query all symbols (all if file=None, else filter by file)
- `lat_references(symbol: str)` — Get all references to symbol
- `lat_impact(symbol: str)` — Get transitive impact (affected symbols)
- `lat_definition(symbol: str)` — Get symbol definition details