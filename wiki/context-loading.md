# Code Indexing & Context Loading (Phase 2)

## Overview

Phase 2 implements code indexing and context injection layer. Spekificity:

1. Indexes the codebase using lat.md (BM25 lexical search)
2. Loads relevant code, decisions, and patterns for task execution
3. Injects context into agent sessions (code snippets, prior decisions, patterns)
4. Compresses context using Caveman notation for token efficiency

---

## Components

### 1. lat.md Integration (`integrations/lat_md.py`)

**Purpose:** Code indexing and semantic search via BM25 retrieval

**API:**
```python
from spekificity.integrations.lat_md import LatMdIndex, query_relevant_context

# Initialize index
index = LatMdIndex(project_path=".")
index.ensure_index()        # Init if missing
index.sync_index()          # Sync with codebase

# Query for files
files = index.query_files("authentication", limit=5)
# Returns: [{"path": "auth.py", "relevance": "high"}, ...]

# Query for functions
funcs = index.query_functions("authenticate", limit=5)
# Returns: [{"file": "auth.py", "line": 42, "signature": "def authenticate(...)"}, ...]

# Query impact analysis
impact = index.query_impact("auth.py")
# Returns: {"callers": [...], "dependencies": [...]}

# Convenience function
context = query_relevant_context("JWT authentication")
# Returns: {"files": [...], "functions": [...]}
```

**Fallback:** If lat.md times out or is unavailable, context loading falls back to semantic search for graceful degradation.

---

### 2. Semantic Search Fallback (`integrations/semantic_search.py`)

**Purpose:** Grep-based code search when lat.md is unavailable

**API:**
```python
from spekificity.integrations.semantic_search import SemanticSearcher, search_relevant_context

# Initialize searcher
searcher = SemanticSearcher(project_path=".")

# Search for files
files = searcher.search_files("authentication", limit=5)

# Search for functions
funcs = searcher.search_functions("def authenticate", limit=5)

# Pattern search
matches = searcher.search_by_pattern(r"class.*Auth", file_type="*.py")

# Convenience function
context = search_relevant_context("JWT authentication")
# Returns: {"files": [...], "functions": [...]}
```

**Advantages:**
- No external tool dependency (uses grep)
- Fast for small codebases
- Reliable fallback when lat.md unavailable

---

### 3. Context Loading (`core/context.py`)

**Purpose:** Load decisions, patterns, code for task execution

**API:**
```python
from spekificity.core.context import ContextLoader, load_context_for_task

# Initialize loader
loader = ContextLoader(
    project_path=".",
    vault_path="vault"
)

# Load decisions relevant to intent
decisions = loader.load_relevant_decisions("authentication", limit=3)

# Load patterns relevant to intent
patterns = loader.load_relevant_patterns("authentication", limit=3)

# Load code relevant to intent
code = loader.load_relevant_code("authenticate", limit=3)

# Load complete context
context = loader.load_task_context(
    task_id="T2.1",
    task_description="Implement JWT authentication",
    max_decisions=3,
    max_patterns=3,
    max_code=3,
)

# Convenience function
context_str = load_context_for_task(
    task_id="T2.1",
    task_description="Implement JWT authentication",
    compressed=False
)
```

**Context Matching:**
- Decisions: Title/content matching against intent
- Patterns: Category + title matching
- Code: lat.md queries → fallback to semantic search

---

### 4. Context Compression (`core/compression.py`)

**Purpose:** Compress context using Caveman notation for token efficiency

**Intensity Levels:**

| Level | Token Savings | Example |
|-------|---------------|---------|
| **lite** | ~25% | Remove filler, keep structure |
| **full** (default) | ~50% | Drop articles, use fragments |
| **ultra** | ~75% | Abbreviate prose, use arrows |

**API:**
```python
from spekificity.core.compression import CavemanCompressor, compress_text, compress_context

# Initialize compressor
compressor = CavemanCompressor(intensity="full")

# Compress text
compressed = compressor.compress_text("Just implement the authentication basically")
# Output: "Implement authentication"

# Compress context
context_str = compressor.compress_context(task_context)

# Convenience functions
compressed = compress_text(text, intensity="full")
compressed = compress_context(context, intensity="ultra")
```

**Caveman Rules:**
- **Lite**: Remove filler (just, really, basically, actually, simply)
- **Full**: Drop articles (a, an, the), use fragments
- **Ultra**: Abbreviate prose (DB, auth, config), use arrows (→)

**Token Estimates:**
- Normal context: 1,000-2,000 tokens
- Lite compression: 750-1,500 tokens (~25% savings)
- Full compression: 500-1,000 tokens (~50% savings)
- Ultra compression: 250-500 tokens (~75% savings)

---

## Workflow

### 1. Prepare Stage

```python
# /spek.prepare command
from spekificity.core.context import ContextLoader

loader = ContextLoader()

# Load vault context
decisions = loader.load_relevant_decisions("feature description")
patterns = loader.load_relevant_patterns("feature description")

# Index codebase
from spekificity.integrations.lat_md import load_index
index = load_index()
index.sync_index()

# Generate navigation guide
code = loader.load_relevant_code("feature description", limit=5)
```

### 2. Plan Stage

```python
# /spek.plan command
# Plans already have architectural context from spec
# No additional context loading needed
```

### 3. Implement Stage

```python
# /spek.implement TASK_ID command
from spekificity.core.context import load_context_for_task

# Load complete context for task
context = load_context_for_task(
    task_id="T1.1",
    task_description="[from tasks.md]",
    compressed=False  # or True with --caveman flag
)

# Inject into agent session
# Agent executes task with context available
```

### 4. Conclude Stage

```python
# /spek.conclude command
# Extracts lessons from implementation
# Updates vault with new decisions/patterns
# Refreshes context for next feature
```

---

## Performance Targets (Phase 2 SLAs)

| Operation | Target | Status |
|-----------|--------|--------|
| lat.md init | < 10s | — |
| lat.md sync | < 5s (incremental), < 30s (full) | — |
| lat.md query | < 1s | — |
| Semantic search fallback | < 3s | — |
| Context loading | < 5s | — |
| Context compression | < 1s | — |
| /spek.prepare | < 30s total | Depends on above |

---

## Configuration

### lat.md

lat.md is configured per-project in `.lat/` directory.

```bash
# Initialize index
lat init .

# Sync with codebase
lat sync .

# Full rebuild
lat sync . --full

# Query
lat query files "authentication"
lat query functions "authenticate"
lat query impact src/auth.py
```

### Fallback Strategy

If lat.md unavailable:
1. Try semantic search (grep-based)
2. Return empty context (graceful degradation)
3. Agent continues without context injection

---

## Testing

Run Phase 2 tests:

```bash
pytest spekificity/tests/test_phase2.py -v
```

Tests cover:
- Semantic search functionality
- Context loading from vault
- Code relevance matching
- Context formatting (normal + compressed)
- Caveman compression at all intensity levels
- Full integration pipeline

---

## Troubleshooting

### lat.md not found

```bash
# Install lat.md
pip install lat-md

# Or use fallback (automatic)
# Semantic search will be used instead
```

### Slow context loading

```python
# Reduce context size
context = loader.load_task_context(
    task_id="T1.1",
    task_description="...",
    max_decisions=2,  # Reduce from 3
    max_patterns=2,   # Reduce from 3
    max_code=2,       # Reduce from 3
)

# Or use compression
compressed = load_context_for_task(..., compressed=True)
```

### No code found in search

```python
# Check if vault/code paths are correct
loader.project_path
loader.vault.path

# Try manual lat sync
lat sync . --full

# Check file permissions
```

---

## Next Phase (Phase 3)

Phase 3 will integrate context loading with SpecKit wrapper:

- Inject context into `/speckit.specify` command
- Inject context into `/speckit.plan` command
- Inject context into `/speckit.implement` command
- Enrichment layer to pass vault context to SpecKit

---

## Related

- [Vault Engine](../spekificity/core/vault.py)
- [Type Contracts](../spekificity/core/types.py)
- [IMPL_PLAN Phase 2](../IMPL_PLAN.md#phase-2-vault--code-indexing-weeks-2-3-50-70-hours)

---

**Phase 2 Status:** In progress  
**Last Updated:** 2026-06-07
