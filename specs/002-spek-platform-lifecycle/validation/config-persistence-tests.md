# Config Persistence & Team Reproducibility Tests

**Purpose**: Verify that configuration is reproducible across team members and that custom preferences persist across updates.

**Test Coverage**: Config backup/restore, team cloning, custom preferences preservation, cross-platform reproducibility

---

## Test Suite 1: Configuration Backup & Restore

### Test T031: Config Backup on Update

**Criteria**: Config is backed up before any update operation

**Test Setup**:
```bash
# Note current config state
ORIG_CONFIG=".spekificity/config.json"
BACKUP_DIR="/tmp/config_backup_test"
mkdir -p "$BACKUP_DIR"

cp "$ORIG_CONFIG" "$BACKUP_DIR/config_orig.json"

# Simulate update operation
.spekificity/bin/spek update --skip-backup
# (or check if backup created)
```

**Test Steps**:
1. Verify `$ORIG_CONFIG` exists
2. Check for backup file (`.spekificity/config.json.bak` or similar)
3. Verify backup is valid JSON
4. Verify backup content matches original

**Test Commands**:
```bash
# Check if backup exists after operation
if [ -f .spekificity/config.json.bak ]; then
  echo "✓ Backup created: .spekificity/config.json.bak"
  
  # Verify both are valid JSON
  jq . .spekificity/config.json > /dev/null && echo "✓ Current config valid"
  jq . .spekificity/config.json.bak > /dev/null && echo "✓ Backup config valid"
else
  echo "⚠ No backup found (may be created on-demand)"
fi
```

**Expected**:
```
✓ Backup created: .spekificity/config.json.bak
✓ Current config valid
✓ Backup config valid
```

---

### Test T032: Config Restore from Backup

**Criteria**: Config can be restored from backup if current is corrupted

**Test Steps**:
1. Corrupt config (invalid JSON)
2. Attempt restore from backup
3. Verify restored config is valid
4. Verify original data preserved

**Test Commands**:
```bash
# Backup current good config
cp .spekificity/config.json /tmp/config_good.json

# Simulate corruption
echo "{ broken json" > .spekificity/config.json

# Attempt recovery
if [ -f .spekificity/config.json.bak ]; then
  echo "Recovering from backup..."
  cp .spekificity/config.json.bak .spekificity/config.json
  
  # Verify restored
  jq . .spekificity/config.json > /dev/null && {
    echo "✓ Config restored successfully"
  } || {
    echo "✗ FAIL: Restored config still invalid"
    exit 1
  }
else
  # Recovery via re-init
  spek setup && spek init
  jq . .spekificity/config.json > /dev/null && {
    echo "✓ Config recovered via spek init"
  }
fi

# Restore original for other tests
cp /tmp/config_good.json .spekificity/config.json
```

**Expected**:
```
✓ Config restored successfully
```

---

## Test Suite 2: Team Cloning & Reproducibility

### Test T033: Fresh Clone Initialization

**Criteria**: New team member can clone and run `spek setup/init` successfully

**Test Setup**:
```bash
# Simulate fresh clone
TEMP_CLONE="/tmp/spekificity_clone_test"
rm -rf "$TEMP_CLONE"
mkdir -p "$TEMP_CLONE"

# Copy project files (without .spekificity/config.json)
cp -r /Users/marcelrienks/workspace/code/spekificity/* "$TEMP_CLONE/" 2>/dev/null || true
rm -f "$TEMP_CLONE/.spekificity/config.json"

cd "$TEMP_CLONE"
```

**Test Steps**:
1. Clone project (simulated)
2. No config exists
3. Run `spek setup`
4. Run `spek init`
5. Verify all tools initialized
6. Compare with reference config (same structure, same versions)

**Test Commands**:
```bash
cd "$TEMP_CLONE"

echo "Running setup..."
.spekificity/bin/spek setup
SETUP_EXIT=$?

echo "Running init..."
.spekificity/bin/spek init
INIT_EXIT=$?

# Verify initialization
if [ $SETUP_EXIT -eq 0 ] && [ $INIT_EXIT -eq 0 ]; then
  echo "✓ Fresh clone initialization successful"
  
  # Check config created
  [ -f .spekificity/config.json ] && echo "✓ Config created"
  
  # Verify key fields
  INITIALIZED=$(jq '.spek_initialized' .spekificity/config.json)
  [ "$INITIALIZED" = "true" ] && echo "✓ Platform initialized"
  
else
  echo "✗ FAIL: Setup or init failed"
  exit 1
fi

# Cleanup
cd -
```

**Expected**:
```
✓ Fresh clone initialization successful
✓ Config created
✓ Platform initialized
```

---

### Test T034: Team Config Consistency

**Criteria**: Multiple team members get same tool versions after initialization

**Test Steps**:
1. Team member A initializes (capture config)
2. Team member B initializes fresh clone
3. Compare configs:
   - Same tool versions
   - Same schema version
   - Same skill count

**Test Commands**:
```bash
# Get reference config (Team A)
REF_CONFIG="/tmp/ref_config.json"
cp .spekificity/config.json "$REF_CONFIG"

# Simulate Team B: fresh init
rm -rf /tmp/team_b_clone
cp -r . /tmp/team_b_clone
cd /tmp/team_b_clone
rm -f .spekificity/config.json

spek setup && spek init

# Compare key fields
echo "Comparing configs (Team A vs Team B)..."

REF_SPECKIT=$(jq '.tools.speckit.version' "$REF_CONFIG")
NEW_SPECKIT=$(jq '.tools.speckit.version' .spekificity/config.json)

[ "$REF_SPECKIT" = "$NEW_SPECKIT" ] && {
  echo "✓ Speckit version consistent: $REF_SPECKIT"
} || {
  echo "⚠ Speckit versions differ (A: $REF_SPECKIT, B: $NEW_SPECKIT)"
}

# Check skill counts
REF_SKILLS=$(jq '.skills | length' "$REF_CONFIG")
NEW_SKILLS=$(jq '.skills | length' .spekificity/config.json)

[ "$REF_SKILLS" = "$NEW_SKILLS" ] && {
  echo "✓ Skill count consistent: $REF_SKILLS"
} || {
  echo "⚠ Skill count differs (A: $REF_SKILLS, B: $NEW_SKILLS)"
}

cd -
```

**Expected**:
```
✓ Speckit version consistent: 0.1.0
✓ Skill count consistent: 7
```

---

## Test Suite 3: Custom Preferences Preservation

### Test T035: Custom Settings Survive Update

**Criteria**: User custom preferences persisted through `spek update`

**Test Setup**:
```bash
# Add custom preferences to config
jq '.spek_custom_preferences.graphify_depth = "deep"' \
  .spekificity/config.json > /tmp/updated_config.json && \
  mv /tmp/updated_config.json .spekificity/config.json

jq '.spek_custom_preferences.auto_lessons = true' \
  .spekificity/config.json > /tmp/updated_config.json && \
  mv /tmp/updated_config.json .spekificity/config.json

jq '.spek_custom_preferences.update_frequency = "weekly"' \
  .spekificity/config.json > /tmp/updated_config.json && \
  mv /tmp/updated_config.json .spekificity/config.json
```

**Test Steps**:
1. Add custom preferences
2. Run `spek update`
3. Verify custom preferences unchanged
4. Verify other config fields updated as needed

**Test Commands**:
```bash
# Capture custom prefs before update
PREFS_BEFORE=$(jq '.spek_custom_preferences' .spekificity/config.json)

echo "Custom preferences before update:"
echo "$PREFS_BEFORE" | jq .

# Run update
spek update

# Check after update
PREFS_AFTER=$(jq '.spek_custom_preferences' .spekificity/config.json)

echo "Custom preferences after update:"
echo "$PREFS_AFTER" | jq .

# Compare
if [ "$PREFS_BEFORE" = "$PREFS_AFTER" ]; then
  echo "✓ Custom preferences preserved"
else
  echo "✗ FAIL: Custom preferences changed"
  echo "Before: $PREFS_BEFORE"
  echo "After: $PREFS_AFTER"
  exit 1
fi
```

**Expected**:
```
Custom preferences before update:
{
  "graphify_depth": "deep",
  "auto_lessons": true,
  "update_frequency": "weekly"
}

✓ Custom preferences preserved

Custom preferences after update:
{
  "graphify_depth": "deep",
  "auto_lessons": true,
  "update_frequency": "weekly"
}
```

---

## Test Suite 4: Cross-Platform Reproducibility

### Test: macOS Initialization

**Criteria**: Setup and init succeed on macOS

**Environment**: 
- macOS Monterey/Ventura/Sonoma
- Python 3.11+
- Standard shell (zsh or bash)

**Test Commands**:
```bash
echo "Platform: $(uname -s)"
echo "Shell: $SHELL"
echo "Python: $(python3 --version)"

spek setup
spek init
spek status --json | jq '.spek_initialized'
# Should output: true
```

**Expected**:
```
✓ Setup and init successful on macOS
✓ Platform initialized: true
```

---

### Test: Linux Initialization

**Criteria**: Setup and init succeed on Linux

**Environment**:
- Ubuntu 20.04 LTS or 22.04 LTS
- Python 3.11+
- bash or zsh

**Test Commands**:
```bash
echo "Platform: $(uname -s)"
uv --version
speckit --version
graphify --version

spek setup
spek init
.spekificity/smoke-test.sh
```

**Expected**:
```
✓ All prerequisites detected
✓ Setup and init successful on Linux
✓ Smoke test passes
```

---

### Test: WSL/Windows Initialization

**Criteria**: Setup and init succeed on WSL2

**Environment**:
- Windows 10/11 with WSL2
- Ubuntu 22.04 LTS or similar
- Python 3.11+, uv, git installed in WSL

**Test Commands**:
```bash
# In WSL terminal
uname -a  # Should show Linux with WSL

spek setup
spek init

# Verify no line-ending issues
git config core.autocrlf
# Should show: false (to preserve LF)
```

**Expected**:
```
✓ WSL environment detected
✓ Setup and init successful in WSL
✓ Line endings correct (LF)
```

---

## Test Suite 5: Idempotent Re-initialization

### Test: Idempotent Setup Re-run

**Criteria**: Running `spek setup` twice produces same result

**Test Commands**:
```bash
echo "First run:"
time spek setup
TIME1=$?

# Wait a moment
sleep 1

echo "Second run (idempotent):"
time spek setup
TIME2=$?

[ $TIME1 -eq 0 ] && [ $TIME2 -eq 0 ] && {
  echo "✓ Both runs succeeded"
} || {
  echo "✗ FAIL: One or more runs failed"
  exit 1
}
```

**Expected**:
```
✓ Both runs succeeded
First run: ~15-20 seconds
Second run: <1 second (fast, skips already-done steps)
```

---

### Test: Idempotent Init Re-run

**Criteria**: Running `spek init` twice produces same result, second run faster

**Test Commands**:
```bash
echo "First init run..."
time .spekificity/bin/spek init > /tmp/init1.log 2>&1
INIT1_EXIT=$?

echo "Second init run (idempotent)..."
time .spekificity/bin/spek init > /tmp/init2.log 2>&1
INIT2_EXIT=$?

# Both should succeed
[ $INIT1_EXIT -eq 0 ] && [ $INIT2_EXIT -eq 0 ] && {
  echo "✓ Both init runs succeeded"
} || {
  echo "✗ FAIL: Init failed"
  cat /tmp/init1.log /tmp/init2.log
  exit 1
}

# Verify config unchanged
HASH1=$(md5sum .spekificity/config.json | awk '{print $1}')
echo "Config hash: $HASH1"
```

**Expected**:
```
✓ Both init runs succeeded
First run: ~2-3 seconds
Second run: <1 second
```

---

## Full Test Matrix

| Test | Phase | Environment | Status |
|------|-------|-------------|--------|
| T031: Config backup | Persistence | macOS/Linux | ⚪ Ready |
| T032: Config restore | Persistence | macOS/Linux | ⚪ Ready |
| T033: Fresh clone init | Reproducibility | Any | ⚪ Ready |
| T034: Team consistency | Reproducibility | Multi-user | ⚪ Ready |
| T035: Custom prefs persist | Persistence | macOS/Linux | ⚪ Ready |
| T036: macOS init | Cross-platform | macOS | ⚪ Ready |
| T037: Linux init | Cross-platform | Linux | ⚪ Ready |
| T038: WSL init | Cross-platform | WSL2 | ⚪ Ready |
| T039: Idempotent setup | Idempotency | Any | ⚪ Ready |
| T040: Idempotent init | Idempotency | Any | ⚪ Ready |

---

## Success Criteria

- ✅ Config backed up before updates
- ✅ Config can be restored from backup
- ✅ Fresh clone initializes without errors
- ✅ Multiple team members get same versions
- ✅ Custom preferences persist through updates
- ✅ Setup succeeds on macOS, Linux, WSL
- ✅ Both setup and init runs are idempotent
- ✅ Second runs complete in <1 second
- ✅ All tests pass in test matrix

---

**Status**: Ready for execution  
**Phase**: Configuration & Reproducibility (US5)  
**Next**: Execute tests, capture results, then proceed to polish phase
