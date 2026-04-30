---
last_deep_read: 2026-04-30T00:00:00Z
version: 1.0
---

# Spekificity Technical Brief

## Project Purpose

**Spekificity** is a meta-tooling layer for AI-assisted development. Produces zero executable code—only markdown skills, workflows, and setup guides. Connects Graphify (codebase mapping), Obsidian (persistent vault), SpecKit/Specify (spec-first CLI), and Caveman skill (compression) into a unified, context-aware, token-efficient workflow.

**Core problems solved**: AI context loss between sessions; token bloat from re-reading codebases; generic SpecKit plans lacking component awareness; verbose AI responses.

---

## Architecture & Tech Stack

**Components** (all interconnected via markdown):
- **Graphify**: Global CLI tool; analyzes source files + docs → produces dependency graph
- **Obsidian Vault**: Local `.md` storage; holds graph map, lessons learnt, persistent decisions/patterns
- **SpecKit/Specify**: Global CLI; core `specify` command for spec-first feature lifecycle
- **Caveman Skill**: Response compression (~60–75% reduction) without losing technical content
- **AI Agents**: GitHub Copilot (`.github/agents/`) and Claude Code (`.claude/commands/`)

**Delivery**: Markdown-only skills, workflows, setup guides. No binaries.

**Directory roles**:
- `skills/` – AI-executable skill files (context-load, map-codebase, lessons-learnt, speckit-enrich/*)
- `workflows/` – Multi-step processes (init-workflow, feature-lifecycle, map-refresh, component-update)
- `setup-guides/` – Per-tool install docs (graphify, obsidian, speckit)
- `vault/` – Runtime Obsidian vault (graph/, lessons/, context/decisions + patterns)
- `specs/` – SpecKit-generated feature docs (spec.md, plan.md, tasks.md)
- `.specify/` – SpecKit configuration (templates, constitution, git extensions)

---

## Key Workflows

### 1. Initialization (init-workflow.md)
- Detect installed tools (Graphify, SpecKit, Obsidian)
- Install missing prerequisites globally or flag requirements
- Deploy Spekificity custom skills locally
- Idempotent: safe to re-run

### 2. Enriched SpecKit Feature Lifecycle (feature-lifecycle.md)
```
Session Start
  ↓
/context-load                    ← AI primed with vault graph + past decisions
  ↓
/speckit-enrich-specify          ← Spec generation with graph cross-refs
  ↓
/speckit-enrich-plan             ← Plan with impacted component list
  ↓
/speckit.tasks                   ← Standard SpecKit (no enrichment needed)
  ↓
/speckit-enrich-implement        ← Impl + auto-lessons + auto-map
  ↓
Feature complete
```
**Decorator pattern**: All enrich-* skills wrap vanilla SpecKit commands; original SpecKit untouched.

### 3. Codebase Mapping (map-refresh.md)
- Run Graphify against source + docs
- Store graph as Obsidian vault (`vault/graph/index.md`)
- Supports incremental refresh
- Reduces token cost: AI queries graph instead of re-reading files

### 4. Lessons Learnt (context-load / lessons-learnt skills)
- End-of-feature structured entry captures: decisions, problems, patterns, recommendations
- Stored in `vault/lessons/<date>-<feature-slug>.md`
- Surfaced in `/context-load` for future sessions
- Maintains `vault/context/decisions.md` and `vault/context/patterns.md`

---

## Documentation Map

| Document | Location | Purpose |
|----------|----------|---------|
| Project overview | `README.md` | Entry point; quickstart; prerequisites; structure |
| PRD (Product Requirements) | `docs/prd.md` | Goals, user journeys, functional/non-functional requirements |
| Architecture | `docs/architecture.md` | Component roles, data flow, vault structure |
| Glossary | `docs/glossary.md` | Term definitions (AI Agent, Caveman, Decorator, Graphify, etc.) |
| Init guide | `docs/init.md` | Initialization narrative and procedures |
| Validation | `docs/validation.md` | Testing and acceptance criteria |
| Feature spec | `specs/001-specificity-platform/spec.md` | Full feature definition with user stories and requirements |
| Quick reference | `specs/001-specificity-platform/quickstart.md` | Step-by-step setup guide |
| Skill definitions | `skills/<skill-name>/SKILL.md` | Triggerable AI skills (agent-agnostic format) |
| Workflow guides | `workflows/*.md` | Multi-step sequences (init, feature lifecycle, map refresh, component updates) |
| Setup guides | `setup-guides/*.md` | Per-tool installation (Graphify, Obsidian, SpecKit) |
| Vault decisions | `vault/context/decisions.md` | Architectural decisions log |
| Vault patterns | `vault/context/patterns.md` | Identified patterns log |
| Vault graph | `vault/graph/index.md` | Generated Graphify output (runtime) |
| Vault lessons | `vault/lessons/*.md` | Feature lessons entries (runtime) |
| Skill discovery | `agents.md` | Claude Code slash-command index |

---

## Critical Success Criteria

- Init completes in <30 min; token savings ≥40% on mapped projects; Caveman ≥60% compression
- All SpecKit steps enriched when map available
- Independent component updates (no cross-breaking changes)
- macOS + Linux support
- No cloud/server required (fully local)

---

## Known Dependencies

- Python 3.11+, `uv` package manager
- SpecKit installed globally: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- Graphify installed globally: `uv tool install graphifyy`
- GitHub Copilot or Claude Code for AI agent
- Obsidian (desktop app optional; vault is plain markdown)
- Git + basic terminal knowledge

---

## Entry Points for Agent Interaction

**At session start:**
```
/context-load
```

**For daily feature work:**
```
/speckit-enrich-specify → /speckit-enrich-plan → /speckit.tasks → /speckit-enrich-implement
```

**For codebase refresh:**
```
/map-codebase
```

**For token efficiency:**
```
/caveman lite     (specs/plans)
/caveman          (implementation)
```

---

**Status**: Production-ready meta-tooling layer. Zero breaking changes expected for dependent projects. Modular: each component can be updated independently.
