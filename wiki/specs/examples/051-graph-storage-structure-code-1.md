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
