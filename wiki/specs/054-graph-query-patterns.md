---
title: "Graph Query Patterns (C5.5)"
status: "ATOMIC SPECIFICATION"
version: "1.0.0-alpha.1"
date: "2026-05-21"
---

# ATOMIC SPECIFICATION: Graph Query Patterns (C5.5)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Usage — Querying wiki/vault/graph/ for Code Context  
**Depends On:** graph-storage-structure.md  
**Used By:** /spek.context, `/spek.plan` plan phase, enrichment layers  

---

## Overview

Query patterns for accessing `lat.md` via its CLI or MCP server (not shell grep/jq). `lat.md` exposes exploration commands and an MCP server; the spec defines an adapter-facing set of tool names that map to lat.md commands. Use the adapter or `lat mcp` for low-latency, zero-token queries.

---

## The 3-Layer Query Rule (Updated for lat.md)

```
Layer 1: MCP Tool Calls (zero tokens, low latency)
├─ Use: lat_symbols, lat_references, lat_callers, lat_definition
├─ Example: "Find all callers of function X"
└─ Cost: zero tokens; low latency

Layer 2: Built-in Impact Analysis (zero tokens, modest latency)
├─ Use: lat_impact
├─ Example: "What's the impact of changing this function?"
└─ Cost: zero tokens; modest latency

Layer 3: LLM Synthesis (LLM reasoning required)
├─ Use: Complex reasoning over multiple queries
├─ Example: "Redesign this module considering all dependencies"
└─ Cost: requires LLM reasoning and associated runtime
```

**Strategy:** Use Layer 1-2 MCP tools whenever possible; fallback to Layer 3 only for complex reasoning.

---

## Layer 1: Direct lat.md Calls (mapped via adapter)

Use lat.md CLI/MCP commands for zero-token, low-latency queries. The spec exposes adapter tool names (e.g. `lat_symbols`) which are mapped to lat.md primitives as shown below.

Mapping examples:

- `lat_symbols` → `lat section` / `lat locate` (list symbols or sections in a file/module)
- `lat_definition` → `lat section` (fetch section content / definition)
- `lat_references` → `lat refs` (find references/backlinks to a section or symbol)
- `lat_callers` / `lat_callees` → derived by graph traversal over `lat refs` results
- `lat_query` → `lat search` or `lat mcp` (free-form queries / semantic search)

Example (adapter usage):

```python
# Adapter maps spec call to lat command
symbols = adapter.call("lat_symbols", file_path="src/services/auth.py")
# adapter runs: `lat section src/services/auth.py` or queries the MCP server
```

**Use:** Discover what's defined in a file (no file reading needed).

### Tool 2: `lat_definition` — Find Symbol Definition

**Agent call:**
```python
definition = call_mcp_tool("lat_definition", symbol="authenticate", context="AuthService")
```

**Response:**
```json
{
  "file": "src/services/auth.py",
  "line": 25,
  "type": "method",
  "signature": "def authenticate(self, username: str, password: str) -> bool",
  "docstring": "Authenticate user with username/password. Returns True if valid."
}
```

**Use:** Find exact definition of a symbol without reading source file.

### Tool 3: `lat_references` — Find All References

**Agent call:**
```python
refs = call_mcp_tool("lat_references", symbol="authenticate")
```

**Response:**
```json
[
  {"file": "src/api/handlers.py", "line": 42, "context": "auth_service.authenticate(...)"},
  {"file": "src/cli/commands.py", "line": 18, "context": "await auth.authenticate(...)"},
  {"file": "tests/test_auth.py", "line": 101, "context": "assert auth.authenticate(...)"}
]
```

**Use:** Find all places a symbol is used.

### Tool 4: `lat_callers` — Find Functions Calling This Function

**Agent call:**
```python
callers = call_mcp_tool("lat_callers", symbol="query_user")
```

**Response:**
```json
[
  {"file": "src/services/auth.py", "function": "authenticate", "line": 45},
  {"file": "src/api/handlers.py", "function": "user_profile", "line": 78}
]
```

**Use:** Discover dependencies (what depends on this function).

### Tool 5: `lat_callees` — Find Functions Called By This Function

**Agent call:**
```python
callees = call_mcp_tool("lat_callees", symbol="authenticate")
```

**Response:**
```json
[
  {"file": "src/database/queries.py", "function": "find_user", "line": 26},
  {"file": "src/security/hash.py", "function": "verify_password", "line": 30}
]
```

**Use:** Understand internal dependencies of a function.

---

## Layer 2: Built-in Impact Analysis

### Tool: Impact (derived)

`lat_impact` is specified as a derived/adapter tool: compute impact by combining `lat refs`/`lat section` responses and traversing the graph (count callers, transitive callers, referenced tests/files). Lat.md does not currently advertise a dedicated `lat_impact` command; implement it in the adapter by aggregating `lat refs` results and applying heuristic risk levels.

Example (adapter call):

```python
impact = adapter.call("lat_impact", file="src/services/auth.py", symbol="authenticate")
# adapter: calls lat refs / lat section, computes direct_callers, indirect_callers, affected_files, affected_tests, and a risk_level
```

**Use:** Built-in change impact analysis (no manual scripting needed).

---

## Layer 3: Free-Form Queries (Advanced)

### Tool 7: `lat_query` — SQL-Like Index Queries

**Agent call (complex reasoning):**
```python
result = call_mcp_tool("lat_query", 
  query="find all methods in AuthService that return bool"
)
```

**Response:**
```json
[
  {"name": "authenticate", "file": "src/services/auth.py", "line": 25, "returns": "bool"},
  {"name": "is_valid_token", "file": "src/services/auth.py", "line": 52, "returns": "bool"}
]
```

**Use:** Advanced queries for complex analysis (minimal need in practice).

---

## Success Criteria

- ✅ MCP tool calls complete quickly (direct index lookups)
- ✅ Impact analysis completes promptly (built-in graph traversal)
- ✅ All queries return accurate results (verified against lat.md database)
- ✅ Layer 1-2 covers the majority of routine use cases (no LLM synthesis needed for routine queries)
- ✅ Zero shell scripting overhead (MCP tools handle complexity)
- ✅ Agent workflows use tool calls, not manual grep/jq
- ✅ Query latency remains low to support real-time context loading in `/spek.plan`

---

## Practical Workflows

### Workflow 1: Understand Code Impact Before Spec

**Agent thinking:** "What would this feature affect?"

**Code:**
```python
# 1. Query: What's in the auth module?
symbols = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")

# 2. Query: What calls authenticate()?
callers = call_mcp_tool("lat_callers", symbol="authenticate")

# 3. Query: What's the full impact?
impact = call_mcp_tool("lat_impact", file="src/services/auth.py", symbol="authenticate")

# Result: Agent knows auth changes affect 5 callers across 3 files
#         Can scope spec accurately without file reading
```

**Tokens:** 0 (all MCP calls)  
**Time:** <300ms

---

## Practical Workflows

### Workflow 1: Understand Code Impact Before Spec

**Agent thinking:** "What would this feature affect?"

**Code:**
```python
# 1. Query: What's in the auth module?
symbols = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")

# 2. Query: What calls authenticate()?
callers = call_mcp_tool("lat_callers", symbol="authenticate")

# 3. Query: What's the full impact?
impact = call_mcp_tool("lat_impact", file="src/services/auth.py", symbol="authenticate")

# Result: Agent knows auth changes affect 5 callers across 3 files
#         Can scope spec accurately without file reading
```

**Tokens:** 0 (all MCP calls)  
**Time:** <300ms

### Workflow 2: Evaluate Reuse of Existing Module

**Agent thinking:** "Should I reuse module X or create new?"

**Code:**
```python
# Check if module is mature (used by many, well-integrated)
refs = call_mcp_tool("lat_references", symbol="crypto.py:verify_hash")
impact = call_mcp_tool("lat_impact", file="src/utils/crypto.py")

# Result: If refs > 5 and risk_level is low, reuse existing module
```

**Tokens:** 0 (all MCP calls)  
**Time:** <200ms

### Workflow 3: Discover Relevant Patterns for Feature

**Agent thinking:** "What patterns apply to this feature?"

**Code:**
```python
# Query vault patterns by tag
patterns = call_mcp_tool("lat_query", query="find all nodes with type=doc and docType=pattern and tags containing api")

# Result: Returns relevant patterns for API features
```

**Tokens:** 0 (MCP call) + optional 200-500 tokens (vault reading for detail)
**Time:** <300ms (query) + <1s (vault read)

### Example 4: "Will this change break existing tests?"

**Approach:** Layer 3 (LLM synthesis)

```
Prompt: "Changed: [files]. Test files that import these: [test_files].
         Will tests break? What else should I check?"
```

**Cost:** 5-15 seconds, 1-2K tokens

---

## Query Performance

| Query | Layer | Duration | Tokens |
|-------|-------|----------|--------|
| Find all in file | 1 | < 100ms | 0 |
| Find all in class | 1 | < 100ms | 0 |
| Find all callers | 2 | 500ms | 0 |
| Find dependencies | 2 | 500ms | 0 |
| Impact analysis | 3 | 10s | 1-2K |
| Pattern lookup | 1 | < 100ms | 0 |

---

## Best Practices

**Do:**
- Use Layer 1-2 for exploration
- Batch multiple grep queries
- Cache results (Node index in memory)
- Use Layer 3 for complex reasoning

**Don't:**
- Parse nodes.jsonl with Python loops (slow)
- Load entire graph into memory (large)
- Use LLM for simple pattern matching
- Re-query same result twice (cache it)

---

## Success Criteria

✅ Layer 1 queries complete in < 100ms  
✅ Layer 2 queries complete in < 500ms  
✅ No token usage for Layer 1-2 queries  
✅ Impact analysis using Layer 3 is valuable  
✅ Agent can query efficiently during feature work  

---

## Implementation Checklist

- [ ] Document Layer 1 grep patterns
- [ ] Document Layer 2 shell patterns
- [ ] Document Layer 3 LLM synthesis
- [ ] Add examples for common queries
- [ ] Benchmark query performance
- [ ] Cache frequently accessed results

---

## References

**Related Specs:**
- [graph-storage-structure.md](graph-storage-structure.md) — nodes.jsonl, edges.jsonl schemas
- [context-layer.md](context-layer.md) — Context queries code graph
- [enrichment-layer.md](enrichment-layer.md) — Enrichment uses code graph queries

**External:**
- [graph-setup Part 5](050-latmd-setup-and-integration.md#part-5-query-patterns)
