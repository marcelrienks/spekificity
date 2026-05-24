# Spec: Graph Merge and Integration


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Concern:** Merging code nodes (lat.md) and doc nodes (Obsidian export) into unified graph  
**Extracted from:** extracted spec Questions 2, 3, 5  
**Depends on:** obsidian-graph-export, node-schema-design  
**Used by:** spek-map-command, graph-storage-structure  

---


## Overview

**Problem:** Code nodes (from lat.md) and doc nodes (from Obsidian) are generated separately. They need to be merged into a single queryable graph, with cross-references computed (e.g., "which code symbols does this decision affect?").

**Solution:** Define merge strategy: deduplication, link discovery, backreference computation, single nodes.jsonl output.

**Outcome:** Unified vault/graph/nodes.jsonl containing code and doc nodes with bidirectional references, enabling agent queries like "find all code affected by [decision]" or "find all decisions related to [function]".

---


## Success Criteria

- [x] Deduplication removes redundant nodes
- [x] Link discovery finds code↔doc cross-references
- [x] Backreferences are computed and symmetric
- [x] Merged graph is validated (no duplicates, consistent references)
- [x] Output format is JSONL (streaming-friendly)
- [x] Metadata tracks merge history and validation
- [x] Problematic cases (broken links, missing files) are handled gracefully
- ## Implementation Checklist
- [ ] Create `merge-graphs.py` script in `.spek/bin/`
- [ ] Implement deduplication logic
- [ ] Implement link discovery patterns (code→doc, doc→code)
- [ ] Implement backreference computation
- [ ] Add validation checks (duplicates, symmetry, file existence)
- [ ] Test on real graph (validate merging works correctly)
- [ ] Add error reporting for broken references
- [ ] Integrate into `/spek.map` workflow (Step 3)
- ## References
- **Input specs:** obsidian-graph-export, node-schema-design
- **Output specs:** spek-map-command, graph-storage-structure, graph-query-patterns


## Step 4: Compute Backreferences

**Goal:** For each reference A→B, add B→A (referencedBy).

**Strategy:** Build reverse index, then update all nodes.

```python
def compute_backreferences(all_nodes):
    """Compute referencedBy based on references"""
    
    # Build reverse index
    referenced_by = {}  # node_id → list of node_ids that reference it
    
    for node in all_nodes:
        for ref in node.get('references', []):
            if ref not in referenced_by:
                referenced_by[ref] = []
            referenced_by[ref].append(node['id'])
    
    # Update nodes
    for node in all_nodes:
        node['referencedBy'] = referenced_by.get(node['id'], [])
    
    return all_nodes
```

---


## Merge Process


## Step 1: Load Source Node Sets

**Input:**
- `vault/graph/nodes-code.jsonl` (from lat.md export or adapter)
- `vault/graph/nodes-docs.jsonl` (from Obsidian export)
- `vault/graph/config.json` (merge strategy config)

**Output:** Two in-memory node sets (code_nodes[], doc_nodes[])

```python
def load_nodes(file_path):
    nodes = []
    with open(file_path, 'r') as f:
        for line in f:
            nodes.append(json.loads(line))
    return nodes

code_nodes = load_nodes('vault/graph/nodes-code.jsonl')
doc_nodes = load_nodes('vault/graph/nodes-docs.jsonl')
```

---


## Step 2: Deduplication

**Problem:** Same file might be indexed as both code node (if executable) and doc node (if has markdown). Remove duplicates.

**Strategy:**
- Code nodes: deduplicate by (file, symbol, symbolType)
- Doc nodes: deduplicate by (file, heading, level)
- Cross-type: If a file is both .ts and referenced as doc, keep separate (different node types)

```python
def deduplicate(nodes):
    seen = {}
    unique = []
    for node in nodes:
        key = (node['type'], node['file'], 
               node.get('symbol') or node.get('heading'))
        if key not in seen:
            seen[key] = node
            unique.append(node)
    return unique

code_nodes = deduplicate(code_nodes)
doc_nodes = deduplicate(doc_nodes)
```

---


## Step 3: Link Discovery

**Goal:** Find cross-references between code and doc nodes (e.g., code imports doc, or code implements pattern).

**Patterns:**

1. **Code → Code references** (already in code_nodes from lat.md)
   - Calls: `function_a` calls `function_b`
   - Dependencies: `class_a` uses `class_b`
   - Imports: `file_a` imports from `file_b`

2. **Doc → Doc references** (already in doc_nodes from Obsidian)
   - Markdown links: `[text](vault/decision.md#heading)`
   - Related entries: "Related Decisions" section

3. **Code → Doc references** (NEW: discover in this step)
   - Pattern matches: `decision.md#caching-pattern` mentioned in `src/cache.ts` comments
   - Skill references: `src/skills/prepare.ts` implements `/spek.prepare` skill definition
   - Manual links: Code has comment `// See vault/decision.md#api-versioning`

4. **Doc → Code references** (NEW: discover in this step)
   - Lesson mentions: `vault/lessons/2026-05-18-003.md` references `src/prepare/prepare.ts`
   - Decision affects: Decision doc lists affected components in frontmatter
   - Spec implements: Spec document lists code files that implement it

**Implementation:**


> Example moved to [Example: 057-graph-merge-integration-code-2.md](./examples/057-graph-merge-integration-code-2.md)


---


## Step 5: Merge into Single Graph

**Strategy:** Concatenate code + doc nodes into single nodes.jsonl.

**Order:** (optional, but suggested for readability)
- All code nodes (sorted by file, then symbol)
- All doc nodes (sorted by file, then heading level)
- All skill nodes (sorted by command)

```python
def merge_graphs(code_nodes, doc_nodes, skill_nodes):
    """Merge all node types into single graph"""
    
    # Sort each type
    code_nodes.sort(key=lambda n: (n['file'], n['symbol']))
    doc_nodes.sort(key=lambda n: (n['file'], n.get('level', 999)))
    skill_nodes.sort(key=lambda n: n.get('command', n['id']))
    
    # Merge
    all_nodes = code_nodes + doc_nodes + skill_nodes
    
    # Write
    with open('vault/graph/nodes.jsonl', 'w') as f:
        for node in all_nodes:
            f.write(json.dumps(node) + '\n')
    
    return len(all_nodes)

total_nodes = merge_graphs(code_nodes, doc_nodes, skill_nodes)
print(f"Merged {total_nodes} nodes")
```

---


## Step 6: Validate Merged Graph

**Checks:**

1. **No duplicate IDs:**
   ```python
   ids = [n['id'] for n in all_nodes]
   assert len(ids) == len(set(ids)), "Duplicate node IDs found"
   ```

2. **Backreferences are symmetric:**
   ```python
   for node in all_nodes:
       for ref in node['references']:
           # Find node with id=ref
           target = find_node_by_id(all_nodes, ref)
           if target:
               assert node['id'] in target.get('referencedBy', [])
   ```

3. **All files exist:**
   ```python
   for node in all_nodes:
       assert Path(node['file']).exists(), f"File not found: {node['file']}"
   ```

4. **Node types are valid:**
   ```python
   for node in all_nodes:
       assert node['type'] in ['code', 'doc', 'skill'], f"Invalid type: {node['type']}"
   ```

---


## Configuration (vault/graph/config.json)


> Example moved to [Example: 057-graph-merge-integration-code-1.md](./examples/057-graph-merge-integration-code-1.md)


---


## Problematic Cases


## Case 1: File is both code and docs

Example: `src/config/vault-config.ts` is TypeScript code but has extensive comments that should be indexed as doc.

**Solution:**
- Create code node for the symbol: `src/config/vault-config.ts:VaultConfig`
- Create doc node for the file comments: `src/config/vault-config.ts` (file-level doc)
- Link them: code node references doc node (describes what the code does)


## Case 2: Code comment mentions decision but link is wrong

Example: Comment says "See caching pattern" but file is `vault/patterns.md` (correct) but heading doesn't exist.

**Solution:**
- Discover pattern in comment
- Try to find heading: `vault/patterns.md#caching-pattern`
- If not found, flag as "broken reference" in validation report
- Proceed anyway (don't fail merge)


## Case 3: Doc links to code that doesn't exist (yet)

Example: Spec mentions `src/new-feature/new-feature.ts` but feature not implemented yet.

**Solution:**
- Store reference as-is (even if target doesn't exist)
- Validation will flag as "orphaned" (optional check)
- When code is later implemented, re-run `/spek.map` to update graph

---


## Output Schema


## vault/graph/nodes.jsonl

```
One node per line, no pretty-printing, in merge order:
```jsonl
{"type":"code","id":"src/prepare/prepare.ts:Prepare",...,"references":["vault/decision.md#git-workflow"],"referencedBy":["src/cli/automate.ts"]}
{"type":"doc","id":"vault/decision.md#git-workflow",...,"references":["src/prepare/prepare.ts:Prepare"],"referencedBy":["src/prepare/prepare.ts"]}
{"type":"skill","id":"skills/spek-prepare/SKILL.md",...,"references":["vault/decision.md#git-workflow"],"referencedBy":[]}
```


## vault/graph/metadata.json

```json
{
  "version": "1.0",
  "lastMerge": "2026-05-18T15:00:00Z",
  "nodeCount": 1234,
  "breakdown": {
    "code": 1000,
    "doc": 200,
    "skill": 34
  },
  "sourceHashes": {
    "nodes-code.jsonl": "a1b2c3d4e5f6...",
    "nodes-docs.jsonl": "f6e5d4c3b2a1...",
    "config.json": "z9y8x7w6v5u4..."
  },
  "validation": {
    "passed": true,
    "errors": [],
    "warnings": [
      "Broken reference: vault/patterns.md#caching-pattern (not found)"
    ]
  }
}
```

---


## Integration with /spek.map


## In `/spek.map` Workflow

**Step 3 (merge):**
```bash
# After lat.md + Obsidian export complete:
# Export code nodes from lat.md (if available):
# `lat export --format jsonl --output vault/graph/nodes-code.jsonl`
# or use your adapter to produce `nodes-code.jsonl`.
python3 .spek/bin/merge-graphs.py \
  --code-nodes "vault/graph/nodes-code.jsonl" \
  --doc-nodes "vault/graph/nodes-docs.jsonl" \
  --config "vault/graph/config.json" \
  --output "vault/graph/nodes.jsonl" \
  --metadata "vault/graph/metadata.json" \
  --validate

echo "Merged $(jq .nodeCount vault/graph/metadata.json) nodes"
```

**Output:** 
- `vault/graph/nodes.jsonl` (queryable)
- `vault/graph/metadata.json` (timestamps, validation report)

---

