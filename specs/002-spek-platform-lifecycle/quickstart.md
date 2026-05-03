# Spekificity Quickstart — 5-Minute Setup

**Goal**: Get spekificity running in your project in 5 minutes.

## Prerequisites

- macOS or Linux (Windows: WSL recommended)
- Python 3.11+
- Terminal/shell access

## Step 1: Run Setup (2 min)

```bash
cd /path/to/your/project
.spekificity/bin/spek setup
```

**Expected output**:
```
═══════════════════════════════════
 Spekificity Platform Setup
═══════════════════════════════════
ℹ Spekificity v1.0.0 — Unified orchestration platform

[spekificity] Detecting platform...
✓ Platform detected: macOS

[spekificity] Checking Python...
  ✓ Python      installed         3.11.6

[spekificity] Checking uv...
  ✓ uv          installed         0.1.25

[spekificity] Checking git...
  ✓ git         installed         2.43.0

✓ Setup complete
```

**If setup fails**, see Troubleshooting below.

## Step 2: Run Init (2 min)

```bash
.spekificity/bin/spek init
```

**Expected output**:
```
═══════════════════════════════════
 Spekificity Platform Initialization
═══════════════════════════════════
ℹ Spekificity v1.0.0 — Unified orchestration platform

[speckit] Initializing specify (speckit)...
✓ speckit initialized

[graphify] Initializing graphify for project analysis...
✓ graphify initialized

[obsidian] Initializing Obsidian vault (optional)...
⚠ Warning: Obsidian not installed (optional). Graph will use fallback storage.

[caveman] Checking for caveman skill integration...
ℹ caveman skill not available (optional)

[spekificity] Installing custom skills...
✓ Custom skills installed

═══════════════════════════════════
 Initialization Complete
═══════════════════════════════════
✓ All tools initialized:
  • speckit/specify ✓
  • graphify ✓
  • Obsidian (optional)
  • caveman (optional)
  • Custom skills ✓
  • Workflows ✓
  • Guides ✓

Available commands:
  /spek.context-load     — Load vault context
  /spek.map-codebase     — Run codebase mapping
  /speckit.specify       — Create feature spec
  /speckit.plan          — Create implementation plan

Next steps:
  1. Read: .spekificity/guides/architecture.md
  2. Start feature work: /context-load
  3. For updates: spek update

✓ Initialization complete
```

## Step 3: Verify Installation (1 min)

```bash
.spekificity/bin/spek status
```

**Expected output**:
```
═══════════════════════════════════
 Spekificity Platform Status
═══════════════════════════════════
Version: 1.0.0
Branch: 002-spek-platform-lifecycle
Initialized: true
Initialized at: 2026-05-03T15:30:00Z

═══════════════════════════════════
 Tool Integration
═══════════════════════════════════
speckit/specify:
  Installed: true (0.1.0)
  Initialized: true

graphify:
  Installed: true (1.0.0)
  Initialized: true

Obsidian (optional):
  Installed: false
  Initialized: false

caveman (optional):
  Available: false
  Integrated: false

═══════════════════════════════════
 Installed Skills
═══════════════════════════════════
Spekificity custom skills: true
Speckit skills: true
Caveman skills: false

Available skills:
  See: .spekificity/skill-index.md
  Total skills registered: 6 (approx)

✓ Status check complete
```

## Step 4: Start Your First Feature

In your AI chat (GitHub Copilot or Claude Code):

```
/context-load
```

This loads your vault context and primes the AI with your codebase map.

Then:

```
/speckit-enrich-specify

Create a feature for: [your feature description]
```

This starts your feature workflow.

## Next Steps

- **Learn the platform**: Read `.spekificity/guides/architecture.md`
- **Detailed workflow**: See `.spekificity/workflows/feature-lifecycle.md`
- **Troubleshooting**: See `.spekificity/guides/troubleshooting.md`
- **Developer guide**: See `.spekificity/guides/skill-development.md`

## Common Issues

| Issue | Solution |
|-------|----------|
| `specify not found` | Run: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` |
| `graphify not found` | Run: `uv tool install graphifyy` |
| `Python 3.11+ not found` | macOS: `brew install python@3.11` |
| Permission denied on setup script | Run: `chmod +x .spekificity/setup-scripts/*.sh .spekificity/bin/spek` |

For more help, see Troubleshooting section.

---

**✅ You're ready!** Run your first feature workflow with `/context-load` → `/speckit-enrich-specify`.
