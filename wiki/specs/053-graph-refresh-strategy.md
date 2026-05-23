---
title: "Graph Refresh Strategy (C5.4)"
status: "ATOMIC SPECIFICATION"
version: "1.0.0-alpha.1"
date: "2026-05-21"
---

# ATOMIC SPECIFICATION: Graph Refresh Strategy (C5.4)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Performance — Caching & Incremental Sync Strategy  
**Depends On:** graph-storage-structure.md, spek-map-command.md  
**Used By:** /spek.map  

---

## Overview

Graph refresh strategy uses SHA256 caching and incremental sync to keep the code graph fresh without expensive full rebuilds; incremental updates are significantly faster than full rebuilds.

---

## Caching Strategy

### SHA256 File Hashing

**Store in:** wiki/vault/graph/cache/sha256.json

```json
{
  "src/services/auth.py": "abc123def456...",
  "src/api/handlers.py": "ghi789jkl012...",
  "wiki/vault/patterns.md": "jkl012mno345..."
}
```

**Process:**
1. Before sync: compute SHA256 for each file
2. Compare with cached hash
3. If match: file unchanged, skip re-indexing
4. If mismatch: file changed, re-index
5. Update cache with new hash

**Cost:** minimal per file (negligible for typical files)

### Node Index Lookup Table

**Store in:** wiki/vault/graph/cache/node-index.json

```json
{
  "authenticate": "python:src/services/auth.py:AuthService:authenticate",
  "query_user": "python:src/database/queries.py:query_user"
}
```

**Use:** Quick symbol lookup without parsing entire nodes.jsonl

---

### Incremental Sync Strategy

### When to Sync (Triggers)

**Automatic:**
- `/spek.map` called without --full
- `--watch` mode detects file changes

**Manual:**
- User runs `/spek.map`

Note: Scheduling and frequency are project-configurable; teams should choose cadence that fits their workflow.

### How to Sync

```
1. Compute SHA256 for all files
2. Compare with cache/sha256.json
3. Identify changed files (list A)
4. Re-index changed files only
5. Update wiki/vault/graph/nodes.jsonl
6. Update edges (remove old, add new)
7. Update cache/sha256.json
8. Update node-index.json
```

### Incremental vs. Full

**Incremental:**
- Re-index only changed files
- Duration: significantly faster than a full rebuild
- Cost: lower

**Full:**
- Re-index entire codebase
- Duration: longer than incremental
- Cost: higher

**Decision:** Use incremental by default; full rebuilds are reserved for cache corruption, major changes, or explicit user request.

---

### Performance Optimization

### Parallel Processing

**Config:**
```yaml
lat:
  performance:
    parallel: true
    max_workers: <n>
```

**Process:** Index multiple files in parallel (configurable worker count)

**Benefit:** Faster sync on multi-core machines

### Cache Expiry

**Config:**
```yaml
lat:
  caching:
    cache_expiry: <duration>
```

**Process:**
- If cache older than configured expiry: force full rebuild
- Reason: file system cache might be stale

**Benefit:** Fresh cache, prevent stale nodes

### Debouncing (Watch Mode)

**Config:**
```yaml
lat:
  refresh:
    watch_debounce_ms: <ms>
```

**Process:**
- Multiple file changes within a short debounce window → batch into one sync

**Benefit:** Reduces unnecessary syncs

---

## Success Criteria

- ✅ Incremental sync detects changed files (SHA256 hashing works correctly)
- ✅ Cache validates correctly (no corruption, valid JSON)
- ✅ Expiry triggers rebuild when cache is stale (per project configuration)
- ✅ Parallel processing speeds up indexing when enabled and configured
- ✅ Debouncing prevents excessive syncs (batching short bursts of edits)
- ✅ Cache validation comprehensive (file exists, checksum valid, timestamp recent)

---
## Cache Validation

### Check 1: File Exists
```bash
ls -la wiki/vault/graph/cache/sha256.json
```
If missing: Initialize empty cache → full rebuild

### Check 2: Cache Age
```bash
find wiki/vault/graph/cache/sha256.json -mtime +1
```
If > 1 day old: Force full rebuild

### Check 3: Cache Integrity
```bash
jq . wiki/vault/graph/cache/sha256.json > /dev/null
```
If invalid JSON: Rebuild cache

### Check 4: Nodes Match
- Count nodes in cache vs. nodes.jsonl
- If mismatch: Corrupted, rebuild

---

## Refresh Triggers

### Automatic Refresh (Recommended)

**Timing:**
- `/spek.prepare` (Step 3-4): Check freshness + refresh if stale
- End of feature (`/spek.conclude` Step 8): Incremental sync
- Manual: `spek.map` command

**Frequency:**
- During feature: only if user requests (or if stale)
- End of feature: always incremental
- Between features: optional

### Manual Refresh

```bash
# Quick sync (if fresh)
/spek.map

# Force full rebuild
/spek.map --full

# Watch mode (continuous)
/spek.map --watch
```

---

## Cost Analysis

| Scenario | Duration | Cache Hit? | Tokens |
|----------|----------|-----------|--------|
| Full rebuild | 30-60s | No | 0 |
| Incremental (5/200 changed) | 2-5s | Yes | 0 |
| Cache miss | 30-60s | No | 0 |
| Watch mode (per change) | 1-2s | Yes | 0 |

**Token Cost:** none (pure local file I/O, no LLM calls)

---

## Success Criteria

✅ SHA256 cache substantially reduces sync time
✅ Incremental sync completes quickly
✅ Full rebuild only when necessary  
✅ Cache is validated on startup  
✅ Watch mode enables continuous updates  

---

## Implementation Checklist

- [ ] Implement SHA256 caching
- [ ] Implement incremental vs. full detection
- [ ] Implement cache validation
- [ ] Add cache expiry checking
- [ ] Implement parallel processing
- [ ] Implement debouncing (watch mode)
- [ ] Test incremental sync performance

---

## References

**Related Specs:**
 - [spek-map-command.md](spek-map-command.md) — /spek.map uses caching
 - [graph-storage-structure.md](graph-storage-structure.md) — Cache file location

**External:**
- [graph-setup Part 4](050-latmd-setup-and-integration.md#part-4-refresh-strategy)
