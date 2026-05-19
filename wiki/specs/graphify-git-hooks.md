# C.3.4 Graphify Git Hooks Integration

**Status:** Specification  
**Priority:** MUST (Phase 1)  
**Effort:** 1 hour  
**Adoption Source:** B.9 (claude-code-memory-setup) + B.11 (Codegraph Setup Spec)

---

## Purpose

Automatically keep the code graph fresh by installing a `post-commit` git hook that:
1. Runs after every local commit
2. Increments ally updates code graph (via graphify)
3. Uses SHA256 caching to skip unchanged files
4. Reports changes to user (2-4 seconds, imperceptible)

**Goal:** Prevent stale graph queries; ensure `/spek.context` always works with fresh code structure.

---

## Scope & Relationships

**What this spec covers:**
- Git hook installation (post-commit)
- Graphify incremental update strategy
- Hook configuration (enable/disable)
- Performance optimization (caching, worker threads)
- Hook removal/troubleshooting

**What this spec does NOT cover:**
- Full graphify setup (see B.11 Codegraph Setup)
- Watch mode (optional; different workflow)
- Graph storage (see B.11)
- Graph query patterns (see B.11, C.3.3)

**Related specs:**
- B.11: Codegraph Setup (graphify installation, storage, refresh strategy)
- B.8.4: Post Command Step 6 (incremental sync after feature implementation)

---

## Git Hook: post-commit

### What It Does

After every successful `git commit`:

```bash
# Triggered automatically by git
.git/hooks/post-commit

1. Get list of changed files (via git diff)
2. Check which files need re-indexing (SHA256 cache)
3. Run graphify incremental update on changed files only
4. Update graph/nodes.jsonl with new definitions
5. Merge with doc nodes (Obsidian export, if present)
6. Cache results
7. Report completion (takes 2-4 seconds)
```

### Hook Installation

```bash
# During .spekificity/bin/spek setup:

graphify hook install

# Equivalent to:
# 1. Create .git/hooks/post-commit
# 2. Add executable bit: chmod +x .git/hooks/post-commit
# 3. Write hook script (see below)
```

### Hook Script Template

```bash
#!/bin/bash
# .git/hooks/post-commit
# Auto-installed by: spek setup
# Purpose: Incremental graph refresh after every commit

set -e

# Configuration
GRAPHIFY_CMD="graphify"
WORKSPACE_ROOT="$(git rev-parse --show-toplevel)"
GRAPH_CONFIG="${WORKSPACE_ROOT}/.spekificity/config.yaml"
GRAPH_DIR="${WORKSPACE_ROOT}/vault/graph"

# Check if hooks are enabled
if [ -f "${WORKSPACE_ROOT}/.spekificity/.disable-git-hooks" ]; then
    exit 0
fi

# Get changed files (only code files)
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | \
    grep -E '\.(js|ts|py|java|go|rb|rs)$' || true)

if [ -z "$CHANGED_FILES" ]; then
    # No code files changed, skip graph update
    exit 0
fi

# Run incremental graphify update
echo "🔄 Updating code graph..."
cd "$WORKSPACE_ROOT"

${GRAPHIFY_CMD} . \
    --update \
    --config "${GRAPH_CONFIG}" \
    --paths ${CHANGED_FILES} \
    --quiet

if [ $? -eq 0 ]; then
    echo "✓ Code graph updated ($(echo $CHANGED_FILES | wc -w) files)"
else
    echo "⚠ Code graph update failed (continuing anyway)"
fi

exit 0
```

---

## Configuration

### Setup in `.spekificity/config.yaml`

Add git hooks configuration:

```yaml
graphify:
  refresh:
    # Git hooks
    enable_git_hook: true           # Auto-sync on commits
    git_hook_quiet: true            # No output unless error
    git_hook_can_disable: true       # User can disable via flag
    
    # Performance
    git_hook_timeout: 30            # Max seconds per hook run
    git_hook_max_files_per_batch: 50 # Files to index per batch
    
  # ... existing graphify config ...
```

### User Control

**Enable/disable hooks:** User can create flag file to disable:

```bash
# Disable hooks temporarily:
touch .spekificity/.disable-git-hooks

# Re-enable:
rm .spekificity/.disable-git-hooks
```

**Or via CLI flag:**

```bash
# Disable for next commit:
git commit -m "..." --env-hook=disabled

# Re-enable (default):
git commit -m "..."
```

---

## Hook Lifecycle

### Installation (during `spek setup`)

```bash
$ .spekificity/bin/spek setup

[Step 5/7] Installing git hooks...
  → Detecting graphify installation
  → Writing post-commit hook
  → Making hook executable
  → Testing hook (dry-run)
  ✓ Git hook installed successfully

  Hook location: .git/hooks/post-commit
  Enable/disable: touch .spekificity/.disable-git-hooks
```

### Activation (first commit after setup)

```bash
$ git commit -m "feat: add auth module"

[post-commit hook runs automatically]
  🔄 Updating code graph...
  ✓ Code graph updated (3 files)

[commit completes normally]
```

### Subsequent Commits

```bash
$ git commit -m "fix: auth edge case"

[post-commit hook runs silently]
  ✓ Code graph updated (1 file)
```

### Removal (if needed)

```bash
$ .spekificity/bin/spek setup --uninstall-hooks

[Removes post-commit hook]
✓ Git hooks uninstalled

[Re-enable later]
$ .spekificity/bin/spek setup --reinstall-hooks
```

---

## Performance Considerations

### Speed: Why 2-4 Seconds?

**Breakdown:**

```
1. Get changed files (git diff-tree):    ~50ms
2. Filter to code files (grep):           ~50ms
3. Run graphify incremental:              ~2-3 seconds
   - SHA256 cache lookup:                 ~500ms
   - Parse changed files:                 ~1000ms
   - Merge with existing graph:           ~500ms
   - Update cache:                        ~500ms
4. Report to user:                        ~10ms

Total:                                    ~2-4 seconds
```

**Imperceptible to User:**
- Commit command returns immediately (hook runs in background)
- Or waits 2-4 seconds silently (depends on config)
- User feedback: "✓ Code graph updated (N files)"

### Optimization Strategies

**1. SHA256 Caching:**

```
First commit:
  - graphify indexes ALL files
  - Stores SHA256 hash per file
  - Time: 28 seconds (full rebuild)

Second commit (1 file changed):
  - graphify compares SHA256 hashes
  - Sees only 1 file changed
  - Re-indexes only that file
  - Time: 2 seconds (14x faster!)
```

**2. Parallel Workers:**

```
config.yaml:
  graphify:
    workers: 4  # Use 4 threads

Performance:
  - Single-threaded: 2 seconds
  - 4-threaded:     0.5 seconds
  - Speedup:        4x
```

**3. Language-Selective Indexing:**

```
config.yaml:
  graphify:
    languages:
      - typescript  # Fast (tree-sitter)
      - python      # Fast
      # Exclude slow languages
      # - rust       # Can be slow
```

---

## Conflict Resolution

### What if Hook Fails?

```bash
$ git commit -m "feature"

[post-commit hook fails]
⚠ Code graph update failed
  Error: /vault/graph/nodes.jsonl locked by other process

[Commit succeeds anyway!]
✓ commit abc123 created
  (Graph update will retry on next commit)
```

**Design:** Hook failures never block commits (git best practice).

**Retry:** Graph refreshes automatically on next commit or via `/spek.post`.

### What if User Runs `graphify` Manually?

```bash
$ graphify . --full

[Manual graphify run updates graph]
[Post-commit hook also tries to update]

[Conflict handling]
  → graphify detects lock
  → Hook waits (timeout: 30s)
  → Continues after manual run completes
```

---

## Integration Points

### 1. Setup Script (`.spekificity/bin/spek setup`)

```bash
# Step 5 of setup process:
function install_git_hooks() {
    echo "Installing git hooks..."
    
    # Check graphify available
    if ! command -v graphify &> /dev/null; then
        echo "⚠ graphify not found; skipping git hooks"
        return 1
    fi
    
    # Install post-commit hook
    graphify hook install
    
    # Create disable flag (for user control)
    touch .spekificity/.disable-git-hooks-template
    
    echo "✓ Git hooks installed"
}
```

### 2. /spek.prepare (B.8.4 Step 3)

```
/spek.prepare Step 3: Check code graph freshness

Current behavior (B.8.4):
  1. Check graph age (modified time)
  2. If > 1 hour: refresh graph
  3. Offer manual refresh if stale

Enhanced with hooks (C.3.4):
  1. Check if git hook installed
  2. If not installed: offer to install
  3. Graph will stay fresh automatically after commit
  4. Manual refresh only needed if hook disabled
```

### 3. /spek.post (B.8.4 Step 6)

```
/spek.post Step 6: Incremental code graph sync

Current behavior (B.8.4):
  1. Run graphify on changed files
  2. Takes 2-4 seconds
  3. Merges with doc nodes

With hooks (C.3.4):
  1. Git hook already ran after last commit
  2. Graph mostly fresh (within seconds of commit)
  3. /spek.post just validates + merges
  4. Faster + always in sync
```

---

## Troubleshooting

### Issue: Hook Not Running

**Diagnosis:**

```bash
$ git commit -m "test"

[No "Code graph updated" message]

Check:
1. Is hook installed?
   $ ls .git/hooks/post-commit
   
2. Is hook executable?
   $ ls -la .git/hooks/post-commit | grep x
   
3. Is hook disabled?
   $ ls .spekificity/.disable-git-hooks
```

**Fix:**

```bash
# Reinstall hook
.spekificity/bin/spek setup --reinstall-hooks

# Or manually:
graphify hook install
chmod +x .git/hooks/post-commit
```

### Issue: Hook Times Out

**Diagnosis:**

```
⚠ Code graph update failed
  Error: Hook timeout (30 seconds exceeded)
```

**Causes:**
- Large number of changed files
- Slow disk I/O
- graphify indexing slow language

**Fix:**

```yaml
# Increase timeout in config.yaml
graphify:
  refresh:
    git_hook_timeout: 60  # 60 seconds instead of 30
```

Or disable hooks for large commits:

```bash
# Skip hook for this commit
git commit -m "..." --env-hook=disabled
```

### Issue: Hook Conflicts with Manual Graphify

**Diagnosis:**

```
Hook tries to run while manual graphify in progress
Graph lock detected
```

**Fix:**

```bash
# Hook automatically waits (timeout: 30s)
# After manual graphify completes, hook continues

# Or disable hooks for long operations:
touch .spekificity/.disable-git-hooks
graphify . --full --watch  # Long-running
rm .spekificity/.disable-git-hooks
```

---

## User Workflows

### Happy Path: Automatic Graph Sync

```
1. Developer works on feature, makes commits
   $ git commit -m "add async handler"
   ✓ Code graph updated (1 file)

2. Developer makes another commit
   $ git commit -m "add tests"
   ✓ Code graph updated (2 files)

3. Developer runs /spek.context for context
   → Graph is fresh (updated 10 seconds ago)
   → Context load uses fresh graph
   → Queries are accurate + efficient

Result: ✅ Graph always in sync, no manual refresh needed
```

### Optional: Disable Hooks for Performance

```
User doing intensive rebasing + cherry-picking?

1. Disable hooks temporarily
   $ touch .spekificity/.disable-git-hooks

2. Do intensive git operations
   $ git rebase -i
   $ git cherry-pick
   $ ... many commits ...

3. Re-enable hooks + do full refresh
   $ rm .spekificity/.disable-git-hooks
   $ graphify . --full

Result: ✅ Hooks re-enabled, graph fresh
```

---

## Success Criteria

- ✅ Git hook installed during `.spekificity/bin/spek setup`
- ✅ Hook runs automatically after every commit
- ✅ Incremental updates complete in 2-4 seconds
- ✅ SHA256 caching prevents unnecessary re-indexing
- ✅ Hook failures never block commits
- ✅ User can enable/disable hooks easily
- ✅ Graph stays fresh (within seconds of latest commit)
- ✅ `/spek.context` always queries fresh graph
- ✅ Troubleshooting guide covers common issues

---

## Related Specifications

- **B.11:** Codegraph Setup (graphify installation, refresh strategies)
- **B.8.4:** Prepare & Post Skills (graph freshness checks)
- **C.3.3:** 3-Layer Query Rule (uses fresh graph for queries)

---

## References

- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (git hook pattern, 659⭐)
- **Graphify:** https://github.com/graphify/graphify (CLI + hook support)
- **Git Hooks:** https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks (post-commit reference)
