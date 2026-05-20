# ATOMIC SPECIFICATION: CodeGraph Setup & Integration (C5.0)

**Status:** ATOMIC SPECIFICATION  
**Type:** Infrastructure — CodeGraph Installation, Configuration, and `/spek.map` Integration  
**Version:** 2026-05-20  
**Replaces:** graphify-installation.md, graphify-git-hooks.md (Graphify specs archived as legacy)  
**Depends On:** spek-map-command.md, graph-refresh-strategy.md, node-schema-design.md  
**Used By:** `/spek.prepare` (freshness check), `/spek.post` (incremental sync), `/spek.automate` (context queries)  

---

## Executive Summary

CodeGraph is Spekificity's primary code analysis tool: pre-indexed, MCP-integrated, built for agent workflows. This spec covers complete setup, integration, and refresh strategy. Graphify is legacy; unsupported for new projects.

---

## Part 1: CodeGraph Overview

### What Is CodeGraph?

**CodeGraph** is a semantic code indexing tool that:
- **Indexes** source code via AST (Abstract Syntax Tree) parsing
- **Generates** queryable knowledge graphs (SQLite + MCP tools)
- **Supports** 20+ languages natively
- **Provides** MCP tool interface (agent-friendly API)
- **Includes** built-in impact analysis (callers, callees, dependencies)
- **Maintains** real-time sync (file watcher + incremental updates)
- **Scales** to large codebases (100K+ symbols)

**Key Advantage:** Pre-indexed queries return results in ~100ms (vs. file scans at 1-5s per file).

---

## Part 2: Installation & Configuration

### Prerequisites

```bash
# Check Python
python3 --version
# Expected: 3.11+

# Check Node.js (CodeGraph runtime)
node --version
# Expected: 18.0+

# Check MCP client (VS Code Copilot integration)
# Built-in; no separate install needed
```

**If missing:**
```bash
# macOS
brew install python@3.11 node@20

# Linux (Ubuntu)
sudo apt install python3.11 python3-pip nodejs

# Verify
python3 --version && node --version
```

---

### Step 1: Install CodeGraph via npm

```bash
# Install globally (recommended)
npm install -g @codegraph/cli

# Verify
codegraph --version
# Expected: 1.0.0+ (as of 2026-05-20)

codegraph --help
# Expected: Help output with commands
```

**Alternative: Local Installation (per-project)**
```bash
# In project root
npm install --save-dev @codegraph/cli

# Invoke via npx
npx codegraph --version
```

**Recommendation:** Global install for easier `/spek.map` integration.

---

### Step 2: Create CodeGraph Configuration

Create `.spekificity/config.yaml`:

```yaml
# CodeGraph Configuration for Spekificity

project_name: "spekificity"
project_root: "."

# Code Indexing
code_indexing:
  enabled: true
  
  # Languages to index
  languages:
    - python
    - typescript
    - javascript
    - yaml
    - markdown
  
  # Paths to index
  include_paths:
    - src/
    - lib/
    - bin/
    - .spekificity/
  
  # Paths to exclude
  exclude_paths:
    - node_modules/
    - .git/
    - __pycache__/
    - "*.min.js"
    - dist/
    - build/
  
  # AST parsing options
  parse_options:
    skip_comments: false
    extract_docstrings: true
    extract_types: true

# Documentation Indexing
doc_indexing:
  enabled: true
  
  # Obsidian vault integration
  vault_path: "vault/"
  
  # Markdown files to index
  include_patterns:
    - "**/*.md"
  
  # Parse frontmatter + headings
  parse_frontmatter: true
  parse_headings: true
  
  # Extract wikilinks
  extract_wikilinks: true

# Graph Storage
graph_storage:
  # SQLite database location
  database_path: "vault/graph/codegraph.db"
  
  # Query cache (for fast repeated queries)
  cache_enabled: true
  cache_path: "vault/graph/cache/"
  cache_ttl_seconds: 3600  # 1 hour
  
  # Incremental refresh
  use_file_hashing: true
  hash_method: sha256

# Refresh Strategy
refresh_strategy:
  # Automatic triggers
  auto_refresh_on_git_commit: true
  auto_refresh_interval_seconds: 3600  # 1 hour if no git activity
  
  # Watch mode (for dev)
  watch_enabled: true
  watch_debounce_ms: 500  # Wait 500ms after last change before syncing
  
  # Performance tuning
  parallel_workers: 4  # Thread pool size
  batch_size: 100  # Process 100 files per batch

# Query Configuration
query_config:
  # 3-layer query rule (token efficiency)
  max_results_per_query: 50
  include_call_graph: true
  include_dependency_graph: true
  include_type_hierarchy: true
  
  # AI agent context
  include_recent_changes: true
  recent_changes_window_days: 7

# MCP Integration
mcp:
  enabled: true
  
  # Available MCP tools (agent can call these)
  tools:
    - codegraph_symbols        # List all symbols in file
    - codegraph_definition     # Find where symbol is defined
    - codegraph_references     # Find all references to symbol
    - codegraph_callers        # Find functions calling this function
    - codegraph_callees        # Find functions called by this function
    - codegraph_impact         # Estimate impact radius of change
    - codegraph_query          # Free-form graph query (SQL-like)
  
  # Tool timeout (prevent agent from hanging)
  tool_timeout_seconds: 5

# Logging & Debug
logging:
  level: info  # debug|info|warning|error
  output: console  # console|file|both
  log_file: ".spekificity/logs/codegraph.log"

# Validation
validation:
  # Run checks after each sync
  check_consistency: true
  check_orphaned_nodes: true  # Warn if symbols defined but never referenced
  check_import_cycles: true   # Warn about circular dependencies
```

---

### Step 3: Initialize CodeGraph Database

```bash
# In project root
codegraph init --config .spekificity/config.yaml

# Output:
# ✓ Created vault/graph/codegraph.db (SQLite)
# ✓ Created vault/graph/cache/ (query cache)
# ✓ Created vault/graph/config.json (metadata)
# ✓ Configuration validated

# Verify initialization
ls -la vault/graph/
# Expected: codegraph.db, cache/, config.json
```

---

### Step 4: Initial Full Index Build

```bash
# Full rebuild (first time)
codegraph index --full

# Output:
# Parsing files...
#   Python: 45 files
#   TypeScript: 12 files
#   Markdown: 38 files
# Total: 95 files processed
#
# Building graph...
#   Symbols indexed: 2,847
#   References indexed: 12,450
#   Dependencies indexed: 1,203
#
# Validation...
#   ✓ Consistency check passed
#   ✓ No orphaned nodes
#   ✓ Circular dependencies: 3 (acceptable)
#
# Graph built: vault/graph/codegraph.db (12.4 MB)
# Time: 47 seconds
```

**First build takes 30-60 seconds (language-dependent). Subsequent incremental builds: 2-5 seconds.**

---

### Step 5: Configure Git Hook (Optional Auto-Sync)

Create `.git/hooks/post-commit`:

```bash
#!/bin/bash
# Auto-sync code graph after each commit

set -e

# Get changed files from git
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

# Invoke CodeGraph incremental sync
codegraph index --incremental --config .spekificity/config.yaml

# Exit silently (don't block commit)
exit 0
```

**Make executable:**
```bash
chmod +x .git/hooks/post-commit
```

**Disable hook (if needed):**
```bash
# Set environment variable
export CODEGRAPH_SKIP_HOOKS=1
git commit -m "..."
```

---

## Part 3: `/spek.map` Command Integration

`/spek.map` orchestrates CodeGraph operations:

```bash
spek map [mode] [options]
  --full          # Full rebuild (5-10 minutes)
  --incremental   # Sync only changed files (2-5 seconds, default)
  --watch         # Watch mode (auto-sync on file changes)
  --query         # Query graph (interactive)
  --validate      # Run consistency checks
  --verbose       # Debug output
```

### Mode 1: Full Rebuild (Force)

```bash
spek map --full

# Execution:
# 1. Drop existing codegraph.db
# 2. Rebuild from scratch (all files)
# 3. Re-index documentation
# 4. Validate consistency
# 5. Report: symbols indexed, dependencies found, time elapsed

# Use case: After major refactoring or graph corruption
# Time: 5-10 minutes
```

### Mode 2: Incremental Sync (Default)

```bash
spek map --incremental

# Execution:
# 1. Run: git diff --name-only HEAD~1..HEAD
# 2. Hash changed files (SHA256)
# 3. Re-index only changed files
# 4. Update graph edges (remove old, add new)
# 5. Validate: no broken references
# 6. Report: files processed, changes merged, time elapsed

# Use case: Normal workflow (called by /spek.prepare, /spek.post)
# Time: 2-5 seconds
```

### Mode 3: Watch Mode (Dev Workflow)

```bash
spek map --watch

# Execution (continuous):
# 1. Start file watcher (all indexed paths)
# 2. Debounce changes (500ms)
# 3. On file change: incremental sync
# 4. Report: "Graph updated (N files changed)"
# 5. Continue watching...

# Use case: Interactive development (optional)
# Runs in foreground; kill with Ctrl+C
```

---

## Part 4: MCP Tool Interface (Agent Queries)

Agents query CodeGraph via MCP tools:

### Tool 1: `codegraph_symbols`

**Purpose:** List all symbols in a file or module

```
Input: file_path = "src/services/auth.py"
Output: [
  { id: "1", name: "AuthService", type: "class", line: 12 },
  { id: "2", name: "authenticate", type: "method", line: 25, parent: "AuthService" },
  { id: "3", name: "refresh_token", type: "method", line: 45, parent: "AuthService" }
]
```

### Tool 2: `codegraph_definition`

**Purpose:** Find where a symbol is defined

```
Input: symbol = "authenticate", context = "AuthService"
Output: {
  file: "src/services/auth.py",
  line: 25,
  type: "method",
  signature: "def authenticate(self, username, password) -> bool"
}
```

### Tool 3: `codegraph_references`

**Purpose:** Find all references to a symbol

```
Input: symbol = "authenticate"
Output: [
  { file: "src/api/handlers.py", line: 42, context: "auth_service.authenticate(...)" },
  { file: "src/cli/commands.py", line: 18, context: "await auth.authenticate(...)" },
  { file: "tests/test_auth.py", line: 101, context: "assert auth.authenticate(...)" }
]
```

### Tool 4: `codegraph_callers`

**Purpose:** Find functions calling this function

```
Input: symbol = "authenticate"
Output: [
  { file: "src/api/handlers.py", function: "login_handler", line: 42 },
  { file: "src/cli/commands.py", function: "cli_login", line: 18 }
]
```

### Tool 5: `codegraph_callees`

**Purpose:** Find functions called by this function

```
Input: symbol = "authenticate"
Output: [
  { file: "src/database/queries.py", function: "find_user", line: 26 },
  { file: "src/security/hash.py", function: "verify_password", line: 30 }
]
```

### Tool 6: `codegraph_impact`

**Purpose:** Estimate change impact radius

```
Input: file = "src/services/auth.py", modified_symbol = "authenticate"
Output: {
  direct_callers: 2,
  indirect_callers: 5,
  affected_tests: 8,
  affected_files: 3,
  risk_level: "medium",
  recommendation: "Test affected_tests/ files before merge"
}
```

### Tool 7: `codegraph_query`

**Purpose:** Free-form graph queries (SQL-like)

```
Input: query = "find all methods in AuthService that return bool"
Output: [
  { name: "authenticate", line: 25, returns: "bool" },
  { name: "is_valid_token", line: 52, returns: "bool" }
]
```

---

## Part 5: Context Injection into Agent Workflows

### During `/spek.automate` Specify Phase

```
Agent is writing specification...

1. Query graph: "recent changes to auth module" (codegraph_query)
   → Returns: [auth.py modified 2 days ago, 3 functions added]

2. Context injected: "Note: auth.py recently changed (3 new functions added)"
   → Spec generation considers recent changes

3. Agent writes specification accounting for recent code state
```

### During `/spek.automate` Plan Phase

```
Agent is writing plan...

1. Query graph: "impact of adding new validator pattern" (codegraph_impact simulation)
   → Returns: 12 affected functions, 5 test files

2. Context injected: "Consider: Validation change affects 12 functions, 5 test files"
   → Plan includes scope awareness

3. Agent plans implementation path considering impact radius
```

### During `/spek.implement` Task Execution

```
Agent executes task: "Refactor auth service"

1. Pre-execution query: "what calls authenticate()?" (codegraph_callers)
   → Returns: [handlers.py, commands.py, 3 test files]

2. Context injected: "Callers found in: handlers.py, commands.py, tests/"
   → Agent is aware of breaking change risk

3. Agent executes task with knowledge of dependencies
   → Lower risk of silent breaking changes
```

---

## Part 6: Performance & Optimization

### Query Performance Baseline

| Query Type | Avg Time | Token Cost |
|-----------|----------|-----------|
| `codegraph_symbols` (single file) | 50ms | ~50 tokens |
| `codegraph_references` (100 refs) | 150ms | ~100 tokens |
| `codegraph_callers` (10 callers) | 80ms | ~50 tokens |
| `codegraph_impact` (full analysis) | 300ms | ~200 tokens |
| File scan (same info) | 2000ms | ~2000 tokens |

**Token Savings:** 20x reduction vs. file scanning.

### Caching Strategy

```yaml
cache:
  query_results: 3600 seconds (1 hour)
  symbol_definitions: 3600 seconds
  reference_lists: 1800 seconds (30 min)
  recent_changes: 300 seconds (5 min)
```

### Parallel Processing

```yaml
indexing:
  workers: 4  # Thread pool
  batch_size: 100  # Files per batch
  
Result: 4x speedup on large codebases
```

---

## Part 7: Success Criteria

✅ CodeGraph installed globally (npm)  
✅ Configuration created (.spekificity/config.yaml)  
✅ Initial index built (codegraph.db exists, 2K+ symbols)  
✅ Git hook installed (optional, auto-sync working)  
✅ `/spek.map --full` completes successfully  
✅ `/spek.map --incremental` syncs in <5 seconds  
✅ MCP tools callable (agent can query graph)  
✅ Context injection working (decisions/patterns loaded pre-spec)  
✅ Query performance <500ms per query  

---

## Part 8: Troubleshooting

| Issue | Symptom | Fix |
|-------|---------|-----|
| CodeGraph not found | "command not found: codegraph" | `npm install -g @codegraph/cli` |
| DB corruption | "SQLite database is locked" | `rm vault/graph/codegraph.db && spek map --full` |
| Stale graph | Queries return old symbols | `spek map --full` (rebuild) |
| High CPU | `codegraph index` consuming 100% CPU | Reduce `parallel_workers` in config.yaml |
| Watch mode not syncing | Files modified but not indexed | Check `watch_debounce_ms`, increase to 1000 |
| MCP tool timeout | "Tool query exceeded 5s timeout" | Increase `tool_timeout_seconds` in config |

---

## Part 9: Integration Checklist

- [ ] CodeGraph installed + verified (npm list @codegraph/cli)
- [ ] Configuration file created (.spekificity/config.yaml)
- [ ] Initial index built (vault/graph/codegraph.db exists)
- [ ] Git hook installed + tested
- [ ] `/spek.map --full` tested (successful rebuild)
- [ ] `/spek.map --incremental` tested (<5s runtime)
- [ ] MCP tools callable (VS Code integration verified)
- [ ] `/spek.prepare` freshness check working
- [ ] `/spek.post` incremental sync working
- [ ] `/spek.automate` context queries working
- [ ] Performance benchmarks met (queries <500ms)
- [ ] Documentation updated (agent guide + user guide)

---

## Related Specifications

- [/spek.map Command](spek-map-command.md) — Orchestration of graph operations
- [Graph Refresh Strategy](graph-refresh-strategy.md) — Incremental sync + caching
- [Node Schema Design](node-schema-design.md) — Database schema
- [Enrichment Layer](enrichment-layer.md) — Context injection into agent workflows
- [Memory Architecture](memory-architecture.md) — Query lifecycle + token costs
