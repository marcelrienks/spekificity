# User Story 3: Independent Update Workflow

**US3**: Update spekificity custom layer independently without re-initializing all tools.

**Feature**: `spek update` command that refreshes skills, workflows, guides, and configurations.

---

## Acceptance Criteria

- [ ] Update command exists: `.spekificity/setup-scripts/update.sh`
- [ ] Main dispatcher routes to update: `spek update`
- [ ] Help available: `spek update --help`
- [ ] Version tracking in config updated
- [ ] Skill index regenerated after update
- [ ] Idempotent: Safe to re-run
- [ ] Non-destructive: Preserves custom preferences
- [ ] Clear output: Progress and success messages
- [ ] Fast execution: <30 seconds (without tool re-installs)

---

## Scenario 1: Update Spekificity (Stub Phase)

**Given**: Spekificity initialized (`spek_initialized = true`)

**When**: User runs `spek update`

**Then**:

```
✓ Checking for updates...
ℹ Spekificity v1.0.0 is current (no updates available)

To manually update:
  1. Check: .github/copilot-instructions.md for latest skill commands
  2. Update custom preferences: Edit .spekificity/config.json
  3. Regenerate skills: spek init

Full Phase 6 implementation coming in v1.1.0
```

**Exit Code**: 0 (success)

**Evidence**:
```bash
.spekificity/bin/spek update
# Output matches stub message above
```

---

## Scenario 2: Update Help Text

**Given**: Spekificity project initialized

**When**: User runs `spek update --help`

**Then**:

```
Usage: spek update [options]

Options:
  --verbose          Enable verbose output
  --skip-backup      Don't backup config before update
  --dry-run          Preview changes without applying
  -h, --help         Show this help

Description:
  Update spekificity custom layer (skills, workflows, guides).
  
  This command refreshes:
    - Custom skill definitions (.spekificity/skills/)
    - Workflow documentation (.spekificity/workflows/)
    - Guide documentation (.spekificity/guides/)
    - Skill index (.spekificity/skill-index.md)
  
  Does NOT re-initialize tools (speckit, graphify, etc.).
  
  Phase 6 Implementation:
    Full update automation with version checking, 
    incremental sync, and conflict resolution coming v1.1.0

Examples:
  spek update              # Preview changes
  spek update --verbose    # Verbose output
  spek update --dry-run    # See what would change

For more info: .spekificity/guides/
```

**Exit Code**: 0 (help)

**Evidence**:
```bash
.spekificity/bin/spek update --help
# Output matches help text above
```

---

## Scenario 3: Dry-Run (Preview)

**Given**: Spekificity initialized with custom modifications

**When**: User runs `spek update --dry-run`

**Then**:

```
Spekificity Update — Dry-Run Mode

Checking for updates...
ℹ Spekificity v1.0.0 (current)

Preview: Changes that would be applied
  • Would regenerate: .spekificity/skill-index.md
  • Would refresh: .spekificity/guides/
  • Would preserve: Custom preferences in config.json
  • Would preserve: Project-specific skills

No changes applied (--dry-run mode)

To apply updates: spek update

Phase 6 Implementation:
  Full update automation with version checks and 
  incremental sync coming in v1.1.0
```

**Exit Code**: 0 (dry-run success)

**Evidence**:
```bash
.spekificity/bin/spek update --dry-run
# Output shows preview without making changes
ls .spekificity/skill-index.md
# File unchanged
```

---

## Scenario 4: Update Config Preservation

**Given**:
```json
{
  "spek_version": "1.0.0",
  "spek_custom_preferences": {
    "graphify_depth": "deep",
    "auto_lessons": true,
    "update_frequency": "weekly"
  }
}
```

**When**: User runs `spek update`

**Then**:

Config after update:
```json
{
  "spek_version": "1.0.0",
  "spek_custom_preferences": {
    "graphify_depth": "deep",
    "auto_lessons": true,
    "update_frequency": "weekly"
  }
}
```

**Evidence**:
```bash
cat .spekificity/config.json | jq '.spek_custom_preferences'
# Output shows custom preferences preserved
```

---

## Scenario 5: Update with Verbose Output

**Given**: Spekificity initialized

**When**: User runs `spek update --verbose`

**Then**:

```
═══════════════════════════════════
 Spekificity Update
═══════════════════════════════════

[spekificity] Checking version...
ℹ Current version: 1.0.0
ℹ Latest version: 1.0.0
✓ Already current

[spekificity] Regenerating skill index...
✓ Discovered: 3 spekificity skills
✓ Discovered: 4 speckit skills
✓ Caveman available: false
✓ Skill index generated: .spekificity/skill-index.md

[spekificity] Validating configuration...
✓ Config valid (schema v1.0.0)
✓ Custom preferences preserved

═══════════════════════════════════
 Update Complete
═══════════════════════════════════

Spekificity is up-to-date.
Next phase (v1.1.0): Automatic version checking and incremental sync
```

**Exit Code**: 0

**Evidence**:
```bash
.spekificity/bin/spek update --verbose 2>&1 | grep "Update Complete"
# Output shows completion
```

---

## Scenario 6: Failed Update (Simulation)

**Given**: Config file corrupted (for testing failure handling)

**When**: User runs `spek update`

**Then**:

```
✗ Error: Config file is invalid

Reason: Unable to parse .spekificity/config.json

Recovery:
  1. Backup: cp .spekificity/config.json .spekificity/config.json.bak
  2. Repair: spek setup
  3. Retry: spek update
  
Or manually:
  1. Delete: rm .spekificity/config.json
  2. Re-init: spek init
```

**Exit Code**: 1 (failure)

**Evidence**:
```bash
# Corrupt config
echo "{ invalid json" > .spekificity/config.json

# Run update
.spekificity/bin/spek update
# Output shows error and recovery guidance

# Exit code 1
echo $?
```

---

## Scenario 7: Update Idempotency

**Given**: `spek update` already run once

**When**: User runs `spek update` again

**Then**:

- No errors
- Same output as first run
- Execution time <5 seconds
- Skill index unchanged (already current)
- Config preserved (unchanged)

**Evidence**:
```bash
# First run
time .spekificity/bin/spek update
# Output: Update complete, duration ~2s

# Second run (idempotent)
time .spekificity/bin/spek update
# Output: Same as first run, duration <1s
```

---

## Test Execution Checklist

### Pre-Tests

- [ ] Spekificity initialized: `spek status --json | jq '.spek_initialized'` returns `true`
- [ ] Config exists: `.spekificity/config.json` present
- [ ] Skill index exists: `.spekificity/skill-index.md` present

### Execute Scenarios

- [ ] **Scenario 1**: `spek update` shows stub message
- [ ] **Scenario 2**: `spek update --help` shows help text
- [ ] **Scenario 3**: `spek update --dry-run` previews without changes
- [ ] **Scenario 4**: Custom preferences preserved after update
- [ ] **Scenario 5**: `spek update --verbose` shows detailed output
- [ ] **Scenario 6**: Error handling works gracefully
- [ ] **Scenario 7**: Idempotent re-run succeeds

### Post-Tests

- [ ] Exit codes correct (0 for success, 1 for failure)
- [ ] All output messages clear and actionable
- [ ] No unexpected files created or modified
- [ ] Skill index valid and current
- [ ] Config schema valid

---

## Success Criteria

✅ All 7 scenarios execute without errors  
✅ Exit codes correct  
✅ Output messages clear  
✅ Idempotent re-runs safe  
✅ Config preservation working  
✅ Help text accurate  

---

## Phase 6 Preview (v1.1.0)

Future enhancements (after MVP):
- Automatic version checking against remote repo
- Incremental skill sync (only changed files)
- Conflict resolution for custom skills
- Automatic backups before major updates
- Update scheduling and notifications
- Rollback to previous version

---

**Status**: Ready for testing  
**Phase**: MVP (v1.0.0 stub)  
**Next Phase**: Phase 6 full implementation (v1.1.0)
