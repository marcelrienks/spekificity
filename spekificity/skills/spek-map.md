# /spek.map

Query lat.md and vault to map code dependencies for a spec topic.

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded)
- Topic or feature area to map provided

## Steps

1. Query lat.md MCP for code references to the spec topic: symbols, callers, definitions, and call graphs.
2. Query `.spek/vault/` for related decisions and dependent specs that touch the same topic.
3. Generate dependency graph: list files, symbols, and specs related to the topic.
4. Highlight blockers (items that must change before this topic can be modified) and critical paths.

## Output

- Dependency graph: files, symbols, and specs related to the topic
- Blockers list: items that must change first
- Critical paths: sequence of changes required

## Exit Criteria

- lat.md queried for all references to the topic
- Vault queried for related decisions and specs
- Dependency graph generated with blockers and critical paths identified
