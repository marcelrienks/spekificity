# Context Flow Architecture

**Purpose**: Document the complete data flow from project vault through agent skills to user interaction and back to persistent storage.

---

## High-Level Flow

```
Project Vault (vault/, .spek/)
    ↓
Context Loading (vault.py, lat_md.py, constitution)
    ↓
Context Formatting (context.py, compression.py)
    ↓
Agent Skill Execution (/spek.* skill prompt injection)
    ↓
User Interaction (clarification, approval, implementation)
    ↓
Decision Capture (during skill execution)
    ↓
Vault Persistence (vault/ updates)
    ↓
[Back to top for next feature]
```

---

## Detailed Stage Breakdown

### Stage 1: Context Discovery

**Responsibility**: Discover what context is available in the project.

**Components**:
- `vault/decisions.md` — Architectural decisions made to date
- `vault/patterns.md` — Design patterns applied in project
- `vault/lessons/{date}-{feature}.md` — Lessons learned from past features
- `lat.md` (in project root) — Code graph index (symbol table, file map, dependencies)
- `.specify/memory/constitution.md` — Project principles and governance

**Discovery Method**:
```python
# Pseudo-code
def discover_context():
    vault_path = project_root / "vault"
    
    decisions_file = vault_path / "decisions.md"
    patterns_file = vault_path / "patterns.md"
    lessons_dir = vault_path / "lessons"
    
    index_file = project_root / "lat.md"
    constitution_file = project_root / ".specify/memory/constitution.md"
    
    return {
        "vault_exists": vault_path.exists(),
        "decisions": decisions_file.exists(),
        "patterns": patterns_file.exists(),
        "lessons": list(lessons_dir.glob("*.md")) if lessons_dir.exists() else [],
        "code_index": index_file.exists(),
        "constitution": constitution_file.exists(),
    }
```

**Validation**:
- ✓ vault/ directory exists (created by `spek init`)
- ✓ decisions.md and patterns.md readable
- ✓ constitution.md is valid YAML
- ⚠ code_index (lat.md) optional; graceful degradation if missing

---

### Stage 2: Context Loading

**Responsibility**: Read and parse discovered context files into memory structures.

**Components**:

#### 2a. Vault Loading
```python
# In spekificity/core/vault.py

class Vault:
    def load_decisions(self) -> List[Decision]:
        # Read vault/decisions.md
        # Parse YAML frontmatter or Markdown sections
        # Return list of Decision objects
        
    def load_patterns(self) -> List[Pattern]:
        # Read vault/patterns.md
        # Parse patterns with examples
        # Return list of Pattern objects
        
    def load_lessons(self, limit=5) -> List[Lesson]:
        # List files in vault/lessons/
        # Load most recent (limit) lesson files
        # Return list of Lesson objects
```

**Sample Output**:
```python
decisions = [
    Decision(
        title="Use agent skills instead of pure CLI commands",
        context="Interactive workflows require user confirmation loops",
        rationale="Pure CLI cannot implement interactive workflows",
        tags=["architecture", "agent-skills"]
    ),
    Decision(
        title="Vault stores decisions, patterns, lessons",
        context="Need persistent project knowledge",
        rationale="Avoid repeating design decisions in future features",
        tags=["architecture", "vault"]
    ),
]

patterns = [
    Pattern(
        name="Context Injection",
        description="Load project context before executing agent workflow",
        applies_to=["agent-skills"],
        examples=["vault loading", "code-index querying"]
    ),
]
```

#### 2b. Code Index Loading
```python
# In spekificity/integrations/lat_md.py

class CodeIndex:
    def load(self, project_root: str) -> "CodeIndex":
        # Read lat.md file
        # Parse symbol table, file map, dependencies
        # Return index ready for queries
        
    def query(self, intent: str, max_results=10) -> List[CodeReference]:
        # BM25 search for intent in code graph
        # Return matching files, functions, classes
        # Include line numbers and relevance scores
```

**Sample Output**:
```
Relevant Files for "authentication":
- spekificity/cli/main.py (lines 1-100) - CLI entry point
- spekificity/core/vault.py (lines 50-150) - Vault context loading
- spekificity/core/context.py (lines 200-250) - Context formatting

Functions/Classes:
- ContextLoader.load_vault() - Load vault context
- Vault.load_decisions() - Get decisions from vault
```

#### 2c. Constitution Loading
```python
# In project setup; read from .specify/memory/constitution.md

constitution = {
    "purpose": "Spekificity is a toolkit and workflow system...",
    "principles": {
        "I. Deterministic Workflows": "...",
        "II. Persistent Knowledge": "...",
        "III. Spec-First Quality": "...",
        "IV. Context Efficiency": "...",
        "V. Simple, Composable Tooling": "...",
    },
    "constraints": {
        "Dual-Instance Clarity": "...",
        "Tool Integration & Composition": "...",
    },
    "version": "1.1.0",
}
```

---

### Stage 3: Context Filtering

**Responsibility**: Filter loaded context to what's relevant for the current task.

**Components**:

#### 3a. Semantic Relevance Filtering
```python
# Query: Filter decisions, patterns, lessons by relevance to feature intent

def filter_context_for_feature(
    intent: str,
    decisions: List[Decision],
    patterns: List[Pattern],
    lessons: List[Lesson],
) -> Dict[str, List]:
    # BM25 search of intent against decision titles/tags
    relevant_decisions = semantic_search(intent, decisions, top_k=3)
    
    # Find patterns relevant to feature domain
    relevant_patterns = semantic_search(intent, patterns, top_k=3)
    
    # Find lessons from related features
    relevant_lessons = semantic_search(intent, lessons, top_k=2)
    
    return {
        "decisions": relevant_decisions,
        "patterns": relevant_patterns,
        "lessons": relevant_lessons,
    }
```

#### 3b. Code Impact Filtering
```python
# Query: What code sections are relevant to this feature?

def filter_code_for_feature(
    intent: str,
    code_index: CodeIndex,
) -> List[CodeReference]:
    # BM25 search for intent in code graph
    # Return files, functions, classes that match intent
    # Prioritize by relevance score
    
    return code_index.query(intent, max_results=10)
```

**Sample Output**:
```
Filtered Context for "Add authentication":

Related Decisions:
1. "Use agent skills for interactive workflows" (relevance: 0.85)
2. "Vault stores architectural decisions" (relevance: 0.72)

Related Patterns:
1. "Context Injection Pattern" (usage: 5 times in codebase)
2. "Decorator Pattern for agent skills" (usage: 3 times)

Related Lessons:
1. "2026-06-07-complete-framework: Phase 4 - Agent skills registration"
   (Lesson: Keep agent skills stateless; context is injected, not stored)

Relevant Code Files:
1. spekificity/cli/main.py (CLI router, skill registration)
2. spekificity/core/vault.py (context loading)
3. spekificity/core/context.py (context formatting)
```

---

### Stage 4: Context Formatting

**Responsibility**: Format filtered context into human-readable, prompt-optimized text.

**Components**:

#### 4a. Text Formatting
```python
# In spekificity/core/context.py

class ContextFormatter:
    def format_decisions(self, decisions: List[Decision]) -> str:
        # Format as Markdown list with title, rationale, tags
        text = "## Prior Decisions\n\n"
        for d in decisions:
            text += f"- **{d.title}**\n"
            text += f"  Rationale: {d.rationale}\n"
            text += f"  Tags: {', '.join(d.tags)}\n\n"
        return text
    
    def format_patterns(self, patterns: List[Pattern]) -> str:
        # Format as Markdown sections with examples
        ...
    
    def format_code(self, references: List[CodeReference]) -> str:
        # Format as file list with line numbers
        ...
```

**Sample Output**:
```markdown
## Prior Decisions

- **Use agent skills instead of CLI commands**
  Rationale: Interactive workflows require user confirmation loops
  Tags: architecture, agent-skills
  
- **Vault stores architectural decisions**
  Rationale: Avoid repeating design decisions across features
  Tags: architecture, vault

## Related Patterns

- **Context Injection Pattern**: Load project context before agent workflow
- **Decorator Pattern**: Wrap SpecKit without rebuilding

## Relevant Code Files

- spekificity/cli/main.py (lines 1-100)
  Purpose: CLI router and command entry points
  
- spekificity/core/vault.py (lines 50-150)
  Purpose: Vault context loading and persistence

## Constitution Highlights

- **Principle I (Deterministic Workflows)**: Work follows spec → plan → implement → conclude sequence
- **Principle III (Spec-First Quality)**: Implementation preceded by written specification
- **Principle IV (Context Efficiency)**: Use indexed context (lat.md) over broad code scans
```

#### 4b. Compression (Caveman Mode)
```python
# In spekificity/core/compression.py

class CavemanCompressor:
    def compress(self, text: str, intensity: str) -> str:
        # intensity: "lite", "full", "ultra"
        
        if intensity == "lite":
            # Remove explanations, keep structure
            # ~30% token reduction
        elif intensity == "full":
            # Abbreviate terms, terse formatting
            # ~60% token reduction
        elif intensity == "ultra":
            # Minimal prose, lossy compression
            # ~80% token reduction
        
        return compressed_text
```

**Sample Output (caveman mode: full)**:
```
## Prior Decisions
- Agent skills (not CLI) — interactive workflows need confirmation loops
- Vault stores decisions — avoid repeating design trade-offs

## Patterns
- Context Injection: load vault before agent workflow
- Decorator: wrap SpecKit, don't rebuild

## Code
- cli/main.py (1-100): CLI router
- core/vault.py (50-150): Context loading

## Constitution
- I. Deterministic Workflows: spec → plan → implement → conclude
- III. Spec-First: written spec before code
- IV. Context Efficiency: indexed context over broad scans
```

---

### Stage 5: Context Injection

**Responsibility**: Inject formatted context into agent skill prompt.

**Components**:

```python
# In agent skill prompt (pseudo-code)

AGENT_SKILL_PROMPT = """
{SKILL_PURPOSE_AND_WORKFLOW}

## Project Context

{FORMATTED_CONTEXT}

## User Input

{USER_INTENT}

## Task

Execute the workflow steps above with the provided context.
When you make design decisions, capture them as @decision "[title]" — [rationale].
Log decisions to vault at the end.
"""
```

**Injection Points**:
1. **Vault Context** — What prior decisions should inform this workflow?
2. **Code Context** — What files/functions are relevant?
3. **Pattern Context** — What patterns have worked before?
4. **Constitutional Context** — What principles govern decisions?

**Example Prompt**:
```
You are executing /spek.plan to convert a feature description into spec + plan + tasks.

## Project Context

Prior Decisions:
- Agent skills (not CLI) for interactive workflows
- Vault stores decisions, patterns, lessons
- Context Efficiency: use indexed context, not broad scans

Relevant Code:
- spekificity/cli/main.py — Where CLI commands are registered
- spekificity/core/vault.py — How to load prior decisions
- spekificity/core/context.py — How to format context

Patterns:
- Context Injection: load vault before execution
- Decorator: wrap SpecKit command runners

Constitution (Key Principles):
- I. Deterministic Workflows: spec → plan → implement → conclude
- III. Spec-First Quality: written spec before implementation

## User Input

Feature: "Implement agent skills architecture fix"

Description: Fix architectural mismatch between intended agent skills 
(documented in wiki) and current CLI implementation (incomplete stubs).

## Task

1. Load vault context (decisions, patterns)
2. Run /speckit.specify to generate feature spec
3. Ask user for clarification on ambiguities
4. Run /speckit.plan to generate implementation plan
5. Run /speckit.tasks to break down into tasks
6. Present spec + plan + tasks for user review
7. Log planning decisions to vault/decisions.md

When you make design decisions, capture them as:
@decision "Decision Title" — Rationale for choice
```

---

### Stage 6: Workflow Execution

**Responsibility**: Execute the agent skill workflow with injected context.

**Components**:
- User interaction (confirmation, clarification, approval)
- SpecKit command execution (specify, plan, tasks, analyze)
- Decision capture (decisions made during workflow)
- Error handling (graceful degradation, helpful messages)
- Progress tracking (step-by-step logging)

**Decision Capture**:
```python
# During workflow execution

decisions_captured = []

while executing_workflow:
    # Execute workflow step
    step_result = execute_step(step)
    
    # If user made a decision, capture it
    if "@decision" in step_result or user_confirmed_choice:
        decision = parse_decision(step_result)
        decisions_captured.append(decision)
    
    # Ask for approval to continue
    approval = ask_user("Is this correct? (y/n)")
    
    if not approval:
        remediate_step()
```

---

### Stage 7: Decision Persistence

**Responsibility**: Write captured decisions back to vault for future use.

**Components**:

#### 7a. Decision Formatting
```python
# Format captured decision into vault entry format

decision_entry = """
## Decision: Use agent skills instead of pure CLI commands

**Status**: Implemented | **Date**: 2026-06-08 | **Author**: Claude Code

**Context**: 
Interactive workflows require user confirmation loops and state management 
that pure CLI commands cannot provide.

**Rationale**: 
Agent skills execute in Claude Code context where user interaction is natural
and state can be maintained across workflow steps.

**Alternatives Considered**:
- Rebuild CLI commands to be fully interactive (complex; duplicates SpecKit logic)
- Create separate "agent wrapper" CLI command (adds confusion about invocation)

**Tags**: architecture, agent-skills, workflow

**Artifacts**: 
- specs/002-agent-skills-architecture/spec.md
- specs/002-agent-skills-architecture/plan.md
"""
```

#### 7b. Vault Append
```python
# In spekificity/core/vault.py

class Vault:
    def append_decision(self, decision: Decision):
        # Read existing vault/decisions.md
        existing = self.load_decisions()
        
        # Append new decision
        existing.append(decision)
        
        # Write back to vault/decisions.md
        self.write_decisions(existing)
        
        # Log to progress/history
        log_to_progress(f"Decision appended: {decision.title}")
```

---

### Stage 8: Context Update

**Responsibility**: Refresh code index and project state for next feature.

**Components**:

#### 8a. Code Index Sync
```python
# Run /lat.sync to refresh code graph

def sync_code_index(project_root: str):
    # Detect file changes since last sync
    index = load_index(project_root)
    
    # Update incrementally (not full rebuild)
    index.sync_incremental()
    
    # Validate graph integrity
    index.validate()
    
    # Report coverage
    coverage = index.get_coverage_report()
    
    return {
        "files_added": coverage["added"],
        "files_modified": coverage["modified"],
        "files_removed": coverage["removed"],
        "total_nodes": coverage["total_nodes"],
        "total_edges": coverage["total_edges"],
    }
```

#### 8b. Memory Sync
```python
# Sync `.spek/memory/` with latest decisions, patterns, lessons

def sync_repo_memory(project_root: str):
    vault = load_vault(project_root / "vault")
    memory = project_root / ".spek" / "memory"
    
    # Sync decisions
    memory.write("decisions-index.md", vault.load_decisions())
    
    # Sync patterns
    memory.write("patterns-index.md", vault.load_patterns())
    
    # Sync lessons (last 10)
    memory.write("lessons-index.md", vault.load_lessons(limit=10))
    
    log_to_progress("Repository memory synced")
```

---

## Complete Flow Example

### Feature: Implement Agent Skills Architecture Fix

```
1. User runs: /spek.prepare "Agent skills architecture"
   ↓
2. Agent skill loads context:
   - vault/decisions.md → 15 prior decisions
   - vault/patterns.md → 8 design patterns
   - vault/lessons/ → 5 recent lessons
   - lat.md → Code index (500+ symbols)
   - constitution.md → Project principles
   ↓
3. Context filtering:
   - Semantic search for "agent skills" → 3 relevant decisions
   - Semantic search for "architecture" → 2 relevant patterns
   - Semantic search for "workflow" → 1 relevant lesson
   - Code query for "agent skills" → 10 relevant files
   ↓
4. Context formatting:
   - Format decisions as Markdown list
   - Format patterns with examples
   - Format code files with line ranges
   - Include constitution highlights
   ↓
5. Caveman compression (if enabled):
   - Abbreviate, remove explanations
   - ~60% token reduction
   ↓
6. Inject into agent prompt:
   /spek.prepare [feature-name]
   
   Project Context:
   - Prior decisions (3 most relevant)
   - Design patterns (2 most relevant)
   - Code files (10 most relevant)
   - Constitution highlights (5 key principles)
   
   User Input:
   "Agent skills architecture"
   ↓
7. Agent executes workflow:
   - Load vault context ✓
   - Format onboarding summary ✓
   - Display prior decisions ✓
   - Display relevant patterns ✓
   - Display code files ✓
   - Suggest next step: /spek.plan ✓
   ↓
8. No decisions captured (preparation is passive)
   ↓
9. User runs: /spek.plan "Agent skills architecture"
   ↓
10. Similar context loading for planning phase
    + Decisions captured during spec clarification
    + Decisions logged to vault/decisions.md
    ↓
11. User runs: /spek.implement
    ↓
12. Similar context loading for implementation phase
    + More decisions captured
    + Code changes committed with spec linkage
    ↓
13. User runs: /spek.conclude --dry-run
    ↓
14. Analysis phase:
    - Compare success criteria vs outcomes
    - Identify lessons learned
    ↓
15. Lessons extraction:
    - "Agent skills reduce complexity vs CLI stubs"
    - "Context injection improves relevance of suggestions"
    ↓
16. Vault updates:
    - Archive spec/plan/tasks to vault/archive/2026-06-08-agent-skills/
    - Write lessons to vault/lessons/2026-06-08-agent-skills-arch.md
    - Update vault/patterns.md with new patterns
    - Append new decisions to vault/decisions.md
    ↓
17. Memory sync:
    - Sync .spek/memory/ with latest vault state
    - Run /lat.sync to refresh code index
    ↓
18. [Ready for next feature; repeat from step 1]
```

---

## Summary

Context flows from persistent vault storage → through agent skill loading/filtering/formatting → into agent prompt injection → through user interaction → back to vault persistence → ready for next feature's context loading.

Each stage is designed to be:
- **Efficient**: Minimal context loaded (filtered by relevance)
- **Composable**: Each stage can be tested independently
- **Deterministic**: Same input always produces same context
- **Graceful**: Failures in optional stages (code-index) don't block workflow

This flow ensures that knowledge compounds over time and future features benefit from past decisions without repeating analysis.
