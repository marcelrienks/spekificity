# /spek.map

Query lat.md and vault to map code dependencies for a spec topic.

## Steps

1. Query lat.md MCP for code references to the spec topic: symbols, callers, definitions, and call graphs.
2. Query `.spek/vault/` for related decisions and dependent specs that touch the same topic.
3. Generate dependency graph: list files, symbols, and specs related to the topic.
4. Highlight blockers (items that must change before this topic can be modified) and critical paths.
