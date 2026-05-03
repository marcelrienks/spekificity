<!-- speckit start -->
for additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/003-spek-full-workflow-cli/plan.md
<!-- speckit end -->

<!-- specificity start -->
## session start

at the start of every session, run:
```
/context-load
```
this loads the obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory. it is the mandatory first step before any feature work.

## spekificity unified skill index

### spekificity custom skills (namespace: `spek.*`)

| command | namespace | description |
|---------|-----------|-------------|
| `/spek.context-load` | spekificity | load vault context (graph, decisions, patterns, lessons) |
| `/spek.map-codebase` | spekificity | run graphify to build/refresh the obsidian vault graph |
| `/spek.lessons-learnt` | spekificity | write structured lessons to the vault at feature end |

### speckit skills (namespace: `speckit.*`)

| command | namespace | description |
|---------|-----------|-------------|
| `/speckit.specify` | speckit | create feature specification from natural language |
| `/speckit.plan` | speckit | create implementation plan with design and tasks |
| `/speckit.tasks` | speckit | generate actionable, dependency-ordered tasks |
| `/speckit.implement` | speckit | execute implementation plan, run all tasks |

### spekificity-enhanced workflows (namespace: `speckit-enrich.*`)

| command | description |
|---------|-------------|
| `/speckit-enrich-specify` | graph-aware decorator for `/speckit.specify` with codebase context |
| `/speckit-enrich-plan` | graph-aware decorator for `/speckit.plan` with architectural decisions |
| `/speckit-enrich-implement` | graph-aware decorator for `/speckit.implement` with auto lessons + map update |

### optional skills

| command | namespace | description |
|---------|-----------|-------------|
| `/caveman lite` | system | token-compressed response mode (optional, if available) |

## namespace reference

- **`spek.*`** — spekificity custom platform skills (`.spekificity/skills/`)
- **`speckit.*`** — speckit/specify framework skills (`.github/agents/`)
- **`speckit-enrich.*`** — enhanced speckit wrappers (graph-aware orchestration)
- **`/caveman`** — system-level token compression (optional, if installed)

see `.spekificity/skill-index.md` for full registry with status and versions.

## full feature lifecycle

see [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md) for the complete enriched speckit workflow using all skills above.

## spekificity platform setup

first-time setup:

```bash
# prerequisite check
.spekificity/bin/spek setup

# initialize all tools (speckit, graphify, obsidian, caveman)
.spekificity/bin/spek init

# verify status
.spekificity/bin/spek status
```

see `.spekificity/guides/quickstart.md` for 5-minute setup guide.
see `.spekificity/guides/manual-setup.md` for step-by-step instructions.
<!-- specificity end -->
