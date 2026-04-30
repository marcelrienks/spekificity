<!-- speckit start -->
for additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/001-spekificity-platform/plan.md
<!-- speckit end -->

<!-- specificity start -->
## session start

at the start of every session, run:
```
/context-load
```
this loads the obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory. it is the mandatory first step before any feature work.

## spekificity skill index

| command | agent file | description |
|---------|-----------|-------------|
| `/context-load` | `.github/agents/context-load.agent.md` | load vault context (graph, decisions, patterns, lessons) |
| `/map-codebase` | `.github/agents/map-codebase.agent.md` | run graphify to build/refresh the obsidian vault graph |
| `/lessons-learnt` | `.github/agents/lessons-learnt.agent.md` | write structured lessons to the vault at feature end |
| `/speckit-enrich-specify` | `.github/agents/speckit-enrich-specify.agent.md` | graph-aware decorator for `/speckit.specify` |
| `/speckit-enrich-plan` | `.github/agents/speckit-enrich-plan.agent.md` | graph-aware decorator for `/speckit.plan` |
| `/speckit-enrich-implement` | `.github/agents/speckit-enrich-implement.agent.md` | graph-aware decorator for `/speckit.implement` with auto lessons + map |

## full feature lifecycle

see [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md) for the complete enriched speckit workflow using all skills above.
<!-- specificity end -->
