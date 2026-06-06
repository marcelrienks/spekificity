# Spekificity — Vision & Tenets

## Vision Statement

Spekificity is a spec-driven agent development framework that ties a persistent knowledge vault, a deterministic spec engine, and a code index into a single workflow. It solves four core problems: token efficiency, deterministic planning, persistent project memory, and agent autonomy.

## Core Problem & Core Solution

- Problem: AI-assisted development often loses context between sessions, wastes tokens re-reading files, and produces work without durable specifications or lessons.
- Solution: Treat documentation as canonical memory (markdown vault), use a code graph/index for precise context (lat.md), and orchestrate feature work with a spec-first engine (SpecKit) wrapped by Spekificity skills.

## Four Pillars

1. Token efficiency
   - Pre-index code and docs; load minimal, relevant context; use compressed output (Caveman) when appropriate.
2. Determinism
   - Enforce spec → plan → implement → conclude workflows so outcomes are reproducible and auditable.
3. Persistence
   - Store specs, decisions, and lessons in a Git-backed markdown vault so knowledge compounds across sessions.
4. Autonomy
   - Equip agents with deterministic tools and indexed context so they can execute work with minimal hand-holding.

## Philosophy & Tenets

- Consolidation, not reinvention: integrate best-in-class tools (SpecKit, lat.md, Obsidian-style vault) rather than rebuilding them.
- Decorator pattern: Spekificity wraps SpecKit commands to inject context and enrichment, without modifying upstream tools.
- Modular independence: each component (vault, index, spec engine, compression) can be upgraded independently.
- Human-in-the-loop safety: agent actions are gated by plan reviews and contradiction flags; human decisions resolve conflicts.
- Token efficiency by default: graph queries + cached vault context replace repeated file scans; Caveman mode provides optional terse outputs.

## How Components Map to the Pillars

- Vault (Obsidian-style markdown): Persistence + determinism (stores specs, decisions, lessons).
- lat.md (code index/graph): Token efficiency + determinism (indexed queries replace file scans; enables impact analysis).
- SpecKit (speckit): Deterministic workflow orchestration (spec → plan → tasks → implement).
- Caveman (compression): Token efficiency (terse, accurate outputs when needed).

## Workflow Stages (brief)

- Stage 0: Init — `spek init` scaffolds vault and tool wiring; index built once.
- Stage 1: Ingest — add raw sources to `wiki/raw/`; agent proposes ingestion plans; human approves.
- Stage 2: Feature development — `/spek.plan` (specify → plan → tasks); `/spek.implement` executes tasks with lat.md context.
- Stage 3: Conclude — `/spek.conclude` archives artifacts and extracts lessons to vault.

## Tooling & Implementation Notes

- Canonical indexer: lat.md is the recommended codegraph/index tool for deterministic queries and impact analysis.
- Persistent vault: a Git-backed Obsidian-style markdown vault (plain files) is the single source of truth. The Obsidian desktop app is optional.
- Obsidian CLI: required for automated vault operations; automation scripts assume the CLI is available for scripted exports/syncs.
- Spec engine: SpecKit (speckit.*) is the spec-first framework Spekificity decorates for orchestration.
- Compression: Caveman mode is available for token-constrained contexts; use `--caveman` or `/caveman` when terse outputs are acceptable.

## Constraints & Out-of-Scope

- Not a build system or CI replacement; integrate with existing CI for builds/tests.
- Not a real-time collaborative editor — vault is Git-backed and eventual-consistency applies.
- No prescribed model selection — skills are model-agnostic.

## Getting Started & Next Steps

- Run `spek init` to scaffold `.spek/`, vault/, and recommended defaults.
- Ensure lat.md and SpecKit are installed per `wiki/setup.md` when you need code indexing + spec workflows.
- Use `/spek.prepare` → `/spek.plan` → `/spek.implement` → `/spek.conclude` as the minimal workflow.

## References

- `wiki/architecture.md` — technical architecture and component responsibilities
- `wiki/workflow.md` — full feature lifecycle and skill semantics
- `wiki/llm-wiki.md` — canonical wiki ingestion and frontmatter rules

