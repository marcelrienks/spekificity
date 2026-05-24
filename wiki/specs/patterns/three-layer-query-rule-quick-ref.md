# Three-Layer Query Rule — Quick Reference

**Category:** Query  
**Problem:** Agent queries cost tokens; naive approach reads all files (expensive)  
**Solution:** Tier queries by cost; use Layer 1-2 for the majority of cases
**Used in:** Context loading, `/spek.context`, code graph queries  

---

## What It Is

Hierarchical query strategy that prioritizes efficiency:

```
QUERY HIERARCHY (lat.md-Based)

Layer 1: lat.md MCP Tools (FAST, LOW-COST)
├─ Cost: low
├─ Latency: low-latency
├─ Query: MCP tool calls (lat_symbols, lat_references, lat_callers, etc.)
├─ Examples:
│  - "Who calls function X?" → lat_callers
│  - "What does module Y depend on?" → lat_callees
│  - "Find all classes in file Z" → lat_symbols
└─ Success rate: high for common structural queries

Layer 2: Vault/Decisions (MEDIUM COST)
├─ Cost: moderate
├─ Latency: moderate-latency
├─ Query: grep + jq on vault files (decisions, patterns)
├─ Examples:
│  - "What decisions affect authentication?"
│  - "What patterns exist for error handling?"
│  - "Find recent lessons about caching"
└─ Success rate: good for metadata and decision queries

Layer 3: Raw Code Files (HIGHER COST)
├─ Cost: higher
├─ Latency: higher-latency
├─ Query: Read entire files, AI synthesis
├─ Examples:
│  - "Explain this complex algorithm"
│  - "Find all edge cases in function X"
│  - "What's the performance bottleneck?"
└─ Success rate: comprehensive when full context is required

RULE: Use Layer 1 → Layer 2 → Layer 3
Only escalate when necessary.
```

---

## Why Use It

- ✅ Token savings (Layer 1-2 handle the majority of common queries)
- ✅ Speed (Layer 1 queries are low-latency)
- ✅ Scalability (multiple features per session)
- ✅ Fallback (if Layer 1 fails, try Layer 2)
- ✅ Measurable (cost breakdown visible)

---

## When to Use

✅ Large codebases (token savings material)  
✅ Context-loading phases (minimize costs)  
✅ Multiple features per session (budget constraints)  
✅ Production deployments (cost optimization needed)  

❌ Small codebases (overhead not worth it)  
❌ One-time queries (Layer 1 setup overhead)  
❌ Complex reasoning (Layer 3 simpler for some queries)  

---

## Layer 1: lat.md MCP Tools

**Setup:**
```
lat.md indexing active. Access via MCP tool calls.
Built-in tools available: lat_symbols, lat_definition, 
lat_references, lat_callers, lat_callees, lat_impact, lat_query
```

**Examples (MCP tool calls):**

```python
# Query 1: Find all symbols in a file
symbols = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")
# Returns: [AuthService, authenticate, refresh_token, ...]

# Query 2: Find all callers of a function
callers = call_mcp_tool("lat_callers", symbol="authenticate")
# Returns: [handlers.login_handler, commands.cli_login, ...]

# Query 3: Find all references to a symbol
refs = call_mcp_tool("lat_references", symbol="authenticate")
# Returns: [handlers.py:42, commands.py:18, tests/test_auth.py:101]

# Query 4: Find definition of symbol
definition = call_mcp_tool("lat_definition", symbol="authenticate", context="AuthService")
# Returns: {file: "src/services/auth.py", line: 25, signature: "def authenticate(...)"}

# Query 5: Find what this function calls (dependencies)
callees = call_mcp_tool("lat_callees", symbol="authenticate")
# Returns: [database.query_user, security.verify_password, ...]

# Query 6: Estimate change impact
impact = call_mcp_tool("lat_impact", file="src/services/auth.py", symbol="authenticate")
# Returns: {direct_callers: 2, indirect_callers: 5, affected_tests: 8, risk_level: "medium"}

# Query 7: Custom graph query (advanced)
result = call_mcp_tool("lat_query", query="find all methods returning bool")
# Returns: [authenticate(...), is_valid_token(...), ...]
```

**Cost:** low per query

---

## Layer 2: Vault/Decisions Queries

**Setup:**
```bash
# Vault files pre-indexed (decisions, patterns, lessons)
# Search via grep + jq
```

**Examples:**

```bash
# Query 1: Find decisions by keyword
grep -i "authentication" vault/decision.md

# Query 2: Find patterns by tag
grep '"tags".*"pattern/caching"' vault/patterns.md

# Query 3: Find recent lessons
ls -t vault/lessons/*.md | head -5

# Query 4: Find lessons mentioning a pattern
grep -l "dependency-injection" vault/lessons/*.md | head -3

# Query 5: Extract decision metadata
grep -A 3 "title: \"Singleton Pattern\"" vault/decision.md
```

**Cost:** moderate (metadata + search results)

---

## Layer 3: Raw Code Files

**When to use:**
- Layer 1-2 insufficient for query
- Complex reasoning needed (algorithm explanation)
- Semantic search required (not keyword-based)

**Example:**
```bash
# Read entire file(s) for AI analysis
cat src/complex-algorithm.py | \
wc -l  # Check size first (avoid huge files)

# If small: read and send to LLM
# If large: break into sections, query one at a time
```

**Cost:** higher per file (more than Layer 1)

---

## Escalation Logic

```python
def query_with_escalation(query_text):
    """Execute query with Layer 1 → 2 → 3 escalation"""
    
    # Try Layer 1: Code graph
    try:
        results = layer1_query(query_text)  # grep + jq
        if results:
            return results
        # Fall through if no results
    except Exception as e:
        log_debug(f"Layer 1 failed: {e}")
    
    # Try Layer 2: Vault/decisions
    try:
        results = layer2_query(query_text)  # grep on vault
        if results:
            return results
        # Fall through if no results
    except Exception as e:
        log_debug(f"Layer 2 failed: {e}")
    
    # Fall back to Layer 3: Raw code files
    try:
        results = layer3_query(query_text)  # Read files + AI
        return results
    except Exception as e:
        log_error(f"Layer 3 failed: {e}")
        raise
```

---

## Related Patterns

- **Code Graph Query** — Layer 1 queries
- **Hybrid Graph** — Code graph data structure
- **Context Injection** — Uses this rule to load context efficiently

---

## Where It's Used

- **Primary:** [3layer-query-rule.md](../specs/3layer-query-rule.md)
- **Applied in:**
  - [graph-query-patterns.md](../specs/graph-query-patterns.md)
  - [context-layer.md](../specs/context-layer.md)
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md)

---

## Quick Checklist

- [ ] Code graph pre-indexed (Layer 1 ready)?
- [ ] Vault searchable (Layer 2 ready)?
- [ ] Query tries Layer 1 first?
- [ ] Fallback to Layer 2 if Layer 1 empty?
- [ ] Fallback to Layer 3 only if 1-2 insufficient?
- [ ] Token cost tracked per layer?
- [ ] Performance targets met (Layer 1 low latency)?

---

## Notes on Resource Use

- Layer 1 is typically the most efficient for structural queries; Layer 2 suits metadata and decision queries; Layer 3 is for full-file analysis when necessary.

Avoid embedding fixed numeric budgets in public docs; teams should configure per-project limits in configuration files.
