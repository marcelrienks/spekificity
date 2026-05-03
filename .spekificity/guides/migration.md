# Migration Guide: Adopting Spekificity in Existing Projects

**Purpose**: How to transition existing projects to use spekificity platform.

## Eligibility Check

Before migrating, verify your project:

- [ ] Git repository initialized
- [ ] Python 3.11+ available
- [ ] Team familiar with speckit workflow (or willing to learn)
- [ ] Codebase documented (README, contributing guide)

**Recommendation**: Review docs before starting migration.

---

## Migration Paths

### Path 1: Fresh Start (Recommended)

**For**: New projects or projects without existing specs

```bash
# 1. Create project directory
mkdir my-new-project
cd my-new-project

# 2. Initialize git
git init
git branch -m main

# 3. Run spekificity setup
.spekificity/bin/spek setup
.spekificity/bin/spek init

# 4. Start your first feature
/context-load
/speckit-enrich-specify
```

**Time**: ~25 minutes  
**Effort**: Minimal  
**Result**: Full spekificity workflow ready

---

### Path 2: Existing Project with Specs

**For**: Projects already using speckit workflow

```bash
# 1. Copy spekificity layer
cp -r /reference/project/.spekificity ./my-project/

# 2. Verify speckit already initialized
.specify/
.github/agents/
# If missing, run: specify init .

# 3. Update spekificity config
.spekificity/bin/spek setup
.spekificity/bin/spek init

# 4. Validate namespace consistency
.spekificity/setup-scripts/validate-namespace.sh

# 5. Update skill index
.spekificity/setup-scripts/skill-discovery.sh generate_skill_index

# 6. Test workflow
/context-load
spek status
```

**Time**: ~15 minutes  
**Effort**: Low  
**Result**: Spekificity layer added on top of existing speckit

---

### Path 3: Legacy Project (No Specs)

**For**: Projects without any spec-driven workflow

#### Phase 1: Onboard to Speckit (4 hours)

```bash
# 1. Setup spekificity
.spekificity/bin/spek setup
.spekificity/bin/spek init

# 2. Read speckit documentation
.spekificity/guides/
.github/workflows/feature-lifecycle.md

# 3. Create initial constitution
/speckit.constitution
# → Define team principles, tech stack, coding standards

# 4. Document existing architecture
# Create: specs/000-legacy-codebase/spec.md
# Document: Current structure, tech stack, dependencies
```

#### Phase 2: Start New Features with Specs (2-3 hours per feature)

```bash
# For each new feature:
/context-load
/speckit-enrich-specify          # Create spec
/speckit-enrich-plan             # Create plan
/speckit-enrich-implement        # Execute tasks
/spek.lessons-learnt             # Capture learning
```

#### Phase 3: Refactor Legacy Code (Optional, ongoing)

```bash
# Gradually refactor legacy code following new patterns
# Each refactoring is a feature:
/speckit-enrich-specify "Refactor user auth module"
# → plan → implement → lessons

# Over time: Legacy code evolves toward new standards
```

**Time**: ~1 week to full adoption  
**Effort**: Medium  
**Result**: New features spec-driven; legacy code refactored incrementally

---

## Data Migration

### Migrating Existing Documentation

If you have existing documentation not in speckit format:

```bash
# 1. Identify existing docs
ls -la docs/
ls -la README.md
ls -la architecture/

# 2. Map to spec structure
README.md               → specs/000-legacy-codebase/spec.md
docs/architecture.md   → specs/000-legacy-codebase/data-model.md
docs/api.md            → specs/000-legacy-codebase/contracts/

# 3. Create spec file
# File: specs/000-legacy-codebase/spec.md
# Content: Paste existing docs into spec structure
# Add: Links to legacy codebase, migrating to new patterns

# 4. Commit
git add specs/
git commit -m "docs: legacy codebase spec"
```

### Migrating Existing Git History

**No action needed**: Spekificity works alongside existing git history.

```bash
# Existing repo structure remains unchanged:
src/
tests/
docs/
README.md

# Spekificity adds new structure:
.spekificity/          (new)
specs/                 (new)
.specify/              (new if not exists)
.github/agents/        (new if not exists)
```

---

## Team Onboarding

### For Product Managers

```
1. Learn speckit spec format
   → Read: specs/002-spek-platform-lifecycle/spec.md

2. Write first spec
   → Use: /speckit.specify [feature description]
   → Review output: specs/NNN-feature/spec.md

3. Review team specs
   → Ensure: All features have clear requirements
   → Check: Acceptance criteria included
```

### For Engineers

```
1. Learn spekificity commands
   → Run: spek setup && spek init
   → Explore: .spekificity/guides/

2. Use workflow for first feature
   → /context-load
   → /speckit-enrich-plan
   → /speckit-enrich-implement
   → /spek.lessons-learnt

3. Provide feedback
   → What worked?
   → What was confusing?
   → Improvements?
```

### For Architects

```
1. Review platform design
   → Read: .spekificity/guides/architecture.md

2. Define team constitution
   → Run: /speckit.constitution
   → Answer: Tech stack, patterns, principles

3. Monitor graph evolution
   → Run: /spek.map-codebase
   → Review: .obsidian/graph/index.md
   → Adjust: Architecture as needed
```

---

## Rollback Plan

If migration goes wrong:

```bash
# Option 1: Remove spekificity (keep speckit)
rm -rf .spekificity/

# Option 2: Full rollback to pre-migration
git reset --hard HEAD~N   # Where N = commits since migration start
git clean -fd             # Remove untracked files

# Option 3: Partial rollback (keep some changes)
git checkout <commit-hash> -- <file-path>
```

**Before migration**: Tag current commit
```bash
git tag pre-spekificity-migration
```

Then rollback if needed:
```bash
git reset --hard pre-spekificity-migration
```

---

## Migration Checklist

- [ ] **Prerequisites**: Python 3.11+, uv, git installed
- [ ] **Backup**: Current codebase backed up or on feature branch
- [ ] **Planning**: Team understands spekificity value (read docs first)
- [ ] **Setup**: `spek setup && spek init` successful
- [ ] **Validation**: `spek status` shows all tools initialized
- [ ] **Test**: `/context-load` works without errors
- [ ] **Documentation**: Team trained on new workflow
- [ ] **Pilot**: First feature completed with new workflow
- [ ] **Review**: Team feedback collected and addressed
- [ ] **Commit**: Changes committed to version control
- [ ] **Communicate**: Team notified of new workflow availability

---

## Common Migration Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `specify: command not found` | speckit not installed | Run `uv tool install specify-cli --from git+...` |
| `Config validation failed` | Old schema version | Delete config, re-run `spek init` |
| `Permission denied` on scripts | Scripts not executable | `chmod +x .spekificity/setup-scripts/*.sh` |
| Team confused by workflow | Insufficient training | Schedule workshop, pair with experienced team member |
| Graph generation takes too long | Large codebase | Run graphify incrementally or with depth limits |

---

## Success Metrics

After migration, track:

- **Time to spec**: How long to create feature spec?
- **Plan accuracy**: How many plan tasks completed as estimated?
- **Feature velocity**: How many features per sprint?
- **Bug escape rate**: How many bugs reach production (lower = better)?
- **Code review efficiency**: How long for review (should decrease with clear specs)?
- **Documentation coverage**: Are new features documented? (target: 100%)

---

## Post-Migration Support

**Need help?**

1. **Check**: `.spekificity/guides/troubleshooting.md`
2. **Review**: `.spekificity/guides/architecture.md`
3. **Test**: `spek status --json` for detailed state
4. **Validate**: `.spekificity/setup-scripts/validate-namespace.sh`

**Team questions?**

- Technical: Review `.spekificity/guides/`
- Workflow: See `.spekificity/workflows/feature-lifecycle.md`
- Troubleshooting: See `.spekificity/guides/troubleshooting.md`

---

**Ready to migrate?** Start with Path 1 or 2 (depends on your current state), run the checklist, and welcome to spekificity!
