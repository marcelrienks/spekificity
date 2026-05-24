# Spec: Obsidian Graph Export Protocol


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Concern:** How to extract documentation nodes from Obsidian vault for graph indexing  
**Extracted from:** extracted spec Question 2  
**Depends on:** node-schema-design  
**Used by:** /spek.map, extracted spec graph merge step  

---


## Overview

**Problem:** Documentation exists in Obsidian vault but is not queryable for agent-assisted spec/plan generation. Need a reliable way to extract doc graph structure (headings, links, metadata) and convert to nodes.jsonl format.

**Solution:** Use Obsidian's built-in export capabilities (dataview plugin, cache.json, or CLI tool) to export vault graph to structured JSONL format that can be merged with code nodes.

**Outcome:** Documentation becomes queryable via vault/graph/nodes-docs.jsonl, enabling agent to discover existing decisions, patterns, and lessons without re-reading all markdown files.

---


## Success Criteria

- [x] Export method chosen and documented (cache.json recommended)
- [x] Conversion script converts cache.json → nodes-docs.jsonl format
- [x] Heading-to-ID conversion handles special characters
- [x] Link discovery extracts all markdown link types
- [x] Backreferences computed and stored
- [x] Configuration templated for different export methods
- [x] Integration with `/spek.map` Step 2 documented
- ## Implementation Checklist
- [ ] Create `obsidian-export.py` script in `.spek/bin/`
- [ ] Test export on real vault (validate cache.json parsing)
- [ ] Verify nodes-docs.jsonl format matches schema (node-schema-design)
- [ ] Add config template to `vault/graph/config.json`
- [ ] Document export troubleshooting in guide
- [ ] Test link discovery (verify backreferences computed correctly)
- ## References
- **Obsidian cache format:** [Obsidian Plugin Development Docs](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata)
- **Cache monitoring:** Watch `.obsidian/cache.json` for real-time vault changes
- **Dataview plugin:** [Obsidian Dataview](https://github.com/blacksmithgu/obsidian-dataview)
- **Related specs:** node-schema-design, spek-map-command


## Obsidian Export Methods (Priority Order)


## Method 1: Dataview Plugin Export (Recommended)

**What it is:**
- Obsidian's Dataview plugin can export query results to structured format
- Supports fetching links, backlinks, frontmatter metadata, file properties

**Setup:**
1. Install Obsidian Dataview plugin (community plugin)
2. Create a dataview query in vault (e.g., `wiki/queries/export-graph.md`)
3. Export query result to JSON/JSONL

**Query Example:**
```
TABLE
  file.name as Name,
  file.frontmatter.type as Type,
  file.frontmatter.tags as Tags,
  file.frontmatter.status as Status,
  length(file.links) as LinkCount
FROM ""
```

**Pros:**
- Highly structured, predictable output
- Can query specific frontmatter fields
- Obsidian-native, no external tools needed
- Supports filtering (e.g., only active decisions)

**Cons:**
- Requires Dataview plugin installation
- Output format needs post-processing to JSONL

**Best for:**
- Projects with rich frontmatter (status, tags, affects, version fields)
- Querying specific doc subsets (only active decisions, recent lessons)

---


## Method 2: Obsidian Native Cache (cache.json)

**What it is:**
- Obsidian stores metadata in `.obsidian/cache.json` 
- Contains file structure, frontmatter, links, backlinks
- No plugin needed; always available

**Setup:**
1. Read `.obsidian/cache.json` directly
2. Parse metadata for each file
3. Extract link graph, frontmatter, heading structure

**Format (cache.json structure):**
```json
{
  "files": {
    "vault/decision.md": {
      "mtime": 1716024000000,
      "size": 5234,
      "hash": "a1b2c3d4",
      "frontmatter": {
        "type": "decision",
        "tags": ["architectural", "api"],
        "status": "active",
        "version": "1.0"
      },
      "links": [
        { "original": "vault/patterns.md#caching", "link": "vault/patterns.md", "displayText": "Caching Pattern" }
      ],
      "headings": [
        { "heading": "API Versioning Strategy", "level": 2, "position": { "start": { "line": 5, "col": 0 }, "end": { "line": 5, "col": 30 } } }
      ]
    }
  }
}
```

**Pros:**
- No plugin required
- Always available (Obsidian maintains automatically)
- Comprehensive (links, backlinks, headings, frontmatter)
- Real-time (updated as vault changes)

**Cons:**
- Requires parsing JSON with embedded metadata
- Heading positions need to be converted to readable anchors
- Cache.json format may change in future Obsidian versions

**Best for:**
- Projects that want zero additional setup
- Real-time graph updates (monitor cache.json for changes)

---


## Obsidian CLI (Recommended)

**What it is:**
- The Obsidian CLI is the `obsidian` command bundled with the Obsidian desktop app. It provides programmatic access to a running Obsidian instance and can be used to script exports, run JS in-app, and invoke plugin commands when the app is running.
- Spekificity recommends using the Obsidian CLI for automated vault operations where available; alternative export methods (Dataview plugin, `.obsidian/cache.json`, or plugin-based exporters) are supported as fallbacks.

**Setup / How to use:**
- Enable the CLI in Obsidian: Settings → General → Command line interface, then follow the on-screen prompt to register the `obsidian` command in your PATH. The Obsidian app must be running for many CLI commands to work. For CI/headless options, see: https://obsidian.md/help/headless
- Example: run a small JS snippet inside the running Obsidian app to inspect files (returns JSON):

```bash
# list file paths (example; Obsidian must be running)
obsidian eval code="JSON.stringify(app.vault.getFiles().map(f=>f.path))"
```

- For structured exports you can use one of these approaches:
  - Dataview plugin queries (export query results to JSON/JSONL)
  - Read and parse `.obsidian/cache.json` for an authoritative metadata snapshot
  - Use `obsidian eval` or plugin commands to produce a JSON export (exact command depends on CLI version and installed plugins)

**Pros:**
- First-class automation path when Obsidian app + CLI are available
- Allows running developer/plugin commands and JS in-app for flexible exports

**Cons:**
- Requires the Obsidian desktop app and CLI registration (bundled; not an npm package)
- Some export workflows require plugins (Dataview) or custom JS snippets

**Best for:**
- Projects that want scripted, repeatable exports from the canonical vault. If CLI is unavailable in CI, prefer cache.json or plugin exports.

---


## Export to JSONL Conversion


## Input: Obsidian cache.json

```json
{
  "files": {
    "vault/decision.md": {
      "frontmatter": {
        "type": "decision",
        "tags": ["api", "versioning"],
        "status": "active"
      },
      "headings": [
        { "heading": "API Versioning Strategy", "level": 2, "position": {...} }
      ],
      "links": [...]
    }
  }
}
```


## Output: nodes-docs.jsonl (one line per heading)

```jsonl
{"type":"doc","id":"vault/decision.md#api-versioning-strategy","file":"vault/decision.md","heading":"API Versioning Strategy","level":2,"docType":"decision","tags":["api","versioning"],"status":"active","description":"Rationale for versioning strategy...","references":[],"referencedBy":[]}
{"type":"doc","id":"vault/decision.md","file":"vault/decision.md","title":"Decision Index","level":"file","docType":"decision","tags":["decision"],"status":"active","description":"Index of all architectural decisions","references":[],"referencedBy":[]}
```


## Conversion Process


> Example moved to [Example: 061-obsidian-graph-export-code-1.md](./examples/061-obsidian-graph-export-code-1.md)


---


## Link Discovery & Reference Extraction


## Markdown Link Parsing

**Pattern:** `[text](vault/decision.md#api-versioning)`

```bash
# Extract all markdown links from a file
grep -o '\[[^\]]*\]([^)]*)\|{{\s*\[\[' vault/decision.md | sed 's/^.*\[\[\|.*\[\([^]]*\).*/\1/g'
```

**Link types to handle:**
1. `[text](vault/decision.md)` → link to file
2. `[text](vault/decision.md#heading)` → link to heading
3. `[[vault/decision.md]]` — Obsidian wiki-link syntax (also in cache.json)
4. `![[image.png]]` — embedded links (skip images)


## Reference Computation

After exporting all nodes, compute backreferences:

```bash
# For each node, find all nodes that reference it
for each node_id in nodes-docs.jsonl:
    find_references = grep node_id nodes-docs.jsonl | extract "references" field
    update node["referencedBy"] = find_references
```

---


## Configuration (vault/graph/config.json)

```json
{
  "version": "1.0",
  "obsidian": {
    "vaultPath": "vault/",
    "cacheFile": ".obsidian/cache.json",
    "exportMethod": "cache.json | dataview-plugin | cli-tool",
    "monitorCacheForChanges": true,
    "lastExportTime": "2026-05-18T15:00:00Z"
  },
  "documentParsing": {
    "includeHeadings": true,
    "headingLevels": [1, 2, 3],
    "includeFrontmatter": true,
    "extractLinks": true,
    "computeBackreferences": true
  },
  "pathsToIndex": {
    "fileLevel": ["vault/decision.md", "vault/intention.md", "vault/lessons/"],
    "headingLevel": ["vault/decision.md", "vault/patterns.md", "specs/", "wiki/"]
  },
  "exclude": [
    "wiki/raw/",
    ".obsidian/",
    ".*archive.*"
  ]
}
```

---


## Integration with /spek.map


## In `/spek.map` Workflow

**Step 2 (export doc nodes):**
```bash
# Read config.json for export method
method=$(jq -r .obsidian.exportMethod vault/graph/config.json)

# If cache.json method:
python3 .spek/bin/obsidian-export.py \
  --cache-file ".obsidian/cache.json" \
  --output "vault/graph/nodes-docs.jsonl" \
  --config "vault/graph/config.json"

# If dataview method:
obsidian-dataview-export \
  --vault "vault/" \
  --query "wiki/queries/export-graph.md" \
  --output "vault/graph/nodes-docs.jsonl"
```

**Output:** `vault/graph/nodes-docs.jsonl` (ready for merge with code nodes)

---

