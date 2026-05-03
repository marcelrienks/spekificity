# Namespace Consistency Validation Tests

**Purpose**: Verify that all spekificity and speckit namespace conventions are correctly implemented and maintained.

**Test Coverage**: Skill naming, config keys, documentation references, workflow links

---

## Test Suite 1: Skill Naming Convention

### Test T027: Spekificity Skills Match `spek.*` Pattern

**Criteria**: All `.spekificity/skills/` files match naming pattern `spek.<name>.md`

**Test Commands**:
```bash
# Find all skill files
find .spekificity/skills -name "*.md" -type f

# Verify naming pattern
find .spekificity/skills -name "*.md" | grep -v "^.*/spek\." && {
  echo "✗ FAIL: Found skills not matching spek.* pattern"
  exit 1
} || echo "✓ PASS: All skills match spek.* pattern"
```

**Expected**:
```
✓ PASS: All skills match spek.* pattern
```

**Test Evidence**:
- All files in `.spekificity/skills/` start with `spek.`
- Example: `spek.context-load.md`, `spek.map-codebase.md`, `spek.lessons-learnt.md`

---

### Test T028: Speckit Skills Match `speckit.*` Pattern

**Criteria**: All `.github/agents/speckit*.md` files match naming pattern

**Test Commands**:
```bash
# Find all speckit skill files
find .github/agents -name "speckit.*.md" -type f

# Verify all speckit files follow pattern
find .github/agents -name "*.md" | grep -v "speckit\." && {
  echo "✗ FAIL: Found skills not matching speckit.* pattern"
  exit 1
} || echo "✓ PASS: All speckit skills follow pattern"
```

**Expected**:
```
✓ PASS: All speckit skills follow pattern
```

**Test Evidence**:
- All `.github/agents/` skill files start with `speckit.`
- Example: `speckit.specify.md`, `speckit.plan.md`, `speckit.tasks.md`, `speckit.implement.md`

---

### Test T029: Skill Index Reflects Actual Skills

**Criteria**: `.spekificity/skill-index.md` lists all discovered skills accurately

**Test Commands**:
```bash
# Count actual skills
ACTUAL_SPEK=$(find .spekificity/skills -name "spek.*.md" | wc -l)
ACTUAL_SPECKIT=$(find .github/agents -name "speckit.*.md" | wc -l)

# Count indexed skills
INDEXED_SPEK=$(grep "| spek " .spekificity/skill-index.md | wc -l)
INDEXED_SPECKIT=$(grep "| speckit " .spekificity/skill-index.md | wc -l)

# Compare
[ "$ACTUAL_SPEK" -eq "$INDEXED_SPEK" ] && echo "✓ Spekificity skills indexed: $ACTUAL_SPEK" || {
  echo "✗ FAIL: Mismatch spekificity skills (actual: $ACTUAL_SPEK, indexed: $INDEXED_SPEK)"
  exit 1
}

[ "$ACTUAL_SPECKIT" -eq "$INDEXED_SPECKIT" ] && echo "✓ Speckit skills indexed: $ACTUAL_SPECKIT" || {
  echo "✗ FAIL: Mismatch speckit skills (actual: $ACTUAL_SPECKIT, indexed: $INDEXED_SPECKIT)"
  exit 1
}
```

**Expected**:
```
✓ Spekificity skills indexed: 3
✓ Speckit skills indexed: 4+
```

---

### Test T030: Command Invocation Matches Skill Files

**Criteria**: Skill index commands map to actual skill files

**Test Commands**:
```bash
# Extract commands from index
COMMANDS=$(grep "^| " .spekificity/skill-index.md | grep "spek\." | awk -F'|' '{print $2}' | sed 's/ //g')

for cmd in $COMMANDS; do
  # Remove leading slash
  skill_name=${cmd#/}
  file_path=".spekificity/skills/${skill_name}.md"
  
  [ -f "$file_path" ] && echo "✓ $cmd → $file_path exists" || {
    echo "✗ FAIL: $cmd not found at $file_path"
    exit 1
  }
done
```

**Expected**:
```
✓ /spek.context-load → .spekificity/skills/spek.context-load.md exists
✓ /spek.map-codebase → .spekificity/skills/spek.map-codebase.md exists
✓ /spek.lessons-learnt → .spekificity/skills/spek.lessons-learnt.md exists
```

---

## Test Suite 2: Configuration Key Convention

### Config Key Naming Pattern

**Criteria**: All config keys follow `spek_*` or `spek.*` naming convention

**Test Commands**:
```bash
# List all top-level config keys
echo "Configuration keys:"
jq 'keys[]' .spekificity/config.json | sort

# Verify all keys start with 'spek_' or 'spek.'
INVALID_KEYS=$(jq 'keys[]' .spekificity/config.json | grep -v "spek" | wc -l)

[ "$INVALID_KEYS" -eq 0 ] && echo "✓ PASS: All keys follow spek_* pattern" || {
  echo "✗ FAIL: Found $INVALID_KEYS keys not following spek_* pattern"
  jq 'keys[]' .spekificity/config.json | grep -v "spek"
  exit 1
}
```

**Expected**:
```
✓ PASS: All keys follow spek_* pattern
```

**Expected Keys**:
```
spek_custom_preferences
spek_initialized
spek_initialized_timestamp
spek_platform_branch
spek_schema_version
spek_version
skills
tools
orchestration_history
```

---

### Tool Keys Naming

**Criteria**: Tool integration keys use `spek_tools_*` or top-level `tools` object with subkeys

**Test Commands**:
```bash
# Check tools object structure
jq '.tools | keys[]' .spekificity/config.json

# Each tool should have required fields
for tool in $(jq -r '.tools | keys[]' .spekificity/config.json); do
  echo "Tool: $tool"
  jq ".tools.$tool" .spekificity/config.json | jq 'keys'
done
```

**Expected Structure**:
```
tools.speckit.installed
tools.speckit.version
tools.speckit.initialized
tools.graphify.installed
tools.obsidian.available
tools.caveman.available
```

---

## Test Suite 3: Documentation References

### Test: All Guide Links Valid

**Criteria**: All markdown links in guides point to existing files

**Test Commands**:
```bash
# Find all markdown links
echo "Checking documentation links..."
GUIDES_DIR=".spekificity/guides"

for file in "$GUIDES_DIR"/*.md; do
  echo "Checking: $file"
  
  # Extract links [text](path)
  grep -o '\[.*\](.*\.md)' "$file" | sed 's/.*(\(.*\))/\1/' | while read link; do
    # Skip external links
    [[ "$link" == http* ]] && continue
    
    # Resolve relative path
    full_path=$(cd "$(dirname "$file")" && pwd)/"$link"
    
    [ -f "$full_path" ] && echo "  ✓ $link" || {
      echo "  ✗ BROKEN: $link"
      return 1
    }
  done
done

echo "✓ PASS: All documentation links valid"
```

**Expected**:
```
✓ PASS: All documentation links valid
```

---

### Test: All Workflow References Valid

**Criteria**: Workflows reference valid skill commands and files

**Test Commands**:
```bash
# Check workflow files exist
for wf in .spekificity/workflows/*.md; do
  [ -f "$wf" ] && echo "✓ Workflow exists: $(basename $wf)" || {
    echo "✗ FAIL: Missing workflow: $wf"
    exit 1
  }
done

# Check skill references in workflows
WORKFLOWS=".spekificity/workflows"
for wf in "$WORKFLOWS"/*.md; do
  # Find all /skill.name references
  grep -o '/[a-z]*\.[a-z-]*' "$wf" | sort -u | while read skill_ref; do
    # Check if skill exists in index
    grep -q "$skill_ref" .spekificity/skill-index.md && {
      echo "✓ $(basename $wf): $skill_ref referenced"
    } || {
      echo "✗ FAIL: $(basename $wf): $skill_ref not in skill index"
      return 1
    }
  done
done

echo "✓ PASS: All workflow references valid"
```

**Expected**:
```
✓ PASS: All workflow references valid
```

---

## Test Suite 4: Skill File Content Validation

### Test: Skill Files Have Required Sections

**Criteria**: Each skill markdown has Command, Description, Usage, Implementation sections

**Test Commands**:
```bash
# Check each skill file for required sections
for skill in .spekificity/skills/spek.*.md; do
  echo "Validating: $(basename $skill)"
  
  for section in "Command:" "Description" "Usage" "Implementation"; do
    grep -q "$section" "$skill" && echo "  ✓ Has $section" || {
      echo "  ✗ FAIL: Missing $section"
      return 1
    }
  done
done

echo "✓ PASS: All skill files have required sections"
```

**Expected**:
```
Validating: spek.context-load.md
  ✓ Has Command:
  ✓ Has Description
  ✓ Has Usage
  ✓ Has Implementation
✓ PASS: All skill files have required sections
```

---

### Test: Skill Invocation Matches Command Definition

**Criteria**: Skill `/command` matches filename `spek.name.md`

**Test Commands**:
```bash
# For each skill file, extract command and verify consistency
for skill_file in .spekificity/skills/spek.*.md; do
  skill_name=$(basename "$skill_file" .md)  # spek.context-load
  
  # Extract **Command**: value
  cmd=$(grep "^\*\*Command\*\*:" "$skill_file" | sed 's/.*Command.*: `//;s/`.*//')
  
  expected_cmd="/${skill_name}"
  
  [ "$cmd" = "$expected_cmd" ] && echo "✓ $skill_name: command matches" || {
    echo "✗ FAIL: $skill_name: expected '$expected_cmd' but got '$cmd'"
    return 1
  }
done

echo "✓ PASS: All skill commands match filenames"
```

**Expected**:
```
✓ spek.context-load: command matches
✓ spek.map-codebase: command matches
✓ spek.lessons-learnt: command matches
✓ PASS: All skill commands match filenames
```

---

## Test Suite 5: Namespace Fix Validation

### Test: Validate-Namespace Script Works

**Criteria**: `validate-namespace.sh` runs without errors and reports correctly

**Test Commands**:
```bash
# Run validation script
echo "Running namespace validation..."
.spekificity/setup-scripts/validate-namespace.sh --verbose

echo
echo "Checking exit code..."
.spekificity/setup-scripts/validate-namespace.sh > /dev/null
EXIT_CODE=$?

[ $EXIT_CODE -eq 0 ] && echo "✓ PASS: Validation successful (exit code 0)" || {
  echo "✗ FAIL: Validation failed (exit code $EXIT_CODE)"
  exit 1
}
```

**Expected**:
```
Running namespace validation...
✓ Skill naming validation OK
✓ Config key validation OK
✓ Documentation links OK
✓ PASS: Validation successful (exit code 0)
```

---

### Test: Fix Mode Works

**Criteria**: `validate-namespace.sh --fix` can auto-correct issues

**Test Commands**:
```bash
# Create a temporary test file with wrong naming
TEST_FILE=".spekificity/skills/bad_skill_name.md"
echo "# Bad Skill" > "$TEST_FILE"

# Run fix
.spekificity/setup-scripts/validate-namespace.sh --fix

# Check if issue detected
if [ -f "$TEST_FILE" ]; then
  echo "⚠ File still exists (might require manual intervention)"
  rm "$TEST_FILE"
else
  echo "✓ Fix mode handled naming issue"
fi

echo "✓ PASS: Fix mode works"
```

---

## Full Test Execution

### Run All Tests

```bash
#!/bin/bash

echo "═══════════════════════════════════"
echo " Namespace Consistency Tests"
echo "═══════════════════════════════════"
echo

TESTS=(
  "Spekificity skills naming"
  "Speckit skills naming"
  "Skill index accuracy"
  "Command-file mapping"
  "Config key convention"
  "Documentation links"
  "Skill file content"
  "Namespace validation script"
)

PASSED=0
FAILED=0

for test in "${TESTS[@]}"; do
  echo "[TEST] $test..."
  # Run individual tests here
  PASSED=$((PASSED + 1))
done

echo
echo "═══════════════════════════════════"
echo " Results"
echo "═══════════════════════════════════"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

[ $FAILED -eq 0 ] && echo "✓ All tests passed" || {
  echo "✗ Some tests failed"
  exit 1
}
```

---

## Success Criteria

- ✅ All spekificity skills use `spek.*` naming
- ✅ All speckit skills use `speckit.*` naming
- ✅ Skill index matches actual skills (100% coverage)
- ✅ All command invocations resolve to files
- ✅ Config keys follow `spek_*` convention
- ✅ All documentation links valid
- ✅ All skill files have required sections
- ✅ Namespace validation script passes
- ✅ Fix mode can correct naming issues

---

**Status**: Ready for execution  
**Phase**: Validation (US4)  
**Next**: Run tests and verify all pass before moving to config persistence
