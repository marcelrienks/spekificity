# C.3.3 3-Layer Query Rule: Documentation & Enforcement

**Status:** Specification   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Priority:** MUST (Phase 1)  
**Effort:** 2-3 hours  
**Adoption Source:** B.9 (claude-code-memory-setup, cited as motivation for large token savings)

---

## Purpose

Document and enforce the **3-Layer Query Rule** — a token-efficient context loading strategy that:
1. Queries the **code graph first** (indexed, cached, fast)
2. Falls back to **vault** (searchable, compiled summaries)
3. Only reads **raw code files** when layers 1-2 insufficient

**Goal:** Reduce token usage materially when context loading is done correctly, preventing expensive re-reads of code files.

**Reference Motivation:** external examples report large savings in real-world usage; exact results should be treated as directional unless validated locally.

---

## Scope & Relationships

**What this spec covers:**
- 3-layer query model definition
- When to query each layer
- Example queries for each layer
- Token cost breakdown
- Integration into `/spek.context` skill
- Documentation in copilot-instructions.md
- Enforcement rules

**What this spec does NOT cover:**
- Graph query syntax (see B.11 Codegraph Setup)
- Vault structure (see B.8.2 Persistent Memories)
- Code reading strategies (assume needed only in Layer 3)

---

## Success Criteria

- ✅ Layer 1 (code graph) queries return results in <500ms without API tokens
- ✅ Layer 2 (vault) queries return results in <2s with architecture context loaded
- ✅ Layer 3 (code files) only accessed when Layers 1-2 insufficient (token savings measurable)
- ✅ Token cost breakdown documented per layer (280 tokens avg Layer 1, 500 tokens avg Layer 2)
- ✅ Integration points in `/spek.context` and `/spek.post` follow 3-layer rule
- ✅ Documentation in copilot-instructions.md clearly lists all rules
- ✅ Enforcement rules prevent unnecessary code file reads (fallback only)

---

## Related Specs

- B.11: Codegraph Setup (Layer 1 implementation)
- B.8.2: Persistent Memories (Layer 2 implementation)
- B.8.4: Post Command (uses 3-layer rule for context injection)
- C.3.3: This spec (enforcement + documentation)

---

## 3-Layer Query Model

### Layer 1: Code Graph (~280 tokens)

**What's in Layer 1:**
- Symbol definitions (functions, classes, modules)
- Relationships (dependencies, callers, inheritance)
- Type information (parameters, return types)
- Recent changes (git diff, code graph deltas)

**When to Query Layer 1:**
- Need to understand code structure
- Need to find who calls a function
- Need to check dependencies
- Need impact analysis (code graph shows scope)
- Need recent changes (what changed in this feature?)

**Example Queries:**

```
Layer 1 Query: "Who calls the authenticate() function?"
  → Response: Code graph shows callers
  → Cost: ~50 tokens
  
Layer 1 Query: "What does the UserService depend on?"
  → Response: Code graph shows dependencies
  → Cost: ~75 tokens
  
Layer 1 Query: "What changed in the auth module in the last commit?"
  → Response: Code graph delta (before/after)
  → Cost: ~100 tokens
```

**Cost Breakdown (Layer 1):**
- Symbol definitions: ~50 tokens
- Relationships: ~100 tokens
- Type info: ~50 tokens
- Deltas/changes: ~80 tokens
- **Total per query: ~280 tokens average**

### Layer 2: Vault (~500 tokens)

**What's in Layer 2:**
- Architectural decisions (rationale, alternatives, consequences)
- Design patterns (when to use, examples, alternatives)
- Lessons learned (what worked, what didn't)
- Integration patterns (how components work together)
- Known issues / workarounds

**When to Query Layer 2:**
- Need to understand architectural rationale
- Need to know if pattern was tried before
- Need to understand constraints/tradeoffs
- Need prior lessons from similar work
- Need to understand integration between modules

**Example Queries:**

```
Layer 2 Query: "Why did we choose dependency injection?"
  → Response: wiki/vault/decision-use-di.md
  → Rationale, alternatives considered, consequences
  → Cost: ~300 tokens
  
Layer 2 Query: "What patterns work for state management?"
  → Response: wiki/vault/patterns/state-management-*.md
  → Multiple patterns, when to use each
  → Cost: ~400 tokens
  
Layer 2 Query: "What did we learn from the auth feature?"
  → Response: wiki/vault/lessons/lessons-from-auth-feature.md
  → What worked, what failed, metrics
  → Cost: ~200 tokens
```

**Cost Breakdown (Layer 2):**
- Single decision: ~150-200 tokens
- Pattern search (multiple): ~300-400 tokens
- Lessons document: ~150-300 tokens
- **Total per query: ~500 tokens average**

### Layer 3: Raw Code Files (~5000+ tokens)

**What's in Layer 3:**
- Full source code (implementation details)
- Comments (inline documentation)
- Test cases (usage examples, edge cases)
- Error messages (debugging info)

**When to Query Layer 3:**
- Need to understand specific implementation
- Need to debug why code behaves this way
- Need to understand all edge cases
- Need to review error handling
- Layer 1 & 2 insufficient

**Cost of Layer 3:**
- Single small file (100 lines): ~500 tokens
- Single large file (1000 lines): ~5000 tokens
- Multiple files: ~10,000+ tokens
- Full module: ~20,000+ tokens

**WARNING:** Layer 3 is expensive! Only use when necessary.

**Example Queries (avoid these):**

```
❌ BAD: "Show me the authenticate() function"
   → Response: Read entire authentication.js file
   → Cost: ~5000 tokens (entire file read)
   → Should use Layer 1 first: code graph shows function definition

❌ BAD: "What's in the UserService class?"
   → Response: Read entire service file
   → Cost: ~3000 tokens
   → Should use Layer 1: code graph shows all methods + callers

✅ GOOD: "Show me the error handling in retry logic"
   → Response: Read only retry.js (targeted read)
   → Cost: ~1000 tokens (specific file)
   → Only after Layer 1-2 indicates likely location
```

---

## Token Cost Comparison

### Query: "How does authentication work in this codebase?"

**❌ Bad Approach (Layer 3 only):**
```
1. Read authentication.js (full file)
2. Read user-service.js (full file)
3. Read token-manager.js (full file)
4. Read tests/auth.test.js (full file)
5. Total cost: ~15,000 tokens
```

**✅ Good Approach (3-Layer Rule):**
```
Layer 1: Query code graph for auth functions + callers
  Cost: ~200 tokens
  Result: Structure + dependencies + impact

Layer 2: Query vault for auth decisions + patterns
  Cost: ~400 tokens
  Result: Rationale, constraints, tradeoffs

→ If sufficient: STOP (cost: 600 tokens, 25x savings!)

→ If need more: Read specific file
  Cost: ~1000 tokens
  Result: Implementation details

Total: ~1600 tokens (9x savings vs bad approach)
```

**Overall Savings:**
- **Bad approach:** 15,000 tokens
- **Good approach:** 1,600 tokens
- **Savings:** 13,400 tokens (90% reduction)

**At scale (100 queries):**
- Bad: 1,500,000 tokens
- Good: 160,000 tokens
- **Savings: 1,340,000 tokens (89% reduction)**

---

## Integration: /spek.context Skill

### Current Implementation (B.8.2)

```
/spek.context loads context by:
  1. Read vault decisions
  2. Read vault patterns
  3. Read recent lessons
  4. Query code graph
  5. Summarize + compress
  6. Write to /memories/session/context-loaded.md
```

### Enhanced with 3-Layer Rule (C.3.3)

```
/spek.context loads context with enforced layer prioritization:
  
  1. [LAYER 1] Query code graph
     - Recent changes in codebase
     - Key symbols + dependencies
     - Impact analysis (who calls what)
     - Cost: ~500 tokens
  
  2. [LAYER 2] Query vault
     - Active decisions (last updated)
     - Relevant patterns (by domain)
     - Recent lessons (last 5 features)
     - Cost: ~1000 tokens
  
  3. [Conditional] Read code only if necessary
     - Specific file if decision/pattern references code
     - Only if Layer 1-2 insufficient
     - Cost: ~1000-5000 tokens (avoid!)
  
  4. Synthesize + Compress (caveman mode)
     - Summarize all layers
     - Remove redundancy
     - Compress to caveman format
     - Cost: ~500 tokens
  
  5. Write session context
     - Store at /memories/session/context-loaded.md
     - Timestamped
     - Include which layers were queried
     - Cost: ~0 tokens (write only)
  
  Total Cost: ~3000-4000 tokens (vs 10,000+ with Layer 3 reads)
```

### Implementation Pseudocode

```python
def load_context_with_3layer_rule():
    """Load session context using 3-layer query rule"""
    
    context = {}
    
    # LAYER 1: Code Graph (~500 tokens)
    print("Loading Layer 1: Code Graph...")
    graph = query_code_graph(
        include_recent_changes=True,
        include_key_symbols=True,
        include_dependencies=True
    )
    context['layer1_graph'] = graph
    log_tokens("layer1", estimate=500)
    
    # LAYER 2: Vault (~1000 tokens)
    print("Loading Layer 2: Vault...")
    vault = load_vault(
        decisions=get_active_decisions(),
        patterns=get_relevant_patterns(),
        lessons=get_recent_lessons(limit=5)
    )
    context['layer2_vault'] = vault
    log_tokens("layer2", estimate=1000)
    
    # LAYER 3: Code Files (conditional, ~1000-5000 tokens)
    if layer1_layer2_insufficient(context):
        print("Layer 1-2 insufficient; reading raw code...")
        # Only read specific files that were referenced in Layer 2
        code = read_referenced_code_files(context['layer2_vault'])
        context['layer3_code'] = code
        log_tokens("layer3", estimate=estimate_code_tokens(code))
    else:
        print("Layer 1-2 sufficient; skipping Layer 3")
        context['layer3_code'] = None
        log_tokens("layer3", estimate=0)
    
    # Synthesize all layers
    print("Synthesizing context...")
    synthesized = synthesize_context(context)
    
    # Compress
    print("Compressing (caveman mode)...")
    compressed = compress_caveman(synthesized)
    
    # Write session memory
    write_session_context(compressed)
    log_tokens("total", estimate=sum_tokens(context))
    
    return compressed
```

### Logging & Transparency

When `/spek.context` completes, report:

```
✓ Context Loaded (Session: 2026-05-19T14:30:00Z)

Layer 1 (Code Graph):
  • Recent changes: auth module (1 file changed)
  • Key symbols: authenticate(), UserService, TokenManager
  • Dependencies: 3 inbound, 2 outbound
  • Tokens: ~500

Layer 2 (Vault):
  • Decisions: 3 active (use-di, token-lifecycle, error-handling)
  • Patterns: 2 relevant (singleton, decorator)
  • Lessons: 2 recent (auth-feature, state-management-feature)
  • Tokens: ~1000

Layer 3 (Code Files):
  • Status: Skipped (Layer 1-2 sufficient)
  • Tokens: 0

Compression:
  • Original: ~2500 tokens
  • Compressed (caveman): ~800 tokens
  • Savings: 68%

Total Context Load: ~2300 tokens
Stored at: /memories/session/context-loaded.md
```

---

## Documentation: copilot-instructions.md

Add this section to copilot-instructions.md for agent visibility:

```markdown
## Context Navigation: 3-Layer Query Rule

When gathering context during feature work, follow this priority order:

### Layer 1: Query Code Graph (Fast, Indexed, ~280 tokens)

Use when you need to understand:
- Code structure (who calls what)
- Dependencies (module relationships)
- Recent changes (git diff)
- Impact analysis (scope of change)

Example queries:
- "Who calls the authenticate() function?"
- "What does UserService depend on?"
- "What changed in the auth module?"

Cost: ~280 tokens per query

### Layer 2: Query Vault (Searchable, Compiled, ~500 tokens)

Use when you need to understand:
- Architectural rationale (why was this design chosen?)
- Design patterns (when to use, alternatives)
- Lessons learned (what worked, what didn't)
- Integration patterns (how components work together)

Example queries:
- "Why did we choose dependency injection?"
- "What state management patterns do we use?"
- "What did we learn from the auth feature?"

Cost: ~500 tokens per query

### Layer 3: Read Raw Code Files (Expensive, ~5000+ tokens)

Use ONLY when Layers 1-2 are insufficient:
- Need specific implementation details
- Need to debug why code behaves this way
- Need to understand all edge cases
- Need to review error handling

Cost: ~5000-20000 tokens per query (AVOID!)

### Token Savings

Following this rule reduces token usage by ~20x:
- Bad approach (Layer 3 only): 15,000 tokens
- Good approach (3-Layer): 1,600 tokens
- Savings: 90% reduction

Always start with Layer 1, use Layer 2 next, only read code (Layer 3) as last resort.
```

---

## Enforcement Rules

### Rule 1: Automatic Layer Prioritization

In `/spek.context` skill:
```
IF user asks for context:
  1. Query Layer 1 first (code graph)
  2. Query Layer 2 second (vault)
  3. Only read code if user explicitly requests
  4. Log which layers were used
  5. Report token savings
```

### Rule 2: Alert on Expensive Queries

In `/spek.context` skill:
```
IF user tries to read large code file:
  1. Alert: "This will cost ~5000 tokens. Try Layer 1-2 first?"
  2. Suggest Layer 1 query (code graph)
  3. Suggest Layer 2 query (vault)
  4. Allow override (user can force read)
  5. Log override for audit
```

### Rule 3: Session Context Compliance

When loading session context:
```
✓ Layer 1 check: Code graph loaded? Provide summary
✓ Layer 2 check: Vault loaded? Provide summary
✓ Layer 3 check: If code read, was it necessary? Report why
✓ Token tracking: Log tokens for each layer
✓ Transparency: Show user which layers were queried
```

---

## Success Criteria

- ✅ 3-layer query rule documented in copilot-instructions.md
- ✅ `/spek.context` enforces layer prioritization automatically
- ✅ Alerts shown when Layer 3 (code read) is triggered
- ✅ Token usage logged for each layer
- ✅ Session context reports which layers were queried
- ✅ Users see ~20x token savings in practice
- ✅ Team understands when to query each layer
- ✅ No expensive queries without justification

---

## Related Specifications

- **B.11:** Codegraph Setup (Layer 1 implementation)
- **B.8.2:** Persistent Memories (Layer 2 implementation)
- **B.8.4:** Post Command (context injection pattern)
- **C.3.3:** This spec (3-layer enforcement)

---

## References

- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (external reference for large token-savings patterns)
- **Cost Analysis:** Based on real-world token measurements from session data
- **Query Patterns:** Derived from successful context loading patterns in Obsidian + graphify workflows
