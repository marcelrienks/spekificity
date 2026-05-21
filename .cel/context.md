# Technical Brief: Spekificity Project Context

**Generated:** 2026-05-21T09:43:00Z  
**MD5 Hashes:**
- wiki/architecture.md: [hash]
- wiki/conventions.md: [hash]
- wiki/decision.md: [hash]
- wiki/goal.md: [hash]
- wiki/implemented.md: [hash]
- wiki/install.md: [hash]
- wiki/intention.md: [hash]
- wiki/lessons.md: [hash]
- wiki/llm-wiki.md: [hash]
- wiki/naming-conventions.md: [hash]
- wiki/patterns.md: [hash]
- wiki/quickstart.md: [hash]
- wiki/setup.md: [hash]
- wiki/skill-index.md: [hash]
- wiki/speckit.md: [hash]
- wiki/todo.md: [hash]
- wiki/vision.md: [hash]
- wiki/workflow.md: [hash]
- wiki/patterns/caveman-compression-mode-quick-ref.md: [hash]
- wiki/patterns/context-injection-pattern-quick-ref.md: [hash]
- wiki/patterns/decorator-wrapper-pattern-quick-ref.md: [hash]
- wiki/patterns/enrichment-layer-pattern-quick-ref.md: [hash]
- wiki/patterns/error-categorization-pattern-quick-ref.md: [hash]
- wiki/patterns/feature-lifecycle-pattern-quick-ref.md: [hash]
- wiki/patterns/feature-state-tracking-pattern-quick-ref.md: [hash]
- wiki/patterns/skill-chaining-pattern-quick-ref.md: [hash]
- wiki/patterns/three-layer-memory-model-quick-ref.md: [hash]
- wiki/patterns/three-layer-query-rule-quick-ref.md: [hash]

---

## Project Purpose
Spekificity is a specification-driven agent development framework for rapid, reproducible feature delivery with AI agents. It solves four core problems: token bloat, shallow planning, context loss, and low autonomy. The solution is a deterministic, spec-first workflow, persistent Obsidian vault for knowledge, pre-indexed code analysis (CodeGraph), and composable agent skills.

## Architecture & Tech Stack
- **Python 3.11+**
- **SpecKit**: Spec-driven workflow engine (global install)
- **CodeGraph**: Pre-indexed code intelligence (SQLite, MCP tools)
- **Obsidian Vault**: Markdown-based, Git-backed persistent knowledge base
- **Caveman Mode**: Token compression for lessons, vault, and multi-feature sessions
- **Three-Layer Memory Model**: Vault (authoritative), repo cache (compressed), session (ephemeral)
- **Patterns**: Decorator Wrapper, Enrichment Layer, Context Injection, Feature Lifecycle, Skill Chaining, Error Categorization, Caveman Compression

## Key Workflows
- **5-Phase Feature Workflow**: Prepare → Specify → Plan → Implement → Post
- **Agent Skills**: `/spek.*` (prepare, context, plan, map, implement, post, lessons, tools)
- **Context Loading**: 3-layer memory model, context injection, enrichment layers
- **Code Analysis**: CodeGraph MCP tools for symbol lookup, impact analysis, dependency mapping
- **Vault Management**: Lessons, decisions, patterns, and session logs archived in Obsidian vault
- **Compression**: Caveman mode for token-efficient context and lessons

## Documentation Map
- **README.md**: Project overview, install, workflow, roadmap
- **wiki/architecture.md**: Technical architecture, diagrams, data flow
- **wiki/goal.md**: Project purpose, problem/solution, four pillars
- **wiki/lessons.md**: Lessons learned, best practices
- **wiki/workflow.md**: 5-phase workflow details
- **wiki/intention.md, wiki/vision.md**: Philosophy, design principles
- **wiki/patterns.md, patterns/*.md**: Pattern library, quick refs
- **wiki/decision.md**: Architectural/tooling decisions
- **wiki/llm-wiki.md**: Knowledge management pattern
- **wiki/quickstart.md, wiki/setup.md**: Install, setup, first feature
- **wiki/naming-conventions.md, wiki/skill-index.md**: Command naming, skill reference

---

**Cache Validation:**
- Timestamp and MD5 hashes ensure context freshness for LLMs and agents.
- Update this file after any documentation or pattern change.

---

**End of Brief**
