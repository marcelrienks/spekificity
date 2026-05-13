# Spekificity: Project Intention

**Date Documented:** May 13, 2026  
**Status:** Active Development  
**Author:** spekificity core team

---

## Vision Statement

Spekificity consolidates current best practices in LLM and AI Agent development into a cohesive, minimal-friction workflow. It is not a toolset that reimplements functionality—it is orchestration that links existing best-in-class tools together and automates the connective tissue between them.

**Core Promise:** From raw code + documentation → idea → spec → implementation → lessons learned, all with AI agent as copilot, all tracked in persistent project memory, with minimal tool-switching.

---

## Philosophy: Consolidation, Not Reinvention

### What Spekificity Does NOT Do

- ❌ Reimplement spec-driven frameworks
- ❌ Reimplement code analysis/mapping tools
- ❌ Reimplement knowledge management systems
- ❌ Reimplement response compression/optimization
- ❌ Build its own AI agent infrastructure

### What Spekificity DOES Do

- ✅ Identify + evaluate best-in-class tools for each pattern
- ✅ Orchestrate tool installation + setup (→ 1-command init)
- ✅ Wire chosen tools into a coherent workflow
- ✅ Automate handoff between stages (spec → plan → tasks → implement)
- ✅ Inject context at each stage (via code analysis + knowledge base)
- ✅ Capture outcomes back to knowledge base (lessons learned)
- ✅ Minimize context-switching (all accessible via single interface)
- ✅ Maintain project memory across sessions (persistent knowledge base)

**Why this matters:** Users get best-in-class tools *and* the workflow orchestration most projects invent manually (and get wrong). No vendor lock-in. Each tool remains independently upgradable. As better tools emerge, swap them out without restructuring the workflow.

---

## The Complete Workflow

### Stage 0: Initialization (One-Command Setup)

```bash
spekificity init
```

**What happens:**
1. Auto-detect installed tools (spec framework, code mapper, vault system, compression tool, git, Python, Node)
2. Install missing tools with user prompts (recommending current best practices)
3. Deploy spekificity skills locally to project
4. Initialize knowledge vault structure (docs/, specs/, vault/, wiki/)
5. Initialize code mapping/analysis
6. Confirm setup complete + tool integrations verified

**Output:** `.spekificity/` config, `.agents/skills/` skill routing, obsidian vault ready

**Time:** ~10 minutes (first time); ~2 minutes (re-init on new project)

---

### Stage 1: Ingest Raw Materials

**Inputs:** Code repository + any raw documentation (PDFs, articles, notes, transcripts)

**Entry Point:** Developer drops files into `vault/raw/` or uses web clipper for articles

**Automatic Actions:**
1. Code analysis tool indexes source → stores structure map in vault
2. Knowledge system processes raw docs via LLM
3. Vault accumulates as source of truth

**Output:** `vault/graph/index.md` (codebase topology), `vault/` (growing knowledge base)

**Trigger:** Manual (`/map-codebase`), or automatic on session start via `/context-load`

---

### Stage 2: Spec-Driven Feature Development

**User:** "Implement user authentication system"

**Agent Workflow:**
1. `/context-load` → Load vault (code map + recent lessons) into session
2. `/speckit-enrich-specify` → Spec-first clarification
   - Injects context: related code modules, prior decisions, lessons from similar features
   - Generates: `specs/<feature>/spec.md`
3. `/speckit-enrich-plan` → Architecture planning
   - Injects context: component impact map, affected test files, integration points
   - Generates: `specs/<feature>/plan.md`
4. `/speckit.tasks` → Actionable task breakdown
   - Tool-agnostic task generation
   - Generates: `specs/<feature>/tasks.md` (dependency-ordered)
5. `/speckit-enrich-implement` → Execution with context
   - Agent executes all tasks with code map + spec + plan in scope
   - Auto-syncs code changes to code analysis tool
   - Auto-captures execution trace

**Output:** 
- Code changes (merged to main branch)
- Execution trace (stores in vault for analysis)
- Lessons entry → `vault/lessons/<date>-<feature>.md`

**Time to Value:** Feature spec to working code: typically 30-60 minutes (depending on complexity)

---

### Stage 3: Continuous Refinement (The Loop)

**After feature complete:**

1. Agent runs `/lessons-learnt`
   - Analyzes execution trace
   - Extracts: what worked, what was harder, what we learned about the codebase
   - Files structured entry into vault
2. Graph auto-updates (incremental via file watch)
3. Next feature starts at Stage 2 with richer context (previous lessons available)

**Long-term Effect:** Vault becomes project's externalized intelligence. Each feature makes the next one faster.

---

## How Tools Integrate

### Spec-Driven Framework
- **Role:** Structure-based feature development (YAML/Markdown specs, planning templates)
- **Integration:** Spekificity enhances with context injection via decorator pattern
- **Contribution:** Spec validation, plan templates, task generation, dependency ordering
- **Independent:** Framework can be upgraded without restructuring spekificity workflows
- **Current Recommendation:** Spec-first frameworks emphasizing YAML/Markdown clarity

### Code Analysis / Mapping Tool
- **Role:** Codebase topology (symbols, calls, inheritance, framework routes, dependencies)
- **Integration:** Indexed once during init; incrementally synced on file changes
- **Contribution:** Context injection during spec/plan stages; impact analysis for refactoring
- **Independent:** Can rebuild analysis via `/map-codebase` without affecting specs
- **Current Recommendation:** Tools with AST parsing, multi-language support, framework awareness

### Knowledge Vault / Document System
- **Role:** Persistent knowledge store across sessions (specs, decisions, lessons, raw materials)
- **Integration:** Central repository for code topology, architectural decisions, lessons learned
- **Contribution:** Browsable interface + serves as AI agent memory between sessions
- **Independent:** Vault uses standard formats (markdown + git); portable across tools
- **Current Recommendation:** Plain-text based systems with git backing + optional rich UI

### Token Efficiency / Response Compression (Optional)
- **Role:** Minimize token usage while preserving technical accuracy
- **Integration:** Invoked at key stages (spec review, plan review) for optimization
- **Contribution:** 25-40% token reduction on outputs; optional efficiency multiplier
- **Independent:** Can be omitted; optional enhancement layer
- **Current Recommendation:** Terse notation systems that preserve code + technical substance

### AI Agent
- **Role:** Executive (spec-ing, planning, implementing, learning)
- **Integration:** Reads spekificity skills from `.agents/skills/`; uses speckit commands; queries graph via MCP tools
- **Contribution:** Intelligence (reasoning, writing code, extracting lessons)
- **Expectation:** Agent is co-developer, not code generator; collaboration required
- **Supported:** Any capable AI agent (e.g. GitHub Copilot, Claude Code)

---

## Not Reinventing: Specific Examples

### Example 1: Setup

**Without Spekificity:**
- User manually: installs spec framework, installs code mapper, creates vault, configures agent, sets up compression tool, links them together
- Time: 1-2 hours; 10+ manual steps; high error rate; decisions about which tools to use

**With Spekificity:**
- User runs: `spekificity init`
- Spekificity orchestrates: evaluates available tools, installs recommended ones, configurations, wiring
- Time: 10 minutes; 1 command; verifiable state

Spekificity doesn't build installers; it evaluates and chains existing ones + adds the glue.

### Example 2: Context Injection

**Without Spekificity:**
- During spec: dev manually reads prior specs, related code, past lessons
- Risk: Misses dependencies; repeats past mistakes; context is fragmented

**With Spekificity:**
- `/speckit-enrich-specify` automatically injects related components + lessons
- Code map + vault are pre-indexed (fresh on session start)
- Agent reads one document; gets full context

Spekificity doesn't build code analysis; it uses the chosen tool's index + presents it at the right moment.

### Example 3: Impact Analysis

**Without Spekificity:**
- Dev must manually trace function calls: "if I change this function, what breaks?"
- Process: grep, manual reading, hope nothing was missed

**With Spekificity:**
- `/speckit-enrich-implement` uses code analysis tool's impact detection
- Impact is instant: "Changing `auth.jwt()` affects 47 call sites, including these tests"
- Agent checks impact before implementing

Spekificity doesn't calculate impact; it surfaces the chosen tool's capabilities at the right moment.

---

## Guiding Principles for Completion

### 1. Enhance, Not Replace
Every spekificity workflow maintains the underlying tool's behavior intact. Tools can be used directly without spekificity; spekificity adds orchestration + context injection, not replacement.

### 2. Markdown-First Delivery
All skills, workflows, configurations are markdown files. AI agents read and execute them directly. No compiled binaries. Portability guaranteed.

### 3. Modular Independence
Each tool (spec framework, code mapper, vault, compression) is independently upgradable. Breaking changes in one tool should not require re-initialization of spekificity. As better tools emerge, they can be swapped in.

### 4. Minimal Configuration
If possible, auto-detect and auto-wire. Manual configuration only for truly customizable aspects (vault structure, skill routing). Defaults should work for 90% of users.

### 5. Persistent Memory
Project vault is the source of truth. Every output (spec, plan, lessons) goes into vault. Every new session starts with vault loaded. Knowledge compounds over time.

### 6. Token Efficiency as First-Class Concern
- Caching (load vault once per session, not per stage)
- Graph-based context (query indexed structure, not read files repeatedly)
- Caveman compression (terse notation on outputs)
- These are not afterthoughts; they drive architecture decisions.

### 7. AI Agent as Copilot
Spekificity assumes an AI agent as the executant. Workflows are designed so agents read spekificity skills + speckit templates, then reason about implementation. Humans review and approve major decisions. Collaboration, not automation.