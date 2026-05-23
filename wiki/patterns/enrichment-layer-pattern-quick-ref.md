# Enrichment Layer Pattern — Quick Reference

**Category:** Architectural  
**Problem:** SpecKit commands run without context; specs diverge from decisions  
**Solution:** Wrap phases with context injection: PRE (load context) → CORE (SpecKit) → POST (validate)  
**Used in:** `/spek.plan` (all phases)  

---

## What It Is

Context injection for each SpecKit phase (specify, plan, implement):

```
ENRICHMENT WORKFLOW

/spek.plan [feature-description]
├─ SPECIFY PHASE
│  ├─ PRE: Load decisions + patterns
│  ├─ CORE: Call /speckit.specify (enriched)
│  └─ POST: Validate spec aligns with decisions
│
├─ PLAN PHASE
│  ├─ PRE: Load decisions + patterns + lat.md index
│  ├─ CORE: Call /speckit.plan (enriched)
│  └─ POST: Validate plan follows architecture
│
└─ IMPLEMENT PHASE (post-approval)
    ├─ PRE: Load decisions + patterns + lat.md index
   ├─ CORE: Call /speckit.implement (enriched)
   └─ POST: Collect diff + validate
```

---

## Why Use It

- ✅ Context-aware specs (decisions inform spec)
- ✅ Consistent planning (patterns reused)
- ✅ Aligned implementation (code follows plan)
- ✅ Drift detection (POST validation catches deviations)
- ✅ Multi-feature consistency (same patterns across features)

---

## When to Use

✅ Spec-driven development with constraints  
✅ Multi-feature projects (pattern reuse)  
✅ Strict architecture (decisions are hard constraints)  

❌ Greenfield projects (no prior context)  
❌ Prototyping (speed > consistency)  
❌ One-off features (no architecture)  

---

## Specify Phase Enrichment

```python
def specify_enriched(feature_description):
    """PRE → CORE → POST for specify phase"""
    
    # PRE: Load context
    decisions = load_from_vault("vault/decision.md")
    patterns = load_from_vault("vault/patterns.md")
    
    # Validate inputs
    if not feature_description:
        raise ValueError("Feature description required")
    
    # Inject context
    enriched_prompt = f"""
    {feature_description}
    
    IMPORTANT: Adhere to these project decisions:
    {format_decisions(decisions)}
    
    Consider these proven patterns:
    {format_patterns(patterns)}
    """
    
    # CORE: Call SpecKit
    spec = speckit_specify(enriched_prompt)
    
    # POST: Validate
    assert "## Overview" in spec
    assert "## Success Criteria" in spec
    # Check alignment with decisions
    for decision in decisions:
        if contradicts(spec, decision):
            log_warning(f"Spec may contradict decision: {decision}")
    
    save_file("spec.md", spec)
    return spec
```

---

## Plan Phase Enrichment

```python
def plan_enriched(spec):
    """PRE → CORE → POST for plan phase"""
    
    # PRE: Load context (via MCP tools, no token cost)
    decisions = load_from_vault("vault/decision.md")
    patterns = load_from_vault("vault/patterns.md")
    
    # Query lat.md structure (MCP tool calls)
    changed_files = extract_files_from_spec(spec)  # e.g., ["src/services/auth.py"]
    graph_context = []
    for file in changed_files:
        symbols = call_mcp_tool("lat_symbols", file_path=file)
        impact = call_mcp_tool("lat_impact", file=file)
        graph_context.append({"file": file, "symbols": symbols, "impact": impact})
    
    # Validate inputs
    assert os.path.exists("spec.md"), "Spec must exist before planning"
    
    # Inject context
    enriched_prompt = f"""
    {spec}
    
    IMPORTANT: Follow these architectural decisions:
    {format_decisions(decisions)}
    
    Proven patterns to apply:
    {format_patterns(patterns)}
    
    Relevant code structure (via lat.md):
    {format_graph_context(graph_context)}
    """
    
    # CORE: Call SpecKit
    plan = speckit_plan(enriched_prompt)
    
    # POST: Validate
    assert "## Implementation Steps" in plan
    # Check architectural alignment
    for decision in decisions:
        if violates(plan, decision):
            raise ValueError(f"Plan violates decision: {decision}")
    
    save_file("plan.md", plan)
    return plan
```

---

## Implement Phase Enrichment

```python
def implement_enriched(tasks):
    """PRE → CORE → POST for implement phase"""
    
    # PRE: Load context (via MCP tools, no token cost)
    decisions = load_from_vault("vault/decision.md")
    patterns = load_from_vault("vault/patterns.md")
    
    # Query code graph for each task (MCP tool calls)
    graph_context = []
    for task in tasks:
        affected_symbols = task.get("affected_code", [])
        for symbol in affected_symbols:
            # Find definition
            definition = call_mcp_tool("lat_definition", symbol=symbol)
            # Find callers
            callers = call_mcp_tool("lat_callers", symbol=symbol)
            # Estimate impact
            impact = call_mcp_tool("lat_impact", symbol=symbol)
            graph_context.append({
                "symbol": symbol,
                "definition": definition,
                "callers": callers,
                "impact": impact
            })
    
    # Inject context (MCP tools have no token cost)
    enriched_context = format_enrichment_context(
        decisions, patterns, graph_context
    )
    
    # CORE: Call SpecKit (task by task)
    for task in tasks:
        print(f"Implementing: {task.name}")
        code = speckit_implement(task, context=enriched_context)
        save_code(code)
    
    # POST: Collect diff + validate
    diff = get_git_diff()
    if not diff:
        raise ValueError("No code changes; check implementation")
    
    # Validate against plan
    if deviates_from_plan(diff, plan):
        log_warning("Implementation deviates from plan")
    
    return diff
```

---

## Context Loading (PRE Layer)

```python
def load_enrichment_context(phase):
    """Load context for enrichment PRE layer"""
    
    # Load from vault (vault queries)
    decisions = load_from_vault("vault/decision.md")
    patterns = load_from_vault("vault/patterns.md")
    
    # Load lat.md via MCP tools (if plan/implement phase)
    if phase in ["plan", "implement"]:
        # Query lat.md structure via MCP tools (no token cost)
        # Example: for each changed file, query its symbols and impact
        graph_queries = []
        recent_changes = get_git_log(limit=20)
        for file in extract_changed_files(recent_changes):
            symbols = call_mcp_tool("lat_symbols", file_path=file)
            impact = call_mcp_tool("lat_impact", file=file)
            graph_queries.append({"file": file, "symbols": symbols, "impact": impact})
    else:
        graph_queries = None
        recent_changes = None
    
    return {
        "decisions": decisions,
        "patterns": patterns,
        "graph_queries": graph_queries,
        "recent_changes": recent_changes,
    }
```

---

## Related Patterns

- **Context Injection** — Mechanism for loading + injecting context
- **Decorator Wrapper** — Overall structure (PRE → CORE → POST)
- **Anti-Sycophancy** — Validation logic in POST layer

---

## Where It's Used

- **Primary:** [enrichment-layer.md](../specs/enrichment-layer.md)
- **Integration points:**
  - [context-layer.md](../specs/context-layer.md) (context loading)
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md) (orchestration)
  - [speckit-integration-contract.md](../specs/speckit-integration-contract.md) (contract)

---

## Quick Checklist

- [ ] PRE layer loads decisions + patterns?
- [ ] PRE layer loads lat.md index (if applicable)?
- [ ] Context injection formats clearly?
- [ ] CORE layer receives enriched input?
- [ ] POST layer validates alignment?
- [ ] Contradiction detection working?
- [ ] Logging clear (what decisions were checked)?
- [ ] Error messages helpful (suggest alignment)?

---

## Notes on Resource Use

- Resource usage varies by feature and environment; teams should configure monitoring and tracking according to their needs.

Optimization: Use the Three-Layer Query Rule to reduce context loading cost significantly.
