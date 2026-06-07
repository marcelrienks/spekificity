Technical Brief: Spekificity — Wiki Context

Last Deep Read: 2026-06-07 (UTC)

Project Purpose

- Spekificity: spec-driven agent development framework combining a Git-backed markdown vault, pre-indexed code graph (lat.md), deterministic spec engine (SpecKit), and composable agent skills to enable token-efficient, repeatable, auditable feature work.
- Install: Global via `uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git`
- Per-project: `spek init` scaffolds `.spek/` skills and initializes SpecKit + vault

Architecture & Tech Stack

- **Four Pillars:** Token Efficiency (Caveman compression + indexed graph), Determinism (SpecKit workflow), Persistence (Git-backed Obsidian vault), Autonomy (lat.md + indexed context)
- **Code Analysis:** lat.md is canonical (ONLY supported option). Provides pre-indexed symbols, calls, impact analysis via MCP tools. Supports incremental sync + optional file-watcher + git post-commit hooks.
- **Vault:** Git-backed Obsidian-style markdown vault (plain `.md` files, no server). Obsidian CLI required for automation (exports, graph, lesson extraction). Desktop app optional for visualization.
- **Spec Engine:** SpecKit (GitHub official) wraps specify CLI. Spekificity enriches via PRE (load context) → CORE (execute) → POST (validate) layers without forking SpecKit.
- **Compression:** Caveman modes (lite|full|ultra) for token budgets. Ultra achieves ~75% reduction while preserving code/URLs/function names exactly.
- **Memory Architecture:** Three layers. Vault (persistent, authoritative, slow) | Repo Memory (compressed cache, fast) | Session State (ephemeral).

Key Workflows

- **Feature Cycle:** /spek.prepare → /spek.plan (orchestrates /speckit.specify + /speckit.plan + /speckit.tasks) → /spek.implement (task execution) → /spek.conclude (archive + lessons + graph refresh)
- **Spec Structure:** Feature intent → enrichment layers (Success Criteria, Assumptions, Risk Assessment, Dependencies, Resource Estimate) → stored in vault
- **3-Layer Query Rule:** ALWAYS use hierarchically. Layer 1 (lat.md code graph, low-cost) → Layer 2 (vault summaries, moderate-cost) → Layer 3 (raw code files, high-cost). Escalate only when necessary.
- **Post-Processing:** /spek.conclude runs automated lesson extraction, auto-tagging + auto-wikilinks, failure pattern capture (backprop reflex), spec drift detection (RARV), and lat.md refresh
- **Zettelkasten Vault:** Atomic notes (one concept per file), YAML frontmatter (metadata, status, tags, created/updated), 2-4 wikilinks per note for graph density

Implementation Architecture

- **Programmatic Pipeline (canonical):** Deterministic outputs, typed contracts (Pydantic), content-addressable IDs (SHA256), integrated lint/repair agents, structural Markdown enforcement (markdown-hero). BM25 lexical retrieval by default.
- **Agentic AGENTS.md (experimental):** Lightweight for discovery/rapid iteration on small vaults (<200 docs). Requires plan-before-execute gating + allowlists; NOT for production ingest or reproducibility-critical flows.
- **Markdown Hygiene (mandatory):** No duplicate H1s, valid YAML frontmatter, parseable tables, correct nesting. Use section-aware chunking. CI lints; structural failures routed to repair agent or human review.
- **HTML Artifact Policy:** Store generated HTML outside primary wiki pages under `wiki/artifacts/html/`. Each must embed or link export-to-markdown. Host on static site (S3/Vercel) when appropriate.

Decision Highlights (Key Decisions 1-12)

- **Decision 1:** lat.md is the canonical, required code analysis tool (purpose-built for agent workflows, pre-indexed queries, MCP interface)
- **Decision 2:** Dual-system approach: Knowledge Vault (git-backed, slow, authoritative) + Code Analysis Tool (pre-indexed, fast, auto-synced on every file save)
- **Decision 4:** Zettelkasten architecture for vault (atomic notes, YAML frontmatter, wikilink density) enables automation, graph exports, AI-friendly queries
- **Decision 5:** Auto-tagging + auto-wikilink insertion during /spek.conclude (reduces manual linking labor, detects redundancy, prevents orphaned notes)
- **Decision 6:** 3-Layer Query Rule (code graph → vault → raw code) reduces token overhead vs naive file scans
- **Decision 7:** Git post-commit hook for auto graph refresh (optional but recommended) ensures Layer 1 queries always current
- **Decision 8:** Backprop Reflex (test failures → vault warnings) closes learning loop: failures → captured → prevent repeats in future features
- **Decision 9:** RARV Reflection Cycles (Reason-Act-Reflect-Verify) detect spec drift post-implementation; user chooses: fix code, justify deviation, or defer
- **Decision 10:** Anti-Sycophancy Validation (contradiction detection, complexity alerts, pattern consistency, tech stack drift) catches AI hallucinations early
- **Decision 11:** Blind Code Review (anonymize + independent checks: linting, tests, static analysis) unbiased quality gates post-implementation
- **Decision 12:** Token Budget Model (soft limits + warnings per phase, no hard caps) enables cost-aware decisions without blocking progress

Documentation Map

- wiki/vision.md — Vision, problem/solution, four pillars, philosophy, tenets
- wiki/architecture.md — Technical components, data flow, responsibilities, programmatic pipeline choice, retrieval guidance, HTML artifact policy
- wiki/workflow.md — Deterministic 4-stage feature workflow (Prepare → Plan [Specify + Task Breakdown] → Implement → Conclude); detailed per-stage steps, checklists, error recovery, example walkthrough
- wiki/conventions.md — File/directory naming (kebab-case, numeric prefixes for specs/lessons, date prefixes for lessons), skill directory → command prefix matching, agentic vs programmatic choice
- wiki/decision.md — 12 architectural decisions, tooling rationale (lat.md canonical, SpecKit chosen, Obsidian for vault, Caveman for compression), decision tree for configuration paths, conflict resolution rules
- wiki/patterns.md — 24 reusable patterns (architectural, query, workflow, memory, compression, error handling, validation, graph, state management), quick reference table, adoption priority
- wiki/setup.md — Installation steps for SpecKit (global via uv), Obsidian vault (local + CLI required), lat.md (global or local), post-installation verification
- wiki/skills.md — Command reference (/spek.* namespace: prepare, plan, implement, conclude, context, map, lessons; /lat.* code queries; /caveman compression; /context.* injection)
- README.md — Project summary, quick start (install globally, run spek init, execute /spek.* skills), key features, target tool stack, working assumptions

Working Assumptions (Core)

- Workflow: 4 main stages (Prepare → Plan [2 sub-stages] → Implement → Conclude)
- Commands: /spek.* prefix (agent skills, not shell CLI)
- Wrapping: Spekificity = decorator pattern on SpecKit (no fork)
- Vault: Markdown, Git-backed, persistent (decisions, patterns, lessons, specs)
- Obsidian CLI: REQUIRED for automation (vault syncs, exports, graph generation, lesson extraction). Desktop app optional for visualization.
- Code Analysis: lat.md only (pre-indexed graph, MCP tools, incremental sync)
- Post-Feature: Lessons are NOT optional; /spek.conclude automates extraction

MD5 Hashes (scanned files; use for cache-hit detection)

- README.md: 9015905bb36664f75d994fc85247cddb
- architecture.md: c7c318198c90ddb84e00ca62ecf9287e
- conventions.md: 54533079f8530ca6099f2be292afd3b5
- decision.md: adfb1f1d0a258660c367368585d3494e
- patterns.md: af1e65f33a78e0aaea6341e805de255b
- setup.md: 3865eaec7ee6f98b3c948ee3bfd10359
- skills.md: e467f28d4852f26688797238c6743dc0
- speckit.md: [not found in current scan]
- vision.md: c3593ea9d60e9d03f159241c306ab40a
- workflow.md: 7910becfa0ce2ee12d42683ca173e123

Notes & Observations

- **Recent Changes (2026-06-07):** All wiki files updated; README restructured to emphasize init-first model, decision tree, and working assumptions. Skills.md expanded with full command reference. Architecture.md clarifies programmatic pipeline vs agentic path.
- **Canonical vs Exploratory:** Programmatic pipeline (package-based, deterministic, CI-friendly) is production default. Agentic AGENTS.md path supported for discovery/small vaults only.
- **Critical Requirement:** Obsidian CLI (not desktop app) is mandatory for /spek.conclude automation. Desktop app is optional visualization layer.
- **Cache Key:** Use hashes above for future change detection. Recompute at next /cel.wiki.read call.
- **Status:** Spekificity complete when all specs in /wiki/specs/ are implemented. No MVP—tool defined entirely by wiki documentation.

Persistence

- Context persisted at: .cel/context.md (this file)
- Use stored hashes for change-detection on subsequent runs
- Forced refresh: /cel.wiki.read refresh (skips hash check, full rescan)

End of brief.
