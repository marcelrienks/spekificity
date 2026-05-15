---
last_deep_read: 2026-05-15t00:00:00z
version: 2.4
scan_status: full
changes_detected: wiki and README updated — 7 files changed, 3 unchanged
---

# spekificity technical brief

## executive summary

**spekificity** = orchestration layer. consolidates best-in-class tools into coherent AI agent workflow. does NOT reimplement tools — wires them together. connects: spec-driven framework (SpecKit), code analysis tool (CodeGraph recommended), knowledge vault (Obsidian), token compression (Caveman). solves persistent context loss, token bloat, shallow feature planning. delivered as markdown skills + workflows that AI agents read and execute.

---

## problem space

| problem | spekificity solution |
|---------|---------------------|
| ai agents lose context between sessions | obsidian vault stores graph, decisions, lessons; `/context-load` restores at session start |
| token bloat from re-reading all files | graphify generates graph once; ai queries graph instead of scanning files |
| speckit specs/plans disconnected from codebase | `/speckit-enrich-specify` and `/speckit-enrich-plan` inject graph context |
| verbose ai responses consume tokens | caveman skill compresses outputs while preserving technical accuracy |

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

## pending todos (wiki/TODO.md)

**completed**: A.1 (vision.md), A.2 (confusion.md), A.3 (toolsets.md)

**open**:
- **B.1** — clarify full speckit canonical flow (specify → plan → tasks → analyze → remediate → implement → ???). critical for `spek automate` sequencing.
- **B.2** — expand `spek prepare` (explicit caveman activation, confirm codegraph fresh, load vault decisions+patterns+lessons) and `spek post` (caveman compress, incremental codegraph after lessons written, update vault decisions/patterns).
- **B.3** — `spek post` lessons-learnt must be self-contained: feature digest (from spec.md), key implementation steps (from tasks.md), decisions made, patterns reused. goal: future sessions skip reading spec.md/tasks.md entirely.
- **B.4** — add `cel.docs.simplify` step to `spek post` after lessons + graph refresh. prefer scoped to modified files in current branch.
- **B.7** — commit to `spek.` namespace for all spekificity platform skills. decide flat vs nested (`spek.*` vs `spek.workflow.*`).
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

---

## documentation map (current wiki/ — 10 files)

| document | location | purpose |
|----------|----------|---------|
| intention.md | `wiki/intention.md` | project vision, philosophy (consolidation not reinvention), 3-stage workflow, tool roles |
| architecture.md | `wiki/architecture.md` | design principles, component roles, CLI scripts, workflow-state.json, component isolation |
| decision.md | `wiki/decision.md` | CodeGraph vs Graphify, dual-system architecture, tool recommendations |
| todo.md | `wiki/todo.md` | open action items (B.1-B.8.2) + completed (A.1-A.3) |
| obsidian-setup.md | `wiki/setup/obsidian-setup.md` | vault install, optional app, vault structure, gitignore |
| speckit-setup.md | `wiki/setup/speckit-setup.md` | speckit global install, `specify init`, verification |
| vision.md | `wiki/llm-wiki/vision.md` | Karpathy LLM wiki approach, consensus on methodology/architecture |
| toolsets.md | `wiki/llm-wiki/toolsets.md` | tools used in LLM wiki pattern + suggested workflows |
| confusion.md | `wiki/llm-wiki/confusion.md` | contradictions + Karpathy validation section |

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

## hash inventory (scanned 2026-05-15)

| file | hash | status |
|------|------|--------|
| README.md | 9a20be75018186970bac69da8bc1425e | ✓ updated |
| wiki/architecture.md | 5a2332bd773f8b9fa3815e41f9b5a9b2 | ✓ updated |
| wiki/decision.md | 7c214da1db5367cbb20f52d6df2956a1 | ✓ updated |
| wiki/intention.md | 936fb0f3e1708abb511f60ebf3f0d5c0 | ✓ updated |
| wiki/todo.md | 853a5d675bdea886fae5b0b15085ebb0 | ✓ unchanged |
| wiki/llm-wiki/confusion.md | ded155c7327b32edd39e1da7906fc668 | ✓ unchanged |
| wiki/llm-wiki/toolsets.md | 991b9863feba59c27e2938f40ba9f5e7 | ✓ updated |
| wiki/llm-wiki/vision.md | 36f122aed50b27d7c4df06322d26cad7 | ✓ unchanged |
| wiki/setup/obsidian-setup.md | 3b0b4f62584b234d6ab542ff94d7065a | ✓ updated |
| wiki/setup/speckit-setup.md | 8b35437502229326f1d78c80d09b24a9 | ✓ updated |

**total files**: 10 files scanned (9 wiki + README). **net change**: 7 files modified, 3 unchanged.
