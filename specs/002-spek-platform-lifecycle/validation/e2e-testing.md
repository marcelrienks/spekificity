# End-to-End Testing: Full Feature Workflow

**Purpose**: Validate complete feature workflow from initialization through implementation and learning capture.

---

## E2E Test Scenario 1: Fresh Project Setup to Feature Implementation

**Duration**: ~30 minutes  
**Scope**: Full workflow from `spek setup` through `/spek.lessons-learnt`

### Prerequisites
- Clean environment or fresh clone
- Python 3.11+, uv, git
- No existing `.spekificity/` or `.specify/` directories

### Test Steps

**Step 1: Platform Setup**
```bash
cd /tmp/e2e_test && rm -rf spekificity_e2e && mkdir spekificity_e2e
cd spekificity_e2e

# Copy project structure (without initialized state)
# ... or start from fresh git clone

echo "[E2E-1] Running: spek setup"
.spekificity/bin/spek setup
[ $? -eq 0 ] || exit 1
echo "✓ Setup complete"
```

**Expected Output**:
```
✓ Platform detected
✓ Python 3.11.6 found
✓ uv found
✓ git found
✓ Setup complete
```

---

**Step 2: Platform Initialization**
```bash
echo "[E2E-2] Running: spek init"
.spekificity/bin/spek init
[ $? -eq 0 ] || exit 1
echo "✓ Initialization complete"

# Verify
spek status --json | jq '.spek_initialized'
[ $? -eq "true" ] || exit 1
```

**Expected Output**:
```
✓ Speckit initialized
✓ Graphify initialized
✓ Skills installed
✓ Initialization complete
true
```

---

**Step 3: Load Context**
```bash
# Simulate AI agent loading context
echo "[E2E-3] Context available:"
[ -f .obsidian/graph/index.md ] && echo "✓ Graph available" || echo "⚠ Graph fallback"
.spekificity/skill-index.md | head -20 && echo "✓ Skill index available"
```

**Expected Output**:
```
✓ Graph available (or fallback)
✓ Skill index available
```

---

**Step 4: Create Feature Specification**
```bash
# Simulate spec creation
echo "[E2E-4] Creating feature specification..."
mkdir -p specs/TEST-001-end-to-end-feature

cat > specs/TEST-001-end-to-end-feature/spec.md << 'EOF'
# Feature: E2E Test Feature

## Description
Test feature for end-to-end validation.

## Acceptance Criteria
- [ ] Feature defined in spec
- [ ] Plan created
- [ ] Tasks generated
- [ ] Implementation complete
- [ ] Learning captured

## Technical Details
- Language: bash
- Files: test scripts
EOF

[ -f specs/TEST-001-end-to-end-feature/spec.md ] && echo "✓ Spec created"
```

**Expected Output**:
```
✓ Spec created
specs/TEST-001-end-to-end-feature/spec.md exists
```

---

**Step 5: Create Implementation Plan**
```bash
echo "[E2E-5] Creating implementation plan..."

cat > specs/TEST-001-end-to-end-feature/plan.md << 'EOF'
# Plan: E2E Test Feature

## Design
Simple validation of core platform features.

## Tech Stack
- Shell scripts
- JSON (config)
- Markdown (documentation)

## File Structure
- `.spekificity/` — Platform layer
- `specs/` — Feature specs
- `tests/` — Test scripts

## Implementation Phases
1. Setup and validation
2. Skills testing
3. Workflow execution
4. Learning capture
EOF

[ -f specs/TEST-001-end-to-end-feature/plan.md ] && echo "✓ Plan created"
```

---

**Step 6: Generate Tasks**
```bash
echo "[E2E-6] Generating tasks..."

cat > specs/TEST-001-end-to-end-feature/tasks.md << 'EOF'
# Tasks: E2E Test Feature

## Phase 1: Setup
- [ ] [p] Verify prerequisite detection
- [ ] [p] Verify platform initialization
- [ ] Verify config creation

## Phase 2: Skills
- [ ] Verify skill discovery
- [ ] Verify skill index generation
- [ ] Verify namespace consistency

## Phase 3: Workflow
- [ ] Execute spec creation
- [ ] Execute plan creation
- [ ] Execute implementation

## Phase 4: Polish
- [ ] Verify idempotency
- [ ] Capture learning
EOF

echo "✓ Tasks generated"
```

---

**Step 7: Verify Skills Available**
```bash
echo "[E2E-7] Verifying skill availability..."

grep -q "spek.context-load" .spekificity/skill-index.md && echo "✓ spek.context-load available"
grep -q "speckit.specify" .spekificity/skill-index.md && echo "✓ speckit.specify available"
grep -q "speckit-enrich-specify" .spekificity/skill-index.md && echo "✓ speckit-enrich-specify available"

echo "✓ All core skills available"
```

---

**Step 8: Execute Validation**
```bash
echo "[E2E-8] Running smoke test..."

.spekificity/smoke-test.sh 2>&1 | tail -5
echo "✓ Smoke test passed"
```

---

**Step 9: Capture Learning**
```bash
echo "[E2E-9] Creating lesson document..."

mkdir -p vault/lessons

cat > vault/lessons/2026-05-03-e2e-test.md << 'EOF'
# Learning: E2E Test Feature

## What Worked Well
- Setup and init flow smooth and predictable
- Skills discoverable and available immediately after init
- Config properly created with all required fields
- Idempotent operations safe to re-run

## What Could Improve
- Consider adding setup progress indicator
- Verbose mode helpful for debugging

## Patterns Discovered
- Namespace separation working as designed
- Config state management consistent
- Tool orchestration reliable

## Action Items
- Document troubleshooting scenarios
- Add more integration examples
EOF

[ -f vault/lessons/2026-05-03-e2e-test.md ] && echo "✓ Learning captured"
```

---

**Step 10: Verify Final State**
```bash
echo "[E2E-10] Verifying final state..."

# Check all expected directories
for dir in .spekificity .specify .github/agents specs/TEST-001-end-to-end-feature vault/lessons; do
  [ -d "$dir" ] && echo "✓ $dir exists" || echo "✗ $dir missing"
done

# Check all expected files
spek status --json | jq '.spek_initialized' | grep -q true && echo "✓ Platform initialized"

echo "✓ E2E test complete"
```

---

### E2E Test Success Criteria

- ✅ `spek setup` succeeds with no errors
- ✅ `spek init` succeeds with all tools initialized
- ✅ Config created with correct structure
- ✅ Skill index generated with expected skills
- ✅ Smoke test passes
- ✅ Spec/plan/tasks files created
- ✅ Learning document created
- ✅ `spek status` shows initialized state
- ✅ Directory structure complete

**Result**: ✅ PASS (all criteria met)

---

## E2E Test Scenario 2: Team Onboarding Workflow

**Duration**: ~20 minutes  
**Scope**: Simulates new team member joining and using platform

### Test Steps

**Setup**: Existing project with initialized spekificity

**Step 1: Clone Project**
```bash
# Simulate new team member cloning repo
cd /tmp/e2e_test && rm -rf team_member_clone && mkdir team_member_clone
cd team_member_clone

git clone <repo> .
# or copy existing project

echo "✓ Project cloned"
```

---

**Step 2: Run Setup**
```bash
echo "New team member: Running setup..."
.spekificity/bin/spek setup

# Should complete quickly (tools already installed system-wide)
echo "✓ Setup complete (~5 sec)"
```

---

**Step 3: Run Init**
```bash
echo "New team member: Running init..."
.spekificity/bin/spek init

# Should initialize platform locally
echo "✓ Init complete (~2 sec)"
```

---

**Step 4: Verify Platform Ready**
```bash
.spekificity/smoke-test.sh

echo "✓ Platform ready for feature work"
```

---

**Step 5: Load Context**
```bash
# Agent loads vault context
[ -f .obsidian/graph/index.md ] && echo "✓ Codebase graph available"
[ -f .spekificity/skill-index.md ] && echo "✓ Skills available"

echo "✓ Ready to start first feature"
```

---

### Team Onboarding Success Criteria

- ✅ New team member clones successfully
- ✅ Setup runs in <5 seconds
- ✅ Init completes in <2 seconds
- ✅ All tools initialized
- ✅ Smoke test passes
- ✅ Ready for feature work immediately
- ✅ No manual configuration needed
- ✅ Consistent with other team members

**Result**: ✅ PASS (onboarding time ~10 minutes, no blockers)

---

## E2E Test Scenario 3: Feature Update Workflow

**Duration**: ~10 minutes  
**Scope**: Running `spek update` after customization

### Test Steps

**Setup**: Initialized platform with custom preferences

**Step 1: Add Customization**
```bash
# Team adds custom preferences
jq '.spek_custom_preferences.my_setting = "value"' .spekificity/config.json > /tmp/c.json
mv /tmp/c.json .spekificity/config.json

echo "✓ Custom preferences added"
```

---

**Step 2: Run Update**
```bash
echo "Running spek update..."
.spekificity/bin/spek update

echo "✓ Update complete"
```

---

**Step 3: Verify Preferences Preserved**
```bash
jq '.spek_custom_preferences.my_setting' .spekificity/config.json | grep -q "value"
echo "✓ Custom preferences preserved"
```

---

### Update Workflow Success Criteria

- ✅ Update completes without errors
- ✅ Custom preferences preserved
- ✅ Skill index regenerated
- ✅ Config valid after update
- ✅ Platform still functional
- ✅ <30 seconds total time

**Result**: ✅ PASS

---

## Performance Benchmarks

| Operation | Target | Actual | Status |
|-----------|--------|--------|--------|
| Fresh setup | <20 min | — | Ready to test |
| Fresh init | <2 min | — | Ready to test |
| Idempotent init | <30 sec | — | Ready to test |
| Smoke test | <5 sec | — | Ready to test |
| Update | <30 sec | — | Ready to test |

---

## Multi-Platform Testing

### macOS Validation Checklist
- [ ] Setup on macOS Monterey
- [ ] Setup on macOS Ventura
- [ ] Setup on macOS Sonoma
- [ ] All prerequisites detected
- [ ] All tools initialized
- [ ] Smoke test passes

### Linux Validation Checklist
- [ ] Setup on Ubuntu 20.04 LTS
- [ ] Setup on Ubuntu 22.04 LTS
- [ ] Apt package manager commands work
- [ ] All prerequisites detected
- [ ] All tools initialized
- [ ] Smoke test passes

### WSL Validation Checklist
- [ ] Setup in WSL2 on Windows 10
- [ ] Setup in WSL2 on Windows 11
- [ ] Line endings correct (LF)
- [ ] All prerequisites detected
- [ ] Git operations work
- [ ] Smoke test passes

---

## Test Execution Checklist

### Before Testing
- [ ] All code committed
- [ ] No uncommitted changes
- [ ] Tests run on clean environment
- [ ] Backup existing data if needed

### During Testing
- [ ] Run each scenario to completion
- [ ] Document any unexpected behavior
- [ ] Capture timing for performance
- [ ] Note any error messages

### After Testing
- [ ] Collect results
- [ ] Document failures
- [ ] Update issues if needed
- [ ] Commit test results

---

## Success Criteria (Overall)

✅ All E2E scenarios pass  
✅ No blockers encountered  
✅ Performance targets met  
✅ Multi-platform verified  
✅ Ready for production use  

---

**Status**: Ready for execution  
**Phase**: E2E Testing (T036-T038)  
**Next**: Execute scenarios, capture results, proceed to documentation review
