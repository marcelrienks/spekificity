# ATOMIC SPECIFICATION: Graph Storage Structure (C5.2)

**Depends On:** node-schema-design.md  
**Used By:** /spek.map, /spek.context, all enrichment layers  

---

## Overview

Code graph stored in `vault/graph/` as SQLite database with optional export formats. `lat.md` maintains a queryable index via MCP tools and optional JSONL exports for integration with external systems.

---

## Directory Structure

```
vault/graph/
├── lat_index.db             # SQLite database (primary store — code + doc nodes + edges)
├── config.json              # Metadata (version, generation timestamp, stats)
├── cache/
│   ├── query-cache.db       # Query result cache (TTL-based)
│   └── sha256.json          # File hash cache for incremental updates
├── exports/                 # Optional JSONL exports (for integration)
│   ├── nodes.jsonl          # Exported nodes (for external tools)
│   ├── edges.jsonl          # Exported edges (for external tools)
│   └── timestamp.txt        # Export generation time
├── graph.html               # Interactive visualization
├── GRAPH_REPORT.md          # Human-readable analysis + metrics
└── refresh-log.md           # Refresh history + timestamps
```

**Primary Interface:** Agents interact with `lat.md` via the `lat` CLI and the optional MCP server (`lat mcp`). `lat.md` exposes exploration and reference commands (e.g. `lat section`, `lat refs`, `lat locate`, `lat search`) and can run an MCP server for editor/agent integration. The spec-level MCP tool names (for example `lat_symbols`, `lat_references`, `lat_impact`) are an adapter-facing contract that should be implemented by a thin adapter translating those calls into `lat` CLI invocations or MCP server calls.

_Note:_ `lat.md` manages its own internal index/store (implementation-specific). The spec's expectation of an on-disk SQLite index and JSONL exports is optional — prefer using `lat`'s native index and use `lat export` (or equivalent) to generate JSONL/SQLite exports when needed for downstream consumers.

**Export Format:** JSONL exports available in `vault/graph/exports/` for compatibility with external systems (updated on each `/spek.map` run).

---

## File Schemas

### config.json (lat.md Metadata)

Metadata file created by lat.md init:

```json
{
  "version": "1.0",
  "generated_at": "2026-05-19T14:00:00Z",
  "database": "lat_index.db",
  "database_format": "SQLite3",
  "graph_type": "hybrid",
  "sources": [
    {
      "type": "code",
      "tool": "lat.md",
      "languages": ["python", "typescript", "yaml", "markdown"],
      "file_count": 156,
      "indexed_symbols": 2847,
      "references": 12450
    },
    {
      "type": "documentation",
      "tool": "obsidian-export",
      "vault_path": "vault/",
      "file_count": 89,
      "doc_nodes": 145
    }
  ],
  "mcp_tools": [
    "adapter:lat_symbols -> lat section/lat locate",
    "adapter:lat_definition -> lat section/lat refs",
    "adapter:lat_references -> lat refs",
    "adapter:lat_callers -> derived via lat refs/graph traversal",
    "adapter:lat_callees -> derived via lat refs/graph traversal",
    "adapter:lat_impact -> derived (lat refs + traversal)",
    "adapter:lat_query -> lat search / lat mcp"
  ],
  "performance": {
    "cache_enabled": true,
    "cache_ttl": 3600,
    "last_full_rebuild": "2026-05-18T14:00:00Z",
    "last_incremental_sync": "2026-05-19T14:00:00Z",
    "last_full_rebuild_time_seconds": 47,
    "typical_query_time_ms": 150
  }
}
```

**Key:** Agents do **not** read JSONL files directly. Instead, they use the **MCP tools** listed above (lat_symbols, lat_references, etc.) to query the SQLite database.

### Node & Edge Storage (SQLite - Internal)

lat.md stores nodes and edges in `lat_index.db` (SQLite format). Agents interact with this database via MCP tool calls:

**Example MCP Tool Call (Agent → lat.md):**
```python
# Agent queries: "Find all methods in AuthService"
result = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")
# Returns: List of symbols (classes, methods, functions) in that file
```

**Response Format:**
```json
[
  {
    "name": "AuthService",
    "type": "class",
    "line": 12,
    "signature": "class AuthService"
  },
  {
    "name": "authenticate",
    "type": "method",
    "line": 25,
    "signature": "def authenticate(self, username: str, password: str) -> bool",
    "parent": "AuthService"
  }
]
```

### JSONL Exports (Optional - External Integration)

For integration with external systems, lat.md can export data to JSONL format (in `vault/graph/exports/`). This is optional and generated on-demand:

**nodes.jsonl (Example):**
```json
{"id":"python:src/services/auth.py:AuthService","type":"class","name":"AuthService","file":"src/services/auth.py","line":12}
{"id":"python:src/services/auth.py:AuthService:authenticate","type":"method","name":"authenticate","file":"src/services/auth.py","line":25,"parent":"AuthService"}
```

**edges.jsonl (Example):**
```json
{"from":"python:src/services/auth.py:AuthService:authenticate","to":"python:src/database/queries.py:query_user","relationship":"calls","context":"Line 45"}
```

**Use:** These exports are for integration with external analysis tools or custom workflows, not for agent queries.

### Query Cache (SQLite - Internal)

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

**Query via MCP Tools (Recommended):**

```python
# Find all symbols in module
symbols = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")

# Find all methods in class
methods = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")
# Filter result: [s for s in symbols if s["parent"] == "AuthService"]

# Find all callers
callers = call_mcp_tool("lat_callers", symbol="authenticate")
```

**Optional: JSONL Export Queries (External Tools)**

If using optional JSONL exports (wiki/vault/graph/exports/nodes.jsonl):

```bash
# Find all symbols in module (NOT RECOMMENDED - use MCP tools instead)
grep '"file": "src/services/auth.py"' wiki/vault/graph/exports/nodes.jsonl

# Find all methods in class (NOT RECOMMENDED - use MCP tools instead)
grep '"scope": "AuthService"' wiki/vault/graph/exports/nodes.jsonl

# Find all callers (NOT RECOMMENDED - use MCP tools instead)
grep '"to_node": "[target-id]"' wiki/vault/graph/exports/edges.jsonl
```

---

## Success Criteria

✅ Directory structure matches layout  
✅ All files in correct location  
✅ SQLite database is accessible and contains nodes
✅ MCP tools can query the database (<100ms per query)  
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
- [graph-setup Part 2](050-latmd-setup-and-integration.md#part-2-vault-structure-for-graphs)