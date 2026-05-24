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
