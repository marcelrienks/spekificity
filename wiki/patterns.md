# Pattern Library: Reusable Patterns from Spekificity

Quick index to 24+ patterns. **Full specifications** are in [decision.md](decision.md), [architecture.md](architecture.md), and [workflow.md](workflow.md). Use this page to find patterns by problem; follow links to detailed specs.

---

## Quick Reference

| # | Pattern | Category | Problem Solved | Phase | Status |
|---|---------|----------|----------------|-------|--------|
| 1 | Decorator Wrapper | Architectural | Extend without modifying internals | Phase 0 | ✅ ACTIVE |
| 2 | Three-Layer Memory | Architectural | Persist context across sessions | Phase 0 | ✅ ACTIVE |
| 3 | Three-Layer Query Rule | Query | Optimize token usage hierarchically | Phase 1 | 🟢 S3 |
| 4 | Enrichment Layer | Architectural | Inject context into SpecKit | Phase 1 | ✅ ACTIVE |
| 5 | Context Injection | Integration | Load & compose context | Phase 1 | ✅ ACTIVE |
| 6 | Feature Lifecycle | Workflow | End-to-end orchestration | Phase 1 | ✅ ACTIVE |
| 7 | Error Categorization | Error Handling | Classify errors for recovery | Phase 0 | ✅ ACTIVE |
| 8 | Zettelkasten | Memory | Atomic notes + frontmatter | Phase 1 | 🟢 S1 |
| 9 | Caveman Compression | Compression | Reduce tokens substantially | Phase 0 | ✅ ACTIVE |
| 10 | Auto-Tagging | Memory | Automate knowledge links | Phase 1 | 🟢 S2 |
| 11 | Skill Chaining | Integration | Sequential execution | Phase 1 | ✅ ACTIVE |
| 12 | Post-Processing | Workflow | Artifact → compress → archive | Phase 1 | ✅ ACTIVE |
| 13 | Hybrid Graph | Graph | Unify code + doc nodes | Phase 1 | 📅 FUTURE |
| 14 | Graph Merge | Graph | Combine node types | Phase 1 | 📅 FUTURE |
| 15 | Incremental Sync | Graph | Cache + file watch | Phase 1 | 🟢 S4 |
| 16 | Feature State | State Mgmt | Track lifecycle phases | Phase 1 | ✅ ACTIVE |
| 17 | Session-to-Vault | Memory | Ephemeral → permanent | Phase 1 | 🟢 S5 |
| 18 | Anti-Sycophancy | Validation | Flag AI drift | Phase 2 | 📅 FUTURE |
| 19 | Blind Review | Validation | Anon. review | Phase 2 | 📅 FUTURE |
| 20 | Backprop Reflex | Validation | Test failures → learning | Phase 2 | 🟡 C1 |
| 21 | RARV Reflection | Validation | Alignment cycle | Phase 2 | 🟡 C2 |
| 22 | Token Budget | Compression | Monitor costs | Phase 2 | 📅 FUTURE |
| 23 | Fallback Hierarchy | Error Handling | Graceful degradation | Phase 0 | ✅ ACTIVE |
| 24 | Sequential Recovery | Error Handling | Pre-core-post recovery | Phase 0 | ✅ ACTIVE |

**Legend:** ✅ ACTIVE | 🟢 S1–S5 = Should adopt soon | 🟡 C1–C2 = Consider later | 📅 FUTURE = Research phase

---

## Pattern Summaries (Quick Reference)

Full specifications available in linked documents. Follow links for complete details.

| # | Pattern | Quick Desc | Spec Location |
|---|---------|-----------|---|
| 1 | Decorator Wrapper | Wrap SpecKit without modification | [architecture.md](architecture.md) |
| 2 | Three-Layer Memory | Vault → Repo Memory → Session Memory | [architecture.md](architecture.md) |
| 3 | Three-Layer Query Rule | Layer 1 (code graph) → Layer 2 (vault) → Layer 3 (raw code) | [decision.md#decision-6](decision.md#decision-6-3-layer-query-rule-hierarchical-context-loading) |
| 4 | Enrichment Layer | Inject context into SpecKit phases | [architecture.md](architecture.md) |
| 5 | Context Injection | Load vault + repo memory + code graph | [architecture.md](architecture.md) |
| 6 | Feature Lifecycle | 4 stages: Prepare → Plan → Implement → Conclude | [workflow.md](workflow.md) |
| 7 | Error Categorization | Classify errors by type + recovery | [decision.md](decision.md) |
| 8 | Zettelkasten | Atomic notes + YAML frontmatter + wikilinks | [decision.md#decision-4](decision.md#decision-4-zettelkasten-architecture-for-vault-notes-recommended-default) |
| 9 | Caveman Compression | Terse, accurate output | [decision.md#decision-3](decision.md#decision-3-toolset-recommendations-for-the-four-pillars) |
| 10 | Auto-Tagging | Keyword extraction → vault mapping → auto-insert | [decision.md#decision-5](decision.md#decision-5-auto-tagging--auto-wikilink-insertion) |
| 11 | Skill Chaining | Execute dependent skills in sequence | [workflow.md](workflow.md) |
| 12 | Post-Processing | Collect → compress → extract lessons → update vault → refresh | [workflow.md](workflow.md) |
| 13 | Hybrid Graph | Unify code + doc nodes | [architecture.md](architecture.md) (future) |
| 14 | Graph Merge | Combine code + doc node types | [architecture.md](architecture.md) (future) |
| 15 | Incremental Sync | Cache + file watch for efficient updates | [decision.md#decision-7](decision.md#decision-7-git-hooks-integration-for-automatic-graph-refresh) |
| 16 | Feature State Tracking | Track lifecycle phases in session memory | [workflow.md](workflow.md) |
| 17 | Session-to-Vault Archival | Convert ephemeral → permanent vault artifacts | [decision.md#decision-5](decision.md#decision-5-auto-tagging--auto-wikilink-insertion) |
| 18 | Anti-Sycophancy | Flag contradictions + complexity increases | [decision.md#decision-10](decision.md#decision-10-anti-sycophancy-validation-rules) |
| 19 | Blind Review | Anon code review + independent checks | [decision.md#decision-11](decision.md#decision-11-blind-code-review-optional-second-pass-qa) |
| 20 | Backprop Reflex | Test failures → vault warnings/lessons | [decision.md#decision-8](decision.md#decision-8-backprop-reflex-test-failures--vault-updates) |
| 21 | RARV Reflection | Code vs. spec alignment cycle | [decision.md#decision-9](decision.md#decision-9-rarv-reflection-cycles-reason-act-reflect-verify) |
| 22 | Token Budget Tracking | Soft limits + warnings per phase | [decision.md#decision-12](decision.md#decision-12-token-budget-model-soft-limits-not-hard-caps) |
| 23 | Fallback Hierarchy | Graceful degradation via layered fallbacks | [architecture.md](architecture.md) |
| 24 | Sequential Error Recovery | PRE-CORE-POST error handling | [architecture.md](architecture.md) |

---

## Adoption Priority

**HIGH (implement now):** Patterns 1-7, 9, 11-12, 16, 23-24  
**MEDIUM (target S2):** Patterns 8, 10, 15, 17, 20-21  
**FUTURE:** Patterns 13-14, 18-19, 22

---

## Pattern Index by Use Case

**Spec-Driven Development (Specify Phase):**
Decorator Wrapper, Context Injection, Enrichment Layer, Anti-Sycophancy, Three-Layer Query Rule, Three-Layer Memory

**Planning & Architecture (Plan Phase):**
Enrichment Layer, Context Injection, Hybrid Graph, Code Graph Query, Token Budget Tracking

**Implementation (Implement Phase):**
Decorator Wrapper, Sequential Error Recovery, Fallback Hierarchy, Blind Code Review

**Post-Feature (Post Phase):**
Post-Processing, Caveman Compression, Feature State Tracking, Session-to-Vault Archival, Auto-Tagging, RARV Reflection, Backprop Reflex

**Knowledge Persistence:**
Three-Layer Memory, Zettelkasten, Auto-Tagging, Session-to-Vault Archival

**Error Handling & Resilience:**
Error Categorization, Fallback Hierarchy, Sequential Error Recovery

**Performance & Efficiency:**
Three-Layer Query Rule, Code Graph Query, Incremental Sync, Caveman Compression, Token Budget

**Quality & Validation:**
Anti-Sycophancy, Blind Code Review, RARV Reflection, Backprop Reflex

**Orchestration & Workflow:**
Feature Lifecycle, Skill Chaining, Feature State Tracking

**Knowledge Graphs & Queries:**
Hybrid Graph, Graph Merge, Incremental Sync, Code Graph Query

---

## Full Specifications

For complete pattern specifications (problem statement, solution, trade-offs, when to use), see links in the Quick Reference table above.

---

## How to Use This Document

1. **Quick Discovery:** Scan "Quick Reference" table by category or problem
2. **Find Details:** Follow links from pattern summaries to full specs
3. **Design by Use Case:** Use "Pattern Index by Use Case" to find relevant patterns
4. **Adoption:** Check phase and status; implement HIGH-priority patterns first

---

**Document Version:** 2026-06-06  
**Pattern Count:** 24 active + proposed  
**Last Updated:** 2026-06-06
