# Three-Layer Memory Model — Quick Reference

**Category:** Architectural  
**Problem:** Persist context across sessions without re-reading files  
**Solution:** Vault (persistent) → Repo Cache (compressed) → Session (ephemeral)  
**Used in:** All skills (context read/write)  

---

## What It Is

Three memory layers with different persistence and granularity:

```
MEMORY ARCHITECTURE

┌──────────────────────────────────────────┐
│ Layer 1: VAULT (Obsidian)                │
│ Persistent, Authoritative                │
│ └─ vault/decision.md                     │
│ └─ vault/patterns.md                     │
│ └─ vault/lessons/<YYYY-MM-DD>-*.md       │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Layer 2: REPO MEMORY (Copilot)           │
│ Persistent, Project-Scoped               │
│ └─ /memories/repo/architectural-*.md     │
│ └─ /memories/repo/patterns-index.md      │
│ └─ /memories/repo/codebase-map.md        │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Layer 3: SESSION MEMORY (Copilot)        │
│ Ephemeral, Session-Scoped                │
│ └─ /memories/session/context-loaded.md   │
│ └─ /memories/session/current-feature.md  │
│ └─ /memories/session/scratchpad.md       │
└──────────────────────────────────────────┘
```

---

## Why Use It

- ✅ Persistent context (decisions survive sessions)
- ✅ Efficient loading (compressed Layer 2 faster than full Layer 1)
- ✅ Flexible fallback (if Layer 1 fails, use Layer 2)
- ✅ Scalable (each layer optimized for its role)
- ✅ Searchable (grep works across all layers)

---

## When to Use

✅ Multi-session workflows (features span days/weeks)  
✅ Knowledge preservation (decisions reusable)  
✅ Context-aware AI (inject prior patterns)  

❌ Single-shot tasks (no persistence needed)  
❌ Stateless APIs (sessionless clients)  
❌ Sensitive data (requires security review)  

---

## Read Lifecycle

```
Session Start:
  1. Load Layer 3 (if exists from prior session)
  2. If Layer 3 empty, load top 3-5 from Layer 2
  3. If Layer 2 empty, load from Layer 1
  ↓
During Feature Work:
  Layer 3 available (kept in context)
  ↓
Feature End:
  Layer 3 → archived to Layer 1 (via /spek.conclude)
```

---

## Write Lifecycle

```
  Layer 3 → archived to Layer 1 (via /spek.conclude)
  1. Extract decisions from artifacts
  2. Write to Layer 1 (vault/decision.md) — AUTHORITATIVE
  3. Compress + write to Layer 2 (/memories/repo/) — CACHE
  1. Extract decisions from artifacts
  2. Write to Layer 1 (vault/decision.md) — AUTHORITATIVE
  3. Compress + write to Layer 2 (/memories/repo/) — CACHE
  4. Layer 3 archived (moved to vault/sessions/)
  ↓
Next Session Start:
  1. Load from Layer 2 (compressed, cached)
  2. Layer 3 fresh (start new session)
```

 [ ] Archival process automated (Layer 3 → Layer 1 at /spek.conclude)?

## Example: Loading Context

```python
def load_context():
    """Load context from all 3 layers"""
    
    # Try Layer 3 first (current session)
    try:
        layer3 = read_file("/memories/session/context-loaded.md")
        return layer3
    except FileNotFoundError:
        pass
    
    # Try Layer 2 (compressed cache)
    try:
        layer2 = read_file("/memories/repo/architectural-decisions.md")
        cache_layer3 = layer2  # Use cache as Layer 3
        return cache_layer3
    except FileNotFoundError:
        pass
    
    # Try Layer 1 (authoritative but slower)
    try:
        layer1 = read_file("vault/decision.md")
        # Compress and cache for future
        save_to_layer2(layer1)
        return layer1
    except FileNotFoundError:
        # All layers failed; continue with empty context
        log_warning("No context found in any layer")
        return ""
```

---

## Related Patterns

- **Zettelkasten Convention** — Structure of vault notes (Layer 1)
- **Session-to-Vault Archival** — How Layer 3 → Layer 1 transition works
- **Context Injection** — Loads all 3 layers for enrichment

---

## Where It's Used

- **Primary:** [memory-architecture.md](../specs/memory-architecture.md)
- **Read in:**
  - [context-layer.md](../specs/context-layer.md)
  - [spek-prepare-command.md](../specs/prepare-command.md)
- **Written in:**
  - [post-processing.md](../specs/post-processing.md)
  - [spek-post-command.md](../specs/post-command.md)

---

## Quick Checklist

- [ ] Layer 1 (vault) exists and is searchable?
- [ ] Layer 2 (repo cache) created and updated at feature end?
- [ ] Layer 3 (session) created at session start?
- [ ] Load order correct (Layer 3 → Layer 2 → Layer 1)?
- [ ] Write hierarchy correct (Layer 1 authoritative)?
- [ ] Fallback working (Layer 2 used if Layer 1 fails)?
- [ ] Archival process automated (Layer 3 → Layer 1 at /spek.conclude)?

---

## Token Cost

- **Layer 1 load:** 1-3K tokens (full vault read)
- **Layer 2 load:** 100-300 tokens (compressed cache)
- **Layer 3 load:** ~50 tokens (ephemeral, already in context)

Best practice: Load Layer 2 or Layer 3, avoid full Layer 1 read unless necessary.
