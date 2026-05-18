# Skill: `spek.prepare`

## Purpose

Prime the agent and development environment for feature work by loading context, activating token optimization, and verifying tool readiness. Runs at session start or feature branch initialization.

**Outcome:** Agent has full project context in scope, caveman mode active for efficiency, code graph verified fresh.

---

## Workflow

```
1. Verify git state (clean tree, on feature branch)
2. Activate caveman mode (explicit for visibility)
3. Load obsidian vault context
4. Verify code analysis tool is fresh
5. Report ready status
```

---

## Step-by-Step

### 1. Verify Git State

**Check:**
- Working tree is clean (no uncommitted changes)
- Current branch is a feature branch (matches pattern: `NNN-<feature-name>`)
- Remote tracking is set up

**Action if failed:**
- If uncommitted changes: warn user, offer to commit or stash
- If not on feature branch: prompt to create or switch to feature branch
- Continue only after checks pass (or user explicitly overrides)

---

### 2. Activate Caveman Mode

**Purpose:** Reduce token consumption throughout the feature work session

**Mechanism:**
- Detect active AI agent (Copilot, Claude Code, etc.)
- **Default behavior:** Auto-enable caveman lite mode for spec/plan work (most token-heavy phases)
  - During spec generation: terse notation enforced
  - During plan generation: minimal verbosity, maximum clarity
- **Alternative behavior** (if user has caveman=disabled): prompt user: "Caveman mode reduces token use by 60%. Enable? [Y/n]"
- Log caveman activation status to `workflow-state.json`

**Documentation:**
- Print: "Caveman mode activated for this session. Responses will be terse but technically complete."
- Print: "To disable: set CAVEMAN_DISABLED=1"
- Print: "For intensity control: set CAVEMAN_MODE=lite|full|ultra"

**Rationale:** Feature work involves spec generation, planning, task generation, and implementation — all token-heavy. Caveman mode compounds savings across all phases.

---

### 3. Load Obsidian Vault Context

**Load from `.cel/context.md`:**
- **Graph summary:** Recent code structure highlights, recently modified modules
- **Decisions:** Stored architectural decisions (from `vault/decisions.md`)
- **Patterns:** Identified and reused patterns (from `vault/patterns.md`)
- **Recent lessons:** Latest 3-5 lesson entries (from `vault/lessons/<date>-*.md`, sorted by date desc)

**Action:**
```
/context-load
  → reads `.cel/context.md` hashes
  → if stale (> 24 hours or code graph changed): trigger refresh
  → load decisions, patterns, lessons into working memory
  → print: "Context loaded. [X decisions, Y patterns, Z lessons available]"
```

**Caching:**
- Hash check automatic (no manual refresh needed unless explicitly requested)
- If hashes differ (code changed): automatically rescan + reload
- If timestamp > 24 hours old: offer to refresh (developer can override)

---

### 4. Verify Code Analysis Tool is Fresh

**Purpose:** Ensure code graph is current before feature work begins (impacts context injection in enrich-specify/plan/implement)

**Check:**
- Code analysis tool is available (MCP server running, or lazy-start it)
- Graph index exists and is recent (≤ 2 hours old, or regenerated since last session)
- Latest code changes are indexed

**Action if fresh:**
- Print: "Code graph is fresh (last updated X minutes ago)"
- Continue

**Action if stale:**
- Print: "Code graph is stale (last updated X hours ago). Regenerating..."
- Run: `codegraph sync` (or equivalent full refresh)
- Wait for completion
- Print: "Code graph updated. Ready."

**Action if absent:**
- Print: "Code graph not initialized. Initializing..."
- Run initialization
- Print: "Code graph initialized."

---

### 5. Report Ready Status

**Print summary:**
```
✓ Git state: [branch-name]
✓ Caveman mode: [lite|full|ultra|disabled]
✓ Vault context: [X decisions, Y patterns, Z lessons]
✓ Code graph: [fresh, ← X minutes ago]

Ready for /speckit-enrich-specify
```

---

## Invocation

### Entry point: CLI

```bash
spek prepare
```

Or via agent skill:

```
/spek.prepare
```

### Entry point: Automatic (on `/context-load`)

If user runs `/context-load` outside of `spek` workflow:
- Optionally prompt: "Run full prepare step? (includes caveman activation, graph check, context load) [Y/n]"
- Or: silently execute prepare as part of context-load

---

## Configuration Options

| Option | Default | Purpose |
|--------|---------|---------|
| `CAVEMAN_ENABLED` | true | Enable caveman mode |
| `CAVEMAN_MODE` | lite | Intensity: lite, full, ultra |
| `CAVEMAN_DISABLED` | false | Override to disable caveman entirely |
| `GRAPH_REFRESH_THRESHOLD` | 2 hours | How old before code graph is considered stale |
| `VAULT_REFRESH_THRESHOLD` | 24 hours | How old before context is considered stale |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Working tree dirty | Warn; offer commit/stash; continue only after clean state or override |
| Not on feature branch | Offer to create/switch; or override to prepare anyway |
| Code graph unavailable | Initialize and continue (or fail if initialization fails) |
| Vault context missing | Initialize vault structure and continue |
| Caveman activation fails | Warn but continue (caveman is optional optimization) |

---

## Integration with `spek automate` CLI

`spek prepare` is the first step of the full automation workflow:

```
spek automate <feature-description>
  → 1. spek prepare (git state, caveman, vault, graph)
  → 2. create feature branch
  → 3. /speckit-enrich-specify
  → 4. /speckit-enrich-plan
  → 5. /speckit.tasks
  → 6. /speckit.analyze (optional)
  → 7. [manual remediation if needed]
  → 8. /speckit-enrich-implement
  → 9. spek post (lessons, graph refresh, vault update)
```

---

## Related Skills

- `/context-load` — Load vault independently (part of prepare, but runnable separately)
- `/spek.post` — Mirror skill that runs after feature complete (caveman compress, graph refresh, vault update)
- `/map-codebase` — Manual code graph refresh
- `/caveman` — Token compression control

---

## Success Criteria

- [x] Git state verified
- [x] Caveman mode activated (with visibility to user)
- [x] Vault context loaded (decisions, patterns, lessons available)
- [x] Code graph verified fresh
- [x] User can see prepared context in AI agent (ready for enrich-specify)

---

## Implementation Notes

- **Idempotent:** Running `spek prepare` multiple times is safe (no side effects)
- **Non-blocking:** If code graph refresh takes time, user can proceed with agent (graph queries happen on-demand)
- **Session-scoped:** Caveman mode activation applies to current session only; next session starts fresh
