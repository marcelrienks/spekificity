# spekificity — product requirements document (prd)

**owner**: project initiator

---

## 1. executive summary

spekificity is an agentic focused toolset that enhances ai-assisted software development by connecting four existing tools — graphify, obsidian, github speckit/specify, and the caveman skill — into a single workflow. designed from the ground up to be executed by ai agents (github copilot, claude code), spekificity provides markdown-based skills, workflow guides, and instructions that agents read and execute to automate development tasks, generate code artifacts, and maintain persistent context across sessions.

**primary value proposition**: reduce the friction, token cost, and context loss of ai-assisted development without replacing or forking any existing tool.

---

## 2. problem statement

### 2.1 context loss between sessions

ai agents have no memory between sessions. every session restart requires the developer to re-orient the agent to the codebase, past decisions, and ongoing design choices. this is time-consuming, error-prone, and expensive in tokens.

### 2.2 high token consumption

when an ai agent needs to understand the codebase or documentation, it typically reads every file recursively. on medium or large projects this consumes significant token budget and slows responses, pushing developers toward truncating context — which degrades quality.

### 2.3 shallow speckit lifecycle

speckit provides an excellent spec-first workflow, but without awareness of the existing codebase the ai produces specs and plans disconnected from reality. developers must manually feed context, which is tedious and inconsistent.

### 2.4 verbose ai interactions

ai agents produce verbose responses by default. in long sessions this accumulates into very large context windows, increasing latency and cost.

---

## 3. goals and non-goals

### goals

| # | goal |
|---|------|
| g1 | provide a one-command (or ai-guided) initialisation that wires all tools together |
| g2 | build and maintain a persistent, graph-indexed context store (graphify → obsidian) |
| g3 | decorate the speckit workflow with graph-aware, context-rich skills |
| g4 | integrate caveman mode throughout to minimise token usage |
| g5 | capture and surface lessons learnt across the speckit lifecycle |
| g6 | allow each component to be updated independently |
| g7 | support github copilot and claude code as first-class ai agents |

### non-goals

- building any of graphify, obsidian, or speckit functionality from scratch
- providing a gui or web interface
- supporting ai agents beyond copilot and claude code
- cloud sync or multi-user vault sharing
- automatic merge conflict resolution between speckit upstream updates and spekificity custom skills

---

## 4. target users

| persona | description |
|---------|-------------|
| **solo developer** | individual working on personal or side projects; values speed and reduced cognitive load |
| **team lead / architect** | sets up the toolchain for a team; values consistency and onboarding simplicity |
| **ai power user** | highly familiar with copilot/claude; wants to squeeze maximum value from every token |

**minimum viable user**: a developer comfortable with a terminal, git, and basic ai agent interaction who wants structured ai assistance without manual context management.

---

## 5. user journeys

### journey 1 — initialise a new project

```
1. developer creates a new project folder
2. runs: spekificity init  (or follows ai-guided setup)
3. spekificity detects tool status (installed / missing)
4. missing tools are installed or flagged as prerequisites
5. custom skills and workflow docs are installed locally
6. developer receives a summary of what was installed and next steps
```

### journey 2 — map an existing codebase

```
1. developer opens ai chat in the project
2. invokes: /map-codebase
3. ai runs graphify against source files and docs
4. graph is stored as an obsidian vault inside the project
5. future ai sessions load the vault index instead of scanning files
```

### journey 3 — run a speckit feature lifecycle (enriched)

```
1. /speckit.specify  → ai reads vault + user description → produces richer spec
2. /speckit.plan     → ai reads vault + spec → plan references existing components
3. /speckit.tasks    → generates dependency-ordered tasks
4. /speckit.implement → ai implements, guided by vault context
5. /lessons-learnt   → structured entry appended to obsidian vault
```

### journey 4 — update a single component

```
1. speckit releases a new version
2. developer runs: npm update -g specify
3. spekificity custom skills continue to work unchanged
4. if the speckit api changed, only the relevant adapter skill needs updating
```

---

## 6. functional requirements

| id | requirement | priority |
|----|-------------|----------|
| fr-001 | init command installs/links graphify, obsidian, speckit | p1 |
| fr-002 | init installs spekificity custom skills locally | p1 |
| fr-003 | init is idempotent | p1 |
| fr-004 | speckit is installed globally; custom skills are local | p1 |
| fr-005 | mapping skill builds graphify graph stored as obsidian vault | p1 |
| fr-006 | mapping skill supports incremental refresh | p2 |
| fr-007 | all speckit-extension skills follow decorator pattern | p1 |
| fr-008 | lessons-learnt skill writes structured entries to obsidian vault | p2 |
| fr-009 | caveman skill is invokable at any workflow step | p2 |
| fr-010 | each component is independently updatable | p1 |
| fr-011 | system supports github copilot and claude code | p1 |
| fr-012 | all non-automatable setup steps are documented as ai-executable guides | p1 |

---

## 7. non-functional requirements

| id | requirement |
|----|-------------|
| nfr-001 | all skills operate on macos and linux |
| nfr-002 | no backend server or cloud service required (fully local) |
| nfr-003 | lessons-learnt entries are surfaced to ai at session start |

---

## 8. architecture overview

### component map

```
spekificity/
├── .agents/                    # global: speckit (installed globally, not here)
│
├── skills/                     # spekificity custom skills (local per-project)
│   ├── map-codebase/           # graphify → obsidian mapping skill
│   ├── lessons-learnt/         # structured lessons capture skill
│   ├── speckit-enrich/         # decorator skills for speckit steps
│   └── context-load/           # vault context loading skill
│
├── workflows/                  # documented workflow sequences
│   ├── init-workflow.md
│   ├── feature-lifecycle.md
│   └── update-component.md
│
├── setup-guides/               # ai-executable setup instructions
│   ├── graphify-setup.md
│   ├── obsidian-setup.md
│   └── speckit-setup.md
│
├── vault/                      # obsidian vault (per-project, gitignored or committed)
│   ├── graph/                  # graphify-generated graph nodes
│   ├── lessons/                # lessons learnt entries
│   └── context/                # persistent ai context notes
│
└── docs/                       # project-level documentation
    ├── init.md
    ├── prd.md
    ├── architecture.md
    └── glossary.md
```

### data flow

```
source files / docs
        │
        ▼
    graphify
        │  generates dependency graph
        ▼
  obsidian vault
        │  provides indexed context
        ▼
   ai agent session
        │  consults vault instead of scanning files
        ▼
  speckit lifecycle  ◄──── spekificity decorator skills
        │
        ▼
  lessons learnt ──► obsidian vault (feedback loop)
```

---

## 9. integration points

| integration | direction | protocol |
|-------------|-----------|----------|
| graphify | spekificity → graphify | cli command invocation |
| obsidian vault | read/write | local filesystem (markdown) |
| speckit / specify | decorator wrapping | skill file invocation |
| github copilot | ai consumes skills | `.github/copilot-instructions.md` + `.agents/` |
| claude code | ai consumes skills | `agents.md` + `.agents/` |
| caveman skill | invoked within sessions | `/caveman` command |

---

## 11. risks and mitigations

| risk | likelihood | impact | mitigation |
|------|-----------|--------|------------|
| graphify requires global install (cannot be local) | medium | medium | document as prerequisite; init verifies before proceeding |
| obsidian vault format changes in a future release | low | high | vault uses plain markdown; format is stable |
| speckit api changes break decorator skills | medium | high | adapter skill pattern isolates breakage to one file |
| ai agent skill format changes (copilot, claude) | medium | medium | skills are plain markdown; format is resilient |
| very large vaults slow context loading | medium | medium | incremental refresh + selective vault loading by skill |

---

## 12. open questions

1. can graphify be installed as a local `node_modules` dependency, or must it be global?
2. does obsidian support headless/cli operation for vault writes, or does it require the gui app?
3. what is the preferred vault commit strategy — vault checked into git, or gitignored?
4. should caveman mode be opt-in per-session or always-on by default?

---

## 13. dependencies and prerequisites

| dependency | version | notes |
|------------|---------|-------|
| graphify | latest stable | install mode tbd (local vs global) |
| obsidian | latest stable | may require gui app as prerequisite |
| speckit / specify | ≥ 0.8.0 | installed globally |
| git | any modern version | required for feature branch workflow |
| node.js / npm | lts | required for specify/speckit |
| github copilot or claude code | current | at least one must be active |

---

## 14. revision history

| version | date | author | changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-29 | project initiator | initial draft |
