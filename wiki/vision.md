# Spekificity: Vision & Core Principles

Quick orientation to Spekificity's goals and philosophy.

---

## Vision

Spekificity is a spec-driven agent development framework that ties persistent knowledge (Obsidian vault), code analysis (lat.md), workflow automation (SpecKit), and skill execution into a cohesive system. It enables rapid, deterministic feature development with minimal token overhead and maximum context reuse.

**Core Problem:** AI-assisted development often loses context between sessions, wastes tokens re-reading files, and produces work without durable specifications or lessons.

**Core Solution:** Treat documentation as canonical memory (markdown vault), use a code graph for precise context (lat.md), and orchestrate feature work with spec-first workflow (SpecKit).

---

## Four Pillars

1. **Token Efficiency** — Pre-index code and docs; load minimal, relevant context; compress outputs when needed.
2. **Determinism** — Enforce spec → plan → implement → conclude workflows; outcomes reproducible and auditable.
3. **Persistence** — Store specs, decisions, and lessons in Git-backed vault; knowledge compounds across sessions.
4. **Autonomy** — Equip agents with deterministic tools and indexed context; execute with minimal hand-holding.

---

## Philosophy

- **Consolidation:** Integrate best-in-class tools (SpecKit, lat.md, Obsidian) rather than rebuilding.
- **Decorator Pattern:** Spekificity wraps SpecKit without modifying it.
- **Modularity:** Each component (vault, index, spec engine, compression) upgradeable independently.
- **Human-in-the-Loop:** Agent actions gated by plan reviews; humans resolve conflicts.
- **Token Efficiency First:** Graph queries + cached context replace file scans; Caveman mode available for terse outputs.

---

## Getting Started

1. Run `spek init` to scaffold `.spek/`, vault/, and recommended defaults.
2. Install lat.md and SpecKit per [setup.md](setup.md).
3. Use `/spek.prepare` → `/spek.plan` → `/spek.implement` → `/spek.conclude` workflow.

---

## Next Steps

- **Architecture & Components:** [architecture.md](architecture.md)
- **Feature Workflow:** [workflow.md](workflow.md)
- **Setup & Installation:** [setup.md](setup.md)
- **Skills & Commands:** [skills.md](skills.md)
- **Reusable Patterns:** [patterns.md](patterns.md)
- **Design Decisions:** [decision.md](decision.md)
