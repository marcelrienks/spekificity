---
title: "Token Budget Allocation & Tracking"
status: "Specification"
version: "1.0.0-alpha.1"
date: "2026-05-20"
priority: "MEDIUM"
---

# C.3.10 Token Budget Allocation & Tracking

**Status:** Specification   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Priority:** MEDIUM (Phase 2, quick win)  
**Effort:** 2-3 hours  
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

```yaml
token_budget:
  per_feature: 12000  # Total tokens per feature
  
  # Phase breakdown
  phases:
    specify_phase:
      budget: 2000  # Spec generation
      tools: ["/spek.plan (specify phase)", "C.3.2 auto-linking"]
    
    plan_phase:
      budget: 3000  # Plan generation + architecture decisions
      tools: ["/spek.plan (plan phase)", "code graph queries"]
    
    implement_phase:
      budget: 5000  # Code generation + debugging
      tools: ["/spek.implement", "pair programming"]
    
    post_phase:
      budget: 2000  # Lessons + vault updates + archival
      tools: ["/spek.conclude", "session archival", "vault updates"]
  
  # Alert thresholds
  alert_threshold_percent: 80  # Alert when 80% used
  warning_threshold_percent: 60  # Warning when 60% used
```

## Success Criteria

- ✅ Token budget allocated per phase (default 12K per feature, customizable)
- ✅ Tracking working (actual usage measured + reported)
- ✅ Alerts functional (warnings at 60%, 80% thresholds)
- ✅ Reporting comprehensive (metrics visible at feature end)
- ✅ Cost-aware optimization enabled (users can adjust budget based on feedback)
- ✅ Token savings measurable (3-layer query rule + caveman compression tracked)
- ✅ Budget customizable (teams can adjust per their needs)

### Customize per Team

```yaml
# Different strategies for different teams

solo_developer:
  per_feature: 8000  # Smaller budget (fewer iterations)
  
team_collaborative:
  per_feature: 15000  # Larger budget (more context loading)

enterprise_cost_sensitive:
  per_feature: 5000  # Aggressive optimization needed
```

---

## Token Tracking

### Per-Phase Tracking

**During `/spek.plan` Specify Phase:**
```
/spek.plan specify-phase execution:
  Layer 1 query (code graph):   ~500 tokens
  Layer 2 query (vault):        ~1000 tokens
  Spec generation:              ~300 tokens
  Auto-linking:                 ~200 tokens
  ─────────────────────────────────────
  Total Phase Cost:             ~2000 tokens
  Budget:                        2000 tokens
  Usage:                         100%
  Status:                        ✓ On budget
```

**During `/spek.plan` Plan Phase:**
```
/spek.plan plan-phase execution:
  Context reload:               ~400 tokens
  Code graph analysis:          ~800 tokens
  Plan generation:              ~1200 tokens
  Architecture validation:      ~400 tokens
  ─────────────────────────────────────
  Total Phase Cost:             ~2800 tokens
  Budget:                        3000 tokens
  Usage:                         93%
  Status:                        ⚠ Approaching limit (80% threshold)
  
  Alert: "Plan phase at 93% of budget; implement efficiently"
```

**During Implement Phase:**
```
[Implement happens locally; token tracking at feature end]
```

**During Conclude Phase:****
```
/spek.conclude execution:
  Context reload:               ~300 tokens
  Test failure analysis:        ~200 tokens
  Lesson generation:            ~600 tokens
  Auto-linking:                 ~400 tokens
  Vault updates:                ~300 tokens
  Session archival:             ~200 tokens
  ─────────────────────────────────────
  Total Phase Cost:             ~2000 tokens
  Budget:                        2000 tokens
  Usage:                         100%
  Status:                        ✓ On budget
```

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
    
    if phase_used > phase_budget * 0.8:
        alert(f"⚠ {phase_name} at {phase_used/phase_budget*100:.0f}% of budget")
    
    return delta
```

### Session Logging

Log all token usage to session memory:

```markdown
# Token Usage: auth-refactor

## Specify Phase
- Spec generation:    500t
- Context loading:    1200t
- Auto-linking:       300t
Total:               2000t (100% of budget)

## Plan Phase
- Planning:           2800t (93% of budget)
⚠ Alert: Approaching limit

## Implement Phase
[Local; tokens estimated at feature end]

## Conclude Phase
- Lessons:            600t
- Vault updates:      400t
- Archival:           300t
Total:               2000t (100% of budget)

## Overall
Total tokens used:    ~9000t of 12000t (75%)
Efficiency:           Above target ✓
```

---

## Reporting & Metrics

### Token Usage Report

At feature end (`/spek.conclude` Step 10), show:

```
╔════════════════════════════════════════════════════════════╗
║       Feature Token Usage Report: auth-refactor            ║
╠════════════════════════════════════════════════════════════╣
║ Feature:        auth-refactor                              ║
║ Duration:       5 days                                     ║
║ Total Tokens:   9200 / 12000 (77%)                        ║
║ Cost Savings:   3000 tokens (20% under budget)            ║
╠════════════════════════════════════════════════════════════╣
║ Phase Breakdown:                                           ║
║                                                            ║
║ Specify:   2000 / 2000  (100%) ███████████ ✓              ║
║ Plan:      2800 / 3000  (93%)  ██████████▌ ⚠ High        ║
║ Implement: 2400 / 5000  (48%)  █████░░░░░ ✓ Efficient    ║
║ Post:      2000 / 2000  (100%) ███████████ ✓              ║
╠════════════════════════════════════════════════════════════╣
║ Key Metrics:                                               ║
║                                                            ║
║ Specify Efficiency:   2000 tokens for 12KB spec            ║
║ Plan Efficiency:      2800 tokens for 8KB plan             ║
║ Implement Efficiency: 2400 tokens (1.9 tokens per LOC)     ║
║ Post Efficiency:      2000 tokens (lessons + archival)     ║
║                                                            ║
║ 3-Layer Query Rule:   Used 15 times, saved ~2500 tokens   ║
║ Auto-linking:         70% wikilinks auto-generated         ║
║ Caveman Compression:  Saved ~800 tokens in lessons         ║
╠════════════════════════════════════════════════════════════╣
║ Trend (Last 3 Features):                                   ║
║                                                            ║
║ auth-refactor:    9200t (77%)  ↓ Improved                 ║
║ state-mgmt:       10500t (88%) ↑ More complex             ║
║ api-redesign:     12000t (100%) = Same as budget           ║
║                                                            ║
║ Trend: Token usage decreasing as patterns improve ✓       ║
╚════════════════════════════════════════════════════════════╝
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
IF tokens > budget * 0.8:
  1. Run report (identify expensive phase)
  2. Suggest optimizations:
     a. Use 3-layer query rule more (save Layer 3 reads)
     b. Enable caveman compression (save ~30% in lessons)
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

### `.spekificity/config.yaml`

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
