# Spekificity FAQ

> **Quick Reference:** Common questions and answers organized by topic

---

## Table of Contents

- [Setup](#setup) (Q1–Q3)
- [Workflow](#workflow) (Q4–Q8)
- [Concepts](#concepts) (Q9–Q13)
- [Troubleshooting](#troubleshooting) (Q14–Q17)
- [Performance & Optimization](#performance--optimization) (Q18–Q20)
- [About Spekificity](#about-spekificity) (Q21–Q22)

---

## Setup

### Q1: What do I need to install before using Spekificity?

**A:** Three core tools:

1. **SpecKit** — Spec-driven workflow engine (global install)
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. **Knowledge Vault** — Obsidian-compatible markdown storage (local to project)
   ```bash
   # Vault is git-backed and stored in wiki/ directory
   # Already set up when you clone the repo
   ```

3. **CodeGraph** — Code intelligence for impact analysis (MCP setup)
   ```bash
   # Installed via MCP protocol; configured in .specify/
   # See setup.md for full configuration
   ```

**Prerequisites:** Python 3.11+, Git, `uv` package manager

**Full walkthrough:** See [setup.md](setup.md) or [quickstart.md](quickstart.md)

---

### Q2: How do I set up Spekificity in an existing project?

**A:** Two options:

**Option 1: Fresh Spekificity setup** (Recommended)
```bash
cd /path/to/project

# 1. Initialize SpecKit (if not already done)
specify init .

# 2. Create knowledge vault structure
mkdir -p wiki/specs wiki/patterns wiki/decisions

# 3. Initialize Spekificity
/spek.init --template=full
```

**Option 2: Gradual migration** (Existing projects with some specs)
```bash
# 1. Import existing documentation
/spek.migrate --from=specs-folder --to=wiki

# 2. Run CodeGraph setup
/spek.setup --tool=codegraph

# 3. Validate and commit
git add wiki/ .specify/
git commit -m "Initialize Spekificity framework"
```

**See also:** [setup.md](setup.md#tool-2-knowledge-vault-local-setup)

---

### Q3: Can I use Spekificity with my favorite IDE (VS Code, PyCharm, etc.)?

**A:** Yes! Spekificity works with any text editor, but **VS Code is recommended** for:

- ✅ Copilot integration (GitHub Copilot can invoke /spek.* skills)
- ✅ Markdown preview (read specs in vault easily)
- ✅ Git integration (stage/commit from editor)
- ✅ MCP support (CodeGraph queries in real-time)

**For PyCharm, Vim, or other editors:**
- All commands work from terminal (not in editor)
- Use `/spek.*` and `/speckit.*` commands directly
- Vault is just markdown files (view anywhere)

---

## Workflow

### Q4: What are the 5 phases of Spekificity workflow?

**A:**

1. **Prepare** (`/spek.prepare`) — Git clean, vault fresh, CodeGraph synced (5 min)
2. **Specify** (`/spek.automate --phase=specify`) — Create detailed spec with enrichment (15 min)
3. **Plan** (`/spek.automate --phase=plan`) — Break spec into tasks, map dependencies (10 min)
4. **Implement** (`/spek.implement`) — Execute tasks with full context (1–4 hours)
5. **Close** (`/spek.post`) — Archive results, capture lessons, refresh state (5 min)

**Total time for one feature:** ~2 hours (including implementation)

**See also:** [workflow.md](workflow.md), [quickstart.md](quickstart.md#phase-1-prepare-your-workspace-5-min)

---

### Q5: Do I have to use all 5 phases, or can I skip some?

**A:** All phases are recommended, but can be used flexibly:

**Best practice:**
```bash
# Use automation for Prepare → Specify → Plan
/spek.automate --all

# Then manually implement
/spek.implement
```

**Quick mode (skip planning):**
```bash
/spek.prepare
/spek.automate --phase=specify
# Implement directly (less guidance, higher risk)
/spek.implement
```

**Custom workflows:**
```bash
# Run only Prepare
/spek.prepare

# Manually write spec (no automation)
vim wiki/specs/my-feature.md

# Run Plan phase with your custom spec
/spek.automate --phase=plan --spec=wiki/specs/my-feature.md
```

**⚠️ Warning:** Skipping Prepare can cause stale context (outdated CodeGraph, vault conflicts). Not recommended.

---

### Q6: What's the difference between `/spek.*` and `/speckit.*` commands?

**A:** Two layers of the same workflow:

| Command | Purpose | Context Injection | Use When |
|---------|---------|-------------------|----------|
| `/speckit.specify` | Raw spec generation | None (plain SpecKit) | You want minimal tooling |
| `/spek.automate --phase=specify` | **Enriched** spec generation | Vault decisions, patterns | You want project context |
| `/speckit.plan` | Raw plan generation | None | Building a standalone spec |
| `/spek.automate --phase=plan` | **Enriched** plan generation | CodeGraph, vault context | You want impact analysis |

**Pattern: Decorator-Wrapper**

```
/spek.* commands = /speckit.* + enrichment layers

[Enrichment Layer]
      ↓
[/speckit command]
      ↓
[Output]
```

Enrichment layer injects:
- ✅ Vault decisions and patterns
- ✅ CodeGraph code analysis
- ✅ Project-specific naming conventions
- ✅ Lessons learned from similar features

**See also:** [patterns/decorator-wrapper-pattern-quick-ref.md](patterns/decorator-wrapper-pattern-quick-ref.md)

---

### Q7: Can I work on multiple features in parallel?

**A:** Not recommended for same agent, but possible with workflows:

**Parallel work (different agents/people):**
```bash
# Agent A: Feature 1
git checkout -b feature-1
/spek.prepare
/spek.automate --phase=specify --feature="Feature 1"

# Agent B: Feature 2 (different branch)
git checkout -b feature-2
/spek.prepare
/spek.automate --phase=specify --feature="Feature 2"
```

**Parallel tasks within same feature:**
```bash
# After Planning, you can parallelize independent tasks
# (not all tasks are sequential)

/spek.implement --task=2 --parallel
# while
/spek.implement --task=4 --parallel
```

**Not parallel:**
```bash
# Don't run multiple /spek.prepare on same branch
# Don't run /spek.implement twice simultaneously
# CodeGraph syncs conflict if modified files overlap
```

**See also:** [specs/multi-developer-coordination.md](../specs/multi-developer-coordination.md)

---

### Q8: What happens if I make a mistake during implementation (Task 2 is wrong)?

**A:** Easy to recover:

```bash
# 1. Identify the task that went wrong
/spek.implement --status

# 2. Undo that task (revert git commit)
git reset --soft HEAD~1
git checkout -- .

# 3. Restart from that task
/spek.implement --restart-task=2

# OR fix it manually and continue
# (mark task 2 as done when ready)
/spek.implement --next
```

**For major issues:**
```bash
# Abort entire feature
/spek.post --abort

# This rolls back spec, plan, and implementation
# (git resets to initial branch point)
```

---

## Concepts

### Q9: What's "Enrichment" and why does it matter?

**A:** Enrichment = **context injection from your vault before execution**.

**Without enrichment (raw SpecKit):**
```
User: "Add authentication"
→ SpecKit generates generic spec (has to guess your conventions)
→ Output: Spec looks like it could be for any project
```

**With enrichment (/spek.automate):**
```
User: "Add authentication"
→ /spek loads vault:
   - Decisions: "We use JWT tokens" (Decision 7)
   - Patterns: Error handling pattern (vault/patterns)
   - Lessons: "We tried OAuth last time" (learned)
→ /speckit.specify runs *with* that context
→ Output: Spec is specific to your project
```

**Why it matters:**

- ✅ Less agent reasoning (facts are injected, not guessed)
- ✅ Fewer tokens (agents don't search for context)
- ✅ Better consistency (all features follow project patterns)
- ✅ Faster implementation (decisions already made)

**See also:** [architecture.md](architecture.md#enrichment-layer), [patterns/enrichment-layer-pattern-quick-ref.md](patterns/enrichment-layer-pattern-quick-ref.md)

---

### Q10: What's Caveman mode and when should I use it?

**A:** **Caveman = compressed responses.** Reduces token usage by ~75%.

**Normal response:**
```
The authentication endpoint should validate the user's credentials 
against the database using bcrypt for password verification. This ensures 
security and compatibility with existing account systems. The implementation 
should follow RESTful conventions...

(Tokens: ~200)
```

**Caveman response:**
```
Auth endpoint: validate creds + hash w/ bcrypt. RESTful.

(Tokens: ~50)
```

**When to use:**

- ✅ Token budget is tight (< 20% remaining)
- ✅ You need quick answers, not detailed explanations
- ✅ You're on the 4th+ feature (you understand patterns)
- ❌ First feature (you need detailed guidance)
- ❌ Complex specs with many edge cases

**How to enable:**

```bash
# Globally for a feature
/spek.implement --caveman

# For specific task
/spek.implement --task=4 --caveman

# Toggle in config
echo "caveman_mode: true" >> .specify/config.yml
```

**See also:** [patterns/caveman-compression-mode-quick-ref.md](patterns/caveman-compression-mode-quick-ref.md)

---

### Q11: Why use CodeGraph instead of Graphify?

**A:** CodeGraph is **10x more efficient for agent workflows**.

| Factor | CodeGraph | Graphify | Impact |
|--------|-----------|----------|--------|
| **Query speed** | 100ms (pre-indexed) | 2000ms+ (file scan) | Faster impl |
| **Token cost** | ~250 tokens/5 queries | ~2500 tokens/5 queries | 10x cheaper |
| **Impact analysis** | Built-in (graph queries) | Manual (agent reasoning) | Less uncertainty |
| **Sync latency** | Automatic, real-time | Manual (`graphify run`) | Always fresh |
| **MCP support** | ✅ Native | ❌ Not available | Better integration |

**Decision made:** CodeGraph only (effective 2026-05-20)

**Migration:** Existing Graphify users should rebuild with CodeGraph.

**See also:** [decision.md#decision-1](decision.md#decision-1-code-analysis-tool-codegraph-only--final)

---

### Q12: What's stored in the knowledge vault and why is it important?

**A:** The vault stores **durable project knowledge** across sessions:

| Content | Purpose | Example |
|---------|---------|---------|
| **Specs** | Feature definitions | `wiki/specs/user-auth.md` |
| **Plans** | Task breakdowns | `wiki/plans/user-auth-plan.md` |
| **Decisions** | Why we chose X over Y | `wiki/decision.md#decision-7` |
| **Patterns** | Reusable solutions | `wiki/patterns/error-handling.md` |
| **Lessons** | What we learned | `wiki/todo.md#lessons` |

**Why it matters:**

- 🔄 **Continuity:** New agent can understand project history
- 📚 **Reuse:** Copy patterns from similar features
- 🤝 **Collaboration:** Multiple developers, same context
- 💾 **Durability:** Knowledge survives team changes
- 📊 **Audit trail:** Why decisions were made (not just what)

**All vault content is Git-backed** (version-controlled, Obsidian-compatible)

**See also:** [intention.md#context-lives-in-the-vault](intention.md#project-tenets)

---

### Q13: Can I use Spekificity for non-agent development (manual development)?

**A:** **Yes!** Spekificity works for any structured development:

**Use Spekificity for:**
- ✅ AI agent workflows (primary use case)
- ✅ Manual solo development (persistent memory helps)
- ✅ Team projects (shared vault, decisions)
- ✅ Complex features (specs, plans prevent mistakes)

**Less ideal for:**
- ❌ One-off bugfixes (overkill)
- ❌ Very rapid prototyping (specs slow you down)
- ❌ Projects without code graphs (impact analysis less useful)

**Manual workflow:**
```bash
# 1. Manual setup (no /spek.* commands)
# 2. Write spec in vault/specs/ manually
# 3. Write plan manually or use /speckit.plan
# 4. Implement using vault for reference
# 5. Commit and capture lessons manually
```

**Hybrid (recommended):**
```bash
# Use Spekificity for big features (specs, plans, lessons)
# Skip for small hotfixes

/spek.prepare  # Always safe to run
/spek.automate --phase=specify --feature="Add auth"  # Yes
# vs
# Small fix: git checkout -b fix/typo, edit file, commit, push
```

---

## Troubleshooting

### Q14: My /spek.prepare fails with "vault not synced" — how do I fix it?

**A:**

```bash
# 1. Check git status
git status
# If it shows vault/ conflicts, resolve them

# 2. Manually pull vault updates
git pull origin main

# 3. Retry prepare
/spek.prepare

# 4. If still fails, force refresh
/spek.prepare --force-codegraph-refresh
```

**Prevention:**
- Run `/spek.prepare` before starting each feature
- Commit any vault changes before switching branches

---

### Q15: CodeGraph shows outdated code references — how do I refresh it?

**A:**

```bash
# Quick refresh (incremental)
/spek.prepare

# Full refresh (rebuilds from scratch)
/spek.prepare --force-codegraph-refresh

# Manual refresh via MCP
codegraph rebuild
codegraph refresh
```

**Why it happens:**
- CodeGraph syncs on file changes
- If you've made many rapid edits, it may lag
- Switching branches can cause stale cache

---

### Q16: I ran out of tokens mid-implementation — what do I do?

**A:**

**Option 1: Continue in new session (Recommended)**
```bash
# Current session: commit what you've done
git commit -am "WIP: tasks 1-3 complete"

# New terminal/session:
/spek.prepare
/spek.implement --resume user-auth-api --task=4
```

**Option 2: Enable Caveman mode**
```bash
# Compress remaining output
/spek.implement --caveman --next
```

**Option 3: Checkpoint and continue**
```bash
# Mark current task as complete
git commit -m "Task 3 complete: implement login validation"

# Continue in background (async)
/spek.implement --next &
```

**Prevention:**
- Check token budget early: `/spek.status --tokens`
- Use `--tokens=20000` flag to set conservative limit
- Enable Caveman mode proactively on feature 3+ (you understand patterns)

---

### Q17: Spec/Plan was wrong and I need to fix it mid-implementation — what do I do?

**A:**

```bash
# 1. Pause implementation
git commit -am "WIP: paused at task 3"

# 2. Fix spec or plan
vim wiki/specs/my-feature.md
# or
vim wiki/plans/my-feature-plan.md

# 3. Commit the fix
git add wiki/
git commit -m "Fix spec: clarify token claims structure"

# 4. Regenerate plan (if you changed spec)
/spek.automate --phase=plan --spec=wiki/specs/my-feature.md

# 5. Decide: restart or continue?
# Option A: Restart from beginning
/spek.implement --restart

# Option B: Continue from current task (if issue doesn't affect it)
/spek.implement --next
```

**Lessons learned:** Specs are easier to fix before implementation. Spend 5 extra minutes on spec review to avoid this.

---

## Performance & Optimization

### Q18: How do I check my token usage and budget?

**A:**

```bash
# Check current session
/spek.status --tokens

# Expected output:
# Session tokens used: 23,400 / 50,000 (47%)
# Remaining: 26,600
# Estimated tokens for remaining tasks: 8,000
# Status: ✓ GREEN

# View budget config
cat .specify/config.yml | grep token_budget

# Set custom budget
echo "token_budget: 75000" >> .specify/config.yml
```

**Conservative defaults:**
- Per-session: 50,000 tokens (for whole feature)
- Per-task: 5,000 tokens (average)
- With Caveman mode: ~75% reduction

---

### Q19: My implementation is taking much longer than planned — how do I optimize?

**A:**

**Check what's taking time:**
```bash
/spek.implement --metrics

# Output:
# Task 1: Prepare environment — 15 min (est. 15 min) ✓
# Task 2: Design schema — 45 min (est. 20 min) ⚠
# Task 3: Validation — 25 min (est. 30 min) ✓
# Task 4: Endpoint — 30 min (est. 20 min) ⚠
```

**Optimization strategies:**

1. **Skip unnecessary detail** → Enable Caveman mode
   ```bash
   /spek.implement --caveman
   ```

2. **Use CodeGraph to avoid manual analysis** (don't re-scan affected files)
   ```bash
   codegraph_callers "auth_service.validate_credentials"
   # Use this instead of manually reading code
   ```

3. **Batch similar tasks**
   ```bash
   # Instead of: Task → commit → Task → commit
   # Do: Task → Task → Task → commit (batch)
   ```

4. **Reuse patterns from vault**
   ```bash
   # Check if similar feature exists
   find wiki/specs -name "*.md" | xargs grep -l "validation"
   # Copy/adapt instead of rewriting
   ```

---

### Q20: How do I reduce tokens while keeping context?

**A:**

**Tier 1: Low-hanging fruit**
- ✅ Use Caveman mode after task 2 (you understand patterns)
- ✅ Enable CodeGraph queries (faster than agent reasoning)
- ✅ Batch commits (fewer git diffs to load)

**Tier 2: Aggressive optimization**
- ✅ Read vault patterns directly (don't ask agent)
- ✅ Use `/spek.implement --no-scaffold` (less guidance, fewer tokens)
- ✅ Implement tasks in order (CodeGraph context accumulates)

**Tier 3: Advanced**
- ✅ Custom enrichment layers (inject only necessary context)
- ✅ Session checkpointing (split feature across multiple sessions)
- ✅ Graph pruning (remove unrelated code from context)

**Typical savings:**

| Strategy | Tokens Saved | Notes |
|----------|--------------|-------|
| Caveman mode | ~75% | After task 2 |
| CodeGraph queries | ~30% | Instead of agent scanning |
| Batch commits | ~15% | Fewer diffs per task |
| Total possible | ~70% | Combining strategies |

---

## About Spekificity

### Q21: Is Spekificity free? What's the license?

**A:** **Yes, Spekificity is free and open-source.**

**License:** MIT License  
**Copyright:** © 2026 Marcel Rienks  
**Restrictions:** None (MIT is permissive)

You can:
- ✅ Use freely (commercial or personal)
- ✅ Modify and distribute
- ✅ Include in your projects
- ⚠️ Include attribution (recommended, not required)

See [LICENSE](../LICENSE) for full text.

---

### Q22: How is Spekificity different from other workflow tools?

**A:**

| Feature | Spekificity | SpecKit | CodeGraph | Obsidian |
|---------|-------------|---------|-----------|----------|
| **Spec-first workflow** | ✅ | ✅ | ❌ | ❌ |
| **Code analysis** | ✅ (CodeGraph) | ❌ | ✅ | ❌ |
| **Knowledge vault** | ✅ | ❌ | ❌ | ✅ |
| **Composable skills** | ✅ | ❌ | ❌ | ❌ |
| **Token efficiency** | ✅ (focus) | ⚠ | ✅ | ⚠ |
| **Deterministic workflows** | ✅ | ⚠ | ❌ | ❌ |
| **Multi-phase orchestration** | ✅ | ❌ | ❌ | ❌ |

**Key difference:** Spekificity **integrates** these tools into a complete workflow, rather than replacing them.

```
Spekificity = SpecKit (specs/plans)
             + CodeGraph (code intelligence)
             + Obsidian Vault (knowledge)
             + /spek.* orchestration
             + Enrichment layers
```

---

## Still Have Questions?

- 📖 **Read [wiki/workflow.md](workflow.md)** — Detailed workflow phases
- 🚀 **Follow [wiki/quickstart.md](quickstart.md)** — Step-by-step guide
- 🏗️ **See [wiki/architecture.md](architecture.md)** — System design
- 💡 **Check [wiki/intention.md](intention.md)** — Project philosophy
- 📋 **Browse [wiki/patterns/](patterns/)** — Common patterns

Or open an issue in the repository!
