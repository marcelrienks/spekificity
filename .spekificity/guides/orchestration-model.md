# Orchestration Model: How Spekificity Coordinates Tools

**Purpose**: Technical reference for how `spek init` orchestrates all tools.

## Orchestration Sequence

### Phase 1: Prerequisites

```bash
Validate system prerequisites:
  ├─ Python 3.11+
  ├─ uv package manager
  ├─ git
  └─ Config file exists
```

### Phase 2: Speckit Orchestration

```bash
orchestrate_specify_init():
  ├─ Check: specify installed globally?
  ├─ Run: specify init .
  │   └─ Creates .specify/ config
  │   └─ Installs speckit skills to .github/agents/
  ├─ Update config: tools.speckit.initialized = true
  └─ Record: orchestration_history (success/failure)
```

### Phase 3: Graphify Setup

```bash
orchestrate_graphify():
  ├─ Check: graphify installed globally?
  ├─ Initialize: graphify for project
  │   └─ Generates project graph
  │   └─ Stores in .obsidian/graph/
  ├─ Update config: tools.graphify.initialized = true
  └─ Record: orchestration_history
```

### Phase 4: Obsidian Vault

```bash
orchestrate_obsidian():
  ├─ Check: Obsidian app installed (optional)?
  ├─ If installed:
  │   └─ Configure vault location (.obsidian/)
  │   └─ Initialize vault structure
  ├─ If not installed:
  │   └─ Skip (non-fatal, optional)
  │   └─ Use fallback JSON storage
  ├─ Update config: tools.obsidian.initialized
  └─ Record: orchestration_history
```

### Phase 5: Caveman Integration

```bash
orchestrate_caveman():
  ├─ Check: caveman skill available in environment?
  ├─ If available:
  │   └─ Mark: tools.caveman.integrated = true
  ├─ If not:
  │   └─ Mark: tools.caveman.available = false
  │   └─ Continue (non-fatal, optional)
  └─ Record: orchestration_history
```

### Phase 6: Skill Installation

```bash
install_spek_skills():
  ├─ Create: .spekificity/skills/
  ├─ Install: spek.context-load.md
  ├─ Install: spek.map-codebase.md
  ├─ Install: spek.lessons-learnt.md
  ├─ Install: [future custom skills]
  ├─ Update config: skills.spekificity_installed = true
  └─ Record: orchestration_history (success)
```

### Phase 7: Workflow & Guide Installation

```bash
install_workflows():
  ├─ Create: .spekificity/workflows/
  ├─ Install: setup-workflow.md
  ├─ Install: init-workflow.md
  ├─ Install: update-workflow.md
  ├─ Install: integration-guide.md
  └─ Record: orchestration_history (success)

install_guides():
  ├─ Create: .spekificity/guides/
  ├─ Install: architecture.md
  ├─ Install: orchestration-model.md
  ├─ Install: skill-development.md
  ├─ Install: troubleshooting.md
  ├─ Install: manual-setup.md
  └─ Install: migration.md
```

### Phase 8: Skill Index Generation

```bash
update_skill_index():
  ├─ Discover: .spekificity/skills/spek.*
  ├─ Discover: .github/agents/speckit.*
  ├─ Check: caveman availability
  ├─ Generate: .spekificity/skill-index.md
  │   └─ Table: all skills with descriptions
  │   └─ Invocation examples
  │   └─ Namespace reference
  └─ Record: skills.last_skill_index_update = now
```

### Phase 9: Finalization

```bash
finalize():
  ├─ Update: spek_initialized = true
  ├─ Update: spek_initialized_timestamp = now
  ├─ Mark step: platform_init (success)
  ├─ Print: summary report
  └─ Exit: code 0 (success)
```

## Error Handling & Recovery

### Non-Fatal Failures (Optional Tools)

```
Obsidian not installed?
  → Skip (non-fatal)
  → Use fallback JSON storage
  → Initialization continues
  → Mark: obsidian.initialized = false

caveman not available?
  → Skip (non-fatal)
  → Project works without caveman mode
  → Mark: caveman.available = false
```

### Fatal Failures (Required Tools)

```
specify not found?
  → ERROR (fatal)
  → Print: installation instructions
  → Halt orchestration
  → Exit: code 1

Python 3.11+ not found?
  → ERROR (fatal)
  → Already caught by setup phase
  → Cannot proceed
```

### Partial Failure Recovery

```
If orchestration interrupted at step N:

1. Detect: orchestration_history shows incomplete steps
2. Identify: Last failed step
3. Provide: Recovery guidance (e.g., "install missing tool, retry")
4. On retry:
   a. Validate: Prerequisites
   b. Skip: Already-completed steps (check config state)
   c. Resume: From failed step
```

## Idempotency Guarantees

### Re-run Behavior

```
First run: Fresh installation
  → Create config (spek_initialized = false)
  → Run all phases
  → Mark: spek_initialized = true

Second run: Already initialized
  → Check: spek_initialized = true
  → Update: State fields (timestamps, versions)
  → Skip: Already-completed tool init (specify already ran)
  → Result: No errors, clean re-run
```

## Tool Integration Contract

Each orchestrated tool must support:

| Tool | Contract |
|------|----------|
| **speckit** | `specify init .` command with no-op on re-run |
| **graphify** | Detect existing vault, update incrementally |
| **obsidian** | Optional; skip if not installed |
| **caveman** | Optional; detect via environment |

## State Transitions

```
NO CONFIG → spek setup
  ↓
CONFIG (not initialized)

CONFIG (not initialized) → spek init
  ↓
Each phase:
  1. Run tool init
  2. Update config
  3. Record history
  ↓
CONFIG (initialized)
  ↓
On re-run: spek init
  ↓
Each phase:
  1. Check state (already done?)
  2. Skip if done
  3. Resume if interrupted
  ↓
CONFIG (initialized)
```

## Configuration State Diagram

```
┌─────────────────┐
│  No config.json │
└────────┬────────┘
         │ spek init
         ▼
┌──────────────────────────┐
│ config.json created      │
│ spek_initialized = false │
└────────┬─────────────────┘
         │ (orchestration phases)
         ▼
┌──────────────────────────┐
│ All phases complete      │
│ spek_initialized = true  │
└────────┬─────────────────┘
         │ spek init again (idempotent)
         ▼
┌──────────────────────────┐
│ State preserved          │
│ Timestamps updated       │
│ spek_initialized = true  │
└──────────────────────────┘
```

---

**Key Principle**: Orchestration is **transparent** — each tool remains independently usable. Users can run `specify`, `graphify` directly if needed, but recommended primary path is through `spek` commands.
