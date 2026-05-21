# Skill Chaining Pattern — Quick Reference

**Category:** Workflow  
**Problem:** Workflow has dependent skills; sequential execution needs error handling  
**Solution:** Chain skills with explicit dependency management  
**Used in:** `/spek.plan` orchestration  

---

## What It Is

Sequential execution of dependent skills with error resilience:

```
SKILL CHAINING

/spek.plan [feature-description]
├─ Orchestrator: Determine skill order
│  └─ canonical or auto-detected workflow
│
├─ For each skill:
│  ├─ PRE-EXECUTION
│  │  ├─ Collect inputs
│  │  ├─ Surface cached values
│  │  └─ Prompt for missing inputs
│  ├─ EXECUTE
│  │  ├─ Call skill via interface
│  │  └─ Capture output + trace
│  ├─ POST-EXECUTION
│  │  ├─ Validate output
│  │  ├─ Detect failures
│  │  └─ Suggest remediation
│  └─ DECISION
│     └─ Continue or remediate?
│
└─ Handoff: Next workflow stage
```

---

## Why Use It

- ✅ Dependency management (clear skill ordering)
- ✅ Error resilience (remediation on failure)
- ✅ Flexible discovery (add/remove skills dynamically)
- ✅ Transparent interface (each skill has contract)
- ✅ Auditable (execution trace captured)

---

## When to Use

✅ Complex workflows with multiple dependent steps  
✅ Error recovery needed (not one-shot)  
✅ Flexible skill discovery (add/remove skills)  
✅ Multi-tool orchestration  

❌ Linear pipelines (no error recovery)  
❌ One-shot scripts (orchestration overhead)  
❌ Tightly coupled (loose coupling required)  

---

## Skill Workflow

```
Canonical Workflow (SpecKit):
  1. constitution (optional)
  2. specify
  3. clarify (optional)
  4. plan
  5. tasks
  6. analyze (optional)
  7. remediate (optional)
  8. implement

Spekificity Enrichment:
  Each skill wrapped with PRE → CORE → POST structure
```

---

## Orchestrator Algorithm

```python
def orchestrate_skills(feature_description):
    """Orchestrate skill chain with error resilience"""
    
    # Step 1: Determine workflow
    skills = discover_skills()  # Scan .specify/ or use canonical
    workflow = determine_workflow(skills)  # Order skills
    
    # Step 2: Execute each skill
    for skill in workflow:
        try:
            # PRE-EXECUTION
            inputs = collect_skill_inputs(skill)
            if inputs.has_cached_values():
                print(f"Cached values available for {skill.name}")
                inputs = surface_cached_values(inputs)
            
            # Validate inputs
            if not validate_inputs(inputs, skill):
                raise ValueError(f"Invalid inputs for {skill.name}")
            
            # EXECUTE
            print(f"Executing {skill.name}...")
            result = call_skill(skill, inputs)
            capture_trace(skill, result)
            
            # POST-EXECUTION
            if not validate_output(result, skill):
                raise ValueError(f"Invalid output from {skill.name}")
            
            # Update feature state
            update_feature_state(skill, "complete")
            
        except SkillError as e:
            # Classify error
            category = categorize_error(e)
            
            if category == "USER":
                # User must fix input
                print(f"Error: {e.message}")
                print(f"Action: {e.suggestion}")
                raise  # Stop workflow
                
            elif category == "TRANSIENT":
                # Retry
                print(f"Retrying {skill.name} (transient error)...")
                result = retry_skill(skill, inputs, max_retries=3)
                
            elif category == "FATAL":
                # Suggest manual remediation
                print(f"Fatal error in {skill.name}: {e.message}")
                print(f"Suggest: {e.suggestion}")
                remediate = prompt_user("Remediate manually? (y/n)")
                if remediate:
                    result = call_skill(skill, inputs)
                else:
                    raise
    
    # Step 3: Handoff
    print("✓ All skills complete")
    return "Ready for /spek.implement"
```

---

## Skill Interface

**Each skill must implement:**

```python
class Skill:
    name: str              # "specify", "plan", "implement"
    inputs: Dict[str, Any]      # Required inputs + types
    outputs: Dict[str, Any]     # Output artifacts
    success_criteria: List[str]  # How to validate output
    dependencies: List[str]     # Skills that must run first
    
    def execute(self, inputs, context) -> Dict[str, Any]:
        """Execute skill with given inputs and context"""
        pass
    
    def validate_output(self, output) -> bool:
        """Validate that output meets success criteria"""
        pass
```

---

## Example: Specify → Plan Chain

```python
def chain_specify_and_plan():
    """Chain specify and plan skills"""
    
    # Skill 1: Specify
    spec_inputs = {
        "feature_description": "Add user authentication",
        "context": load_context(),
    }
    spec_result = specify_skill.execute(spec_inputs)
    spec_skill.validate_output(spec_result)
    save_artifact("spec.md", spec_result)
    
    # Skill 2: Plan (depends on spec)
    plan_inputs = {
        "spec": spec_result,  # From prior skill
        "context": load_context(),
        "code_graph": load_code_graph(),
    }
    plan_result = plan_skill.execute(plan_inputs)
    plan_skill.validate_output(plan_result)
    save_artifact("plan.md", plan_result)
    
    return plan_result
```

---

## Related Patterns

- **Feature Lifecycle** — Phases that skills traverse
- **Decorator Wrapper** — Structure of each skill
- **Error Categorization** — Error handling per skill

---

## Where It's Used

- **Primary:** [spek-automate-workflow.md](../specs/spek-automate-workflow.md)
- **Integration points:**
  - [cli-orchestration.md](../specs/cli-orchestration.md)
  - [speckit-integration-contract.md](../specs/speckit-integration-contract.md)
  - [error-handling-and-recovery.md](../specs/error-handling-and-recovery.md)

---

## Quick Checklist

- [ ] Skill interface defined (all skills conform)?
- [ ] Workflow order correct (dependencies respected)?
- [ ] Input validation working (garbage in → error)?
- [ ] Output validation working (garbage out → error)?
- [ ] Error categorization per skill?
- [ ] Retry logic for transient errors?
- [ ] User guidance clear (what to fix)?
- [ ] Audit trail recorded (skill trace captured)?

---

## Token Cost

- **Orchestrator overhead:** ~50-100 tokens per feature
- **Per-skill I/O:** ~50 tokens (input collection + output validation)
- **Error handling:** ~100-200 tokens (if errors occur)

Total: ~200-500 tokens overhead (vs. ~50 tokens for bare skill execution).
