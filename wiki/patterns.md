# Pattern Library: Reusable Patterns from Spekificity Architecture

**Status:** Complete  
**Version:** current
**Phases Covered:** Phase 0 (Foundation), Phase 1 (Agent Skills), Phase 2 (Validation & Optimization)  
**Total Patterns:** multiple distinct, reusable patterns

---

## Overview

This document catalogs all reusable architectural, workflow, and optimization patterns extracted from many specification files in Spekificity. Each pattern is:
- **Self-contained** — Solves a specific, recurring problem
- **Cross-referenced** — Links to specs, related patterns, and use cases
- **Actionable** — Includes examples, implementation notes, and integration points
- **Classified** — Grouped by domain (architectural, workflow, error handling, memory, query, compression, integration, validation, graph, state management)

**Purpose:** Enable pattern reuse across future features, document proven solutions, and provide a reference for architecture decisions.

---

## Quick Reference Table

| # | Pattern Name | Category | Problem | Primary Spec | Frequency | Adoption Priority |
|---|---|---|---|---|---|---|
| 1 | Decorator Wrapper Pattern | Architectural | Extend functionality without modifying internals | [decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md) | HIGH | ✅ ACTIVE |
| 2 | Three-Layer Memory Model | Architectural | Persist context across sessions | [memory-architecture.md](wiki/specs/memory-architecture.md) | HIGH | ✅ ACTIVE |
| 3 | Three-Layer Query Rule | Query | Optimize token usage via hierarchical queries | [3layer-query-rule.md](wiki/specs/3layer-query-rule.md) | HIGH | 🟢 S3 |
| 4 | Enrichment Layer Pattern | Architectural | Inject context into SpecKit commands | [enrichment-layer.md](wiki/specs/enrichment-layer.md) | HIGH | ✅ ACTIVE |
| 5 | Context Injection Pattern | Integration | Load & compose context for tool invocation | [context-layer.md](wiki/specs/context-layer.md) | HIGH | ✅ ACTIVE |
| 6 | Feature Lifecycle Pattern | Workflow | End-to-end feature orchestration | [cli-orchestration.md](wiki/specs/cli-orchestration.md) | HIGH | ✅ ACTIVE |
| 7 | Error Categorization Pattern | Error Handling | Classify errors for targeted recovery | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | HIGH | ✅ ACTIVE |
| 8 | Zettelkasten Convention Pattern | Memory | Atomic, interconnected notes with frontmatter | [zettelkasten-conventions.md](wiki/specs/zettelkasten-conventions.md) | MEDIUM | 🟢 S1 |
| 9 | Caveman Compression Mode | Compression | Reduce token usage substantially | [caveman-integration.md](wiki/specs/caveman-integration.md) | HIGH | ✅ ACTIVE |
| 10 | Auto-Tagging + Auto-Wikilink Pattern | Memory | Automate knowledge interconnection | [auto-tagging-wikilinks.md](wiki/specs/auto-tagging-wikilinks.md) | MEDIUM | 🟢 S2 |
| 11 | Skill Chaining Pattern | Integration | Sequential execution with dependencies | [spek-automate-workflow.md](wiki/specs/spek-automate-workflow.md) | HIGH | ✅ ACTIVE |
| 12 | Post-Processing Pattern | Workflow | Artifact collection → compression → archive | [101-conclude-processing.md](wiki/specs/101-conclude-processing.md) | HIGH | ✅ ACTIVE |
| 13 | Hybrid Graph Pattern | Graph | Unify code + doc + skill nodes | [code-and-document-maps.md](wiki/specs/code-and-document-maps.md) | MEDIUM | 📅 FUTURE |
| 14 | Graph Merge Integration Pattern | Graph | Combine heterogeneous node types | [graph-merge-integration.md](wiki/specs/graph-merge-integration.md) | MEDIUM | 📅 FUTURE |
| 15 | Incremental Sync Pattern | Graph | Cache + file watching for efficient updates | [graph-refresh-strategy.md](wiki/specs/graph-refresh-strategy.md) | MEDIUM | 🟢 S4 |
| 16 | Feature State Tracking Pattern | State Management | Track feature lifecycle phases | [feature-state-tracking.md](wiki/specs/feature-state-tracking.md) | HIGH | ✅ ACTIVE |
| 17 | Session-to-Vault Archival Pattern | Memory | Convert ephemeral context to permanent | [session-logs-vault-artifacts.md](wiki/specs/session-logs-vault-artifacts.md) | MEDIUM | 🟢 S5 |
| 18 | Anti-Sycophancy Validation Pattern | Validation | Flag AI drift & contradictions | [anti-sycophancy.md](wiki/specs/anti-sycophancy.md) | LOW | 📅 FUTURE |
| 19 | Blind Code Review Pattern | Validation | Anonymized independent review | [blind-code-review.md](wiki/specs/blind-code-review.md) | LOW | 📅 FUTURE |
| 20 | Backprop Reflex Pattern | Validation | Test failures → vault updates → better specs | [backprop-reflex.md](wiki/specs/backprop-reflex.md) | MEDIUM | 🟡 C1 |
| 21 | RARV Reflection Pattern | Validation | Reason-Act-Reflect-Verify alignment cycle | [rarv-reflection.md](wiki/specs/rarv-reflection.md) | LOW | 🟡 C2 |
| 22 | Token Budget Tracking Pattern | Compression | Allocate & monitor per-phase token costs | [token-budget.md](wiki/specs/token-budget.md) | MEDIUM | 📅 FUTURE |
| 23 | Fallback Hierarchy Pattern | Error Handling | Graceful degradation via layered fallbacks | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | HIGH | ✅ ACTIVE |
| 24 | Sequential Error Recovery Pattern | Error Handling | Pre-core-post with error classification | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | HIGH | ✅ ACTIVE |

**Adoption Legend:**
- ✅ ACTIVE: Currently implemented
- 🟢 S1–S5: SHOULD adopt (high priority, production-validated)
- 🟡 C1–C2: COULD adopt (medium priority, for future phases)
- 📅 FUTURE: Research/experimental, defer for now

---

## Adoption Guidance (From Research)

### High Priority (`S` tier) — Should Adopt Soon

**S1: Zettelkasten Conventions** (Atomic vault notes with YAML frontmatter)  
Enable graph navigation, make lessons discoverable, zero conflicts with current design. Dependencies: None.

**S2: Auto-Tagging + Auto-Wikilink** (Keyword extraction → vault mapping)  
Create natural interconnection, enable discovery, validate lessons against patterns. Dependencies: S1 (Zettelkasten).

**S3: 3-Layer Query Rule** (Graph → Vault → Code priority)  
Reduce token waste, already planned. Dependencies: None.

**S4: lat.md File Watcher (optional)** (Auto-sync on file changes)  
Keep index fresh, prevent stale queries. `lat.md` supports on-demand refresh and an optional file-watcher for incremental updates. Dependencies: lat.md setup spec.

**S5: Session Logs as Vault Artifacts** (Archive session memory)  
Provide audit trail, enable cross-feature discovery. Dependencies: S1, S2 (auto-linking).

### Medium Priority (`C` tier) — Consider for Future Phases

**C1: Backprop Reflex** (Test failures → vault updates)  
Reduce repeat mistakes, depends on automated testing infrastructure.

**C2: RARV Reflection** (Reason-Act-Reflect-Verify cycles)  
Continuous alignment, requires orchestration loop-back.

For details, see [research.md](research.md).

---

## Pattern Catalog (Detailed)

### CATEGORY 1: ARCHITECTURAL PATTERNS

---

## Pattern 1: Decorator Wrapper Pattern

**Category:** Architectural  
**Solves:** Extend functionality without modifying internals  
**Primary Spec:** [decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Spekificity needs to enrich SpecKit commands (specify, plan, implement) with context (decisions, patterns, code graph) without modifying SpecKit's internals. Hooks/middleware would require SpecKit modifications and vendor coupling.

### Solution
Implement decorator wrapper pattern: Pre-Execution (load context, validate inputs) → Core (call SpecKit) → Post-Execution (validate output, update memory).

```python
def spek_enriched_command(command_name, *args, **kwargs):
    try:
        # LAYER 1: PRE-EXECUTION
        context = load_context(command_name)
        enriched_inputs = validate_and_enrich_inputs(*args, context=context)
        
        # LAYER 2: CORE EXECUTION
        result = speckit_command(command_name, *enriched_inputs, **kwargs)
        
        # LAYER 3: POST-EXECUTION
        validated_result = validate_output(result)
        update_memory(validated_result)
        return validated_result
    except Exception as e:
        handle_error(e, command_name)
        return fallback_result(command_name)
```

### When to Use
- Extending third-party tools without coupling
- Adding cross-cutting concerns (logging, validation, enrichment)
- Maintaining vendor independence

### When NOT to Use
- When tool provides hooks/plugins (prefer hooks)
- For simple wrapping with single responsibility (prefer composition)
- When performance is critical (decorator adds overhead)

### Example Code / Integration
- **Used in:** `/spek.plan` (specify, plan, implement phases)
- **Enrichment layers:** context-layer.md (PRE), enrichment-layer.md (POST)
- **Related specs:** speckit-integration-contract.md

### Related Patterns
- Context Injection Pattern (data flow in PRE layer)
- Skill Chaining Pattern (orchestrates decorators)
- Sequential Error Recovery Pattern (error handling in PRE/POST)

### Specs Using This Pattern
- Primary: [decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md)
- Supporting: [enrichment-layer.md](wiki/specs/enrichment-layer.md), [speckit-integration-contract.md](wiki/specs/speckit-integration-contract.md)

---

## Pattern 2: Three-Layer Memory Model

**Category:** Architectural  
**Solves:** Persist context across sessions and features  
**Primary Spec:** [memory-architecture.md](wiki/specs/memory-architecture.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Agent context is lost between sessions. Each feature start requires re-reading decisions, patterns, and lessons. Token usage explodes; context is incomplete.

### Solution
Implement three-layer memory architecture:
- **Layer 1 (Vault):** Obsidian-based persistent store (decisions, patterns, lessons)
- **Layer 2 (Repo Memory):** Compressed cache in /memories/repo/ (recent decisions, index)
- **Layer 3 (Session Memory):** Ephemeral context in /memories/session/ (current feature state)

```
Layer 1: Vault (Obsidian) — Persistent, Authoritative
├── vault/decision.md
├── vault/intention.md
├── vault/patterns.md
└── vault/lessons/<YYYY-MM-DD>-<feature>-*.md

Layer 2: Repo Memory (Copilot) — Persistent, Project-Scoped
├── [056-code-and-document-maps.md](wiki/specs/056-code-and-document-maps.md)
├── [022-architectural-decisions.md](wiki/specs/022-architectural-decisions.md)
└── [023-patterns-library.md](wiki/specs/023-patterns-library.md)

Layer 3: Session Memory (Copilot) — Ephemeral, Session-Scoped
├── /memories/session/context-loaded.md
├── /memories/session/current-feature.md
└── /memories/session/scratchpad.md
```

### When to Use
- Multi-session workflows (features span multiple sessions)
- Knowledge preservation (decisions reusable across features)
- Context-aware AI assistance (inject prior patterns into new work)

### When NOT to Use
- Single-shot tasks (no persistence needed)
- Stateless APIs (sessionless clients)
- Highly sensitive data (vault requires security review)

### Example Code / Integration
- **Write Flow:** /spek.conclude (Step 4-7) writes to vault and repo memory
- **Read Flow:** /spek.prepare (Step 5) → /spek.context loads all three layers
- **Persistence:** Obsidian vault + Copilot memory filesystem

### Related Patterns
- Zettelkasten Convention Pattern (structure of vault notes)
- Session-to-Vault Archival Pattern (Layer 3 → Layer 1 transition)
- Context Injection Pattern (loads Layer 1+2 for enrichment)

### Specs Using This Pattern
- Primary: [memory-architecture.md](wiki/specs/memory-architecture.md)
- Supporting: [context-layer.md](wiki/specs/context-layer.md), [101-conclude-processing.md](wiki/specs/101-conclude-processing.md)

---

## Pattern 3: Enrichment Layer Pattern

**Category:** Architectural  
**Solves:** Inject context into SpecKit workflow phases  
**Primary Spec:** [enrichment-layer.md](wiki/specs/enrichment-layer.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
SpecKit commands (specify, plan, implement) operate without project context. Specs diverge from decisions; plans ignore code constraints; implementation misses patterns.

### Solution
Wrap each SpecKit phase with enrichment:
1. **Specify Enrichment:** Inject decisions + patterns before spec generation
2. **Plan Enrichment:** Inject decisions + patterns + code graph before planning
3. **Implement Enrichment:** Collect code diff + validate against decisions post-implementation

```
/spek.plan [feature-description]
├─ specify phase
│  ├─ PRE: Load decisions + patterns
│  ├─ CORE: Call /speckit.specify
│  └─ POST: Validate spec aligns with decisions
├─ plan phase
│  ├─ PRE: Load decisions + patterns + code graph
│  ├─ CORE: Call /speckit.plan
│  └─ POST: Validate plan follows architecture
└─ implement phase (post-approval)
   ├─ PRE: Load decisions + patterns + code graph
   ├─ CORE: Call /speckit.implement
   └─ POST: Collect diff + validate
```

### When to Use
- Spec-driven development with architectural constraints
- Maintaining consistency across features
- Preventing architectural drift

### When NOT to Use
- Greenfield projects (no prior context to inject)
- Prototyping (speed > consistency)
- One-off features (no long-term architecture)

### Example Code / Integration
- **Used in:** `/spek.plan` (all three phases)
- **Context source:** Context Layer (loads vault + repo memory)
- **Validation:** Anti-Sycophancy rules (Phase 2)

### Related Patterns
- Context Injection Pattern (PRE layer mechanism)
- Decorator Wrapper Pattern (overall structure)
- Anti-Sycophancy Validation Pattern (validation logic)

### Specs Using This Pattern
- Primary: [enrichment-layer.md](wiki/specs/enrichment-layer.md)
- Supporting: [context-layer.md](wiki/specs/context-layer.md), [speckit-integration-contract.md](wiki/specs/speckit-integration-contract.md)

---

### CATEGORY 2: WORKFLOW PATTERNS

---

## Pattern 4: Feature Lifecycle Pattern

**Category:** Workflow  
**Solves:** End-to-end orchestration of feature development  
**Primary Spec:** [cli-orchestration.md](wiki/specs/cli-orchestration.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Feature work involves multiple steps (spec → plan → implement → archive) with interdependencies. Without orchestration, steps get skipped or run out of order, causing inconsistencies.

### Solution
Define explicit feature lifecycle with required transitions:

```
(START) → prepare
          ↓
        specify
          ↓
        plan
          ↓
        implement
          ↓
        post
        ↓
        (COMPLETE)
```

Each phase:
- Validates preconditions (prior phase artifacts exist)
- Updates feature state (phase + completion %)
- Records transitions in session log
- Enables/disables features based on phase

### When to Use
- Multi-phase workflows with dependencies
- Ensuring process compliance (no skipping steps)
- Tracking progress through feature work

### When NOT to Use
- Ad-hoc/organic development (phases too rigid)
- Prototype-only workflows (state overhead)

### Example Code / Integration
- **State File:** /memories/session/current-feature.md (feature state)
- **State Transitions:** Each skill (`/spek.prepare`, `/spek.conclude`, etc.) updates state
- **Validation:** Preconditions checked at skill start (e.g., spec must exist before plan)

### Related Patterns
- Feature State Tracking Pattern (state file structure)
- Sequential Error Recovery Pattern (error handling per phase)
- Skill Chaining Pattern (orchestrates skills across phases)

### Specs Using This Pattern
- Primary: [cli-orchestration.md](wiki/specs/cli-orchestration.md)
- Supporting: [feature-state-tracking.md](wiki/specs/feature-state-tracking.md), [100-prepare-command.md](wiki/specs/100-prepare-command.md), [102-conclude-command.md](wiki/specs/102-conclude-command.md)

---

## Pattern 5: Skill Chaining Pattern

**Category:** Workflow  
**Solves:** Execute dependent skills in sequence with error resilience  
**Primary Spec:** [spek-automate-workflow.md](wiki/specs/spek-automate-workflow.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Workflow consists of multiple skills that depend on each other (e.g., context must load before enrichment). Sequential execution must handle failures, validate outputs, and offer remediation.

### Solution
Chain skills with explicit dependency management:

```
1. Load workspace context
2. Scan for available SpecKit skills
3. Determine workflow order (canonical or auto-detected)
4. For each skill:
   a. Pre-execution: Collect inputs
   b. Execute: Call skill via interface
   c. Post-execution: Validate output
   d. Decision: Continue or remediate?
5. Remediation if needed: Re-run with different inputs
6. Handoff to next workflow stage
```

### When to Use
- Complex workflows with multiple dependent steps
- Error recovery needed (not one-shot)
- Flexible skill discovery (add/remove skills dynamically)

### When NOT to Use
- Linear pipelines without interdependencies
- One-shot scripts (no recovery logic needed)
- Tightly coupled systems (decoupling would be expensive)

### Example Code / Integration
- **Orchestrator:** `/spek.plan` orchestrates specify/plan/implement skills
- **Skill Interface:** Each skill exposes (inputs, outputs, success criteria)
- **Validation:** Skills validate outputs before proceeding

### Related Patterns
- Sequential Error Recovery Pattern (error handling per skill)
- Feature Lifecycle Pattern (workflow sequencing)
- Decorator Wrapper Pattern (skill wrapping structure)

### Specs Using This Pattern
- Primary: [spek-automate-workflow.md](wiki/specs/spek-automate-workflow.md)
- Supporting: [cli-orchestration.md](wiki/specs/cli-orchestration.md), [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)

---

## Pattern 6: Post-Processing Pattern

**Category:** Workflow  
**Solves:** Extract, compress, and archive feature artifacts  
**Primary Spec:** [101-conclude-processing.md](wiki/specs/101-conclude-processing.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
After feature implementation, artifacts (spec, plan, code changes) must be preserved for future learning. Manual archival is error-prone; compression overhead is high.

### Solution
Automated post-processing performs a sequence of archival and indexing steps after feature implementation:

- Collect artifacts (spec/plan/tasks/trace/diff)
- Activate caveman compression mode
- Generate lessons document (vault/lessons/)
- Update vault/decision.md and related indexes
- Sync repo memory and patterns index
- Refresh code graph (/spek.map)
- Archive session memory and report completion

### When to Use
- Feature-driven development (lessons at feature end)
- Permanent memory (vault persistence)
- Pattern extraction (identify reusable solutions)

### When NOT to Use
- Throwaway prototypes (no long-term value)
- Single-use features (no pattern opportunity)

### Example Code / Integration
- **Triggered by:** `/spek.conclude` command (called after implementation complete)
- **Artifacts collected:** spec.md, plan.md, tasks.md, git diff
- **Output:** vault/lessons/<date>-<feature>.md

### Related Patterns
- Three-Layer Memory Model (writes to all layers)
- Caveman Compression Mode (compresses lessons)
- Session-to-Vault Archival Pattern (ephemeral → permanent)

### Specs Using This Pattern
- Primary: [101-conclude-processing.md](wiki/specs/101-conclude-processing.md)
- Supporting: [102-conclude-command.md](wiki/specs/102-conclude-command.md), [lessons-format.md](wiki/specs/lessons-format.md)

---

### CATEGORY 3: QUERY PATTERNS

---

## Pattern 7: Three-Layer Query Rule

**Category:** Query  
**Solves:** Optimize token usage via hierarchical queries  
**Primary Spec:** [3layer-query-rule.md](wiki/specs/3layer-query-rule.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Agent queries cost tokens. Naive approach: read all files (expensive). Better approach: tier queries by cost.

### Solution
Three-tier query hierarchy (cost increases; Layer 1-2 handle the majority of common queries):

**Layer 1: lat.md MCP Tools (local index)**
- Query: lat.md MCP tools (lat_symbols, lat_references, lat_callers, etc.)
- Examples: "Who calls function X?", "What does module Y depend on?"
- Cost: low (local index)
- Latency: low-latency

**Layer 2: Vault/Decisions (searchable metadata)**
- Query: grep + jq on vault files (or MCP query tool)
- Examples: "What decisions affect authentication?", "What patterns exist for error handling?"
- Cost: moderate (searching structured docs)
- Latency: moderate-latency

**Layer 3: Raw Code Files (full-file analysis)**
- Query: Read entire files, AI synthesis
- Examples: "Explain this complex algorithm", "Find all callers of function X across repo"
- Cost: high for full-file reads
- Latency: higher for full-file analysis

**Rule:** Use Layer 1 first; fallback to Layer 2; use Layer 3 only if necessary.

### When to Use
- Large codebases (token savings material)
- Repeated queries (cache Layer 1-2 results)
- Context-loading phases (minimize token budgets)

### When NOT to Use
- Small codebases (overhead not worth savings)
- One-time complex queries (Layer 3 simpler)
- Real-time reasoning (latency matters more than tokens)

### Example Code / Integration
- **Layer 1:** `/spek.context` uses lat.md for symbol lookup
- **Layer 2:** `/spek.prepare` queries vault for decisions
- **Layer 3:** `/spek.implement` reads affected code files only when Layer 1-2 insufficient

### Related Patterns
- Hybrid Graph Pattern (Layer 1 data source)
- Code Graph Query Pattern (Layer 1 queries)
- Token Budget Tracking Pattern (tracks Layer 1-3 costs)

### Specs Using This Pattern
- Primary: [3layer-query-rule.md](wiki/specs/3layer-query-rule.md)
- Supporting: [graph-query-patterns.md](wiki/specs/graph-query-patterns.md), [context-layer.md](wiki/specs/context-layer.md)

---

## Pattern 8: Code Graph Query Pattern

**Category:** Query  
**Solves:** Query code graph efficiently for context  
**Primary Spec:** [graph-query-patterns.md](wiki/specs/graph-query-patterns.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Code structure needs to be queryable (who calls this function? what does this module depend on?). Reading all source files is expensive.

### Solution
Use lat.md MCP tools for pre-indexed queries:

```python
# Layer 1: Direct MCP tool calls (built-in, low-latency)
symbols = call_mcp_tool("lat_symbols", file_path="src/services/auth.py")
callers = call_mcp_tool("lat_callers", symbol="authenticate")
impact = call_mcp_tool("lat_impact", file="src/services/auth.py", symbol="authenticate")

# Layer 2: Complex query composition (multiple tool calls)
# Agent chains multiple queries to answer complex questions

# Layer 3: Complex reasoning (fallback to LLM if needed)
# "Design refactoring considering all dependencies"
```

### When to Use
- Finding callers/callees (use lat_callers, lat_callees)
- Dependency analysis (use lat_impact for change scope)
- Code structure exploration (use lat_symbols, lat_references)
- Impact estimation (use lat_impact for built-in analysis)

### When NOT to Use
- Semantic reasoning ("What does this code do?" → need source code reading)
- Logic understanding (code graph doesn't understand behavior)
- Complex refactoring reasoning (may need LLM synthesis)

### Example Code / Integration
-- **Tool 1:** lat_symbols — Find all symbols in a file
-- **Tool 2:** lat_definition — Find where a symbol is defined
-- **Tool 3:** lat_references — Find all uses of a symbol
-- **Tool 4:** lat_callers — Find functions calling this function
-- **Tool 5:** lat_callees — Find functions called by this function
-- **Tool 6:** lat_impact — Estimate change impact radius
-- **Tool 7:** lat_query — Free-form index queries

### Related Patterns
- Three-Layer Query Rule (code graph = Layer 1)
- Hybrid Graph Pattern (code graph data structure)
- Incremental Sync Pattern (keeps code graph fresh)

### Specs Using This Pattern
- Primary: [graph-query-patterns.md](wiki/specs/graph-query-patterns.md)
- Supporting: [graph-storage-structure.md](wiki/specs/graph-storage-structure.md), [code-and-document-maps.md](wiki/specs/code-and-document-maps.md)

---

### CATEGORY 4: MEMORY PATTERNS

---

## Pattern 9: Zettelkasten Convention Pattern

**Category:** Memory  
**Solves:** Create atomic, interconnected notes with structure  
**Primary Spec:** [zettelkasten-conventions.md](wiki/specs/zettelkasten-conventions.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Vault notes need consistent structure for discoverability and linking. Unstructured markdown causes duplicates, broken links, and lost connections.

### Solution
Apply Zettelkasten conventions: atomic notes + YAML frontmatter + mandatory wikilinks.

```yaml
---
title: "Decision: Use Dependency Injection"
type: "decision"
tags: ["pattern/di", "architecture", "service-layer"]
status: "active"
created: "2026-05-10"
updated: "2026-05-19"
source: "feature-auth-refactor"
related: ["[[singleton-pattern]]", "[[service-locator-pattern]]"]
---

## Context
[1-2 sentences on why this decision was needed]

## Options Considered
- Option A: ...
- Option B: ...

## Decision
[Option chosen] because [rationale]

## Impact
[Affected systems, ripple effects]

## Related
- [[service-patterns]]
- [[dependency-injection-alternatives]]
```

### When to Use
- Knowledge bases with interconnected concepts
- Long-term reference material (Obsidian vaults)
- Pattern discovery across features

### When NOT to Use
- One-shot documents (overhead not justified)
- Unstructured research (frontmatter constraints)

### Example Code / Integration
- **Filename:** `<kebab-case-title>.md` (max 50 chars)
- **Frontmatter:** Mandatory fields (title, type, tags, status, created, updated, source, related)
- **Wikilinks:** Minimum 2 per note (enable discovery)

### Related Patterns
- Auto-Tagging + Auto-Wikilink Pattern (automates linking)
- Session-to-Vault Archival Pattern (applies Zettelkasten to sessions)

### Specs Using This Pattern
- Primary: [zettelkasten-conventions.md](wiki/specs/zettelkasten-conventions.md)
- Supporting: [memory-architecture.md](wiki/specs/memory-architecture.md), [auto-tagging-wikilinks.md](wiki/specs/auto-tagging-wikilinks.md)

---

## Pattern 10: Auto-Tagging + Auto-Wikilink Pattern

**Category:** Memory  
**Solves:** Automate knowledge interconnection (majority automation)  
**Primary Spec:** [auto-tagging-wikilinks.md](wiki/specs/auto-tagging-wikilinks.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
Manually linking vault notes is time-consuming (a significant portion of lesson generation). Manual tagging leads to inconsistencies.

### Solution
Automate extraction, mapping, and linking:

```
1. Extract keywords from generated lesson
2. Map keywords to existing vault items (decisions, patterns, lessons)
3. Auto-insert wikilinks [[item]] into lesson
4. Auto-generate tags from keyword extraction
5. Validate lesson against vault (detect redundancy)
```

**Configuration:**
```yaml
auto_linking:
  enabled: true
  extraction:
    min_keyword_length: "project-configured-min-length"
    max_keywords_per_lesson: "project-configured-max-keywords"
    exclude_stopwords: true
  mapping:
    strategy: "longest-match"
```

### When to Use
- Generating lessons at feature end (integration point)
- Large vault (100+ notes, manual linking impossible)
- Consistency enforcement (standardize tags)

### When NOT to Use
- Manual curation required (semantic linking needs human judgment)
- Small vault (overhead not worth savings)

### Example Code / Integration
- **Integration Point:** `/spek.conclude` Step 3 (Generate Lessons)
- **Output:** vault/lessons/<date>-<feature>.md with auto-inserted wikilinks
- **Validation:** Redundancy detection (lesson duplicates vault pattern → alert)

### Related Patterns
- Zettelkasten Convention Pattern (frontmatter structure)
- Three-Layer Memory Model (storage layers)

### Specs Using This Pattern
- Primary: [auto-tagging-wikilinks.md](wiki/specs/auto-tagging-wikilinks.md)
- Supporting: [zettelkasten-conventions.md](wiki/specs/zettelkasten-conventions.md), [102-conclude-command.md](wiki/specs/102-conclude-command.md)

---

## Pattern 11: Session-to-Vault Archival Pattern

**Category:** Memory  
**Solves:** Convert ephemeral session context to permanent vault artifacts  
**Primary Spec:** [session-logs-vault-artifacts.md](wiki/specs/session-logs-vault-artifacts.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Session memory (`/memories/session/current-feature.md`) is ephemeral. Once feature ends, session log is deleted. Valuable context (decisions, patterns discovered) is lost.

### Solution
Archive session logs to vault with Zettelkasten format:

```
/spek.conclude Step 9: Archive Session Memory
├─ Read /memories/session/current-feature.md
├─ Extract sections (What Built, How Built, Decisions, Patterns, Pending)
├─ Format as vault note with Zettelkasten structure
├─ Add wikilinks to related decisions/patterns
└─ Write to vault/sessions/<YYYY-MM-DD>-<feature>.md
```

### When to Use
- Feature end (permanent archival)
- Cross-feature discovery (pattern identification)
- Audit trail (feature development lifecycle)

### When NOT to Use
- Session in progress (wait until feature complete)
- Sensitive context (requires vault security review)

### Example Code / Integration
- **Trigger:** `/spek.conclude` Step 9
- **Source:** /memories/session/current-feature.md
- **Destination:** vault/sessions/<YYYY-MM-DD>-<feature>.md
- **Format:** Zettelkasten (frontmatter + wikilinks)

### Related Patterns
- Three-Layer Memory Model (Layer 3 → Layer 1 transition)
- Zettelkasten Convention Pattern (format of archived sessions)

### Specs Using This Pattern
- Primary: [session-logs-vault-artifacts.md](wiki/specs/session-logs-vault-artifacts.md)
- Supporting: [101-conclude-processing.md](wiki/specs/101-conclude-processing.md), [lessons-format.md](wiki/specs/lessons-format.md)

---

### CATEGORY 5: COMPRESSION PATTERNS

---

## Pattern 12: Caveman Compression Mode

**Category:** Compression  
**Solves:** Reduce token usage (significant reduction) while preserving meaning
**Primary Spec:** [caveman-integration.md](wiki/specs/caveman-integration.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Lessons + vault updates consume significant token budgets per feature. Multi-feature sessions can hit token limits.

### Solution
Ultra-compressed communication style (caveman mode) preserving technical accuracy:

**Mode 1: Lite (modest reduction)**
- Full sentences, natural language
- Use: First feature (readability), complex decisions

**Mode 2: Full (substantial reduction, DEFAULT)**
- Caveman syntax (terse, meaning preserved)
- Example: "Why: DI pattern. Benefit: Decoupling. Cost: Setup overhead."
- Use: Standard feature workflow

**Mode 3: Ultra (maximal reduction)**
- Minimal syntax, abbreviations, extreme compression
- Use: Token-constrained sessions

### When to Use
- Multi-feature sessions (token budget constraints)
- Lessons generation (integration point: `/spek.conclude` Step 2)
- Vault compression (repo memory cache)

### When NOT to Use
- First-time documentation (prefer clarity)
- Code comments (readability critical)
- User-facing docs (clarity required)

### Example Code / Integration
- **Triggered by:** `/spek.conclude --caveman-mode=full` (default)
- **Compression rules:** Active voice, concrete, short, specific
- **Output:** Compressed lessons, tags, wikilinks preserved

### Related Patterns
- Token Budget Tracking Pattern (monitors compression impact)
- Post-Processing Pattern (integration point)

### Specs Using This Pattern
- Primary: [caveman-integration.md](wiki/specs/caveman-integration.md)
- Supporting: [lessons-format.md](wiki/specs/lessons-format.md), [102-conclude-command.md](wiki/specs/102-conclude-command.md)

---

## Pattern 13: Token Budget Tracking Pattern

**Category:** Compression  
**Solves:** Allocate and monitor per-phase token costs  
**Primary Spec:** [token-budget.md](wiki/specs/token-budget.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
Token costs are invisible. Phase phase blows budget; future optimizations guided by guesses, not data.

### Solution
Explicit per-phase budgets with tracking and alerts:

```yaml
token_budget:
  per_feature: configured-value  # Total tokens per feature (team-configurable)

  phases:
    specify_phase:
      budget: configured-value  # Spec generation
    plan_phase:
      budget: configured-value  # Plan + architecture
    implement_phase:
      budget: configured-value  # Code generation
    post_phase:
      budget: configured-value  # Lessons + vault
```
  alert_threshold: "project-configured-alert-threshold"   # Alert when usage exceeds configured threshold
  warning_threshold: "project-configured-warning-threshold" # Warning when usage exceeds configured threshold
```

### When to Use
- Token-constrained environments (cloud APIs, limited credits)
- Optimization (identify expensive phases)
- Planning (estimate feature costs)

### When NOT to Use
- Unlimited token budgets (overhead not justified)
- Research (focus > efficiency)

### Example Code / Integration
- **Tracking:** Each skill reports token usage
- **Alerts:** Warnings at configured thresholds
- **Reporting:** `/spek.conclude` Step 10 (feature-end report)

### Related Patterns
- Caveman Compression Mode (reduces phase costs)
- Three-Layer Query Rule (Layer 1-2 cheaper than Layer 3)

### Specs Using This Pattern
- Primary: [token-budget.md](wiki/specs/token-budget.md)
- Supporting: [102-conclude-command.md](wiki/specs/102-conclude-command.md), [caveman-integration.md](wiki/specs/caveman-integration.md)

---

### CATEGORY 6: INTEGRATION PATTERNS

---

## Pattern 14: Context Injection Pattern

**Category:** Integration  
**Solves:** Load and compose context for tool invocation  
**Primary Spec:** [context-layer.md](wiki/specs/context-layer.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Tools (SpecKit skills) run blind without context. Specs ignore prior decisions; plans miss architectural constraints.

### Solution
Load and inject context at pre-execution:

```
PRE-EXECUTION:
  1. Load from vault (decisions, patterns, lessons)
  2. Load from repo memory (compressed cache)
  3. Load from code graph (module list, hotspots)
  4. Compose into enrichment prompt
  5. Prepend to tool input

CORE EXECUTION:
  Call tool with enriched input

POST-EXECUTION:
  Validate output aligns with injected context
```

### When to Use
- Spec-driven development (context-aware specs/plans)
- Architectural alignment (enforce constraints)
- Pattern reuse (inject proven patterns)

### When NOT to Use
- Greenfield projects (no context to inject)
- One-shot tools (no long-term context)

### Example Code / Integration
- **Integration Point:** Decorator wrapper PRE layer
- **Context sources:** vault/decision.md, vault/patterns.md, lat.md MCP tools
- **Injection format:** Prompt text ("IMPORTANT: Adhere to these decisions: ...") + MCP tool results

### Related Patterns
- Decorator Wrapper Pattern (PRE layer mechanism)
- Three-Layer Memory Model (context sources)
- Three-Layer Query Rule (efficient loading)

### Specs Using This Pattern
- Primary: [context-layer.md](wiki/specs/context-layer.md)
- Supporting: [enrichment-layer.md](wiki/specs/enrichment-layer.md), [decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md)

---

## Pattern 15: Skill Chaining Pattern (See also Workflow Patterns - Pattern 5)

Already documented in Workflow Patterns section. Repeated here for completeness in Integration category.

---

### CATEGORY 7: ERROR HANDLING PATTERNS

---

## Pattern 16: Error Categorization Pattern

**Category:** Error Handling  
**Solves:** Classify errors for targeted recovery  
**Primary Spec:** [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Errors need different handling strategies (git errors need user intervention; vault errors can fallback; network errors can retry). One-size-fits-all error handling doesn't work.

### Solution
Classify errors into categories; apply category-specific recovery:

**Category 1: Git State Errors (TRANSIENT or USER)**
- Issue: Git repo dirty, branch conflicts, detached HEAD
- Severity: HIGH
- Action: FAIL + GUIDE (report error + show required action)
- Recovery: No auto-retry (requires user action)

**Category 2: Vault Access Errors (TRANSIENT or FATAL)**
- Issue: Vault missing, JSON parse error, permission denied
- Severity: MEDIUM-HIGH
- Action: WARN + FALLBACK (continue with cache or empty vault)
- Recovery: Async retry (30s intervals, max 3 retries)

**Category 3: Graph/Code Index Errors (TRANSIENT or RECOVERABLE)**
- Issue: lat.md index corrupted, lat.md index rebuild fails
- Severity: MEDIUM
- Action: WARN + FALLBACK (continue with stale graph or grep)
- Recovery: Re-trigger `/spek.map` on next run

**Category 4: LLM Errors (TRANSIENT)**
- Issue: API timeout, rate limit, model unavailable
- Severity: MEDIUM
- Action: RETRY + FALLBACK (retry 3x; fallback to simpler prompt)
- Recovery: Exponential backoff

**Category 5: SpecKit Errors (FATAL or USER)**
- Issue: Spec generation failed, plan invalid
- Severity: HIGH
- Action: FAIL + GUIDANCE (show error + suggest manual edit)
- Recovery: Manual intervention (user edits artifact)

**Category 6: User Errors (USER)**
- Issue: Invalid input, missing required flag
- Severity: HIGH
- Action: FAIL + GUIDANCE (show error + usage example)
- Recovery: User re-runs with correct input

### When to Use
- Autonomous workflows (error recovery needed)
- Production deployments (failures expected)
- Multi-phase workflows (partial failures tolerated)

### When NOT to Use
- Script with no recovery ("fail fast" better)
- Interactive debugging (user intervention for every error)

### Example Code / Integration
- **Integration Point:** All skills (prepare, automate, post, etc.)
- **Logging:** All errors logged to `.cel/error-log.md` with category + action
- **User Guidance:** Clear error messages + remediation suggestions

### Related Patterns
- Sequential Error Recovery Pattern (recovery structure per skill)
- Fallback Hierarchy Pattern (layered fallback strategies)

### Specs Using This Pattern
- Primary: [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)
- Supporting: All workflow specs (prepare, automate, post, implement)

---

## Pattern 17: Fallback Hierarchy Pattern

**Category:** Error Handling  
**Solves:** Graceful degradation via layered fallbacks  
**Primary Spec:** [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
When primary systems fail (vault inaccessible, graph stale), workflow should degrade gracefully, not crash.

### Solution
Implement fallback hierarchy (Layer 1 primary, Layer 2-3 fallbacks):

**Example: Context Loading Fallback**
```
Layer 1 (PRIMARY): Load from vault (vault/decision.md)
  ↓ (if fails)
Layer 2 (FALLBACK): Load from repo cache ([022-architectural-decisions.md](wiki/specs/022-architectural-decisions.md))
  ↓ (if fails)
Layer 3 (MINIMAL): Continue with empty context (log warning)
```

**Example: Code Graph Query Fallback**
```
Layer 1 (PRIMARY): Query via lat.md MCP tools (lat_symbols, lat_references, lat_callers, lat_callees, lat_impact, lat_definition, lat_query)
  ↓ (if unavailable)
Layer 2 (FALLBACK): Fall back to vault grep or file reading
  ↓ (if fails)
Layer 3 (MINIMAL): Skip context injection (log warning, continue)
```

### When to Use
- Resilient systems (failures expected, not fatal)
- Multi-layer architecture (natural fallback path)
- Critical workflows (must not crash)

### When NOT to Use
- Fail-fast scripts (early detection preferred)
- Immutable systems (fallback complexity not justified)

### Example Code / Integration
- **Integration Point:** Context loading, graph queries, vault writes
- **Fallback logic:** Try/except with specific recovery per layer
- **Logging:** All fallback triggers logged (enable diagnostics)

### Related Patterns
- Error Categorization Pattern (classifies which errors trigger fallback)
- Sequential Error Recovery Pattern (recovery structure)

### Specs Using This Pattern
- Primary: [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)
- Supporting: [context-layer.md](wiki/specs/context-layer.md), [graph-query-patterns.md](wiki/specs/graph-query-patterns.md)

---

## Pattern 18: Sequential Error Recovery Pattern

**Category:** Error Handling  
**Solves:** Structured pre-core-post error handling  
**Primary Spec:** [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)  
**Phase Introduced:** Phase 0 (Foundation)  
**Status:** ACTIVE  

### Problem
Error handling must be consistent across all skills and phases. Unstructured error handling causes inconsistent behavior.

### Solution
Apply consistent pre-core-post structure with error handling at each layer:

```python
def skill_with_error_recovery(inputs):
    try:
        # PRE-EXECUTION
        try:
            context = load_context()
            validated_inputs = validate(inputs)
        except ValidationError as e:
            log_error(e, category="USER")
            raise  # Fail fast on user input errors
        
        # CORE EXECUTION
        try:
            result = core_execution(validated_inputs, context)
        except TransientError as e:
            log_error(e, category="TRANSIENT")
            result = retry_with_backoff(core_execution, max_retries=3)
        except FatalError as e:
            log_error(e, category="FATAL")
            raise
        
        # POST-EXECUTION
        try:
            validated_result = validate_output(result)
            update_memory(validated_result)
        except MemoryError as e:
            log_error(e, category="VAULT")
            # Continue with in-memory only; vault will retry later
        
        return validated_result
        
    except Exception as e:
        log_error(e, category="UNKNOWN")
        return fallback_result()
```

### When to Use
- All autonomous workflows (error recovery needed)
- Multi-step processes (partial failures must be handled)
- Production deployments (reliability critical)

### When NOT to Use
- Simple scripts (overhead not justified)
- Interactive workflows (user intervention for errors)

### Example Code / Integration
- **Integration Point:** All skills (prepare, automate, post, implement, etc.)
- **Error logging:** Structured format (category, action, recovery attempt)
- **Fallback:** Return minimal valid result if core fails

### Related Patterns
- Error Categorization Pattern (classifies errors)
- Fallback Hierarchy Pattern (fallback structure)
- Decorator Wrapper Pattern (wrapper provides structure)

### Specs Using This Pattern
- Primary: [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md)
- Supporting: All workflow specs

---

### CATEGORY 8: VALIDATION PATTERNS

---

## Pattern 19: Anti-Sycophancy Validation Pattern

**Category:** Validation  
**Solves:** Flag AI drift and contradictions  
**Primary Spec:** [anti-sycophancy.md](wiki/specs/anti-sycophancy.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
AI tends to agree with context without critical evaluation. Specs drift from vault decisions; plans ignore architectural constraints; scope creeps silently.

### Solution
Implement explicit validation rules that flag deviations:

**Rule 1: Contradiction Detection**
- If spec contradicts vault decisions, flag conflict
- Severity: HIGH
- Action: Require justification or alignment

**Rule 2: Complexity Increase**
- If spec 50% above baseline, flag scope creep
- Severity: MEDIUM
- Action: Require justification

**Rule 3: Pattern Consistency**
- If recent patterns suggest different approach, alert
- Severity: MEDIUM
- Action: Offer alternative, require decision

**Rule 4: Scope Validation**
- Compare spec scope to similar past features
- Severity: MEDIUM
- Action: Validate for silent scope creep

### When to Use
- Solo developer workflows (no human review)
- Long features (scope creep risk)
- Strict architectural requirements (deviations costly)

### When NOT to Use
- Prototyping (rules too restrictive)
- Exploration (constraints inhibit discovery)

### Example Code / Integration
- **Integration Point:** `/spek.plan` specify and plan phases
- **Validation:** Pre-submission, before calling SpecKit
- **Action:** Flag conflicts, offer override with documentation

### Related Patterns
- Error Categorization Pattern (classifies validation errors)
- Context Injection Pattern (uses vault for comparisons)

### Specs Using This Pattern
- Primary: [anti-sycophancy.md](wiki/specs/anti-sycophancy.md)
- Supporting: [context-layer.md](wiki/specs/context-layer.md), [enrichment-layer.md](wiki/specs/enrichment-layer.md)

---

## Pattern 20: RARV Reflection Pattern

**Category:** Validation  
**Solves:** Reason-Act-Reflect-Verify alignment cycle  
**Primary Spec:** [rarv-reflection.md](wiki/specs/rarv-reflection.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
Implementation often diverges from spec/plan. Misalignments accumulate, creating technical debt. No automatic detection until problems compound.

### Solution
Implement RARV cycle (Reason-Act-Reflect-Verify) post-implementation:

```
Phase 1: REASON
  Compare spec/plan to implemented code
  Identify deviations (scope creep, missing features, architecture divergence)

Phase 2: ACT
  For each deviation: fix or justify?
  Options: A) Fix code to align with spec
           B) Keep code, update spec (justified)
           C) Keep code, document reason (for future learning)

Phase 3: REFLECT
  Update vault decisions if justified
  Capture new patterns discovered

Phase 4: VERIFY
  Re-validate alignment against original decisions
  Confirm no new contradictions introduced
```

### When to Use
- After implementation completes
- Long features (divergence accumulates)
- Strict alignment requirements

### When NOT to Use
- Prototyping (spec is just a guide)
- Rapid iteration (overhead slows velocity)

### Example Code / Integration
- **Trigger:** `/spek.conclude` Step 7 (optional integration point)
- **Input:** spec.md, plan.md, git diff
- **Output:** Deviation report + user choices + updated vault (if reflected)

### Related Patterns
- Anti-Sycophancy Validation Pattern (pre-implementation checks)
- Error Categorization Pattern (classifies deviations)

### Specs Using This Pattern
- Primary: [rarv-reflection.md](wiki/specs/rarv-reflection.md)
- Supporting: [101-conclude-processing.md](wiki/specs/101-conclude-processing.md), [context-layer.md](wiki/specs/context-layer.md)

---

## Pattern 21: Backprop Reflex Pattern

**Category:** Validation  
**Solves:** Test failures → vault updates → better specs  
**Primary Spec:** [backprop-reflex.md](wiki/specs/backprop-reflex.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
Test failures contain valuable learning (race conditions, timeout issues, assertion failures). Without capture, same mistakes repeat.

### Solution
Automatic feedback loop: parse test failures → extract patterns → update vault → tag future specs:

```
End-of-Feature Test Failure Analysis:
  1. Get last test run results
  2. Parse failure output (error messages, stack traces)
  3. Extract failure patterns (race condition, timeout, assertion, etc.)
  4. Update vault with failure warnings
  5. Tag lesson with failure patterns
  6. Tag future specs with warnings ("watch out for race conditions here")
```

### When to Use
- Extensive test suites (failures common)
- Long-running features (patterns emerge)
- Team learning (mistakes become vault knowledge)

### When NOT to Use
- Prototyping (test failures expected)
- Ad-hoc testing (not automated)

### Example Code / Integration
- **Integration Point:** `/spek.conclude` Step 3 (Generate Lessons)
- **Failure parser:** Extract from Jest/pytest/etc. output
- **Vault update:** Append warnings to decision.md + lesson
- **Future tagging:** Flag similar specs with warnings

### Related Patterns
- Post-Processing Pattern (integration point)
- Zettelkasten Convention Pattern (vault format)

### Specs Using This Pattern
- Primary: [backprop-reflex.md](wiki/specs/backprop-reflex.md)
- Supporting: [101-conclude-processing.md](wiki/specs/101-conclude-processing.md), [lessons-format.md](wiki/specs/lessons-format.md)

---

## Pattern 22: Blind Code Review Pattern

**Category:** Validation  
**Solves:** Anonymized independent review  
**Primary Spec:** [blind-code-review.md](wiki/specs/blind-code-review.md)  
**Phase Introduced:** Phase 2 (Validation & Optimization)  
**Status:** ACTIVE  

### Problem
AI-generated code may have blind spots (hallucinations, over-reliance on context). Independent review needed without bias from feature description.

### Solution
Optional second-pass review with anonymization:

```
Step 1: Anonymize Code
  - Remove AI-generated markers
  - Strip context comments
  - Remove feature names
  - Remove author/timestamp

Step 2: Blind Review
  - Run linters (style, errors)
  - Run tests (behavior)
  - Run static analysis (security, performance)

Step 3: Flag Issues
  - Report findings for developer attention
  - Suggest fixes

Step 4: Remediation
  - Fix issues or document reason
  - Re-validate
```

### When to Use
- Production-critical code (quality non-negotiable)
- Long-term maintenance (debt compounds)
- Team projects (code review standard practice)

### When NOT to Use
- Prototypes (review overhead)
- Trusted AI output (review ritual, not practical)

### Example Code / Integration
- **Trigger:** Post-implementation, before `/spek.conclude` archival
- **Anonymization:** Strip AI markers, feature context, author info
- **Review checks:** Linters, tests, static analysis
- **Output:** Issue report + remediation guidance

### Related Patterns
- RARV Reflection Pattern (alignment verification)
- Sequential Error Recovery Pattern (error handling)

### Specs Using This Pattern
- Primary: [blind-code-review.md](wiki/specs/blind-code-review.md)
- Supporting: [integration-validation-and-testing.md](wiki/specs/integration-validation-and-testing.md)

---

### CATEGORY 9: GRAPH PATTERNS

---

## Pattern 23: Hybrid Graph Pattern

**Category:** Graph  
**Solves:** Unify code + doc + skill nodes in single queryable graph  
**Primary Spec:** [code-and-document-maps.md](wiki/specs/code-and-document-maps.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Code lives in lat.md index; documentation lives in Obsidian vault. Separate queries make context loading expensive (query index + query vault separately).

### Solution
Access unified code + doc index via lat.md MCP tools:

```
lat.md index (vault/graph/lat_index.db) contains:
├─ Code nodes (from lat.md indexing)
│  └─ Functions, classes, modules, variables
├─ Doc nodes (from Obsidian export)
│  └─ Decisions, patterns, lessons, specs
└─ Skill nodes (file-level)
  └─ `/spek.prepare`, `/spek.conclude`, etc.

Query via MCP tools:
├─ lat_symbols → Find all code/doc in file
├─ lat_references → Find all uses of code or doc reference
├─ lat_callers → Find code calling this code
├─ lat_impact → Estimate impact of change (code + doc scope)
└─ lat_query → Custom index queries (advanced)
```

**Node Types (in lat.md index):**
- **Code:** language="python" or other → function/class/variable
- **Doc (file-level):** language="markdown", type="documentation" → decision.md
- **Doc (heading-level):** type="documentation", heading=true → decision.md#heading
- **Skill:** language="yaml", type="skill" → spek-prepare/SKILL.md

**Benefits:**
- MCP tools find related code + docs with low latency
- Impact analysis across code/doc boundary (via lat_impact)
- Zero token cost for queries

### When to Use
- Large codebases with extensive documentation
- Spec-driven development (need code+doc integration)
- Agent-assisted tools (queries must be fast)

### When NOT to use
- Simple projects (overhead not justified)
- Code-only or doc-only systems (no integration benefit)

### Example Code / Integration
- **Build process:** `/spek.map` generates hybrid graph (code pass + doc pass + merge)
- **Query interface:** MCP tools (all 7 tools support hybrid queries)
- **Storage:** vault/graph/lat_index.db (SQLite) + optional vault/graph/exports/ (JSONL exports)

### Related Patterns
- Graph Merge Integration Pattern (merge algorithm)
- Incremental Sync Pattern (update strategy)
- Code Graph Query Pattern (query interface)

### Specs Using This Pattern
- Primary: [code-and-document-maps.md](wiki/specs/code-and-document-maps.md)
- Supporting: [graph-merge-integration.md](wiki/specs/graph-merge-integration.md), [spek-map-command.md](wiki/specs/spek-map-command.md)

---

## Pattern 24: Graph Merge Integration Pattern

**Category:** Graph  
**Solves:** Combine heterogeneous node types into unified graph  
**Primary Spec:** [graph-merge-integration.md](wiki/specs/graph-merge-integration.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Code nodes (from lat.md) and doc nodes (from Obsidian) are generated separately with different schemas. Merging requires deduplication, link discovery, and backreference computation.

### Solution
Merge process (5 steps):

```
Step 1: Load source node sets
  ├─ vault/graph/nodes-code.jsonl
  └─ vault/graph/nodes-docs.jsonl

Step 2: Deduplication
  ├─ Deduplicate by (type, file, symbol/heading)
  └─ Output: unique code_nodes[], unique doc_nodes[]

Step 3: Link discovery
  ├─ Code → Code (already in lat.md edges)
  ├─ Doc → Doc (from markdown links)
  ├─ Code → Doc (from code comments referencing decisions)
  └─ Doc → Code (from decision.md affecting module.py)

Step 4: Backreference computation
  ├─ For each edge (A → B), add reverse edge (B ← A)
  └─ Enable efficient "who references me?" queries

Step 5: Merge & validation
  ├─ Merge all nodes → vault/graph/nodes.jsonl
  ├─ Merge all edges → vault/graph/edges.jsonl
  └─ Validate schema compliance
```

### When to Use
- Hybrid code+doc graphs (integration needed)
- Agent-assisted tools (need unified query interface)
- Impact analysis (trace code/doc relationships)

### When NOT to Use
- Separate concerns (keep code/doc separate)
- Real-time systems (merge overhead)

### Example Code / Integration
- **Trigger:** `/spek.map` (merge is final step)
- **Input:** nodes-code.jsonl + nodes-docs.jsonl
- **Output:** vault/graph/nodes.jsonl (merged) + vault/graph/edges.jsonl (merged)

### Related Patterns
- Hybrid Graph Pattern (data model)
- Incremental Sync Pattern (update strategy)

### Specs Using This Pattern
- Primary: [graph-merge-integration.md](wiki/specs/graph-merge-integration.md)
- Supporting: [spek-map-command.md](wiki/specs/spek-map-command.md), [graph-storage-structure.md](wiki/specs/graph-storage-structure.md)

---

## Pattern 25: Incremental Sync Pattern

**Category:** Graph  
**Solves:** Cache + file watching for efficient updates  
**Primary Spec:** [graph-refresh-strategy.md](wiki/specs/graph-refresh-strategy.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Full graph rebuild is expensive (30-60 seconds). Most changes are small. Rebuilding entire graph on every change wastes time.

### Solution
Incremental sync with SHA256 caching:

```
SHA256 Caching:
  ├─ Store hash of every file: vault/graph/cache/sha256.json
  ├─ Before sync: compute current hashes
  ├─ Compare with cached hashes
  ├─ Identify changed files
  └─ Re-index only changed files

Node Index Lookup:
  ├─ Store symbol → node-id mapping: vault/graph/cache/node-index.json
  ├─ Enable fast symbol lookups (no full jsonl read)
  └─ Update on each sync

Incremental Sync Modes:
  ├─ Default: Incremental (2-5 seconds)
  ├─ --full: Full rebuild (30-60 seconds; on corruption)
  └─ --watch: Continuous file watcher (real-time updates)
```

### When to Use
- Large codebases (rebuild time material)
- Frequent changes (caching pays for itself)
- Real-time updates needed (watch mode)

### When NOT to Use
- Small codebases (overhead not justified)
- One-time builds (full rebuild simpler)

### Example Code / Integration
- **Default behavior:** `/spek.map` uses incremental sync
- **Full rebuild:** `/spek.map --full` (on corruption or when cache unreliable)
- **Watch mode:** `/spek.map --watch` (continuous sync during development)
- **Integration:** `/spek.prepare` Step 4, `/spek.conclude` Step 8

### Related Patterns
- Hybrid Graph Pattern (data model)
- Graph Merge Integration Pattern (merge + incremental updates)

### Specs Using This Pattern
- Primary: [graph-refresh-strategy.md](wiki/specs/graph-refresh-strategy.md)
- Supporting: [spek-map-command.md](wiki/specs/spek-map-command.md), [graph-storage-structure.md](wiki/specs/graph-storage-structure.md)

---

### CATEGORY 10: STATE MANAGEMENT PATTERNS

---

## Pattern 26: Feature State Tracking Pattern

**Category:** State Management  
**Solves:** Track feature lifecycle phases  
**Primary Spec:** [feature-state-tracking.md](wiki/specs/feature-state-tracking.md)  
**Phase Introduced:** Phase 1 (Agent Skills)  
**Status:** ACTIVE  

### Problem
Feature work involves multiple steps (prepare → specify → plan → implement → post). Without tracking, it's unclear which phase is current, what's been completed, and what's pending.

### Solution
Explicit state file (`/memories/session/current-feature.md`) tracking:

```yaml
---
feature_name: "spek-full-workflow-cli"
feature_id: "003"
status: "initialized | specifying | planning | implementing | completing"
session_start: "2026-05-19T10:00:00Z"
session_count: 1
phase: "prepared | specifying | planning | implementing | completing"
completion: progress-indicator
---

## Current Phase: [Prepared|Specifying|Planning|Implementing|Completing]

## Progress by Phase
- [ ] Spec drafted (initial)
- [ ] Plan drafted (in-progress)
- [ ] Tasks generated (ready for implementation)
- [ ] Implementation complete (completed)

## Session Log
- Session 1: [timestamp] Prepared, loaded context
- Session 2: [timestamp] Specified, generated spec
```

### When to Use
- Multi-phase workflows (state tracking useful)
- Multi-session features (resume capability)
- Progress visibility (user/agent knows current status)

### When NOT to Use
- Single-shot tasks (state overhead)
- Stateless systems (no phase concept)

### Example Code / Integration
- **Create:** `/spek.prepare` Step 6 (initialized status)
- **Update:** Each skill updates status through defined phases (drafted → planned → implementing → completing → completed)
- **Archive:** `/spek.conclude` Step 9 (move to /memories/session/archive/)

### Related Patterns
- Feature Lifecycle Pattern (phases that state tracks)
- Session-to-Vault Archival Pattern (archival process)

### Specs Using This Pattern
- Primary: [feature-state-tracking.md](wiki/specs/feature-state-tracking.md)
- Supporting: [cli-orchestration.md](wiki/specs/cli-orchestration.md), [100-prepare-command.md](wiki/specs/100-prepare-command.md)

---

## Pattern Evolution During Phases 1-2

### Phase 0 → Phase 1

**Patterns Introduced in Phase 1 (Agent Skills):**
- Skill Chaining Pattern (no existing workflow orchestration)
- Context Injection Pattern (context loading layer)
- Feature State Tracking Pattern (progress visibility)
- Feature Lifecycle Pattern (multi-phase orchestration)
- Post-Processing Pattern (artifact archival)
- Code Graph Query Pattern (pre-indexed queries)
- Hybrid Graph Pattern (code+doc unification)

**Patterns Evolved in Phase 1:**
- Decorator Wrapper Pattern: Enhanced with context injection
- Error Categorization Pattern: Refined with category definitions

### Phase 1 → Phase 2

**Patterns Introduced in Phase 2 (Validation & Optimization):**
- Anti-Sycophancy Validation Pattern (catch AI drift)
- Blind Code Review Pattern (independent review)
- RARV Reflection Pattern (alignment verification)
- Backprop Reflex Pattern (test failures → learning)
- Token Budget Tracking Pattern (cost transparency)
- Auto-Tagging + Auto-Wikilink Pattern (automation)

**Patterns Evolved in Phase 2:**
- Session-to-Vault Archival Pattern: Formalized archival format
- Caveman Compression Mode: Tuned compression levels (lite/full/ultra)

### Summary: Pattern Adoption Timeline

| Pattern | Phase 0 | Phase 1 | Phase 2 | Status |
|---------|---------|---------|---------|--------|
| Decorator Wrapper | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Three-Layer Memory | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Three-Layer Query | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Enrichment Layer | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Context Injection | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Feature Lifecycle | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Error Categorization | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Zettelkasten | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Caveman Compression | ~ SPEC | ✓ IMPL | ✓ EVOLVED | ACTIVE |
| Auto-Tagging | ~ SPEC | ~ IMPL | ✓ IMPL | ACTIVE (Phase 2+) |
| Skill Chaining | - | ✓ SPEC | ✓ IMPL | ACTIVE |
| Post-Processing | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Hybrid Graph | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Graph Merge | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Incremental Sync | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Feature State Tracking | ~ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Session-to-Vault | ~ SPEC | ~ IMPL | ✓ IMPL | ACTIVE (Phase 2+) |
| Anti-Sycophancy | - | - | ✓ SPEC | ACTIVE (Phase 2+) |
| Blind Review | - | - | ✓ SPEC | ACTIVE (Phase 2+) |
| Backprop Reflex | - | - | ✓ SPEC | ACTIVE (Phase 2+) |
| RARV Reflection | - | - | ✓ SPEC | ACTIVE (Phase 2+) |
| Token Budget | - | - | ✓ SPEC | ACTIVE (Phase 2+) |
| Fallback Hierarchy | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |
| Sequential Error Recovery | ✓ SPEC | ✓ IMPL | ✓ ACTIVE | ACTIVE |

---

## Pattern-Spec Mapping (Cross-Reference Validation)

| Pattern | Primary Spec | Supporting Specs | Use Phase | Frequency |
|---------|---|---|---|---|
| 1. Decorator Wrapper | decorator-wrapper-pattern.md | enrichment-layer.md, speckit-integration-contract.md | 1-2 | HIGH |
| 2. Three-Layer Memory | memory-architecture.md | context-layer.md, 101-conclude-processing.md, session-logs-vault-artifacts.md | 1-2 | HIGH |
| 3. Three-Layer Query | 3layer-query-rule.md | graph-query-patterns.md, context-layer.md | 1-2 | HIGH |
| 4. Enrichment Layer | enrichment-layer.md | context-layer.md, speckit-integration-contract.md, decorator-wrapper-pattern.md | 1-2 | HIGH |
| 5. Context Injection | context-layer.md | enrichment-layer.md, decorator-wrapper-pattern.md, memory-architecture.md | 1-2 | HIGH |
| 6. Feature Lifecycle | cli-orchestration.md | 100-prepare-command.md, 102-conclude-command.md, feature-state-tracking.md | 1-2 | HIGH |
| 7. Error Categorization | error-handling-and-recovery.md | All workflow specs | 1-2 | HIGH |
| 8. Zettelkasten | zettelkasten-conventions.md | auto-tagging-wikilinks.md, session-logs-vault-artifacts.md | 1-2 | MEDIUM |
| 9. Caveman Compression | caveman-integration.md | lessons-format.md, 102-conclude-command.md, 101-conclude-processing.md | 1-2 | HIGH |
| 10. Auto-Tagging | auto-tagging-wikilinks.md | zettelkasten-conventions.md, 102-conclude-command.md | 2+ | MEDIUM |
| 11. Skill Chaining | spek-automate-workflow.md | cli-orchestration.md, error-handling-and-recovery.md | 1-2 | HIGH |
| 12. Post-Processing | 101-conclude-processing.md | 102-conclude-command.md, lessons-format.md, caveman-integration.md | 1-2 | HIGH |
| 13. Hybrid Graph | code-and-document-maps.md | graph-merge-integration.md, node-schema-design.md, spek-map-command.md | 1-2 | MEDIUM |
| 14. Graph Merge | graph-merge-integration.md | hybrid-graph (code-and-document-maps.md), graph-storage-structure.md | 1 | MEDIUM |
| 15. Incremental Sync | graph-refresh-strategy.md | spek-map-command.md, graph-storage-structure.md | 1-2 | MEDIUM |
| 16. Feature State | feature-state-tracking.md | cli-orchestration.md, 100-prepare-command.md, 102-conclude-command.md | 1-2 | HIGH |
| 17. Session-to-Vault | session-logs-vault-artifacts.md | 101-conclude-processing.md, zettelkasten-conventions.md, lessons-format.md | 2+ | MEDIUM |
| 18. Anti-Sycophancy | anti-sycophancy.md | context-layer.md, enrichment-layer.md | 2+ | LOW |
| 19. Blind Review | blind-code-review.md | integration-validation-and-testing.md, 102-conclude-command.md | 2+ | LOW |
| 20. Backprop Reflex | backprop-reflex.md | 102-conclude-command.md, lessons-format.md | 2+ | MEDIUM |
| 21. RARV Reflection | rarv-reflection.md | 101-conclude-processing.md, context-layer.md, anti-sycophancy.md | 2+ | LOW |
| 22. Token Budget | token-budget.md | 102-conclude-command.md, caveman-integration.md, 3layer-query-rule.md | 2+ | MEDIUM |
| 23. Fallback Hierarchy | error-handling-and-recovery.md | context-layer.md, graph-query-patterns.md | 1-2 | HIGH |
| 24. Sequential Recovery | error-handling-and-recovery.md | All workflow specs, decorator-wrapper-pattern.md | 1-2 | HIGH |
| 25. Code Graph Query | graph-query-patterns.md | graph-storage-structure.md, code-and-document-maps.md | 1-2 | HIGH |
| 26. (RESERVED for future patterns) | | | | |

---

## Pattern Index by Use Case

### Patterns for **Spec-Driven Development (Specify Phase)**
- Decorator Wrapper Pattern (wrapping SpecKit.specify)
- Context Injection Pattern (loading vault decisions/patterns)
- Enrichment Layer Pattern (injecting context)
- Anti-Sycophancy Validation (catch contradictions)
- Three-Layer Query Rule (efficient context loading)
- Three-Layer Memory Model (context sources)

### Patterns for **Planning & Architecture (Plan Phase)**
- Enrichment Layer Pattern (injecting code graph + decisions)
- Context Injection Pattern (loading decisions + patterns + code graph)
- Hybrid Graph Pattern (query code+doc relationships)
- Code Graph Query Pattern (find dependencies, impact analysis)
- Token Budget Tracking (monitor context loading costs)

### Patterns for **Implementation (Implement Phase)**
- Decorator Wrapper Pattern (wrapping SpecKit.implement)
- Sequential Error Recovery (error handling per task)
- Fallback Hierarchy (graceful degradation)
- Blind Code Review (independent validation)

### Patterns for **Post-Feature (Post Phase)**
- Post-Processing Pattern (artifact collection + archival)
- Caveman Compression Mode (token-efficient lessons)
- Feature State Tracking (completion tracking)
- Session-to-Vault Archival (ephemeral → permanent)
- Auto-Tagging + Auto-Wikilink (knowledge interconnection)
- RARV Reflection Pattern (alignment verification)
- Backprop Reflex (test failure learning)

### Patterns for **Knowledge Persistence**
- Three-Layer Memory Model (multi-layer storage)
- Zettelkasten Convention (atomic, interconnected notes)
- Auto-Tagging + Auto-Wikilink (automation)
- Session-to-Vault Archival (permanent preservation)

### Patterns for **Error Handling & Resilience**
- Error Categorization Pattern (classify errors)
- Fallback Hierarchy Pattern (graceful degradation)
- Sequential Error Recovery Pattern (structured recovery)

### Patterns for **Performance & Efficiency**
- Three-Layer Query Rule (token optimization)
- Code Graph Query Pattern (fast queries)
- Incremental Sync Pattern (cache efficiency)
- Caveman Compression Mode (token reduction)
- Token Budget Tracking (cost visibility)

### Patterns for **Quality & Validation**
- Anti-Sycophancy Validation (catch AI drift)
- Blind Code Review (independent assessment)
- RARV Reflection (alignment verification)
- Backprop Reflex (test failure learning)

### Patterns for **Orchestration & Workflow**
- Feature Lifecycle Pattern (phase sequencing)
- Skill Chaining Pattern (dependency management)
- Feature State Tracking (progress visibility)

### Patterns for **Knowledge Graphs & Queries**
- Hybrid Graph Pattern (code+doc unification)
- Graph Merge Integration (combine node types)
- Incremental Sync Pattern (efficient updates)
- Code Graph Query Pattern (queryable structure)

---

## Implementation Checklist (per Pattern)

Each pattern follows this verification checklist:

- ✅ **Spec Written:** Full specification exists and is linked
- ✅ **Concept Clear:** What problem it solves is explicit
- ✅ **Solution Documented:** How it works is described
- ✅ **When/When-Not:** Use cases clearly defined
- ✅ **Example Code:** Code snippet or integration point shown
- ✅ **Related Patterns:** Cross-links to other patterns
- ✅ **Primary Spec Identified:** Single authoritative source
- ✅ **Supporting Specs Identified:** Related specs listed
- ✅ **Phase Introduced:** Phase 0/1/2 noted
- ✅ **Status:** ACTIVE/DEPRECATED/PROPOSED noted
- ✅ **Frequency:** HIGH/MEDIUM/LOW adoption rate noted

---

## How to Use This Document

### For Pattern Discovery
1. **Search by use case:** See "Pattern Index by Use Case" section
2. **Search by problem:** Use CTRL+F to find pattern names/problems
3. **Follow cross-references:** Each pattern links to related patterns

### For Implementation
1. **Find pattern:** Look up pattern by name or use case
2. **Read spec:** Click primary spec link
3. **Check related patterns:** Ensure dependencies are understood
4. **Review code examples:** Copy and adapt
5. **Check integration points:** Understand where pattern fits in workflow

### For Extension
1. **Identify gap:** What recurring problem exists without a pattern?
2. **Check if pattern exists:** Search document + related specs
3. **If new pattern needed:** Document in wiki/patterns/<PATTERN-NAME>-quick-ref.md (see next section)
4. **Update this file:** Add to Pattern Catalog + Index

---

## Quick Reference: Top 10 Most-Used Patterns

1. **Decorator Wrapper Pattern** — Used in: `/spek.plan` (all phases), `/spek.implement`
2. **Three-Layer Memory Model** — Used in: All skills (read/write context)
3. **Feature Lifecycle Pattern** — Used in: All skills (phase sequencing)
4. **Error Categorization Pattern** — Used in: All skills (error handling)
5. **Enrichment Layer Pattern** — Used in: `/spek.plan` specify/plan phases
6. **Context Injection Pattern** — Used in: Decorator wrapper PRE layer
7. **Three-Layer Query Rule** — Used in: Context loading (optimize tokens)
8. **Caveman Compression Mode** — Used in: `/spek.conclude` (lessons generation)
9. **Skill Chaining Pattern** — Used in: `/spek.plan` orchestration
10. **Feature State Tracking Pattern** — Used in: All skills (progress visibility)

---

**Document Version:** 2026-05-20  
**Last Updated:** 2026-05-20  
**Next Review:** Phase 3 (planned)
