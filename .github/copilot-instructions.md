<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/001-spekificity-platform/plan.md
<!-- SPECKIT END -->

<!-- SPECIFICITY START -->
## Session Start

At the start of every session, run:
```
/context-load
```
This loads the Obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory. It is the mandatory first step before any feature work.

## Spekificity Skill Index

| Command | Agent file | Description |
|---------|-----------|-------------|
| `/context-load` | `.github/agents/context-load.agent.md` | Load vault context (graph, decisions, patterns, lessons) |
| `/map-codebase` | `.github/agents/map-codebase.agent.md` | Run Graphify to build/refresh the Obsidian vault graph |
| `/lessons-learnt` | `.github/agents/lessons-learnt.agent.md` | Write structured lessons to the vault at feature end |
| `/speckit-enrich-specify` | `.github/agents/speckit-enrich-specify.agent.md` | Graph-aware decorator for `/speckit.specify` |
| `/speckit-enrich-plan` | `.github/agents/speckit-enrich-plan.agent.md` | Graph-aware decorator for `/speckit.plan` |
| `/speckit-enrich-implement` | `.github/agents/speckit-enrich-implement.agent.md` | Graph-aware decorator for `/speckit.implement` with auto lessons + map |

## Full Feature Lifecycle

See [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md) for the complete enriched SpecKit workflow using all skills above.
<!-- SPECIFICITY END -->
