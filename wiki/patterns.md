# Pattern Library: Reusable Patterns from Spekificity

Quick index to 24+ patterns. **Full specifications** are in [decision.md](decision.md), [architecture.md](architecture.md), and [workflow.md](workflow.md). Use this page to find patterns by problem; follow links to detailed specs.

---

## Quick Reference

| # | Pattern | Category | Problem Solved | Status | Spec Location |
|---|---------|----------|----------------|--------|---------------|
| 1 | Decorator Wrapper | Architectural | Extend without modifying internals | ✅ ACTIVE | [architecture.md](architecture.md) |
| 2 | Three-Layer Memory | Architectural | Persist context across sessions | ✅ ACTIVE | [architecture.md](architecture.md) |
| 3 | Three-Layer Query Rule | Query | Optimize token usage hierarchically | 🟢 ADOPT SOON | [decision.md#decision-6](decision.md#decision-6-3-layer-query-rule-hierarchical-context-loading) |
| 4 | Enrichment Layer | Architectural | Inject context into SpecKit | ✅ ACTIVE | [architecture.md](architecture.md) |
| 5 | Context Injection | Integration | Load & compose context | ✅ ACTIVE | [architecture.md](architecture.md) |
| 6 | Feature Lifecycle | Workflow | End-to-end orchestration | ✅ ACTIVE | [workflow.md](workflow.md) |
| 7 | Error Categorization | Error Handling | Classify errors for recovery | ✅ ACTIVE | [decision.md](decision.md) |
| 8 | Zettelkasten | Memory | Atomic notes + frontmatter | 🟢 ADOPT SOON | [decision.md#decision-4](decision.md#decision-4-zettelkasten-architecture-for-vault-notes-recommended-default) |
| 9 | Caveman Compression | Compression | Reduce tokens substantially | ✅ ACTIVE | [decision.md#decision-3](decision.md#decision-3-toolset-recommendations-for-the-four-pillars) |
| 10 | Auto-Tagging | Memory | Automate knowledge links | 🟢 ADOPT SOON | [decision.md#decision-5](decision.md#decision-5-auto-tagging--auto-wikilink-insertion) |
| 11 | Skill Chaining | Integration | Sequential execution | ✅ ACTIVE | [workflow.md](workflow.md) |
| 12 | Post-Processing | Workflow | Artifact → compress → archive | ✅ ACTIVE | [workflow.md](workflow.md) |
| 13 | Hybrid Graph | Graph | Unify code + doc nodes | 📅 FUTURE | [architecture.md](architecture.md) |
| 14 | Graph Merge | Graph | Combine node types | 📅 FUTURE | [architecture.md](architecture.md) |
| 15 | Incremental Sync | Graph | Cache + file watch | 🟢 ADOPT SOON | [decision.md#decision-7](decision.md#decision-7-git-hooks-integration-for-automatic-graph-refresh) |
| 16 | Feature State | State Mgmt | Track lifecycle phases | ✅ ACTIVE | [workflow.md](workflow.md) |
| 17 | Session-to-Vault | Memory | Ephemeral → permanent | 🟢 ADOPT SOON | [decision.md#decision-5](decision.md#decision-5-auto-tagging--auto-wikilink-insertion) |
| 18 | Anti-Sycophancy | Validation | Flag AI drift | 📅 FUTURE | [decision.md#decision-10](decision.md#decision-10-anti-sycophancy-validation-rules) |
| 19 | Blind Review | Validation | Anon. review | 📅 FUTURE | [decision.md#decision-11](decision.md#decision-11-blind-code-review-optional-second-pass-qa) |
| 20 | Backprop Reflex | Validation | Test failures → learning | 🟡 CONSIDER | [decision.md#decision-8](decision.md#decision-8-backprop-reflex-test-failures--vault-updates) |
| 21 | RARV Reflection | Validation | Alignment cycle | 🟡 CONSIDER | [decision.md#decision-9](decision.md#decision-9-rarv-reflection-cycles-reason-act-reflect-verify) |
| 22 | Token Budget | Compression | Monitor costs | 📅 FUTURE | [decision.md#decision-12](decision.md#decision-12-token-budget-model-soft-limits-not-hard-caps) |
| 23 | Fallback Hierarchy | Error Handling | Graceful degradation | ✅ ACTIVE | [architecture.md](architecture.md) |
| 24 | Sequential Recovery | Error Handling | Pre-core-post recovery | ✅ ACTIVE | [architecture.md](architecture.md) |

**Legend:** ✅ ACTIVE | 🟢 ADOPT SOON | 🟡 CONSIDER | 📅 FUTURE

---

## Adoption Priority

**HIGH (implement now):** Patterns 1-7, 9, 11-12, 16, 23-24  
**MEDIUM:** Patterns 8, 10, 15, 17, 20-21  
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

