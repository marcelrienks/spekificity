# Three-Layer Query Rule — Quick Reference

**Category:** Query  
**Problem:** Agent queries cost tokens; naive approach reads all files (expensive)  
**Solution:** Tier queries by cost; use Layer 1-2 for 90% of cases  
**Used in:** Context loading, `/spek.context`, code graph queries  

---

## What It Is

Hierarchical query strategy that prioritizes efficiency:

```
QUERY HIERARCHY

Layer 1: Code Graph (FAST, FREE)
├─ Cost: ~50-100 tokens
├─ Latency: <100ms
├─ Query: grep + jq on vault/graph/nodes.jsonl
├─ Examples:
│  - "Who calls function X?"
│  - "What does module Y depend on?"
│  - "Find all classes in file Z"
└─ Success rate: 95% of queries

Layer 2: Vault/Decisions (MEDIUM, CHEAP)
├─ Cost: ~200-300 tokens
├─ Latency: <1s
├─ Query: grep + jq on vault files
├─ Examples:
│  - "What decisions affect authentication?"
│  - "What patterns exist for error handling?"
│  - "Find recent lessons about caching"
└─ Success rate: 85% of queries

Layer 3: Raw Code Files (SLOW, EXPENSIVE)
├─ Cost: 1-3K tokens
├─ Latency: 5-15s
├─ Query: Read entire files, AI synthesis
├─ Examples:
│  - "Explain this complex algorithm"
│  - "Find all edge cases in function X"
│  - "What's the performance bottleneck?"
└─ Success rate: 100% (if query possible at all)

RULE: Use Layer 1 → Layer 2 → Layer 3
Only escalate when necessary.
```

---

## Why Use It

- ✅ Token savings (Layer 1-2 cover 90% of cases, save 90% tokens)
- ✅ Speed (Layer 1 queries complete in <100ms)
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

## Layer 1: Code Graph Queries

**Setup:**
```bash
# Code graph pre-indexed in vault/graph/nodes.jsonl
# One JSON per line; queryable with grep + jq
```

**Examples:**

```bash
# Query 1: Find all nodes in a file
grep '"file": "src/services/auth.py"' vault/graph/nodes.jsonl

# Query 2: Find all methods in a class
grep '"scope": "AuthService"' vault/graph/nodes.jsonl | \
grep '"type": "method"'

# Query 3: Find all nodes of a type
grep '"type": "function"' vault/graph/nodes.jsonl | \
grep '"language": "python"'

# Query 4: Find nodes by name
grep '"name": "authenticate"' vault/graph/nodes.jsonl

# Query 5: Find all callers of a function
NODE_ID=$(grep '"name": "query_user"' vault/graph/nodes.jsonl | \
          grep '"file": "src/database' | jq -r '.id')
grep "\"to_node\": \"$NODE_ID\"" vault/graph/edges.jsonl

# Query 6: Find all dependencies of a module
grep '"file": "src/services/' vault/graph/nodes.jsonl | \
jq -r '.id' | \
while read NODE_ID; do
  grep "\"from_node\": \"$NODE_ID\"" vault/graph/edges.jsonl
done
```

**Cost:** 0-100 tokens (mostly depends on result size)

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

**Cost:** 100-300 tokens (metadata + search results)

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

# If < 500 lines: read and send to LLM
# If > 500 lines: break into sections, query one at a time
```

**Cost:** 1-3K tokens per file (can be 10x more than Layer 1)

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
- [ ] Performance targets met (Layer 1 <100ms)?

---

## Token Cost Example

**Scenario: Find all callers of a function**

```
Layer 1 approach:
  grep + node lookup: ~50 tokens
  grep edges: ~20 tokens
  Total: ~70 tokens ✓ EFFICIENT

Layer 2 approach:
  grep vault: ~100 tokens
  parse results: ~50 tokens
  Total: ~150 tokens

Layer 3 approach:
  Read src/ files: ~1000 tokens
  Parse and analyze: ~1000 tokens
  Total: ~2000 tokens ✗ EXPENSIVE

Savings: Layer 1 vs. Layer 3 = 28x cheaper (70 vs. 2000 tokens)
```

For multi-feature sessions, Layer 1 queries enable 10-15 queries per feature budget.
