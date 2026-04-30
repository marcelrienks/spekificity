# agents.md

## claude code skill discovery index

this file enables claude code's slash-command auto-discovery for spekificity skills.

---

## session start

> **always run `/context-load` before any feature work.** this loads the obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory.

```
/context-load
```

---

## available skills

| command | file | description |
|---------|------|-------------|
| `/context-load` | `.claude/commands/context-load.md` | load vault context (graph, decisions, patterns, lessons) into ai session |
| `/map-codebase` | `.claude/commands/map-codebase.md` | run graphify to build or refresh the obsidian vault graph |
| `/lessons-learnt` | `.claude/commands/lessons-learnt.md` | write structured lessons to the vault at the end of a feature |
| `/speckit-enrich-specify` | `.claude/commands/speckit-enrich-specify.md` | graph-aware decorator for `/speckit.specify` |
| `/speckit-enrich-plan` | `.claude/commands/speckit-enrich-plan.md` | graph-aware decorator for `/speckit.plan` |
| `/speckit-enrich-implement` | `.claude/commands/speckit-enrich-implement.md` | graph-aware decorator for `/speckit.implement` — automatically runs lessons + map update |

---

## token efficiency

activate caveman mode to reduce response verbosity and token consumption:

```
/caveman lite      ← for spec/plan work (preserves structure)
/caveman           ← for implementation sessions (full compression)
```

---

## full feature lifecycle

for the complete enriched speckit workflow step-by-step:

see [workflows/feature-lifecycle.md](workflows/feature-lifecycle.md)
