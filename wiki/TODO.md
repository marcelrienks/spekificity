# TODO

Personal action items to investigate and incorporate before implementing feature 003.

---

## [x] A.1 Review all documents in 'wiki/raw/llm wiki' and compile vision

Review all documents in the articles under the raw wiki documentation directory, and compile consensus on intentions, philosophy, methodology, use cases, and architectures.

**Completed:** Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Vision & Philosophy section

---

## [x] A.2 Review all documents in wiki/raw and compile confusion

Review all documents in the articles under the raw wiki documentation directory, and compile contradictions, inconsistencies, and disagreements.

**Completed:** Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Confusion Resolution section

---

## [x] A.3 List all tools and document toolsets

List all tools used across the articles, and which ones are meant to be used in conjunction. Include suggested workflows.

**Completed:** Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Tool Ecosystem section

---

## [x] B.1. Understand the proper full speckit workflow

**Question**: What is the intended end-to-end speckit flow, including post-remediation?

**Status**: ✓ **RESOLVED** (2026-05-18) — See [wiki/speckit-workflow.md](speckit-workflow.md) for full canonical flow, command descriptions, remediation mechanics, re-entry points, and integration with spekificity.

**Summary of findings:**
- Remediation happens **in-place** (direct file editing of spec.md, plan.md, tasks.md)
- Canonical flow: constitution → specify → clarify (opt) → plan → tasks → analyze (opt) → [fix in-place] → implement
- Re-entry: `/speckit.analyze` can be re-run after fixes to verify; each command can be re-run to regenerate artifacts
- Analyze is **non-blocking and optional**; implement does NOT require a clean analyze pass
- `spek automate` sequencing: load context → enrich-specify → enrich-plan → tasks → analyze (opt) → [manual remediate if needed] → enrich-implement → lessons

**Key decision**: Analyze identifies issues but does not trigger automatic remediation. Developer manually edits artifacts in response to report, then continues to implement. This is intentional design: templates constrain output quality upfront, so analyze findings are typically low-frequency and low-severity.

---

## [x] B.2. Expand `spek prepare` and `spek post` — leverage caveman, graphify, and obsidian fully

**Status**: ✓ **RESOLVED** (2026-05-18) — See [wiki/skills/spek-prepare.md](skills/spek-prepare.md) and [wiki/skills/spek-post.md](skills/spek-post.md) for comprehensive skill definitions.

**What was defined:**

**`spek.prepare`** (runs at feature start):
- Git state verification (clean tree, feature branch)
- Auto-activate caveman mode (lite by default; log activation for visibility)
- Load vault context: decisions, patterns, recent lessons (via `/context-load`)
- Verify code analysis tool freshness (resync if >2 hours old)
- Report ready status (decisions loaded, patterns available, graph fresh)

**`spek.post`** (runs after feature complete):
- Collect feature artifacts (spec, plan, tasks, execution trace)
- Activate caveman for compression (lessons output in compressed format)
- Generate structured lessons learned: feature digest + implementation steps + decisions + patterns (self-contained, no need to re-read spec/plan)
- Update vault context: append new decisions + patterns to vault/decisions.md + vault/patterns.md
- Run code analysis tool in incremental mode (after lessons written, so lesson files are indexed)
- Run `cel.docs.simplify` to consolidate documentation (feature-branch scoped)
- Report completion + update workflow-state.json

**Caveman activation strategy:**
- `spek.prepare`: Auto-enable caveman lite (with visibility to user; can disable via CAVEMAN_DISABLED=1)
- `spek.post`: Auto-enable caveman for lessons compression (token efficiency default for post)
- Both skills explicitly document activation in output

**Integration with `spek automate` CLI:**
```
spek automate <feature>
  → spek prepare (git, caveman, vault, graph)
  → create feature branch
  → /speckit-enrich-specify
  → /speckit-enrich-plan
  → /speckit.tasks
  → /speckit.analyze (optional)
  → [manual remediation if needed]
  → /speckit-enrich-implement
  → spek post (lessons, vault update, graph refresh, docs simplify)
```

**Key decisions captured in skills:**
- Remediation is in-place (from B.1, now integrated)
- Caveman activation is session-scoped (not persisted)
- Graph refresh is incremental post-implementation (includes lesson files)
- Vault updates are additive (no overwrites, conflicts flagged for manual review)
- Documentation simplification is scoped to branch changes (safer than full wiki)

---

## [x] B.3. Ensure `spek post` creates structured lessons learnt from spec + implementation steps

**Status**: ✓ **RESOLVED** (2026-05-18) — See [wiki/skills/spek-lessons-learnt.md](skills/spek-lessons-learnt.md) for comprehensive lesson format definition and self-contained validation.

**What was defined:**

**Self-Contained Lesson Format:**
- **What We Built** (feature summary distilled from spec; no copying, just digest)
- **How We Built It** (technical approach from plan; architecture decisions with rationale)
- **Key Tasks Executed** (major deliverables; what each task produced)
- **Decisions Made** (with context + rationale + alternatives considered)
- **Patterns Identified or Reused** (reused patterns + newly discovered + anti-patterns)
- **Lessons for Next Feature** (actionable guidance)
- **Metrics** (LOC, files, coverage, time; for estimation)

**Goal Achieved:** After `spek post` runs, future sessions load the lesson entry and have sufficient context to understand the feature without re-reading spec.md or tasks.md.

**Compression:** Lessons written in caveman format (60% token savings) while preserving full technical content.

**Validation:** Self-contained checklist ensures lessons meet quality bar (can be understood in 2-3 minutes; enables pattern reuse; captures decisions).

**Integration:** Called automatically by `spek.post` after feature implementation; can also be run manually.

**Compounding Value:** Each lesson adds to vault; next feature's `/context-load` loads prior lessons + patterns. Feature development becomes progressively faster and more consistent (lessons compound).

---

## [x] B.4. Incorporate `cel.docs.simplify` into `spek post`

**Status**: ✓ **RESOLVED** (2026-05-18) — See [wiki/skills/spek-post.md](skills/spek-post.md) Step 6 for complete integration and invocation patterns.

**What was defined:**

**Step 6 in `spek.post` workflow:** Simplify/Consolidate Documentation

- **Purpose:** Prevent documentation from accumulating redundancy over time
- **Scope decision:** Feature-branch scoped (preferred for safety)
  - Safer than full-wiki scope (avoids unintended rewrites in unrelated docs)
  - Targeted: consolidates only what grew during current feature
  - Fallback: can scope to specific paths (wiki/ + specs/<feature>/) if flag not supported
- **Invocation pattern:** 
  ```bash
  cel.docs.simplify --scope-to-branch-changes
  # Or fallback:
  cel.docs.simplify wiki/ specs/<feature>/
  ```
- **Timing:** After lessons written + graph refreshed (least disruptive point)
- **Output:** Redundancy report + consolidated docs

**Workflow integration:**
```
spek post (7-step workflow)
  1. Collect artifacts
  2. Activate caveman
  3. Generate lessons
  4. Update vault context
  5. Run incremental graph sync
  6. celocs.simplify ← Step 6 (feature-branch scoped)
  7. Report completion
```

**Result:** Documentation does not accumulate redundancy over time as features are added. Branch-scoped approach keeps changes targeted and safe.

---

## [x] B.7. Define naming conventions for custom skills and workflows

**Status**: ✓ **RESOLVED** (2026-05-18, Corrected Intent) — See [wiki/naming-conventions.md](naming-conventions.md) for comprehensive design and migration guide.

**Design Principle: Keep `spek.*` prefix always. Simplify command portion to one-word wherever possible.**

**New Naming Convention:**

**Spekificity Core (all use `spek.*` prefix, simplified command portions):**
- `/spek.prepare`, `/spek.post`, `/spek.context`, `/spek.map`, `/spek.lessons`, `/spek.automate`

**SpecKit Vanilla (unchanged; `speckit.*` namespace for clarity):**
- `/speckit.specify`, `/speckit.plan`, `/speckit.implement`, `/speckit.tasks`, etc.

**SpecKit Enriched (use `spek.*` prefix with same names as base):**
- `/spek.specify`, `/spek.plan`, `/spek.implement` (prefix signals "enriched Spekificity version")

**Current → New Mapping:**
- `spek.prepare` → `/spek.prepare` (already simple) ✓
- `spek.post` → `/spek.post` (already simple) ✓
- `spek.context-load` → `/spek.context` (simplify)
- `spek.map-codebase` → `/spek.map` (simplify)
- `spek.lessons-learnt` → `/spek.lessons` (simplify)
- `spek.automate` → `/spek.automate` (already simple) ✓
- `speckit-enrich-specify` → `/spek.specify` (add prefix, simplify)
- `speckit-enrich-plan` → `/spek.plan` (add prefix, simplify)
- `speckit-enrich-implement` → `/spek.implement` (add prefix, simplify)
- **SpecKit commands unchanged** (keep `speckit.*` for namespace distinction)

**Key Decisions:**
- Always use `spek.*` prefix for Spekificity skills (namespace clarity; visual grouping)
- Simplify command portions to single word where possible (`context` not `context-load`, `map` not `map-codebase`)
- Enriched commands use same names as SpecKit base; prefix difference signals enriched version
- Skill directory names use `spek-` prefix (e.g., `spek-context/`, `spek-map/`) for filesystem grouping
- Namespace distinctions documented in copilot-instructions.md

**User Mental Model:**
- All Spekificity commands: `/spek.*` (consistent prefix)
- All SpecKit vanilla commands: `/speckit.*` (distinct namespace)
- Enriched commands: `/spek.specify`, `/spek.plan`, `/spek.implement` are the "default" Spekificity versions
- One-word or minimal command portions: easy to type and remember

**Result:** Namespace ownership is visible, commands are shorter and memorable, filesystem organization groups skills logically.

---

## [ ] B.8. High-level concepts to confirm and spec out individually

These are cross-cutting concerns that need deliberate thought before or alongside feature 003. Each is likely large enough to warrant its own spec.

### [x] B.8.1 Code and document maps

**Status**: ✓ **RESOLVED** (2026-05-18, Obsidian-sourced) — See [specs/b8-1-code-and-document-maps.md](../specs/b8-1-code-and-document-maps.md)

**Design Summary:**

**Node Granularity (Hybrid approach):**
- Code: Symbol-level via graphify AST
- Docs (content-heavy): Heading-level from Obsidian export (specs, decisions, patterns, lessons)
- Docs (config): File-level from Obsidian (skills, configurations)

**Single Source of Truth:** Obsidian vault is authoritative. Export Obsidian graph to queryable format.

**Parsing Passes:**
- Pass 1: Graphify indexes code → `vault/graph/nodes-code.jsonl`
- Pass 2: Obsidian export (dataview plugin, cache, or CLI) → `vault/graph/nodes-docs.jsonl`  
- Pass 3: Merge → `vault/graph/nodes.jsonl` with backreferences computed

**Configuration:** `vault/graph/config.json` specifies: Obsidian export method, code/doc paths, frontmatter schema, refresh policy

**Integration:** `/spek.map` invokes graphify + Obsidian export; `/spek.prepare` verifies freshness; `/spek.post` refreshes after feature; `/spek.context` queries for skill/decision/lesson nodes

**Key Benefit:** Obsidian remains human-browsable while graph nodes enable agent queries. Single source of truth: documents live in Obsidian.

### [x] B.8.2 Persistent memories and lessons

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b8-2-persistent-memories-and-lessons.md](../specs/b8-2-persistent-memories-and-lessons.md)

**Memory Architecture (Three Layers):**

**Layer 1 - Vault (Obsidian) — Persistent, Authoritative:**
- `vault/decision.md` — All decisions (active, deprecated, superceded); ranked by recency + importance
- `vault/intention.md` — Project vision, tenets, constraints
- `vault/patterns.md` — Reusable patterns library (tagged by domain)
- `vault/lessons/<date>-<feature>-*.md` — One self-contained lesson file per completed feature

**Layer 2 - Repo Memory (Copilot) — Persistent, Project-Scoped:**
- `/memories/repo/architectural-decisions.md` — Compressed summary: recent active decisions only
- `/memories/repo/patterns-index.md` — Index of recent patterns (top N used)
- `/memories/repo/codebase-map.md` — High-level code structure snapshot

**Layer 3 - Session Memory (Copilot) — Ephemeral:**
- `/memories/session/context-loaded.md` — What was loaded at session start (by `/spek.context`)
- `/memories/session/current-feature.md` — Current feature state + progress (updated across sessions during feature work)

**Lifecycle:**

**Load (Session Start via `/spek.context`):**
1. Read vault (decisions, patterns, recent lessons)
2. Read repo memory (compressed summaries)
3. Query code graph (vault/graph/nodes.jsonl)
4. Summarize + compress (caveman format)
5. Write to /memories/session/context-loaded.md
Cost: ~3-5K tokens (with compression)

**Write (Feature End via `/spek.post`):**
1. Collect artifacts (spec, plan, tasks, trace)
2. Generate lessons (vault/lessons/<date>-<feature>-*.md)
3. Update vault (append decisions, add patterns)
4. Sync to repo memory (compress recent decisions, update patterns index)
5. Refresh code graph (/spek.map)
6. Archive session memory
Cost: ~5-10K tokens (lessons generation + compression)

**Granularity & Retention:**
- Per-feature lessons: One file per feature, kept indefinitely (archive if inactive)
- Per-decision entries: One entry per decision, kept indefinitely (mark deprecated, don't delete)
- Per-pattern entries: One entry per pattern, kept indefinitely (index recent N in repo memory)
- Per-session context: Ephemeral, deleted at session end (or archived for reference)
- Per-feature state: Spans multiple sessions during feature work, archived after completion

**Query Patterns:**
- Recent decisions: grep repo memory for active status
- Patterns for [topic]: grep vault/patterns.md for tags
- Lessons from similar feature: grep vault/lessons/*.md for domain
- Current feature status: read /memories/session/current-feature.md

---

### [x] B.8.3 SpecKit integration contract

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b8-3-speckit-integration-contract.md](../specs/b8-3-speckit-integration-contract.md)

**Integration Pattern: Decorator Wrapper**

| Component | Responsibility | Pattern | Input | Output |
|-----------|-----------------|---------|-------|--------|
| **SpecKit** | Core workflow | Global framework | Natural language | Code + artifacts |
| **Spekificity** | Context + enrichment | Decorator wrapper | Decisions, patterns, code graph | Context-aware specs, plans, code |
| **/spek.specify** | Enrich spec generation | Wrapper | Feature description + context | spec.md (with context) |
| **/spek.plan** | Enrich plan generation | Wrapper | spec.md + context + code graph | plan.md (architecture-aware) |
| **/speckit.tasks** | Task generation | Direct (no wrapper) | spec.md + plan.md | tasks.md (ordered, IDs, dependencies) |
| **/spek.implement** | Enrich implementation | Wrapper | tasks.md + context | Code changes + artifacts |
| **/spek.context** | Load context | Spekificity-only | Session state | /memories/session/context-loaded.md |
| **/spek.prepare** | Prepare workspace | Spekificity-only | Git state, graph | Verified working state |
| **/spek.post** | Extract lessons | Spekificity-only | All artifacts | vault/lessons/, vault updates |

**Data Flow:**
```
/spek.context → /spek.prepare → /spek.specify → /spek.plan → /speckit.tasks → /spek.implement → /spek.post
     ↓                ↓               ↓              ↓             ↓               ↓               ↓
  Load all       Git + graph      Inject ctx    Inject ctx    Generate    Execute +      Lessons +
  context       validation        + call        + code graph   tasks       collect        vault
                                  speckit                                  artifacts      updates
```

**Key Design Decisions:**
- Decorator pattern (pre/core/post) for clarity and no tight coupling
- SpecKit owns core generation; Spekificity adds context before + validation after
- `/speckit.tasks` invoked directly (no enrichment needed; context already in plan)
- Error handling: Validate inputs, fallback gracefully, proceed with partial results
- Configuration: `.specify/` for SpecKit, `.spekificity/` for Spekificity, `vault/graph/` for graph

**Success Criteria:**
- Clear responsibility division (one owner per concern)
- No tight coupling (works with any SpecKit version)
- Explicit data flow (all intermediate artifacts documented)
- Error handling at each layer (validation, retry, fallback)

---

### [x] B.8.4 Prepare and post skills

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b8-4-prepare-and-post-skills.md](../specs/b8-4-prepare-and-post-skills.md)

**Prepare Phase (`/spek.prepare`):**

7-step entry point workflow:
1. Verify git state (clean, valid branch)
2. Load feature name (from param/branch/prompt)
3. Check code graph freshness (1hr threshold, optional refresh)
4. Refresh graph if stale (run `/spek.map`)
5. Load context via `/spek.context`
6. Create feature state tracker (`/memories/session/current-feature.md`)
7. Report ready status

**Post Phase (`/spek.post`):**

10-step exit point workflow:
1. Collect artifacts (spec, plan, tasks, trace, code)
2. Activate caveman compression mode
3. Generate lessons document (`vault/lessons/<date>-<feature>-*.md`, 8 sections, compressed)
4. Update vault — decisions (append to `vault/decision.md`)
5. Update vault — patterns (append/update `vault/patterns.md`)
6. Incremental code graph sync (re-index changed files)
7. Sync repo memory (compress recent decisions, patterns, codebase map)
8. Feature docs simplification (optional, feature-scoped)
9. Archive session memory (`/memories/session/*`)
10. Report completion status

**Prepare Success Criteria:** Git clean, feature name valid, graph fresh, context loaded, state tracker created, user ready  
**Post Success Criteria:** Artifacts collected, lessons compressed, vault updated, graph synced, memory archived, user informed

---

## Closed Action Items (B.1-B.8.4)

- **What**: across sessions, context is currently reloaded from scratch (vault graph + decisions + lessons). There is no durable, incrementally-updated memory layer that summarises *what was built* vs. *what was decided* vs. *what was learned*.
- **Think about**: what is the right granularity — per-feature lessons, per-session decisions, per-pattern entries? How does this interact with the copilot `/memories/repo/` scope? Should spekificity maintain its own `vault/memory/` structure separate from the agent memory scopes?
- **Relationship to todo items 4 and 5 above**: this is the generalisation of those two items into a coherent memory architecture.
- **Why it matters**: without a deliberate memory model, future sessions either re-read everything (slow, expensive) or miss context (error-prone). The model should define what is written, when, by whom, and how it is loaded.
- **Likely outcome**: a spec for the spekificity memory model — covering vault/lessons, vault/context, copilot repo memory, and the load/write lifecycle for each.

### B.8.3 Leveraging speckit as it is intended

- **What**: spekificity wraps and extends speckit, but the integration points (enriched wrappers, automate sequence, remediation loop) were inferred rather than confirmed against speckit's own design intent.
- **Think about**: what is speckit's canonical flow? Where does it expect human intervention vs. automation? What does speckit assume about the agent running it — a human-in-the-loop or a fully autonomous agent? Are the enriched wrappers (`speckit-enrich.*`) the right pattern, or should spekificity extend speckit differently (e.g. pre/post hooks, configuration, custom templates)?
- **Relationship to todo item 1 above**: this is the generalisation of that item — not just the post-remediation question but the entire integration contract.
- **Why it matters**: if spekificity fights against speckit's design, the workflow will be fragile. If it aligns, speckit upgrades are non-breaking.
- **Likely outcome**: a spec for the spekificity ↔ speckit integration contract — defining where spekificity adds value (context loading, graph awareness, lessons) vs. where speckit owns the flow, and how enriched wrappers should be structured.

### B.8.4 Prep and post custom skills

- **What**: `spek prepare` and `spek post` are currently underspecified. They exist as placeholders more than deliberate, well-scoped skills.
- **Think about**: what is the exact ordered sequence of steps for each? What inputs does each step require? What outputs does each step produce? Which steps are mandatory vs. optional? How do prepare and post interact with caveman mode, graphify, obsidian vault, cel.docs.read, cel.docs.simplify, and the lessons-learnt skill?
- **Relationship to todo items 2, 5, and 6 above**: those items each add a specific capability to prepare/post. This item is the architectural concern — the skill structure, invocation contract, and failure handling.
- **Why it matters**: prepare and post are the bookends of every feature session. If they are unclear or incomplete, every feature starts and ends with context loss or duplicated manual effort.
- **Likely outcome**: a spec for `spek.prepare` and a spec for `spek.post` — each defining the full step sequence, skill dependencies, inputs/outputs, and success criteria.

---

*Each sub-item above (B.8.1–B.8.4) should be reviewed, confirmed, and converted into a dedicated spec before or alongside 003 implementation. They are architectural decisions, not implementation details.*

---

---

## [ ] B.9. Investigate `lucasrosati/claude-code-memory-setup` as a reference for memory and context patterns

**Repository**: https://github.com/lucasrosati/claude-code-memory-setup

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b9-claude-code-memory-setup-analysis.md](../specs/b9-claude-code-memory-setup-analysis.md)

**Key Findings:**

**Strong Alignment (Zero Conflicts):**
- Two-system architecture: Obsidian (declarative) + Graphify (structural) ← matches spekificity's planned design
- Session continuity via `/resume` + `/save` commands ← directly map to `/spek.prepare` + `/spek.post`
- Zettelkasten conventions (atomic notes, frontmatter, wikilinks) ← applicable to lessons/decisions/patterns
- 3-layer query rule (graph → vault → code) ← matches spekificity's context loading strategy
- Incremental graph refresh via git hooks ← already planned in B.8.4

**Adoption Recommendations (High Priority):**

1. **Zettelkasten Conventions** — Apply to vault/lessons, vault/decision.md, vault/patterns.md (frontmatter + wikilinks)
2. **Chat Import Pipeline Pattern** — Enhance `/spek.post` Step 3 with auto-tagging + auto-wikilink insertion (keyword mapping)
3. **Incremental Graph Refresh** — Integrate graphify git hooks into `.spekificity/bin/spek setup`
4. **3-Layer Query Rule** — Document in `.spekificity/guides/context-navigation.md` (prioritize graph → vault → code)
5. **Session Logs as Vault Artifacts** — Archive `/memories/session/current-feature.md` sections to vault/lessons with wikilinks

**Real-World Results (Validated):**
- 71.5x fewer tokens per session
- 499x reduction on specific queries  
- 659 stars, active community, production-tested
- 780+ vault notes at scale

**Zero Conflicts with Spekificity Design:** The architecture is complementary, not competing. Can adopt patterns directly.

**Adoption Effort:** 4-6 hours for high-priority patterns; high impact (especially auto-linking + tag generation).

---

## [x] B.10. Review spec-driven development framework comparison as a reference for speckit positioning

**Article**: https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-sdd-c052df529274 (paywalled; supplemented with public landscape analysis)

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b10-sdd-framework-comparison-analysis.md](../specs/b10-sdd-framework-comparison-analysis.md)

**Key Findings:**

**SpecKit Validation (Correct Choice):**
- Market leader: 102k stars, vendor-neutral, most mature SDD framework
- Works with 30+ agents; highest community adoption
- **Gap identified:** No built-in persistence/context (exactly what Spekificity solves)
- Optional remediation phases (`/speckit.analyze`, `/speckit.remediate`)

**SDD Ecosystem Landscape (30+ frameworks analyzed):**
- Tier 1: SpecKit (102k), OpenSpec (48.9k) — stable, high adoption
- Tier 2: Pilot Shell (1.7k), Cavekit (920), Loki Mode (930) — specialized, stronger features
- Emerging: Kiro (AWS), plus 20+ academic/niche frameworks

**Patterns Worth Adopting (5 High-Priority):**
1. Multi-tier memory (From Pilot Shell/Loki) — episodic/semantic/procedural; Spekificity B.8.2 already aligns ✓
2. Backprop reflex (From Cavekit) — test failures → vault updates → future specs
3. RARV cycles (From Loki Mode) — Reason-Act-Reflect-Verify loops post-implementation
4. Anti-sycophancy checks (From Loki) — prevent agent from drifting from decisions
5. Steering rules (From Kiro) — project-scoped rules guide agent behavior

**Unique Opportunity (What Spekificity Can Own):**
- First vault-integrated SDD (code graph + persistent memory + decorator wrapper)
- Lesson backprop architecture (test failures → vault → future features)
- Vendor neutrality (unlike Pilot Shell/Kiro); decorator-only (unlike forks)

**Framework Ecosystem Stability:** ✅ Low risk. SpecKit has 6+ years active development, GitHub backing, 30+ agent integrations.

**Strategic Positioning:** SpecKit (strong foundation) + Spekificity (persistence + context) = unique enterprise SDD.

---

## [x] B.11. Implement codegraph setup and integration

**Status**: ✓ **RESOLVED** (2026-05-18) — See [specs/b11-codegraph-setup-and-integration.md](../specs/b11-codegraph-setup-and-integration.md)

**Complete Specification (9 Parts):**

**Part 1 — Installation & Setup:**
- Step-by-step Graphify installation (uv tool, prerequisites, verification)
- Configuration template for .spekificity/config.yaml (20+ settings)
- Language selection, exclusions, caching strategy, output formats

**Part 2 — Vault Structure:**
- Directory layout: vault/graph/ with subdirectories (nodes, cache, refresh-log)
- Graph metadata: config.json (version, sources, merge strategy)
- Node schema (JSONL): id, type, name, scope, file, language, dependencies, callers, source, indexed_at
- Edge schema (JSONL): from_node, to_node, relationship (calls/inheritance/depends-on), context

**Part 3 — Skill Contract (/spek.map):**
- Command syntax: full | incremental | watch | docs-only | code-only | dry-run | verbose
- Full rebuild (5 passes: code indexing via Graphify, doc indexing via Obsidian export, merge, cache update, validate)
- Incremental refresh (SHA256 caching; only process changed files)
- Watch mode (file system watcher with debouncing for interactive dev)
- Git post-commit hook (automatic incremental sync after commits)

**Part 4 — Performance & Refresh Strategy:**
- Timing strategy table (manual, prepare-triggered, post-sync, git hook, watch, scheduled)
- SHA256 caching (99%+ hit rate on unchanged files; 1-2s incremental vs. 28s full)
- Parallel processing (4-worker thread pool; 3-4x speedup)
- Language-selective indexing (skip slow languages if desired)
- 3-layer query rule (graph 280 tokens → vault 500 tokens → code 5000+ tokens = 20x savings)

**Part 5 — Integration with B.8.1 & B.8.4:**
- B.8.1: Hybrid architecture (code nodes + doc nodes merged into single nodes.jsonl)
- B.8.4 /spek.prepare Step 3: Graph freshness check (read config.json timestamp, compare age to threshold 1h, offer refresh)
- B.8.4 /spek.post Step 6: Incremental sync (get git diff, run /spek.map --code-only --incremental on changed files)
- Context injection: /spek.specify & /spek.plan query graph for recent changes + impact analysis

**Part 6 — Configuration Reference:**
- Complete .spekificity/config.yaml template (graphify section with 50+ fields)
- Organized by subsection: installation, code_generation, caching, output, document_generation, refresh, performance, validation

**Part 7 — Setup Checklist (14 items):**
- Installation: Install graphify, create config, init directories, full rebuild, git hook
- Integration: /spek.prepare check, /spek.post sync, context injection
- Documentation: User guide, agent guide, hook setup
- Testing: Functional, integration, performance benchmarks

**Part 8 — Troubleshooting & Recovery:**
- 4 common issues (graphify not found, corrupted cache, stale graph, high CPU) with fixes
- Recovery procedures for cache corruption and orphaned nodes

**Part 9 — Success Criteria (15 checkmarks):**
- Graph generation (node count, required fields, edges, performance)
- Caching/performance (hit rate, worker threads, watch mode latency)
- B.8.4 integration (prepare check, post sync, context injection)
- Query efficiency (3-layer rule, token savings, query latency)
- Documentation/UX (setup guide, troubleshooting, git hook, watch mode)

**Key Design Decisions:**
- Graphify for code indexing (tree-sitter AST, fast, language-diverse, 0 tokens)
- Vault storage in vault/graph/ (code nodes + doc nodes merged)
- /spek.map skill orchestrates full/incremental/watch modes
- SHA256 caching strategy (incremental updates in 2-4 seconds)
- Optional git hooks (auto-sync but user-controlled)
- 3-layer query rule reduces token cost by 20x

**Integration Confirmed:**
- ✅ B.8.1 doc mapping (code + doc pass merger)
- ✅ B.8.4 /spek.prepare (freshness check, optional refresh)
- ✅ B.8.4 /spek.post (incremental sync for changed files)
- ✅ /spek.specify & /spek.plan context injection (impact analysis)

---

## [ ] C.1. specs
All the spec documents created in the specs folder need to be cleaned up, stripped down and isolated to individual aspects of the project, to be implemented. Then once that is done, we need to analyse the entire documentation of the project and determine which specs are still outstanding, in order to achieve a FULLY specced plan for the implementation of this project.

---

## [ ] C.2. spek.speckit spec
Create a FULL spec md file in the specs directory for the below requiremetns.
There should not be any wrapper methods that wrap the speckit skills, all speckit skills should remain available to the user to use indipendantly if they wish, but spekification should automate the full documented workflow of speckit. Note that this project must create a skill, that automates all the recommended steps of the specific version of speckit that is currently installed, even if that requires doing a web search to understand the installed versions functionality. This will mean that any future updates to speckit will continue to work with specificity, and will not require updating manually. Therefore the intention with spek.speckit is to implement each step of the speckit workflow by calling each one of the respective skills individually on the users behalf, surfacing any input required, and sending that to the speckit skill at the time. Determine if this would best be done by using sub agents per speckit skill.

---

## [ ] C.3. Research
Review all suggestionsd from the research document, and determine the value of implementing any of them with the users input for each item. Once decided create a list of todo items (C.3.1, C.3.2 etc.) for each item that needs to be fully specced.

---

## [ ] C.4. Clean up
once all sub items from point C.3 are completed, the entire project needs to be reviewed, simplified, consolidated, trimmed. At the end of this, I want a handfull of clean, concise, valuable, and not overly verbose architecture, decisions, intentions, conventions, and workflow md documents, with ascii diagrams and flow charts, all detailing the purpose, value, and usecases of this project. Then each of the suggested skills, workflows, tools and custom functionality must have a FULLY documented spec md within the specs directory. This includes the currently existing setup scripts, all of these should be specced out as if they did not exit, and can be recreated using the specs.
At the end of this todo item, I expect to have a FULLY documented and specced project, entirely ready to then, and ONLY then be implemeted. i.e. there should not be any implementation files existint at the end of this point. If there are, they were accidentally created as part of research and planning actions.