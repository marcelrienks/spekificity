# Spec: Code and Document Maps (extracted spec)

## Overview

**Problem:** The vault graph currently targets source code only. Documentation (specs, plans, skills, architectural decisions) exists in Obsidian vault outside the queryable graph, so AI-assisted steps (specify, plan, implement) cannot easily discover what documentation already exists. This leads to duplicated specs, contradictory plans, and missed opportunities to reuse patterns.

**Solution:** Unify code and documentation graphs by querying Obsidian's built-in graph API for documentation nodes and integrating them with code nodes from lat.md.

**Outcome:** A single `/spek.map` command that indexes both code (via lat.md) and documentation (via Obsidian graph export), enabling context-aware specification, planning, and implementation.

---

## Design Questions and Decisions

### Question 1: What is a "node" for documentation?

**Options:**

1. **File-level nodes** — One node per markdown file (e.g., `wiki/vault/decision.md` → one node)
2. **Heading-level nodes** — One node per heading (e.g., `wiki/vault/decision.md#heading-1`, `wiki/vault/decision.md#heading-2`)
3. **Link-graph topology** — Nodes based on markdown link structure (e.g., decision nodes linked to affected specs)
4. **Hybrid** — Different granularity for different document types (file-level for specs, heading-level for decisions)

**Decision: Hybrid (heading-level for content-rich docs, file-level for configs)**

**Rationale:**
- **Specs and decisions:** Heading-level enables querying specific architectural decisions or spec sections without re-reading entire files
- **Plans and tasks:** Heading-level enables step-by-step task lookup
- **Skills and configurations:** File-level is sufficient (usually short, single-purpose files)
- **Skills list:** File-level (already referenced by name in invocations)

**Node schema example:**

```
Code node: {
  type: "code",
  id: "src/prepare/prepare.ts:Prepare",
  file: "src/prepare/prepare.ts",
  symbol: "Prepare",
  symbolType: "class",
  description: "...",
  lineRange: [10, 50],
  imports: ["@module/foo", "@module/bar"],
  exports: ["Prepare"]
}

Documentation node (file-level): {
  type: "doc",
  id: "wiki/vault/decision.md",
  file: "wiki/vault/decision.md",
  title: "Decision Index",
  level: "file",
  description: "...",
  tags: ["architectural", "decisions"],
  references: []
}

Documentation node (heading-level): {
  type: "doc",
  id: "wiki/vault/decision.md#api-versioning-strategy",
  file: "wiki/vault/decision.md",
  heading: "API Versioning Strategy",
  level: "h2",
  description: "...",
  tags: ["api", "versioning"],
  references: ["wiki/vault/decision.md"]
}

Skill node (file-level): {
  type: "skill",
  id: "skills/spek-prepare/SKILL.md",
  file: "skills/spek-prepare/SKILL.md",
  command: "spek.prepare",
  purpose: "Prime agent and environment for feature work",
  description: "...",
  tags: ["workflow", "setup"],
  references: []
}
```

**Storage:** Primary storage in the lat.md SQLite index (`.spek/lat_index.db`); optional JSONL export in `wiki/vault/graph/exports/nodes.jsonl` for compatibility with external tools

---

## Success Criteria

- ✅ Unified graph combines code + documentation nodes (hybrid graph functional)
- ✅ Hybrid granularity applied (heading-level for specs/decisions, file-level for configs)
- ✅ Cross-references computed (code ↔ doc bidirectional links working)
- ✅ Query interface unified (`/spek.map` command single entry point)
- ✅ Agent can discover documentation (no manual re-reading of full files)
- ✅ Context-aware spec/plan/implementation enabled (decisions + patterns injected)
- ✅ Duplicate detection prevents confusion (same concept not indexed twice)

---

### Question 2: How should documentation be parsed?

**Options:**

1. **Custom markdown parser** — Write code to extract headings, frontmatter, and link structure from markdown files
2. **Obsidian's built-in graph** — Query Obsidian's graph API or export feature to get links, backlinks, and structure
3. **Obsidian CLI (obsidian command)** — Use the Obsidian CLI (bundled `obsidian` command) or plugin-based exports to export the vault graph
4. **Hybrid** — Obsidian for storage + structure, custom parser for agent queries

**Decision: Use Obsidian's graph export directly**

**Rationale:**
- Obsidian already maintains the graph (links, backlinks, metadata) — don't duplicate work
- Obsidian vault is the authoritative source for documentation
- Export Obsidian's graph to a queryable format (JSONL or metadata cache)
- Obsidian CLI or graph export feature can generate nodes with heading structure, links, frontmatter metadata
- Single source of truth: documents live in Obsidian; graph is derived from Obsidian

**Implementation pattern:**

```bash
# In spek.map workflow:
spek.map step 1: lat.md index-code → SQLite (.spek/lat_index.db)
spek.map step 2: obsidian export-graph (via CLI or plugin) → wiki/vault/graph/nodes-docs.jsonl (temporary)
spek.map step 3: merge both → SQLite (permanent storage) + optional JSONL export (wiki/vault/graph/exports/nodes.jsonl)

# Result: All data stored in lat.md SQLite index
# JSONL files are intermediate format during merge; optional exports for external tools
```

(Obsidian can export via CLI, plugin API, or metadata.json cache depending on setup)

---

### Question 3: Which files/folders should be indexed?

**For Code:**
- `src/` — All user-written source code
- `.github/agents/skills/` — All skill definitions
- `.spek/` — Platform code and scripts

**For Documentation:**
- `specs/` — Feature specifications (heading-level)
- `vault/decision.md` — Architectural decisions (heading-level)
- `vault/intention.md` — Intention statements (file-level)
- `vault/patterns.md` — Patterns library (heading-level)
- `vault/lessons/` — Lessons learned (file-level, one per feature)
- `wiki/` — General wiki/reference docs (heading-level by default, can override with frontmatter)
- `.github/agents/skills/*/SKILL.md` — Skill definitions (file-level)

**Exclude:**
- `node_modules/`, `dist/`, `.git/`, `wiki/vault/graph/` — Build/generated/index files
- `.env`, `*.log`, `*.tmp` — Temporary/config files
- `wiki/raw/` — Raw research materials (not part of canonical docs)

---

### Question 4: What metadata should each doc node capture?

**Frontmatter Format (optional, at top of markdown):**

```yaml
---
tags: [tag1, tag2, ...]
affects: [affected-feature, ...]
---

# Heading

Content here.
```

**Parser should extract:**
- File type (decision, spec, skill, etc.)
- Title/heading
- Description (first paragraph or summary)
- Tags (from frontmatter + implicit tags from folder structure)
- References (links to other docs and code)
- Status (active, archived, draft from frontmatter or inferred)
- Version (for tracking changes)
- Relationships (which features/decisions this doc affects)

---

### Question 5: How are references/links discovered?

**Code references:**
- lat.md's AST analysis: `import Foo from "path/to/foo"` → code node link
- Cross-file function calls: `foo()` → link to `Foo` definition

**Doc references:**
- Markdown links: `[text](wiki/vault/decision.md#heading)` → doc node link
- Implicit tags: Mention of `spek.prepare` in a spec → implicit link to skill node
- Heading anchors: `# API Versioning Strategy` → node id = `#api-versioning-strategy`

**Link storage:**
```json
{
  "id": "node-id",
  "references": [
    "wiki/vault/decision.md",
    "src/prepare/prepare.ts:Prepare",
    "skills/spek-prepare/SKILL.md"
  ]
}
```

---

## Node Schema (Final)

### Code Nodes (from lat.md)

```typescript
interface CodeNode {
  type: "code";
  id: string; // e.g., "src/prepare/prepare.ts:Prepare"
  file: string; // relative path
  symbol: string; // function/class/variable name
  symbolType: "function" | "class" | "interface" | "type" | "variable" | "const";
  description: string; // JSDoc or comment
  lineRange: [start: number, end: number];
  imports: string[]; // module imports
  exports: string[]; // exported symbols
  tags: string[]; // implicit: ["code", "source"]
  references: string[]; // code nodes this references
  referencedBy: string[]; // code nodes that reference this (computed during merge)
}
```

### Documentation Nodes (heading-level)

```typescript
interface DocNodeHeading {
  type: "doc";
  id: string; // e.g., "wiki/vault/decision.md#api-versioning-strategy"
  file: string; // relative path
  heading: string; // "API Versioning Strategy"
  level: 1 | 2 | 3 | 4 | 5 | 6; // h1, h2, ... h6
  description: string; // first paragraph or custom summary
  status: "active" | "archived" | "draft"; // from frontmatter or inferred
  version: string; // from frontmatter or "1.0"
  tags: string[]; // from frontmatter + implicit from folder
  docType: "decision" | "spec" | "skill" | "pattern" | "lesson" | "guide"; // from frontmatter or inferred
  references: string[]; // other docs or code this references
  referencedBy: string[]; // docs that reference this
  parent: string | null; // parent heading id if nested
  children: string[]; // child heading ids
}
```

### Documentation Nodes (file-level)

```typescript
interface DocNodeFile {
  type: "doc";
  id: string; // e.g., "vault/intention.md" or "skills/spek-prepare/SKILL.md"
  file: string; // relative path
  title: string; // first h1 or filename
  level: "file";
  description: string; // summary
  status: "active" | "archived" | "draft";
  version: string;
  tags: string[];
  docType: "decision" | "spec" | "skill" | "pattern" | "lesson" | "guide";
  references: string[];
  referencedBy: string[];
  parent: null;
  children: null; // file-level nodes don't have children in the graph
}
```

---

## Vault Graph Structure

**Directory structure:**

```
vault/graph/
├── lat_index.db         # PRIMARY: SQLite database with all code + doc nodes (lat.md index)
├── cache/               # Query cache (TTL-based, auto-expiring)
├── config.json          # lat.md configuration metadata
├── exports/             # OPTIONAL: JSONL exports for external tools
│   ├── nodes.jsonl      # All nodes (code + doc) in JSONL format
│   ├── nodes-code.jsonl # Code nodes only
│   └── nodes-docs.jsonl # Doc nodes only
└── metadata.json        # Timestamp, versions, source file hashes
```

**Primary Storage:** SQLite database (`.spek/lat_index.db`)
- Contains all code nodes (indexed via lat.md)
- Contains all doc nodes (merged from Obsidian export)
- Maintained via MCP tools (lat_symbols, lat_references, lat_callers, lat_callees, lat_impact, lat_definition, lat_query)
  - Queried via lat.md MCP tools (no token cost)

**Optional Exports:** JSONL files in `exports/` subdirectory
- Generated on-demand for external tool compatibility
- Not meant for direct agent queries (use MCP tools instead)
-- Can be regenerated from SQLite via `lat export` command

**Obsidian export format to use:**
- Obsidian's `dataview` plugin export (most structured)
- Or Obsidian's native `.obsidian/cache.json` (metadata cache)
- Or custom Obsidian CLI tool that exports graph as JSONL

**nodes.jsonl format (one line per node, OPTIONAL export):**

```jsonl
{"type":"code","id":"src/prepare/prepare.ts:Prepare",...}
{"type":"doc","id":"wiki/vault/decision.md#api-versioning-strategy",...}
{"type":"doc","id":"skills/spek-prepare/SKILL.md",...}
```

**Query examples (via MCP tools):**

```python
# Find all decisions (from lat.md hybrid index)
decisions = call_mcp_tool("lat_query", query="find all nodes with type=doc and docType=decision")

# Find all code that references wiki/vault/decision.md
refs = call_mcp_tool("lat_references", symbol="decision.md#api-versioning-strategy")

# Find all active docs (via query on metadata)
active_docs = call_mcp_tool("lat_query", query="find all nodes with status=active and type=doc")
```

---

## Configuration (config.json)

```json
{
  "version": "1.0",
  "graphVersion": "latmd-0.1",
  "parser": {obsidian-export"
  },
  "obsidian": {
    "vaultPath": "vault/",
    "exportMethod": "dataview-plugin | obsidian-cache | cli-tool",
    "includeMetadata": true,
    "includeFrontmatter": true,
    "includeBacklinks": true
  },
  "indexing": {
  "codePaths": ["src/", ".github/agents/skills/", ".spek/"],
    "docPaths": ["specs/", "vault/decision.md", "vault/intention.md", "vault/patterns.md", "vault/lessons/", "wiki/", ".github/agents/skills/*/SKILL.md"],
    "exclude": [
      "node_modules/",
      "dist/",
      ".git/",
      "wiki/vault/graph/",
      "wiki/raw/",
      ".obsidian/",
      "**/*.log",
      "**/*.tmp"
    ]
  },
  "docTypes": {
    "decision": { "folder": "vault/", "file": "decision.md", "granularity": "heading", "source": "obsidian" },
    "spec": { "folder": "specs/", "file": "*.md", "granularity": "heading", "source": "obsidian" },
    "skill": { "folder": ".github/agents/skills/", "file": "SKILL.md", "granularity": "file", "source": "obsidian" },
    "pattern": { "folder": "vault/", "file": "patterns.md", "granularity": "heading", "source": "obsidian" },
    "lesson": { "folder": "wiki/vault/lessons/", "file": "*.md", "granularity": "file", "source": "obsidian" },
    "guide": { "folder": "wiki/", "file": "*.md", "granularity": "heading", "source": "obsidian" }
  },
  "frontmatter": {
    "enabled": true,
    "required": [],
    "optional": ["type", "tags", "affects", "status", "version"]
  },
  "refreshPolicy": {
    "fullRefresh": "on-demand or after-obsidian-rebuild",
    "incrementalRefresh": "after-feature (spek.conclude)",
    "obsidianCacheMonitor": "watch .obsidian/cache.json for
    "incrementalRefresh": "after-feature (spek.conclude)",
    "cacheInvalidation": "when source file hash changes"
  }
}
```

---
Export Obsidian graph (via dataview, cache, or CLI tool) → wiki/vault/graph/nodes-docs.jsonl
   - Extract heading structure from Obsidian's link graph and frontmatter
   - Convert Obsidian links to node references
4. Merge both into wiki/vault/graph/nodes.jsonl (deduplicate, compute backreferences)
5. Update wiki/vault/graph/metadata.json (timestamp, Obsidian version, file hashes)
6. Report: "Graph indexed: X code nodes, Y doc nodes (from Obsidian)

```
1. Load config from wiki/vault/graph/config.json
2. Run lat.md indexer on code paths → wiki/vault/graph/nodes-code.jsonl
3. Run spek-doc-parser on doc paths → wiki/vault/graph/nodes-docs.jsonl
4. Merge both into wiki/vault/graph/nodes.jsonl (deduplicate, compute backreferences)
5. Update wiki/vault/graph/metadata.json (timestamp, file hashes, version)
6. Report: "Graph indexed: X code nodes, Y doc nodes"
```

### Input/Output Contract

**Input:**
-- Source code files (all languages supported by lat.md indexer)
- Documentation files (markdown, YAML frontmatter optional)
- Config file (wiki/vault/graph/config.json)

**Output:**
- `wiki/vault/graph/nodes.jsonl` — Queryable index
- `wiki/vault/graph/metadata.json` — Timestamp, source hashes, version info
- Console output — Summary of indexing

**Exit codes:**
- `0` — Success
- `1` — Configuration error
- `2` — Source file parse error
- `3` — I/O error (permission denied, disk full)

---

## Integration with Skills

### In `/spek.prepare`

```
Step 4: Verify code analysis tool is fresh

- If first run: `/spek.map` (full index)
- Else: Check if source files have changed since last map
  - If changed: `/spek.map` (full index, conservative)
  - Else: Skip (graph already current)
```

### In `/spek.conclude`

```
Step 5: Run code analysis tool in incremental mode

- `/spek.map` (incremental: only re-index files that changed during feature)
- Update wiki/vault/graph/metadata.json with new timestamp
```

### In `/spek.context`

```
When loading vault context:
- Read wiki/vault/graph/nodes.jsonl
- Query for skill nodes → pass to user fo sourced from Obsidian export
- File-level parsing for skills and configurations
- Link discovery from Obsidian's built-in graph structure and markdown `[text](url)` syntax
- Static storage (JSONL, derived from Obsidian vault)

**Phase 2 (future):**
- Real-time sync from Obsidian (file watcher on .obsidian/cache.json)
- Semantic search across nodes (embedding-based on Obsidian content)
- Interactive graph CLI tool (query Obsidian-sourced nodes)
- Relationship visualization (which decisions affect which specs)

**Out of scope:**
- Bidirectional sync (don't write back to Obsidian vault from graph)
- Non-Obsidian documentation sources (different vault systems)
- Video or image indexing — stick to text
- Non-markdown formats (HTML, Asciidoc) — Obsidian is markdown-first
- Full-text search — query by node ID, tags, or reference
- Incremental graph updates (file watcher, not full re-index on each call)
- Semantic search across nodes (embedding-based)
- Interactive graph queries (CLI tool to search nodes)
- Relationship visualization (which decisions affect which specs)

**Out of scope:**
- Real-time graph updates (by-file as you edit) — too expensive
- Video or image indexing — stick to text
- Non-markdown formats (HTML, Asciidoc) — can add later
- Full-text search — query by node ID or tags for now

---

## Success Criteria

- [x] Node schema is defined for both code and doc nodes
- [x] Hybrid granularity approach chosen (heading-level for content, file-level for config)
- [x] Separate parsing passes defined (lat.md for code, custom for docs)
- [x]Choose Obsidian export method** — Dataview plugin, native cache.json, or custom CLI tool
2. **Implement Obsidian export integration** — Script or plugin that exports Obsidian graph to JSONL format
3. **Update `/spek.map` skill** — Integrate lat.md + Obsidian export into unified command
4. **Create config.json template** — Place in `.spek/config/graph-config.json`
5. **Integrate with `/spek.prepare` and `/spek.conclude`** — Add graph refresh steps (watch Obsidian cache for changes)
6. **Document query patterns** — Create a guide for agents on how to query the merged graph

---

## References

- **Decision:** Use Obsidian's graph export as authoritative source for doc nodes; merge with lat.md code nodes
- **Node schema:** Unified structure for code and doc nodes with references; docs sourced from Obsidian
- **Storage:** JSONL in `wiki/vault/graph/nodes.jsonl` derived from Obsidian vault + lat.md code output
- **Integration:** `/spek.map`, `/spek.prepare`, `/spek.conclude`, `/spek.context`
- **Config:** `wiki/vault/graph/config.json` specifies Obsidian export method, indexing rules, refresh policy
- **Authority:** Obsidian vault is single source of truth for documentation; graph is derived
5. **Document query patterns** — Create a guide for agents on how to query the graph

---

## References

- **Decision:** Heading-level for docs with variable granularity; separate parsing passes
- **Node schema:** Unified structure for code and doc nodes with references
- **Storage:** JSONL in `wiki/vault/graph/nodes.jsonl` for simplicity and streaming
- **Integration:** `/spek.map`, `/spek.prepare`, `/spek.conclude`, `/spek.context`
- **Config:** `wiki/vault/graph/config.json` defines indexing rules and refresh policy