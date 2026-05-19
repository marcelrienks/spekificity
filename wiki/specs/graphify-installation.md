# ATOMIC SPECIFICATION: Graphify Installation (C5.1)

**Status:** ATOMIC SPECIFICATION  
**Type:** Setup — Graphify Installation & Configuration  
**Depends On:** None  
**Used By:** /spek.prepare, /spek.map  

---

## Overview

Graphify is a code indexing tool that generates queryable code graphs via tree-sitter AST. This spec covers installation, verification, and configuration.

---

## Installation Steps

### 1. Prerequisites Check

```bash
# Python 3.11+
python3 --version

# uv package manager
uv --version
```

If missing: Install via Homebrew (macOS) or system package manager

### 2. Install Graphify

```bash
# Via uv (recommended)
uv tool install graphifyy

# Verify
graphify --version
```

### 3. Configuration

Create `.spekificity/config.yaml`:

```yaml
graphify:
  mode: global  # "global" = via uv; "local" = pip in venv
  
  generation:
    languages:
      - python
      - typescript
      - javascript
    exclude_paths:
      - node_modules/
      - venv/
      - __pycache__/
      - dist/
      - build/
    max_file_size: 1000000
  
  output:
    primary_format: jsonl
    generate_html: true
  
  refresh:
    enable_git_hook: true
  
  performance:
    parallel: true
    max_workers: 4
```

### 4. Verification

```bash
# Test graphify works
graphify --help

# Verify can index a Python file
graphify index path/to/sample.py
```

---

## Verification Checklist

✅ Graphify installed  
✅ `graphify --version` works  
✅ `.spekificity/config.yaml` created  
✅ Configuration is valid YAML  
✅ Test index succeeds  

---

## Implementation Checklist

- [ ] Check Python 3.11+
- [ ] Check uv installed
- [ ] Install graphifyy
- [ ] Create config.yaml
- [ ] Verify installation
- [ ] Create graph/ directory

---

## References

**Related Specs:**
- [graph-storage-structure.md](graph-storage-structure.md) — Graph directory layout
- [spek-map-command.md](spek-map-command.md) — /spek.map uses graphify

**External:**
- [graph-setup Part 1](codegraph-setup-and-integration.md#part-1-graphify-installation--setup)
