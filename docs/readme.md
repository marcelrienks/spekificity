# spekificity

an agentic focused toolset that connects four existing tools into a single ai-driven development workflow. designed to be executed by ai agents (github copilot, claude code).

---

## what is spekificity?

**spekificity** enhances ai-assisted software development by wiring together graphify, obsidian, github speckit/specify, and caveman mode into a unified workflow. it provides markdown-based skills, workflow guides, and setup documentation that agents read and execute to automate development tasks, maintain persistent context across sessions, and reduce token consumption.

**value proposition**: reduce friction, token cost, and context loss in ai-assisted development without replacing or forking any existing tool.

---

## components

| tool | role |
|------|------|
| **graphify** | generates dependency/relationship graphs of source code and documentation |
| **obsidian** | stores and navigates graphs as a local markdown vault, providing persistent ai context |
| **github speckit / specify** | drives spec-first, ai-guided feature development lifecycle |
| **caveman skill** | compresses ai prompts and responses to minimize token usage |

---

## core problems solved

1. **context loss between sessions** — ai agents have no persistent memory of past decisions. spekificity stores decisions, patterns, and lessons in an obsidian vault that agents can read at session start.
2. **high token consumption** — agents typically read every file recursively to understand a codebase. spekificity indexes the codebase as a graph, replacing recursive file scans with targeted vault queries (40%+ token savings).
3. **shallow speckit lifecycle** — speckit lacks awareness of existing code structure. spekificity decorates speckit steps with graph-aware skills that ground specs and plans in reality.
4. **verbose ai interactions** — agents are verbose by default. caveman mode compresses responses 60%+ without losing technical accuracy.

---

## quick start

### 1. initialize spekificity in your project

```bash
# run from project root
spekificity init
```

this command installs/verifies graphify, obsidian, speckit, and installs spekificity custom skills locally.

### 2. map your codebase

```bash
/map-codebase
```

ai runs graphify against your source files and documentation. the graph is stored as an obsidian vault inside your project. future ai sessions load the vault index instead of scanning files.

### 3. start a feature

**automated (recommended)**: use the `spek` cli to drive the full lifecycle:

```bash
spek automate "add user authentication with JWT"
```

this creates a feature branch, then drives spec → plan → tasks → analyse → implement → postflight without manual step invocations. the ai agent is invoked at each step via `/spek.automate`.

**manual**: invoke speckit steps individually in your ai session:

```bash
/speckit.specify
```

ai reads your vault context and produces a richer spec grounded in your actual codebase.

see [guide.md](guide.md) for the full feature lifecycle including the `spek` cli command reference.

---

## target users

- **solo developers** on personal or side projects who value speed and reduced cognitive load
- **team leads / architects** setting up toolchains for teams; value consistency and onboarding simplicity
- **ai power users** who want to maximize value from every token

**minimum viable user**: comfortable with terminal, git, and ai agent interaction. wants structured ai assistance without manual context management.

---

## documentation

- [architecture.md](architecture.md) — directory structure, component roles, data flow, update strategy
- [guide.md](guide.md) — full feature lifecycle workflow, enriched speckit lifecycle
- [glossary.md](glossary.md) — terminology reference
- [faq.md](faq.md) — troubleshooting and common questions
- [validation.md](validation.md) — success criteria validation methodology

---

## design principles

- **decorator pattern**: spekificity skills wrap, not replace, standard speckit commands
- **modular independence**: each component (graphify, obsidian, speckit, spekificity layer) can be updated independently
- **global speckit, local customisation**: speckit installs globally; spekificity skills install locally per-project
- **ai-executable setup**: wherever automation is impractical, setup is documented as step-by-step guides
- **token efficiency by default**: caveman mode and graph-based context loading are first-class citizens

---

## component ownership

| component | owner | update |
|-----------|-------|--------|
| graphify | third party | update independently |
| obsidian | third party | update independently |
| speckit / specify | third party (global) | `npm update -g specify` |
| spekificity custom skills | this project | `git pull` in this repo |

---

## supported ai agents

- github copilot
- claude code

---

## no application code

spekificity contains **no runtime code, servers, or applications**. it is purely markdown documentation — skills, workflows, guides, and setup instructions that agents read and execute.
