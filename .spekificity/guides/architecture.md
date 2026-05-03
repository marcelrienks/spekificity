# Architecture: Spekificity Platform

**Version**: 1.0.0  
**Date**: 2026-05-03

## High-Level Design

Spekificity is a **consolidation and automation layer** that orchestrates four core tools (speckit, graphify, obsidian, caveman) into a unified developer workflow.

```
┌─────────────────────────────────────────────────┐
│           Spekificity Platform                  │
│  (Unified entry point: spek setup/init/update) │
└──────────┬──────────────────────────────────────┘
           │ orchestrates
    ┌──────┴────────┬──────────┬──────────┐
    ▼               ▼          ▼          ▼
 speckit        graphify    obsidian   caveman
 (specify)      (mapping)   (vault)    (tokens)
    │               │          │          │
    └────────┬──────┴──────┬───┴─────┬────┘
             │ consolidated skills
             ▼
  .spekificity/skills/  (spek.*)
  .github/agents/       (speckit.*)
  [system]              (caveman)
```

## Component Architecture

### 1. Spekificity Platform Layer

**Location**: `.spekificity/`

- **setup-scripts/** — CLI commands (setup, init, update, status)
- **skills/** — Custom skills (spek.context-load, spek.map-codebase, spek.lessons-learnt)
- **workflows/** — Multi-step processes (setup-workflow, init-workflow, etc.)
- **guides/** — Developer and user documentation
- **config.json** — Orchestration state tracking

**Responsibilities**:
- Detect prerequisites
- Orchestrate tool initialization
- Manage project configuration
- Track initialization history
- Provide unified skill index

### 2. Speckit (specify)

**Global**: `specify` CLI command  
**Project**: `.specify/`, `.github/agents/`

- Primary feature specification framework
- Spec-first workflow (specify → plan → tasks → implement)
- Skills installed via `specify init`

**How Spekificity Uses It**:
- `spek init` calls `specify init` internally
- Speckit skills (speckit.specify, speckit.plan, etc.) installed alongside spekificity skills
- Unified skill index references both namespaces

### 3. Graphify

**Global**: `graphify` CLI command  
**Project**: `.obsidian/graph/` (via obsidian vault)

- Codebase analysis & graph generation
- Source file → dependency relationships
- Vault storage in Obsidian

**How Spekificity Uses It**:
- `spek init` checks/initializes graphify
- Graph index feeds context-load skill
- `/spek.map-codebase` runs graphify update

### 4. Obsidian

**Desktop**: Obsidian.app (optional)  
**Project**: `.obsidian/` vault

- Markdown-based knowledge vault
- Graph visualization (optional UI)
- Plain-text storage (filesystem)

**How Spekificity Uses It**:
- `spek init` configures vault location
- Optional (fallback: plain JSON storage)
- Graphify graph stored in vault
- Lessons stored in vault

### 5. Caveman Skill

**System**: Global or environment-available  
**Project**: System-level invocation

- Token compression for AI responses
- Ultra-terse notation
- Optional integration

**How Spekificity Uses It**:
- `spek init` detects availability
- Integrated if present (caveman commands available)
- Optional (not required for core functionality)

## Data Flow

### Initialization Flow

```
1. spek setup
   ├─ Detect platform (macOS/Linux/WSL)
   ├─ Verify prerequisites (Python 3.11+, uv, git)
   ├─ Initialize .spekificity/config.json
   └─ Summary report

2. spek init
   ├─ Check prerequisites
   ├─ specify init (orchestrate speckit)
   ├─ graphify init (setup codebase analysis)
   ├─ obsidian config (setup vault, optional)
   ├─ caveman check (integrate if available)
   ├─ install spekificity skills
   ├─ install workflows & guides
   ├─ generate skill-index.md
   └─ mark spek_initialized = true

3. Skills become available
   ├─ /spek.context-load
   ├─ /speckit.specify
   ├─ caveman (if available)
   └─ all tools accessible
```

### Feature Workflow Data Flow

```
/context-load
  ├─ Read .obsidian/graph/index.md
  ├─ Load vault decisions/patterns
  └─ AI primed with context

/speckit-enrich-specify
  ├─ Read graph context
  ├─ Create specs/spec.md
  └─ Cross-references to components

/speckit.plan
  ├─ Read spec.md
  ├─ Create specs/plan.md
  └─ Tech stack from graph

/spek.lessons-learnt
  ├─ Capture learning
  └─ Store in vault/lessons/
```

## State Management

### Configuration File Structure

`.spekificity/config.json` tracks:
- **Platform state** — version, initialized flag, timestamps
- **Tool integration** — each tool's installed/initialized status
- **Skills status** — which skill layers installed
- **Orchestration history** — audit trail of all operations
- **Custom preferences** — user settings (preserved across updates)

### Idempotency Model

- **Fresh run**: No config → create config → initialize all tools
- **Re-run (initialized)**: Config exists → update state → skip already-done steps
- **Partial failure**: History entries but not initialized → detect failure → provide recovery path

## Directory Organization

```
.spekificity/                    (local per-project)
├── setup-scripts/
│   ├── setup.sh                 (spek setup — prerequisite detection)
│   ├── init.sh                  (spek init — orchestration)
│   ├── update.sh                (spek update — custom layer updates)
│   ├── status.sh                (spek status — state reporting)
│   ├── prerequisites.sh         (tool detection)
│   ├── platform.sh              (OS detection)
│   ├── config-handler.sh        (config management)
│   ├── skill-discovery.sh       (skill index generation)
│   ├── idempotency.sh           (state tracking)
│   ├── logging.sh               (structured output)
│   └── validate-namespace.sh    (namespace checking)
├── skills/
│   ├── spek.context-load.md
│   ├── spek.map-codebase.md
│   ├── spek.lessons-learnt.md
│   └── [future skills]
├── workflows/
│   ├── setup-workflow.md
│   ├── init-workflow.md
│   ├── update-workflow.md
│   └── integration-guide.md
├── guides/
│   ├── architecture.md           (this file)
│   ├── orchestration-model.md
│   ├── skill-development.md
│   ├── troubleshooting.md
│   ├── manual-setup.md
│   └── migration.md
├── bin/
│   └── spek                      (command dispatcher)
├── config.json                   (orchestration state)
├── config-schema.json            (JSON schema)
├── skill-index.md                (unified skill registry)
├── version.txt                   (1.0.0)
└── README.md                     (directory guide)

.specify/                         (speckit, created by specify init)
├── constitution.md
├── feature.json
├── memory/
└── [other speckit files]

.github/agents/                   (speckit skills, created by specify init)
├── speckit.specify.md
├── speckit.plan.md
├── speckit.tasks.md
└── speckit.implement.md

.obsidian/                        (optional, created by spek init)
├── vault-info.json
├── graph/
│   └── index.md                  (graphify output)
├── decisions.md
└── [other vault files]
```

## Namespace Convention

### Spekificity Namespace
- **Skills**: `/spek.*` (e.g., `/spek.context-load`)
- **Config keys**: `spek_*` or `spek.*` (e.g., `spek_version`, `spek.tools`)
- **Files**: `.spekificity/` directory tree

### Speckit Namespace
- **Skills**: `/speckit.*` (e.g., `/speckit.specify`)
- **Files**: `.specify/`, `.github/agents/`

### Caveman Namespace
- **Mode**: `caveman` (system-level, no project-specific prefix)

## Extension Points

### Adding Custom Skills

1. Create `spek.my-skill.md` in `.spekificity/skills/`
2. Follow skill format (AI agent markdown)
3. Run `spek init` to regenerate skill index
4. Skills available as `/spek.my-skill`

### Customizing Configuration

Edit `.spekificity/config.json` → `spek_custom_preferences`:
```json
{
  "spek_custom_preferences": {
    "graphify_depth": "deep",
    "auto_lessons": true,
    "update_frequency": "weekly"
  }
}
```

### Extending Workflows

Create new workflow markdown in `.spekificity/workflows/`
- Reference existing skills and tools
- Document orchestration sequence
- Link to guides

## Performance Targets

- **spek setup**: <20 min (including tool installs)
- **spek init**: <2 min (with prerequisites installed)
- **spek status**: <1 sec
- **Idempotent re-run**: <30 sec
- **Skill invocation**: <100 ms overhead

---

**Next**: See `orchestration-model.md` for detailed orchestration flow documentation.
