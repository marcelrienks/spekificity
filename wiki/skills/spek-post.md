# Skill: `spek.post`

## Purpose

Finalize feature work by capturing lessons learned, compressing outputs for token efficiency, refreshing code analysis tool with new code, and updating vault context with new patterns and decisions discovered during the feature.

**Outcome:** Feature is complete, lessons are persistent, code graph is current, vault context enriched for next feature.

---

## Workflow

```
1. Collect feature artifacts (spec.md, tasks.md, plan.md, execution trace)
2. Activate caveman mode for compression
3. Generate structured lessons learned
4. Update vault context (decisions.md, patterns.md)
5. Run code analysis tool in incremental mode
6. Simplify/consolidate documentation
7. Report completion
```

---

## Step-by-Step

### 1. Collect Feature Artifacts

**Gather:**
- `specs/<feature>/spec.md` — feature specification
- `specs/<feature>/plan.md` — implementation plan
- `specs/<feature>/tasks.md` — task list
- Execution trace (git log, code changes, time logged)
- Branch name, feature number, dates

**Store in memory:**
- Feature digest (for lessons)
- Key implementation decisions made during work
- Patterns discovered or reused

---

### 2. Activate Caveman Mode for Compression

**Purpose:** Compress lessons + any documentation updates to save vault storage and reading time

**Mechanism:**
- Detect caveman mode setting from session
- If caveman already active: continue with current mode
- If caveman disabled: auto-enable caveman for this post step (compression is default for post)
- Log activation to workflow-state.json

**Documentation:**
- Print: "Caveman mode activated for post-processing. Lessons will be compressed."
- Print: "This reduces vault reading time by 60% while preserving technical content."

---

### 3. Generate Structured Lessons Learned

**Input:** Artifacts from Step 1  
**Output:** `vault/lessons/<date>-<feature-number>-<feature-name>.md`

**Lesson entry structure** (compressed format):

```
# Lesson: [Feature Name] (2026-05-18, spec-003)

## What We Built
[2-3 sentence digest of feature purpose and scope]
- [Key domain concept 1]
- [Key domain concept 2]

## How We Built It
[Technical approach; distilled from plan.md]
- [Architecture decision 1 + rationale]
- [Tech stack choice + why]
- [Integration point with existing code]

## Key Tasks Executed
- [Task 1: what it delivered]
- [Task 2: what it delivered]
- [Critical task: why it mattered]

## Decisions Made (Linked to Implementation)
- [Design decision 1: context → outcome]
- [Architecture choice: trade-off → outcome]

## Patterns Identified or Reused
- [Pattern 1: used from <prior feature>, adapted for ...]
- [Pattern 2: new pattern discovered, applicable to ...]
- [Anti-pattern: what NOT to do; discovered through ...]

## Lessons for Next Feature
- [If you need to do X again, avoid Y because...]
- [For similar features, this approach worked well...]
- [Watch out for Z in future; took us time to discover...]

## Metrics
- Lines of code: [X]
- Files modified: [N]
- Test coverage: [%]
- Time spent: [HH:MM]

---
*Compressed by caveman mode. For full spec/plan/tasks, see specs/<feature>/*
```

**Caveman compression rules:**
- One line per concept (no elaboration)
- Bullet format for quick scanning
- Link to full specs (not duplicated)
- No fluff; every word counts

**Self-contained goal:**
- Future sessions should be able to understand the feature from the lesson entry alone
- Reader should NOT need to open spec.md or tasks.md to understand what was done and why
- All critical decisions and patterns should be summarized here

---

### 4. Update Vault Context (Decisions, Patterns)

**Update `vault/decisions.md`:**
- Add any new decisions made during feature to decision log
- Format: `[2026-05-18] Feature 003: Decision name → outcome/impact`
- Include brief rationale

**Update `vault/patterns.md`:**
- Add any new patterns identified (reused or discovered)
- Format: `[Pattern Name]: When to use → key characteristics → where first seen`
- Include examples or references to feature

**Mechanism:**
```
/spek.post → analyze lessons entry
           → extract decisions + patterns
           → append to vault/decisions.md + vault/patterns.md
           → flag any conflicts with existing entries (for manual review)
```

**Example:**

```markdown
## vault/decisions.md (append)
[2026-05-18] Spec-003 Authentication: Chose JWT + refresh tokens over session cookies → 
  Rationale: Stateless design, works with distributed systems, easier to test. 
  Trade-off: Client must manage token expiry; mitigated via automatic refresh. 
  See: specs/003-auth/plan.md for architecture.

## vault/patterns.md (append)
[Async Task Queue Pattern]: 
  When to use: Long-running background work (user imports, report generation, cron jobs)
  First seen: Spec-003 Authentication (email verification queue)
  Key characteristic: Decouple request-response from processing; use Redis/Celery
  Applicable to: Any feature with user-initiated async work
```

---

### 5. Run Code Analysis Tool in Incremental Mode

**Purpose:** Index new code + lessons files in code analysis tool so next feature has graph context

**Action:**
- Trigger: `codegraph sync --incremental`
- Scope: Changed files in current feature branch (code + new lesson files)
- Output: Updated graph index (lessonfiles now queryable by agent)

**Timing:** After lessons are written, so lesson files are included in graph

**Benefit:** Next feature's `/context-load` → code graph queries include references to lessons (agent can surface relevant prior work automatically)

---

### 6. Simplify/Consolidate Documentation

**Purpose:** Prevent documentation from accumulating redundancy over time

**Action:**
- Trigger: `cel.docs.simplify` (scoped to feature branch changes or full wiki)
- Scope: Prefer **feature-branch scoped** (files modified in current branch)
  - Safer: avoids unintended rewrites in unrelated docs
  - Targeted: consolidates only what grew during this feature
- Output: Redundancy report + consolidated docs

**Timing:** After lessons written + graph refreshed (least disruptive point)

**Example scoping:**
```bash
cel.docs.simplify --scope-to-branch-changes
# Or, if that's not supported:
cel.docs.simplify wiki/ specs/<feature>/
```

---

### 7. Report Completion

**Print summary:**
```
✓ Lessons written: vault/lessons/2026-05-18-003-auth.md
✓ Vault context updated: [X new decisions, Y new patterns]
✓ Code graph refreshed (incremental): [N new files indexed]
✓ Documentation consolidated: [M files processed, K redundancies found]

Feature 003 complete. Context ready for next feature.
```

**Update workflow-state.json:**
```json
{
  "status": "complete",
  "completed_steps": ["preflight", "specify", "plan", "tasks", "analyze", "remediate", "implement", "post"],
  "postflight": {
    "lessons_written": true,
    "graph_refreshed": true,
    "vault_updated": true,
    "docs_simplified": true
  }
}
```

---

## Invocation

### Entry point: CLI

```bash
spek post
```

Or via agent skill:

```
/spek.post
```

### Entry point: Automatic (after `/speckit-enrich-implement`)

`spek automate` workflow automatically runs post after implement completes:

```
spek automate <feature-description>
  → ... implement ...
  → spek post (automatic)
```

### Manual invocation (if feature was worked on outside of spek automation)

Developer can run post manually after feature is merged:

```bash
spek post --feature-number 003
```

---

## Configuration Options

| Option | Default | Purpose |
|--------|---------|---------|
| `CAVEMAN_MODE_POST` | lite | Compression intensity for lessons |
| `GRAPH_INCREMENT` | true | Use incremental sync vs full rebuild |
| `DOCS_SIMPLIFY_SCOPE` | branch-changes | Scope: branch-changes or full |
| `VAULT_DECISION_UPDATE` | true | Auto-extract decisions for vault |
| `VAULT_PATTERN_UPDATE` | true | Auto-extract patterns for vault |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Lessons generation fails | Warn; offer manual entry; continue |
| Code graph unavailable | Warn; skip incremental sync (can run manually later) |
| Vault update conflicts | Flag for manual review; don't overwrite |
| Docs simplify fails | Warn; report failures; continue |
| Caveman compression unavailable | Skip compression; write uncompressed lessons |

---

## Integration with Feature Lifecycle

`spek post` is the final step of feature completion:

```
spek automate <feature-description>
  → 1. spek prepare
  → 2. create feature branch
  → 3. /speckit-enrich-specify
  → 4. /speckit-enrich-plan
  → 5. /speckit.tasks
  → 6. /speckit.analyze (optional)
  → 7. [manual remediation if needed]
  → 8. /speckit-enrich-implement
  → 9. spek post ← YOU ARE HERE
        ├─ compress lessons (caveman)
        ├─ write vault/lessons/
        ├─ update vault/decisions.md + vault/patterns.md
        ├─ codegraph sync --incremental
        └─ cel.docs.simplify
```

**Next feature benefit:**
- `/context-load` will load the new lesson
- Code graph will include references to new patterns
- Vault context will highlight related decisions
- Next feature starts with richer precedent

---

## Related Skills

- `/spek.prepare` — Mirror skill that runs at session start
- `/context-load` — Load vault (can be run independently)
- `/lessons-learnt` — Manual lessons capture (can be run separately)
- `/map-codebase` — Manual code graph refresh
- `/caveman` — Token compression control
- `/cel.docs.simplify` — Manual documentation consolidation

---

## Success Criteria

- [x] Lessons entry created (self-contained, compressed, references spec/plan)
- [x] Vault context updated (decisions + patterns added)
- [x] Code graph refreshed (new code + lessons indexed)
- [x] Documentation consolidated (redundancy audit complete)
- [x] Workflow state marked complete
- [x] Next feature has richer context available

---

## Implementation Notes

- **Idempotent:** Running `spek post` twice is safe (lessons entries are date-stamped, won't overwrite)
- **Non-destructive:** All operations are additive; no data loss
- **Session-independent:** Caveman compression applies only to lessons output, not to future sessions
- **Compounding benefit:** Each feature adds to vault; next feature learns from prior work
