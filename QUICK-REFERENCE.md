# Quick Reference: Phase 4 Implementation

## Command Summary

```
spek prepare          # 7-step workspace initialization
spek context          # Load 3-layer memory context
spek plan             # SpecKit workflow orchestration
spek map              # CodeGraph analysis & symbol queries
spek implement        # Task execution engine
spek post             # Outcome archival & vault updates
spek lessons          # Retrospective & pattern extraction
```

## Workflow: Feature Development Cycle

```
┌─────────────────────────────────────────────────────────┐
│ 1. PREPARE: Initialize Feature                          │
├─────────────────────────────────────────────────────────┤
│ $ spek prepare --feature-name "auth-system"             │
│ • Git verification (clean state required)               │
│ • Feature branch: feature/auth-system                   │
│ • Context loaded: .memories/session/                    │
│ • CodeGraph indexed: .cel/codegraph.db                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. PLAN: Create Specification & Tasks                   │
├─────────────────────────────────────────────────────────┤
│ $ spek plan "Add JWT authentication to API"             │
│ • SpecKit specify → auth-system-spec.md                 │
│ • SpecKit plan   → auth-system-plan.md                  │
│ • SpecKit tasks  → auth-system-tasks.md                 │
│ • Committed to feature branch                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. IMPLEMENT: Execute Tasks                             │
├─────────────────────────────────────────────────────────┤
│ $ spek implement --dry-run    # Preview                 │
│ $ spek implement              # Execute                 │
│ • Read tasks from tasks.md                              │
│ • Execute sequentially                                  │
│ • Track execution trace                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. POST: Archive & Vault Updates                        │
├─────────────────────────────────────────────────────────┤
│ $ spek post          # Archive feature                  │
│ $ spek post --merge  # Archive + merge to main          │
│ • Extract lessons → wiki/lessons/                       │
│ • Update CodeGraph (final refresh)                      │
│ • Commit to vault                                       │
│ • Optional: merge feature branch                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. LESSONS: Generate Retrospective                      │
├─────────────────────────────────────────────────────────┤
│ $ spek lessons --format markdown                        │
│ • Scan completed features                               │
│ • Extract patterns & insights                           │
│ • Generate recommendations                              │
│ • Output: wiki/lessons/insights-report.md               │
└─────────────────────────────────────────────────────────┘
```

## Common Commands

### Preparation Phase
```bash
# Initialize new feature
spek prepare --feature-name "payment-gateway"

# View project context
spek context --layer all
spek context --layer session

# Check CodeGraph status
spek map
spek map --symbol "PaymentController"
spek map --symbol "PaymentController" --impact
```

### Planning Phase
```bash
# Create specification from intent
spek plan "Add Stripe payment integration"

# Interactive mode
spek plan --interactive
```

### Implementation Phase
```bash
# Preview tasks (dry-run)
spek implement --dry-run

# Execute all tasks
spek implement

# Execute specific tasks
spek implement --task 1 --task 3
```

### Post-Processing Phase
```bash
# Archive without merging
spek post

# Archive and merge to main
spek post --merge
```

### Analysis Phase
```bash
# Generate markdown report
spek lessons --format markdown

# Generate JSON report
spek lessons --format json
```

## Options Reference

### Global Options
```
--version, -V          Show version and exit
-v, --verbose          Enable verbose logging
--help, -h            Show help for command
```

### Command-Specific Options
```
prepare:
  --feature-name TEXT              Feature name (auto-generated if omitted)
  --skip-context                   Skip context loading
  --force-graph-refresh            Force CodeGraph refresh

context:
  --layer [user|session|repo|all]  Memory layer to display (default: all)

plan:
  [FEATURE_INTENT]                Feature requirement (interactive if omitted)
  --interactive                    Interactive mode

map:
  --symbol TEXT                    Look up symbol definition
  --impact                         Show impact analysis
  --dependencies                   Show symbol dependencies
  --format [ascii|json|markdown]   Output format
  --refresh                        Force CodeGraph refresh

implement:
  --dry-run                        Preview without executing
  --task TEXT                      Execute specific task(s)

post:
  --merge                          Auto-merge feature branch to main

lessons:
  --format [markdown|json]         Output format (default: markdown)
```

## Memory Layer Architecture

### User Layer (`~/.memories/preferences.md`)
- Persistent across all projects
- YAML frontmatter: preferences, skills, patterns
- Loaded on every command

### Session Layer (`.memories/session/`)
- Feature-specific, ephemeral
- Files:
  - `context-loaded.md` - Last loaded context
  - `{feature}-state.yaml` - Feature lifecycle state
  - `decisions.yaml` - Feature-specific decisions
- Cleared when feature archived

### Repo Layer (`.cel/`)
- Persistent per repository
- Contents:
  - `codegraph.db` - SQLite symbol database
  - `features/` - Archived feature states
  - `patterns-index.md` - Reusable patterns

## CodeGraph Queries

```bash
# Display stats
spek map

# Look up symbol
spek map --symbol "UserService"

# Find references to symbol
spek map --symbol "authenticate" --dependencies

# Analyze change impact
spek map --symbol "APIRouter" --impact

# Force re-index
spek map --refresh

# Different output formats
spek map --symbol "Config" --format json
spek map --symbol "Config" --format markdown
```

## Feature State Lifecycle

```
pending     → Just initialized
specify     → Spec created (after plan)
plan        → Plan created
implement   → Tasks being executed
post        → Archiving outcomes
archived    → Feature complete
```

View feature state:
```bash
spek context --layer session
```

## Vault Structure

```
wiki/
├── specs/              # Specifications
│   ├── 010-*.md
│   ├── 100-*.md
│   └── ...
├── lessons/            # Extracted lessons
│   ├── {feature}-lessons.md
│   └── insights-report.md
├── patterns/           # Reusable patterns (via loader)
└── decisions/          # Architectural decisions
```

## Integration Points

### SpecKit Integration
- Requires: `specify` CLI installed
- Install: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- Calls: specify, clarify, plan, analyze, tasks
- Timeout: 300 seconds per command

### CodeGraph
- Backend: SQLite (`.cel/codegraph.db`)
- Indexes: Python AST analysis
- Queries: Symbol lookup, references, impact analysis
- Refresh: Automatic on prepare (if >24hrs), manual via `spek map --refresh`

### Git
- Verification: `git status --porcelain`
- Branching: `feature/{feature-name}`
- Commits: Spec/plan/tasks/lessons artifacts

## Troubleshooting

### SpecKit Not Found
```
Error: SpecKit not found in PATH
Fix: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Git Not Clean
```
Error: Git working directory not clean
Fix: Commit or stash changes before running prepare
```

### No Tasks File
```
Error: No tasks.md found
Fix: Run 'spek plan' first to generate tasks
```

### CodeGraph Stale
```
Warning: CodeGraph is 48 hours old
Fix: Run 'spek map --refresh' or use --force-graph-refresh with prepare
```

## Testing

Run test suite:
```bash
cd /Users/marcelrienks/workspace/code/spekificity
python -m pytest tests/unit/test_cli.py -v

# Override problematic addopts
python -m pytest -o "addopts=" tests/unit/test_cli.py -v
```

Test coverage: 19 passing tests, 100% command coverage

## Development Status

| Component | Status |
|-----------|--------|
| Core CLI Framework | ✅ Complete |
| 7 Commands | ✅ Complete |
| Memory System (3-layer) | ✅ Complete |
| CodeGraph | ✅ Complete |
| Git Integration | ✅ Complete |
| SpecKit Integration | ✅ Complete |
| Test Suite | ✅ 19/19 passing |
| Documentation | ✅ Complete |
| **Phase 4 Overall** | **✅ COMPLETE** |

Next: Phase 5 (CodeGraph MCP Integration)
