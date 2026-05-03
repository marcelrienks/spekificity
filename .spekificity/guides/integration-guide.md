# Integration Guide: Using Spekificity in Your Workflow

**Purpose**: How to integrate spekificity into your daily feature development.

## Feature Workflow Integration

### Day 1: Setup

```bash
# 1. Clone your project
git clone https://github.com/your-org/your-project.git
cd your-project

# 2. Run setup (one-time)
.spekificity/bin/spek setup
#   Output: Prerequisites verified

# 3. Run initialization
.spekificity/bin/spek init
#   Output: All tools initialized, skill index ready
```

**Result**: Project ready for feature development.

---

### Day N: Start Feature

**In your AI chat** (GitHub Copilot or Claude):

#### Step 1: Load Context

```
/context-load
```

AI loads your vault:
- Codebase graph
- Architectural decisions
- Recent lessons learned
- Current project state

#### Step 2: Start Feature Specification

```
/speckit-enrich-specify

Create a new feature: [your feature description]
```

AI creates: `specs/NNN-feature-name/spec.md`

#### Step 3: Create Implementation Plan

```
/speckit-enrich-plan
```

AI creates: `specs/NNN-feature-name/plan.md` (design, architecture, tasks)

#### Step 4: Execute Implementation

```
/speckit-enrich-implement
```

AI executes all tasks from `tasks.md`, updates lessons learned.

#### Step 5: Review Results

```
spek status
```

Shows:
- All tools initialized
- Skills available
- Recent operations
- Vault status

---

## Integration Points

### 1. Vault Integration

Spekificity stores decisions in `.obsidian/` vault:

```
.obsidian/
  ├─ graph/index.md          (codebase map from graphify)
  ├─ decisions.md            (architectural decisions)
  ├─ patterns.md             (design patterns discovered)
  ├─ lessons/
  │   └─ YYYY-MM-DD-feature.md  (lessons after each feature)
```

**Your action**: Regularly review vault to stay aligned with evolving architecture.

### 2. Speckit Integration

Spekificity wraps speckit for spec-first workflow:

```
specs/
  └─ NNN-feature-name/
      ├─ spec.md              (feature specification)
      ├─ plan.md              (implementation plan)
      ├─ tasks.md             (actionable tasks)
      ├─ data-model.md        (entities)
      ├─ contracts/           (API specs)
      └─ checklists/          (QA/UX/security checklists)
```

**Your action**: Commit specs to version control alongside code.

### 3. Graphify Integration

Graphify provides codebase analysis:

```
/spek.map-codebase
```

Updates graph with latest code relationships, used by:
- `/spek.context-load` (feeds AI with accurate context)
- Architecture decisions (guides new features)
- Component impact analysis

**Your action**: Run periodically (weekly or after major refactoring).

### 4. Caveman Integration (Optional)

If caveman skill available, use for token efficiency:

```
/caveman lite
```

Reduces AI response verbosity while maintaining clarity. Useful for:
- Long feature work (preserve token budget)
- Complex implementation discussions
- Iterative refinement

---

## Skill Usage Patterns

### Pattern 1: Daily Context Priming

**Before any feature work**:
```
1. /context-load           — AI loads vault context
2. [Your feature work]     — AI uses cached context
3. /spek.lessons-learnt    — Capture what you learned
```

### Pattern 2: Mid-Feature Decisions

**When stuck on design**:
```
1. /context-load                          — Load context
2. Review vault decisions                 — Understand existing patterns
3. /speckit-enrich-specify [updated]      — Refine spec with new clarity
```

### Pattern 3: End-of-Feature Documentation

**After feature implementation**:
```
1. /spek.lessons-learnt                   — Capture learning
2. /spek.map-codebase                     — Update codebase graph
3. spek status                            — Record final state
4. git commit && git push                 — Save to version control
```

---

## Team Collaboration

### Onboarding New Developer

```bash
# Existing project
git clone https://github.com/org/project.git
cd project

# Setup takes ~20 min (includes tool installs)
.spekificity/bin/spek setup

# Init takes ~2 min
.spekificity/bin/spek init

# Now ready for feature work
/context-load
```

### Shared Vault Strategy

```
Option 1: Vault in Git
  ✓ Pros: Team sees all decisions, lessons, patterns
  ✓ Cons: Merge conflicts possible (resolve manually)

Option 2: Vault in shared storage (optional)
  ✓ Pros: Centralized knowledge, no conflicts
  ✓ Cons: Requires external storage setup

Option 3: Fallback JSON storage
  ✓ Pros: No Obsidian app needed, works in CI/CD
  ✓ Cons: No visual graph UI (still available in markdown)
```

**Recommendation**: Check `spec.md` for guidance on your team's choice.

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Spekificity Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Check Spekificity Status
        run: |
          .spekificity/bin/spek status --json
      - name: Validate Specs
        run: |
          # If PR touches spec.md or plan.md, validate completeness
          if git diff HEAD~1 HEAD --name-only | grep -q "spec.md"; then
            echo "Spec changed — ensure linked to plan.md and tasks.md"
          fi
```

### Namespace Validation

```bash
# In your CI/CD:
.spekificity/setup-scripts/validate-namespace.sh --verbose
```

Ensures:
- All skills use correct namespace (`spek.*`, `speckit.*`)
- Config keys follow naming convention
- Documentation references are valid

---

## Troubleshooting Integration

### "Skills not showing up in my chat"

**Cause**: Skill index not updated

**Solution**:
```bash
spek init                    # Regenerates skill index
.spekificity/bin/spek status # Verify skills registered
```

### "Vault not syncing across team"

**Cause**: Different vault locations or fallback storage used

**Solution**:
Check `.spekificity/config.json`:
```json
{
  "tools": {
    "obsidian": {
      "vault_path": "/path/to/.obsidian"
    }
  }
}
```

Ensure all team members have same vault location, or use centralized storage.

### "Graph outdated"

**Cause**: Codebase changed, graph not updated

**Solution**:
```bash
/spek.map-codebase           # Updates graph
spek status                  # Shows last update timestamp
```

---

## Performance Tips

1. **Cache vault context**: Once loaded with `/context-load`, context persists in AI session. No need to reload unless codebase changed significantly.

2. **Batch graph updates**: Run `/spek.map-codebase` weekly or after major refactoring, not per-feature.

3. **Use caveman mode** for long feature work to preserve tokens.

4. **Prune old lessons**: Archive lessons older than 6 months to keep vault responsive.

---

## Workflow Example: Building a New API Endpoint

```bash
# 1. Setup (first time only)
.spekificity/bin/spek setup
.spekificity/bin/spek init

# 2. Load context
/context-load

# 3. Create feature spec
/speckit-enrich-specify
# → Creates specs/045-user-auth-api/spec.md

# 4. Plan implementation
/speckit-enrich-plan
# → Creates specs/045-user-auth-api/plan.md
# → Includes: tech stack, architecture, file structure

# 5. Execute tasks
/speckit-enrich-implement
# → Generates specs/045-user-auth-api/tasks.md
# → Executes all implementation tasks
# → Updates lessons

# 6. Save progress
/spek.lessons-learnt
git add -A && git commit -m "feat: user auth endpoint"

# 7. Check final state
spek status
```

---

**Ready to integrate spekificity into your workflow?** Start with `/context-load` and let the AI guide your feature development!
