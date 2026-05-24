# Spec: Obsidian Graph Export Protocol


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Concern:** How to extract documentation nodes from Obsidian vault for graph indexing  
**Extracted from:** extracted spec Question 2  
**Depends on:** node-schema-design  
**Used by:** /spek.map, extracted spec graph merge step  

---


## Overview

**Problem:** Documentation exists in Obsidian vault but is not queryable for agent-assisted spec/plan generation. Need a reliable way to extract doc graph structure (headings, links, metadata) and convert to nodes.jsonl format.

**Solution:** Use Obsidian's built-in export capabilities via the Obsidian CLI to export vault graph to structured JSONL format that can be merged with code nodes. Alternative export methods (Dataview plugin, `.obsidian/cache.json`) are unsupported for core automation.

**Outcome:** Documentation becomes queryable via vault/graph/nodes-docs.jsonl, enabling agent to discover existing decisions, patterns, and lessons without re-reading all markdown files.

---


## Success Criteria

- [x] Export method chosen and documented (Obsidian CLI export)
- [x] Conversion script converts Obsidian CLI export → nodes-docs.jsonl format
- [x] Heading-to-ID conversion handles special characters
- [x] Link discovery extracts all markdown link types
- [x] Backreferences computed and stored
- [x] Configuration templated for Obsidian CLI export
- [x] Integration with `/spek.map` Step 2 documented
- ## Implementation Checklist
- [ ] Create `obsidian-export.py` script in `.spek/bin/`
- [ ] Test export on real vault (validate Obsidian CLI export parsing)
- [ ] Verify nodes-docs.jsonl format matches schema (node-schema-design)
- [ ] Add config template to `vault/graph/config.json`
- [ ] Document export troubleshooting in guide
- [ ] Test link discovery (verify backreferences computed correctly)
- ## References
- **Obsidian cache format:** [Obsidian Plugin Development Docs](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata)
- **Monitoring:** Use Obsidian CLI export hooks to detect real-time vault changes. The Obsidian CLI is the primary integration; the Obsidian desktop app is optional and may be used for visualization or to enable certain plugin-driven exports.
- **Dataview plugin:** [Obsidian Dataview](https://github.com/blacksmithgu/obsidian-dataview)
- **Related specs:** node-schema-design, spek-map-command


## Obsidian Export Methods (Priority Order)


## Method 1: Dataview Plugin Export (deprecated/unsupported)

-**What it is (unsupported for core automation):**
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


## Method 2: Obsidian Native Cache (cache.json) — deprecated/unsupported

**Note:** Direct parsing of `.obsidian/cache.json` is deprecated for core Spekificity automation. The canonical, supported export path is the Obsidian CLI export. Cache-based parsing may be used only for experimental or legacy workflows and is unsupported for primary automation flows.

---


## Obsidian CLI (Required)

**What it is:**
- The `obsidian` CLI is the `obsidian` command. It provides programmatic access to script exports, run JS in-app, and invoke plugin commands for Spekificity automation. The `obsidian` CLI is the primary integration; the Obsidian desktop app is optional and may be used for visualization or to enable some plugin-driven exports. Alternative export methods (Dataview plugin, `.obsidian/cache.json`) are unsupported for core automation.

**Setup / How to use:**
- Enable the CLI in Obsidian: Settings → General → Command line interface, then follow the on-screen prompt to register the `obsidian` command in your PATH. The `obsidian` CLI is the primary integration; some CLI operations or plugin-driven exports may require the Obsidian app to be running — for CI/headless options, see: https://obsidian.md/help/headless
- Example: run a small JS snippet inside the running Obsidian app to inspect files (returns JSON):

```bash
# list file paths (example; some operations may require the Obsidian app to be running)
obsidian eval code="JSON.stringify(app.vault.getFiles().map(f=>f.path))"
```

-- For structured exports prefer Obsidian CLI-based approaches:
  - Use `obsidian eval` or plugin commands via the Obsidian CLI to produce a JSON export (exact command depends on CLI version and installed plugins). Dataview/plugin exports and direct `.obsidian/cache.json` parsing are unsupported for core automation.

**Pros:**
- First-class automation path when Obsidian app + CLI are available
- Allows running developer/plugin commands and JS in-app for flexible exports

**Cons:**
- Requires the `obsidian` CLI to be registered in PATH. The Obsidian desktop app is optional and used only for interactive visualization or for export workflows that depend on a running instance.
- Some export workflows require plugins (Dataview) or custom JS snippets — plugin-based exports are unsupported for core automation

**Best for:**
- Projects that want scripted, repeatable exports from the canonical vault. CI environments must provide the Obsidian CLI; automation is unsupported otherwise.

---


## Export to JSONL Conversion


## Input: Obsidian CLI export (JSON)

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
3. `[[vault/decision.md]]` — Obsidian wiki-link syntax (also present in CLI export)
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
    "obsidianCliExportPath": "vault/graph/export.jsonl",
    "exportMethod": "cli-tool",
    "useCliExportHooks": true,
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

## Obsidian CLI export (required)

Use the Obsidian CLI to produce a structured JSON/JSONL export for Spekificity automation. The `obsidian` CLI must be available and registered in PATH; depending on the export method, a running Obsidian app may be required. Example (pseudo-command; adapt to your export plugin/snippet):

```bash
# Example: run a JS export inside Obsidian and save output
obsidian eval code="JSON.stringify(app.plugins.plugins['my-export-plugin'].exportVault())" > vault/graph/nodes-docs.jsonl
```

**Output:** `vault/graph/nodes-docs.jsonl` (ready for merge with code nodes)

---

