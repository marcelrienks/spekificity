---
consolidated-from:
  - 057-graph-merge-integration-code-1.md
  - 057-graph-merge-integration-code-2.md
consolidated-at: 2026-05-24T12:10:00Z
---

# Examples: 057 — Graph Merge Integration

This file consolidates merge strategy JSON and helper code used to discover references between code and docs.

## Source: 057-graph-merge-integration-code-1.md

```json
{
  "version": "1.0",
  "merge": {
    "strategy": "union-with-dedup",
    "deduplication": {
      "codeNodes": "by (file, symbol, symbolType)",
      "docNodes": "by (file, heading, level)",
      "crossType": "keep separate (code and doc are different)"
    },
    "linkDiscovery": {
      "codeToDocPatterns": [
        "vault/path#heading in comments/docstrings",
        "decision/pattern name mentions",
        "See [doc] comments"
      ],
      "docToCodePatterns": [
        "src/path/file.ts code paths",
        "import statements",
        "function/class name mentions"
      ]
    },
    "backreferenceComputation": "bidirectional mirrors (A→B means B←A)",
    "sortOrder": ["code nodes by (file, symbol)", "doc nodes by (file, heading)", "skill nodes by command"]
  },
  "validation": {
    "noDuplicateIds": true,
    "backreferencesSymmetric": true,
    "allFilesExist": true,
    "noOrphanedNodes": false,
    "nodeTypesValid": true
  }
}
```

## Source: 057-graph-merge-integration-code-2.md

```python
def discover_code_to_doc_refs(code_node):
    """Find doc references in code (comments, docstrings)"""
    refs = []
    file_path = code_node['file']
    
    with open(file_path, 'r') as f:
        content = f.read()
        
    # Pattern 1: vault/path.md#heading comments
    pattern = r'vault/[a-z-]+\.md#[a-z0-9-]+'
    matches = re.findall(pattern, content, re.IGNORECASE)
    refs.extend(matches)
    
    # Pattern 2: See decision/pattern named X
    if 'caching' in content.lower() and 'See' in content:
        refs.append('vault/patterns.md#caching-pattern')  # heuristic
    
    return refs

def discover_doc_to_code_refs(doc_node):
    """Find code references in docs (links to files, imports, etc)"""
    refs = []
    
    # If doc mentions 'src/prepare/prepare.ts', link it
    file_path = doc_node['file']
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern: Code file paths (e.g., src/prepare/prepare.ts)
    pattern = r'src/[a-z0-9/_-]+\.(?:ts|py|js)'
    matches = re.findall(pattern, content, re.IGNORECASE)
    refs.extend(matches)
    
    return refs

# Add discovered references to nodes
for code_node in code_nodes:
    discovered = discover_code_to_doc_refs(code_node)
    code_node['references'].extend(discovered)

for doc_node in doc_nodes:
    discovered = discover_doc_to_code_refs(doc_node)
    doc_node['references'].extend(discovered)
```
