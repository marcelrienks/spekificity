# Acceptance Tests: SC-004 — Vault Context Injection (≥2 References)

**Scenario**: SC-004: Spec and plan contain ≥2 vault-grounded references  
**Feature**: 003-spek-full-workflow-cli  
**Test Date**: [fill on execution]  
**Tester**: [AI Agent / Developer]

---

## Test Scenario 1: Vault context visible in spec.md

**Given**:
- Vault has `vault/context/decisions.md` and `vault/context/patterns.md` with entries
- `vault/graph/index.md` exists with at least 5 nodes

**When**: `/spek.automate` runs the `spec` step with vault context injection

**Then**:
- [ ] `spec.md` references ≥1 decision from `vault/context/decisions.md` (by name or summary)
- [ ] `spec.md` references ≥1 pattern from `vault/context/patterns.md`
- [ ] Or: ≥1 existing codebase component from `vault/graph/nodes/` referenced by name
- [ ] Total vault-grounded references ≥ 2
- [ ] `[spek] ⚠ vault context not available` NOT present in AI session output (vault was available)

**Evidence**:
```bash
# check for vault-derived terms in spec.md
grep -i "decision\|pattern\|vault\|graph\|existing" specs/*/spec.md | head -10
wc -l specs/*/spec.md   # non-trivial spec produced
```

---

## Test Scenario 2: Vault absent — graceful fallback

**Given**: `vault/context/` does not exist or is empty

**When**: `/spek.automate` runs the `spec` step

**Then**:
- [ ] AI session output contains: `[spek] ⚠ vault context not available — proceeding without codebase context`
- [ ] Spec generation continues without error
- [ ] `spec.md` is created (possibly less specific)
- [ ] Exit code 0 (no hard failure)

**Evidence**:
```bash
# Temporarily rename vault to test
mv vault vault.bak
spek automate "test feature"
# AI session: invoke /spek.automate, check for warning message
mv vault.bak vault
```

---

## Test Scenario 3: Plan references architectural decisions

**Given**: Vault `decisions.md` has at least 2 entries

**When**: `/spek.automate` runs the `plan` step

**Then**:
- [ ] `plan.md` references ≥1 architectural constraint from `vault/context/decisions.md`
- [ ] Plan does not contradict any documented decision

**Evidence**:
```bash
cat vault/context/decisions.md
grep -i "decision\|architecture\|constraint" specs/*/plan.md | head -5
```
