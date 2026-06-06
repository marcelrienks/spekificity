Technical Brief: Spekificity — Wiki Context

Last Deep Read: 2026-06-06T00:00:00Z (UTC)

Project Purpose

- Spekificity: spec-driven agent development framework that combines a Git-backed markdown vault, a pre-indexed code graph, and a deterministic spec engine to enable token-efficient, repeatable, auditable feature work.

Architecture & Tech Stack (concise)

- Code index: lat.md (canonical). MCP tools: lat_symbols, lat_references, lat_callers, lat_impact, lat_query. Incremental sync, optional file-watcher + git hook for freshness.
- Spec engine: SpecKit (spec → plan → tasks → implement). Spekificity orchestrates SpecKit via /spek.plan and /spek.implement wrappers.
- Persistent vault: Obsidian-style markdown vault (vault/). Zettelkasten conventions, YAML frontmatter, git-backed. Obsidian app optional; CLI used for scripted exports where automation requires it.
- Compression: Caveman modes (lite|full|ultra) for token-budgeted outputs.
- Retrieval default: BM25 lexical for wiki-scale; hybrid/vector optional for large stable KBs or UX needs.
- Programmatic pipeline (chosen canonical direction): deterministic package/pipeline outputs, typed contracts, content-addressable IDs, markdown-hero structural enforcement, CI-friendly ingestion.
- Supporting tools: markdown-hero (structural hygiene), qmd (scalable search optional), AGENTS.md (agent-agnostic runtime policy), CI checks for HTML artifacts (store under wiki/artifacts/html/).

Key Workflows (high level)

- Feature cycle: /spek.prepare → /spek.plan (--phase=specify → --phase=plan) → /spek.implement → /spek.conclude (lessons). Optional: /spek.context, /spek.map, /spek.lessons --deep.
- Spec enrichment: each spec includes Success Criteria, Assumptions, Risk Assessment, Dependencies, Resource Estimate.
- 3-layer query rule: Layer 1 (lat.md index) → Layer 2 (vault / decisions & patterns) → Layer 3 (raw code files). Always prefer lower-cost layers first.
- Post-processing: automated lesson extraction, caveman compression, auto-tagging + auto-wikilinks during /spek.conclude (with human review gates).
- Safety: plan-before-execute gating; allowlists for destructive tooling; pre-merge structural linting.

Documentation Map (where to look)

- wiki/architecture.md — canonical architecture, programmatic pipeline choice, retrieval guidance, HTML artifact policy.
- wiki/vision.md — vision, pillars, and tenets.
- wiki/workflow.md — deterministic feature workflow, entry/exit criteria, artifacts.
- wiki/llm-wiki.md — canonical wiki ingestion pattern and ingestion workflow (plan review gate, frontmatter schema).
- wiki/conventions.md — command naming, file naming, markdown structural hygiene, pre-merge checklist.
- wiki/decision.md — recorded architecture & tool decisions (lat.md, SpecKit, Obsidian, caveman, zettelkasten conventions).
- wiki/patterns.md — pattern library and cross-reference map (enrichment patterns, memory, query, error handling, validation, graph patterns).
- wiki/speckit.md — mapping of SpecKit flow and Spekificity orchestration.
- wiki/setup.md — installation and verification steps for SpecKit, vault, and indexer.
- wiki/skills.md — agent/skill surface and usage notes.
- wiki/goal.md — problem statement and goals.
- README.md — repository-level summary and quickstart pointers.

MD5 Hashes (scanned files)

- decision.md: f6e3665a31cd7efc4a0cac97c929d82e
- llm-wiki.md: 0bcdfb0bbb00e1c5d1439f20cd1d2954
- skills.md: 5b6e20a93d23a4abe1d3eb0d0831f4c4
- vision.md: e840e1ec98827a7047e6007f1a19583f
- patterns.md: 6d287b10206ca175bf06d25ae4bc6394
- workflow.md: a5a4f972d218ed4780ed619e1208b3ec
- goal.md: 5eb3b8bdd75760f9e83c707ded18a7a1
- speckit.md: 35fc01d830f28dcefc785766cb305031
- setup.md: bebe65fb19f361dce1bf0fa7c9f0981b
- conventions.md: 39cfb4c55fb5ee747273113ba0991e6d
- architecture.md: ab4f32c5f3479d2275e7ab1fc74e8673
- README.md: 52a31c42d8f0bdeb7b1140a987f28824

Notes & Observations (brief)

- Canonical direction: Programmatic pipeline chosen as default for production/reproducible runs. Agentic/AGENTS.md path kept as experimental/ exploratory for small vaults only.
- Structural hygiene is required: no duplicate H1s, valid YAML frontmatter, parseable tables, section-aware chunking — markdown-hero recommended.
- HTML artifact policy enforced: store under wiki/artifacts/html/ and require export-to-markdown or canonical 3-line summary linked from a wiki page; CI must flag large HTML artifacts.
- Cache note: .cel/context.md contains file hashes used for future cache-hit checks. Use `/cel.wiki.read refresh` to force a full re-scan.

Persistence

- Context persisted at: .cel/context.md (this file)
- Use the stored hashes above for change-detection on subsequent runs.

End of brief.
