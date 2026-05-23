---
title: "Obsidian Graph Export Protocol"
status: "ATOMIC SPECIFICATION"
version: "1.0.0-alpha.1"
date: "2026-05-20"
---

# Spec: Obsidian Graph Export Protocol

**Status:** ATOMIC SPECIFICATION (2026-05-18)   | **Version:** 1.0.0-alpha.1 (2026-05-20)
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

## Obsidian Export Methods (Priority Order)

### Method 1: Dataview Plugin Export (Recommended)

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

### Method 2: Obsidian Native Cache (cache.json)

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

### Obsidian CLI Tool (Recommended)

**What it is:**
- Obsidian CLI is the recommended tool for automated vault operations, export, and graph extraction in Spekificity.
- Automated persistent memory and vault management is best performed via the Obsidian CLI at runtime to enable scriptable CI workflows; however, manual markdown-based workflows and cache-based exports are supported when the CLI is unavailable.

**Setup:**
```bash
# Install obsidian CLI (required)
npm install -g @obsidianmd/obsidian-cli

# Export vault structure
obsidian export-graph /path/to/vault --format=json
```

**Output Format:**
```json
{
  "nodes": [
    {
      "id": "vault/decision.md#api-versioning",
      "label": "API Versioning Strategy",
      "type": "document",
      "frontmatter": { ... }
    }
  ],
  "links": [
    { "source": "vault/decision.md#api-versioning", "target": "vault/patterns.md#versioning-pattern", "type": "references" }
  ]
}
```

**Pros:**
- Dedicated tool for graph export
- Structured JSON output (ready for processing)
- Supports multiple formats (JSON, GraphML, SVG)

**Cons:**
- Requires npm installation
- Dependency on external tool maintenance

**Best for:**
- All projects using Spekificity (mandatory)
- Integration with external graph visualization tools

---

## Export to JSONL Conversion

### Input: Obsidian cache.json

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

### Output: nodes-docs.jsonl (one line per heading)

```jsonl
{"type":"doc","id":"vault/decision.md#api-versioning-strategy","file":"vault/decision.md","heading":"API Versioning Strategy","level":2,"docType":"decision","tags":["api","versioning"],"status":"active","description":"Rationale for versioning strategy...","references":[],"referencedBy":[]}
{"type":"doc","id":"vault/decision.md","file":"vault/decision.md","title":"Decision Index","level":"file","docType":"decision","tags":["decision"],"status":"active","description":"Index of all architectural decisions","references":[],"referencedBy":[]}
```

### Conversion Process

```bash
# Python script: obsidian-export.py
import json
import re
from pathlib import Path

def convert_heading_to_id(heading_text):
    """Convert 'API Versioning Strategy' → 'api-versioning-strategy'"""
    return heading_text.lower().replace(" ", "-").replace("--", "-")

def parse_obsidian_cache(cache_file):
    """Read cache.json and yield doc nodes"""
    
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    for file_path, file_data in cache['files'].items():
        # Skip non-markdown files
        if not file_path.endswith('.md'):
            continue
        
        # Extract file-level metadata
        fm = file_data.get('frontmatter', {})
        doc_type = fm.get('type', 'guide')
        status = fm.get('status', 'active')
        tags = fm.get('tags', [])
        
        # Skip files outside documentation paths
        doc_paths = ['vault/decision.md', 'vault/intention.md', 'vault/patterns.md', 
                     'vault/lessons/', 'specs/', 'wiki/', '.github/agents/skills/']
        if not any(file_path.startswith(p) for p in doc_paths):
            continue
        
        # Create file-level node
        yield {
            "type": "doc",
            "id": file_path,
            "file": file_path,
            "level": "file",
            "title": fm.get('title') or Path(file_path).stem.replace('-', ' ').title(),
            "docType": doc_type,
            "status": status,
            "tags": tags,
            "description": fm.get('description', ''),
            "references": [],
            "referencedBy": []
        }
        
        # Create heading-level nodes (only for content-heavy files)
        if file_path in ['vault/decision.md', 'vault/patterns.md', 'specs/', 'wiki/']:
            for heading in file_data.get('headings', []):
                heading_text = heading['heading']
                heading_id = convert_heading_to_id(heading_text)
                node_id = f"{file_path}#{heading_id}"
                
                yield {
                    "type": "doc",
                    "id": node_id,
                    "file": file_path,
                    "heading": heading_text,
                    "level": heading['level'],
                    "docType": doc_type,
                    "status": status,
                    "tags": tags,
                    "description": f"See {file_path}#{heading_id}",  # placeholder
                    "references": [],
                    "referencedBy": [],
                    "parent": file_path
                }

# Usage
cache_file = ".obsidian/cache.json"
output_file = "vault/graph/nodes-docs.jsonl"

with open(output_file, 'w') as out:
    for node in parse_obsidian_cache(cache_file):
        out.write(json.dumps(node) + '\n')

print(f"Exported {output_file}")
```

---

## Link Discovery & Reference Extraction

### Markdown Link Parsing

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

### Reference Computation

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

### In `/spek.map` Workflow

**Step 2 (export doc nodes):**
```bash
# Read config.json for export method
method=$(jq -r .obsidian.exportMethod vault/graph/config.json)

# If cache.json method:
python3 .spekificity/bin/obsidian-export.py \
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

## Success Criteria

- [x] Export method chosen and documented (cache.json recommended)
- [x] Conversion script converts cache.json → nodes-docs.jsonl format
- [x] Heading-to-ID conversion handles special characters
- [x] Link discovery extracts all markdown link types
- [x] Backreferences computed and stored
- [x] Configuration templated for different export methods
- [x] Integration with `/spek.map` Step 2 documented

---

## Implementation Checklist

- [ ] Create `obsidian-export.py` script in `.spekificity/bin/`
- [ ] Test export on real vault (validate cache.json parsing)
- [ ] Verify nodes-docs.jsonl format matches schema (node-schema-design)
- [ ] Add config template to `vault/graph/config.json`
- [ ] Document export troubleshooting in guide
- [ ] Test link discovery (verify backreferences computed correctly)

---

## References

- **Obsidian cache format:** [Obsidian Plugin Development Docs](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata)
- **Cache monitoring:** Watch `.obsidian/cache.json` for real-time vault changes
- **Dataview plugin:** [Obsidian Dataview](https://github.com/blacksmithgu/obsidian-dataview)
- **Related specs:** node-schema-design, spek-map-command
