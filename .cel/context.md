---
last_deep_read: 2026-05-20T18:00:00Z
version: 5.1
scan_status: full
changes_detected: multiple files updated since last scan; full rescan performed; 21 file hashes changed
tracked_files: 57
tracked_wiki_files: 56
---

# spekificity technical brief

## project purpose

Spekificity = agentic consolidation platform solving four recurring LLM agent failures:

| problem | mechanism |
|---|---|
| token bloat | code graph queries + aggressive compression instead of file scans |
| shallow planning | canonical SpecKit workflow `spec → plan → tasks → implement` enforced |
| context loss | persistent markdown vault for decisions, patterns, lessons across sessions |
| low autonomy | reusable project memory + graph-grounded context injection; agent works independently |

Core promise: from code + docs → feature idea → spec → implementation → lessons, all with AI agent as copilot, all tracked in vault, minimal token waste, minimal tool-switching.

Repository is **design-first, not shipped product**. Contains architectural specs, implementation contracts, setup guides. CLI and skill bundle planned for future release.

---

## architecture and tech stack

### core stack

- **SpecKit/Specify**: spec-driven workflow engine (global install, unmodified)
- **Spekificity layer**: enrichment wrappers around SpecKit commands (decorator pattern)
- **Code Graph**: preferred backend for code intelligence (SQLite + MCP tools)
- **Obsidian vault**: markdown knowledge store for decisions, patterns, lessons
- **Caveman**: compression mode for token efficiency at each stage
- **CLI**: planned `spek` command surface for setup, context load, automation, post-processing

### architecture model

Two-system pattern repeated:

1. **Knowledge vault** (slow-moving): human-readable, durable context
2. **Code graph** (fast-moving): machine-oriented, indexed code intelligence

Key design principles:

- Decorate, not fork, upstream tools
- Keep components independently updateable
- Prefer markdown + AI-executable guides over custom binaries
- Token efficiency first-class, not cleanup
- Global tool installs separate from per-project skills

---

## key workflows

### one-time setup

```
spekificity init
  → detect installed tools (speckit, code mapper, vault system, compression, git)
  → install missing + prompt on options
  → deploy skills locally
  → initialize vault structure
  → initialize code analysis
  → confirm setup + verify integrations
```

### enriched feature lifecycle (canonical flow)

```
/spek.context          (load vault + graph)
  ↓
/speckit.specify       (enriched with decisions + patterns)
  ↓
/speckit.clarify       (optional; resolve gaps before plan)
  ↓
/speckit.plan          (enriched with graph context + impact analysis)
  ↓
/speckit.tasks         (generate dependency-ordered tasks)
  ↓
/speckit.analyze       (optional; cross-artifact consistency check)
  ↓
[manual remediation if needed]
  ↓
/speckit.implement     (with spec/plan/task context available)
  ↓
/spek.lessons          (write structured lessons; compress with caveman)
  ↓
/spek.post             (update vault, refresh graph, consolidate docs)
```

### persistent memory model

Multi-layer memory:

- **vault memory**: authoritative project knowledge (survives sessions)
- **repo memory**: compressed project context for repository (`.cel/context.md`)
- **session memory**: ephemeral feature/session state (cleared between features)

Lessons self-contained so future sessions don't need full artifact re-reads.

### token-efficiency strategy

- Graph queries replace file scans for code context queries
- Context loaded once per session (not repeatedly)
- Caveman compression available at key stages
- Incremental graph refresh (not full rebuild)

---

---

## documentation map

### entry + orientation

- `README.md`: pitch, four pillars, prerequisites, command entry points, quick start
- `wiki/intention.md`: vision, philosophy, lifecycle framing
- `wiki/architecture.md`: component roles, design principles, CLI structure, workflow state
- `wiki/decision.md`: architectural choices (e.g., CodeGraph vs Graphify, tool decisions)

### workflow + conventions

- `wiki/speckit-workflow.md`: canonical SpecKit lifecycle, command descriptions, re-entry points
- `wiki/naming-conventions.md`: namespace + command naming rules
- `wiki/todo.md`: progress tracker, completed items, investigation summaries

### knowledge + research

- `wiki/llm-wiki.md`: LLM wiki concept, tool ecosystem, confusion resolution
- `wiki/research.md`: rationale synthesis, comparisons

### setup guides

- `wiki/setup/speckit-setup.md`: SpecKit install + verification
- `wiki/setup/obsidian-setup.md`: vault setup + usage expectations
- `wiki/setup/graphify-setup.md`: code graph setup + integration

### specification library

`wiki/specs/`: implementation contracts covering:

- Memory + context loading (context-load-lifecycle, session-memory, persistent-memories-and-lessons)
- Enrichment wrappers (specify-enrichment, plan-enrichment, implement-enrichment)
- Graph schema + operations (node-schema-design, graph-storage-structure, graph-refresh-strategy, graph-query-patterns)
- CLI + orchestration (cli-orchestration, spek-automate-workflow, prepare-command, post-command)
- Error handling + reflection (error-handling-and-recovery, rarv-reflection, anti-sycophancy, blind-code-review)
- Lessons + patterns (lessons-format, patterns-library, zettelkasten-conventions)
- Integration testing (integration-validation-and-testing)

---

## current project state

Repository active design + implementation-planning surface. Architectural spec broad + mature.

Recent investigation (completed 2026-05-18):

- **B.1**: Canonical SpecKit flow documented → full lifecycle with post-remediation mechanics
- **B.2**: `spek.prepare` + `spek.post` fully defined → context loading, caveman activation, lessons compression

Next themes from docs:

1. Implement agent skills for all workflow stages
2. Complete CLI orchestration + dispatch
3. Validate end-to-end integration
4. Tighten + consolidate documentation

---

## scan scope

**Scanned:**

- Root `README.md`
- Top-level authored docs in `wiki/` (not `wiki/raw/`)
- Setup guides in `wiki/setup/`
- Implementation specs in `wiki/specs/`
- Workflow + todo docs

**Excluded:**

- `.cel/`, `.github/`, `.specify/`, `wiki/raw/`
- External/vendor/archive/backup content
- Non-markdown source files

---

## hash inventory

Hashes below drive cache validation for future `/cel.wiki.read` runs. Regenerate with rescan.

| file | md5 |
|---|---|
| README.md | c4dbe5a2900e16eb599358dfa513fc19 |
| wiki/architecture.md | c63af49f6601e15b8349a923437bb4e9 |
| wiki/decision.md | d69614e12d5498596fc1c4fa88afdb5a |
| wiki/intention.md | e8d85b2f8eb112fd90c5a3c7eebd1aeb |
| wiki/llm-wiki.md | 985cb6d43e1f405449440625fbe1ed06 |
| wiki/naming-conventions.md | 940b1554ecdc7a901e43a7c98f5f3e1e |
| wiki/research.md | 58327bde008a6639c0092d15a6a1adbc |
| wiki/setup/graphify-setup.md | 7a70832c1de2db617250ab50ffbd4049 |
| wiki/setup/obsidian-setup.md | 3b0b4f62584b234d6ab542ff94d7065a |
| wiki/setup/speckit-setup.md | 8b35437502229326f1d78c80d09b24a9 |
| wiki/speckit-workflow.md | 61af19534e047afa35fa72c7ac0726dc |
| wiki/specs/3layer-query-rule.md | d7dd233f8113a49440e6652e233d6ec4 |
| wiki/specs/anti-sycophancy.md | ee9e4b7f49538ed8f2e5b89204e4f3a1 |
| wiki/specs/architectural-decisions.md | 675c9d4814ddb17a883fa4380224e38a |
| wiki/specs/auto-tagging-wikilinks.md | 2e7dd4543fcabfd054ba72c7c94cbab9 |
| wiki/specs/backprop-reflex.md | 215905227849b4b8f160473ccf95971c |
| wiki/specs/blind-code-review.md | 8bfe9109dd8d9b458624e713c4cd18b6 |
| wiki/specs/caveman-integration.md | 416ea05d9cd687128cc3774579e4d900 |
| wiki/specs/claude-code-memory-setup-analysis.md | 44314cc1c17f03d9fe0936cc57995bf2 |
| wiki/specs/cli-orchestration.md | fbe1ecb1c68c5e38d87ffbbd0de8fdc7 |
| wiki/specs/code-and-document-maps.md | 2410083e24d035def86a9aa7c9c9b07b |
| wiki/specs/codegraph-setup-and-integration.md | 70643b11c52aeb5be0581416b58c68a0 |
| wiki/specs/context-layer.md | 726ef5465a3f9e1c390388c95885a5bf |
| wiki/specs/context-load-lifecycle.md | 35c4ad9e40ac10835980cf03e45f075f |
| wiki/specs/decorator-wrapper-pattern.md | 03b0fb60d4b837a795e45bb98675d86a |
| wiki/specs/error-handling-and-recovery.md | 93203ce6a6f45c88b0ef6cfa20012320 |
| wiki/specs/feature-state-tracking.md | d78be9329a6ae4ada23b5d96ae5908cd |
| wiki/specs/git-verification.md | 89b788d8c8e807f3c8edbf923cef0f01 |
| wiki/specs/graph-merge-integration.md | 3cde3354f848b233bdc678b9e689c0f8 |
| wiki/specs/graph-query-patterns.md | 80d94190e08bc2555d28c461026e9b74 |
| wiki/specs/graph-refresh-strategy.md | 637eed474434aecc1e645f84b9c3f904 |
| wiki/specs/graph-storage-structure.md | a7df3d2db1d6b5934e29b8332a86b814 |
| wiki/specs/graphify-git-hooks.md | db543e2cbd9cec1e8a132d5d1a0ab7a0 |
| wiki/specs/graphify-installation.md | 0c70fcd123ce187313b623bdbca5f6c7 |
| wiki/specs/implement-enrichment.md | a94a441abb4c51b4ebf6471fe467f05e |
| wiki/specs/integration-validation-and-testing.md | 90e5b185002621883c699764c3c677f |
| wiki/specs/lessons-format.md | 47c4bf7d1c5301f8f458dee09d687c4c |
| wiki/specs/node-schema-design.md | b5b8f0684322b0fddad46fe3b463a14a |
| wiki/specs/obsidian-graph-export.md | fe2cdaa83def9de2abb32eb04208a9e1 |
| wiki/specs/patterns-library.md | e177794a22c67d614c29e7ebc5dc94c6 |
| wiki/specs/persistent-memories-and-lessons.md | b5f3e5e9aff60ab56420daeec95de62f |
| wiki/specs/plan-enrichment.md | fa9a4825e2b9ab2ae9c49652437a7b46 |
| wiki/specs/post-command.md | 124835e44f5a9dffe8b5a7684e6f2368 |
| wiki/specs/post-processing.md | 1ff4bd1e137fb7fed892474f199e27f8 |
| wiki/specs/prepare-and-post-skills.md | 3616c3c8bb8b91d9e828afa3913be3b1 |
| wiki/specs/prepare-command.md | dfb38fa4203e587af948c8b600a5119f |
| wiki/specs/rarv-reflection.md | 516a7e0f237ddf11cce90a54edd4559a |
| wiki/specs/sdd-framework-comparison-analysis.md | 4b3ed030afed8ecea956cd82c713d662 |
| wiki/specs/session-logs-vault-artifacts.md | c1a348cc04040ea7d83762ac8b7073a2 |
| wiki/specs/session-memory.md | bb3b7af053ddbb7417423cc0b5626993 |
| wiki/specs/specify-enrichment.md | 7f57618ad9eb1f14940521919c9a097e |
| wiki/specs/speckit-integration-contract.md | 00543d21c9ba1446bb1edd80ba07fab7 |
| wiki/specs/spek-automate-workflow.md | 4250ec498372d8cf5f21813d21c96989 |
| wiki/specs/spek-map-command.md | c1e1dc08795d02fc08ad7b6cfb74d5b4 |
| wiki/specs/token-budget.md | 8d7f123e3a01abcbbd0bb035e736f79e |
| wiki/specs/zettelkasten-conventions.md | 92da1eda8711d724951da085db4aa5e1 |
| wiki/todo.md | 7a89e70b4c34f4b5bd47c111fc98afec |
