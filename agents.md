# AGENTS.md

## Claude Code Skill Discovery Index

This file enables Claude Code's slash-command auto-discovery for Spekificity skills.

---

## Session Start

> **Always run `/context-load` before any feature work.** This loads the Obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory.

```
/context-load
```

---

## Available Skills

| Command | File | Description |
|---------|------|-------------|
| `/context-load` | `.claude/commands/context-load.md` | Load vault context (graph, decisions, patterns, lessons) into AI session |
| `/map-codebase` | `.claude/commands/map-codebase.md` | Run Graphify to build or refresh the Obsidian vault graph |
| `/lessons-learnt` | `.claude/commands/lessons-learnt.md` | Write structured lessons to the vault at the end of a feature |
| `/speckit-enrich-specify` | `.claude/commands/speckit-enrich-specify.md` | Graph-aware decorator for `/speckit.specify` |
| `/speckit-enrich-plan` | `.claude/commands/speckit-enrich-plan.md` | Graph-aware decorator for `/speckit.plan` |
| `/speckit-enrich-implement` | `.claude/commands/speckit-enrich-implement.md` | Graph-aware decorator for `/speckit.implement` — automatically runs lessons + map update |

---

## Token Efficiency

Activate Caveman mode to reduce response verbosity and token consumption:

```
/caveman lite      ← For spec/plan work (preserves structure)
/caveman           ← For implementation sessions (full compression)
```

---

## Full Feature Lifecycle

For the complete enriched SpecKit workflow step-by-step:

See [workflows/feature-lifecycle.md](workflows/feature-lifecycle.md)
