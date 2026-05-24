# ⚠️ REDIRECT: RARV Reflection Cycles: Reason-Act-Reflect-Verify

**This specification has been consolidated into a single archive file.**

**Status:** REDIRECTED (Consolidated 2026-05-20)  
**Original ID:** C.3.7  
**See:** [Validation Patterns Archive](validation-patterns-archive.md#section-3-rarv-reflection-cycle-reason-act-reflect-verify)

---

## Purpose

Implement continuous alignment verification loop that:
1. **Reasons:** Did implementation match spec?
2. **Acts:** Fix any spec/plan/code deviations
3. **Reflects:** Update decisions if justified
4. **Verifies:** Re-validate against original decisions

**Goal:** Prevent spec drift; ensure code aligns with architectural decisions; catch misalignments early before they accumulate.

**Loop:** Can run after implementation, or periodically during long features.

---

## Scope & Relationships

**What this spec covers:**
- Code-to-spec comparison (auto-diff analysis)
- Deviation detection + classification
- Reflection loop logic (re-plan if needed)
- Integration into `/spek.conclude` (post-implementation analysis)
- Optional re-entry points (run mid-feature if desired)
- Decision alignment verification

**What this spec does NOT cover:**
- Code review process (see C.3.9 Blind Review)
- Test execution (assume exists from C.3.6)
- Spec/plan editing (assume done manually with re-run)

**Related specs:**
- B.8.4: Post Command (Step 7 optional integration point)
- C.3.1-C.3.5: Phase 1 specs (context for comparison)
- C.3.6: Backprop Reflex (failure patterns feed into reflection)

---

## Success Criteria

- ✅ Code-to-spec comparison detects deviations (scope creep, missing features, architecture divergence)
- ✅ Deviation classification accurate (addition/omission/divergence categorized correctly)
- ✅ User choice mechanism working (A/B/C options clear, override documented)
- ✅ Reflection loop updates decisions (new rationale captured in vault)
- ✅ Verification re-validates against decisions (alignment checked)
- ✅ Loop prevents spec drift (misalignments caught before accumulating)
- ✅ Integration seamless (optional in `/spek.conclude` workflow)

---

## RARV Cycle: 4 Phases

### Phase 1: REASON - Code vs. Spec Comparison

**When:** After `/spek.implement` completes, before `/spek.conclude`

**Process:**

```
1. Get original spec (spec.md)
2. Get final plan (plan.md)
3. Get implemented code (diff from branch)
4. Compare:
   a. Spec requirements → Implemented features
   b. Plan architecture → Actual structure
   c. Feature scope → Delivered code
5. Identify deviations:
   - Scope creep (code adds beyond spec)
   - Missing features (spec requires, code doesn't have)
   - Architecture divergence (plan says X, code does Y)
```

**Output:**

```yaml
reason_results:
  spec_coverage: 95%  # % of spec requirements met
  scope_changes: [
    {
      type: "addition",
      item: "batch token refresh endpoint",
      reason: "not in original spec, added for performance"
    },
    {
      type: "omission",
      item: "audit logging for token refresh",
      reason: "deferred to v2"
    }
  ]
  architecture_alignment: 92%
  deviations: [
    {
      plan_says: "singleton auth service",
      code_does: "factory pattern for auth service",
      impact: "medium (affects testability)"
    }
  ]
```

### Phase 2: ACT - Fix Deviations

**When:** User reviews REASON output

**Choices:**

```
For each deviation:
  Option A: Fix code to match spec
    → Regenerate plan if needed
    → Re-implement
    → Re-run tests
  
  Option B: Update spec to justify deviation
    → Document rationale
    → Update spec.md + plan.md
    → Accept deviation
  
  Option C: Defer to next feature
    → Create tech debt item
    → Document in decisions
    → Continue
```

**User Workflow:**

```
1. Review REASON output
2. For each deviation:
   a. Understand the deviation
   b. Choose A/B/C
3. Execute changes (if any)
4. Continue to Phase 3 (REFLECT)
```

**Example:**

```
Deviation: Code uses factory pattern, plan says singleton

User choice: Accept (Option B)
Rationale: "Factory provides better testability; original spec didn't mandate singleton"

Action:
  1. Update plan.md: "Use factory pattern instead of singleton"
  2. Update decisions: "Why factory: testability > simplicity in this case"
  3. Continue to Phase 3
```

### Phase 3: REFLECT - Update Decisions

**When:** After deviations resolved (or accepted)

**Process:**

```
1. Compare final implementation against decisions in vault
2. For each decision that changed:
   a. Was change justified? (document rationale)
   b. Should this decision be updated? (affect future features?)
   c. Is this a new pattern? (add to wiki/vault/patterns.md)
3. Update vault with decision changes
4. Add reflection notes to feature lesson
```

**Output:**

```yaml
reflect_results:
  decisions_verified: 7
  decisions_changed: 2
  new_patterns_discovered: 1
  
  changed_decisions:
    - decision: "use singleton for auth service"
      change: "use factory instead"
      rationale: "better testability, lower coupling"
      action: "update wiki/vault/decision-auth-service-pattern.md"
    
    - decision: "token expiry: 1 hour"
      change: "token expiry: 30 minutes"
      rationale: "security audit recommendation"
      action: "update wiki/vault/decision-token-lifecycle.md"
  
  new_patterns:
    - name: "Factory pattern for service creation"
      source: "discovered in auth service implementation"
      action: "add to wiki/vault/patterns/factory-pattern.md"
```

### Phase 4: VERIFY - Re-Validate Against Decisions

**When:** After Phase 3 (REFLECT) changes applied

**Process:**

```
1. Re-run original decision checks
2. Verify new/updated decisions are consistent
3. Check for conflicts between decisions
4. Verify code still passes tests
5. Report alignment status
```

**Output:**

```yaml
verify_results:
  all_decisions_aligned: true
  code_tests_passing: true
  no_conflicts_detected: true
  alignment_score: 98%
  
  status: "✓ RARV cycle complete; implementation aligned with decisions"
```

---

## RARV Loop Logic

### Simple 1-Pass (Most Features)

```
Spec → Plan → Implement → RARV (Reason-Act-Reflect-Verify) → Post
  ↑                                                             ↓
  └─────────────────────────────────────────────────────────────┘
                     If major deviations: loop back
```

### Multi-Pass (Complex Features)

```
Spec → Plan → Implement (Phase 1) 
  → RARV: Reasons shows issues
  → ACT: Fix code/spec/plan
  → Implement (Phase 2)
  → RARV again: Reasons shows alignment
  → REFLECT + VERIFY
  → Post
```

### Early Reflection (Optional)

```
Users can trigger RARV mid-feature:

During implementation, if uncertain:
  → Run /spek.rarv
  → See Reason output (deviations so far)
  → Adjust plan/code
  → Continue implementation
```

---

## Integration: /spek.conclude Enhancement

### Current Workflow (B.8.4)

```
/spek.conclude Step 7: [optional] Reflection
  (Currently skipped or manual)

/spek.conclude Step 8: Simplify Docs
/spek.conclude Step 9: Archive Session
/spek.conclude Step 10: Report Complete
```

### Enhanced with RARV (C.3.7)

```
/spek.conclude Step 7: RARV Reflection Cycle (Enhanced)

  7.1. REASON: Compare code vs. spec
       - Analyze scope coverage (spec requirements met?)
       - Detect architecture divergence
       - Identify missed features or scope creep
       - Output alignment report
  
  7.2. ACT: Fix deviations (if any)
       - User reviews deviations
       - User chooses: Fix/Accept/Defer
       - Auto-regenerate plan if major changes
  
  7.3. REFLECT: Update decisions + patterns
       - For each deviation: should decision update?
       - Add new patterns discovered
       - Document rationale in vault
  
  7.4. VERIFY: Re-validate alignment
       - Check all decisions still consistent
       - Run final tests
       - Report alignment score

→ If alignment < 90%: Alert user
→ If alignment >= 90%: Continue to Step 8
```

### Implementation Pseudocode

```python
def rarv_reflection_cycle():
    """RARV cycle: Reason → Act → Reflect → Verify"""
    
    # Phase 1: REASON
    print("Phase 1: Reasoning about spec vs. code...")
    spec = read_file("spec.md")
    plan = read_file("plan.md")
    code_diff = get_git_diff("main", "HEAD")
    
    reason_output = compare_spec_to_code(spec, plan, code_diff)
    print(f"Alignment: {reason_output['spec_coverage']}%")
    print(f"Deviations: {len(reason_output['deviations'])}")
    
    if len(reason_output['deviations']) == 0:
        print("✓ Code perfectly matches spec; skipping ACT")
        return rarv_reflect(reason_output)
    
    # Phase 2: ACT
    print("Phase 2: Fixing deviations...")
    for deviation in reason_output['deviations']:
        user_choice = prompt_user(deviation)  # Fix/Accept/Defer
        
        if user_choice == "fix":
            print(f"  → Re-implementing: {deviation['item']}")
            regenerate_and_reimplement(deviation)
            code_diff = get_git_diff("main", "HEAD")
        
        elif user_choice == "accept":
            print(f"  → Accepting deviation (updating spec): {deviation['item']}")
            update_spec_and_plan(deviation)
    
    # Re-run REASON after fixes
    reason_output = compare_spec_to_code(read_file("spec.md"), 
                                         read_file("plan.md"), 
                                         get_git_diff("main", "HEAD"))
    
    # Phase 3: REFLECT
    print("Phase 3: Reflecting on decisions...")
    reflect_output = update_vault_decisions(reason_output)
    
    # Phase 4: VERIFY
    print("Phase 4: Verifying alignment...")
    verify_output = verify_all_decisions_aligned(reflect_output)
    
    if verify_output['alignment_score'] < 90:
        print("⚠ Alignment < 90%; recommend re-planning")
    else:
        print(f"✓ RARV complete; alignment: {verify_output['alignment_score']}%")
    
    return verify_output

def rarv_reflect(reason_output):
    """Shortcut: REFLECT + VERIFY if no deviations"""
    reflect_output = update_vault_decisions(reason_output)
    verify_output = verify_all_decisions_aligned(reflect_output)
    return verify_output
```

---

## Decision Alignment Verification

### What Gets Checked

**1. Scope Alignment**
```
Decision: "Token refresh happens every 1 hour"
Code: "Token refresh every 30 minutes"
Alignment: 70% (code is more conservative)
Question: "Should we update decision to 30 minutes?"
```

**2. Architecture Alignment**
```
Decision: "Use singleton for auth service"
Code: "Use factory for auth service"
Alignment: 85% (both valid, different tradeoffs)
Question: "Was factory necessary? Should we document in decisions?"
```

**3. Pattern Alignment**
```
Decision: "Apply observer pattern for events"
Code: "Observer pattern implemented in 3/5 components"
Alignment: 60% (incomplete implementation)
Question: "Should we defer pattern to v2? Or finish implementation?"
```

---

## User Workflows

### Happy Path: Spec → Code Perfect Alignment

```
1. /spek.conclude Step 7: RARV starts
2. REASON phase: "Alignment: 98%; 1 minor deviation found"
3. ACT phase: User accepts deviation (added logging for debugging)
4. REFLECT phase: Vault updated (no decision changes)
5. VERIFY phase: "✓ Alignment: 99%; ready for production"
6. Continue to Step 8
```

### Spec Drift Caught & Fixed

```
1. /spek.conclude Step 7: RARV starts
2. REASON phase: "Alignment: 72%; 4 major deviations found"
   - Missed: Audit logging
   - Added: Batch refresh endpoint
   - Changed: Service pattern (factory vs singleton)
   - Deferred: Rate limiting

3. ACT phase: 
   - User fixes: "Implement audit logging"
   - User accepts: "Batch refresh is good; update spec"
   - User defers: "Rate limiting to v2"

4. REFLECT phase: 
   - Updated decision: "Why factory better than singleton"
   - Added pattern: "Batch API pattern"
   - Added tech debt: "Rate limiting v2"

5. VERIFY phase: "✓ Alignment: 94%; all decisions consistent"
6. Continue to Step 8
```

### Mid-Feature Reflection

```
User: "I'm implementing auth, but uncertain about service pattern"

Command: /spek.rarv --partial

Output: "Alignment so far: 85%; factory emerging as better choice"

User: "I'll continue with factory; update plan when done"

Later: /spek.conclude RARV confirms alignment, auto-updates decisions
```

---

## Configuration

### RARV Settings (`.spek/config.yaml`)

```yaml
rarv:
  enabled: true
  
  # Which phase to run by default
  default_phase: "reason-verify"  # or "reason-act-reflect-verify"
  
  # Thresholds
  min_alignment_score: 90  # Warn if below this
  alignment_definitions:
    # How to calculate alignment scores
    scope_coverage: 0.4  # Spec requirements met
    architecture_match: 0.35  # Plan vs code
    decision_consistency: 0.25  # Decisions reflected
  
  # Output
  fail_on_deviation: false  # Don't block post on low alignment
  generate_alignment_report: true
  
  # Re-planning
  auto_regenerate_plan_on_major_deviation: false  # Let user decide
```

---

## Success Criteria

- ✅ REASON phase compares code against spec with 80%+ accuracy
- ✅ ACT phase lets user choose: Fix/Accept/Defer
- ✅ REFLECT phase auto-updates vault decisions + patterns
- ✅ VERIFY phase confirms alignment > 90%
- ✅ Multi-pass loops supported (re-plan + re-implement if needed)
- ✅ Integrated into `/spek.conclude` Step 7
- ✅ Mid-feature `/spek.rarv` command available (optional)
- ✅ Alignment reports generated for every feature
- ✅ Decision drift prevented across features

---

## Related Specifications

- **B.8.4:** Post Command (Step 7 integration)
- **C.3.1:** Zettelkasten Conventions (reflect output format)
- **C.3.6:** Backprop Reflex (failure patterns feed into reflection)
- **B.10:** SDD Framework Comparison (source: Loki Mode)

---

## References

- **Production Source:** https://github.com/Loki-Mode/loki-mode (930⭐, RARV pattern)
- **Spec Alignment:** Semantic diff tools, AST comparison
- **Decision Consistency:** Constraint satisfaction problem (CSP) solving