# Spekificity: Vision, Philosophy & Tenets

**See also:** [vision.md](vision.md) (overview) → [architecture.md](architecture.md) (technical) → [workflow.md](workflow.md) (process)

---

## Project Vision

### What is Spekificity?

Spekificity is a **specification-driven agent development framework** designed to enable rapid, reproducible feature delivery with AI agents while minimizing token overhead and maximizing knowledge persistence.

**Core Problem:** AI agents often produce code without clear, durable specifications. Knowledge gets lost between sessions. Context is rebuilt from scratch. Token budgets explode.

**Core Solution:** Keep specifications in a persistent Obsidian vault, tie code analysis to a real-time CodeGraph, route work through a deterministic SpecKit pipeline, and expose all workflows as repeatable agent skills (`/spek.*` commands).

**Outcome:** Teams can build features faster, audit decisions, extract lessons, and reuse context across sessions without token waste or knowledge loss.

---

## Philosophy: Core Principles

### 1. Token Efficiency

**Every token counts. Agent queries should be pre-indexed, not re-scanned.**

- Code analysis via CodeGraph MCP (pre-indexed SQLite) instead of grep + file reads
- Vault context loaded once per session, not re-read per query
- Specifications written once, referenced many times
- Lessons learned captured, stored, and reused across features

### 2. Determinism

**Repeatable workflows. No guessing. No drift.**

- All major steps captured in version-controlled specs and plans
- Skills (`/spek.*`) define deterministic sequences
- Impact analysis powered by CodeGraph, not agent reasoning
- Decisions logged and linked to code changes

### 3. Persistence

**Knowledge outlives sessions.**

- Specifications, plans, decisions stored in Obsidian vault (Git-backed)
- Lessons extracted and committed to vault at feature end
- CodeGraph syncs automatically; never stale
- Session memory persists via repo-scoped YAML files

### 4. Autonomy

**Agents have clear boundaries and tools.**

- SpecKit pipeline is deterministic (not agent-driven)
- Agent skills (`/spek.*`) are composable but opinionated
- CodeGraph provides pre-indexed facts (no agent reasoning about code structure)
- Skill chaining and multi-agent workflows are explicit, not emergent

---

## Project Tenets

### 1. Context Lives in the Vault

Obsidian vault is the single source of truth for project knowledge:
- Specifications define *what* and *why*, not agents
- Plans break specs into tasks; agents execute tasks, not design them
- Decisions are documented with rationale and dates
- Lessons learned are captured and indexed

**Implication:** A new agent joining mid-project can read the vault and understand what's been tried, what worked, and why.

---

### 2. Specs Drive Code

No code without a specification.

- Before implementation, a spec exists in the vault
- Spec includes Success Criteria, Assumptions, Risk Assessment
- Tasks are derived from spec, not invented mid-implementation
- Implementation can't proceed without spec approval

**Implication:** Every feature is traceable to its intent. Scope creep is visible and explicit.

---

### 3. CodeGraph is Code Intelligence

Real-time, pre-indexed code analysis via CodeGraph MCP. No file scanning.

- CodeGraph automatically syncs on every file change
- Queries are deterministic (impact analysis, caller chains, definitions)
- Agents use CodeGraph for code context, not file grep
- CodeGraph is the modern standard for agent-driven code analysis

**Implication:** Agent queries stay fast and token-cheap, even in large codebases.

---

### 4. Skills are Deterministic Checkpoints

Agent skills (`/spek.prepare`, `/spek.plan`, etc.) are deterministic, composable steps.

- Each skill has a clear pre-condition and post-condition
- Skills can be chained or run standalone
- Skill output is predictable (spec exists, plan exists, etc.)
- Skills don't invent new workflows; they execute known ones

**Implication:** Users know what will happen when they invoke `/spek.plan`. No surprises.

---

### 5. Enrichment Layers Embed Context

Specifications and plans gain context-specific layers:
- Success Criteria (what defines done?)
- Assumptions (what's true?)
- Risk Assessment (what could go wrong?)
- Resource Estimates (time, tokens, complexity)
- Metrics (how do we measure success?)

**Implication:** Plans are richer, more realistic, and easier for agents to execute well.

---

### 6. Lessons Learned are Captured and Indexed

At the end of each feature:
- Extract structured lessons (what worked, what didn't, why)
- Store in vault with links to specs, plans, decisions
- Tag for later retrieval ("token-efficiency", "error-handling", etc.)
- Reuse lessons for future planning

**Implication:** The project learns. Mistakes don't repeat. Good practices compound.

---

### 7. Naming is Explicit and Namespaced

Consistent naming makes the system intuitive:
- `spek.*` = Spekificity user-facing skills
- `speckit.*` = SpecKit workflow engine commands
- Prefix always present; commands one-word where possible
- Rationale: Namespace clarity + ease of invocation

**Implication:** New users can guess what `/spek.prepare` does. Command surface is predictable.

---

## Constraints: What We Won't Do

### Out of Scope

1. **Build System Integration:** Spekificity is for spec-driven development, not build/test automation. Projects handle builds via CI/CD.

2. **Real-time Collaboration:** Vault is Git-backed, not real-time synced. Multiple agents can work on different features; merge conflicts are resolved offline.

3. **Graphical UI:** Spekificity is CLI + Markdown. No custom editor or dashboard. Obsidian is the UI.

4. **AI Model Selection:** Spekificity doesn't recommend models. Users choose their own (OpenAI, Anthropic, etc.). Skills are model-agnostic.

5. **Project Initialization:** Spekificity assumes an existing codebase and Obsidian vault. It's not a project generator or template system.

6. **Execution Guarantees:** Spekificity provides structure, not guarantees. Agents can still fail, hallucinate, or produce incorrect code. Specs reduce risk; they don't eliminate it.

---

## Target Users

### Primary

- **AI Developers:** Teams using agents to build software; want structure and repeatability
- **Specification Authors:** Developers who write detailed specs before coding
- **Knowledge Stewards:** Teams that value long-term context and lesson capture

### Secondary

- **Small Teams (1-3 devs):** Projects where one person wears many hats
- **Research Teams:** Experimenting with agent workflows and trying to measure progress
- **Enterprises:** Large codebases where impact analysis and spec traceability matter

### NOT a Fit

- **Exploratory Hacking:** "Rapid iteration" teams that don't write specs
- **Waterfall-Averse Teams:** Teams that view detailed planning as process overhead
- **Manual Development Only:** Teams not using agents (Spekificity overhead outweighs benefit)

---

## Why Spekificity Exists

**Without Spekificity:**
- Agents generate specs, code, and docs in every session (token waste)
- Knowledge about why decisions were made is lost (no persistence)
- Impact analysis is agent-reasoned, not data-backed (slow, error-prone)
- Every feature starts from scratch (no reuse)
- Code quality is inconsistent (no standardized workflow)

**With Spekificity:**
- Specs written once, referenced many times (token-efficient)
- Decisions logged and linked to code (persistence)
- Impact analysis is CodeGraph-backed (deterministic)
- Lessons learned are captured and reused (cumulative improvement)
- Workflow is standardized and repeatable (consistent quality)

---

## References

- **Architecture Details:** [architecture.md](architecture.md)
- **Development Workflow:** [workflow.md](workflow.md)
- **Naming & Conventions:** [conventions.md](conventions.md)
