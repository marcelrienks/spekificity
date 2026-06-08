---
title: Spekificity Project Context
last_read: 2026-06-08
---

# Technical Brief: Spekificity

## Project Purpose
**Spekificity** is a specification-driven agent development framework that integrates SpecKit (workflow orchestration), lat.md (code indexing), Obsidian vault (knowledge persistence), and Caveman compression (token efficiency) into a coherent pipeline.

**Core Goal:** Enable rapid, deterministic feature development with minimal token overhead and maximum context reuse.

**Problem Solved:** AI-assisted development loses context between sessions, wastes tokens re-reading files, and produces work without durable specifications or lessons. Spekificity addresses this by treating documentation as canonical memory (markdown vault), using a code graph for precise context (lat.md), and orchestrating feature work with spec-first workflow (SpecKit).

---

## Architecture & Tech Stack

### Languages & Frameworks
- **Python 3.11+** — CLI and core infrastructure
- **SpecKit/Specify (GitHub official)** — Spec-driven workflow engine
- **lat.md** — Code indexing and analysis for agents
- **Obsidian** — Knowledge vault (markdown-based, Git-tracked)
- **Caveman** — Token compression (integrated)

### Core Components
```
vault/ (persistent knowledge)
  ├── decision.md (architectural decisions)
  ├── patterns.md (reusable patterns)
  ├── lessons/ (per-feature retrospectives)
  └── vision.md (project philosophy)

.lat/ (code index)
  └── per-project incremental index (SQLite)

.spek/ (Spekificity config + skills)
  └── skills/ (agent skill definitions)

.specify/ (SpecKit per-project config)
  ├── memory/ (constitution.md)
  ├── extensions.yml
  └── templates/
```

### Core Pillars
1. **Token Efficiency** — Pre-indexed code + context layers + compression
2. **Determinism** — Spec → plan → implement → conclude workflow
3. **Persistence** — Git-backed vault stores specs, decisions, lessons
4. **Autonomy** — Agents equipped with indexed context and deterministic tools

### Design Pattern
**Decorator Pattern:** Spekificity wraps SpecKit (via enrichment layer) to inject context without modifying SpecKit internals.

---

## Key Workflows

### 4-Stage Feature Lifecycle

**Stage 1: Prepare**
- Validate workspace (git state, vault sync, code index)
- Load session context (decisions, patterns, vault)
- Ready for planning

**Stage 2: Plan**
- Generate specification (what, why, success criteria, risk assessment)
- Create implementation plan (architecture, tech choices, dependencies)
- Break into executable tasks (ordered, dependency-aware)
- User review and approval gates

**Stage 3: Implement**
- Execute tasks sequentially with context injection
- Per-task: load spec + plan + lat.md impact + prior decisions
- Validate against Success Criteria
- Commit code with task references

**Stage 4: Conclude**
- Archive outcomes (spec, plan, code changes)
- Extract lessons learned (what worked, what was difficult, patterns)
- Update vault with new decisions and patterns
- Refresh code index (lat.md)
- Ready for next feature

### Agent Skills (Claude Code)
All workflow commands are `/spek.*` agent skills (not CLI):

```
/spek.prepare [feature-name]              # Pre-flight setup
/spek.plan [feature-name|spec-file]       # Spec → plan → tasks
/spek.implement [feature-name] [--steps N] # Execute tasks
/spek.conclude [--caveman-mode=...]       # Archive + lessons + sync
```

Optional enhancements:
```
/spek.context [--scope user|session|repo] # Load vault knowledge
/spek.map [spec-file] [--show-...]        # Dependency analysis
/spek.lessons [feature-name|--deep]       # Explicit retrospective
```

**CLI Command (Only One):**
```
spek init                                  # One-time project setup
```

---

## Documentation Map

### Getting Started
- **[README.md](README.md)** — Overview, quick start, installation
- **[wiki/vision.md](wiki/vision.md)** — Design philosophy, 4 pillars

### Understanding the System
- **[wiki/architecture.md](wiki/architecture.md)** — Components, execution model, data flow
- **[wiki/setup.md](wiki/setup.md)** — Installation, per-project initialization, Obsidian

### Daily Reference
- **[wiki/workflow.md](wiki/workflow.md)** — Complete 4-stage workflow with examples
- **[wiki/skills.md](wiki/skills.md)** — Command reference for /spek.*, /speckit.*, etc.
- **[wiki/conventions.md](wiki/conventions.md)** — File/directory naming, command naming

### Knowledge & Patterns
- **[wiki/decision.md](wiki/decision.md)** — 12 architectural decisions with rationale
- **[wiki/patterns.md](wiki/patterns.md)** — 24+ reusable patterns indexed by problem
- **[wiki/context-loading.md](wiki/context-loading.md)** — Code indexing + context injection

---

## Key Concepts

### Three-Layer Memory Model
1. **Vault** (persistent knowledge) — Specs, decisions, lessons, patterns stored in Git
2. **Repo Memory** (workspace facts) — Architecture decisions, patterns indexed in `.spek/memory/`
3. **Session State** (temporary) — Current feature context (cleaned after conclude)

### Three-Layer Query Rule
1. **Layer 1: Code Graph** (lat.md) — Pre-indexed symbols, calls, impact analysis
2. **Layer 2: Vault** — Architecture decisions, patterns, lessons (searchable summaries)
3. **Layer 3: Raw Code** — Full source files (only when layers 1-2 insufficient)

Prioritize lower layers to reduce token overhead.

### Enrichment Layer
Spekificity injects context into SpecKit phases:
- Vault decisions + patterns loaded before `/speckit.specify`
- Code graph (lat.md) impact analysis loaded before `/speckit.plan`
- Previous outcomes injected during `/speckit.implement`

### Zettelkasten Vault Structure
- **Atomic notes** — One concept per file
- **YAML frontmatter** — Metadata (type, tags, status, created, updated, source, related)
- **Kebab-case filenames** — Consistent naming for automation
- **2-4 wikilinks per note** — Creates knowledge graph

### Caveman Compression
Three intensity levels for token reduction:
- **lite** (~25% savings) — Remove filler words
- **full** (~50% savings) — Drop articles, use fragments (default)
- **ultra** (~75% savings) — Abbreviate, use arrows, minimal prose

---

## File Locations by Purpose

| Purpose | File | Use When |
|---------|------|----------|
| First-time setup | wiki/setup.md | Installing Spekificity |
| Understand design | wiki/vision.md, wiki/architecture.md | Onboarding, design review |
| Execute workflow | wiki/workflow.md | Running a feature |
| Look up commands | wiki/skills.md | Command syntax, options |
| Naming decisions | wiki/conventions.md | Creating specs, files, skills |
| Find patterns | wiki/patterns.md | Solving a recurring problem |
| Understand decisions | wiki/decision.md | Why a choice was made |
| Code indexing | wiki/context-loading.md | How context is loaded |
| Project philosophy | vault/vision.md | Project principles |
| Architecture record | vault/decision.md | Recorded decisions |
| Patterns used | vault/patterns.md | Reusable patterns |

---

## Critical Files & Configs

### Per-Project Setup
- `.specify/memory/constitution.md` — Project principles (SpecKit)
- `.lat/` — Code index (lat.md; auto-created)
- `vault/` — Knowledge vault (Git-tracked)
- `specs/` — Feature specifications directory

### Agent Skills (Claude Code)
- `.claude/skills/spek-prepare.md`
- `.claude/skills/spek-plan.md`
- `.claude/skills/spek-implement.md`
- `.claude/skills/spek-conclude.md`

---

## Important States & Transitions

### Feature Lifecycle
```
PREPARE (workspace ready)
  ↓
PLAN (spec → plan → tasks approved)
  ↓
IMPLEMENT (tasks complete, tests pass, code committed)
  ↓
CONCLUDE (lessons extracted, vault updated, ready for next feature)
```

### Vault State
- **During feature** — Session memory accumulates (ephemeral)
- **After conclude** — Session memory → vault (persistent)
- **Between features** — Vault serves as knowledge base for next feature

---

## Quick Decisions & Patterns

### Latest Architectural Decisions (Decision 1-12)
1. **Toolset** — SpecKit (planning), lat.md (code), Obsidian (vault), Caveman (compression)
2. **Dual System** — Knowledge vault + code analysis (separate, optimized rhythms)
3. **Tools for 4 Pillars** — Caveman, SpecKit, Obsidian, lat.md (recommended)
4. **Zettelkasten** — Atomic notes, YAML metadata, wikilinks
5. **Auto-Tagging** — Keyword extraction + vault mapping + auto-insert (enabled in conclude)
6. **3-Layer Query** — Code graph → vault → raw code (prioritize lower layers)
7. **Git Hooks** — Optional auto-sync of lat.md index post-commit
8. **Backprop Reflex** — Test failures → vault warnings (prevent repeat mistakes)
9. **RARV Cycles** — Reason-Act-Reflect-Verify for spec drift detection
10. **Anti-Sycophancy** — Contradiction detection, complexity alerts, pattern consistency
11. **Blind Review** — Optional anonymized code review pre-deployment
12. **Token Budget** — Soft limits, per-phase tracking, configurable thresholds

### Top Patterns (Quick Reference)
- **Decorator Wrapper** — Spekificity wraps SpecKit
- **Enrichment Layer** — Context injection into spec/plan/implement phases
- **Context Injection** — Load vault + code graph + prior outcomes
- **Feature Lifecycle** — 4-stage workflow (prepare → plan → implement → conclude)
- **Session-to-Vault** — Ephemeral session memory → persistent vault
- **Post-Processing** — Collect → compress → extract lessons → update vault → refresh
- **Skill Chaining** — Sequential execution of dependent skills
- See [wiki/patterns.md](wiki/patterns.md) for 24+ patterns.

---

## Token Efficiency Tips

1. **Use 3-layer rule** — Query code graph (lat.md) before vault; vault before raw files
2. **Enable Caveman compression** — Use `/caveman lite|full|ultra` for 25-75% token savings
3. **Load context once** — `/spek.prepare` loads context once; reused by all downstream tasks
4. **Avoid file scans** — lat.md queries replace grep (no file reads)
5. **Batch queries** — Combine related context loads in single phase

---

## Common Entry Points

**First-Time User:** README.md → wiki/vision.md → wiki/setup.md → wiki/workflow.md

**Quick Command Lookup:** wiki/skills.md

**Stuck on a Problem:** wiki/patterns.md (problem index) → linked pattern spec

**Need to Understand a Design Choice:** wiki/decision.md (decision tree + rationale)

**Implementing a Feature:** wiki/workflow.md (4-stage walkthrough with example)

---

## Metadata
- **Project Type:** Agent Development Framework (Python CLI + Agent Skills)
- **Repository:** spekificity (GitHub: marcelrienks/spekificity)
- **License:** MIT
- **Status:** Production ready (feature 001 complete, feature 002 in progress)

---

## File Hashes (for change detection)
```
README.md: dfc0801e4c619214c98cca7412df1a2f
wiki/architecture.md: 4a3f7f72a23c9fec2034e7fbecdb7b11
wiki/context-loading.md: 807d55ca70c0700155d4346efed963a9
wiki/conventions.md: 54533079f8530ca6099f2be292afd3b5
wiki/decision.md: df9c070a4bf2bcf7d7c1adc23755cc24
wiki/patterns.md: b59a9fa0bfd5457df579c62a38318beb
wiki/setup.md: 8473665648b0beb8d752e423f9a285a0
wiki/skills.md: bfcf83c921cfc705d6aa7da7f4f683ac
wiki/vision.md: c3593ea9d60e9d03f159241c306ab40a
wiki/workflow.md: 323302fd616bf4bb66176f2e55e26fe6
```
