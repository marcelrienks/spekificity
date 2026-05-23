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

Query patterns for accessing CodeGraph via **MCP tools** (not shell grep/jq). CodeGraph exposes 7 primary MCP tools for agent queries with zero token cost and <500ms latency.

---

## The 3-Layer Query Rule (Updated for CodeGraph)

```
Layer 1: MCP Tool Calls (0 tokens, <100ms)
├─ Use: codegraph_symbols, codegraph_references, codegraph_callers, codegraph_definition
├─ Example: "Find all callers of function X"
└─ Cost: 0 tokens, <100ms latency

Layer 2: Built-in Impact Analysis (0 tokens, <500ms)
├─ Use: codegraph_impact
├─ Example: "What's the impact of changing this function?"
└─ Cost: 0 tokens, <500ms latency

Layer 3: LLM Synthesis (1-2K tokens, 5-15s)
├─ Use: Complex reasoning over multiple queries
├─ Example: "Redesign this module considering all dependencies"
└─ Cost: 1-2K tokens, requires LLM reasoning
```

**Strategy:** Use Layer 1-2 MCP tools whenever possible; fallback to Layer 3 only for complex reasoning.

---

## Layer 1: Direct MCP Tool Calls

Agents call MCP tools directly. CodeGraph returns structured data (not text files).

### Tool 1: `codegraph_symbols` — List All Symbols in File

**Agent call:**
```python
symbols = call_mcp_tool("codegraph_symbols", file_path="src/services/auth.py")
```

**Response:**
```json
[
  {"name": "AuthService", "type": "class", "line": 12},
  {"name": "authenticate", "type": "method", "line": 25, "parent": "AuthService"},
  {"name": "refresh_token", "type": "method", "line": 45, "parent": "AuthService"}
]
```

**Use:** Discover what's defined in a file (no file reading needed).

### Tool 2: `codegraph_definition` — Find Symbol Definition

**Agent call:**
```python
definition = call_mcp_tool("codegraph_definition", symbol="authenticate", context="AuthService")
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

### Tool 3: `codegraph_references` — Find All References

**Agent call:**
```python
refs = call_mcp_tool("codegraph_references", symbol="authenticate")
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

### Tool 4: `codegraph_callers` — Find Functions Calling This Function

**Agent call:**
```python
callers = call_mcp_tool("codegraph_callers", symbol="query_user")
```

**Response:**
```json
[
  {"file": "src/services/auth.py", "function": "authenticate", "line": 45},
  {"file": "src/api/handlers.py", "function": "user_profile", "line": 78}
]
```

**Use:** Discover dependencies (what depends on this function).

### Tool 5: `codegraph_callees` — Find Functions Called By This Function

**Agent call:**
```python
callees = call_mcp_tool("codegraph_callees", symbol="authenticate")
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

### Tool 6: `codegraph_impact` — Estimate Change Impact

**Agent call:**
```python
impact = call_mcp_tool("codegraph_impact", file="src/services/auth.py", symbol="authenticate")
```

**Response:**
```json
{
  "direct_callers": 2,
  "indirect_callers": 5,
  "affected_files": 3,
  "affected_tests": 8,
  "risk_level": "medium",
  "recommendation": "Run tests in tests/test_auth.py and tests/test_api.py before merge",
  "affected_modules": ["src/api/handlers.py", "src/cli/commands.py"],
  "estimated_scope": "Small change; affects auth+API layer"
}
```

**Use:** Built-in change impact analysis (no manual scripting needed).

---

## Layer 3: Free-Form Queries (Advanced)

### Tool 7: `codegraph_query` — SQL-Like Graph Queries

**Agent call (complex reasoning):**
```python
result = call_mcp_tool("codegraph_query", 
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

- ✅ MCP tool calls complete in <100ms (direct index lookups)
- ✅ Impact analysis completes in <500ms (built-in graph traversal)
- ✅ All queries return accurate results (verified against CodeGraph database)
- ✅ Layer 1-2 covers 95%+ of use cases (no LLM synthesis needed for routine queries)
- ✅ Zero shell scripting overhead (MCP tools handle complexity)
- ✅ Agent workflows use tool calls, not manual grep/jq
- ✅ Query latency <500ms (supports real-time context loading in `/spek.plan`)

---

## Practical Workflows

### Workflow 1: Understand Code Impact Before Spec

**Agent thinking:** "What would this feature affect?"

**Code:**
```python
# 1. Query: What's in the auth module?
symbols = call_mcp_tool("codegraph_symbols", file_path="src/services/auth.py")

# 2. Query: What calls authenticate()?
callers = call_mcp_tool("codegraph_callers", symbol="authenticate")

# 3. Query: What's the full impact?
impact = call_mcp_tool("codegraph_impact", file="src/services/auth.py", symbol="authenticate")

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
symbols = call_mcp_tool("codegraph_symbols", file_path="src/services/auth.py")

# 2. Query: What calls authenticate()?
callers = call_mcp_tool("codegraph_callers", symbol="authenticate")

# 3. Query: What's the full impact?
impact = call_mcp_tool("codegraph_impact", file="src/services/auth.py", symbol="authenticate")

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
refs = call_mcp_tool("codegraph_references", symbol="crypto.py:verify_hash")
impact = call_mcp_tool("codegraph_impact", file="src/utils/crypto.py")

# Result: If refs > 5 and risk_level is low, reuse existing module
```

**Tokens:** 0 (all MCP calls)  
**Time:** <200ms

### Workflow 3: Discover Relevant Patterns for Feature

**Agent thinking:** "What patterns apply to this feature?"

**Code:**
```python
# Query vault patterns by tag
patterns = call_mcp_tool("codegraph_query", query="find all nodes with type=doc and docType=pattern and tags containing api")

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
- [graph-setup Part 5](codegraph-setup-and-integration.md#part-5-query-patterns)
