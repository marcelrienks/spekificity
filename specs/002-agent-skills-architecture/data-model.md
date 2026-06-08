# Data Model: Agent Skills Architecture

**Purpose**: Define entities, relationships, and data structures for agent skill registration, context injection, and workflow execution.

---

## Core Entities

### 1. Agent Skill Definition

**Entity**: `AgentSkill`

**Fields**:
- `name: string` — Unique skill identifier (dash-separated, e.g., `spek-prepare`)
- `display_name: string` — Human-readable name (e.g., "Prepare for Feature Development")
- `purpose: string` — One-line purpose statement
- `usage: string` — Command syntax with arguments and flags
- `workflow_steps: List[WorkflowStep]` — Ordered list of execution steps
- `output_artifacts: List[string]` — Files or data produced by skill
- `documentation_link: string` — Link to full skill documentation (wiki/skills.md section)
- `required_context: List[ContextType]` — What context must be loaded (vault, code-index, constitution)
- `handlers: Dict[str, Handler]` — Input handlers and validators

**Validation Rules**:
- `name` matches pattern: `^[a-z]+-[a-z]+(-[a-z]+)*$` (kebab-case)
- `name` is globally unique within `.claude/skills/`
- `workflow_steps` is non-empty
- `required_context` is subset of {vault, code-index, constitution}

**State Transitions**:
- Created → Registered (skill file written to `.claude/skills/`)
- Registered → Active (skill discoverable by Claude Code)
- Active → Invoked (user runs `/spek.name`)
- Invoked → Executing (context loaded, workflow starts)
- Executing → Complete (artifacts generated, decisions logged)

---

### 2. Workflow Step

**Entity**: `WorkflowStep`

**Fields**:
- `name: string` — Step name (e.g., "Load Vault Context")
- `action: string` — What the step does (narrative description)
- `inputs: List[string]` — What data this step needs
- `outputs: List[string]` — What data this step produces
- `handlers: List[Handler]` — Input validation and prompts
- `error_recovery: string` — How to handle step failure
- `checkpoint: bool` — Whether step is a persistent checkpoint

**Validation Rules**:
- `name` is non-empty, descriptive
- `inputs` and `outputs` are non-empty
- `checkpoint=true` only for steps that persist to vault

---

### 3. Context

**Entity**: `ProjectContext`

**Fields**:
- `vault: Vault` — Loaded vault (decisions, patterns, lessons)
- `code_index: CodeIndex` — Loaded code graph (lat.md index)
- `constitution: Constitution` — Project constitution and principles
- `cwd: string` — Current working directory
- `metadata: Dict[string, Any]` — Additional context (branch, user, timestamp)

**Relationships**:
- Each agent skill loads its `required_context` before execution
- Context is formatted and injected into agent prompt
- Decisions made during execution are logged back to `vault.decisions`

**Validation Rules**:
- `vault` must exist (created by `spek init`)
- `code_index` must be synchronized with current codebase (via `/lat.sync`)
- `constitution` must be valid YAML with required sections
- `cwd` must be git repository root

---

### 4. CLI Command (Minimalist)

**Entity**: `CLICommand`

**Fields**:
- `name: string` — Command name (e.g., `init`, `prepare`)
- `arg_parser: ArgumentParser` — Click argument/option definitions
- `handler: Callable` — Function to execute
- `deprecated: bool` — Whether command is deprecated/redirects
- `redirect_message: string` — Message to show if deprecated

**Validation Rules**:
- `name` is lowercase, single-word
- Active (non-deprecated) commands must have valid `handler`
- Deprecated commands must have non-empty `redirect_message`

**State Transitions**:
- Active → Deprecated (e.g., `spek plan` redirects to `/spek.plan`)
- Deprecated → Removed (after migration period)

---

### 5. Decision Log Entry

**Entity**: `Decision`

**Fields**:
- `title: string` — Decision title (e.g., "Use agent skills for workflow commands")
- `status: enum` — {proposed, approved, implemented, superseded}
- `context: string` — What problem this decision addresses
- `rationale: string` — Why this choice was made
- `alternatives: List[string]` — What was considered but rejected
- `timestamp: ISO8601` — When decision was made
- `author: string` — Who made the decision
- `related_artifact: string` — Link to spec/plan/code that implements it
- `tags: List[string]` — Keywords for querying (e.g., architecture, agent-skills)

**Relationships**:
- Each decision is logged to `vault/decisions.md` by agent skill
- Decisions are queried by `/spek.prepare` for context injection
- Decisions inform `/spek.plan` for design decisions

---

## Relationships & Workflows

### Relationship 1: Agent Skill → Context → Workflow

```
Agent Skill (e.g., /spek.plan)
  ↓
Load Required Context
  ├─ Vault (decisions, patterns, lessons)
  ├─ Code Index (via lat.md)
  └─ Constitution (principles)
  ↓
Format Context for Agent Prompt
  ↓
Execute Workflow Steps
  ├─ Step 1: Load context
  ├─ Step 2: User interaction/confirmation
  ├─ Step 3: SpecKit command (specify, plan, tasks)
  ├─ Step 4: Log decisions to vault
  └─ Step 5: Output artifacts
  ↓
Persist Context Updates
  ├─ Write to vault (decisions, patterns)
  └─ Update code index (if code changed)
```

### Relationship 2: CLI Command → Agent Skill

```
User runs: spek plan "feature description"
  ↓
CLI checks: Is this an agent skill?
  ├─ If YES: Error message → "/spek.plan" invocation
  └─ If NO (init): Execute normally
  ↓
Error Message:
  "Error: 'spek plan' requires Claude Code agent context. Use agent skill:
   /spek.plan [feature-name]"
```

### Relationship 3: Decision Persistence

```
Agent Skill Workflow
  ↓
During execution: User makes design decisions
  ↓
Agent captures: @decision "..." or equivalent
  ↓
Decision Parser:
  ├─ Extract decision text
  ├─ Create Decision entity
  └─ Append to vault/decisions.md
  ↓
Future /spek.prepare:
  ├─ Loads vault/decisions.md
  ├─ Queries relevant decisions
  └─ Injects into context for new features
```

---

## Data Structures

### AgentSkill Definition (YAML format)

```yaml
name: spek-plan
display_name: "Generate Specification & Implementation Plan"
purpose: "Convert feature description into spec, plan, and task breakdown with interactive clarification"
usage: "/spek.plan [feature-name|spec-file]"

workflow_steps:
  - name: "Load Vault Context"
    action: "Load decisions, patterns, lessons from vault/"
    inputs: [vault_path]
    outputs: [decisions, patterns, lessons]
    checkpoint: false
    
  - name: "Run Specification Phase"
    action: "Execute speckit.specify with context enrichment"
    inputs: [feature_intent, vault_context]
    outputs: [spec.md, clarification_questions]
    checkpoint: true
    
  - name: "Interactive Clarification"
    action: "Ask user to clarify ambiguities, collect answers"
    inputs: [clarification_questions]
    outputs: [clarified_spec]
    checkpoint: true
    handlers:
      - type: prompt
        text: "Does this interpretation match your intent?"
      - type: validator
        rule: "Spec must include success criteria"

output_artifacts:
  - specs/{feature}/spec.md
  - specs/{feature}/plan.md
  - specs/{feature}/tasks.md

required_context:
  - vault
  - code-index
  - constitution

documentation_link: "wiki/skills.md#spek.plan"
```

### CLI Command Definition (Python Click)

```python
@cli.command(short_help="Initialize project")
@click.pass_context
def init(ctx):
    """Initialize Spekificity in current project."""
    # Handler implementation
```

### Context Structure (Python dataclass)

```python
@dataclass
class ProjectContext:
    vault: Vault
    code_index: CodeIndex
    constitution: Constitution
    cwd: Path
    metadata: Dict[str, Any]
```

---

## Validation Rules

### Agent Skill Validation
- ✓ Skill file exists in `.claude/skills/{name}.md`
- ✓ Skill name matches kebab-case pattern
- ✓ Skill name is globally unique
- ✓ `workflow_steps` is non-empty
- ✓ Each step has inputs and outputs
- ✓ `required_context` is valid subset

### CLI Command Validation
- ✓ Command name is lowercase single-word
- ✓ Active commands have valid handler
- ✓ Deprecated commands have redirect message
- ✓ No command name conflicts

### Context Validation
- ✓ Vault exists and is readable
- ✓ Code index is recent (synced within last session)
- ✓ Constitution file is valid YAML
- ✓ CWD is git repository root

### Decision Validation
- ✓ Title is non-empty
- ✓ Status is valid enum value
- ✓ Timestamp is ISO8601
- ✓ At least one tag is provided

---

## Summary

The agent skills architecture defines:
1. **Agent Skills**: Registered skill definitions in `.claude/skills/`, each with workflow steps and context requirements
2. **Context**: Project vault, code index, and constitution loaded before skill execution
3. **CLI Commands**: Minimal set (init only); others deprecated with helpful redirect messages
4. **Decisions**: Captured during agent skill execution, persisted to vault for future context loading
5. **Relationships**: Clear data flow from context loading → skill execution → decision persistence

All entities follow validation rules to ensure consistency, discoverability, and reproducibility.
