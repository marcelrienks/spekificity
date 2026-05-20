# Graphify Setup Guide

**Companion to:** [obsidian-setup.md](obsidian-setup.md), [speckit-setup.md](speckit-setup.md)

**Status:** legacy / transition reference. [wiki/decision.md](../decision.md) recommends **CodeGraph** as the primary code analysis tool for Spekificity. Keep this guide for teams that explicitly choose Graphify or need a simpler interim setup until dedicated CodeGraph setup docs are written.

This guide walks through installing and configuring Graphify (code graph indexing) for Spekificity.

---

## What is Graphify?

**Graphify** (pip: `graphifyy`) is a multi-language code indexing tool that builds a searchable knowledge graph from your codebase using tree-sitter AST (Abstract Syntax Tree).

**What it does:**
- Indexes Python, TypeScript, JavaScript, Go, Rust, Java, C, C++ (20+ languages)
- Generates queryable graph of functions, classes, modules, and their relationships
- Supports incremental updates with SHA256 caching (only re-indexes changed files)
- Outputs multiple formats: JSON (queryable), HTML (interactive visualization), JSONL (agent-readable)
- Integrates with git hooks for automatic refresh on commits

**Why some Spekificity setups still use it:**
- Context injection: Recent code changes inform feature specifications
- Impact analysis: Understand which modules are affected by changes
- Token efficiency: 3-layer query strategy (graph → vault → code) reduces tokens by 20x

**Primary recommendation:** If you are following the current baseline tool decisions, prefer CodeGraph for day-to-day agent workflows and treat Graphify as fallback or migration path.

---

## Installation

### Prerequisites

Check your Python version:
```bash
python3 --version
# Expected: 3.11 or higher
```

If needed, install Python 3.11+:
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Windows (via WSL)
sudo apt-get install python3.11
```

### Install Graphify

```bash
# Recommended: via uv (fast, isolated)
uv tool install graphifyy

# Verify installation
graphify --version
# Expected output: graphifyy x.x.x
```

**Alternative: pip**
```bash
pip install graphifyy
```

---

## Configuration

### Create .spekificity/config.yaml

Copy this template into your `.spekificity/config.yaml` file:

```yaml
# Graphify Configuration Section
graphify:
  installation:
    mode: global  # "global" = uv tool; "local" = pip in venv
  
  code_generation:
    # Languages to index
    languages:
      - python
      - typescript
      - javascript
      - go
      - rust
    
    # Patterns to exclude
    exclude:
      - "node_modules/**"
      - "venv/**"
      - ".venv/**"
      - "__pycache__/**"
      - "dist/**"
      - "build/**"
      - ".git/**"
  
  caching:
    enabled: true
    cache_dir: graph/cache/
  
  output:
    primary_format: jsonl
    generate_html: true
  
  refresh:
    enable_git_hook: true
    watch_debounce_ms: 1000
  
  performance:
    parallel_enabled: true
    max_workers: 4
```

---

## First-Run Setup

### 1. Initialize Vault Graph Directory

```bash
mkdir -p vault/graph/nodes
mkdir -p vault/graph/cache
```

### 2. Run Initial Full Build

```bash
graphify . --output jsonl --obsidian-dir vault/graph/nodes/
```

This generates:
- `vault/graph/nodes.jsonl` — Main queryable graph
- `vault/graph/graph.json` — Full graph structure
- `vault/graph/graph.html` — Interactive visualization (open in browser)
- `vault/graph/GRAPH_REPORT.md` — Human-readable summary

### 3. Verify Graph Generated

```bash
# Check if nodes exist
wc -l vault/graph/nodes.jsonl
# Expected: 50+ lines (depends on codebase size)

# View summary
cat vault/graph/GRAPH_REPORT.md
```

---

## Git Hook Setup (Optional But Recommended)

Auto-refresh the graph on every commit:

```bash
graphify hook install
```

This installs `.git/hooks/post-commit` that runs `graphify . --update` after each commit.

**Verify installation:**
```bash
cat .git/hooks/post-commit
# Expected: Contains "graphify . --update"
```

**To disable later:**
```bash
rm .git/hooks/post-commit
```

---

## Usage

### Manual Refresh

```bash
# Incremental refresh (only changed files)
graphify .

# Full rebuild (expensive, rarely needed)
graphify . --full

# Watch mode (auto-refresh on file save)
graphify . --watch

# Dry-run (see what would change)
graphify . --dry-run
```

### Querying the Graph

Query the generated graph using `jq`:

```bash
# Find all functions named "authenticate"
jq '.[] | select(.name == "authenticate")' vault/graph/nodes.jsonl

# Find all callers of a function
jq '.[] | select(.callers[] | contains("login_handler"))' vault/graph/nodes.jsonl

# Count total nodes
jq 'length' vault/graph/nodes.jsonl
```

---

## Troubleshooting

### "graphify: command not found"

**Cause:** Graphify not installed or not in PATH.

**Fix:**
```bash
# Install
uv tool install graphifyy

# Verify PATH
which graphify

# If not found, add to PATH (macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"
```

---

### Graph seems stale (dates are old)

**Cause:** Graph wasn't rebuilt after code changes.

**Fix:**
```bash
# Manual refresh
graphify . --update

# Or check if git hook is installed
cat .git/hooks/post-commit | grep graphify
```

---

### High CPU usage during indexing

**Cause:** Large codebase or slow machine.

**Fix:**
- Reduce parallel workers in `.spekificity/config.yaml`:
  ```yaml
  performance:
    max_workers: 2  # Default is 4
  ```

- Exclude slow/unnecessary directories:
  ```yaml
  exclude:
    - "node_modules/**"
    - ".git/**"
    - "build/**"
  ```

---

### "nodes.jsonl corrupted"

**Cause:** Invalid JSON in graph file.

**Fix:**
```bash
# Validate
jq . vault/graph/nodes.jsonl > /dev/null
# If error: file is corrupt

# Recover
rm vault/graph/nodes.jsonl
graphify . --full  # Full rebuild
```

---

## Integration with Spekificity

### How Graph is Used

**In `/spek.prepare`:**
- Graph freshness check (Step 3)
- If >1 hour old, offers refresh

**In `/spek.post`:**
- Incremental sync for changed files (Step 6)
- Graph updated with new/modified symbols

**In `/spek.automate` specify/plan phases:**
- Recent changes injected into specs
- Impact analysis provided
- Related modules identified

### 3-Layer Query Rule

Context queries follow this priority:

```
1. Query graph (fast, indexed, 280 tokens)
   └─ If empty:
   
2. Query vault (searchable, 500 tokens)
   └─ If empty:
   
3. Read code files (expensive, 5000+ tokens)
```

This strategy saves ~20x tokens per session.

---

## Performance Reference

On a medium codebase (156 Python/TypeScript files):

| Operation | Time | Cache Hit |
|-----------|------|-----------|
| Full rebuild | ~28 seconds | — |
| Incremental (1 file changed) | ~2 seconds | 99% |
| Incremental (10 files changed) | ~4 seconds | 94% |
| Graph query (find callers) | ~0.5 seconds | Indexed |

---

## Next Steps

1. ✅ Install Graphify (`uv tool install graphifyy`)
2. ✅ Initialize vault/graph/ directory
3. ✅ Configure .spekificity/config.yaml
4. ✅ Run initial full build (`graphify .`)
5. ✅ (Optional) Install git hook (`graphify hook install`)
6. ✅ Verify graph generation (`cat vault/graph/GRAPH_REPORT.md`)

Once complete, the graph will automatically update and support Spekificity's context injection workflow.

---

## See Also

- [obsidian-setup.md](obsidian-setup.md) — Vault setup
- [speckit-setup.md](speckit-setup.md) — SpecKit installation
- [../specs/b11-codegraph-setup-and-integration.md](../specs/b11-codegraph-setup-and-integration.md) — Complete technical specification
