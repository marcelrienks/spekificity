---
last_deep_read: 2026-05-20T04:57:07Z
version: 5.0
scan_status: full
changes_detected: cache miss; root README changed; hash inventory refreshed for README plus 56 wiki markdown files
tracked_files: 57
tracked_wiki_files: 56
---

# spekificity technical brief

## project purpose

Spekificity is agentic consolidation platform. Goal: solve four recurring LLM agent failures with orchestration, not reinvention.

| problem | response |
|---|---|
| token bloat | code graph queries + compressed responses instead of recursive file reads |
| shallow planning | canonical SpecKit flow `spec -> plan -> tasks -> implement` |
| context loss | persistent vault for decisions, patterns, lessons |
| low autonomy | reusable project memory + graph-grounded context so agent works with less developer steering |

Repository is documentation-first. It defines operating model, command surface, setup, and implementation contracts for future Spekificity runtime rather than shipping finished CLI in this tree.

## architecture and tech stack

### core stack

- SpecKit/Specify: spec-driven workflow engine, installed globally, left unmodified.
- Spekificity wrappers: enrichment layer around SpecKit commands using decorator pattern.
- Obsidian-style vault: markdown knowledge store for decisions, patterns, lessons, research.
- CodeGraph: preferred code intelligence backend for agent queries; SQLite/MCP style indexed graph.
- Caveman: compression mode for token efficiency at each workflow stage.
- CLI shell layer: planned `spek` command surface for setup, context load, workflow automation, and post-processing.

### architecture model

Two-system design repeated across docs:

1. Knowledge vault for slow-moving, human-readable, durable context.
2. Code graph for fast-moving, query-heavy, machine-oriented code intelligence.

Key design principles:

- Decorate, do not fork, upstream tools.
- Keep components independently updateable.
- Prefer markdown contracts and AI-executable guides over custom binaries.
- Make token efficiency first-class, not cleanup work.
- Keep global tool installs separate from per-project skills and config.

## key workflows

### one-time setup

Typical path documented in README and setup guides:

1. `spek setup`
2. `spek init`
3. `spek status`
4. `/context-load` or `/spek.context`
5. start feature flow

### enriched feature lifecycle

Main recurring loop across README, intention, workflow, and spec docs:

1. Load context from vault and validate graph freshness.
2. Run enriched specify command with decisions and patterns in scope.
3. Run enriched plan command with graph-informed impact context.
4. Run vanilla `speckit.tasks` for ordered tasks.
5. Optionally analyze/remediate cross-artifact consistency.
6. Run enriched implement with spec/plan/task context.
7. Write lessons, refresh graph, optionally consolidate docs.

Canonical control flow:

```text
/spek.context
-> /spek.specify
-> /spek.plan
-> /speckit.tasks
-> /speckit.analyze (optional)
-> manual remediation (optional)
-> /spek.implement
-> /spek.lessons
-> /spek.post
```

### persistent memory model

Docs describe multi-layer memory model:

- vault memory: authoritative project knowledge across sessions
- repo memory: compressed project context for current repository
- session memory: ephemeral feature/session state

Lessons are intended to be self-contained so future sessions do not need to reread full feature artifacts.

### token-efficiency strategy

Repeated claims across docs:

- graph queries cut token load versus file scanning
- compression cuts narrative waste further
- context loaded once per session should beat repeated rediscovery
- incremental graph refresh should replace full rebuild where possible

### diagram-derived flow notes

Docs include mermaid/text flow descriptions for:

- full feature lifecycle from context load to lessons/post-processing
- wrapper model where `/spek.*` commands decorate vanilla `speckit.*`
- stage progression from specification to implementation to retained learning

## documentation map

### entry and orientation

- `README.md`: project pitch, four pillars, prerequisites, command entry points, quick start.
- `wiki/intention.md`: project vision, philosophy, lifecycle framing.
- `wiki/architecture.md`: structure, component roles, CLI and state flow.
- `wiki/decision.md`: major architectural choices and trade-offs.

### workflow and conventions

- `wiki/speckit-workflow.md`: canonical SpecKit lifecycle and enrichment insertion points.
- `wiki/naming-conventions.md`: namespace and command naming rules.
- `wiki/todo.md`: progress tracker and implementation roadmap.

### knowledge and research

- `wiki/llm-wiki.md`: LLM wiki concept, persistence model, tool ecosystem.
- `wiki/research.md`: supporting rationale, research synthesis, comparisons.

### setup guides

- `wiki/setup/speckit-setup.md`: SpecKit install and verification.
- `wiki/setup/obsidian-setup.md`: vault setup and usage expectations.
- `wiki/setup/graphify-setup.md`: code graph setup and integration guidance.

### specification library

`wiki/specs/` is current detailed contract surface. Themes covered there:

- memory and context loading
- enrichment wrappers for specify/plan/implement
- graph schema, storage, refresh, git hooks, query rules
- workflow automation, prepare/post orchestration, CLI dispatch
- error handling, anti-sycophancy, blind review, reflection loops, token budget
- lessons formatting, patterns library, zettelkasten conventions
- integration validation and session-log/vault artifact handling

Most current repo intent appears to be moving from architectural specification phase into implementation of skills, CLI orchestration, and end-to-end validation.

## scan scope

Scanned:

- root `README.md`
- top-level authored docs in `wiki/`
- setup guides in `wiki/setup/`
- implementation specs in `wiki/specs/`

Excluded by policy:

- `.cel/`, `.github/`, `.specify/`
- `wiki/raw/`
- non-markdown source files
- external/vendor/archive/backup content if present

## current project state

Repository is active design and implementation-planning surface. Architectural specification is broad and mature. Next work themes called out in docs: implement agent skills, complete CLI orchestration, validate integration end to end, tighten documentation.

## hash inventory

Hashes below drive cache validation for future `/cel.wiki.read` runs.

| file | md5 |
|---|---|
| README.md | 37e6686ea5ea307b6b70495eda83b4dc |
| wiki/architecture.md | bbf522e363e2184e9db4b89a328c1f21 |
| wiki/decision.md | 6629751a38fc52b3144db10c873f2f46 |
| wiki/intention.md | b0ded9879d2ccb2a21c2272bf66a4c43 |
| wiki/llm-wiki.md | 985cb6d43e1f405449440625fbe1ed06 |
| wiki/naming-conventions.md | 4716f752645806d39788b7830f4a4b5f |
| wiki/research.md | e84ccffa6da76180301a181f4613ba06 |
| wiki/setup/graphify-setup.md | 6801d17febc0804d6d4b52f983a2c63d |
| wiki/setup/obsidian-setup.md | 3b0b4f62584b234d6ab542ff94d7065a |
| wiki/setup/speckit-setup.md | 8b35437502229326f1d78c80d09b24a9 |
| wiki/speckit-workflow.md | b8231e96d7047ffcd0c1e1703c10c9fd |
| wiki/specs/3layer-query-rule.md | 1d89b347e3d571e0a976bd1ac3d97544 |
| wiki/specs/anti-sycophancy.md | f1985c4808ac32b6e23b633585813ff3 |
| wiki/specs/architectural-decisions.md | 90639422dd7213db0ba045d8d1f24281 |
| wiki/specs/auto-tagging-wikilinks.md | 2e7dd4543fcabfd054ba72c7c94cbab9 |
| wiki/specs/backprop-reflex.md | bc17370795f9bd0dbca4525c1b592795 |
| wiki/specs/blind-code-review.md | 8bfe9109dd8d9b458624e713c4cd18b6 |
| wiki/specs/caveman-integration.md | 416ea05d9cd687128cc3774579e4d900 |
| wiki/specs/claude-code-memory-setup-analysis.md | f42c3a38d3c3598074c70b088c1f6724 |
| wiki/specs/cli-orchestration.md | 9d19c1f45092884ceb9990e0cb9b9d07 |
| wiki/specs/code-and-document-maps.md | 2410083e24d035def86a9aa7c9c9b07b |
| wiki/specs/codegraph-setup-and-integration.md | 61ce642770344c4e4b7809557b9378f2 |
| wiki/specs/context-layer.md | acca6fc54901f2cf2666775a7cb1e306 |
| wiki/specs/context-load-lifecycle.md | 35c4ad9e40ac10835980cf03e45f075f |
| wiki/specs/decorator-wrapper-pattern.md | 03b0fb60d4b837a795e45bb98675d86a |
| wiki/specs/error-handling-and-recovery.md | 93203ce6a6f45c88b0ef6cfa20012320 |
| wiki/specs/feature-state-tracking.md | 351410009e4ea79fd0c53852d54dae27 |
| wiki/specs/git-verification.md | 89b788d8c8e807f3c8edbf923cef0f01 |
| wiki/specs/graph-merge-integration.md | 3cde3354f848b233bdc678b9e689c0f8 |
| wiki/specs/graph-query-patterns.md | 7e565276d29997f4d2a322d23c773e61 |
| wiki/specs/graph-refresh-strategy.md | 637eed474434aecc1e645f84b9c3f904 |
| wiki/specs/graph-storage-structure.md | a7df3d2db1d6b5934e29b8332a86b814 |
| wiki/specs/graphify-git-hooks.md | db543e2cbd9cec1e8a132d5d1a0ab7a0 |
| wiki/specs/graphify-installation.md | 0c70fcd123ce187313b623bdbca5f6c7 |
| wiki/specs/implement-enrichment.md | a94a441abb4c51b4ebf6471fe467f05e |
| wiki/specs/integration-validation-and-testing.md | 27433a49b51f941a3618ba424b6916e4 |
| wiki/specs/lessons-format.md | 2be382bc47b0c81d4d5bb1f6dc55963c |
| wiki/specs/node-schema-design.md | b5b8f0684322b0fddad46fe3b463a14a |
| wiki/specs/obsidian-graph-export.md | fe2cdaa83def9de2abb32eb04208a9e1 |
| wiki/specs/patterns-library.md | ad3a3ef368fbe3ebdb1f3e1174df374d |
| wiki/specs/persistent-memories-and-lessons.md | b5f3e5e9aff60ab56420daeec95de62f |
| wiki/specs/plan-enrichment.md | 4f9c89b5ecf5453e78d6300d87f08292 |
| wiki/specs/post-command.md | 124835e44f5a9dffe8b5a7684e6f2368 |
| wiki/specs/post-processing.md | 1ff4bd1e137fb7fed892474f199e27f8 |
| wiki/specs/prepare-and-post-skills.md | 7742ecbc52142c82e466bb75d4a9b71b |
| wiki/specs/prepare-command.md | a75d86c3b8a38c90f813029ec8d53fe2 |
| wiki/specs/rarv-reflection.md | b528d63550e406d7c35a8f66596898de |
| wiki/specs/sdd-framework-comparison-analysis.md | 5edd471c8fac5371df6388de638ac0d0 |
| wiki/specs/session-logs-vault-artifacts.md | c1a348cc04040ea7d83762ac8b7073a2 |
| wiki/specs/session-memory.md | 72995a4cec109400aafc12d74ae72803 |
| wiki/specs/specify-enrichment.md | 368563705b7dca5a110e9cd3f9e6285c |
| wiki/specs/speckit-integration-contract.md | 04dcfa0bf63660353915e646d75bcc73 |
| wiki/specs/spek-automate-workflow.md | a2f3630e5afc0b2094ef736fc2615f21 |
| wiki/specs/spek-map-command.md | c1e1dc08795d02fc08ad7b6cfb74d5b4 |
| wiki/specs/token-budget.md | d78f964fc356f22a0c5958bbed681ab0 |
| wiki/specs/zettelkasten-conventions.md | 40066fb5d8330a79416c9e9b976a0872 |
| wiki/todo.md | 010d0de693538bb7a7babae7a08ec52e |
