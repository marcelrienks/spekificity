# FOUNDATIONAL SPECIFICATION: Error Handling and Recovery (F1.0)




## Overview

Spekificity operates in autonomous mode with limited user intervention. This spec defines the error handling and recovery strategy across all components: error categorization, per-category handling, logging, graceful degradation, recovery flows, and testing.

**Purpose:**
- Ensure **predictable behavior** under error conditions (fail safely, not crash)
- Enable **autonomous recovery** (retry logic, fallbacks, self-healing)
- Support **user intervention** when recovery fails (clear error messages, guidance)
- Maintain **audit trail** (logging for debugging and improvement)

---


## Success Criteria

- ✅ Error categories clearly defined (Git/Vault/Graph/LLM/SpecKit/User)
- ✅ Handling strategy per category documented (severity, default action, recovery flow)
- ✅ Logging comprehensive (all errors captured with context)
- ✅ Graceful degradation working (failures don't halt workflows)
- ✅ Autonomous recovery implemented (retries, fallbacks, healing)
- ✅ User intervention enabled (clear error messages, guidance)
- ✅ Testing strategy defined (unit + integration tests for error paths)
- ### Category 3: Graph/Code Index Errors (TRANSIENT or RECOVERABLE)
- **Definition:** Code graph (lat.md output) is corrupted, stale, or export fails
- **Errors:**
- `vault/graph/nodes.jsonl` corrupted (invalid JSON)
- lat.md crashed or hung
- Obsidian export API failure
- Graph merge failed
- No symbols found (empty graph)
- **Handling:**
- **Severity:** MEDIUM (doesn't block workflows, just limits context richness)
- **Default Action:** WARN + FALLBACK (continue with stale graph or empty graph)
- **Recovery Flow:**
- Attempt to use last known good graph (cached version)
- If no cache: Continue with **empty graph** (no code context)
- Offer async refresh: `/spek.map --force` (background job)
- Log warning: "Graph index stale, some code references may be incomplete"
- At feature end: Attempt graph rebuild before archival
- **Logging:** Log graph error, fallback action, and retry status to `.spek/error-log.md`
- **Example:**
- ```
- Warning: lat.md index corrupted (nodes.jsonl parse error at line 542)
- Fallback: Using cached graph from 4 hours ago
- Tip: Run `/spek.map --force` to rebuild the lat.md index (can take 1-2 min)
- Continue: Proceeding with stale graph; some code references may be incomplete
- ### Category 4: Context Injection Errors (TRANSIENT)
- **Definition:** Failed to load or inject context into agent environment
- Context file too large (>100K tokens for current session)
- Session memory write fails (disk full, permission denied)
- Context variable injection fails (env var limit exceeded)
- `vault/session/` directory not writable
- **Severity:** MEDIUM (blocks enrichment, requires manual context injection)
- **Default Action:** WARN + FALLBACK (continue with minimal context)
- Reduce context size: Remove least-recent lessons
- If still too large: Use decision index + pattern index only (compressed)
- If still failing: Continue with code graph only (no memory)
- Offer fix: "Increase context token budget or simplify vault"
- Log warning + offered fix
- **Logging:** Log context size, budget used, and fallback action to `.spek/error-log.md`
- Warning: Context too large for session (245K tokens, budget: 200K)
- Fallback: Loading compressed context (decisions + patterns index only, ~50K tokens)
- Tip: Run `/spek.conclude --caveman-mode=ultra` on recent features to reduce vault size
- Continue: Full context available after cleanup
- ### Category 5: File I/O Errors (TRANSIENT or FATAL)
- **Definition:** Failed to write/read specification or artifact files
- Disk full (no space for spec file, lesson file, etc.)
- Permission denied (can't write to `specs/` or `wiki/specs/`)
- File locked (concurrent write access)
- Parent directory missing (should not happen with dir creation, but fallback)
- File path too long (OS limit)
- **Severity:** HIGH (blocks artifact persistence)
- **Default Action:** FAIL + GUIDE (provide alternative location or recovery steps)
- Check disk space: `df -h`
- If full: Offer cleanup: "Archive old lessons: `mv wiki/vault/lessons/2024-* archive/`"
- If permissions: Offer fix: "Fix permissions: `chmod 755 specs/`"
- If locked: Offer retry: "Close any open editors, then retry"
- If parent missing: Create directory and retry
- If path too long: Use alternate naming scheme (shorten feature name)
- **Logging:** Log full error + offered fix to `.spek/error-log.md`
- Error: Disk full (Failed to write wiki/vault/lessons/2026-05-19-feature.md)
- Fix 1: Free up space: `rm -rf wiki/vault/lessons/2024-*` (archive old lessons)
- Fix 2: Use external storage: `export VAULT_DIR=/external/vault`
- Action: Choose fix, then run `/spek.conclude` again
- ### Category 6: SpecKit Integration Errors (TRANSIENT or FATAL)
- **Definition:** SpecKit command failed, timed out, or returned invalid output
- `/speckit.specify` timed out (>5 min)
- `/speckit.plan` returned invalid JSON/YAML
- `/speckit.tasks` output missing required fields
- `/speckit.implement` subprocess crashed
- SpecKit not installed or corrupted
- **Severity:** HIGH (blocks feature workflow)
- **Default Action:** FAIL + RETRY (retry speckit command 2x with backoff)
- **Retry 1:** Wait 10s, retry same command
- **Retry 2:** Wait 30s, retry with `--verbose` flag (for debugging)
- On retry success: Continue, log recovery
- On retry failure: FAIL with guidance
- Offer: Check SpecKit install: `specify --version` (Spec Kit CLI is provided by the `specify` command; install via `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` or use `pipx`/`pip` alternatives per Spec Kit docs)
- Offer: Run in verbose: `speckit.specify --verbose`
- Offer: Manual fallback: Create spec/plan/tasks manually
- **Logging:** Log speckit error + full output to `.spek/error-log.md`
- Error: /speckit.plan timed out after 5 min
- Retry 1: Retrying (10s delay)...
- Retry 2: Retrying with --verbose (30s delay)...
- Error: /speckit.plan still failing (timeout)
- Fix: Check SpecKit: `specify --version` or reinstall via `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (or `pipx install specify-cli` / follow https://github.com/github/spec-kit for alternatives)
- Manual fallback: Create specs/plan.md manually, then run `/spek.tasks`
- ### Category 7: Memory/Performance Errors (RARE, GRACEFUL)
- **Definition:** Out of memory, excessive token usage, or extreme latency
- Agent context window exhausted (>90% tokens used)
- Session memory too large (>500MB)
- Code graph too large (>10K symbols)
- Lesson generation taking >10 min
- **Severity:** MEDIUM-HIGH (degrades performance, may abort feature work)
- **Default Action:** WARN + OFFER COMPRESSION (reduce context, compress artifacts)
- Detect: Monitor token usage + session memory size
- At 80% usage: Warn user, offer compression
- At 90% usage: Auto-compress recent lessons (caveman mode)
- At 95% usage: ABORT current operation, ask user to restart with fresh context
- Logging: Log resource usage + compression/abort action
- **Logging:** Log memory/token usage metrics to `.spek/error-log.md`
- Warning: Session memory 75% full (375MB of 500MB)
- Offer: Compress artifacts? Run `/spek.conclude --caveman-mode=ultra` after this feature
- Continue: Proceeding with current context
- [After feature end]
- Info: Compressed lessons 2026-05-19 (80% reduction via caveman mode)
- ## Cross-Cutting Error Handling Rules
- ### Rule 1: Fail Safely, Not Silently
- **Principle:** Always alert the user and log the error. Never silently skip critical operations.
- **Application:**
- Vault update fails → Log error, alert user, don't pretend vault was updated
- Graph refresh fails → Log error, continue with old graph (not silent)
- Context injection fails → Log error, continue with fallback context (not silent)
- **Implementation:**
- Every error path logs to `.spek/error-log.md` with timestamp, category, and action taken
- User-facing errors shown in CLI output (red/warning color)
- Logged errors are summarized in feature end report
- ### Rule 2: Provide Actionable Guidance
- **Principle:** Every error message includes a suggested fix or recovery action.
- Git state error → Show required git command
- Vault permission error → Show chmod command + explanation
- Disk full error → Show cleanup suggestion + alternative location
- SpecKit timeout → Show version check + manual fallback option
- Error message format: `Error: {what happened}\nFix: {action to take}\nThen: {next step}`
- All fixes are runnable as-is (no manual interpretation needed)
- ### Rule 3: Retry with Exponential Backoff (For Transient Errors)
- **Principle:** Transient errors (network, disk I/O, process contention) should retry automatically.
- **Transient errors** (git state unclear, file locked, graph export timing out): Retry 2-3x with 10s/30s/60s backoff
- **User-facing errors** (git dirty, vault permission): Fail immediately (require user action)
- **Fatal errors** (vault corrupted, speckit missing): Fail after 1-2 retries with clear guidance
- attempt = 1
- while attempt <= 3:
- try:
- result = operation()
- return result
- except TransientError as e:
- if attempt < 3:
- wait(10 * 2^attempt)  # Exponential backoff: 10s, 20s, 40s
- attempt += 1
- else:
- raise FatalError(e) with guidance
- ### Rule 4: Graceful Degradation (Use Fallbacks)
- **Principle:** Missing optional data should not block the workflow. Use fallbacks.
- Code graph missing → Use empty graph, continue (code context just won't be available)
- Vault inaccessible → Use cached decisions, continue (decisions just won't be persisted)
- Recent lessons missing → Use empty lessons history, continue (no historical context)
- Define **fallback hierarchy** for each data source:
- Primary: Fresh data from wiki/vault/graph
- Secondary: Cached data from `vault/repo/` or `.spek/`
- Tertiary: Empty/minimal data (continue with no context)
- Always log which fallback was used
- ### Rule 5: Log All Errors with Context
- **Principle:** Every error is logged with enough detail to debug and improve the system.
- **Logging Format:**
- ```markdown
- ## Error Log (2026-05-19)
- ### Error: {Category}
- **Time:** 2026-05-19 14:32:15 UTC
- **Operator:** /spek.prepare
- **Severity:** {HIGH|MEDIUM|LOW}
- **Error Message:** {actual error text}
- **Context:** {relevant data: file paths, git status, vault state}
- **Action Taken:** {fallback|retry|fail + guidance}
- **Recovery:** {success|pending|failed}
- **Lessons:** {if applicable: how to prevent this in future}
- **Log Location:** `.spek/error-log.md` (persistent across sessions)
- ## Logging Structure
- ### `.spek/error-log.md` (Persistent Error Log)
- **Purpose:** Audit trail of all errors across all sessions
- **Format:**
- # Error Log
- ## Session: 2026-05-19 (10:00 - 16:30)
- ### Feature: 003-spek-full-workflow-cli
- #### Error 1: Vault Permission Denied
- Time: 2026-05-19 14:32:15
- Component: /spek.conclude (Step 4)
- Severity: MEDIUM
- Action: Retry after permission fix
- Recovery: SUCCESS (after `chmod 755 vault/`)
- #### Error 2: Graph Export Timeout
- Time: 2026-05-19 14:45:22
- Component: /spek.map (lat.md)
- Action: Fallback to cached graph (2h old)
- Recovery: AUTO (retried after 30s)
- ...
- **Retention:** Keep last 100 errors (oldest archived to `archive/error-log-*.md`)
- ## Testing & Validation
- ### Test Coverage (Per Category)
- **Category 1: Git State Errors**
- [ ] Test: `.git` missing → Fail + guidance
- [ ] Test: Working tree dirty → Fail + guidance
- [ ] Test: Feature branch missing → Fail + guidance
- [ ] Validation: Error message includes `git` command to fix
-- **Category 2: Vault Access Errors**
-- [ ] Test: `vault/` missing → Fail + guidance (do not auto-fallback for core automation)
-- [ ] Test: Permission denied → Fail + guidance (do not auto-fallback for core automation)
-- [ ] Test: JSON corrupted → Fail + guidance (do not auto-fallback for core automation)
-- [ ] Validation: Fail-fast for core automation; surface recovery steps to operator/CI
- **Category 3: Graph Errors**
- [ ] Test: `nodes.jsonl` corrupted → Warn + fallback to old graph
- [ ] Test: lat.md hung → Timeout after 2 min, offer async refresh
-- [ ] Test: Obsidian export fails → Fail + guidance (Obsidian CLI required for core automation)
-- [ ] Validation: Graph export failures block core automation and report actionable remediation
- **Category 4: Context Injection Errors**
- [ ] Test: Context too large → Auto-compress, continue
- [ ] Test: Session memory write fails → Warn + fallback
- [ ] Validation: Continue with reduced context
- **Category 5: File I/O Errors**
- [ ] Test: Disk full → Fail + show cleanup suggestion
- [ ] Test: Permission denied → Fail + show chmod command
- [ ] Test: File locked → Retry 3x, then fail + guidance
- [ ] Validation: Error message includes recovery command
- **Category 6: SpecKit Errors**
- [ ] Test: SpecKit timeout → Retry 2x with backoff
- [ ] Test: Invalid output → Fail + offer manual fallback
- [ ] Test: SpecKit missing → Fail + suggest reinstall
- [ ] Validation: Retry uses exponential backoff, final error is actionable
- **Category 7: Memory Errors**
- [ ] Test: Token usage >90% → Auto-compress
- [ ] Test: Session memory >500MB → Warn + offer compression
- [ ] Test: Extreme latency → Timeout + restart with fresh context
- [ ] Validation: Resource usage monitored and reported
- ### Integration Tests
- [ ] **Full error recovery flow:** Trigger Category 2 error, verify fallback, verify retry succeeds
- [ ] **Multi-error scenario:** Trigger git + vault errors simultaneously, verify both handled
- [ ] **Error log creation:** Trigger error, verify logged to `.spek/error-log.md` with full context
- [ ] **User guidance:** Trigger error, verify error message includes actionable fix
- ## Implementation Checklist
- [ ] All skills include error handling per this spec (don't add new error handling logic; reference this spec)
- [ ] All error paths log to `.spek/error-log.md`
- [ ] All errors include actionable guidance (not just error codes)
- [ ] Transient errors retry with exponential backoff
- [ ] Fallback hierarchies defined for optional data sources
- [ ] Test suite covers all error categories
- [ ] Error handling is **tested in integration** (not just unit tests)
- [ ] Logging includes enough context for debugging
- ## Related Specs
- **Vault and Memory:**
- [Memory Architecture](030-memory-architecture.md)
- [Architectural Decisions](022-architectural-decisions.md)
- [Patterns Library](023-patterns-library.md)
- **Code Graph:**
- [Code and Document Maps](056-code-and-document-maps.md)
- [Graph Refresh Strategy](053-graph-refresh-strategy.md)
- **Skills:**
- [Prepare Command](100-prepare-command.md)
- [Post Command](102-conclude-command.md)
- [Enrichment Layer](032-enrichment-layer.md)
- **Integration:**
- [Speckit Integration Contract](110-speckit-integration-contract.md)
- [Context Layer](031-context-layer.md)
- ## Final Notes
- This spec is **foundational** — all other specs should reference it for error handling strategy rather than defining their own. By centralizing error handling, we ensure:
- **Consistency** — All components handle errors the same way
- **Maintainability** — Updates to error strategy happen in one place
- **Debuggability** — All errors logged to one location with consistent format
- **Autonomy** — Agent can recover from most errors without user intervention
- **Reference this spec in:**
- Skill definitions (e.g., "For error handling, see error-handling-and-recovery.md")
- Integration layer specs (e.g., "Errors are handled per error-handling-and-recovery.md")
- Implementation plans (e.g., "Error handling: Follow category X from error-handling-and-recovery.md")


## Error Categories


## Category 1: Git State Errors (TRANSIENT or USER)

**Definition:** Git repository validation failures or dirty working tree

**Errors:**
- `.git/` directory not found → Not in a git repository
- Working tree dirty (unstaged changes, untracked files)
- Feature branch not detected
- Merge/rebase in progress
- Detached HEAD state

**Handling:**
- **Severity:** HIGH (blocks all workflows)
- **Default Action:** FAIL + GUIDE (report error, show required action)
- **Recovery Flow:**
  1. Report: "Git workspace error: {error details}"
  2. Show guidance: "Required fix: {action}" (e.g., "git add .", "git stash", "git checkout feature-branch")
  3. Offer: "Run `/spek.prepare` again after fixing"
  4. **No retry** — Requires user action
- **Logging:** Log full git output + recommended fix to `.spek/error-log.md`

**Example:**
```
Error: Git working tree is dirty
  Unstaged changes: src/main.py, src/utils.py
  Untracked files: .env.local
Action: git add . && git commit -m "checkpoint" OR git stash
Then: /spek.prepare
```

---


## Category 2: Vault Access Errors (TRANSIENT or FATAL)

**Definition:** Obsidian vault not found, corrupted, or permission denied

**Errors:**
- `vault/` directory not found
- `vault/decision.md` or `vault/patterns.md` missing
- JSON parse error in vault files
- Permission denied (read/write)
- Vault file locked (concurrent access)

**Handling:**
- **Severity:** MEDIUM-HIGH (blocks context loading and persistence)
- **Default Action:** WARN + FALLBACK (continue with stale context or empty vault)
- **Recovery Flow:**
  1. Attempt read from cache (`vault/repo/` or `vault/`)
  2. If cache exists: Use cached context, log warning
  3. If cache missing: Continue with **minimal context** (code graph only)
  4. Async retry: Attempt vault access every 30 seconds (max 3 retries)
  5. On retry success: Reload context, log recovery
  6. On retry exhaustion: Continue, log error, alert user at feature end
- **Logging:** Log vault error + fallback action to `.spek/error-log.md`

**Example:**
```
Warning: Vault inaccessible (permission denied: wiki/vault/decision.md)
Fallback: Using cached decisions from vault/repo/architectural-decisions.md (age: 2 days)
Retry: Vault access will be attempted every 30s for 3 retries
Action: Check vault permissions: `chmod -R 755 vault/`
```

