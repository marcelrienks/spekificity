# Spekificity: Vision and Philosophy

**Date Documented:** May 13-20, 2026  
**Status:** Active Development  
**See also:** [intention.md](intention.md) (principles) → [architecture.md](architecture.md) (technical) → [workflow.md](workflow.md) (process)

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

## Design Principles

- **Four pillars by design**: Every component targets one of four core problems — **token efficiency, determinism, persistence, autonomy**. No feature accepted that doesn't improve one of these.
- **Decorator pattern**: Spekificity skills wrap, not replace, standard SpecKit commands. Vanilla SpecKit remains untouched and upgradable.
- **Modular independence**: Code graphing tool, knowledge vaulting tool, spec driven development tool, and the Spekificity custom layer can each be updated independently.
- **Global tools, local customisation**: Global tools (like SpecKit) are installed per-machine via package manager, while Spekificity custom layer is per-project. Setup automation handles both.
- **AI-executable setup**: Wherever CLI automation is impractical, setup is documented as step-by-step guides that an AI agent can follow.
- **Token efficiency + compression by default**: Graph-based context loading and response compression are first-class, built into every workflow stage, not afterthoughts.

---

## Four Pillars Mapping

How each component targets the four core problems:

| Pillar | Token Efficiency | Determinism | Persistence | Autonomy |
|--------|---|---|---|---|
| **Code Graph** (CodeGraph preferred) | Indexed queries cut token usage by an order of magnitude versus file scans | Exact ground-truth context eliminates hallucinations | Graph auto-syncs on file changes | Agent answers code questions without asking dev |
| **Vault** (Obsidian markdown) | Pre-synthesized context loads once per session | Enforces consistent structure; decisions stay consistent | Lessons + decisions persist across sessions + projects | Agent recalls patterns from history; no redundant searching |
| **Spec-Driven Framework** (SpecKit) | Canonical steps = no token-wasteful exploration | Enforces spec → plan → tasks → implement | Specs + plans captured in vault for future reference | Deterministic workflow = less dev clarification needed |
| **Compression** (Caveman) | Substantial output reduction at key stages | Terse notation cuts noise, improves clarity | — | Agent reads faster, processes more context in same tokens |

**Result:** Each tool improves *all four pillars*, but emphasizes one. Together = compounding effect.

---

## How Workflow Stages Address the Four Pillars

| Stage | Token Efficiency | Determinism | Persistence | Autonomy |
|-------|---|---|---|---|
| **Stage 0: Init** | Graph indexing configured once (amortizes over project lifetime) | Canonical tool choices established | Vault structure initialized | Agent has all tools available at start |
| **Stage 1: Ingest** | Code graph indexed (92% fewer queries later) | Prior context structured consistently | Raw materials + graph stored permanently | Agent can analyze codebase independently |
| **Stage 2: Feature Dev** | `/context-load` loads vault once per session; graph queries replace file reads | Spec → plan → tasks → implement enforced; no exploration phase | Decisions + lessons captured in vault | Agent executes workflow autonomously with graph + vault context |
| **Stage 3: Refinement** | Lessons written terse (caveman style); graph incrementally updated | Outcomes feed back into vault structure | Agent learns from each feature; compounding | Next feature starts with richer context; less dev guidance needed |

**Result:** Token usage is managed through targeted graph queries and context caching. Determinism improves with each cycle. Persistence means NO context reset. Autonomy grows as vault accumulates.

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

**Output:** `.spekificity/` config, `.agents/skills/` skill routing, Obsidian vault ready

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

1. Agent runs `/spek.post`
   - Analyzes execution trace
   - Extracts: what worked, what was harder, what we learned about the codebase
   - Files structured entry into vault
2. Graph auto-updates (incremental via file watch)
3. Next feature starts at Stage 2 with richer context (previous lessons available)

**Long-term Effect:** Vault becomes project's externalized intelligence. Each feature makes the next one faster.

---

## Component Architecture

Spekificity has no deployed application runtime or backend service. Its architecture is the structure of its files, CLI entry points, skill contracts, and how those pieces compose.

### 1. Skills (Primary Deliverable)

Skills are markdown files that an AI agent reads and executes. Each skill file contains:
- **Description**: What this skill does and when to use it
- **Trigger**: How it is invoked (command name or condition)
- **Inputs**: What the skill expects before executing
- **Steps**: Ordered, unambiguous instructions the AI follows
- **Outputs**: What the skill produces and where it is stored

**User-facing command surface:**
- `/spek.prepare` — Initialize workspace, git state, graph freshness, and feature state
- `/spek.context` — Load or reload project context into session
- `/spek.map` — Build or refresh code/document graph
- `/spek.automate` — Orchestrate spec-first flow through task generation
- `/spek.implement` — Execute implementation after automation has prepared artifacts
- `/spek.post` — Archive feature outcomes, lessons, vault updates, and graph refresh
- `/spek.lessons` — Extract structured lessons explicitly when needed

### 2. CLI Scripts

- `bin/spek` — Globally-installable entry point (copy to `/usr/local/bin/spek`)
- `.spekificity/bin/` — Per-project scripts:
  - `_lib.sh` — Shared utilities
  - `prepare.sh` — Pre-execution setup
  - `automate.sh` — Workflow orchestration
  - `post.sh` — Post-execution processing

### 3. Workflows

Workflow documents describe how skills compose into multi-step processes:
- Ordered sequence of skill invocations
- Decision points (conditional paths)
- Expected state at each checkpoint
- Recovery procedures for partial failures

### 4. Setup Guides

Step-by-step, AI-executable installation and configuration instructions for each prerequisite tool. Assumes only that the AI has access to a terminal and internet.

### 5. Obsidian Vault

The vault is the persistent context store for project documentation:
- `vault/lessons/` — Per-feature lessons learned
- `vault/context/` — Decisions, patterns, project principles
- `vault/graph/` — Code structure index (generated by code analysis tool)

Uses plain markdown, compatible with Obsidian format. AI agents read it directly without the app running.

---

## Component Isolation and Update Strategy

Each component can be updated independently:

| Component | Isolation Mechanism |
|-----------|-------------------|
| **SpecKit** | Installed globally; Spekificity skills invoke it by command name only (no internal API assumptions) |
| **Code Analysis Tool** | Invoked via CLI in the `map-codebase` skill; only the skill file needs updating if the CLI changes |
| **Obsidian** | Vault uses plain markdown; no dependency on Obsidian internal format |
| **Spekificity Custom Layer** | Local per-project; updated by pulling latest from this repo |

### Update Procedures

- **SpecKit update**: `uv tool install --reinstall specify-cli` — No Spekificity changes required unless SpecKit's command interface changes
- **Code Analysis Tool update**: Update MCP server config or CLI invocation if args change; update only the skill file if invocation changes
- **Obsidian update**: No action required (vault is plain markdown)
- **Spekificity update**: `git pull` in the Spekificity repo; copy updated skills to target project

---

## AI Agent Integration

Skills are placed in `.agents/skills/` — the canonical, agent-agnostic location. Any AI agent (GitHub Copilot, Claude Code, or similar) reads skills from this directory.

- `.agents/skills/` — Canonical skill files; all agents read from here
- `agents.md` at project root lists available skills and workflow entry points
- Agent-specific config files reference `.agents/skills/` rather than duplicating content

**Cross-platform note:** `.agents/` uses only forward slashes and lowercase names; compatible with Windows, macOS, and Linux.

---

## How Tools Integrate

### Spec-Driven Framework (SpecKit)
- **Role:** Structure-based feature development (YAML/Markdown specs, planning templates)
- **Integration:** Spekificity enhances with context injection via decorator pattern
- **Contribution:** Spec validation, plan templates, task generation, dependency ordering
- **Independent:** Framework can be upgraded without restructuring Spekificity workflows
- **Current Recommendation:** Spec-first frameworks emphasizing YAML/Markdown clarity

### Code Analysis / Mapping Tool (CodeGraph)
- **Role:** Codebase topology (symbols, calls, inheritance, framework routes, dependencies)
- **Integration:** Indexed once during init; incrementally synced on file changes
- **Contribution:** Context injection during spec/plan stages; impact analysis for refactoring
- **Independent:** Can rebuild analysis via `/map-codebase` without affecting specs
- **Current Recommendation:** Tools with AST parsing, multi-language support, framework awareness

### Knowledge Vault / Document System (Obsidian)
- **Role:** Persistent knowledge store across sessions (specs, decisions, lessons, raw materials)
- **Integration:** Central repository for code topology, architectural decisions, lessons learned
- **Contribution:** Browsable interface + serves as AI agent memory between sessions
- **Independent:** Vault uses standard formats (markdown + git); portable across tools
- **Current Recommendation:** Plain-text based systems with git backing + optional rich UI

### Token Efficiency / Response Compression (Caveman)
- **Role:** Minimize token usage while preserving technical accuracy
- **Integration:** Invoked at key stages (spec review, plan review) for optimization
- **Contribution:** Optional compression layer; works alongside graph queries
- **Independent:** Can be omitted; optional enhancement layer
- **Current Recommendation:** Terse notation systems that preserve code + technical substance

### AI Agent
- **Role:** Executive (spec-ing, planning, implementing, learning)
- **Integration:** Reads Spekificity skills from `.agents/skills/`; uses SpecKit commands; queries graph via MCP tools
- **Contribution:** Intelligence (reasoning, writing code, extracting lessons)
- **Expectation:** Agent is co-developer, not code generator; collaboration required
- **Supported:** Any capable AI agent (e.g., GitHub Copilot, Claude Code)

---

## Vault Commit Strategy

**Recommended:** Commit the vault to git with the project.

- **Rationale:** Vault entries (lessons learnt, decisions, patterns) are project artifacts with long-term value. Version-controlling them preserves history and enables team sharing.
- **Exception:** Generated code-analysis indexes (e.g., `.codegraph/graph.db` or Graphify cache output) should be gitignored and regenerated per machine via `/map-codebase`. The vault itself (lessons + context) is always small and should always be committed.

A `.gitignore` template covering this exception is included in the init workflow.

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
Every Spekificity workflow maintains the underlying tool's behavior intact. Tools can be used directly without Spekificity; Spekificity adds orchestration + context injection, not replacement.

### 2. Markdown-First Delivery
All skills, workflows, configurations are markdown files. AI agents read and execute them directly. No compiled binaries. Portability guaranteed.

### 3. Modular Independence
Each tool (spec framework, code mapper, vault, compression) is independently upgradable. Breaking changes in one tool should not require re-initialization of Spekificity. As better tools emerge, they can be swapped in.

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
Spekificity assumes an AI agent as the executant. Workflows are designed so agents read Spekificity skills + SpecKit templates, then reason about implementation. Humans review and approve major decisions. Collaboration, not automation.

---

## Repository State

This repository is design-first and ahead on architectural definition. It currently contains:

- Project vision and philosophy
- Architecture and component structure
- Workflow definitions for enriched SpecKit usage
- Atomic specifications for context loading, orchestration, memory, graph integration, and post-processing
- Setup notes for supporting tools
- Design decisions and rationale

The repository does **not** currently contain a complete shipped `spek` CLI, installed skill bundle, or runnable platform distribution. These will be delivered in Phase 2 (implementation).

---

## See Also

- [wiki/naming-conventions.md](naming-conventions.md) — Naming conventions for skills and workflows
- [wiki/setup.md](setup.md) — Prerequisites and tool installation
- [wiki/workflow.md](workflow.md) — Complete feature development workflow
