# Spekificity — Product Requirements Document (PRD)

**Version**: 1.0.0  
**Status**: Draft  
**Date**: 2026-04-29  
**Owner**: Project Initiator

---

## 1. Executive Summary

Spekificity is a meta-tooling project that enhances AI-assisted software development by connecting four existing tools — Graphify, Obsidian, GitHub SpecKit/Specify, and the Caveman skill — into a single, cohesive workflow. It does not produce executable application code. Instead, it produces a structured library of skills, workflow guides, and AI agent instructions that any developer can install into any project to gain persistent context, token-efficient AI interactions, and a supercharged SpecKit development lifecycle.

**Primary value proposition**: Reduce the friction, token cost, and context loss of AI-assisted development without replacing or forking any existing tool.

---

## 2. Problem Statement

### 2.1 Context Loss Between Sessions

AI agents have no memory between sessions. Every session restart requires the developer to re-orient the agent to the codebase, past decisions, and ongoing design choices. This is time-consuming, error-prone, and expensive in tokens.

### 2.2 High Token Consumption

When an AI agent needs to understand the codebase or documentation, it typically reads every file recursively. On medium or large projects this consumes significant token budget and slows responses, pushing developers toward truncating context — which degrades quality.

### 2.3 Shallow SpecKit Lifecycle

SpecKit provides an excellent spec-first workflow, but without awareness of the existing codebase the AI produces specs and plans disconnected from reality. Developers must manually feed context, which is tedious and inconsistent.

### 2.4 Verbose AI Interactions

AI agents produce verbose responses by default. In long sessions this accumulates into very large context windows, increasing latency and cost.

---

## 3. Goals and Non-Goals

### Goals

| # | Goal |
|---|------|
| G1 | Provide a one-command (or AI-guided) initialisation that wires all tools together |
| G2 | Build and maintain a persistent, graph-indexed context store (Graphify → Obsidian) |
| G3 | Decorate the SpecKit workflow with graph-aware, context-rich skills |
| G4 | Integrate Caveman mode throughout to minimise token usage |
| G5 | Capture and surface lessons learnt across the speckit lifecycle |
| G6 | Allow each component to be updated independently |
| G7 | Support GitHub Copilot and Claude Code as first-class AI agents |

### Non-Goals (v1)

- Building any of Graphify, Obsidian, or SpecKit functionality from scratch
- Providing a GUI or web interface
- Supporting AI agents beyond Copilot and Claude Code
- Cloud sync or multi-user vault sharing
- Automatic merge conflict resolution between SpecKit upstream updates and Spekificity custom skills

---

## 4. Target Users

| Persona | Description |
|---------|-------------|
| **Solo Developer** | Individual working on personal or side projects; values speed and reduced cognitive load |
| **Team Lead / Architect** | Sets up the toolchain for a team; values consistency and onboarding simplicity |
| **AI Power User** | Highly familiar with Copilot/Claude; wants to squeeze maximum value from every token |

**Minimum viable user**: A developer comfortable with a terminal, git, and basic AI agent interaction who wants structured AI assistance without manual context management.

---

## 5. User Journeys

### Journey 1 — Initialise a New Project

```
1. Developer creates a new project folder
2. Runs: spekificity init  (or follows AI-guided setup)
3. Spekificity detects tool status (installed / missing)
4. Missing tools are installed or flagged as prerequisites
5. Custom skills and workflow docs are installed locally
6. Developer receives a summary of what was installed and next steps
```

### Journey 2 — Map an Existing Codebase

```
1. Developer opens AI chat in the project
2. Invokes: /map-codebase
3. AI runs Graphify against source files and docs
4. Graph is stored as an Obsidian vault inside the project
5. Future AI sessions load the vault index instead of scanning files
```

### Journey 3 — Run a SpecKit Feature Lifecycle (Enriched)

```
1. /speckit.specify  → AI reads vault + user description → produces richer spec
2. /speckit.plan     → AI reads vault + spec → plan references existing components
3. /speckit.tasks    → Generates dependency-ordered tasks
4. /speckit.implement → AI implements, guided by vault context
5. /lessons-learnt   → Structured entry appended to Obsidian vault
```

### Journey 4 — Update a Single Component

```
1. SpecKit releases a new version
2. Developer runs: npm update -g specify
3. Spekificity custom skills continue to work unchanged
4. If the SpecKit API changed, only the relevant adapter skill needs updating
```

---

## 6. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Init command installs/links Graphify, Obsidian, SpecKit | P1 |
| FR-002 | Init installs Spekificity custom skills locally | P1 |
| FR-003 | Init is idempotent | P1 |
| FR-004 | SpecKit is installed globally; custom skills are local | P1 |
| FR-005 | Mapping skill builds Graphify graph stored as Obsidian vault | P1 |
| FR-006 | Mapping skill supports incremental refresh | P2 |
| FR-007 | All SpecKit-extension skills follow decorator pattern | P1 |
| FR-008 | Lessons-learnt skill writes structured entries to Obsidian vault | P2 |
| FR-009 | Caveman skill is invokable at any workflow step | P2 |
| FR-010 | Each component is independently updatable | P1 |
| FR-011 | System supports GitHub Copilot and Claude Code | P1 |
| FR-012 | All non-automatable setup steps are documented as AI-executable guides | P1 |

---

## 7. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-001 | First-time init completes in under 10 minutes on a standard dev machine |
| NFR-002 | Token consumption for cross-cutting queries reduced ≥40% vs. unmapped equivalent |
| NFR-003 | Caveman mode reduces response verbosity ≥60% by character count |
| NFR-004 | All skills operate on macOS and Linux |
| NFR-005 | No backend server or cloud service required (fully local) |
| NFR-006 | Lessons-learnt entries are surfaced to AI within 2 seconds of session start |
| NFR-007 | A developer with basic terminal/git knowledge can complete setup in under 30 minutes |

---

## 8. Architecture Overview

### Component Map

```
spekificity/
├── .agents/                    # Global: SpecKit (installed globally, not here)
│
├── skills/                     # Spekificity custom skills (local per-project)
│   ├── map-codebase/           # Graphify → Obsidian mapping skill
│   ├── lessons-learnt/         # Structured lessons capture skill
│   ├── speckit-enrich/         # Decorator skills for SpecKit steps
│   └── context-load/           # Vault context loading skill
│
├── workflows/                  # Documented workflow sequences
│   ├── init-workflow.md
│   ├── feature-lifecycle.md
│   └── update-component.md
│
├── setup-guides/               # AI-executable setup instructions
│   ├── graphify-setup.md
│   ├── obsidian-setup.md
│   └── speckit-setup.md
│
├── vault/                      # Obsidian vault (per-project, gitignored or committed)
│   ├── graph/                  # Graphify-generated graph nodes
│   ├── lessons/                # Lessons learnt entries
│   └── context/                # Persistent AI context notes
│
└── docs/                       # Project-level documentation
    ├── init.md
    ├── prd.md
    ├── architecture.md
    └── glossary.md
```

### Data Flow

```
Source files / Docs
        │
        ▼
    Graphify
        │  generates dependency graph
        ▼
  Obsidian Vault
        │  provides indexed context
        ▼
   AI Agent Session
        │  consults vault instead of scanning files
        ▼
  SpecKit Lifecycle  ◄──── Spekificity decorator skills
        │
        ▼
  Lessons Learnt ──► Obsidian Vault (feedback loop)
```

---

## 9. Integration Points

| Integration | Direction | Protocol |
|-------------|-----------|----------|
| Graphify | Spekificity → Graphify | CLI command invocation |
| Obsidian vault | Read/write | Local filesystem (markdown) |
| SpecKit / Specify | Decorator wrapping | Skill file invocation |
| GitHub Copilot | AI consumes skills | `.github/copilot-instructions.md` + `.agents/` |
| Claude Code | AI consumes skills | `AGENTS.md` + `.agents/` |
| Caveman skill | Invoked within sessions | `/caveman` command |

---

## 10. Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Init completion time | ≤ 30 minutes (first-time) | Stopwatch from command to first `/speckit.specify` |
| Token reduction | ≥ 40% on cross-cutting queries | Compare token counts: mapped vs. unmapped project |
| Caveman verbosity reduction | ≥ 60% character count | Compare response lengths: caveman on vs. off |
| Component update effort | ≤ 5 minutes per component | Time a SpecKit global update with Spekificity active |
| Developer onboarding | Usable without prior knowledge of tools | Usability test with an unfamiliar developer |

---

## 11. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Graphify requires global install (cannot be local) | Medium | Medium | Document as prerequisite; init verifies before proceeding |
| Obsidian vault format changes in a future release | Low | High | Vault uses plain markdown; format is stable |
| SpecKit API changes break decorator skills | Medium | High | Adapter skill pattern isolates breakage to one file |
| AI agent skill format changes (Copilot, Claude) | Medium | Medium | Skills are plain markdown; format is resilient |
| Very large vaults slow context loading | Medium | Medium | Incremental refresh + selective vault loading by skill |

---

## 12. Open Questions

1. Can Graphify be installed as a local `node_modules` dependency, or must it be global?
2. Does Obsidian support headless/CLI operation for vault writes, or does it require the GUI app?
3. What is the preferred vault commit strategy — vault checked into git, or gitignored?
4. Should Caveman mode be opt-in per-session or always-on by default?

---

## 13. Dependencies and Prerequisites

| Dependency | Version | Notes |
|------------|---------|-------|
| Graphify | Latest stable | Install mode TBD (local vs global) |
| Obsidian | Latest stable | May require GUI app as prerequisite |
| SpecKit / Specify | ≥ 0.8.0 | Installed globally |
| Git | Any modern version | Required for feature branch workflow |
| Node.js / npm | LTS | Required for Specify/SpecKit |
| GitHub Copilot or Claude Code | Current | At least one must be active |

---

## 14. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-29 | Project Initiator | Initial draft |
