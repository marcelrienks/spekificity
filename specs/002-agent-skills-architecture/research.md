# Research Phase: Agent Skills Architecture

**Purpose**: Resolve design decisions for agent skill architecture, CLI graceful degradation, and CLAUDE.md update strategy.

## Research Questions & Findings

### 1. Agent Skill Registration Format

**Question**: How should agent skills be registered in Claude Code environment?

**Research**: Consulted `wiki/skills.md` (intended design) and `.claude/skills/speckit-plan` (existing agent skill example).

**Finding**: 
Agent skills in Claude Code are registered as markdown files in `.claude/skills/` directory. Each skill definition includes:
- Skill name (dash-separated, e.g., `spek-prepare`)
- Purpose (one-line description)
- Usage (command syntax with args/flags)
- What it does (detailed workflow steps)
- Output artifacts
- Reference to documentation

**Decision**: 
- Create 4 agent skill definition files: `spek-prepare.md`, `spek-plan.md`, `spek-implement.md`, `spek-conclude.md`
- Each follows format from `wiki/skills.md` section (lines 19-195)
- Skills are invoked as `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude` (slashes used in Claude Code)
- When called from CLI context, users see error message directing them to agent skill invocation

**Rationale**: Aligns implementation with intended design; consistent with existing agent skill patterns in Spekificity.

---

### 2. CLI Graceful Degradation Strategy

**Question**: What should happen if users run `spek prepare/plan/implement/conclude` from pure CLI without agent context?

**Research**: Checked current CLI implementation (main.py) — commands exist but are incomplete stubs. Error handling currently silent-fails or prints partial output.

**Finding**:
Current behavior: 
- `spek prepare`: Loads vault, prints onboarding (incomplete; missing agent interaction)
- `spek plan`: Runs SpecKit (incomplete; missing clarification loops, remediation)
- `spek implement`: Prints "Agent session started" but doesn't (misleading)
- `spek conclude`: Prints state changes but doesn't analyze (incomplete)

**Decision**:
Keep `spek prepare` as CLI fallback (basic context loading is useful standalone).
Replace other three (`spek plan`, `spek implement`, `spek conclude`) with error messages directing users to agent skills:
```
Error: 'spek plan' requires Claude Code agent context. Use agent skill instead:
  /spek.plan [feature-name]
For more: https://github.com/user/spekificity/wiki/skills.md
```

**Rationale**: 
- Prevents misleading "Agent session started" message
- Directs users to the correct, working invocation method
- Preserves useful CLI fallback (`spek prepare` for quick context load)
- Reduces maintenance burden (no need to keep partial CLI implementations in sync with agent skills)

---

### 3. CLAUDE.md Update Strategy

**Question**: How to update CLAUDE.md without breaking existing references or losing context?

**Research**: Read current CLAUDE.md; checked 001-complete-framework spec/plan/tasks references.

**Finding**:
Current CLAUDE.md includes:
- Summary section with 5 CLI commands listed (lines 9-10)
- Usage section (lines 18-20) with `spek` commands
- Phase 4-5 completion claims about "agent skills registered"

Changes needed:
- Clarify: `spek init` is CLI; others are agent skills
- Update Usage section to show `/spek.*` syntax
- Update Summary to reflect agent skill approach
- Add section on how agent skills are invoked (with examples)
- Link to new agent skill definitions in `.claude/skills/`

**Decision**:
Update CLAUDE.md with:
1. Revised Summary section clarifying CLI vs agent skills
2. Updated Usage section with `/spek.*` invocation notation
3. New "Agent Skills Invocation" section with examples
4. Cross-references to agent skill definition files
5. Keep existing references to vault, context, compression (still valid)
6. Note that Phase 4 completion means "skills designed"; this feature implements them

**Rationale**:
- Minimal changes to preserve existing context and references
- Clear, visible distinction between CLI and agent skills
- Serves as single source of truth for agent context
- Allows future readers to quickly understand architecture

---

### 4. Agent Skill Context Injection Mechanism

**Question**: How do agent skills inject context (vault, lat.md, constitution) into the workflow?

**Research**: Reviewed `spekificity/core/context.py`, `spekificity/core/vault.py`, `wiki/architecture.md` (context-loading section).

**Finding**:
Existing context loading infrastructure:
- `vault.py`: Load decisions, patterns, lessons from `vault/` directory
- `context.py`: Format loaded context into prompt-ready text
- `lat_md.py`: Index code and query relevant files/symbols
- `compression.py`: Caveman mode compression for context

Each agent skill should:
1. Call `load_vault()` to load decisions, patterns, lessons
2. Call `load_index()` and `query_relevant_context()` for code intelligence
3. Load `constitution.md` for principle references
4. Format context via `ContextLoader`
5. Compress if caveman mode enabled
6. Inject context into agent prompt before workflow execution

**Decision**:
Agent skills will follow this pattern:
```python
# In agent skill prompt/execution:
1. Load vault context (via Python wrapper or agent instruction)
2. Load code index (via lat.md query)
3. Format context for agent
4. Execute workflow with context injected
5. Persist decisions to vault (post-workflow)
```

**Rationale**:
Leverages existing infrastructure; no new modules needed. Keeps context flow deterministic and testable.

---

### 5. Testing & Validation Strategy

**Question**: How to validate that agent skills work correctly without full integration testing?

**Research**: Checked existing test structure in `tests/` and agent skill invocation patterns.

**Finding**:
- Unit tests exist for vault, context, speckit_wrapper modules
- Agent skill invocation testing requires Claude Code environment
- Validation can be done via quickstart scenarios in `quickstart.md`

**Decision**:
- Unit tests: Existing tests for vault/context/index modules remain unchanged
- Integration tests: Agent skill invocation tests in `tests/agent_skills/` (new)
- Validation: Quickstart guide documents end-to-end scenarios
  - Scenario 1: `spek init` → vault created
  - Scenario 2: `/spek.prepare` → context loaded and displayed
  - Scenario 3: `/spek.plan` → spec/plan/tasks generated
  - Scenario 4: CLI error message for `spek plan` directs to `/spek.plan`

**Rationale**:
Ensures both CLI and agent skill paths are testable. Quickstart provides human-readable validation without requiring full test automation.

---

## Summary of Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| `/spek.*` agent skills in `.claude/skills/` | Aligns with Claude Code registration pattern | New files: 4 agent skill definitions |
| Keep `spek prepare` as CLI fallback; error on `spek plan/implement/conclude` | Prevents misleading output; directs users correctly | Modified: `spek plan/implement/conclude` commands in main.py |
| Update CLAUDE.md with clear CLI vs agent skill distinction | Single source of truth; minimal changes | Modified: CLAUDE.md Summary and Usage sections |
| Leverage existing vault/context/index infrastructure | No new dependencies; proven approach | No new modules; agent skills call existing Python functions |
| Quickstart scenarios for validation | Human-readable validation without complex test automation | New file: quickstart.md with 4 scenarios |

---

## Alternatives Considered & Rejected

### Alternative 1: Keep all CLI commands, make them call agent skills internally
**Why Rejected**: 
- CLI cannot invoke Claude Code agent skills programmatically
- Would require separate "agent wrapper" CLI command (e.g., `spek agent-invoke`)
- Still misleading to users who run `spek plan` expecting agent interaction
- Adds complexity without user benefit

### Alternative 2: Rebuild agent skill workflows in pure Python
**Why Rejected**:
- Duplicates interactive prompting logic already in SpecKit
- Loses Claude Code integration (vault loading, context injection)
- Cannot implement interactive clarification/remediation loops without Claude
- Out of scope (SpecKit is stable; no need to reimplement)

### Alternative 3: Remove all CLI commands except init, provide only Bash wrapper for agent skills
**Why Rejected**:
- `spek prepare` is useful as CLI fallback (quick vault/code index load)
- Bash wrappers don't improve discoverability
- CLAUDE.md is clearer than external documentation

---

## Conclusion

Agent skill architecture will follow Claude Code conventions, leverage existing context infrastructure, and use CLAUDE.md as single source of truth. CLI remains minimal (init only), with helpful error messages guiding users to agent skill invocation. This approach aligns implementation with intended design and reduces maintenance burden.
