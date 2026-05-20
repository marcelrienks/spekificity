# ATOMIC SPECIFICATION: /spek.map Command (C5.3)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Skill — /spek.map (Code Graph Generation & Maintenance)  
**Depends On:** graphify-installation.md, graph-storage-structure.md  
**Used By:** /spek.prepare (Step 4), /spek.post (Step 8)  

---

## Overview

`/spek.map` generates and maintains the code graph through graphify (code pass), Obsidian export (doc pass), and merge (unified graph).

---

## Modes

### Mode 1: Full Rebuild (Expensive)

```bash
/spek.map --full
```

**Process:**
1. Disable cache (force re-index all files)
2. Code pass: graphify index all code
3. Doc pass: export Obsidian vault
4. Merge: combine into nodes.jsonl
5. Validate: check schema + node count
6. Write: vault/graph/config.json + nodes.jsonl + edges.jsonl

**Cost:** 30-60 seconds (depends on codebase size)

**When to use:** After major refactoring, or if cache corrupted

### Mode 2: Incremental Sync (Default)

```bash
/spek.map
```

**Process:**
1. Use cache (SHA256 hashes)
2. Identify changed files (git diff, file mtime)
3. Code pass: re-index only changed files
4. Doc pass: check Obsidian vault for new/changed files
5. Merge: update only affected nodes + edges
6. Validate + write

**Cost:** 2-5 seconds (much faster than full)

**When to use:** Normal workflow (after /spek.prepare, end of feature)

### Mode 3: Watch Mode (Interactive Dev)

```bash
/spek.map --watch
```

**Process:**
1. Starts file watcher
2. On file change: trigger incremental sync
3. Debounce: 1s (configurable)
4. Continuous updates to vault/graph/

**Cost:** Background process, 1-2s per file change

**When to use:** During active development (optional)

---

## Command Sequence

```
/spek.map [mode]
├─ Phase 1: Setup
│  ├─ Parse arguments
│  ├─ Validate config.yaml
│  └─ Create vault/graph/ if missing
├─ Phase 2: Code Pass (Graphify)
│  ├─ List all code files (Python, TypeScript, etc.)
│  ├─ For each file:
│  │  ├─ Check cache (SHA256 match?)
│  │  ├─ If no match: graphify index file
│  │  └─ If match: skip (cached)
│  ├─ Output: vault/graph/nodes-code.jsonl
│  └─ Update cache
├─ Phase 3: Doc Pass (Obsidian Export)
│  ├─ Export vault via cache.json or plugin
│  ├─ Output: vault/graph/nodes-docs.jsonl
│  └─ Update cache
├─ Phase 4: Merge
│  ├─ Read nodes-code.jsonl + nodes-docs.jsonl
│  ├─ Deduplicate (by name + type)
│  ├─ Compute edges (calls, inheritance, depends-on)
│  ├─ Output: vault/graph/nodes.jsonl + edges.jsonl
│  └─ Generate node-index.json
├─ Phase 5: Validate
│  ├─ Check schema compliance
│  ├─ Check node count > threshold
│  ├─ Check edges reference valid nodes
│  └─ Report validation results
└─ Phase 6: Finalize
   ├─ Write vault/graph/config.json
   ├─ Update refresh-log.md
   └─ Report completion
```

---

## Output

**Files Created/Updated:**
- vault/graph/nodes.jsonl (MERGED code + doc nodes)
- vault/graph/edges.jsonl (relationships)
- vault/graph/config.json (metadata)
- vault/graph/cache/sha256.json (for incremental)
- vault/graph/cache/node-index.json (lookup table)
- vault/graph/GRAPH_REPORT.md (summary)
- vault/graph/refresh-log.md (history)

**Report:**
```
✓ Graph updated (incremental)
├─ Code pass: 3 files changed, 45 nodes updated
├─ Doc pass: 2 files changed, 8 nodes updated
├─ Merge: 53 total nodes, 67 edges
├─ Cache: updated 5 file hashes
├─ Validation: ✓ passed
└─ Duration: 3.2 seconds
```

---

## Success Criteria

✅ Code pass indexes all relevant code  
✅ Doc pass exports Obsidian nodes  
✅ Merge combines into unified graph  
✅ Cache enables fast incremental updates  
✅ Validation checks schema compliance  
✅ Graph is queryable (nodes.jsonl, edges.jsonl)  

---

## Implementation Checklist

- [ ] Implement Phase 1 (setup)
- [ ] Implement Phase 2 (code pass via graphify)
- [ ] Implement Phase 3 (doc pass via Obsidian)
- [ ] Implement Phase 4 (merge + deduplication)
- [ ] Implement Phase 5 (validation)
- [ ] Implement Phase 6 (finalize + report)
- [ ] Add --full, --watch modes
- [ ] Add error handling + recovery

---

## References

**Related Specs:**
- [graphify-installation.md](graphify-installation.md) — Graphify setup
- [graph-storage-structure.md](graph-storage-structure.md) — Output formats
- [graph-refresh-strategy.md](graph-refresh-strategy.md) — Cache strategy
- [graph-merge-integration.md](graph-merge-integration.md) — Merge logic

**External:**
- [graph-setup Part 3](codegraph-setup-and-integration.md#part-3-skill-invocation-contract--spekmap)
