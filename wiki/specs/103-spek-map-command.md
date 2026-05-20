# ATOMIC SPECIFICATION: /spek.map Command (C5.3)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Skill — /spek.map (Code Graph Generation & Maintenance)  
**Depends On:** codegraph-setup-and-integration.md, graph-storage-structure.md  
**Used By:** /spek.prepare (Step 4), /spek.post (Step 8)  

---

## Overview

`/spek.map` queries and maintains the code graph through CodeGraph MCP (real-time indexed code analysis), Obsidian export (doc pass), and merge (unified graph). CodeGraph handles indexing automatically; `/spek.map` focuses on querying and keeping documentation in sync.

---

## Modes

### Mode 1: Full Refresh

```bash
/spek.map --full
```

**Process:**
1. Query CodeGraph for all symbols (fresh scan, no cache)
2. Doc pass: export Obsidian vault
3. Merge: combine code symbols + doc nodes into unified graph
4. Validate: check schema + node count
5. Write: wiki/vault/graph/nodes.jsonl + edges.jsonl + config.json

**Cost:** 1-3 seconds (CodeGraph queries are 20x faster than graphify)

**When to use:** After major refactoring, or to refresh cached snapshot

### Mode 2: Incremental Sync (Default)

```bash
/spek.map
```

**Process:**
1. Query CodeGraph for recently modified symbols (CodeGraph auto-watches files)
2. Doc pass: check Obsidian vault for new/changed files
3. Merge: update affected nodes + edges incrementally
4. Validate + write

**Cost:** < 500ms (CodeGraph handles file watching; /spek.map only merges + writes)

**When to use:** Normal workflow (after /spek.prepare, end of feature)

### Mode 3: Query-Only (No Sync)

```bash
/spek.map --query [symbol|file]
```

**Process:**
1. Query CodeGraph for specific symbol or file
2. Return results (no file writes)

**Cost:** < 100ms (CodeGraph MCP query)

**When to use:** During implementation when you need to explore code structure without updating graph

---

## Command Sequence

```
/spek.map [mode]
├─ Phase 1: Setup
│  ├─ Parse arguments
│  ├─ Validate config.yaml
│  ├─ Verify CodeGraph is available (MCP tool check)
│  └─ Create wiki/vault/graph/ if missing
├─ Phase 2: Code Pass (CodeGraph Query)
│  ├─ Call codegraph_symbols (all | recent-only, based on mode)
│  ├─ Call codegraph_references + codegraph_impact for each symbol
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
├─ Code pass: CodeGraph queried (12 recent symbols)
├─ Doc pass: 2 files changed, 8 nodes updated
├─ Merge: 53 total nodes, 67 edges
├─ Validation: ✓ passed
└─ Duration: 0.4 seconds
```

---

## Success Criteria

✅ Code pass queries CodeGraph for all symbols (or recent changes)  
✅ Doc pass exports Obsidian nodes  
✅ Merge combines into unified graph  
✅ CodeGraph file watching enables sub-second updates  
✅ Validation checks schema compliance  
✅ Graph is queryable (nodes.jsonl, edges.jsonl)  
✅ Query mode can answer "what calls this symbol?" via CodeGraph

---

## Implementation Checklist

- [ ] Implement Phase 1 (setup + CodeGraph availability check)
- [ ] Implement Phase 2 (code pass via CodeGraph MCP queries)
- [ ] Implement Phase 3 (doc pass via Obsidian export)
- [ ] Implement Phase 4 (merge + deduplication)
- [ ] Implement Phase 5 (validation)
- [ ] Implement Phase 6 (finalize + report)
- [ ] Add --full, --query modes
- [ ] Add error handling + recovery
- [ ] Add CodeGraph timeout handling (graceful fallback)

---

## References

**Related Specs:**
- [codegraph-setup-and-integration.md](codegraph-setup-and-integration.md) — CodeGraph MCP setup + tool contract
- [graph-storage-structure.md](graph-storage-structure.md) — Output formats
- [graph-refresh-strategy.md](graph-refresh-strategy.md) — Refresh strategy (CodeGraph auto-watches; /spek.map syncs on demand)
- [graph-merge-integration.md](graph-merge-integration.md) — Merge logic

**CodeGraph MCP Tool Contract:**
- `codegraph_symbols(file: str | None)` — Query all symbols (all if file=None, else filter by file)
- `codegraph_references(symbol: str)` — Get all references to symbol
- `codegraph_impact(symbol: str)` — Get transitive impact (affected symbols)
- `codegraph_definition(symbol: str)` — Get symbol definition details
