# ATOMIC SPECIFICATION: Graph Query Patterns (C5.5)

**Status:** ATOMIC SPECIFICATION  
**Type:** Usage — Querying vault/graph/ for Code Context  
**Depends On:** graph-storage-structure.md  
**Used By:** /spek.context, /spek.plan, enrichment layers  

---

## Overview

Query patterns for accessing code graph efficiently using grep, jq, and basic shell commands (zero tokens, fast).

---

## The 3-Layer Query Rule

```
Layer 1: Direct grep (fastest, simple patterns)
├─ Query: "Find all nodes in module X"
├─ Cost: < 100ms
└─ Token: 0

Layer 2: Composed grep (medium, filtered patterns)
├─ Query: "Find all methods called by function Y"
├─ Cost: 100-500ms
└─ Token: 0

Layer 3: LLM synthesis (slowest, complex reasoning)
├─ Query: "What modules would be affected by changing API?"
├─ Cost: 5-15s
└─ Token: 1-2K
```

**Strategy:** Use Layer 1-2 whenever possible; Layer 3 only for complex reasoning.

---

## Layer 1: Direct Grep Queries

### Query 1: Find all nodes in a file

```bash
grep '"file": "src/services/auth.py"' vault/graph/nodes.jsonl
```

**Output:** All symbols defined in that file

### Query 2: Find all methods in a class

```bash
grep '"scope": "AuthService"' vault/graph/nodes.jsonl | grep '"type": "method"'
```

**Output:** All methods in AuthService class

### Query 3: Find all nodes of a type

```bash
grep '"type": "function"' vault/graph/nodes.jsonl | grep '"language": "python"'
```

**Output:** All Python functions

### Query 4: Find nodes by name

```bash
grep '"name": "authenticate"' vault/graph/nodes.jsonl
```

**Output:** All symbols named "authenticate"

---

## Layer 2: Composed Grep + Shell

### Query 5: Find all callers of a function

```bash
# Step 1: Find node ID
NODE_ID=$(grep '"name": "query_user"' vault/graph/nodes.jsonl | grep '"file": "src/database' | jq -r '.id')

# Step 2: Find all edges TO this node
grep "\"to_node\": \"$NODE_ID\"" vault/graph/edges.jsonl

# Step 3: Extract from_node and resolve to symbol names
```

**Output:** All functions/methods that call query_user

### Query 6: Find all dependencies of a module

```bash
# All edges FROM nodes in src/services/
grep '"file": "src/services/' vault/graph/nodes.jsonl | jq -r '.id' | \
while read NODE_ID; do
  grep "\"from_node\": \"$NODE_ID\"" vault/graph/edges.jsonl
done
```

**Output:** All symbols that module depends on

### Query 7: Find recently changed code

```bash
# Code changed in last 5 commits
git log -5 --name-only --pretty=format: | grep -v '^$' | \
while read FILE; do
  grep '"file": "'$FILE'"' vault/graph/nodes.jsonl
done
```

**Output:** All symbols in recently changed files

---

## Layer 3: LLM Synthesis (When Needed)

### Query: Impact analysis ("What breaks if I change X?")

```bash
# Collect context
CHANGED_SYMBOLS=$(grep '"file": "src/services/auth.py"' vault/graph/nodes.jsonl | jq -r '.id')
AFFECTED=$(for ID in $CHANGED_SYMBOLS; do grep "to_node.*$ID" vault/graph/edges.jsonl; done)

# Pass to LLM with prompt:
# "These symbols changed: [changed]. These edges reference them: [affected].
#  What modules might break? What tests should run?"
```

**Cost:** 1-2K tokens (worth it for complex reasoning)

---

## Practical Examples

### Example 1: "What modules will feature X affect?"

**Approach:** Layer 1-2 (direct grep)

```bash
# From spec/plan, extract affected files: [src/services/auth.py, src/api/handlers.py]
grep '"file": "src/services/auth.py"\|"file": "src/api/handlers.py"' vault/graph/nodes.jsonl | \
  jq -r '.scope' | sort -u
```

**Cost:** < 1 second, 0 tokens

### Example 2: "Should I reuse module X?"

**Approach:** Layer 1-2 (grep + jq)

```bash
# Check if module exists and is mature (used by many)
grep '"file": "src/utils/crypto.py"' vault/graph/nodes.jsonl | wc -l
```

**Cost:** < 1 second, 0 tokens

### Example 3: "What patterns apply to this feature?"

**Approach:** Layer 2 (vault/patterns.md grep)

```bash
grep "#api\|#database" vault/patterns.md
```

**Cost:** < 1 second, 0 tokens

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
- [plan-enrichment.md](plan-enrichment.md) — Plan uses code graph queries

**External:**
- [graph-setup Part 5](codegraph-setup-and-integration.md#part-5-query-patterns)
