# Pattern Library: Reusable Patterns from Spekificity Architecture

## Overview

Reusable patterns extracted from Spekificity specifications. Each pattern solves a recurring problem and links to its authoritative spec.

---

## Quick Reference

| # | Pattern | Category | Problem | Spec | Adoption |
|---|---------|----------|---------|------|----------|
| 1 | Decorator Wrapper | Architectural | Extend without modifying internals | [decorator-wrapper-pattern.md](wiki/specs/decorator-wrapper-pattern.md) | ✅ ACTIVE |
| 2 | Three-Layer Memory | Architectural | Persist context across sessions | [memory-architecture.md](wiki/specs/memory-architecture.md) | ✅ ACTIVE |
| 3 | Three-Layer Query | Query | Optimize token usage hierarchically | [3layer-query-rule.md](wiki/specs/3layer-query-rule.md) | 🟢 S3 |
| 4 | Enrichment Layer | Architectural | Inject context into SpecKit | [enrichment-layer.md](wiki/specs/enrichment-layer.md) | ✅ ACTIVE |
| 5 | Context Injection | Integration | Load & compose context | [context-layer.md](wiki/specs/context-layer.md) | ✅ ACTIVE |
| 6 | Feature Lifecycle | Workflow | End-to-end orchestration | [cli-orchestration.md](wiki/specs/cli-orchestration.md) | ✅ ACTIVE |
| 7 | Error Categorization | Error Handling | Classify errors for recovery | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | ✅ ACTIVE |
| 8 | Zettelkasten | Memory | Atomic notes + frontmatter | [zettelkasten-conventions.md](wiki/specs/zettelkasten-conventions.md) | 🟢 S1 |
| 9 | Caveman Compression | Compression | Reduce tokens substantially | [caveman-integration.md](wiki/specs/caveman-integration.md) | ✅ ACTIVE |
| 10 | Auto-Tagging | Memory | Automate knowledge links | [auto-tagging-wikilinks.md](wiki/specs/auto-tagging-wikilinks.md) | 🟢 S2 |
| 11 | Skill Chaining | Integration | Sequential execution | [spek-automate-workflow.md](wiki/specs/spek-automate-workflow.md) | ✅ ACTIVE |
| 12 | Post-Processing | Workflow | Artifact → compress → archive | [101-conclude-processing.md](wiki/specs/101-conclude-processing.md) | ✅ ACTIVE |
| 13 | Hybrid Graph | Graph | Unify code + doc nodes | [code-and-document-maps.md](wiki/specs/code-and-document-maps.md) | 📅 FUTURE |
| 14 | Graph Merge | Graph | Combine node types | [graph-merge-integration.md](wiki/specs/graph-merge-integration.md) | 📅 FUTURE |
| 15 | Incremental Sync | Graph | Cache + file watch | [graph-refresh-strategy.md](wiki/specs/graph-refresh-strategy.md) | 🟢 S4 |
| 16 | Feature State | State Mgmt | Track lifecycle phases | [feature-state-tracking.md](wiki/specs/feature-state-tracking.md) | ✅ ACTIVE |
| 17 | Session-to-Vault | Memory | Ephemeral → permanent | [session-logs-vault-artifacts.md](wiki/specs/session-logs-vault-artifacts.md) | 🟢 S5 |
| 18 | Anti-Sycophancy | Validation | Flag AI drift | [anti-sycophancy.md](wiki/specs/anti-sycophancy.md) | 📅 FUTURE |
| 19 | Blind Review | Validation | Anon. review | [blind-code-review.md](wiki/specs/blind-code-review.md) | 📅 FUTURE |
| 20 | Backprop Reflex | Validation | Test failures → learning | [backprop-reflex.md](wiki/specs/backprop-reflex.md) | 🟡 C1 |
| 21 | RARV Reflection | Validation | Alignment cycle | [rarv-reflection.md](wiki/specs/rarv-reflection.md) | 🟡 C2 |
| 22 | Token Budget | Compression | Monitor costs | [token-budget.md](wiki/specs/token-budget.md) | 📅 FUTURE |
| 23 | Fallback Hierarchy | Error Handling | Graceful degradation | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | ✅ ACTIVE |
| 24 | Sequential Recovery | Error Handling | Pre-core-post recovery | [error-handling-and-recovery.md](wiki/specs/error-handling-and-recovery.md) | ✅ ACTIVE |

**Legend:** ✅ ACTIVE = Implemented | 🟢 S1–S5 = Should adopt soon | 🟡 C1–C2 = Consider later | 📅 FUTURE = Research phase

---

## Adoption Priority

**HIGH (implement now):** Patterns 1-7, 9, 11-12, 16, 23-24  
**MEDIUM (target S2):** Patterns 8, 10, 15, 17, 20-21  
**FUTURE:** Patterns 13-14, 18-19, 22

---

## Full Reference

### Architectural Patterns

#### Pattern 1: Decorator Wrapper Pattern

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
├── vault/vision.md
├── vault/patterns.md
└── vault/lessons/<YYYY-MM-DD>-<feature>-*.md

Layer 2: Repo Memory — Persistent, Project-Scoped
├── .spek/memory/architecture-index.md
├── .spek/memory/patterns-summary.md
└── (synced by /spek.conclude, read by /spek.context)

Layer 3: Session Memory — Ephemeral, Session-Scoped
├── .spek/memory/session/context-loaded.md
├── .spek/memory/session/current-feature.md
└── .spek/memory/session/scratchpad.md (deleted at feature end)
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

_Note: Pattern 3 (Three-Layer Query Rule) — Implementation details in [decision.md](decision.md#decision-6) (Decision 6). See adoption guidance above._

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

_Note: Pattern 8 (Zettelkasten Convention) — Implementation details in [decision.md](decision.md#decision-4) (Decision 4). See adoption guidance above._

---

_Note: Pattern 10 (Auto-Tagging + Auto-Wikilink) — Implementation details in [decision.md](decision.md#decision-5) (Decision 5). See adoption guidance above._

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

_Note: Pattern 13 (Token Budget Tracking) — Implementation details in [decision.md](decision.md#decision-12) (Decision 12). See adoption guidance above._

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
- Action: FAIL + GUIDANCE (do not fallback for core automation; surface actionable error)
- Recovery: Manual intervention or CI provisioning (do not auto-fallback to cache for core flows)

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
When primary systems fail (graph stale, non-vault services), workflow should degrade gracefully, not crash.

Exception: For Obsidian vault exports, Spekificity requires the Obsidian CLI; vault export failures are considered authoritative failures for core automation and must fail-fast (no automatic fallback to cache/plugin exports).

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

_Note: Patterns 19-22 (Anti-Sycophancy, RARV, Backprop, Blind Review) — Implementation details in [decision.md](decision.md#decision-10) (Decisions 10-11). See adoption guidance above._

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
- **Create:** `/spek.prepare` Step 6 (initialized status in `.spek/memory/session/current-feature.md`)
- **Update:** Each skill updates status through defined phases (drafted → planned → implementing → completing → completed)
- **Archive:** `/spek.conclude` Step 9 (archived in vault or deleted)

### Related Patterns
- Feature Lifecycle Pattern (phases that state tracks)
- Session-to-Vault Archival Pattern (archival process)

### Specs Using This Pattern
- Primary: [feature-state-tracking.md](wiki/specs/feature-state-tracking.md)
- Supporting: [cli-orchestration.md](wiki/specs/cli-orchestration.md), [100-prepare-command.md](wiki/specs/100-prepare-command.md)

---

## Pattern-Spec Mapping

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

## How to Use

**Discovery:** See "Pattern Index by Use Case" below. Use CTRL+F for problem names.  
**Implementation:** Find pattern → read spec link → check related patterns → review examples.  
**Extension:** Identify gap → check if pattern exists → add to spec catalog and this index.

---

## Top 10 Most-Used Patterns

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
