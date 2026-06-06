# Pattern Library: Reusable Patterns from Spekificity

Quick reference to 24+ patterns. Each pattern links to its authoritative spec for full details.

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

## Pattern Summaries

### Architectural Patterns

**1. Decorator Wrapper** — Extend functionality without modifying internals. Wraps SpecKit with PRE (load context) → CORE (execute) → POST (validate output) layers.

**2. Three-Layer Memory** — Persist context across sessions via three layers: Vault (persistent, authoritative) → Repo Memory (compressed cache) → Session Memory (ephemeral).

**4. Enrichment Layer** — Inject context into SpecKit workflow phases (specify, plan, implement). PRE layer loads decisions+patterns+code graph; validates output post-execution.

---

### Query & Analysis Patterns

**3. Three-Layer Query Rule** — Hierarchical context loading: Layer 1 (Code Graph via lat.md) → Layer 2 (Vault summaries) → Layer 3 (Raw Code Files). Use lower layers first; escalate only when necessary.

**5. Context Injection** — Load and inject context at pre-execution: Vault (decisions, patterns, lessons) → Repo Memory (compressed cache) → Code Graph (symbols, relationships).

---

### Workflow Patterns

**6. Feature Lifecycle** — End-to-end orchestration via 4 stages: Prepare → Specify → Plan → Implement → Conclude. Each phase validates preconditions and updates feature state.

**11. Skill Chaining** — Execute dependent skills in sequence with error resilience. Explicit dependency management; retry + fallback for failures.

**12. Post-Processing** — After implementation: collect artifacts → compress output → extract lessons → update vault → refresh code graph → archive session.

---

### Memory & Knowledge Patterns

**8. Zettelkasten** — Atomic notes (one concept per file) with YAML frontmatter (metadata) and wikilinks (2-4 per note). Enables automation: auto-tagging, graph exports, AI-friendly queries.

**10. Auto-Tagging & Auto-Wikilink** — Keyword extraction → Vault mapping → Auto-insert wikilinks during lesson generation. Reduces manual cross-referencing labor.

**17. Session-to-Vault Archival** — Convert ephemeral session context to permanent vault artifacts at feature end. Session notes → Zettelkasten format → Vault storage.

---

### Compression & Efficiency Patterns

**9. Caveman Compression** — Ultra-compressed communication style (terse, accurate). Three modes: Lite (modest), Full (substantial reduction, DEFAULT), Ultra (maximal).

**22. Token Budget Tracking** — Soft limits + warnings per phase. Track usage; enable cost-aware decisions without blocking progress.

---

### Error Handling Patterns

**7. Error Categorization** — Classify errors by type (Git, Vault, Graph, LLM, User) → Apply category-specific recovery. Ensures consistent handling across all skills.

**23. Fallback Hierarchy** — Graceful degradation via layered fallbacks: Layer 1 (primary) → Layer 2 (fallback) → Layer 3 (minimal). Continue with reduced capability on failure.

**24. Sequential Error Recovery** — Structured pre-core-post error handling. PRE (validation, fail fast) → CORE (retry or fallback) → POST (update memory or continue).

---

### Graph Patterns

**13. Hybrid Graph** — Unify code + doc nodes in single queryable graph. Query via lat.md MCP tools; enables code+doc relationship discovery.

**14. Graph Merge** — Combine heterogeneous node types: code nodes (from lat.md) + doc nodes (from Obsidian) → merged unified graph. Dedup, link discovery, backreference computation.

**15. Incremental Sync** — Cache + file watching for efficient updates. SHA256 caching; node index lookup; incremental (2-5s) or full rebuild (30-60s) modes.

---

### State Management Patterns

**16. Feature State Tracking** — Track feature lifecycle phases in `.spek/memory/session/current-feature.md`. State file shows: phase, completion %, session log.

---

### Validation Patterns

**18. Anti-Sycophancy** — Flag contradictions (spec vs. vault), complexity increases, pattern deviations, tech stack drift. Violations require documented override.

**19. Blind Review** — Anonymize code (remove AI markers, strip context) → Run independent checks (linting, tests, static analysis) → Flag issues independently.

**20. Backprop Reflex** — Capture test failure patterns at feature end; update vault with warnings/lessons. Failures feed backward into decisions.

**21. RARV Reflection** — After implementation, compare code vs. spec: Reason (identify deviations) → Act (fix code or justify change) → Reflect (update decisions) → Verify (check alignment).

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

## Full Pattern Specs

For complete pattern specifications (problem statement, solution, trade-offs, when to use, example code, related patterns), see:

- **Architectural Patterns:** [architecture.md](architecture.md) → Design Patterns section
- **Workflow Patterns:** [workflow.md](workflow.md) → Feature Development Workflow
- **Memory Patterns:** [decision.md](decision.md) → Decision 4-5 (Zettelkasten, Auto-Tagging)
- **Query & Efficiency:** [decision.md](decision.md) → Decision 6 (3-Layer Query Rule)
- **Error Handling:** [decision.md](decision.md) → Error Handling Patterns
- **Validation:** [decision.md](decision.md) → Decision 10-11 (Anti-Sycophancy, Blind Review)

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
