# Spekificity — Project Initialisation Document

## What Is This Project?

**Spekificity** is a meta-tooling layer that orchestrates four existing tools into a unified, AI-assisted development workflow:

| Tool | Role |
|------|------|
| **Graphify** | Generates dependency/relationship graphs of source code and documentation |
| **Obsidian** | Stores and navigates those graphs as a local markdown vault, providing persistent AI context |
| **GitHub SpecKit / Specify** | Drives spec-first, AI-guided feature development lifecycle |
| **Caveman skill** | Compresses AI prompts and responses to minimise token usage |

Spekificity itself contains **no application code**. It is a curated collection of skills, workflow guides, and setup documentation that tells any AI agent how to initialise, configure, and operate the full stack on any project.

---

## Core Problem Being Solved

Vanilla AI-assisted development suffers from three recurring problems:

1. **Context loss between sessions** — AI agents have no persistent memory of past decisions, making every session start from scratch.
2. **High token consumption** — Agents read every file recursively to answer cross-cutting questions, which is expensive and slow.
3. **Shallow SpecKit usage** — The speckit lifecycle lacks awareness of existing code structure, so specs and plans are not grounded in the actual codebase.

Spekificity solves all three by wiring Graphify → Obsidian as a persistent, graph-indexed context store, then decorating SpecKit's workflow with skills that consult that store.

---

## Design Principles

- **Decorator pattern**: Spekificity skills wrap, not replace, standard SpecKit commands. Vanilla SpecKit remains untouched and upgradable.
- **Modular independence**: Graphify, Obsidian, SpecKit, and the Spekificity custom layer can each be updated independently.
- **Global SpecKit, local customisation**: SpecKit/Specify is installed globally so upstream updates apply immediately. Spekificity installs its custom skills locally per-project.
- **AI-executable setup**: Wherever CLI automation is impractical, setup is documented as step-by-step guides that an AI agent can follow.
- **Token efficiency by default**: Caveman mode and graph-based context loading are first-class citizens, not afterthoughts.

---

## High-Level Architecture

```
[Developer runs init command]
         │
         ▼
┌────────────────────────────────────────────┐
│           Spekificity Init                 │
│  1. Install / verify Graphify              │
│  2. Install / verify Obsidian              │
│  3. Install / verify SpecKit (global)      │
│  4. Install custom skills & workflows      │
│     (local, per-project)                   │
└────────────────────────────────────────────┘
         │
         ▼
[Developer starts AI session]
         │
         ▼
┌────────────────────────────────────────────┐
│         Spekificity Workflow               │
│                                            │
│  /map-codebase ──► Graphify ──► Obsidian  │
│  /speckit.specify (enriched with graph)    │
│  /speckit.plan    (enriched with graph)    │
│  /speckit.tasks                            │
│  /speckit.implement                        │
│  /lessons-learnt ──► Obsidian vault        │
│  /caveman (active throughout)              │
└────────────────────────────────────────────┘
```

---

## Intended Workflow (Step by Step)

1. Developer runs the Spekificity init command inside a project folder (empty or populated).
2. Init detects installed tools; installs or links missing ones.
3. Custom Spekificity skills and workflow docs are installed locally.
4. Developer invokes `/map-codebase` to build the Graphify → Obsidian context graph.
5. Developer begins a SpecKit feature lifecycle (`/speckit.specify`, `/speckit.plan`, etc.).
6. At each SpecKit step the AI agent reads from the Obsidian vault rather than scanning all files.
7. On feature completion, `/lessons-learnt` appends a structured entry to the vault.
8. Caveman mode is available at any point to compress context and reduce token costs.

---

## Component Boundaries

| Component | Owned By | Update Path |
|-----------|----------|-------------|
| Graphify | Third party | Update independently; Spekificity adapts |
| Obsidian | Third party | Update independently; vault format is stable markdown |
| SpecKit / Specify | Third party (global) | `npm update -g specify` or equivalent |
| Spekificity custom skills | This project | Pull latest from this repo |

---

## Supported AI Agents (Initial Version)

- GitHub Copilot
- Claude Code

---

## Out of Scope (v1)

- Any GUI or web interface
- Multi-user / shared vault synchronisation
- Support for AI agents beyond Copilot and Claude Code
- Automatic conflict resolution between SpecKit upstream changes and Spekificity customisations