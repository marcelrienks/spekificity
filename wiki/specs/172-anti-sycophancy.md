# ⚠️ REDIRECT: Anti-Sycophancy Validation Rules

**This specification has been consolidated into a single archive file.**

**Status:** REDIRECTED (Consolidated 2026-05-20)  
**Original ID:** C.3.8  
**See:** [Validation Patterns Archive](validation-patterns-archive.md#section-1-anti-sycophancy-validation-rules)

---

## Purpose

Prevent AI drift by enforcing **explicit validation rules** that:
1. Flag contradictions between new decisions and vault
2. Alert when recent patterns suggest different approach
3. Question scope/complexity increases without justification
4. Prevent over-agreement with context
5. Keep AI accountable to architectural decisions

**Goal:** For solo developers, catch AI hallucinations or drift before they impact code quality.

---

## Scope & Relationships

**What this spec covers:**
- Anti-sycophancy rule definitions
- Rule enforcement in `/spek.automate` phases and `/spek.implement`
- Conflict detection logic
- User override mechanism
- Configuration (project-specific rules)

**What this spec does NOT cover:**
- Code review logic (see C.3.9)
- Test validation (see C.3.6)
- Decision updates (see C.3.7)

---

## Success Criteria

- ✅ Contradiction detection identifies spec vs vault decision conflicts (flags HIGH priority)
- ✅ Complexity increase rule flags specs 50% above baseline (with justification required)
- ✅ Pattern consistency rule alerts when recent patterns suggest different approach
- ✅ Scope validation catches silent scope creep (vs similar past features)
- ✅ Configuration allows project-specific rules (customizable thresholds)
- ✅ User override mechanism permits justified deviations with documented reason
- ✅ All conflicts logged with rationale (for learning + future pattern extraction)

---

## Related Specs

- C.3.1-C.3.5: Phase 1 foundations
- C.3.7: RARV Reflection (complements anti-sycophancy)

---

## Anti-Sycophancy Rules

### Rule 1: Contradiction Detection

**Rule:** If spec contradicts vault decisions, flag conflict

**Example:**
```
Vault Decision: "Use dependency injection pattern"
Spec Proposes: "Inject via service locator"

Conflict: "Spec contradicts wiki/vault/decision-use-di.md"
Alert Level: HIGH
User Action Required: Justify deviation or align with decision
```

**Implementation:**

```
For each spec requirement:
  1. Extract architectural choice
  2. Check wiki/vault/decisions.md for related decisions
  3. If contradiction found:
     a. Alert: "Spec contradicts vault decision [X]"
     b. Show rationale from vault
     c. Require user justification for deviation
```

### Rule 2: Complexity Increases

**Rule:** If spec complexity > 50% higher than similar past features, question

**Example:**
```
Recent Feature (auth): 1200 LOC, 2 components, 6 patterns
Current Spec (payment): 2000 LOC estimate, 5 components, 12 patterns

Complexity increase: 67% (1200 → 2000 LOC)
Alert: "Complexity 67% higher than similar features; justify additional scope"
```

**Implementation:**

```
1. Get similar past features from wiki/vault/lessons
2. Calculate average LOC + patterns
3. If current estimate > (avg * 1.5):
   a. Alert user
   b. Require justification
   c. Allow override with documented reason
```

### Rule 3: Pattern Consistency

**Rule:** If 3+ recent patterns suggest different approach, flag

**Example:**
```
Vault Patterns (last 5 features):
  - Observer pattern (3 uses): for event handling
  - Singleton pattern (2 uses): for service management
  - Factory pattern (2 uses): for creation

Current Spec Proposes:
  - Direct event subscription (not observer)
  - Multiple service instances (not singleton)

Alert: "Contradicts pattern consensus; suggest [[observer-pattern]] + [[singleton-pattern]]"
```

**Implementation:**

```
1. Count pattern usage across recent features
2. Identify consensus patterns for domain
3. If spec deviates:
   a. Alert: "Deviates from pattern consensus"
   b. Show recommended patterns
   c. Require override justification
```

### Rule 4: Technology Stack Drift

**Rule:** If spec uses new tech not in vault, require justification

**Example:**
```
Vault Tech Stack: TypeScript, React, Node.js, Jest
Spec Proposes: Add Rust for performance

Alert: "New technology Rust not in current stack; justify addition"
```

**Implementation:**

```
1. Extract tech stack from wiki/vault/decisions
2. Scan spec for new technologies
3. If new tech found:
   a. Alert: "New tech [X]; not in current stack"
   b. Require justification document
   c. Add to tech stack decision if approved
```

### Rule 5: Scope Creep Detection

**Rule:** If scope grows during feature work, question

**Example:**
```
Original Spec: "Add password reset flow"
Plan: "Add password reset + email notifications"
Implementation: "Add password reset + email + SMS + backup codes"

Scope creep: 3 additional items
Alert: "Scope grew 200%; verify with stakeholder or reduce"
```

**Implementation:**

```
During implementation:
  1. Compare original spec vs current tasks
  2. Identify scope additions
  3. Alert: "Added [N] items beyond spec; confirm intended"
```

---

## Validation Points

### During `/spek.automate` specify phase

```
/spek.automate (specify phase with anti-sycophancy):

After spec generated:
  1. Run Rule 1: Check for vault contradictions
  2. Run Rule 2: Check complexity vs similar features
  3. Run Rule 3: Check pattern suggestions
  4. Run Rule 4: Check tech stack alignment
  
  Alerts found? → Show to user
  User can: Accept / Modify / Override with justification
```

### During `/spek.automate` plan phase

```
/spek.automate (plan phase with anti-sycophancy):

After plan generated:
  1. Run Rule 1: Check architecture vs decisions
  2. Run Rule 3: Check pattern alignment
  3. Run Rule 2: Check scope complexity
  
  Alerts found? → Show to user
  User can: Accept / Re-plan / Override with justification
```

### During /spek.implement

```
/spek.implement (with anti-sycophancy):

Mid-implementation:
  1. Run Rule 5: Monitor for scope creep
  2. Run Rule 1: Check tech choices vs stack
  
  Alerts found? → Surface before too much work done
  User can: Continue / Re-plan / Reduce scope
```

---

## Configuration: Project Rules

### `.spekificity/validation-rules.md`

Create per-project rules (team + solo):

```markdown
# Validation Rules (Anti-Sycophancy)

## Spec Generation Rules (`/spek.automate` specify phase)

### Rule: No contradictions with vault decisions
- **Trigger:** Spec proposes something conflicting vault
- **Action:** ALERT - show vault rationale
- **Override:** Allowed with justification

### Rule: Complexity within 50% of similar features
- **Trigger:** Estimated LOC > 1.5x similar feature
- **Action:** ALERT - question scope
- **Override:** Allowed with stakeholder approval

### Rule: Use established patterns
- **Trigger:** Spec avoids consensus pattern
- **Action:** ALERT - suggest pattern + show usage
- **Override:** Allowed with new-pattern-name justification

### Rule: Stay within tech stack
- **Trigger:** Spec introduces new technology
- **Action:** ALERT - show current stack
- **Override:** Allowed with tech-evaluation document

## Plan Generation Rules (`/spek.automate` plan phase)

### Rule: Architecture aligns with decisions
- **Trigger:** Plan violates wiki/vault/decision-*.md
- **Action:** ALERT - show decision + rationale
- **Override:** Allowed; may trigger RARV reflection

### Rule: Use established patterns
- **Trigger:** Plan reinvents wheel
- **Action:** ALERT - suggest wiki/vault/patterns
- **Override:** Allowed with innovation-memo

## Implementation Rules (/spek.implement)

### Rule: No scope creep
- **Trigger:** Tasks added beyond plan
- **Action:** ALERT - list new items
- **Override:** Allowed; log for post-mortem

### Rule: Code follows patterns
- **Trigger:** Code style drifts from similar modules
- **Action:** WARNING - suggest refactor
- **Override:** Allowed; document exception

## Appendix: Vault References

Decisions:
- [[use-dependency-injection-pattern]]
- [[error-handling-recovery]]
- [[token-lifecycle-decision]]

Patterns:
- [[singleton-pattern]]
- [[observer-pattern]]
- [[factory-pattern]]

Tech Stack:
- TypeScript (mandatory for new code)
- React (UI framework)
- Node.js (backend runtime)
- Jest (test framework)
```

---

## Rule Override Mechanism

### When User Overrides

```
Alert: "Spec contradicts [[use-di-pattern]]; proceed anyway?"

User choice: "Yes, but [JUSTIFICATION]"

System action:
  1. Record override with justification
  2. Add to feature session log
  3. Flag for RARV reflection later
  4. Proceed with spec
  5. Alert post-mortem: "Review override at feature end"
```

### Tracking Overrides

Store in `/memories/session/current-feature.md`:

```markdown
## Validation Rule Overrides

1. **Rule:** Complexity (1.5x higher than auth-refactor)
   **Override:** Proceed with payment feature scope
   **Justification:** Stakeholder approved complex integration

2. **Rule:** Use DI pattern
   **Override:** Use service locator for compatibility
   **Justification:** Integrating with legacy system; DI not applicable

→ [At feature end, RARV reviews overrides; decides if vault should update]
```

---

## Success Criteria

- ✅ Rules 1-5 implemented in `/spek.automate` phases and `/spek.implement`
- ✅ Contradictions detected + alerted (Rule 1)
- ✅ Complexity increases questioned (Rule 2)
- ✅ Pattern deviations flagged (Rule 3)
- ✅ Tech stack drift prevented (Rule 4)
- ✅ Scope creep detected (Rule 5)
- ✅ Override mechanism tracks justifications
- ✅ Project-specific rules in `.spekificity/validation-rules.md`
- ✅ Solo devs protected from AI drift
- ✅ All overrides reviewed in RARV (C.3.7)

---

## Related Specifications

- **C.3.1-C.3.5:** Phase 1 foundations (vault, decisions, patterns)
- **C.3.7:** RARV Reflection (reviews overrides, decides vault updates)
- **B.10:** SDD Framework Comparison (source: Loki Mode)

---

## References

- **Production Source:** https://github.com/Loki-Mode/loki-mode (930⭐, anti-sycophancy rules)
- **Constraint Checking:** Rule engines, validation frameworks
