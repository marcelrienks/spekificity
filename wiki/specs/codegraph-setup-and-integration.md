# [ARCHIVED] Graphify Setup Specification — LEGACY

**Status:** ARCHIVED (Superseded 2026-05-20)  
**Replacement:** [CodeGraph Setup Complete](codegraph-setup-complete.md)  

**⚠️ DEPRECATION NOTICE:**

This specification is **ARCHIVED as LEGACY**. Graphify is no longer the recommended code analysis tool for Spekificity. All new projects should use **CodeGraph** (see [codegraph-setup-complete.md](codegraph-setup-complete.md)).

**Why:** CodeGraph is 20x faster for agent queries, has built-in MCP integration, and requires less manual refresh logic.

**Migration:** Existing Graphify users should rebuild their code graphs with CodeGraph. See [codegraph-setup-complete.md](codegraph-setup-complete.md) Step 1-4 for setup.

---

## LEGACY CONTENT (Preserved for Reference)

---

## Executive Summary

**graph-setup specifies the Graphify-based codegraph setup and integration layer retained for transition and fallback scenarios in Spekificity.**

Graphify transforms the codebase into a persistent, queryable knowledge graph using tree-sitter AST (Abstract Syntax Tree). This graph becomes a critical input to `/spek.automate` specify and plan phases, enabling:

- **Context-aware spec generation** — Recent code changes inform feature requirements
- **Architectural alignment checking** — Plans validated against codebase topology
- **Impact analysis** — Code changes traced to affected modules
- **Zero-token graph queries** — Pure AST mode uses no API tokens

**Key deliverables:**
1. Step-by-step Graphify installation guide
2. Vault structure for graph storage and access
3. `/spek.map` skill specification (generate + maintain graphs)
4. Incremental refresh strategy (git hooks + SHA256 caching)
5. Performance scoping and token efficiency
6. Configuration templates (.spekificity/config.yaml)
7. Integration contracts with extracted spec and extracted spec

---

## Part 1: Graphify Installation & Setup

### What is Graphify?

**Graphify** (pip: `graphifyy` package) is a multi-language code indexing tool that:

- **Parses code via tree-sitter** — AST-based, accurate for 20+ languages
- **Generates knowledge graphs** — Nodes (functions, classes, modules) + Edges (calls, inheritance, dependencies)
- **Supports incremental updates** — SHA256 caching; only processes changed files
- **Exports multiple formats** — JSON (queryable), HTML (interactive), JSONL (agent-readable), Markdown (human-browsable)
- **Zero tokens in AST mode** — No API calls; pure local processing

### Installation Steps

#### 1a. Prerequisites

```bash
# Check Python
python3 --version
# Expected: 3.11+

# Check uv package manager
uv --version
# Expected: uv 0.x or later
```

**If missing:**
```bash
# Install Python 3.11+ (macOS)
brew install python@3.11

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 1b. Install Graphify

```bash
# Via uv (recommended for Spekificity)
uv tool install graphifyy

# Verify
graphify --version
# Expected: graphifyy x.x.x

graphify --help
# Expected: Help output with commands
```

**Alternative: pip**
```bash
pip install graphifyy
```

#### 1c. Configure Graphify in .spekificity/

Create `.spekificity/config.yaml`:

```yaml
# Graphify Configuration
graphify:
  # Installation mode (global or local)
  mode: global  # "global" = installed via uv tool; "local" = pip in venv
  
  # Graph generation settings
  generation:
    # Languages to index
    languages:
      - python
      - typescript
      - javascript
      - go
      - rust
      - java
    
    # Folders to exclude
    exclude_paths:
      - node_modules/
      - venv/
      - __pycache__/
      - dist/
      - build/
      - .git/
    
    # Include hidden files?
    include_hidden: false
    
    # Max file size (bytes)
    max_file_size: 1000000
  
  # Caching strategy
  caching:
    # Cache directory
    cache_dir: .spekificity/cache/graphify/
    # Enable SHA256 caching?
    enable_cache: true
    # Cache expiry (hours)
    cache_expiry_hours: 24
  
  # Output formats
  output:
    # Primary format for agent queries
    primary_format: jsonl  # "json" | "jsonl" | "markdown"
    # Generate interactive HTML?
    generate_html: true
    # Generate Obsidian notes?
    generate_obsidian_notes: true
    # Obsidian vault path
    obsidian_output_dir: vault/graph/nodes/
  
  # Refresh strategy
  refresh:
    # Enable git post-commit hook?
    enable_git_hook: true
    # Enable watch mode for interactive dev?
    enable_watch_mode: false
    # Watch mode debounce (ms)
    watch_debounce_ms: 1000
  
  # Performance settings
  performance:
    # Use parallel processing?
    parallel: true
    # Number of worker threads
    max_workers: 4
    # Log verbose output?
    verbose: false
```

---

## Part 2: Vault Structure for Graphs

### Vault Graph Directory Structure

```
vault/
├── graph/                             ← All graph-related artifacts
│   ├── config.json                    ← Graph metadata (version, timestamp, language list)
│   ├── nodes.jsonl                    ← Primary agent-queryable graph (MERGED)
│   ├── nodes-code.jsonl               ← Code symbols from Graphify (pure AST)
│   ├── nodes-docs.jsonl               ← Document nodes from Obsidian export
│   ├── edges.jsonl                    ← Relationships (calls, inheritance, depends-on)
│   ├── cache/
│   │   ├── sha256.json                ← File hash cache for incremental updates
│   │   └── node-index.json            ← Lookup table (symbol → node ID)
│   ├── nodes/                         ← Obsidian notes (optional, if generate_obsidian_notes=true)
│   │   ├── functions/
│   │   ├── classes/
│   │   ├── modules/
│   │   └── frameworks/
│   ├── graph.json                     ← Full queryable graph (for interactive tools)
│   ├── graph.html                     ← Interactive visualization (open in browser)
│   ├── GRAPH_REPORT.md                ← Human-readable summary (metrics, communities, analysis)
│   └── refresh-log.md                 ← Timestamp + refresh history
```

### Graph Configuration File (vault/graph/config.json)

```json
{
  "version": "1.0",
  "generated_at": "2026-05-18T14:00:00Z",
  "graph_type": "hybrid",
  "sources": [
    {
      "type": "code",
      "tool": "graphify",
      "version": "0.5.0",
      "languages": ["python", "typescript", "javascript"],
      "file_count": 156,
      "node_count": 423
    },
    {
      "type": "documentation",
      "tool": "obsidian-export",
      "vault_path": "vault/",
      "file_count": 89,
      "node_count": 45
    }
  ],
  "merge_strategy": "hybrid",
  "merge_rules": {
    "code_node_weight": 0.7,
    "doc_node_weight": 0.3,
    "deduplication": "by_name_and_type"
  },
  "performance": {
    "cache_enabled": true,
    "incremental_enabled": true,
    "last_full_rebuild": "2026-05-18T14:00:00Z",
    "last_incremental_sync": "2026-05-18T14:30:00Z"
  },
  "queries": {
    "format": "jsonl",
    "indexed_fields": ["id", "type", "name", "scope", "file", "language"],
    "search_engine": "jq | grep"
  }
}
```

### Node Schema (JSONL Format)

Each line in `nodes.jsonl` is a JSON object representing a code symbol or document:

```json
{
  "id": "python:src/services/auth.py:AuthService:authenticate",
  "type": "method",
  "name": "authenticate",
  "language": "python",
  "scope": "AuthService",
  "file": "src/services/auth.py",
  "line_start": 42,
  "line_end": 58,
  "signature": "def authenticate(self, username: str, password: str) -> bool",
  "docstring": "Authenticate user against credentials database.",
  "complexity": "medium",
  "dependencies": [
    "src.database.query_user",
    "src.crypto.verify_password"
  ],
  "callers": [
    "src.api.login_handler",
    "src.api.token_refresh"
  ],
  "source": "code",
  "indexed_at": "2026-05-18T14:00:00Z"
}
```

### Edge Schema (JSONL Format)

```json
{
  "id": "edge:auth_authenticate->database_query_user",
  "from_node": "python:src/services/auth.py:AuthService:authenticate",
  "to_node": "python:src/database/queries.py:query_user",
  "relationship": "calls",
  "weight": 1.0,
  "context": "Line 45: user = query_user(username)",
  "indexed_at": "2026-05-18T14:00:00Z"
}
```

---

## Part 3: Skill Invocation Contract — `/spek.map`

### Overview

**`/spek.map`** is the skill that generates and maintains the Spekificity knowledge graph. It orchestrates:
1. Code pass (Graphify indexing)
2. Doc pass (Obsidian export)
3. Merge pass (Combine into unified graph)
4. Cache update pass (SHA256 tracking)
5. Validation pass (Schema check)

### Command Syntax

```bash
# Full rebuild (expensive; use sparingly)
/spek.map --full

# Incremental refresh (default; efficient)
/spek.map

# Refresh with watch mode (for interactive dev)
/spek.map --watch

# Obsidian export only (update docs without code re-index)
/spek.map --docs-only

# Code indexing only (don't touch Obsidian)
/spek.map --code-only

# Dry run (show what would happen without making changes)
/spek.map --dry-run

# Verbose output (debug logging)
/spek.map --verbose
```

### Invocation Lifecycle

#### 3a. Entry Point

**When called:**
```
/spek.map
├── Check if vault/graph/ exists
│   ├── If no: Initialize (create directories, config.json, empty caches)
│   └── If yes: Continue
├── Determine mode (full | incremental | watch)
└── Execute appropriate pass sequence
```

#### 3b. Full Rebuild (--full)

**Use case:** Initial setup or after major codebase restructuring.

```
/spek.map --full
├── Pass 1: Code Indexing (Graphify)
│   ├── Run: graphify . --output json --obsidian-dir vault/graph/nodes/
│   ├── Output: vault/graph/nodes-code.jsonl (all symbols)
│   ├── Generate: vault/graph/graph.json, vault/graph/graph.html, vault/graph/GRAPH_REPORT.md
│   └── Cache: Compute SHA256 for all files → vault/graph/cache/sha256.json
│
├── Pass 2: Document Indexing (Obsidian)
│   ├── Export vault/* to nodes
│   ├── Output: vault/graph/nodes-docs.jsonl (vault notes as nodes)
│   └── Link: Wikilinks become edges
│
├── Pass 3: Merge
│   ├── Read nodes-code.jsonl + nodes-docs.jsonl
│   ├── Deduplicate by (name, type, scope)
│   ├── Merge metadata (union of fields, weight by source)
│   ├── Output: vault/graph/nodes.jsonl (primary query file)
│   └── Generate: vault/graph/edges.jsonl (merged edges)
│
├── Pass 4: Index & Cache Update
│   ├── Build node-index.json (name → ID lookup)
│   ├── Update vault/graph/cache/sha256.json with all file hashes
│   └── Validate schema (all nodes have required fields)
│
├── Pass 5: Report & Validate
│   ├── Count: Total nodes, edges, communities (via clustering algorithm)
│   ├── Generate: vault/graph/GRAPH_REPORT.md (human-readable)
│   ├── Update: vault/graph/config.json (timestamp, stats)
│   └── Update: vault/graph/refresh-log.md (entry: "Full rebuild", timestamp)
│
└── Output: Success message with node/edge count
    Example: "Graph rebuilt: 423 nodes, 598 edges, 12 communities. Ready for queries."
```

**Execution time:** ~10-30 seconds (depends on codebase size).

---

#### 3c. Incremental Refresh (default)

**Use case:** Regular updates during development.

**Strategy:** SHA256 caching; only process changed files.

```
/spek.map
├── Read vault/graph/cache/sha256.json (previous hashes)
├── Scan all source files (compare SHA256)
│   ├── Unchanged: Skip (reuse cached nodes)
│   ├── Changed: Flag for re-indexing
│   └── New: Flag for indexing
│   └── Deleted: Remove from graph
│
├── Run graphify on changed files only
│   └── graphify src/auth.py src/api.py  (example: only these changed)
│
├── Merge incremental nodes with cached nodes
│   ├── Remove nodes for deleted files
│   ├── Update nodes for changed files
│   └── Add nodes for new files
│
├── Update edges (re-compute only affected edges)
│   └── Re-scan callers/callees for changed functions
│
├── Cache update
│   └── Update SHA256 for changed files
│
└── Output: Success message with delta
    Example: "Graph updated: +15 nodes, -3 nodes, ~47 edge changes. 420 total nodes."
```

**Execution time:** ~1-5 seconds (much faster than full rebuild).

---

#### 3d. Watch Mode (--watch)

**Use case:** Interactive development; auto-refresh on file save.

```
/spek.map --watch
├── Start file system watcher
├── On any file change:
│   ├── Wait debounce_ms (e.g., 1000 ms to batch changes)
│   ├── Run incremental refresh (as above)
│   ├── Update vault/graph/nodes.jsonl
│   └── Log: "Updated at 2026-05-18 14:32:15 (2 files changed)"
│
└── Continue until user stops (Ctrl+C)
```

**Benefits:** 
- Real-time graph sync during coding
- Agents always see latest codebase state
- Perfect for long-running `/spek.implement` sessions

---

#### 3e. Git Post-Commit Hook

**Configuration:** Automatic (if enable_git_hook=true in config.yaml).

**Setup:**
```bash
# During /spek.prepare, run:
graphify hook install

# This installs .git/hooks/post-commit:
#!/bin/bash
/spek.map --incremental
```

**Effect:** Graph auto-updates after each git commit (if graphify hook installed).

---

### Invocation Contracts with Other Skills

#### Contract 1: `/spek.prepare` → `/spek.map` (Graph Freshness Check)

**extracted spec `/spek.prepare` Step 3 — Check Graph Freshness:**

```
In /spek.prepare:
├── Read vault/graph/config.json → generated_at timestamp
├── Compare to current time
├── If age > graph_refresh_threshold_hours (default 1 hour):
│   ├── Offer user: "Graph is 2 hours old. Refresh? (Y/n)"
│   ├── If yes: Call /spek.map --incremental
│   └── If no: Continue with stale graph (with warning)
│
└── Result: Graph is fresh (≤1 hour old) or user accepted staleness
```

**Success criteria:**
- Graph age checked ✓
- User choice respected ✓
- /spek.map called if needed ✓

---

#### Contract 2: `/spek.automate` specify/plan phases → `/spek.map` (Context Injection)

**extracted spec & extracted spec Enriched Specify/Plan:**

```
In `/spek.automate` specify or plan phase:
├── Load vault/graph/nodes.jsonl
├── Query graph for:
│   ├── Recent changes (modified_at in last 7 days)
│   ├── Related modules (to proposed feature)
│   ├── Complexity analysis (number of nodes in affected scope)
│   └── Callers/callees (impact analysis)
│
├── Inject into prompt:
│   "Recent code changes in auth module: [list]
│    Impact analysis: [affected functions]
│    Complexity: [metric]"
│
└── Generate context-aware spec/plan
```

**Success criteria:**
- Graph queried without errors ✓
- Context injected into spec/plan ✓
- Impact analysis provided ✓

---

#### Contract 3: `/spek.post` → `/spek.map` (Incremental Graph Sync)

**extracted spec `/spek.post` Step 6 — Incremental Graph Sync:**

```
In /spek.post after implementation:
├── Get list of changed files from git diff
│   └── Example: ["src/auth.py", "src/api.py", "tests/test_auth.py"]
│
├── Run targeted graph update:
│   └── /spek.map --code-only --incremental
│      └── Only re-index changed files
│
├── Update vault/graph/nodes.jsonl
├── Log graph sync results
└── Result: Graph reflects latest implementation
```

**Success criteria:**
- Changed files identified ✓
- Graph updated for changed files only ✓
- Execution time < 5 seconds ✓

---

### Error Handling

**Scenario 1: Graphify not installed**
```
/spek.map
→ Error: graphify command not found
→ Action: Print installation instructions
   "Install Graphify: uv tool install graphifyy"
→ Exit with helpful error message
```

**Scenario 2: Corrupted cache**
```
/spek.map
→ Detect: vault/graph/cache/sha256.json corrupted
→ Action: Automatically run --full rebuild
→ Log: "Cache corrupted; performing full rebuild"
```

**Scenario 3: Graph query (in `/spek.automate` specify phase)**
```
/spek.automate
  └─ specify phase
→ Query: jq '.[] | select(.name == "authenticate")' vault/graph/nodes.jsonl
→ If no results: Continue (graph might be empty or stale)
→ Log: "Graph query found 0 matches"
```

**Scenario 4: Merge conflict (code + doc node with same name)**
```
/spek.map (merge pass)
→ Detect: node "User" exists in both code (class) and docs (decision)
→ Action: Merge with weight preference (code_node_weight: 0.7 vs doc_node_weight: 0.3)
→ Result: Single node with metadata from both sources
→ Log: "Merged nodes: code:User + doc:User → User (class, with doc context)"
```

---

## Part 4: Refresh Strategy & Performance

### Refresh Timing Strategy

| Trigger | Mode | Cost | Use Case |
|---------|------|------|----------|
| **Manual `/spek.map`** | Incremental | ~1-5s | After significant changes |
| **`/spek.prepare` check** | Incremental (if age > 1h) | ~1-5s | Start of session |
| **`/spek.post` sync** | Incremental (changed only) | ~1-5s | End of feature |
| **Git post-commit** | Incremental (if hook installed) | ~1-5s | After each commit |
| **Watch mode** | Incremental (on file save) | ~1-5s | Interactive dev session |
| **Scheduled (cron)** | Full rebuild | ~10-30s | Nightly, if desired |

---

### Performance Optimization

#### 4a. SHA256 Caching

**Mechanism:**
```
vault/graph/cache/sha256.json:
{
  "src/auth.py": "a1b2c3d4e5f6...",
  "src/api.py": "f6e5d4c3b2a1...",
  "tests/test_auth.py": "9z8y7x6w5v4u..."
}

On next /spek.map:
├── Compute SHA256 for all files
├── Compare to cache
├── If match: Skip file (use cached nodes)
└── If mismatch: Re-index file (update nodes)
```

**Impact:** 
- First run (no cache): ~30 seconds for 500 files
- Subsequent runs (95% cache hit): ~1-2 seconds

---

#### 4b. Parallel Processing

**Configuration** (in .spekificity/config.yaml):
```yaml
performance:
  parallel: true
  max_workers: 4  # Number of threads
```

**Effect:**
- 4 files indexed in parallel
- Speedup: 3-4x vs. sequential
- Impact on medium repos (100-500 files): ~5-10 seconds total

---

#### 4c. Language-Specific Optimization

**Selective Language Indexing:**
```yaml
graphify:
  generation:
    languages:
      - python        # Fast (most repos)
      - typescript    # Medium (compilation needed)
      - javascript    # Fast
      # Skip slow languages if not needed:
      # - java        # Slow (requires javac context)
      # - cpp         # Slow (requires build context)
```

**Impact:** Excluding slow languages can halve indexing time.

---

#### 4d. Node Query Efficiency (3-Layer Rule)

**Priority order for context injection:**

```
Layer 1: Query graph.json (280 tokens)
  ├── jq '.nodes | select(.name == "X")' → Fast, cached
  ├── Use for: "What functions call X?"
  └── Cost: ~280 tokens vs. 20,000 if re-reading files

Layer 2: Query Obsidian (vault)
  ├── grep vault/decision.md "related pattern"
  ├── Use for: "What decisions affect this feature?"
  └── Cost: ~500 tokens

Layer 3: Read raw code files (only if needed)
  ├── Read src/auth.py (full file)
  ├── Use for: "Exact implementation details?"
  └── Cost: ~5,000 tokens
```

**Result:** 3-layer queries reduce token usage materially versus always reading raw files.

---

### Performance Benchmarks

**Tested on 156 Python/TypeScript files (medium repo):**

| Operation | Files | Mode | Cache Hit | Time | Tokens (if queried) |
|-----------|-------|------|-----------|------|-------------------|
| Full rebuild | 156 | — | — | 28s | — |
| Incremental (1 file changed) | 156 | Incremental | 155/156 (99%) | 2s | — |
| Incremental (10 files changed) | 156 | Incremental | 146/156 (94%) | 4s | — |
| Graph query (find callers) | — | — | Cache | 0.5s | 280 tokens |
| Re-read all files | — | — | — | — | 20,000 tokens |
| Vault grep (search decisions) | — | — | Cache | 0.3s | 500 tokens |

---

## Part 5: Integration with extracted spec and extracted spec

### Integration Point 1: extracted spec (Code and Document Maps)

**extracted spec specifies the hybrid node architecture:**

```
Pass 1: Graphify indexes code
  → vault/graph/nodes-code.jsonl (pure AST nodes)

Pass 2: Obsidian export indexes docs
  → vault/graph/nodes-docs.jsonl (decision + pattern nodes)

Pass 3: Merge
  → vault/graph/nodes.jsonl (unified queryable graph)
```

**graph-setup implementation:** `/spek.map` orchestrates all three passes.

**Success criteria:**
- ✅ Code nodes merged with doc nodes
- ✅ Deduplication by (name, type, scope)
- ✅ Edges computed for both layers
- ✅ Final nodes.jsonl has both code + doc context

---

### Integration Point 2: extracted spec (Prepare and Post Skills)

**extracted spec `/spek.prepare` Step 3:**
```
Check Graph Freshness:
  ├── Read vault/graph/config.json → timestamp
  ├── Compare age to threshold (default 1 hour)
  ├── If stale: Offer refresh
  └── If yes: Call /spek.map
```

**extracted spec `/spek.post` Step 6:**
```
Incremental Graph Sync:
  ├── Get git diff (changed files)
  ├── Run /spek.map --code-only --incremental
  └── Update nodes.jsonl for changed symbols
```

**graph-setup responsibility:** Ensure `/spek.map` handles both triggered contexts.

**Success criteria:**
- ✅ `/spek.prepare` can detect stale graph
- ✅ `/spek.post` can efficiently sync changed files
- ✅ Both integrations complete in < 5 seconds

---

## Part 6: Configuration Reference

### Complete .spekificity/config.yaml (Graphify Section)

```yaml
################################################################################
# Spekificity Configuration — graph-setup Codegraph Setup
################################################################################

# Global settings (used by all skills)
global:
  vault_path: ./vault/
  log_level: info
  dry_run: false

# Graphify / Codegraph Configuration
graphify:
  # Installation & execution
  installation:
    mode: global  # "global" (uv tool) or "local" (pip in venv)
    # Path to graphify executable (if not in PATH)
    executable: null  # Auto-detect by default
  
  # Code indexing settings
  code_generation:
    # Languages to index (tree-sitter AST supported)
    languages:
      - python
      - typescript
      - javascript
      - go
      - rust
      - java
      - c
      - cpp
    
    # Exclude patterns (glob)
    exclude:
      - "node_modules/**"
      - "venv/**"
      - ".venv/**"
      - "__pycache__/**"
      - "dist/**"
      - "build/**"
      - ".git/**"
      - ".pytest_cache/**"
      - "*.egg-info/**"
      - ".mypy_cache/**"
    
    # Include hidden files?
    include_hidden: false
    
    # Max file size to index (bytes)
    max_file_size: 1000000
    
    # Complexity thresholds
    complexity:
      cyclomatic_max_warn: 10  # Warn if cyclomatic > 10
      lines_max_warn: 300      # Warn if file > 300 lines
  
  # Caching settings (for incremental updates)
  caching:
    # Enable SHA256 caching?
    enabled: true
    
    # Cache directory (relative to vault_path)
    cache_dir: graph/cache/
    
    # Cache expiry (hours; 0 = no expiry)
    expiry_hours: 0
    
    # Clear cache on startup?
    clear_on_startup: false
  
  # Output formats & locations
  output:
    # Primary output (for agent queries)
    # Options: "json", "jsonl", "markdown"
    primary_format: jsonl
    
    # Output directory (relative to vault_path)
    output_dir: graph/
    
    # Generate interactive HTML visualization?
    generate_html: true
    
    # Generate human-readable report?
    generate_report: true
    
    # Generate Obsidian-compatible notes?
    generate_obsidian_notes: true
    obsidian_notes_dir: graph/nodes/
  
  # Document indexing (Obsidian)
  document_generation:
    enabled: true
    # Obsidian vault to index
    vault_path: ./vault/
    # Include only these paths (leave empty for all)
    include_paths: []
    # Exclude patterns
    exclude_patterns:
      - "graph/**"
      - ".obsidian/**"
      - ".trash/**"
  
  # Refresh strategy
  refresh:
    # Git post-commit hook (auto-refresh after commit)
    enable_git_hook: true
    hook_mode: incremental  # "full" or "incremental"
    
    # Watch mode (auto-refresh on file save)
    enable_watch_mode: false
    watch_debounce_ms: 1000  # Wait time before re-indexing
    
    # Scheduled refresh (cron)
    enable_scheduled: false
    scheduled_time: "02:00"  # 2 AM daily
    scheduled_mode: full     # "full" or "incremental"
  
  # Performance tuning
  performance:
    # Parallel processing
    parallel_enabled: true
    max_workers: 4  # Number of threads
    
    # Verbose logging?
    verbose: false
    
    # Track timing metrics?
    track_metrics: true
  
  # Validation & quality gates
  validation:
    # Minimum node count (warn if graph has fewer)
    min_nodes_warn: 50
    
    # Enforce schema validation?
    validate_schema: true
    
    # Check for orphaned nodes?
    check_orphans: true
```

---

## Part 7: Setup Implementation Checklist

### Installation & Setup (One-Time)

- [ ] **graph-setup.1** Install Graphify via uv tool
  - Run: `uv tool install graphifyy`
  - Verify: `graphify --version`
  - Expected: graphifyy x.x.x

- [ ] **graph-setup.2** Create .spekificity/config.yaml with graphify section
  - Copy template from Part 6
  - Adjust languages, exclude patterns for your project
  - Validate YAML syntax

- [ ] **graph-setup.3** Initialize vault/graph/ directory structure
  - Create: `mkdir -p vault/graph/{nodes,cache}`
  - Create: `vault/graph/config.json` (use template from Part 2)
  - Create: `vault/graph/refresh-log.md` (empty)

- [ ] **graph-setup.4** Perform initial full graph rebuild
  - Run: `/spek.map --full`
  - Check: `vault/graph/nodes.jsonl` exists + has nodes
  - Check: `vault/graph/graph.html` can be opened in browser
  - Check: `vault/graph/GRAPH_REPORT.md` readable

- [ ] **graph-setup.5** Install git post-commit hook (optional)
  - Run: `graphify hook install`
  - Verify: `.git/hooks/post-commit` exists
  - Test: Make small commit, check graph updates

---

### Integration with extracted spec Skills

- [ ] **graph-setup.6** Integrate `/spek.prepare` graph freshness check
  - In extracted spec `/spek.prepare` Step 3 implementation:
    - Read `vault/graph/config.json` → `generated_at`
    - Calculate age in hours
    - If age > `graph_refresh_threshold_hours` (default 1): offer refresh
    - Call `/spek.map --incremental` if user accepts

- [ ] **graph-setup.7** Integrate `/spek.post` graph sync
  - In extracted spec `/spek.post` Step 6 implementation:
    - Run `git diff --name-only HEAD~1` to get changed files
    - If changed files > 0: call `/spek.map --code-only --incremental`
    - Log: "Graph synced for X changed files"

- [ ] **graph-setup.8** Integrate graph context injection (extracted spec enriched skills)
  - In `/spek.automate` specify phase:
    - Query `vault/graph/nodes.jsonl` for related modules
    - Query graph for recent changes
    - Inject into prompt: "Recent changes: [list], Related modules: [list]"
  - In `/spek.automate` plan phase:
    - Query graph for impact analysis
    - Inject: "This change affects: [list of callees/callers]"

---

### Documentation & Guides

- [ ] **graph-setup.9** Create `.spekificity/guides/graphify-setup.md` (user-facing guide)
  - Installation steps (simplified version of Part 1)
  - First-run instructions
  - Troubleshooting

- [ ] **graph-setup.10** Create `.spekificity/guides/graph-queries.md` (agent guide)
  - Example queries using jq
  - How to find modules, functions, callers
  - Common query patterns

- [ ] **graph-setup.11** Document git hook setup in `.spekificity/guides/setup.md`
  - Instructions for enabling post-commit hooks
  - How to disable/remove hooks if needed

---

### Testing & Validation

- [ ] **graph-setup.12** Functional tests for /spek.map
  - Test full rebuild: nodes.jsonl generated ✓
  - Test incremental: SHA256 cache works ✓
  - Test watch mode: File change triggers update ✓
  - Test merge: Code + doc nodes combined ✓

- [ ] **graph-setup.13** Integration tests with extracted spec skills
  - `/spek.prepare` detects stale graph ✓
  - `/spek.post` syncs changed files ✓
  - Graph context injected into specs ✓

- [ ] **graph-setup.14** Performance benchmarks
  - Full rebuild time < 30s ✓
  - Incremental < 5s ✓
  - Watch mode latency < 2s ✓
  - Query latency < 1s ✓

---

## Part 8: Troubleshooting & Recovery

### Common Issues

#### Issue: "graphify: command not found"

**Cause:** Graphify not installed or not in PATH.

**Fix:**
```bash
# Install
uv tool install graphifyy

# If still not found, verify uv tool path
which graphify
# Expected: /Users/username/.local/bin/graphify
```

---

#### Issue: "vault/graph/nodes.jsonl corrupted"

**Cause:** Invalid JSON in JSONL file.

**Fix:**
```bash
# Validate JSONL
jq . vault/graph/nodes.jsonl > /dev/null
# If error: JSONL is corrupt

# Recover
rm vault/graph/nodes.jsonl
/spek.map --full  # Rebuild
```

---

#### Issue: Graph is stale (>1 hour old) but `/spek.prepare` didn't offer refresh

**Cause:** Graph freshness threshold not set correctly.

**Fix:**
- Edit `.spekificity/config.yaml`
- Check: `graph_refresh_threshold_hours: 1` (or desired value)
- Re-run `/spek.prepare`

---

#### Issue: Watch mode consuming too much CPU

**Cause:** debounce_ms too low (files being re-indexed on every keystroke).

**Fix:**
```yaml
graphify:
  refresh:
    watch_debounce_ms: 2000  # Increase to 2 seconds
```

---

## Part 9: Success Criteria

### Graph Generation
- ✅ Full rebuild completes in < 30 seconds
- ✅ Incremental updates complete in < 5 seconds
- ✅ nodes.jsonl contains ≥50 nodes
- ✅ All nodes have required fields (id, type, name, file)
- ✅ Edges properly computed (calls, inheritance, depends-on)

### Caching & Performance
- ✅ SHA256 cache works (95%+ hit rate on unchanged files)
- ✅ Parallel processing active (4+ workers)
- ✅ Watch mode latency < 2 seconds

### Integration with extracted spec Skills
- ✅ `/spek.prepare` detects stale graph
- ✅ `/spek.post` syncs changed files efficiently
- ✅ Graph context injected into specs/plans

### Graph Query (3-Layer Rule)
- ✅ Layer 1 queries complete < 1 second
- ✅ Layer 1 queries cost ~280 tokens (vs. 20,000 if reading files)
- ✅ Fallback to Layer 2/3 if Layer 1 results empty

### Documentation & User Experience
- ✅ Setup guide clear and complete
- ✅ Troubleshooting guide covers common issues
- ✅ Git hook installation optional but documented
- ✅ Watch mode enables interactive development

---

## References

**Related specs:**
- [extracted spec Code and Document Maps](code-and-document-maps.md)
- [extracted spec Prepare and Post Skills](prepare-and-post-skills.md)
- [memory-setup claude-code-memory-setup Analysis](claude-code-memory-setup-analysis.md) (graphify patterns)

**External tools:**
- Graphify: https://github.com/graphifyy/graphifyy
- Tree-sitter: https://tree-sitter.github.io/tree-sitter/
- Obsidian Export: https://github.com/zoni/obsidian-export

**Configuration template:**
- See Part 6 for complete `.spekificity/config.yaml`

