# Decisions: Spekificity Architecture & Tooling

## Decision 1: Code Analysis Tool (Not Vault Docs)

### Decision

**Graphify vs CodeGraph as the code analysis tool. Agent efficiency is the primary requirement.**

---

### Rationale

#### Project Priority: Agent-First Development

Spekificity is designed for AI agent development workflows. Agent efficiency is non-negotiable:
- Minimize token calls (every grep = tokens)
- Instant queries (no file reading)
- Deterministic impact analysis (not agent reasoning)
- Real-time sync (fresh data on every session)

#### Comparison: Graphify vs CodeGraph

**Graphify (Current Implementation)**

| Aspect | Evaluation |
|--------|-----------|
| Purpose | Generate markdown vault docs of code structure |
| Output | Obsidian vault files (human-browsable) |
| Agent Experience | Reads markdown files (100s+ tokens per query) |
| Impact Analysis | Manual (agent must grep + reason) |
| Sync | Manual (requires re-run) |
| Setup | Simple (`--output vault/`) |
| **Fit for Agent Workflows** | **7/10** (works, but inefficient) |

**CodeGraph (Recommended)**

| Aspect | Evaluation |
|--------|-----------|
| Purpose | Pre-indexed code intelligence for agents |
| Output | SQLite graph + MCP tools |
| Agent Experience | Instant tool calls (92% fewer tokens, 77% faster) |
| Impact Analysis | Built-in (`codegraph_impact`, `codegraph_callers`) |
| Sync | Automatic (file watcher, debounced) |
| Setup | Medium (init + MCP config) |
| Framework Support | 13+ frameworks (routing detection) |
| **Fit for Agent Workflows** | **9/10** (built for this use case) |

#### The Critical Difference

**Graphify:** Agent reads markdown files repeatedly → high token cost per feature  
**CodeGraph:** Agent queries pre-indexed graph → few tool calls per feature

**Concrete impact:**
- Feature cycle with Graphify: ~90+ minutes (includes token overhead)
- Feature cycle with CodeGraph: ~45 minutes (instant queries, impact analysis)

---

### Trade-offs

| Trade-off | Impact | Decision |
|-----------|--------|----------|
| Setup complexity | CodeGraph slightly more complex (MCP config) | Accept (one-time setup, ongoing efficiency gain) |
| No human vault docs of code | Graphify generates browsable vault; CodeGraph doesn't | Accept (vault is for knowledge, not code structure) |
| Learn new tool | CodeGraph is newer; less familiar | Accept (more actively developed; better long-term alignment) |
| Daily usage | Token savings compound over many feature cycles | Accept (immediate measurable benefit) |

---

## Decision 2: Recommended Toolset for Spekificity Users

### Decision

**Recommend dual-system approach for users: Knowledge Vault + Code Analysis Tool.**

Each owns a domain; together they enable fast, informed development with minimal context-switching.

---

### Rationale

Knowledge vault and code analysis serve different rhythms and access patterns:

| System | Purpose | Content | Access | Rhythm |
|--------|---------|---------|--------|--------|
| **Knowledge Vault** | Knowledge base | Specs, plans, decisions, lessons, raw materials | Git + UI (optional) | Changes once per feature cycle |
| **Code Analysis Tool** | Code intelligence | Symbols, calls, inheritance, framework routes | MCP tools (agent queries) | Changes on every file save |

**Why separate them?**

1. **Vault changes slowly** — updated once when feature completes
2. **Code changes constantly** — file watch → instant refresh
3. **Agent queries code frequently** — during every implementation cycle
4. **Vault queries once per session** — `/context-load` at start

**With separation:**
- Vault stays lean + human-navigable
- Code analysis stays fast + agent-efficient
- No redundancy between systems

**Recommended Architecture for Users:**

```
Spekificity Workflow (via agent)
├── /context-load
│   └── Loads knowledge vault (specs, decisions, lessons)
├── /enrich-specify
│   └── Uses vault context + code analysis tool for related symbols
├── /enrich-plan
│   └── Uses vault context + code analysis tool for impact analysis
├── /enrich-implement
│   └── Uses vault context + code analysis tool for structure queries
└── /lessons-learnt
    └── Writes back to vault
```

**Result:** 30-40% faster development on refactoring/debugging tasks.

---

### Benefits

**For Individual Developers:**
- Understand codebase intent (vault) + structure (code analysis tool)
- Refactor with confidence (impact analysis automated)
- Onboard faster (specs + code structure visible)

**For AI agents:**
- Fewer token calls (vs. manual exploration)
- Faster exploration (pre-indexed analysis)
- Impact radius instant (no missed breaking changes)

**For Teams:**
- Shared knowledge base (vault; version-controlled)
- Shared code structure (auto-synced)
- Faster code reviews (impact clear; rationale documented)

---

### Trade-offs

| Aspect | Cost | Benefit |
|--------|------|---------|
| Setup | Medium (2 tools to initialize) | Fast onboarding (both tools visible immediately) |
| Maintenance | Medium (vault + code analysis tool sync) | High (automated impact analysis saves errors) |
| Complexity | 2 systems instead of 1 | Clear separation (no sprawl; each tool optimized) |
| Token efficiency | Lower (vault queries) | Very high (code analysis tool queries) |

---

### When NOT to Use This

- **Greenfield projects with no existing code:** Obsidian alone sufficient initially (add code analysis tool when code grows)
- **Scripts/utilities without complexity:** Code analysis tool overhead > value
- **Projects <10 files:** Manual code understanding cheaper than indexing
- **Fully no-code platforms:** Skip code analysis tool; use Obsidian only

---

### When to Use This

- **Production codebases >100 files**
- **Teams using AI agents for implementation**
- **Refactoring/debugging workflows (frequent changes)**
- **Onboarding new developers**

---

## Decision 3: Toolset Recommendations for the Four Pillars

### Overview

Spekificity's four pillars (token efficiency, determinism, persistence, autonomy) can be addressed by different community tools. This decision evaluates options, rates them by popularity and cohesive fit with Spekificity's architecture, and documents the recommended baseline for each pillar.

---

### Pillar 1: Token Efficiency & Verbosity

**Problem:** Agents waste tokens on file scans and verbose outputs; context window fills with noise.

| Tool | Type | Popularity | Fit | Token Savings | Notes |
|------|------|-----------|-----|---------------|-------|
| **Caveman (recommended)** | Compression | Medium | 9/10 | 60%+ | Simple notation; preserves code; tested with Claude Code |
| Squeez | Compression | Low | 7/10 | 70%+ | Rust-based; multi-CLI support; self-teaching protocol; zero deps |
| contextzip | Compression | Low | 6/10 | 60-90% | CLI-focused; stdout compression; session history coming |
| clipforge-PAKT | Compression | Low | 5/10 | 50%+ | Lossless for JSON/YAML; library + CLI + MCP + browser extension |
| claw-compactor | Compression | Low | 4/10 | 70%+ | 14-stage pipeline; AST-aware; reversible; complex setup |

**Recommendation:** Use `Caveman` for token compression. Sufficient for most use cases; if higher compression needed, evaluate `squeez` (70% savings, multi-tool support) or `contextzip` (60-90% savings, stdout focus).

---

### Pillar 2: Planning & Determinism

**Problem:** Ad-hoc agent planning leads to inconsistent specs, hallucinated context, and redundant work.

| Tool | Type | Popularity | Fit | Determinism | Notes |
|------|------|-----------|-----|-------------|-------|
| **SpecKit/Specify (recommended)** | Spec Framework | **High** | 10/10 | YAML-first; enforces spec→plan→tasks | GitHub's official tool; most active community; battle-tested |
| SDD Pilot | Spec Framework | Medium | 8/10 | Spec-driven phases + quality gates | VSCode + Windsurf support; strong quality gates; enforces phases |
| FSPEC | Spec Framework | Low | 7/10 | Multi-agent factory; DDD/BDD support | TDD/DDD/BDD focus; example mapping; guardrails; newer |
| spec-driven-steroids | Spec Framework | Low | 6/10 | Simple toolkit; native AI tool integration | Focus on CLI discipline; minimal overhead; less documented |
| Paul (Plan-Apply-Unify Loop) | Framework | Low | 7/10 | Plan-Apply-Unify; quality-over-speed | Claude Code native; roundtable-style; newer |
| spec2ship | Spec Framework | Low | 6/10 | Multi-agent; roundtable collaboration | Claude Code focus; social/collaborative; emerging |

**Recommendation:** Use `SpecKit/Specify` for planning & determinism. Highest ecosystem maturity, most features, largest community. Alternatives (SDD Pilot, FSPEC) target specific niches (quality gates, DDD) but require more specialized setup.

---

### Pillar 3: Memory Persistence

**Problem:** Context lost at session end; agents can't build knowledge across features; decisions repeat.

| Tool | Type | Popularity | Fit | Persistence | Notes |
|------|------|-----------|-----|-------------|-------|
| **Obsidian (recommended)** | Vault | **Very High** | 10/10 | Markdown; git-backed; desktop + vault | Largest PKM community; markdown standard; optional UI; proven |
| Basic Memory | Vault | Low | 9/10 | MCP-based; cross-conversation memory | Privacy-first; Obsidian-compatible; emerging; active development |
| SilverBullet | Vault | Medium | 8/10 | Markdown + Lua scripting; self-hosted | Open-source; scriptable; more feature-rich; active community |
| Trilium | Vault | Medium | 7/10 | Notes + knowledge graph; multi-platform | Desktop app; rich UI; not git-backed; harder to version |
| ByteRover (byterover-cli) | Memory Layer | Low | 6/10 | Portable memory for agents; MCP | Emerging; agent-specific; good for session-scoped memory; not file-based |
| Draft | Chrome Extension | Low | 5/10 | Capture AI chats into KB; cloud | Browser-only; cloud-dependent; not ideal for offline/local |
| TidGi-Desktop | Vault | Low | 7/10 | TiddlyWiki + git-backup + REST API | Git-backed; web-clipper; Anki connect; less common; Qt-based |

**Recommendation:** Use `Obsidian` for memory persistence. Unmatched ecosystem for PKM; markdown portable; git versioning standard. Alternatives (Basic Memory, SilverBullet) offer better agent integration (MCP) or richer features (scripting); evaluate based on project needs.

---

### Pillar 4: Autonomy & Code Understanding

**Problem:** Agents can't answer code questions without scanning files; no architectural understanding; clarifications burn tokens.

| Tool | Type | Popularity | Fit | Autonomy | Notes |
|------|------|-----------|-----|----------|-------|
| **CodeGraph (recommended)** | Code Analysis | Medium | 10/10 | MCP tools; instant; 155 languages; framework-aware | Purpose-built for agents; 99% fewer tokens; 77% faster; SQLite graph |
| codebase-memory-mcp | Code Analysis | Low | 9/10 | MCP server; persistent knowledge graph; zero deps | 155 languages; sub-ms queries; high-performance; Cypher support |
| Joern | Code Analysis | Medium | 7/10 | Code property graph; multi-language; dataflow | Academic-grade; C/C++/Java focus; more complex; strong dataflow |
| Pylance | Code Analysis | **High** | 6/10 | Python-specific; language server; fast | Python community standard; not agent-optimized; limited to Python |
| Graphify | Code Analysis | Low | 5/10 | Markdown vault output; human-browsable | Legacy; outputs readable docs; inefficient for agent queries |
| codeflow | Visualization | Low | 4/10 | Browser-based; D3.js visualization; GitHub-linked | Great for humans; not agent-efficient; one-off analysis |

**Recommendation:** Use `CodeGraph` for autonomy & code understanding. Purpose-built for agent workflows with instant queries and impact analysis. Alternative: `codebase-memory-mcp` (slightly better architecture, newer, zero dependencies) for high-performance scenarios.

---

### Recommended Baseline Toolset for Spekificity

**Decision:** For each pillar, recommend the tool that best combines popularity, maturity, and cohesive fit with Spekificity's architecture.

| Pillar | Tool | Fit | Rationale |
|--------|------|-----|-----------|
| Token Efficiency | Caveman | 9/10 | Simple notation; preserves code; tested across tools |
| Determinism | SpecKit/Specify | 10/10 | YAML-first; GitHub official; battle-tested |
| Persistence | Obsidian | 10/10 | Largest PKM community; markdown portable; git-backed |
| Autonomy | CodeGraph | 10/10 | Purpose-built for agents; 99% fewer tokens; instant queries |

**Installation for New Projects:**

```bash
spekificity init
# → auto-detects installed tools
# → prompts for missing tools with recommendations
# → deploys skills locally
```

---

### Alternative Toolsets (Use Cases)

#### **Use Case 1: Minimum Setup (No Optional Dependencies)**
- **Token Efficiency:** Caveman (skill-based; no install)
- **Determinism:** SpecKit/Specify (global install)
- **Persistence:** Markdown vault (plain files; no dependencies)
- **Autonomy:** Manual grep (no tool; skip for small projects)

**Best for:** <100-file projects; teams without CI/CD infrastructure

---

#### **Use Case 2: Maximum Token Savings (Production Codebases)**
- **Token Efficiency:** Squeez (Rust CLI; 70% savings) + Caveman
- **Determinism:** SDD Pilot (strict quality gates)
- **Persistence:** Obsidian + SilverBullet (markdown + scripting)
- **Autonomy:** codebase-memory-mcp (emerging; better than CodeGraph for high-performance scenarios)

**Best for:** Teams running frequent agent cycles; large codebases >500 files

---

#### **Use Case 3: Ecosystem-Focused (GitHub, Enterprise)**
- **Token Efficiency:** Caveman (GitHub Copilot native)
- **Determinism:** SpecKit/Specify (GitHub official; enterprise ready)
- **Persistence:** Obsidian + git (enterprise-friendly)
- **Autonomy:** CodeGraph (standard; good GitHub integration)

**Best for:** Enterprise; GitHub-first teams; standardization priority

---

### Trade-off Matrix

| Criterion | Caveman | Squeez | contextzip | clipforge | claw-compactor |
|-----------|---------|---------|-----------|-----------|--------|
| Token Savings | 60% | 70% | 60-90% | 50% | 70% |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Community | Medium | Small | Small | Small | Small |
| Setup Time | <5 min | 10 min | 10 min | 15 min | 30 min |
| Multi-Tool Support | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Recommendation** | **Yes** | Consider | Consider | Optional | Advanced |

---

### Evaluation Methodology

Each tool rated on:

1. **Popularity** — GitHub stars, community size, adoption in production (high/medium/low)
2. **Fit** — How well it integrates with Spekificity's decorator pattern and four-pillar model (1-10)
3. **Technical Metric** — Pillar-specific measure (token savings %, determinism level, etc.)
4. **Maintenance** — Active development, responsiveness to issues, documentation quality

---

### When to Consider Alternatives

| Scenario | Recommendation |
|----------|-----------------|
| **Extreme token constraints** | Replace Caveman with Squeez; evaluate claw-compactor |
| **Dataflow analysis needed** | Add Joern alongside CodeGraph |
| **Team already uses SilverBullet** | Replace Obsidian (compatible via markdown export) |
| **Python-only codebase** | Pylance sufficient for autonomy; skip CodeGraph |
| **100+ files, deep history** | Replace Graphify/CodeGraph with codebase-memory-mcp |
| **Offline-first requirement** | Ensure all tools work locally; Obsidian + CodeGraph do; verify others |

---

### Conclusion

**Spekificity's recommended toolset balances popularity, maturity, and cost-effectiveness:**
- `Caveman` — sufficient compression; mature; no setup friction
- `SpecKit/Specify` — industry standard; battle-tested; largest community
- `Obsidian` — de facto PKM standard; markdown portable; proven at scale
- `CodeGraph` — purpose-built for agents; recommended for teams doing frequent cycles

**Alternatives exist for each pillar; use matrix above to evaluate against your constraints.**
- **Projects that need both intent + structure understanding**