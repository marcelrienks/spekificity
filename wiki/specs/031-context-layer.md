---
title: "Context Layer (C3.1)"
status: "ATOMIC SPECIFICATION"
version: "1.0.0-alpha.1"
date: "2026-05-20"
type: "integration"
---

# ATOMIC SPECIFICATION: Context Layer (C3.1)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Integration Layer 1 — Context Loading and Injection  
**Depends On:** memory-architecture.md  
**Used By:** All enrichment layers (enrichment-layer.md)  

---

## Overview

The context layer loads project knowledge (decisions, patterns, lessons, code graph) and makes it available to enrichment wrappers. This spec defines what context is loaded, where it's stored, how it's accessed, and error handling.

---

## Scope & Relationship

**This spec defines:**
- **WHAT** context is loaded (decisions, patterns, lessons, code graph)
- **HOW** context is injected (composition, structure, access patterns, error handling)
- **WHERE** context is stored (session memory, variables, file references)

**Related specs define complementary concerns:**
- [Memory Architecture](memory-architecture.md) defines the 3-layer memory model (vault, repo memory, session memory), **WHEN** context is loaded, **COSTS** (token counts, latency), and **CACHING** strategy
- [Context Layer](context-layer.md) (THIS SPEC) defines **WHAT** + **HOW** + **WHERE**

**Use together:**
- For *what to load, injection patterns, access*: Start here (context-layer.md)
- For *memory model, timing, costs, caching strategy*: See memory-architecture.md

## Success Criteria

- ✅ Context loads at session start (decisions, patterns, lessons, code graph all available)
- ✅ Context accessible to enrichment layers (decisions/patterns queryable from session memory)
- ✅ Session memory persists throughout feature work (context doesn't reset mid-feature)
- ✅ Vault queries work without errors (no missing files, permission issues, or parse errors)
- ✅ Code graph context injected correctly (modules, hotspots, recent changes available)
- ✅ Manual context refresh works (user can refresh if context becomes stale)
- ✅ Fallback behavior graceful (if context missing, enrichments continue with partial context)

---

## Context Composition

### What Is Loaded (at session start)

**From vault (permanent archive):**
- Active decisions (vault/decision.md)
- Active patterns (vault/patterns.md)
- Recent lessons (vault/lessons/ — a small set of recent lessons)

**NOTE:** Vault context is authoritative and can be loaded via multiple mechanisms. Spekificity recommends using the Obsidian CLI (`obsidian` command bundled with the desktop app) where available for scripted automation; alternative methods include reading `.obsidian/cache.json`, using Dataview/plugin exports, or running `obsidian eval` snippets. The implementation should gracefully fall back to cache/plugin-based exports when the CLI is not available.

**From repo memory (compressed cache):**
- Recent decisions (if already synced)
- Pattern index

**From code graph (local index):**
- Module/function list
- Recently modified files
- Code hotspots (frequently connected nodes)

**From session memory (ephemeral):**
- Current feature state
- Progress tracking
- Decisions made this feature

### Context Storage

**In Agent Memory (embedded):**
- Context is loaded into the agent's context window at session start
- Format: Compressed markdown (caveman mode)
- Availability: Entire session (until context refresh)
- Size: compact (compressed)

**In Session Files (persistent within session):**
- vault/session/ — What was loaded
- vault/session/ — Feature state

**In Vault (permanent):**
- vault/decision.md, vault/patterns.md, vault/lessons/ — Authoritative

---

## Context Access Patterns

### Read-Only Queries During Work

**Query Type 1: "What decisions exist?"**
```python
# Agent queries embedded context
decisions = search_context("active decisions", limit="project-configured-limit")
# Returns: a limited set of active decisions from embedded context
```

**Query Type 2: "What patterns are relevant?"**
```python
# Agent queries embedded context
patterns = search_context("patterns for [domain]", limit="project-configured-limit")
# Returns: a limited set of patterns matching domain tags
```

**Query Type 3: "What's the code structure?"**
```python
# Agent queries embedded context
modules = search_context("module list", limit="project-configured-limit")
# Returns: a limited set of modules by importance
```

**Query Type 4: "What was learned?"**
```python
# Agent queries embedded context
lessons = search_context("lessons from similar feature", limit="project-configured-limit")
# Returns: lessons from similar features
```

### Manual Context Refresh

**Trigger:** During feature, if context is stale or incomplete

```bash
# Refresh specific context
/spek.context --refresh decisions

# Refresh all context
/spek.context --refresh all

# Query specific topic
/spek.context "patterns for database design"
```

**Process:**
1. Call /spek.context with refresh flag
2. Re-read vault (bypass cache if needed)
3. Re-summarize (fresh LLM call)
4. Update vault/session/
5. Inject new context into agent memory

---

## Enrichment Integration

### Pre-Execution Context Injection

**In Decorator Wrapper Pattern (decorator-wrapper-pattern):**

```python
def wrapped_speckit_command(command, args, **kwargs):
    # PRE-EXECUTION: Load context
    context = load_context_for_command(command)
    
    # CORE EXECUTION: Call speckit
    result = speckit_command(command, args, **context_injected)
    
    # POST-EXECUTION: Update memory
    update_feature_state(result)
    
    return result
```

### Context Injection Points

**For `/spek.plan` specify phase:**
- Recent decisions (to guide spec toward existing constraints)
- Recent patterns (to suggest proven approaches)
- Code graph (to understand what code already exists)

**For `/spek.plan` plan phase:**
- Recent decisions + patterns (same as specify)
- Code graph + impact analysis (which code modules will be affected)
- Architecture patterns (decorator, separation of concerns, etc.)

**For `/spek.implement`:**
- Feature state (what tasks are complete)
- Code structure (where to implement)
- Patterns (implementation guidance)

---

## Error Handling & Resilience

### If Context Load Fails

**Scenario 1: Vault is inaccessible**
- Fallback: Use repo memory (cached version, might be stale)
- If repo memory also missing: Use code graph only
- Log: "Vault load failed; using cached context"
- Continue: Yes (partial context is useful)

**Scenario 2: Code graph is missing or corrupted**
- Fallback: Skip code structure summary
- Continue with vault/repo memory
- Log: "Code graph unavailable; using vault context only"
- Continue: Yes

**Scenario 3: LLM summarization fails**
- Fallback: Use uncompressed context (raw vault text)
- Trade-off: Uses more tokens, but complete
- Log: "Summarization failed; using uncompressed context"
- Continue: Yes

### Graceful Degradation

**Full Context:** Decisions + Patterns + Lessons + Code  
**Reduced Context:** Decisions + Patterns + Lessons (no code)  
**Minimal Context:** Decisions + Patterns (no lessons, code)  
**Fallback Context:** Code graph only (vault unavailable)  
**No Context:** Continue without context (all sources fail)  

**Strategy:** Try full context, fallback to reduced, then minimal, then fallback, then none. At each level, continue (don't fail).

---

## Context Lifecycle During Feature

```
Session Start
  │
  ├─ /spek.prepare
  │  └─ /spek.context (Load full context)
  │     ├─ Read vault (decisions, patterns, lessons)
  │     ├─ Read code graph
  │     ├─ Summarize (caveman mode)
  │     └─ Write vault/session/
  │     └─ Inject into agent memory
  │
  ├─ /spek.plan (specify phase uses injected context)
  │  └─ Decisions + Patterns guide spec generation
  │
  ├─ /spek.plan (plan phase uses injected + fresh context)
  │  └─ Re-inject context (might have changed)
  │  └─ Decisions + Patterns + Code graph guide plan
  │
  ├─ /spek.implement (Use feature state context)
  │  └─ Current feature state guides task execution
  │
  └─ /spek.conclude (Archive context)
     └─ Extract decisions + patterns
     └─ Write to vault
     └─ Sync to repo memory
     └─ Archive session context

Feature Complete / Next Session
  │
  └─ Context is reset (new session)
     └─ /spek.context loads fresh context
```

---

## Configuration

### .spek/config.yaml

```yaml
context_layer:
  # Enable context injection?
  enabled: true
  
  # Context injection points
  inject_into:
    specify: true      # Inject for /spek.plan specify phase?
    plan: true         # Inject for /spek.plan plan phase?
    implement: true    # Inject for /spek.implement?
  
  # Refresh strategy
  refresh:
    # Refresh context before each command?
    before_each_command: false
    # OR refresh only after N minutes?
    refresh_interval_minutes: 30
    # OR refresh only when user requests?
    on_demand: true
  
  # Fallback behavior
  fallback:
    # If vault unavailable, use repo memory?
    use_repo_memory: true
    # If summarization fails, use uncompressed?
    use_uncompressed: true
    # If all sources fail, continue anyway?
    continue_without_context: true
```

---

## Success Criteria

✅ Context is loaded at session start  
✅ Context is available throughout session  
✅ Context is injected into enrichment commands  
✅ Decisions and patterns guide spec/plan generation  
✅ Code graph is queryable and up-to-date  
✅ Graceful fallback if any context source fails  
✅ Manual refresh possible with `/spek.context`  
✅ Session files track what was loaded  

---

## Implementation Checklist

- [ ] Implement context loading in /spek.context
- [ ] Implement context injection in wrapper functions
- [ ] Implement context refresh mechanism
- [ ] Add fallback handling for missing sources
- [ ] Write vault/session/ format
- [ ] Add context query patterns
- [ ] Test with vault missing / code graph stale / LLM failure

---

## References

**Related Specs:**
- [memory-architecture.md](memory-architecture.md) — How context is loaded + memory layers
- [enrichment-layer.md](enrichment-layer.md) — Uses context in `/spek.plan` phases
- [decorator-wrapper-pattern.md](decorator-wrapper-pattern.md) — Pattern for injection

**External:**
- [extracted spec Context Layer](speckit-integration-contract.md#layer-1-context-layer-spekcontext) — Original spec
