---
last_deep_read: 2026-05-18t00:00:00z
version: 2.6
scan_status: full
changes_detected: four pillars (token efficiency, determinism, persistence, autonomy) now explicit in README, intention.md, architecture.md; mapping added
---

# spekificity technical brief

## executive summary

**spekificity** = agentic consolidation platform. solves four foundational LLM agent problems by wiring best-in-class tools:

1. **Token Efficiency and Verbosity** — graph queries replace file scans (92% savings); compression removes fluff (60%)
2. **Planning and Determinism** — canonical workflow (spec → plan → tasks → implement); ground truth context from code graph
3. **Memory Persistence** — vault stores decisions, lessons, patterns; survives session boundaries
4. **Autonomy** — agent operates independently; code questions answered without dev hand-holding

**does NOT reimplement tools** — orchestrates existing best-in-class tools (code analysis, spec-driven framework, knowledge vault, compression) into coherent workflow. delivered as markdown skills + workflows that AI agents read and execute directly.

---

## problem space (mapped to four pillars)

| pillar | problem | spekificity solution |
|--------|---------|---------------------|
| **token efficiency** | agents read all files recursively; verbose outputs waste tokens | graph-based context (92% reduction); compression at each stage (60%) |
| **determinism** | ad-hoc agent planning; hallucinated context; inconsistent results | spec-driven framework enforces canonical steps; code graph provides ground truth |
| **persistence** | context lost at session end; no accumulated knowledge | obsidian vault stores decisions, lessons, patterns; `/context-load` restores all context at start |
| **autonomy** | agents need constant dev hand-holding; clarifications burn tokens | graph answers code questions directly; vault recalls patterns; deterministic workflow reduces ambiguity |

---

## target users & journeys

**user personas**:
- solo developer: values speed + cognitive load reduction
- team lead/architect: needs consistent toolchain + easy onboarding
- ai power user: wants maximum roi from every token

**core journeys**:
1. **init**: `spekificity init` → auto-detect tools, install missing, deploy skills (~10 min)
2. **map**: `/map-codebase` → graphify generates graph → stored in obsidian vault
3. **feature**: `/context-load` → `/speckit-enrich-specify` → `/speckit-enrich-plan` → `/speckit.tasks` → `/speckit-enrich-implement` → lessons logged
4. **update**: update single tool (graphify/obsidian/speckit/caveman) independently without re-init

---

## architecture & tech stack

**core components**:
- **speckit/specify** (global install): spec-first CLI; spekificity wraps via decorator pattern
- **code analysis tool** (recommended: CodeGraph): AST-indexed graph, MCP tools, auto-sync via file watcher. 92% fewer agent token calls vs file scanning. NOT Graphify (graphify deprecated for agent use — outputs markdown files requiring token-expensive reads)
- **knowledge vault** (Obsidian format): plain markdown, git-backed, optional app. stores specs, decisions, lessons, raw materials. accessed once per session via `/context-load`
- **caveman skill**: response compression. invoked at workflow steps for token efficiency
- **AI agents**: GitHub Copilot + Claude Code (first-class)

**philosophy: consolidation not reinvention**:
- does NOT reimplement spec frameworks, code mappers, knowledge systems, compression, or AI infra
- DOES: identify best tools, orchestrate install, wire into workflow, automate handoffs, inject context, capture lessons, maintain project memory

**delivery**: all skills/workflows = `.md` files only. no binaries. AI agents read + execute directly.

**CLI layer** (`.spekificity/bin/`):
- `bin/spek` — globally-installable entry point; dispatches to per-project scripts
- `_lib.sh` — shared utilities (config, atomic JSON writes, graph state: fresh/stale/absent)
- `prepare.sh` — checks graph staleness, rebuilds if needed, hands off to `/spek.prepare` skill
- `automate.sh` — preflight (clean tree), creates feature branch, writes `workflow-state.json`, hands off to `/spek.automate`
- `post.sh` — reads `workflow-state.json`, surfaces `--no-lessons`/`--no-graph` flags to skill

**workflow-state.json schema**:
```json
{
  "status": "in-progress | halted | complete",
  "current_step": "<step>",
  "next_step": "<step>",
  "completed_steps": ["preflight", "spec", "..."],
  "preflight": { "branch_created": true, "clean_working_tree": true },
  "postflight": { "lessons_written": false, "graph_refreshed": false, "pr_created": false, "pr_url": null }
}
```

**dual-system design** (key architectural decision):
| system | purpose | content | rhythm |
|--------|---------|---------|--------|
| knowledge vault | persistent knowledge | specs, decisions, lessons, raw | once per feature cycle |
| code analysis tool | code intelligence | symbols, calls, routes, deps | every file save (auto-sync) |

**directory structure** (project-scoped):
```
spekificity/
├── wiki/                ← project wiki (architecture, decisions, intention, todo, setup, llm-wiki)
├── .spekificity/        ← bin scripts, config, guides
├── .specify/            ← speckit config (constitution, templates, extensions)
└── .github/agents/      ← agent skill routing
```

---

## enriched feature lifecycle (3 stages)

**stage 0 — init** (`spekificity init` or `spek automate`):
- auto-detect tools, install missing, deploy skills locally
- init knowledge vault structure + code analysis
- creates `workflow-state.json` + feature branch

**stage 1 — ingest**:
- dev drops raw files to `vault/raw/`
- code analysis tool indexes source → vault graph
- knowledge system processes raw docs via LLM
- trigger: manual `/map-codebase` or auto on `/context-load`

**stage 2 — spec/implement loop**:
```
/context-load → load vault (code map + recent lessons)
/enrich-specify → inject context (related symbols, prior decisions) → spec.md
/enrich-plan → inject impact analysis → plan.md
/generate-tasks → dependency-ordered tasks.md
/enrich-implement → execute with code map + spec + plan in scope
```

**stage 3 — refine**:
- `/lessons-learnt` → structured entry to `vault/lessons/<date>-<feature>.md`
- graph auto-updates (incremental)
- next feature starts with richer context

**decorator pattern**: all enrich-* skills wrap vanilla speckit. speckit untouched, independently upgradable.

---

## token efficiency strategy

**mechanisms**:
1. **graph-based context**: query dependency map instead of reading all files
2. **caveman compression**: terse notation, no fluff, full technical content
3. **persistent memory**: load lessons/decisions at start, not re-explained
4. **incremental mapping**: update only changed nodes, not full regeneration

**invocation**: `/caveman lite` (for spec/plan work) or `/caveman` (for implementation)

---

## functional requirements (core)

| id | requirement | status |
|----|-------------|--------|
| fr-001 | init installs/links graphify, obsidian, speckit/specify | core |
| fr-002 | init deploys spekificity custom skills locally (idempotent) | core |
| fr-003 | mapping skill runs graphify + stores output as obsidian vault | core |
| fr-004 | mapping skill supports incremental refresh | core |
| fr-005 | all speckit-extension skills use decorator pattern | core |
| fr-006 | lessons-learnt entries structured, versioned, vault-stored | core |
| fr-007 | caveman skill integrated + invokable at any workflow step | core |
| fr-008 | each component independently updatable (no re-init required) | core |
| fr-009 | support github copilot + claude code as first-class agents | core |
| fr-010 | non-automatable setup steps documented as ai-executable guides | core |

---

## pending todos (wiki/todo.md)

**completed (moved to llm-wiki.md)**:
- A.1 Review all documents in 'wiki/raw/llm wiki' and compile vision → Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Vision & Philosophy section
- A.2 Review all documents in wiki/raw and compile confusion → Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Confusion Resolution section
- A.3 List all tools and document toolsets → Consolidated into [wiki/llm-wiki.md](wiki/llm-wiki.md) — Tool Ecosystem section

**open**:
- **B.1** — clarify full speckit canonical flow (specify → plan → tasks → analyze → remediate → implement → ???). does remediation happen in-place or via re-run? are there re-entry points? does implement expect clean analyze pass? critical for `spek automate` sequencing.
- **B.2** — expand `spek prepare` (explicit caveman activation, confirm codegraph fresh, load vault decisions+patterns+lessons) and `spek post` (caveman compress, incremental codegraph after lessons written, update vault decisions/patterns). document caveman activation in both skills.
- **B.3** — `spek post` lessons-learnt must be self-contained: feature digest (from spec.md), key implementation steps (from tasks.md), decisions made, patterns reused. goal: future sessions skip reading spec.md/tasks.md entirely. update spek.post skill definition.
- **B.4** — add `cel.docs.simplify` step to `spek post` after lessons + graph refresh. clarify: full directory or scoped to modified files in current branch? prefer scoped.
- **B.7** — commit to `spek.` namespace for all spekificity platform skills. decide flat vs nested (`spek.*` vs `spek.workflow.*`). document decision.
- **B.8** — high-level concepts: code + document maps (B.8.1), persistent memories + lessons (B.8.2).

---

## key decisions (wiki/decision.md)

**Decision 1: CodeGraph over Graphify** (accepted):
- Graphify: outputs markdown vault files → agent must read files → 100s tokens per query
- CodeGraph: SQLite graph + MCP tools → instant queries → 92% fewer tokens, 77% faster
- Agent queries code frequently (every cycle); vault queries once per session → separate rhythms justify separate tools
- Trade-off: no human-browsable vault of code structure (accepted — vault is for knowledge, not code)

**Decision 2: Dual-system toolset** (accepted):
- Knowledge Vault (Obsidian) = intent, decisions, lessons. slow rhythm.
- Code Analysis Tool (CodeGraph) = symbols, calls, routes. fast rhythm (file watcher).
- Together: 30-40% faster dev on refactoring/debugging vs. vault alone.

---

## core design principles

1. **decorator pattern**: wrap, never replace. vanilla speckit untouched, independently upgradable.
2. **global speckit, local customization**: speckit installed globally; spekificity skills deployed locally per-project.
3. **modular independence**: each component (graphify, obsidian, speckit, caveman) updatable without full re-init.
4. **ai-executable setup**: where cli automation impractical, setup documented as step-by-step ai-followable guides.
5. **token efficiency by default**: graph-based queries + caveman compression are first-class, not afterthoughts.
6. **markdown-only delivery**: no binaries. all skills/workflows are `.md` files that ai agents read and execute directly.
7. **persistent context across sessions**: obsidian vault stores graph, lessons, decisions; `/context-load` restores at session start.
9 files)

| document | location | purpose |
|----------|----------|---------|
| README.md | `README.md` | entry point, capabilities table, prerequisites, skills list, core problems solved, session start |
| intention.md | `wiki/intention.md` | project vision, philosophy (consolidation not reinvention), 3-stage workflow, tool roles |
| architecture.md | `wiki/architecture.md` | design principles, component roles, CLI scripts, workflow-state.json, component isolation |
| decision.md | `wiki/decision.md` | CodeGraph vs Graphify, dual-system architecture, tool recommendations |
| llm-wiki.md | `wiki/llm-wiki.md` | LLM Wiki framework, vision, principles, implementation schema, operations, tool ecosystem (consolidated from raw/) |
| todo.md | `wiki/todo.md` | open action items (B.1-B.8.2) + completed items (A.1-A.3) with pointers to llm-wiki.md |
| obsidian-setup.md | `wiki/setup/obsidian-setup.md` | vault install, optional app, vault structure, gitignore |
| speckit-setup.md | `wiki/setup/speckit-setup.md` | speckit global install, `specify init`, verification |

---

## non-goals (v1)

- reimplementing spec frameworks, code mappers, knowledge systems, compression, or AI infra
- gui or web interface
- support for AI agents beyond Copilot + Claude Code
- cloud sync or multi-user vault sharing
- automatic merge conflict resolution with speckit upstream updates

**v1 scope**: all speckit steps enriched when map available; independent component updates; macOS + Linux support; fully local operation

---

## wiki organization (cel.wiki.init) - 2026-05-12

**status**: ✓ completed. 46 md files organized into structured wiki/ at project root.

**structure created**:
```
wiki/
├── docs/         (5 files, 35KB)    - guide, architecture, faq, glossary, validation
├── setup/        (3 files, 10KB)    - graphify-setup, obsidian-setup, speckit-setup
├── skills/       (4 files, 45KB)    - context-load/skill, lessons-learnt/skill, map-codebase/skill, speckit-enrich/*
├── specs/        (29 files, 262KB)  - specs/001,002,003 (spec.md, plan.md, tasks.md, contracts, acceptance-tests)
├── vault/        (2 files, 12KB)    - decisions.md, patterns.md
├── workflows/    (4 files, 28KB)    - component-update, feature-lifecycle, init-workflow, map-refresh
├── TODO.md       (13KB)             - project todo list
└── raw/          (empty)            - reserved for static assets (PDFs, transcripts, exports)
```

**files moved**: 46 md files from scattered doc locations → wiki/ flat then sorted into subdirs  
**original dirs removed**: docs/, setup-guides/, workflows/ (now empty, cleaned)  
**readme.md preserved**: yes, remains at project root  
**static assets**: 0 moved (none found)  

**next**: run `/cel.wiki.read` to refresh with content analysis, then `/cel.wiki.simplify` to audit redundancies.

---


## known dependencies

- python 3.11+, `uv` package manager
- speckit: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (global)
- graphify: `uv tool install graphifyy` (legacy; CodeGraph preferred for agents)
- CodeGraph: MCP server + sqlite graph (recommended code analysis tool)
- GitHub Copilot or Claude Code for AI agent
- Obsidian (optional desktop app; vault is plain markdown)
- git + terminal

---

## entry points for agent interaction

```
/context-load          # session start — always
/map-codebase          # codebase refresh
/enrich-specify        # spec with context
/enrich-plan           # plan with impact analysis
/generate-tasks        # dependency-ordered tasks
/enrich-implement      # execute with graph context
/lessons-learnt        # capture outcomes to vault
/caveman               # token compression (any step)
```

---

**status**: active development. CodeGraph transition underway. wiki updated. open todos: B.1-B.8.2.

---

## hash inventory (scanned 2026-05-18)

| file | hash | status |
|------|------|--------|
| README.md | 79fdb36dcce7f0a31f5be49272f37124 | ✓ updated (four pillars added) |
| wiki/architecture.md | bbf522e363e2184e9db4b89a328c1f21 | ✓ updated (four pillars mapping + design principles) |
| wiki/decision.md | 7c214da1db5367cbb20f52d6df2956a1 | ✓ unchanged |
| wiki/intention.md | b0ded9879d2ccb2a21c2272bf66a4c43 | ✓ updated (four pillars vision + workflow stage mapping) |
| wiki/llm-wiki.md | 985cb6d43e1f405449440625fbe1ed06 | ✓ unchanged |
| wiki/todo.md | 628abfc0f6982f57a8a8355b7c7ea0be | ✓ unchanged |
| wiki/setup/obsidian-setup.md | 3b0b4f62584b234d6ab542ff94d7065a | ✓ unchanged |
| wiki/setup/speckit-setup.md | 8b35437502229326f1d78c80d09b24a9 | ✓ unchanged |

**total files**: 8 files scanned (7 wiki + README). **net change**: 3 updated (README, architecture.md, intention.md), 5 unchanged.
