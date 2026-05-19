# ATOMIC SPECIFICATION: Context Load Lifecycle (C2.5)

**Status:** ATOMIC SPECIFICATION  
**Type:** Memory Architecture — Context Loading Timing and Costs  
**Depends On:** architectural-decisions.md, patterns-library.md, session-memory.md, graph-merge-integration.md  
**Used By:** /spek.context (implements this), /spek.prepare (calls /spek.context), all enrichment layers (read context)  

---

## Overview

The context load lifecycle specifies when context is loaded, what is loaded, how much it costs (tokens), caching strategy, and fallback behavior. This spec bridges memory architecture (what to store) with actual execution (when/how to load).

---

## Scope & Relationship

**This spec defines:**
- **WHEN** context is loaded (timing, phases, triggers)
- **COSTS** (token counts, latency targets, caching strategy)
- **FALLBACK** behavior (stale context, missing vault, recovery)

**Related specs define complementary concerns:**
- [Context Layer](context-layer.md) defines **WHAT** context is loaded and **HOW** to inject it (composition, structure, access patterns)
- [Persistent Memories & Lessons](persistent-memories-and-lessons.md) defines the 3-layer memory model (vault, repo memory, session memory)
- [Context Load Lifecycle](context-load-lifecycle.md) (THIS SPEC) defines **WHEN** + **COSTS** + **CACHING**

**Use together:**
- For *timing, costs, caching*: Start here (context-load-lifecycle.md)
- For *composition, injection, access*: See context-layer.md

---

## Context Loading Phases

### Phase 0: Preparation (OFFLINE)

**When:** Before session starts  
**Duration:** < 1 second  
**Tokens:** 0  

**Process:**
1. User or system triggers `/spek.context`
2. Command parsed (any parameters?)
3. Validate vault exists and is accessible

**Output:**
- Command ready to execute

---

### Phase 1: Vault Read (LOCAL FILE I/O)

**When:** Session start (`/spek.prepare` → `/spek.context` → Step 1)  
**Duration:** 1-2 seconds  
**Tokens:** 0 (local file reads)  

**Process:**
1. Read vault/decision.md (active decisions only)
   - Parse file
   - Filter to `status: active` entries
   - Extract decision titles + rationale
2. Read vault/patterns.md (recent patterns)
   - Parse file
   - Filter to `status: active` entries
   - Filter to patterns used in last 3 features
   - Extract pattern names + tags
3. Read vault/lessons/ (most recent)
   - List files in vault/lessons/
   - Sort by date
   - Read 3-5 most recent files
   - Extract: What We Built, How We Built It, Key Patterns, Key Lessons
4. Read /memories/repo/ (if exists)
   - Read /memories/repo/architectural-decisions.md
   - Read /memories/repo/patterns-index.md

**Output:**
- Raw vault content (markdown text)
- Raw repo memory content (markdown text)
- File read timestamps (for cache validation)

**Error Handling:**
- If vault/decision.md missing → Log warning, continue without decisions
- If vault/patterns.md missing → Log warning, continue without patterns
- If vault/lessons/ empty → Log info, continue without recent lessons
- If repo memory missing → Log info (it will be created at first feature end)

---

### Phase 2: Code Graph Query (LOCAL FILE I/O)

**When:** Immediately after vault read (Phase 1)  
**Duration:** 1-2 seconds  
**Tokens:** 0 (local file reads)  

**Process:**
1. Validate code graph freshness
   - Read vault/graph/config.json
   - Check last_incremental_sync timestamp
   - If age > GRAPH_REFRESH_THRESHOLD (default: 1 hour)
     - Warn user "Code graph is stale; consider running `/spek.map`"
     - Proceed anyway (use old graph)
   - If age < GRAPH_REFRESH_THRESHOLD
     - Use graph as-is
2. Read code graph summary
   - Read vault/graph/nodes.jsonl (first 50 lines or ~5KB)
   - Extract node types: function, class, module, document
   - Count by language
   - Identify most recently modified files (from edges.jsonl)
3. High-level structure summary
   - Extract top-level modules/packages
   - Extract recently changed files
   - Identify code hotspots (files with most connections)

**Output:**
- Code structure summary (module list, language breakdown, recent changes)
- Graph freshness status
- Timestamp of last graph update

**Error Handling:**
- If vault/graph/ missing → Log warning, proceed without code context
- If graph is corrupted → Log error, attempt to recover or skip
- If graph is very old (> 7 days) → Warn strongly "Code graph is very stale"

---

### Phase 3: Context Summarization (LLM CALL)

**When:** After vault + repo memory + code graph read  
**Duration:** 5-15 seconds  
**Tokens:** ~3-5K tokens (with compression)  

**Process:**
1. Construct context briefing prompt
   ```
   You are a code agent assistant. Here is the project context:
   
   RECENT DECISIONS:
   [decisions from Phase 1]
   
   RECENT PATTERNS:
   [patterns from Phase 1]
   
   CODE STRUCTURE:
   [structure from Phase 2]
   
   RECENT LESSONS:
   [lessons from Phase 1]
   
   Summarize this context in caveman mode (active voice, concrete, short, specific).
   Be concise. Output only the summary, no preamble.
   ```

2. Call Claude Haiku (or configured model)
   - Model: Claude Haiku 4.5 (fast + cheap for summarization)
   - Temperature: 0.3 (low creativity; fact-focused)
   - Max tokens: 2000 (keep summary compact)
   - System: "You compress technical context into caveman mode (active voice, concrete, short)"

3. Receive summarized context

4. Compress to caveman format
   - Active voice: "We chose X" not "X was chosen"
   - Concrete: "Decorator pattern" not "a flexible approach"
   - Short: 1-2 sentences per item
   - Specific: "Use for SpecKit integration" not "use in many places"

**Output:**
- Compressed context (1-2K tokens)
- Execution metadata (model used, tokens, latency)

**Cost Analysis:**
- Input tokens: ~2.5K (context briefing)
- Output tokens: ~1K (compressed summary)
- Total: ~3.5K tokens
- Latency: 5-15 seconds

**Token Optimization:**
- Cache vault reads (no tokens)
- Cache code graph reads (no tokens)
- Only compress most recent context (filters in Phase 1-2)
- Use cheaper model (Haiku vs. Opus) → 70% cost reduction

**Error Handling:**
- If LLM call fails → Use uncompressed context (raw vault text)
- If response is empty → Retry once, then fallback
- If response is corrupted → Use most recent cache

---

### Phase 4: Session Memory Write (LOCAL FILE I/O)

**When:** After context summarization (Phase 3)  
**Duration:** < 1 second  
**Tokens:** 0  

**Process:**
1. Create /memories/session/context-loaded.md
   - YAML frontmatter (session_date, timestamp, token usage)
   - Context summary (from Phase 3)
   - Decisions + patterns + code structure + lessons (raw)
   - Timestamps and cache hit info

2. Validate file created
   - Check file exists
   - Check file size > 100 bytes (not empty)
   - Check YAML is parseable

3. Log context load completion

**Output:**
- /memories/session/context-loaded.md (created or updated)
- Log entry: "Context loaded: X decisions, Y patterns, Z lessons, ~3.5K tokens"

**Error Handling:**
- If file write fails → Log error, continue (context is in agent memory anyway)
- If file is empty → Log error, retry write

---

## Complete Lifecycle Flow

```
User: /spek.context
  ├─ Phase 0: Prepare (< 1s, 0 tokens)
  ├─ Phase 1: Vault Read (1-2s, 0 tokens)
  │  ├─ Read vault/decision.md
  │  ├─ Read vault/patterns.md
  │  ├─ Read vault/lessons/ (top 3-5)
  │  └─ Read /memories/repo/ (if exists)
  ├─ Phase 2: Code Graph Query (1-2s, 0 tokens)
  │  ├─ Validate graph freshness
  │  ├─ Read vault/graph/config.json
  │  ├─ Read first 50 lines of vault/graph/nodes.jsonl
  │  └─ Extract summary
  ├─ Phase 3: Summarization (5-15s, ~3.5K tokens)
  │  ├─ Construct briefing
  │  ├─ Call LLM (Claude Haiku)
  │  └─ Compress with caveman mode
  ├─ Phase 4: Session Write (< 1s, 0 tokens)
  │  ├─ Create /memories/session/context-loaded.md
  │  └─ Validate creation
  └─ Output: Context loaded summary (user visible)
     Total: ~10-20 seconds, ~3.5K tokens
```

---

## Caching Strategy

### Input Caching (Vault Reads)

**Cache Key:** Vault file modification times  
**Cache Validation:** Check if vault/decision.md, vault/patterns.md, vault/lessons/ have changed

**Process:**
1. On first `/spek.context` call → Read all vault files
2. Store hashes: `{vault/decision.md: sha256(content), ...}`
3. On next `/spek.context` call → Check current hashes
4. If hashes match → Reuse previous read (skip Phase 1)
5. If hashes differ → Re-read changed files

**Benefit:** Skip vault I/O if vault unchanged (speeds up context refresh mid-session)

**Storage:** /memories/session/context-cache.json
```json
{
  "last_load": "2026-05-19T10:30:00Z",
  "vault_hashes": {
    "vault/decision.md": "abc123...",
    "vault/patterns.md": "def456...",
    "vault/lessons/": "ghi789..."
  },
  "code_graph_hash": "jkl012...",
  "tokens_used": 3500
}
```

### Output Caching (Summarization)

**Cache Key:** Vault content + code graph content  
**Cache Validation:** Check if vault/code graph have changed

**Process:**
1. On first `/spek.context` call → Summarize, store result
2. Compute cache key: `hash(vault_content + graph_content)`
3. On next `/spek.context` call → Check if key matches
4. If matches → Reuse previous summary (skip Phase 3, save ~3.5K tokens)
5. If differs → Re-summarize

**Benefit:** Skip LLM call if context unchanged (saves tokens and latency)

**Storage:** /memories/session/context-summary-cache.json
```json
{
  "cache_key": "abc123def456...",
  "summary": "[compressed context text]",
  "timestamp": "2026-05-19T10:30:00Z",
  "tokens_saved": 3500
}
```

---

## Fallback Behavior

### If Vault Read Fails (Phase 1)

**Fallback:**
- Skip to Phase 2 (code graph only)
- Continue without decisions/patterns/lessons
- Log warning "Could not load decisions/patterns"

**Impact:** Context is incomplete but usable

### If Code Graph Query Fails (Phase 2)

**Fallback:**
- Skip to Phase 3 (proceed without code context)
- Continue without code structure summary
- Log warning "Could not load code graph"

**Impact:** Context lacks code-specific insights

### If LLM Summarization Fails (Phase 3)

**Fallback Option 1 (Preferred):**
- Use uncompressed context (raw vault text)
- Skip caveman compression
- Add ~2K tokens to output
- Log warning "Context compression failed; using uncompressed"

**Fallback Option 2 (Quick Recovery):**
- Retry LLM call once
- If retry fails, use cached summary (if available)
- If no cache, use uncompressed

**Impact:** Context is verbose but complete

### If Session Memory Write Fails (Phase 4)

**Fallback:**
- Context is already in agent memory (embedded)
- Log error "Could not write session memory"
- Continue without persisting context
- Next session will reload

**Impact:** Context is not persisted between turns, but session works

---

## Cost Optimization

### Token Budget

**Standard Load:** ~3.5K tokens
- Phase 1 (vault read): 0 tokens
- Phase 2 (code graph): 0 tokens
- Phase 3 (LLM summarization): ~3.5K tokens
- Phase 4 (file write): 0 tokens

**Optimization Strategies:**

1. **Cache Reuse** → 0 tokens (if cache hit)
   - If vault unchanged → Skip Phase 1
   - If summary cached → Skip Phase 3 (use cache)
   - Result: 0 tokens (pure file I/O, ~1-2 seconds)

2. **Lite Mode** → ~2K tokens (less compression)
   - Use simpler summarization prompt
   - Output only top N items (top 3 decisions, top 3 patterns)
   - Max tokens: 1000 instead of 2000

3. **Ultra Lite Mode** → ~1K tokens (minimal compression)
   - Extract 1-2 line summary only
   - Use cheaper model (Claude 3.5 Haiku)
   - Max tokens: 500

### Example Flows

**Scenario 1: First session load**
- No cache → All phases execute
- Tokens: ~3.5K
- Time: ~15 seconds

**Scenario 2: Context refresh mid-session (vault unchanged)**
- Cache hit on vault + summary
- Phases 1-3 skipped
- Tokens: 0
- Time: ~1 second

**Scenario 3: New feature, vault changed**
- Vault cache miss → Phase 1 executes
- Summary cache miss → Phase 3 executes
- Tokens: ~3.5K
- Time: ~15 seconds

**Scenario 4: Multi-session feature (resuming)**
- First call: ~3.5K tokens
- Second call (same session): 0 tokens (cache)
- Third call (new session): ~3.5K tokens (fresh load)
- Total for feature: ~7K tokens

---

## Integration Points

### Called By

- `/spek.prepare` (Step 5) — Load context at feature start
- `/spek.context [query]` — Manual context refresh
- User request — "refresh context on [topic]"

### Uses

- vault/decision.md
- vault/patterns.md
- vault/lessons/
- /memories/repo/architectural-decisions.md
- /memories/repo/patterns-index.md
- vault/graph/nodes.jsonl

### Writes

- /memories/session/context-loaded.md

### Triggers

- /spek.prepare step 5
- Optionally during work (manual refresh)

---

## Configuration

### .spekificity/config.yaml

```yaml
context_loading:
  # Enable caching?
  enable_cache: true
  cache_expiry_minutes: 60  # Re-summarize after this long
  
  # Model for summarization
  model: "claude-haiku-4.5"  # Fast + cheap
  temperature: 0.3  # Low creativity
  max_tokens_output: 2000
  
  # Token limits (by mode)
  token_limits:
    standard: 3500
    lite: 2000
    ultra: 1000
  
  # Graph freshness threshold
  graph_stale_threshold_hours: 1
  
  # How many items to include
  recent_decisions_count: 5
  recent_patterns_count: 5
  recent_lessons_count: 3
```

---

## Success Criteria

✅ Context loads in 10-20 seconds  
✅ Cost is predictable (~3.5K tokens, or 0 with cache)  
✅ Vault reads are fast (< 2 seconds)  
✅ LLM summarization is reliable (Haiku model, temp 0.3)  
✅ Caching works (reduces token usage on repeat calls)  
✅ Fallback behavior is graceful (partial context is better than none)  
✅ /memories/session/context-loaded.md is well-formed  

---

## Implementation Checklist

- [ ] Implement Phase 1 (vault read)
- [ ] Implement Phase 2 (code graph query)
- [ ] Implement Phase 3 (LLM summarization with caveman mode)
- [ ] Implement Phase 4 (session memory write)
- [ ] Implement caching strategy
- [ ] Implement fallback behavior
- [ ] Add configuration to .spekificity/config.yaml
- [ ] Test end-to-end context load
- [ ] Document in /spek.context skill

---

## References

**Related Specs:**
- [architectural-decisions.md](architectural-decisions.md) — Decisions read in Phase 1
- [patterns-library.md](patterns-library.md) — Patterns read in Phase 1
- [session-memory.md](session-memory.md) — Session memory written in Phase 4
- [graph-merge-integration.md](graph-merge-integration.md) — Code graph structure read in Phase 2

**External:**
- [extracted spec Load/Write Lifecycle](persistent-memories-and-lessons.md#loadwrite-lifecycle) — Original spec
