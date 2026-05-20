# Spekificity: Project Intention

**Date Documented:** May 13, 2026  
**Status:** Active Development  
**Author:** spekificity core team

---

## Vision Statement

Spekificity consolidates existing best-in-class tools to solve four foundational LLM agent problems:

1. **Token Efficiency and Verbosity** — Replace file scans with graph queries; compress outputs substantially
2. **Planning and Determinism** — Enforce canonical workflows; ground plans in code reality
3. **Memory Persistence** — Store decisions, lessons, patterns; survive session boundaries
4. **Autonomy** — Enable agents to operate independently without constant developer hand-holding

**Core Promise:** From raw code + documentation → idea → spec → implementation → lessons learned, all with AI agent as autonomous copilot, all tracked in persistent project memory, with minimal tool-switching.

---

## Philosophy: Consolidation, Not Reinvention

### What Spekificity Does NOT Do

- ❌ Reimplement spec-driven frameworks
- ❌ Reimplement code analysis/mapping tools
- ❌ Reimplement knowledge management systems
- ❌ Reimplement response compression/optimization
- ❌ Build its own AI agent infrastructure

### What Spekificity DOES Do

- ✅ Identify + evaluate best-in-class tools for **token efficiency, planning, persistence, autonomy**
- ✅ Orchestrate tool installation + setup (→ 1-command init)
- ✅ Wire chosen tools into a coherent, deterministic workflow
- ✅ Automate handoff between stages with context injection (spec → plan → tasks → implement)
- ✅ Replace file scanning with indexed graph queries where possible
- ✅ Compress verbose outputs at each stage
- ✅ Capture outcomes back to persistent knowledge base (lessons learned)
- ✅ Maintain project memory across sessions (AI agent loads full context at start)
- ✅ Enable agent autonomy (code questions answered without dev context injection)

**Why this matters:** Users get best-in-class tools *and* the workflow orchestration most projects invent manually (and get wrong). No vendor lock-in. Each tool remains independently upgradable. As better tools emerge, swap them out without restructuring the workflow.

---

## How Workflow Stages Address the Four Pillars

| stage | token efficiency | determinism | persistence | autonomy |
|-------|---|---|---|---|
| **Stage 0: Init** | graph indexing configured once (amortizes over project lifetime) | canonical tool choices established | vault structure initialized | agent has all tools available at start |
| **Stage 1: Ingest** | code graph indexed (92% fewer queries later) | prior context structured consistently | raw materials + graph stored permanently | agent can analyze codebase independently |
| **Stage 2: Feature Dev** | `/context-load` loads vault once per session; graph queries replace file reads | spec → plan → tasks → implement enforced; no exploration phase | decisions + lessons captured in vault | agent executes workflow autonomously with graph + vault context |
| **Stage 3: Refinement** | lesions written terse (caveman style); graph incrementally updated | outcomes feed back into vault structure | agent learns from each feature; compounding | next feature starts with richer context; less dev guidance needed |

**Result:** token usage is managed through targeted graph queries and context caching. determinism improves with each cycle. persistence means NO context reset. autonomy grows as vault accumulates.

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

**Setup required:** One-time initialization of tools and vault structure

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
1. `/spek.automate` → Load vault + code context, then orchestrate SpecKit through specification, clarification, planning, tasks, analysis, and remediation
   - Injects context: related code modules, prior decisions, lessons from similar features
   - Generates: `specs/<feature>/spec.md`, `specs/<feature>/plan.md`, `specs/<feature>/tasks.md`
2. Human reviews generated artifacts and any analyze findings
3. `/spek.implement` → Execution with context
   - Agent executes approved tasks with code map + spec + plan in scope
   - Auto-syncs code changes to code analysis tool
   - Auto-captures execution trace

**Output:** 
- Code changes (merged to main branch)
- Execution trace (stores in vault for analysis)
- Lessons entry → `vault/lessons/<date>-<feature>.md`

**Time to Value:** Feature development workflow from spec through code

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
- **Contribution:** Optional compression layer; works alongside graph queries
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
- Traditional approach: Manual context setup and orchestration; trial-and-error tool integration

**With Spekificity:**
- User runs: `spekificity init`
- Spekificity orchestrates: evaluates available tools, installs recommended ones, configurations, wiring
- One command for verifiable state

Spekificity doesn't build installers; it evaluates and chains existing ones + adds the glue.

### Example 2: Context Injection

**Without Spekificity:**
- During spec: dev manually reads prior specs, related code, past lessons
- Risk: Misses dependencies; repeats past mistakes; context is fragmented

**With Spekificity:**
- `/spek.automate` automatically injects related components + lessons during specify/plan phases
- Code map + vault are pre-indexed (fresh on session start)
- Agent reads one document; gets full context

Spekificity doesn't build code analysis; it uses the chosen tool's index + presents it at the right moment.

### Example 3: Impact Analysis

**Without Spekificity:**
- Dev must manually trace function calls: "if I change this function, what breaks?"
- Process: grep, manual reading, hope nothing was missed

**With Spekificity:**
- `/spek.implement` uses code analysis tool's impact detection
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