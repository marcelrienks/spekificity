# ATOMIC SPECIFICATION: Graph Storage Structure (C5.2)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Data Schema — Code Graph Directory & File Formats  
**Depends On:** node-schema-design.md  
**Used By:** /spek.map, /spek.context, all enrichment layers  

---

## Overview

Code graph stored in `vault/graph/` with nodes.jsonl (JSONL), edges.jsonl, config.json, and cache files. This spec defines directory layout and file schemas.

---

## Directory Structure

```
vault/graph/
├── config.json              # Metadata (version, generation timestamp, stats)
├── nodes.jsonl              # MERGED nodes (code + doc) — agent queryable
├── nodes-code.jsonl         # Code symbols from graphify
├── nodes-docs.jsonl         # Document nodes from Obsidian
├── edges.jsonl              # Relationships (calls, inheritance, depends-on)
├── cache/
│   ├── sha256.json          # File hash cache for incremental updates
│   └── node-index.json      # Symbol → node ID lookup table
├── nodes/                   # Obsidian notes (optional output)
│   ├── functions/
│   ├── classes/
│   └── modules/
├── graph.html               # Interactive visualization
├── GRAPH_REPORT.md          # Human-readable analysis + metrics
└── refresh-log.md           # Refresh history + timestamps
```

---

## File Schemas

### config.json

```json
{
  "version": "1.0",
  "generated_at": "2026-05-19T14:00:00Z",
  "graph_type": "hybrid",
  "sources": [
    {
      "type": "code",
      "tool": "graphify",
      "languages": ["python", "typescript"],
      "file_count": 156,
      "node_count": 423
    },
    {
      "type": "documentation",
      "tool": "obsidian-export",
      "file_count": 89,
      "node_count": 45
    }
  ],
  "performance": {
    "cache_enabled": true,
    "last_full_rebuild": "2026-05-18T14:00:00Z",
    "last_incremental_sync": "2026-05-19T14:00:00Z"
  }
}
```

### nodes.jsonl (Agent-Queryable)

One JSON per line:

```json
{
  "id": "python:src/services/auth.py:AuthService:authenticate",
  "type": "method",
  "name": "authenticate",
  "language": "python",
  "file": "src/services/auth.py",
  "line_start": 42,
  "scope": "AuthService",
  "signature": "def authenticate(self, username: str, password: str) -> bool",
  "complexity": "medium",
  "source": "code",
  "indexed_at": "2026-05-19T14:00:00Z"
}
```

### edges.jsonl

```json
{
  "id": "edge:auth_authenticate->database_query_user",
  "from_node": "python:src/services/auth.py:AuthService:authenticate",
  "to_node": "python:src/database/queries.py:query_user",
  "relationship": "calls",
  "context": "Line 45: user = query_user(username)"
}
```

### sha256.json (Cache)

```json
{
  "src/services/auth.py": "abc123def456...",
  "src/api/handlers.py": "ghi789jkl012...",
  "...": "..."
}
```

### node-index.json (Lookup)

```json
{
  "authenticate": "python:src/services/auth.py:AuthService:authenticate",
  "query_user": "python:src/database/queries.py:query_user",
  "...": "..."
}
```

## Success Criteria

- ✅ Directory structure matches spec layout (all folders + files present)
- ✅ All files in correct location (nodes.jsonl, edges.jsonl, cache/ at right paths)
- ✅ nodes.jsonl is valid JSONL (one JSON per line, no parsing errors)
- ✅ edges.jsonl is valid JSONL (relationship entries complete)
- ✅ config.json is valid JSON (version, sources, performance metadata present)
- ✅ Cache files exist and valid (sha256.json, node-index.json readable)
- ✅ Storage handles large graphs (100K+ symbols supported)

---

## Query Patterns

**Find all nodes in module:**
```bash
grep '"file": "src/services/auth.py"' vault/graph/nodes.jsonl
```

**Find all methods in class:**
```bash
grep '"scope": "AuthService"' vault/graph/nodes.jsonl
```

**Find all callers:**
```bash
grep '"to_node": "[target-id]"' vault/graph/edges.jsonl
```

---

## Success Criteria

✅ Directory structure matches layout  
✅ All files in correct location  
✅ nodes.jsonl is valid JSONL (one JSON per line)  
✅ edges.jsonl is valid JSONL  
✅ config.json is valid JSON  
✅ Cache files exist and are valid JSON  

---

## Implementation Checklist

- [ ] Create vault/graph/ directory
- [ ] Create subdirectories (cache/, nodes/)
- [ ] Validate nodes.jsonl format
- [ ] Validate edges.jsonl format
- [ ] Generate config.json
- [ ] Implement cache file updates
- [ ] Test query patterns

---

## References

**Related Specs:**
- [node-schema-design.md](node-schema-design.md) — Node schema details
- [spek-map-command.md](spek-map-command.md) — /spek.map generates these
- [graph-refresh-strategy.md](graph-refresh-strategy.md) — Cache strategy

**External:**
- [graph-setup Part 2](codegraph-setup-and-integration.md#part-2-vault-structure-for-graphs)
