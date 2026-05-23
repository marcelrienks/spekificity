# Decisions: Spekificity Architecture & Tooling

## Decision 1: Indexing Tool (lat.md — Final)

### Decision

**lat.md is the canonical indexing tool for Spekificity. Legacy indexing approaches are deprecated and not supported for new projects.**

---

### Rationale

#### Project Priority: Agent-First Development

Spekificity is designed for AI agent development workflows. Agent efficiency is non-negotiable:
- Minimize token calls (every grep = tokens)
- Instant queries (no file reading)
- Deterministic impact analysis (not agent reasoning)
- Real-time sync (fresh data on every session)

#### Why lat.md

**lat.md (Selected)**

| Aspect | Evaluation |
|--------|-----------|
| Purpose | Pre-indexed code intelligence for agents |
| Output | SQLite graph + MCP tools |
| Agent Experience | Pre-indexed tool calls for code analysis without file scanning |
| Impact Analysis | Built-in (`lat_impact`, `lat_callers`) |
| Sync | Automatic (file watcher, debounced) |
| Setup | Medium (init + MCP config) |
| Framework Support | Broad framework support (including routing detection) |
| Query Performance | 100ms average (vs. 2000ms+ for file scan) |
| **Fit for Agent Workflows** | **9/10** (purpose-built for this use case) |

#### Legacy indexing approaches

Older indexing tools required manual syncs and produced document-heavy outputs that were costly for agent queries. Those legacy approaches are archived and not recommended for new projects.

**Concrete Impact (illustrative):**
- Manual indexers: higher token cost per query and stale results without watch mode
- Modern incremental indexers (lat.md): fast incremental queries and lower token overhead

#### Decision Made: lat.md as the canonical indexer

**Effective Date:** 2026-05-23  
**Status:** Final (lat.md is the project's canonical indexing tool)  
**Legacy Support:** Legacy specs archived for reference only; migrate to `lat.md` for active work  
**Migration:** Existing legacy-index users → rebuild index using `lat.md` and update configuration as specified in the lat.md setup spec

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| MCP Configuration Complexity | Small one-time cost; pays off in session 2 |
| No Human-Browsable Code Docs | Vault is for architecture + decisions; lat.md is for code intelligence |
| New Tool Learning Curve | lat.md simpler to configure via extractors than legacy AST setups |
| Long-term Vendor Lock | lat.md risk mitigated by pluggable extractors and open ecosystem |

---

### Previous Decision (Archived Reference)

Earlier analysis compared legacy indexers vs newer indexers (see Decision 1 v1 below). This decision confirms and finalizes the choice to standardize on `lat.md` for new projects.

**Previous Comparison (For Reference):**
- Legacy indexers (archived): 7/10 fit for agent workflows
- lat.md (Recommended): 9/10 fit for agent workflows

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

**Result:** Faster development on refactoring/debugging tasks with pre-indexed analysis.

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
| **Caveman (recommended)** | Compression | Medium | 9/10 | substantial | Simple notation; preserves code; used in agent workflows |
| Squeez | Compression | Low | 7/10 | 70%+ | Rust-based; multi-CLI support; self-teaching protocol; zero deps |
| contextzip | Compression | Low | 6/10 | 60-90% | CLI-focused; stdout compression; session history coming |
| clipforge-PAKT | Compression | Low | 5/10 | 50%+ | Lossless for JSON/YAML; library + CLI + MCP + browser extension |
| claw-compactor | Compression | Low | 4/10 | 70%+ | 14-stage pipeline; AST-aware; reversible; complex setup |

**Recommendation:** Use `Caveman` for token compression. Evaluating additional compression tools for specific use cases.

---

### Pillar 2: Planning & Determinism

**Problem:** Ad-hoc agent planning leads to inconsistent specs, hallucinated context, and redundant work.

| Tool | Type | Popularity | Fit | Determinism | Notes |
|------|------|-----------|-----|-------------|-------|
| **SpecKit/Specify (recommended)** | Spec Framework | **High** | 10/10 | YAML-first; enforces spec→plan→tasks | GitHub's official tool; active ecosystem; broad adoption |
| SDD Pilot | Spec Framework | Medium | 8/10 | Spec-driven phases + quality gates | VSCode + Windsurf support; strong quality gates; enforces phases |
| FSPEC | Spec Framework | Low | 7/10 | Multi-agent factory; DDD/BDD support | TDD/DDD/BDD focus; example mapping; guardrails; newer |
| spec-driven-steroids | Spec Framework | Low | 6/10 | Simple toolkit; native AI tool integration | Focus on CLI discipline; minimal overhead; less documented |
| Paul (Plan-Apply-Unify Loop) | Framework | Low | 7/10 | Plan-Apply-Unify; quality-over-speed | Claude Code native; roundtable-style; newer |
| spec2ship | Spec Framework | Low | 6/10 | Multi-agent; roundtable collaboration | Claude Code focus; social/collaborative; emerging |

**Recommendation:** Use `SpecKit/Specify` for planning & determinism. Strong ecosystem maturity, broad feature coverage, and active maintenance. Alternatives (SDD Pilot, FSPEC) target specific niches (quality gates, DDD) but require more specialized setup.

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

**Recommendation:** Use `Obsidian` for memory persistence. Large PKM ecosystem, portable markdown, and standard git versioning make it a practical baseline. Alternatives (Basic Memory, SilverBullet) offer better agent integration (MCP) or richer features (scripting); evaluate based on project needs.

---

### Pillar 4: Autonomy & Code Understanding

**Problem:** Agents can't answer code questions without scanning files; no architectural understanding; clarifications burn tokens.

| Tool | Type | Popularity | Fit | Autonomy | Notes |
|------|------|-----------|-----|----------|-------|
| **lat.md (recommended)** | Code Analysis | Medium | 10/10 | Pluggable extractors; fast incremental queries; framework-aware | Strong fit for agent workflows; lower token cost; faster queries |
| codebase-memory-mcp | Code Analysis | Low | 9/10 | MCP server; persistent knowledge graph; zero deps | Broad language support; fast queries; high-performance; Cypher support |
| Joern | Code Analysis | Medium | 7/10 | Code property graph; multi-language; dataflow | Academic-grade; C/C++/Java focus; more complex; strong dataflow |
| Pylance | Code Analysis | **High** | 6/10 | Python-specific; language server; fast | Python community standard; not agent-optimized; limited to Python |
| Legacy markdown indexers | Code Analysis | Low | 5/10 | Markdown vault output; human-browsable | Legacy; outputs readable docs; inefficient for agent queries |
| codeflow | Visualization | Low | 4/10 | Browser-based; D3.js visualization; GitHub-linked | Great for humans; not agent-efficient; one-off analysis |

**Recommendation:** Use `lat.md` for autonomy & code understanding. It fits agent workflows well through fast queries and impact analysis. Alternative: `codebase-memory-mcp` (slightly better architecture, newer, zero dependencies) for high-performance scenarios.

---

### Recommended Baseline Toolset for Spekificity

**Decision:** For each pillar, recommend the tool that best combines popularity, maturity, and cohesive fit with Spekificity's architecture.

| Pillar | Tool | Fit | Rationale |
|--------|------|-----|-----------|
| Token Efficiency | Caveman | 9/10 | Simple notation; preserves code; tested across tools |
| Determinism | SpecKit/Specify | 10/10 | YAML-first; GitHub official; broadly adopted |
| Persistence | Obsidian | 10/10 | Largest PKM community; markdown portable; git-backed |
| Autonomy | lat.md | 10/10 | Strong fit for agent workflows; lower token cost; fast queries |

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
- **Autonomy:** codebase-memory-mcp (emerging; better than lat.md for high-performance scenarios)

**Best for:** Teams running frequent agent cycles; large codebases >500 files

---

#### **Use Case 3: Ecosystem-Focused (GitHub, Enterprise)**
- **Token Efficiency:** Caveman (internal Spekificity compression skill)
- **Determinism:** SpecKit/Specify (GitHub official; enterprise ready)
- **Persistence:** Obsidian + git (enterprise-friendly)
- **Autonomy:** lat.md (standard; good GitHub integration)

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
| **Dataflow analysis needed** | Add Joern alongside lat.md |
| **Team already uses SilverBullet** | Replace Obsidian (compatible via markdown export) |
| **Python-only codebase** | Pylance sufficient for autonomy; skip lat.md |
| **100+ files, deep history** | Consider codebase-memory-mcp for extreme scale scenarios |
| **Offline-first requirement** | Ensure all tools work locally; Obsidian + lat.md do; verify others |

---

### Conclusion

**Spekificity's recommended toolset balances popularity, maturity, and cost-effectiveness:**
- `Caveman` — sufficient compression; mature; no setup friction
- `SpecKit/Specify` — strong baseline; active ecosystem; broad community adoption
- `Obsidian` — de facto PKM standard; markdown portable; proven at scale
- `lat.md` — strong fit for agent workflows; recommended for teams doing frequent cycles

**Alternatives exist for each pillar; use matrix above to evaluate against your constraints.**
- **Projects that need both intent + structure understanding**

---

## Decision 4: Zettelkasten Architecture for Vault Notes

### Decision

**Recommendation:** We strongly recommend adopting Zettelkasten conventions for vault notes: atomic notes (one concept per file), YAML frontmatter with metadata (title, type, tags, status, created, updated, source, related), filename kebab-case, and a suggested wikilink density (2-4 links per note). These conventions enable reliable automation (auto-tagging, graph exports, and AI-friendly context injection).

If a project cannot adopt the full convention immediately, the automation features will still work with less-structured markdown, but some tooling (auto-tagging, graph visualizations, and automated lesson extraction) may be degraded. We provide migration guidance and helper scripts for teams that want to progressively adopt these conventions.

---

### Rationale

#### Problem: Knowledge Fragmentation

Without atomic structure:
- Notes sprawl across multiple topics (hard to find)
- Metadata lost (creation dates, update history)
- Cross-references manual (time-consuming, incomplete)
- Context duplication (same pattern described 5 ways)

#### Zettelkasten Solution

**Atomicity:** One concept per file ensures:
- Clear scope (reader knows what file answers)
- Searchability (title + tags precise)
- Composability (can nest concepts via wikilinks)
- Reusability (patterns applicable to multiple features)

**YAML Frontmatter:** Standardized metadata enables:
- Status tracking (active, deprecated, superseded)
- Discovery via tags (grep, Obsidian search)
- Audit trail (created, updated dates)
- Relationship mapping (related notes)

**Wikilink Density:** 2-4 links per note creates:
- Knowledge graph (visual discovery in Obsidian)
- Cross-domain discovery (auth pattern links to error handling pattern)
- Prevents silos (patterns interconnected, not isolated)
- Future AI queries (lat.md can traverse links)

#### Historical Context

This approach is validated from:
- Obsidian PKM community standards
- Luhmann's zettelkasten method (1900s; still effective)
- Andrej Karpathy's LLM Wiki pattern (2025; AI-native knowledge base)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| More files (not one monolithic doc) | Discoverability + atomicity outweigh file count overhead |
| Frontmatter overhead | Small one-time cost; enables automation (auto-tagging) |
| Enforced naming (kebab-case) | Consistency across vault enables grep/automation |
| Wikilink density requirement | Forces meaningful cross-references; prevents orphaned notes |

---

### When to Use

- All vault notes (decisions, patterns, lessons, guides)
- Any note that should persist beyond single feature
- Any note intended for team discovery
- Any content meant for future AI queries

### When NOT to Use

- Session logs (ephemeral; deleted after feature) → ❌ Use temporary format
- Raw implementation drafts (temporary scratchpad) → ❌ Use `/memories/session/`
- Code comments (live in source) → ✅ Use code, not vault
- Ad-hoc notes (single-use) → ❌ Don't persist to vault

---

## Decision 5: Auto-Tagging & Auto-Wikilink Insertion

### Decision

**Automate 70%+ of wikilink insertion and tag generation by implementing keyword extraction → vault mapping → auto-insert pipeline, enabled by default in `/spek.conclude` lesson generation step.**

---

### Rationale

#### Problem: Manual Linking Burden

Without automation:
- Every lesson requires manual cross-referencing (~5-10 min per lesson)
- Cross-references incomplete (patterns missed)
- Redundancy undetected (lesson duplicates prior pattern)
- Tags manually added (inconsistent naming)

#### Auto-Linking Solution

**Keyword Extraction + Vault Mapping:**
- Extract keywords from generated lesson (NLP + pattern matching)
- Map keywords to existing vault entries (semantic matching, configurable)
- Insert wikilinks automatically (no manual work)
- Generate tags from keywords (consistent naming)

**Benefits:**
- Saves ~70% of manual linking labor
- Detects redundancy (alerts if lesson duplicates vault pattern)
- Prevents orphaned patterns (all notes interconnected)
- Enables auto-discovery (wikilinks make patterns discoverable)

- **Configuration:**
- `.spek/config.yaml` contains keyword-to-tag mappings
- Per-project customization (teams can add domain-specific keywords)
- Scoring threshold configurable (match confidence 0-1)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Config file complexity | Upfront cost (~1 hour) pays off after 3-5 features |
| False positives (wrong links) | Override mechanism exists; user can remove incorrect links |
| NLP accuracy limits | 75% confidence threshold catches most; 25% manual review acceptable |
| New dependency (keyword extraction) | Lightweight; no external service calls; works offline |

---

### When to Use

- During `/spek.conclude` lesson generation (enabled by default)
- Any time vault notes are created programmatically
- For reducing manual cross-reference work

### When NOT to Use

- Manual vault note creation (disable auto-linking; edit by hand)
- Highly specialized domain (before config tuned) → review links before committing
- Small projects with <10 notes (overhead > benefit)

---

## Decision 6: 3-Layer Query Rule (Hierarchical Context Loading)

### Decision

**Enforce 3-layer query hierarchy: (1) Code Graph (indexed, fast, ~280 tokens), → (2) Vault (searchable, ~500 tokens), → (3) Raw Code Files (full scan, ~5000+ tokens). Prioritize lower layers; only escalate when necessary.**

---

### Rationale

#### Problem: Token Bloat from File Scanning

Without hierarchy:
- Every code question triggers full file scan (2000-5000 tokens per query)
- Context window fills with implementation details
- Agent cannot reason efficiently (noise >> signal)

#### 3-Layer Solution

**Layer 1 — Code Graph:**
- Pre-indexed symbol definitions, relationships, types
- Query cost: ~280 tokens (symbol info only, no file content)
- Use for: "Who calls this function?" "What changed in this module?"
- Result: Instant, deterministic, no ambiguity

**Layer 2 — Vault:**
- Architecture decisions, patterns, lessons, integration context
- Query cost: ~500 tokens (searchable summaries)
- Use for: "Why did we choose this pattern?" "What patterns work for X?"
- Result: Architectural intent, not implementation details

**Layer 3 — Raw Code:**
- Full source files, comments, test cases
- Query cost: ~5000+ tokens per file
- Use ONLY when Layers 1-2 insufficient
- Example: "Debug this error; show full stack trace"

**Token Savings:**
- Typical agent workflow: 5 queries
- With files: 5 × 5000 = 25,000 tokens
- With 3-layer rule: (3 × 280) + (2 × 500) = 1840 tokens
- **Savings: ~86% token reduction**

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Requires lat.md setup | One-time cost (~30 min); saves tokens every session thereafter |
| Requires vault context | Architectural decisions must be documented first |
| Misses implementation details | By design; saves tokens; details available in Layer 3 if needed |
| User discipline needed | Follow 3-layer rule consistently; document rationale when escalating |

---

### When to Use

- Every `/spek.context` load (query graph first)
- Every `/spek.plan` phase (use layers in order)
- Every `/spek.implement` debugging session
- Large codebases (>100 files)

### When NOT to Use

- Projects <10 files (overhead of maintaining graph > benefit)
- Codebases with no architectural decisions (can't use Layer 2; use Layers 1 + 3)
- Codebases without pre-indexed symbols (use Layers 2 + 3 as fallback)

---

## Decision 7: Git Hooks Integration for Automatic Graph Refresh

### Decision

**Enable automatic code graph refresh via git post-commit hook (optional but recommended). Graph updates incrementally on every commit, ensuring `/spek.context` Layer 1 queries always reflect current code state.**

---

### Rationale

#### Problem: Stale Code Graph

If auto-sync (file-watcher) and git hooks are disabled:
- The code graph may become stale after edits (user must manually refresh)
- `/spek.context` queries may return outdated structure
- An agent could make decisions based on stale code state

Note: Spekificity's supported default, lat.md, provides a file-watcher-based auto-sync and supports the optional git post-commit hook described below; enabling either ensures `/spek.context` Layer 1 queries reflect current code state. Manual refresh is only required when auto-sync and hooks are intentionally disabled.

#### Git Hook Solution

**Auto-Sync Strategy:**
- Git post-commit hook runs `lat update` after every commit
- Only changed files re-indexed (incremental, fast: 2-4 seconds)
- Graph stored in SQLite; queries instant
- No user intervention required

**Benefits:**
- Code graph always fresh (layer 1 queries accurate)
- Transparent to user (runs in background)
- Incremental updates (fast; only changed files)
- Optional (users can disable if conflicts with workflow)

**Implementation:**
- `/spek/bin/spek setup` installs hook automatically
- User can disable via flag: `.spek/.disable-git-hooks`
- Works with CI/CD (hook runs locally only)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Git hook overhead (~2-4s per commit) | Negligible; background refresh; more than offset by query speed |
| Potential hook conflicts | Rare; hook exits quickly; can be disabled if issues arise |
| Graph storage (SQLite on disk) | Small footprint (~5-50MB depending on codebase size) |
| Requires lat.md installed | lat.md + MCP already required for Layer 1 queries |

---

### When to Use

- Production codebases (>100 files)
- Long-lived features (>1 day)
- Frequent implementation cycles
- Teams using lat.md for Layer 1 queries

### When NOT to Use

- Temporary sandboxes (manual refresh acceptable)
- Projects where commit frequency extremely high (>100/day; consider batch refresh)
- Environments where `.git/hooks` restricted (corporate policies)

---

## Decision 8: Backprop Reflex (Test Failures → Vault Updates)

### Decision

**Automatically capture test failure patterns at feature end and update vault with warnings/lessons. Test failures feed backward into decisions, preventing repeat mistakes across features.**

---

### Rationale

#### Problem: Forgotten Lessons from Test Failures

Without automation:
- Test failures discovered, fixed locally
- Lessons not captured (knowledge lost)
- Same mistake repeated in future features
- Time wasted on repeated failures

#### Backprop Reflex Solution

**Failure → Learning Loop:**
1. `/spek.conclude` Step 3 runs automated test failure analysis
2. Parses failure output (error messages, stack traces, assertions)
3. Extracts failure patterns (race condition, timeout, assertion, etc.)
4. Updates vault with failure warnings (appended to related decisions/patterns)
5. Tags future specs with failure pattern cautions (prevents repeats)

**Example:**
```
Feature: auth-refactor
Test Failure: "Race condition in concurrent token refresh"

Backprop captures:
  → Failure Type: race_condition
  → Pattern: concurrent-access
  → Related Decision: use-singleton-pattern
  → Lesson: "Singleton pattern + concurrent access = race risk"
  → Vault Update: [[singleton-pattern]] gets warning about concurrency

Future features proposing singleton automatically see warning.
```

**Benefits:**
- Failures documented (become permanent knowledge)
- Patterns visible to future features (warnings prevent repeats)
- Feedback loop closed (mistakes → learning → better specs)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Requires test infrastructure | Assume existing (Jest/Mocha/pytest); no new setup |
| Parsing overhead | Minimal (~50-100ms per feature end) |
| False positives possible | Manual review before committing warnings; can override |
| Schema changes to vault | Minor (add tags/notes; no breaking changes) |

---

### When to Use

- Features with automated test suites
- Long-lived projects (>5 features) where lessons accumulate
- Teams seeking continuous improvement from failures

### When NOT to Use

- Projects with manual testing only (not automated)
- One-off projects (no future features to learn from)
- Early prototype stages (failures expected; lessons premature)

---

## Decision 9: RARV Reflection Cycles (Reason-Act-Reflect-Verify)

### Decision

**After implementation completes, optionally run RARV (Reason-Act-Reflect-Verify) cycle to detect spec drift. RARV compares code against original spec/plan, flags deviations, allows user to fix code OR justify deviation in vault, then re-validates architectural alignment.**

---

### Rationale

#### Problem: Spec Drift (Implementation Diverges from Spec)

Without reflection:
- Code evolves; spec stays static
- Implementation scope creeps beyond spec
- Architecture diverges from plan (without justification)
- Team confusion (code and spec are inconsistent)

#### RARV Solution

**4-Phase Cycle:**

1. **REASON:** Code vs. Spec comparison
   - Extract original spec requirements
   - Extract actual implemented features
   - Identify deviations (additions, omissions, architecture divergence)
   - Output: "Code is 95% aligned; 3 additions, 1 omission, 1 architecture change"

2. **ACT:** User chooses response for each deviation
   - Option A: Fix code to match spec
   - Option B: Update spec to justify deviation
   - Option C: Defer to tech debt (document + continue)

3. **REFLECT:** Update decisions if justified
   - If Option B chosen: Update vault decision with new rationale
   - Capture why deviation was necessary
   - Learn from the change

4. **VERIFY:** Re-validate architectural alignment
   - Check that updated decisions still align with business goals
   - Confirm no contradictions introduced

**Example:**
```
REASON: Original spec says "Singleton auth service"
        Code implements "Factory pattern auth service"
        Deviation: Architecture change (scope: medium)

ACT: User chooses Option B
     Rationale: "Factory provides better testability; singleton too rigid"

REFLECT: Update vault/decision-auth-service-pattern.md
         New rationale: "Factory pattern for testability + flexibility"
         
VERIFY: Check if factory aligns with "testability-first" goal
        Result: ✓ Aligns; confirms factory was right call
```

**Benefits:**
- Catches spec drift early (before features accumulate deviations)
- Justifies architectural changes (decisions updated, not hidden)
- Prevents surprise departures (all deviations documented)
- Enables learning (spec deviations become future patterns)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Extra step at feature end | Optional; can skip if tight deadline; catches issues early |
| User judgment required | Necessary; RARV surfaces decisions, doesn't make them |
| Requires up-to-date spec | Spec drift detection only works if spec accurate at start |
| Potential rework (Option A) | User decides; may fix code or accept deviation (their call) |

---

### When to Use

- Long features (>1 week) where scope creep likely
- Architectural decisions sensitive (need alignment verification)
- Team size >1 (spec drift compounds with multiple people)
- Production codebases (architecture consistency critical)

### When NOT to Use

- Spike/exploration features (spec intentionally loose)
- Solo developers on greenfield projects (flexibility more important than spec)
- Very short features (<1 day; overhead > benefit)

---

## Decision 10: Anti-Sycophancy Validation Rules

### Decision

**Enforce explicit validation rules that flag contradictions between new decisions and vault, alert on complexity increases without justification, validate technology stack consistency, and prevent AI drift. Violations require documented override or alignment.**

---

### Rationale

#### Problem: AI Hallucinations & Drift

Without validation:
- AI proposes contradiction to vault decision (not caught)
- Spec complexity blooms beyond similar features (no alert)
- New tech introduced without justification (scope bloat)
- Solo developers unaware of drift (no peer review)

#### Anti-Sycophancy Solution

**Rule 1: Contradiction Detection**
- If spec contradicts vault decision → Flag HIGH
- Example: Vault says "Use DI", spec proposes "service locator" → Conflict
- Require user to justify deviation

**Rule 2: Complexity Increases**
- If spec complexity > 50% above similar features → Alert
- Example: Similar feature ~1200 LOC, current spec ~2000 LOC → Justify 67% increase
- Allow override with documented reason

**Rule 3: Pattern Consistency**
- If 3+ recent features used pattern X → Flag deviations
- Example: 3 recent features used observer pattern; spec proposes direct subscription → Suggest observer
- User can override with rationale

**Rule 4: Technology Stack Drift**
- If spec introduces new tech not in vault stack → Alert
- Example: Current stack TypeScript/React/Node; spec proposes Rust → Justify addition
- Prevent tool sprawl

**Implementation:**
- Checks run during `/spek.plan` phases
- Violations logged to `/memories/session/violations.md`
- User can override via flag (documented in session)
- Configuration customizable per project

**Benefits:**
- Catches AI hallucinations early (before they compound)
- Prevents scope creep (complexity justified before spec)
- Maintains technology consistency (no surprise tools)
- Enables learning (override reasons captured for future analysis)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| May slow spec generation | Checks fast (~1-2s per rule); worth early detection |
| False positives possible | Override mechanism exists; documented violations captured |
| Requires tuned thresholds | Per-project config; teams adjust based on their patterns |
| Complexity of rules | Simple rules (threshold-based); easy to understand + debug |

---

### When to Use

- Solo developers (no peer review; need AI guardrails)
- Teams with strict architecture governance
- Projects sensitive to scope creep
- Long-running projects (rules catch drift over time)

### When NOT to Use

- Spike/exploration features (rules too rigid for creative work)
- Greenfield projects (no vault history to contradict)
- Projects with very flexible architecture (rules friction > value)

---

## Decision 11: Blind Code Review (Optional Second-Pass QA)

### Decision

**Optionally run blind code review post-implementation: anonymize code to remove AI markers and context bias, run independent checks (linters, tests, style analysis), and flag AI-specific issues before production deployment.**

---

### Rationale

#### Problem: AI-Generated Code Biases

Without blind review:
- AI-generated code bias invisible (hallucinations, over-reliance on context)
- Context-based errors slip through (code logic sound for given context, but wrong for general case)
- AI markers visible (bias human reviewers; "ah, this is AI, maybe lower bar")
- Duplicate patterns (AI repeats similar solutions; limits diversity)

#### Blind Review Solution

**Anonymization:**
- Strip AI-generation markers (comments mentioning Claude, etc.)
- Remove context bias (feature names, implementation rationale)
- Anonymize service/class names (ServiceA instead of AuthService)
- Keeps: code logic, structure, tests, error handling

**Independent Checks:**
1. Linting (ESLint, Pylint, etc.) — style compliance
2. Tests (all passing? coverage above threshold?)
3. Static Analysis — security, common bugs, performance
4. Complexity — function length, cyclomatic complexity, nesting depth

**Issue Reporting:**
- Flag issues for developer review (not auto-fixed)
- Provide remediation suggestions (actionable)
- Severity levels (CRITICAL, WARNING, INFO)

**Benefits:**
- Catches AI hallucinations (independent check perspective)
- Improves code quality (linting + static analysis enforced)
- Unbiased perspective (anonymization removes context bias)
- Optional (can integrate into CI/CD or run manually)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Extra step before merge | Optional; can skip for rapid iteration; recommended for production |
| Setup effort (GitHub Actions) | ~1 hour one-time; pay-as-you-go thereafter |
| Anonymization overhead | ~100ms per run; minimal compared to CI/CD |
| May flag false positives | Manual review; user decides if flags valid |

---

### When to Use

- Production code (quality gates strict)
- Security-sensitive code (auth, payments, etc.)
- Team code review enabled (feed issues into review)
- Post-implementation before `/spek.conclude`

### When NOT to Use

- Spike code (temporary; quality not critical)
- Solo projects (code ownership clear; review overhead)
- Early stages (move fast; quality gates added later)

---

## Decision 12: Token Budget Model (Soft Limits, Not Hard Caps)

### Decision

**Implement token budget allocation (12K tokens default per feature, configurable) with soft limits (warnings at 60%, 80% thresholds, not hard caps). Track usage per phase; enable cost-aware optimization decisions without blocking progress.**

---

### Rationale

#### Problem: Uncontrolled Token Spending

Without budgets:
- No visibility into token costs per phase
- Expensive phases go unnoticed (bad habits compound)
- Optimization decisions made without data
- Token limits hit unexpectedly (deadline pressure)

#### Token Budget Solution

**Soft Limits Strategy:**
- Allocate 12K tokens per feature (configurable per team)
- Break down per phase: Specify (2K), Plan (3K), Implement (5K), Post (2K)
- Alert at 60% and 80% thresholds (warning, not blocking)
- Track actual usage (report at feature end)

**Per-Phase Tracking:**
```
/spek.plan Specify Phase:
  Budget: 2000 tokens
  Layer 1 queries: 500 tokens
  Layer 2 queries: 1000 tokens
  Spec generation: 300 tokens
  Auto-linking: 200 tokens
  ─────────────────────────────
  Total: 2000 tokens (100% of budget, ON BUDGET)
```

**Soft Limit Behavior:**
- 60% threshold: Log warning "Approaching budget"
- 80% threshold: Alert "80% of budget used; optimize next phase"
- >100% allowed: Continue; discuss why in post-feature review

**Benefits:**
- Visibility into token costs (data-driven optimization)
- Early warning system (avoid budget surprises)
- Flexibility (soft limits, not hard caps; team can exceed if justified)
- Learning loop (budget metrics feed into future improvements)

**Configuration:**
```yaml
token_budget:
  per_feature: 12000  # Adjust based on team budget
  alert_60_percent: true
  alert_80_percent: true
  
# Different teams can customize:
solo_developer: 8000   # Smaller budget
team_collaborative: 15000  # Larger budget
enterprise: 5000  # Cost-sensitive
```

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Soft limits not enforced | By design; team has flexibility; alerts guide discipline |
| Tracking overhead | Minimal (~10-20ms per phase; negligible) |
| Requires monitoring | User reads alerts; can ignore if justified |
| Per-phase granularity | Can add sub-phase tracking if needed (optional) |

---

### When to Use

- Any feature workflow (teams should track token costs)
- Cost-sensitive environments (startups, individuals)
- Long-running projects (costs accumulate; visibility important)
- Teams optimizing for efficiency (3-layer rule + caveman compression)

### When NOT to Use

- Projects with unlimited token budgets (no cost pressure)
- One-off projects (no historical baseline to improve)
- Prototyping stage (move fast; add metrics later)

---

## Decision Tree: Choosing Your Spekificity Approach

### How to Use This Tree

Answer each question from top to bottom. Each path leads to a recommended configuration.

```
START: "Do you use AI agents for development?"

├─ YES → "Is token efficiency critical?"
│  │
│  ├─ YES → "Do you need test-driven development?"
│  │  │
│  │  ├─ YES → Configuration: FULL STACK + TDD
│  │  │  Recommendations:
│  │  │  • Enable all Phase 1-2 decisions (4-12)
│  │  │  • Use 3-layer query rule (Decision 6)
│  │  │  • Enable backprop reflex (Decision 8)
│  │  │  • Enable RARV cycles (Decision 9)
│  │  │  • Use caveman mode for compression
│  │  │  • Budget: 12K tokens per feature
│  │  │  • Best for: Production codebases, TDD teams
│  │  │
│  │  └─ NO → Configuration: TOKEN-OPTIMIZED
│  │     Recommendations:
│  │     • Enable Decisions 6 (3-layer), 10 (anti-sycophancy), 12 (budget)
│  │     • Skip backprop + RARV (TDD not priority)
│  │     • Use caveman mode + 3-layer rule
│  │     • Budget: 12K tokens per feature (strict)
│  │     • Best for: Tight token budgets, non-TDD teams
│  │
│  └─ NO → "Team size?"
│     │
│     ├─ 1 developer → Configuration: SOLO WITH GUARDRAILS
│     │  Recommendations:
│     │  • Enable Decisions 4-5 (zettelkasten, auto-tagging)
│     │  • Enable Decision 10 (anti-sycophancy) [critical for solo dev]
│     │  • Enable Decision 12 (budget tracking)
│     │  • Skip blind review (no team to review)
│     │  • Standard mode (no caveman compression)
│     │  • Budget: 8K tokens per feature
│     │  • Best for: Solo developers, token monitoring
│     │
│     └─ 2-5 developers → Configuration: TEAM BASELINE
│        Recommendations:
│        • Enable Decisions 4-7 (full Phase 1)
│        • Enable Decisions 8-9 (backprop, RARV)
│        • Enable Decision 11 (blind review)
│        • Enable Decision 12 (budget)
│        • Standard mode (caveman optional)
│        • Budget: 15K tokens per feature
│        • Best for: Collaborative teams, shared vault
│

└─ NO → "Is this a production codebase?"
   │
   ├─ YES → "How large is the codebase?"
   │  │
   │  ├─ >500 files → Configuration: MINIMAL AGENT USE
   │  │  Recommendations:
   │  │  • Enable Decision 6 (3-layer) for manual queries
  │  │  • Use lat.md for code analysis (human-driven)
   │  │  • Use Obsidian for vault (human-driven docs)
   │  │  • Skip automated Phase 2 features (not agent-driven)
   │  │  • Manual reviews via blind review
   │  │  • Best for: Human-centric teams with existing tools
   │  │
   │  └─ 100-500 files → Configuration: MANUAL FIRST, AGENT OPTIONAL
   │     Recommendations:
   │     • Zettelkasten vault (Decision 4)
  │     • Manual code analysis + optional lat.md
   │     • Optional auto-tagging (Decision 5)
   │     • No agent workflows yet
   │     • Best for: Teams not ready for full agent integration
   │
   └─ NO → "Is this a greenfield project?"
      │
      ├─ YES → Configuration: FLEXIBLE EARLY STAGE
      │  Recommendations:
      │  • Lightweight: Zettelkasten (Decision 4) + Manual vault
      │  • Skip automated tooling (premature)
      │  • Focus on code quality (tests, basic linting)
      │  • Add agent workflows after 100+ files + stable architecture
      │  • Budget: Not applicable (no agents)
      │  • Best for: New projects, move fast
      │
      └─ NO → Configuration: EXPLORATORY / SPIKE
         Recommendations:
         • Minimal tooling (plain markdown vault if any)
         • No automated workflows
         • Manual code understanding
         • Add structure after exploration confirms direction
         • Best for: Spike code, prototypes, one-off projects
```

---

## Decision Mapping: Decisions → Specifications

### Table Format: Decision ID | Title | Related Specs | Activation Phase

| ID | Title | Related Specs | Phase | When Activated |
|:--:|-------|---------------|-------|---|
| 4 | Zettelkasten Architecture | `zettelkasten-conventions.md` `lessons-format.md` `session-logs-vault-artifacts.md` | Phase 1 | Vault setup; all note creation |
| 5 | Auto-Tagging & Auto-Wikilinks | `auto-tagging-wikilinks.md` `zettelkasten-conventions.md` `session-logs-vault-artifacts.md` | Phase 1 | `/spek.conclude` Step 3 (lesson generation) |
| 6 | 3-Layer Query Rule | `3layer-query-rule.md` `latmd-setup-and-integration.md` `memory-architecture.md` | Phase 1 | `/spek.context` load; `/spek.plan` phases |
| 7 | Git Hooks Integration | `latmd-setup-and-integration.md` Part 5 (git hook config) | Phase 1 | `spek setup`; post-commit execution |
| 8 | Backprop Reflex | `backprop-reflex.md` `spek-lessons-command.md` `integration-validation-and-testing.md` | Phase 2 | `/spek.conclude` Step 3 (lesson generation) |
| 9 | RARV Reflection Cycles | `rarv-reflection.md` `architectural-decisions.md` `feature-state-tracking.md` | Phase 2 | `/spek.conclude` Step 7 (optional; code vs spec analysis) |
| 10 | Anti-Sycophancy Validation | `anti-sycophancy.md` `error-handling-and-recovery.md` `lessons-format.md` | Phase 2 | `/spek.plan` (specify + plan phases) |
| 11 | Blind Code Review | `blind-code-review.md` `integration-validation-and-testing.md` `error-handling-and-recovery.md` | Phase 2 | `/spek.conclude` Step 8 (optional; pre-archival) |
| 12 | Token Budget Model | `token-budget.md` `spek-automate-workflow.md` `spek-map-command.md` | Phase 2 | All phases; tracked throughout feature |

---

### Decision Dependencies

**Prerequisite Chain (required order):**

```
Phase 1 (Foundation):
  Decision 4 (Zettelkasten) 
    ↓ (required by)
  Decision 5 (Auto-Tagging) 
    ↓ (required by)
  Decision 6 (3-Layer Query)
    ↓ (required by)
  Decision 7 (Git Hooks)

Phase 2 (Enhancement):
  Decision 8 (Backprop) — requires Phase 1 foundation
  Decision 9 (RARV) — requires Phase 1 + Decision 8
  Decision 10 (Anti-Sycophancy) — requires Phase 1 foundation
  Decision 11 (Blind Review) — requires Phase 1 + testing infrastructure
  Decision 12 (Token Budget) — independent; can enable anytime
```

**Optional Dependencies:**

```
High-Value Combinations:
  Backprop (8) + RARV (9) → Closed learning loop
  Anti-Sycophancy (10) + Blind Review (11) → AI drift prevention
  3-Layer (6) + Token Budget (12) → Cost-aware optimization
```

---

### Quick Reference: Which Decisions to Enable

**Minimal Setup (Vault + Graph):**
- Decision 4 (Zettelkasten)
- Decision 6 (3-Layer Query)
- Decision 7 (Git Hooks)

**Standard Setup (Vault + Graph + Automation):**
- Decisions 4, 5, 6, 7 (Phase 1 complete)
- Decision 12 (Token Budget)

**Full Stack (All features enabled):**
- Decisions 4-12 (Phase 1 + Phase 2)

**Production-Hardened (Quality + Cost):**
- Decisions 4, 6, 7, 10, 11, 12
- Skip 5, 8, 9 (optional; add if needed)

**Solo Developer Setup:**
- Decisions 4, 6, 10 (zettelkasten, 3-layer, anti-sycophancy)
- Decision 12 (budget tracking)
- Optional: 5, 7 (auto-linking, git hooks)

---

### Conflict Resolution: When Decisions Interact

| Interaction | Resolution |
|-------------|-----------|
| **Anti-Sycophancy (10) flags decision 4 contradiction** | Decision 10 raises alert; user reviews vault + spec; either updates spec or documents override rationale |
| **Backprop (8) + RARV (9) find conflicting failure patterns** | Backprop logs failure; RARV compares to spec; RARV decision takes precedence (architectural); update failure notes accordingly |
| **Blind Review (11) finds issues backprop missed (8)** | Blind review flags issues; if caught by backprop alert, document; if new issue, create tech debt item |
| **Token Budget (12) exceeded during Phase 1** | Warning at 80% threshold; user can continue (soft limit) or optimize; review 3-layer rule usage for Phase 2 |
| **Git Hooks (7) conflict with CI/CD** | Disable hooks via `.spek/.disable-git-hooks`; use CI/CD graph refresh instead |