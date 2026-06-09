# Decisions: Spekificity Architecture & Implementation

Architectural and implementation decisions that guide Spekificity design and tooling choices.

---

# Section 1: Tooling & Architecture

## Decision 1: Recommended Baseline Toolset

### Summary

For each of Spekificity's four pillars, a tool is recommended that balances maturity, community adoption, and cohesive fit:

| Pillar | Tool | Why | Setup |
|--------|------|-----|-------|
| **Token Efficiency** | Caveman (compression) | Simple notation; preserves code; tested | Low (integrated) |
| **Determinism** | SpecKit/Specify | GitHub official; broad adoption; YAML-first | Medium (install + init) |
| **Persistence** | Obsidian (vault) | Largest PKM community; markdown portable; git-backed | Medium (CLI required for all vault R/W; desktop UI optional for visualization) |
| **Autonomy & Code Understanding** | lat.md | Agent-optimized; fast queries; framework-aware | Medium (install + MCP config) |

---

### Tooling Decisions Detail

#### Code Analysis: lat.md is Canonical

**lat.md is the canonical, required indexing tool for Spekificity.** It is the only supported code analysis solution.

**Why:**
- Purpose-built for agent-driven workflows
- Pre-indexed queries (no file scans; low token cost)
- Fast incremental updates (file watcher optional)
- MCP tool interface (agent-friendly)
- Deterministic impact analysis
- Framework-aware extractors

**Status:** lat.md is the ONLY code analysis tool supported by Spekificity. Migration path: If using legacy tools, rebuild index with `lat.md` per [setup.md](setup.md).

---

#### Dual-System Architecture: Vault + Code Analysis

**Recommend dual-system approach: Knowledge Vault + Code Analysis Tool.**

Each system owns a domain and operates on different rhythms:

| System | Purpose | Access | Rhythm |
|--------|---------|--------|--------|
| **Vault** | Knowledge base (specs, decisions, lessons) | Git + UI (optional) | Once per feature cycle |
| **Code Analysis** | Code intelligence (symbols, calls, impact) | MCP tools (agent queries) | Every file save (auto-sync) |

**Why separation?**
- Vault changes slowly; code analysis changes constantly
- Agents query code frequently (per implementation cycle); vault queried once per session
- Vault stays lean + human-navigable; code analysis stays fast + agent-efficient

**Result:** Faster development with pre-indexed analysis and persistent architectural context.

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Multiple tools (not monolithic) | Clear separation; each tool optimized for its domain |
| lat.md required | Agent workflows depend on indexed queries; fallback to grep is manual overhead |
| Setup effort | One-time effort; pays for itself in token efficiency and query speed |
| Obsidian CLI required | All vault reads and writes go through Obsidian CLI; ensures consistent indexing, backlinks, and graph state. Desktop app optional for visualization only. |

---

## Rationale: Agent-First Design

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
| Query Performance | low-latency average (vs. much slower for file scan) |
| **Fit for Agent Workflows** | **high** (purpose-built for this use case) |

---


## Decision 3: Toolset for the Four Pillars

| Pillar | Tool | Why |
|--------|------|-----|
| Token Efficiency | Caveman | Simplest compression; no setup friction; already integrated |
| Determinism | SpecKit/Specify | GitHub official; YAML-first; enforces spec→plan→tasks |
| Persistence | Obsidian | Largest PKM community; portable markdown; git-backed; CLI required |
| Autonomy | lat.md | Purpose-built for agents; pre-indexed MCP queries; deterministic impact analysis |

Alternatives exist for each pillar. These four balance maturity, fit, and setup simplicity for Spekificity's architecture.

---

## Decision 4: Zettelkasten Architecture for Vault Notes (Recommended Default)

### Decision

**Recommendation:** Adopt Zettelkasten conventions as the default for vault notes: atomic notes (one concept per file), YAML frontmatter with metadata (title, type, tags, status, created, updated, source, related), filename kebab-case, and 2-4 wikilinks per note. These conventions enable reliable automation (auto-tagging, graph exports, AI-friendly context injection).

**Fallback:** If a project cannot immediately adopt full Zettelkasten structure, less-structured markdown is supported. Automation features (auto-tagging, graph visualization, lesson extraction) degrade gracefully; no failures, just reduced capability. Migration and helper scripts provided for progressive adoption.

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

**Automate the majority of wikilink insertion and tag generation by implementing keyword extraction → vault mapping → auto-insert pipeline, enabled by default in `/spek.conclude` lesson generation step.**

---

### Rationale


#### Problem: Manual Linking Burden

Without automation:
- Every lesson requires manual cross-referencing (a few minutes per lesson)
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
- Saves the majority of manual linking labor
- Detects redundancy (alerts if lesson duplicates vault pattern)
- Prevents orphaned patterns (all notes interconnected)
- Enables auto-discovery (wikilinks make patterns discoverable)

- **Configuration:**
- `.spek/config.yaml` contains keyword-to-tag mappings
- Per-project customization (teams can add domain-specific keywords)
-- Scoring threshold configurable (use a high confidence threshold by default)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Config file complexity | Upfront cost is small; benefits accrue after a few features |
| False positives (wrong links) | Override mechanism exists; user can remove incorrect links |
| NLP accuracy limits | High-confidence threshold recommended; lower-confidence results require manual review |
| New dependency (keyword extraction) | Lightweight; no external service calls; works offline |

---

### When to Use

- During `/spek.conclude` lesson generation (enabled by default)
- Any time vault notes are created programmatically
- For reducing manual cross-reference work

### When NOT to Use

- Manual vault note creation (disable auto-linking; edit by hand)
- Highly specialized domain (before config tuned) → review links before committing
- Small projects with few notes (overhead may exceed benefit)

---

## Decision 6: 3-Layer Query Rule (Hierarchical Context Loading)

### Decision

**Enforce a 3-layer query hierarchy: (1) Code Graph (indexed, compact), → (2) Vault (searchable summaries), → (3) Raw Code Files (full content). Prioritize lower layers; escalate to deeper layers only when necessary.**

---

### Rationale

#### Problem: Token and Context Bloat from File Scanning

Without hierarchy:
- Full-file scans are comparatively costly and can overload reasoning with implementation details
- Context windows become noisy and impede efficient agent reasoning

#### 3-Layer Solution

**Layer 1 — Code Graph:**
- Pre-indexed symbol definitions, relationships, and types
- Semantic symbol summaries and relationships (minimal content)
- Use for: "Who calls this function?" "What changed in this module?"
- Result: Fast, deterministic answers with low overhead

**Layer 2 — Vault:**
- Architecture decisions, patterns, lessons, and integration context
- Searchable summaries and intent-level context (moderate content)
- Use for: "Why did we choose this pattern?" "What patterns work for X?"
- Result: Architectural intent without implementation noise

**Layer 3 — Raw Code:**
- Full source files, tests, and comments
- Full-file content is expensive to process and should be used sparingly
- Use ONLY when Layers 1-2 do not provide sufficient detail (for deep debugging or full-context reconstruction)

Using the 3-layer rule reduces overall query cost significantly compared to naive full-file scans and preserves useful, intent-focused context for agents.

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Requires lat.md setup | One-time setup effort; saves tokens every session thereafter |
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
- Only changed files re-indexed (incremental, fast)
- Graph stored in SQLite; queries instant
- No user intervention required

**Benefits:**
- Code graph always fresh (layer 1 queries accurate)
- Transparent to user (runs in background)
- Incremental updates (fast; only changed files)
- Optional (users can disable if conflicts with workflow)

**Implementation:**
- `spek init` installs hook automatically
- User can disable via flag: `.spek/.disable-git-hooks`
- Works with CI/CD (hook runs locally only)

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Git hook overhead (short per commit) | Negligible; background refresh; more than offset by query speed |
| Potential hook conflicts | Rare; hook exits quickly; can be disabled if issues arise |
| Graph storage (SQLite on disk) | Small footprint (varies with codebase size) |
| Requires lat.md installed | lat.md + MCP already required for Layer 1 queries |

---

### When to Use

- Production codebases with many files
- Long-lived features
- Frequent implementation cycles
- Teams using lat.md for Layer 1 queries

### When NOT to Use

- Temporary sandboxes (manual refresh acceptable)
- Projects with very high commit frequency (consider batch refresh)
- Environments where `.git/hooks` restricted (corporate policies)

---

---

## Planned Features (Not Yet Implemented)

Decisions 8–12 describe features to build. None are active in the current implementation. They are documented here to preserve the design intent and dependencies.

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
| Parsing overhead | Minimal (per-feature parsing overhead is small) |
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
  - Output: "Code largely aligned; a small number of additions and minor omissions detected"

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

- Long features where scope creep likely
- Architectural decisions sensitive (need alignment verification)
- Team size >1 (spec drift compounds with multiple people)
- Production codebases (architecture consistency critical)

### When NOT to Use

- Spike/exploration features (spec intentionally loose)
- Solo developers on greenfield projects (flexibility more important than spec)
- Spike/short features (overhead > benefit)

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
- If spec complexity is substantially above similar features → Alert
- Example: Compared to a baseline feature size, the current spec is substantially larger — justify the increased scope
- Allow override with documented reason

**Rule 3: Pattern Consistency**
- If multiple recent features used pattern X → Flag deviations
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
| May slow spec generation | Checks are fast; worth early detection |
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
- Strip AI-generation markers (comments mentioning vendor or specific agent names)
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
| Setup effort (GitHub Actions) | One-time setup effort; pay-as-you-go thereafter |
| Anonymization overhead | Minimal per-run overhead; negligible compared to CI/CD |
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

**Implement a configurable token budget model with soft limits and warnings. Track usage per phase to enable cost-aware decisions without blocking progress; exact numeric budgets are team-configurable and not documented as fixed values in public-facing docs.**

---

### Rationale

#### Problem: Uncontrolled Token Spending

Without budgets:
- No visibility into token costs per phase
- Expensive phases go unnoticed (bad habits compound)
- Optimization decisions made without data

#### Token Budget Solution

**Soft Limits Strategy:**
- Allocate a configurable token budget per feature (team-defined)
- Break down the budget per phase according to team preferences
- Configure warning thresholds (non-blocking) to guide optimization
- Track actual usage and report at feature end for learning

**Per-Phase Tracking:**
Use per-phase accounting to capture relative costs for layer queries, spec generation, and automation steps; numeric values are recorded in internal telemetry and omitted from public docs.

**Soft Limit Behavior:**
- Configured warning thresholds issue non-blocking alerts
- Teams may exceed budgets when justified and discuss in post-feature reviews

**Benefits:**
- Visibility into token costs (data-driven optimization)
- Early warning system (avoid surprises)
- Flexibility (soft limits; configurable by team)
- Learning loop (budget metrics feed into future improvements)

**Configuration (example schema):**
```yaml
token_budget:
  per_feature: TBD  # Team-defined
  alert_thresholds: []  # Configure warning thresholds as needed

# Team presets (placeholders)
solo_developer: TBD
team_collaborative: TBD
enterprise: TBD
```

---

### Trade-offs Accepted

| Trade-off | Reasoning |
|-----------|-----------|
| Soft limits not enforced | By design; team has flexibility; alerts guide discipline |
| Tracking overhead | Minimal (small processing time per phase) |
| Requires monitoring | User reads alerts; can ignore if justified |
| Per-phase granularity | Can add sub-phase tracking if needed (optional) |

---

### When to Use

- Any feature workflow (teams should track token costs)
- Cost-sensitive environments (startups, individuals)
- Long-running projects (costs accumulate; visibility important)
- Teams optimizing for efficiency (use 3-layer rule and compression techniques)

### When NOT to Use

- Projects with unlimited token budgets (no cost pressure)
- One-off projects (no historical baseline to improve)
- Prototyping stage (move fast; add metrics later)

---


## Decision Mapping: Decisions → Specifications

### Active

| ID | Title | Related Specs | When Activated |
|:--:|-------|---------------|---|
| 4 | Zettelkasten Architecture | See [architecture.md](architecture.md) and [patterns.md](patterns.md) | Vault setup; all note creation |
| 5 | Auto-Tagging & Auto-Wikilinks | See [patterns.md](patterns.md) (Pattern 10) | `/spek.conclude` Step 3 (lesson generation) |
| 6 | 3-Layer Query Rule | See [architecture.md](architecture.md) | `/spek.context` load; `/spek.plan` phases |
| 7 | Git Hooks Integration | See [setup.md](setup.md) | `spek init`; post-commit execution |

### Planned (see Planned Features section above)

| ID | Title | Related Specs | When Activated |
|:--:|-------|---------------|---|
| 8 | Backprop Reflex | See [decision.md](decision.md#decision-8) | `/spek.conclude` Step 3 (lesson generation) |
| 9 | RARV Reflection Cycles | See [decision.md](decision.md#decision-9) | `/spek.conclude` Step 7 (optional; code vs spec analysis) |
| 10 | Anti-Sycophancy Validation | See [decision.md](decision.md#decision-10) | `/spek.plan` (specify + plan phases) |
| 11 | Blind Code Review | See [decision.md](decision.md#decision-11) | `/spek.conclude` Step 8 (optional; pre-archival) |
| 12 | Token Budget Model | See [patterns.md](patterns.md) (Pattern 22) | All stages; tracked throughout feature |

---

### Decision Dependencies

**Prerequisite Chain (required order):**

```
Foundation:
  Decision 4 (Zettelkasten) 
    ↓ (required by)
  Decision 5 (Auto-Tagging) 
    ↓ (required by)
  Decision 6 (3-Layer Query)
    ↓ (required by)
  Decision 7 (Git Hooks)

Enhancements:
  Decision 8 (Backprop) — requires Decisions 4-7
  Decision 9 (RARV) — requires Decisions 4-7 + Decision 8
  Decision 10 (Anti-Sycophancy) — requires Decisions 4-7
  Decision 11 (Blind Review) — requires Decisions 4-7 + testing infrastructure
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
- Decisions 4, 5, 6, 7
- Decision 12 (Token Budget)

**Full Stack (All features enabled):**
- Decisions 4-12

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
| **Token Budget (12) exceeded** | Warning when approaching the configured budget; user can continue (soft limit) or optimize; review 3-layer rule usage |
| **Git Hooks (7) conflict with CI/CD** | Disable hooks via `.spek/.disable-git-hooks`; use CI/CD graph refresh instead |