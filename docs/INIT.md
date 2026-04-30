# spekificity — project initialisation document

## what is this project?

**spekificity** is a platform that connects four existing tools into a single ai development workflow:

| tool | role |
|------|------|
| **graphify** | generates dependency/relationship graphs of source code and documentation |
| **obsidian** | stores and navigates those graphs as a local markdown vault, providing persistent ai context |
| **github speckit / specify** | drives spec-first, ai-guided feature development lifecycle |
| **caveman skill** | compresses ai prompts and responses to minimise token usage |

spekificity itself contains **no application code**. it is a collection of skills, workflow guides, and setup documentation that tells any ai agent how to initialise, configure, and operate the full stack on any project.

---

## core problem being solved

vanilla ai-assisted development suffers from three recurring problems:

1. **context loss between sessions** — ai agents have no persistent memory of past decisions, making every session start from scratch.
2. **high token consumption** — agents read every file recursively to answer cross-cutting questions, which is expensive and slow.
3. **shallow speckit usage** — the speckit lifecycle lacks awareness of existing code structure, so specs and plans are not grounded in the actual codebase.

spekificity solves all three by wiring graphify → obsidian as a persistent, graph-indexed context store, then decorating speckit's workflow with skills that consult that store.

---

## design principles

- **decorator pattern**: spekificity skills wrap, not replace, standard speckit commands. vanilla speckit remains untouched and upgradable.
- **modular independence**: graphify, obsidian, speckit, and the spekificity custom layer can each be updated independently.
- **global speckit, local customisation**: speckit/specify is installed globally so upstream updates apply immediately. spekificity installs its custom skills locally per-project.
- **ai-executable setup**: wherever cli automation is impractical, setup is documented as step-by-step guides that an ai agent can follow.
- **token efficiency by default**: caveman mode and graph-based context loading are first-class citizens, not afterthoughts.

---

## high-level architecture

```
[developer runs init command]
         │
         ▼
┌────────────────────────────────────────────┐
│           spekificity init                 │
│  1. install / verify graphify              │
│  2. install / verify obsidian              │
│  3. install / verify speckit (global)      │
│  4. install custom skills & workflows      │
│     (local, per-project)                   │
└────────────────────────────────────────────┘
         │
         ▼
[developer starts ai session]
         │
         ▼
┌────────────────────────────────────────────┐
│         spekificity workflow               │
│                                            │
│  /map-codebase ──► graphify ──► obsidian  │
│  /speckit.specify (enriched with graph)    │
│  /speckit.plan    (enriched with graph)    │
│  /speckit.tasks                            │
│  /speckit.implement                        │
│  /lessons-learnt ──► obsidian vault        │
│  /caveman (active throughout)              │
└────────────────────────────────────────────┘
```

---

## intended workflow (step by step)

1. developer runs the spekificity init command inside a project folder (empty or populated).
2. init detects installed tools; installs or links missing ones.
3. custom spekificity skills and workflow docs are installed locally.
4. developer invokes `/map-codebase` to build the graphify → obsidian context graph.
5. developer begins a speckit feature lifecycle (`/speckit.specify`, `/speckit.plan`, etc.).
6. at each speckit step the ai agent reads from the obsidian vault rather than scanning all files.
7. on feature completion, `/lessons-learnt` appends a structured entry to the vault.
8. caveman mode is available at any point to compress context and reduce token costs.

---

## component boundaries

| component | owned by | update path |
|-----------|----------|-------------|
| graphify | third party | update independently; spekificity adapts |
| obsidian | third party | update independently; vault format is stable markdown |
| speckit / specify | third party (global) | `npm update -g specify` or equivalent |
| spekificity custom skills | this project | pull latest from this repo |

---

## supported ai agents (initial version)

- github copilot
- claude code

---

## out of scope (v1)

- any gui or web interface
- multi-user / shared vault synchronisation
- support for ai agents beyond copilot and claude code
- automatic conflict resolution between speckit upstream changes and spekificity customisations