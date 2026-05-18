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

### [ ] B.8.2 Persistent memories and lessons (NEXT)

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

## [ ] B.9. Investigate `lucasrosati/claude-code-memory-setup` as a reference for memory and context patterns

**Repository**: https://github.com/lucasrosati/claude-code-memory-setup

**Question**: What memory and context management patterns does this repository implement, and what can spekificity adopt or take inspiration from?

- Review how `claude-code-memory-setup` structures persistent memory across sessions.
- Identify any patterns for storing, loading, and refreshing context that complement or improve upon the current spekificity vault + lessons approach.
- Compare its memory lifecycle (write triggers, read triggers, invalidation) against spekificity's planned model (see item B.8.2 above).
- Note any tooling, file formats, or conventions that could be reused or adapted — particularly anything relevant to the `spek.prepare` / `spek.post` memory steps.

**Why it matters**: This repository was identified as a real-world example of Claude-based memory setup and may contain proven patterns that spekificity's memory architecture (item B.8.2) can build on rather than reinvent.

---

## [ ] B.10. Review spec-driven development framework comparison as a reference for speckit positioning

**Article**: https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-sdd-c052df529274

**Question**: How does speckit compare against the broader SDD landscape, and are there patterns or frameworks worth adopting or avoiding?

- Read the comparison of 15 spec-driven development frameworks to understand where speckit sits in the SDD ecosystem.
- Identify any frameworks with stronger remediation loops, persistent context, or automation pipelines that could inform spekificity's design.
- Note any frameworks whose spec → plan → implement flow differs significantly from speckit's — particularly around human-in-the-loop checkpoints (relevant to todo item B.1 and B.8.3).

---

## [ ] B.11. Implement codegraph setup and integration

**Question**: How should codegraph be configured, initialized, and integrated into the spekificity platform?

**Required setup**:

- **Installation & Configuration**: Define the installation process for graphify/codegraph tooling. Document where the tool should be installed (`.spekificity/bin/`, system PATH, or as a dependency), required configuration files, and any environment variables needed.
- **Vault Integration**: Establish how codegraph output feeds into the `vault/graph/` structure. Define the node schema for both code and documentation nodes (see B.8.1), and how the index is generated and stored.
- **Invocation in Skills**: Clarify how `spek.map-codebase` invokes codegraph — should it be a direct CLI call, a wrapper script, or an agent-based orchestration? Define the input/output contracts.
- **Incremental vs. Full Refresh**: Determine the refresh strategy — when should codegraph perform a full map (initial setup, after major refactoring) vs. incremental updates (after each feature, as part of `spek.post`)?
- **Performance and Scoping**: Document any performance considerations and whether the graph should cover the entire codebase or be scoped to active features/directories.

**Why it matters**: codegraph is referenced throughout the platform (context loading, B.8.1 doc mapping, B.2 prepare/post steps) but its setup is not yet documented. Without explicit setup instructions, `spek.map-codebase` and the vault loading steps remain partially specified.

**Likely outcome**: A step-by-step codegraph setup guide, configuration templates, and updated `spek.map-codebase` skill with clear invocation patterns and output expectations. Should be integrated into `.spekificity/guides/` and referenced in the `spek.prepare` flow.
