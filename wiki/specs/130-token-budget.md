# C.3.10 Token Budget Allocation & Tracking

**Priority:** MEDIUM (phasing and prioritization)  
**Effort:** effort estimate omitted / configurable
**Adoption Source:** B.10 (Pilot Shell)  
**Requires:** C.3.1-C.3.5 Phase 1 specs

---

## Purpose

Implement token cost transparency by:
1. **Allocating** per-phase token budget (Specify, Plan, Implement, Post)
2. **Tracking** actual usage per phase
3. **Alerting** when approaching budget limits
4. **Reporting** efficiency metrics at feature end
5. **Enabling** cost-aware optimization decisions

**Goal:** Control token costs; identify expensive phases; optimize before budget blooms.

---

## Scope & Relationships

**What this spec covers:**
- Token budget allocation per phase
- Token usage tracking during each skill
- Alert thresholds + notifications
- Budget reporting + metrics
- Configuration + customization

**What this spec does NOT cover:**
- Token pricing (assume cost is measured in tokens)
- Cost forecasting (just track actual)
- GPU/compute optimization (out of scope)

**Related specs:**
- C.3.3: 3-Layer Query Rule (reduces token usage)
- B.8.4: Post Command (where reporting integrates)

---

## Token Budget Model

### Default Per-Feature Budget

Per-feature token budgets are configurable per team. The specification recommends defining a per-feature budget and breaking it down by phase (specify, plan, implement, post), but exact numeric values are environment-specific and should be set in project configuration.

Example configuration (qualitative):
- `per_feature`: configurable total budget for a feature
- `phases`: per-phase allocations (specify, plan, implement, post)
- `alerts`: configured thresholds to trigger warnings and alerts

## Success Criteria

-- ✅ Token budget allocated per phase (configurable)
-- ✅ Tracking working (actual usage measured + reported)
-- ✅ Alerts functional (configured thresholds trigger warnings)
-- ✅ Reporting comprehensive (metrics visible at feature end)
-- ✅ Cost-aware optimization enabled (users can adjust budget based on feedback)
-- ✅ Token savings measurable (3-layer query rule + caveman compression tracked)
-- ✅ Budget customizable (teams can adjust per their needs)

### Customize per Team

```yaml
# Different strategies for different teams (numeric values omitted)
solo_developer:
  per_feature: configured-value  # Team-specific configured budget

team_collaborative:
  per_feature: configured-value  # Team-specific configured budget

enterprise_cost_sensitive:
  per_feature: configured-value  # Team-specific configured budget
```

---

## Token Tracking

### Per-Phase Tracking

Token usage should be measured and tracked per phase. Concrete token counts vary by project and feature; the system records per-operation deltas and aggregates them per phase for reporting.

- During `specify` and `plan` phases, track Layer 1 (code graph) vs Layer 2 (vault) usage and report aggregated phase cost.
- Implement phase token usage is typically determined at feature end and reported in conclude.
- Conclude phase tracks lesson generation, auto-linking, vault updates, and archival costs.

Reports should show per-phase totals, configured budget vs actual usage, and triggered alerts when configured thresholds are met.

---

## Usage Tracking Mechanism

### Token Counter Integration

**In each skill:**

```python
def track_token_usage(phase_name, operation_name):
    """Track tokens using Claude API usage"""
    
    # Start counter
    start_tokens = get_usage_total()
    
    # Run operation
    operation()
    
    # Calculate delta
    end_tokens = get_usage_total()
    delta = end_tokens - start_tokens
    
    # Log
    log_token_usage(phase=phase_name, operation=operation_name, tokens=delta)
    
    # Check budget
    phase_budget = config.token_budget.phases[phase_name]['budget']
    phase_used = get_phase_token_total(phase_name)
    
    if phase_used > phase_budget * configured_threshold:
      alert(f"⚠ {phase_name} approaching configured budget threshold")
    
    return delta
```

### Session Logging

Log all token usage to session memory (numeric values omitted in examples):

```markdown
# Token Usage: <feature-name>

## Specify Phase
- Spec generation:    recorded (omitted)
- Context loading:    recorded (omitted)
- Auto-linking:       recorded (omitted)
Total:               recorded (omitted)

## Plan Phase
- Planning:           recorded (omitted)
⚠ Alert: Approaching configured limit (qualitative)

## Implement Phase
[Local; tokens recorded at feature end]

## Conclude Phase
- Lessons:            recorded (omitted)
- Vault updates:      recorded (omitted)
- Archival:           recorded (omitted)
Total:               recorded (omitted)

## Overall
Total tokens used:    recorded (omitted)
Efficiency:           qualitative descriptor (see metrics)
```

---

## Reporting & Metrics

### Token Usage Report

At feature end (`/spek.conclude` Step 10), show:

```
Feature Token Usage Report (numeric values omitted):

Feature:        <feature-name>
Duration:       recorded (omitted)
Total Tokens:   recorded (omitted)
Cost Savings:   qualitative descriptor (numeric omitted)

Phase Breakdown:
- Specify:   recorded (omitted)
- Plan:      recorded (omitted)
- Implement: recorded (omitted)
- Post:      recorded (omitted)

Key Metrics:
- Specify Efficiency:   recorded (omitted)
- Plan Efficiency:      recorded (omitted)
- Implement Efficiency: recorded (omitted)
- Post Efficiency:      recorded (omitted)
- 3-Layer Query Rule:   usage recorded (omitted)
- Auto-linking:         qualitative descriptor
- Caveman Compression:  qualitative descriptor

Trend (Last features): numeric values omitted; see trend logs
```

### Efficiency Metrics

**Track:**
- Tokens per phase (breakdown)
- Tokens per LOC of code generated
- 3-layer query rule adoption % (reduces tokens)
- Caveman compression savings (%)
- Auto-linking efficiency (manual vs auto)

**Example Metrics Across Features:**

```
Feature          | Total | Specify | Plan | Implement | Post | Tokens/LOC
────────────────────────────────────────────────────────────────────────────
auth-refactor    | 9200  | 2000    | 2800 | 2400      | 2000 | 1.9t/LOC
state-mgmt       | 10500 | 2200    | 3500 | 3800      | 1000 | 2.1t/LOC
api-redesign     | 12000 | 2500    | 3000 | 5500      | 1000 | 2.4t/LOC
──────────────────────────────────────────────────────────────────────────
Average          | 10567 | 2233    | 3100 | 3900      | 1333 | 2.1t/LOC

Trend:
- Tokens/LOC improving (1.9 < 2.4): ✓ Getting more efficient
- Conclude phase decreasing: ✓ Lessons compression working
- Specify stable: ✓ Consistent cost
```

---

## Optimization Strategies

### If Budget Exceeded

**Action Plan:**

```
IF tokens exceed configured warning threshold:
  1. Run report (identify expensive phase)
  2. Suggest optimizations:
     a. Use 3-layer query rule more (save Layer 3 reads)
     b. Enable caveman compression (reduces lesson cost significantly)
     c. Defer optional features to v2 (reduce scope)
     d. Batch similar queries (avoid duplication)
  3. User can:
     - Accept and continue (log override)
     - Optimize and re-run phase
     - Reduce scope for this feature
```

### If Budget Significantly Under

**Opportunity to Invest:**

```
IF tokens < budget * 0.5:
  - Could increase test coverage (use tokens for testing)
  - Could add more documentation (generate guides)
  - Could explore alternative approaches
  - Celebrate efficiency!
```

---

## Configuration

### `.spek/config.yaml`

```yaml
token_budget:
  # Global settings
  per_feature: 12000
  enabled: true
  track_usage: true
  report_at_end: true
  
  # Threshold alerts
  alert_threshold_percent: 80
  warning_threshold_percent: 60
  
  # Phase budgets
  phases:
    specify_phase:
      budget: 2000
      optimization_tips: 
        - "Use Layer 1 queries (code graph)"
        - "Limit spec length (<10KB)"
    
    plan_phase:
      budget: 3000
      optimization_tips:
        - "Reuse decisions from vault"
        - "Reference similar plans"
    
    implement_phase:
      budget: 5000
      optimization_tips:
        - "Use pair programming mode (less context)"
        - "Batch similar tasks"
    
    post_phase:
      budget: 2000
      optimization_tips:
        - "Enable caveman compression (lessons)"
        - "Auto-linking reduces manual work"
  
  # Reporting
  report_format: "detailed"  # or "summary"
  save_report_to_session: true
  send_alert_on_exceed: true
```

---

## Success Criteria

- ✅ Per-phase token budgets configured
- ✅ Token usage tracked in each skill
- ✅ Alerts triggered at 80% budget usage
- ✅ Token usage report generated at feature end
- ✅ Efficiency metrics calculated (tokens/LOC, phase breakdown)
- ✅ 3-layer query rule adoption measured
- ✅ Caveman compression savings quantified
- ✅ Trend analysis across features (improving efficiency?)
- ✅ Optimization suggestions provided when over budget

---

## Related Specifications

- **C.3.3:** 3-Layer Query Rule (primary cost reduction strategy)
- **B.8.4:** Post Command (Step 10 reporting)
- **C.3.2:** Auto-tagging (reduces manual token cost)

---

## References

- **Production Source:** https://github.com/Pilot-Shell/pilot-shell (token budgeting pattern)
- **Token Pricing:** Anthropic Claude pricing (varies by model)