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
