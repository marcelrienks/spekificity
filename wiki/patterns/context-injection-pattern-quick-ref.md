# Context Injection Pattern — Quick Reference

**Category:** Integration  
**Problem:** Tools need context but don't know how to load it  
**Solution:** Load context in PRE layer; inject into tool input  
**Used in:** Decorator wrapper PRE layer (all enriched skills)  

---

## What It Is

Loading and composing context for tool invocation:

```
CONTEXT INJECTION

Load Phase:
  ├─ Load vault (decisions, patterns, lessons)
  ├─ Load repo cache (compressed decisions)
  ├─ Load code graph (modules, dependencies)
  └─ Load session context (current feature state)

Compose Phase:
  ├─ Select relevant context (don't inject all)
  ├─ Format as enrichment prompt
  └─ Combine with user input

Inject Phase:
  └─ Prepend to tool input

Result:
  Tool receives enriched input with full context
```

---

## Why Use It

- ✅ Context-aware output (tool knows project constraints)
- ✅ Efficient loading (don't read all files)
- ✅ Flexible fallback (Layer 2 or Layer 3 if Layer 1 fails)
- ✅ Testable (can mock context)
- ✅ Reusable (same pattern for all tools)

---

## When to Use

✅ Spec-driven development (context-aware specs)  
✅ Architectural constraints (enforce decisions)  
✅ Pattern reuse (inject proven patterns)  

❌ Greenfield projects (no context to inject)  
❌ Context-agnostic tools (tool doesn't benefit)  

---

## Load Phase: Hierarchical Fallback

```python
def load_context(phase="specify"):
    """Load context with fallback hierarchy"""
    
    context = {}
    
    # Layer 1: Vault (authoritative but slow)
    try:
        context["decisions"] = load_from_vault("vault/decision.md")
        context["patterns"] = load_from_vault("vault/patterns.md")
    except FileNotFoundError:
        # Layer 2: Repo cache (compressed)
        try:
            context["decisions"] = load_from_cache(
                "/memories/repo/architectural-decisions.md"
            )
            context["patterns"] = load_from_cache(
                "/memories/repo/patterns-index.md"
            )
        except FileNotFoundError:
            # Layer 3: Minimal (continue without)
            context["decisions"] = []
            context["patterns"] = []
            log_warning("No decisions found; proceeding with minimal context")
    
    # Code graph via MCP tools (for plan/implement phases)
    if phase in ["plan", "implement"]:
        try:
            # Query code graph structure via MCP tools (no token cost)
            recent_files = get_git_log(limit=RECENT_LIMIT)
            graph_context = []
            for file in recent_files:
                symbols = call_mcp_tool("lat_symbols", file_path=file)
                graph_context.append({"file": file, "symbols": symbols})
            context["graph"] = graph_context
            context["recent_files"] = recent_files
        except Exception as e:
            context["graph"] = None
            context["recent_files"] = None
            log_warning(f"Code graph unavailable: {e}; using vault context only")
    
    return context
``````

---

## Compose Phase: Context Selection

```python
def compose_enrichment_prompt(user_input, context, phase="specify"):
    """Compose enrichment prompt with relevant context"""
    
    # Select relevant context (don't inject everything)
    relevant_decisions = select_by_relevance(
        context["decisions"],
        user_input,
        limit=TOP_N  # configurable top-N most relevant
    )
    relevant_patterns = select_by_relevance(
        context["patterns"],
        user_input,
        limit=TOP_M  # configurable top-M most relevant
    )
    
    # Format as enrichment prompt
    enrichment = f"""
    IMPORTANT: Adhere to these project decisions:
    """
    for decision in relevant_decisions:
        enrichment += f"\n- {decision.title}: {decision.rationale}"
    
    enrichment += f"\n\nConsider these proven patterns:"
    for pattern in relevant_patterns:
        enrichment += f"\n- {pattern.name}: When to use: {pattern.use_case}"
    
    # Add code context (if plan/implement)
    if phase in ["plan", "implement"] and context.get("graph"):
        enrichment += f"\n\nRelated code:"
        for file in context["recent_files"][:RECENT_FILES_PREVIEW]:
            enrichment += f"\n- {file}"
    
    return enrichment
```

---

## Inject Phase: Prepend to Input

```python
def inject_context_and_call(user_input, context, tool_fn, phase="specify"):
    """Inject context and call tool"""
    
    # Compose enrichment prompt
    enrichment = compose_enrichment_prompt(user_input, context, phase)
    
    # Inject: prepend enrichment to user input
    enriched_input = enrichment + f"\n\nUSER REQUEST:\n{user_input}"
    
    # Call tool with enriched input
    result = tool_fn(enriched_input)
    
    return result
```

---

## Example: Full Injection Flow

```python
def specify_with_context_injection(feature_description):
    """Full context injection flow"""
    
    # LOAD PHASE
    context = load_context(phase="specify")
    
    # Validate inputs
    if not feature_description:
        raise ValueError("Feature description required")
    
    # COMPOSE PHASE
    enrichment = compose_enrichment_prompt(
        feature_description, context, phase="specify"
    )
    
    # INJECT PHASE
    enriched_input = enrichment + f"\n\nUSER REQUEST:\n{feature_description}"
    
    # Call SpecKit
    spec = speckit_specify(enriched_input)
    
    # Validate output
    assert "## Overview" in spec, "Spec missing Overview"
    
    # Save
    save_file("spec.md", spec)
    
    return spec
```

---

## Related Patterns

- **Three-Layer Memory** — Context sources (vault/repo/session)
- **Three-Layer Query** — Efficient context loading
- **Fallback Hierarchy** — Layered fallback (if Layer 1 fails)

---

## Where It's Used

- **Primary:** [context-layer.md](../specs/context-layer.md)
- **Integration points:**
  - [enrichment-layer.md](../specs/enrichment-layer.md)
  - [decorator-wrapper-pattern.md](../specs/decorator-wrapper-pattern.md)
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md)

---

## Quick Checklist

- [ ] Load phase has fallback hierarchy (Layer 1 → 2 → 3)?
- [ ] Compose phase selects relevant context (don't inject all)?
- [ ] Inject phase prepends to user input?
- [ ] Tool receives enriched input?
- [ ] Error handling covers all layers (missing context)?
- [ ] Logging clear (which context was loaded)?
- [ ] Performance acceptable (context loading within acceptable bounds)?

---

## Notes on Resource Use

- Resource usage varies by feature and environment; teams should configure monitoring and tracking according to their needs.

Optimization: Use Layer 2 (compressed cache) instead of Layer 1 to reduce context-loading resource use.
