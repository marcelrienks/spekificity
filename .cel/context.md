Technical Brief: Spekificity — Wiki Context

Last Deep Read: 2026-06-06 (UTC)

Project Purpose

- Spekificity: spec-driven agent development framework combining a Git-backed markdown vault, pre-indexed code graph (lat.md), deterministic spec engine (SpecKit), and composable agent skills to enable token-efficient, repeatable, auditable feature work.

Architecture & Tech Stack (concise)

- Code index: lat.md (canonical). MCP tools: lat_symbols, lat_references, lat_callers, lat_impact, lat_definition, lat_query. Incremental sync, optional file-watcher + git hook for freshness.
- Spec engine: SpecKit (spec → plan → tasks → implement). Spekificity orchestrates SpecKit via /spek.plan and /spek.implement wrappers.
- Persistent vault: Git-backed Obsidian-style markdown vault (vault/). Zettelkasten conventions, YAML frontmatter, git-backed. Obsidian app optional; CLI required for automated vault operations.
- Compression: Caveman modes (lite|full|ultra) for token budgets.
- Retrieval default: BM25 lexical for wiki-scale; hybrid/vector optional for large stable KBs.
- Programmatic pipeline (canonical direction): deterministic package/pipeline outputs, typed contracts, content-addressable IDs, markdown-hero structural enforcement, CI-friendly ingestion.
- Supporting tools: markdown-hero (structural hygiene), lat.md (code intelligence), Obsidian CLI (vault automation), AGENTS.md (agent-agnostic runtime policy).

Key Workflows (high level)

- Feature cycle: /spek.prepare → /spek.plan (--phase=specify → --phase=plan) → /spek.implement → /spek.conclude (lessons). Optional: /spek.context, /spek.map, /spek.lessons --deep.
- Spec enrichment: each spec includes Success Criteria, Assumptions, Risk Assessment, Dependencies, Resource Estimate.
- 3-layer query rule: Layer 1 (lat.md index, low-cost) → Layer 2 (vault/decisions/patterns, moderate-cost) → Layer 3 (raw code files, high-cost). Always prefer lower-cost layers first.
- Post-processing: automated lesson extraction, caveman compression, auto-tagging + auto-wikilinks during /spek.conclude (with human review gates).
- Safety: plan-before-execute gating; allowlists for destructive tooling; pre-merge structural linting.

Documentation Map (where to look)

- wiki/architecture.md — canonical architecture, programmatic pipeline choice, retrieval guidance, HTML artifact policy.
- wiki/vision.md — vision, pillars, and tenets.
- wiki/workflow.md — deterministic feature workflow, entry/exit criteria, artifacts.
- wiki/conventions.md — command naming, file naming, markdown structural hygiene, pre-merge checklist.
- wiki/decision.md — recorded architecture & tool decisions (lat.md, SpecKit, Obsidian, caveman, zettelkasten conventions).
- wiki/patterns.md — pattern library and cross-reference map (enrichment patterns, memory, query, error handling, validation, graph patterns).
- wiki/speckit.md — mapping of SpecKit flow and Spekificity orchestration.
- wiki/setup.md — installation and verification steps for SpecKit, vault, Obsidian CLI, and lat.md.
- wiki/skills.md — agent/skill surface and usage notes.
- wiki/tutorial.md — walkthrough and hands-on workflow example.
- README.md — repository-level summary and quickstart pointers.

MD5 Hashes (scanned files)

- architecture.md: daa260c1424cf13d6c509f37ab6f88a9
- conventions.md: 39cfb4c55fb5ee747273113ba0991e6d
- decision.md: f6e3665a31cd7efc4a0cac97c929d82e
- patterns.md: 6d287b10206ca175bf06d25ae4bc6394
- setup.md: 39234da4678c206abaa9946d9fdc7473
- skills.md: 5b6e20a93d23a4abe1d3eb0d0831f4c4
- speckit.md: 35fc01d830f28dcefc785766cb305031
- tutorial.md: 37111f60b428b741201e45fdd4bb2c23
- vision.md: b69c9b7b1214ce841c9c23466505faf4
- workflow.md: a5a4f972d218ed4780ed619e1208b3ec
- README.md: 52a31c42d8f0bdeb7b1140a987f28824

Notes & Observations (brief)

- Canonical direction: Programmatic pipeline chosen as default for production/reproducible runs. Agentic/AGENTS.md path kept as experimental/exploratory for small vaults only.
- Structural hygiene is required: no duplicate H1s, valid YAML frontmatter, parseable tables, section-aware chunking — markdown-hero recommended.
- Obsidian CLI required: primary integration for vault automation (syncs, exports, metadata extraction). Desktop app optional for visualization.
- Cache note: .cel/context.md contains file hashes used for future cache-hit checks. Use `/cel.wiki.read refresh` to force a full re-scan.
- Recent changes: architecture.md, setup.md, vision.md updated. tutorial.md added. llm-wiki.md and goal.md removed/consolidated.

Persistence

- Context persisted at: .cel/context.md (this file)
- Use the stored hashes above for change-detection on subsequent runs.

End of brief.
