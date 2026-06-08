<!-- SPECKIT START -->

# Spekificity Framework Skills

**4-Stage Feature Development Workflow:**

## 1. `/spek.prepare [FEATURE]` — Load Context
Load vault decisions, patterns, lessons. Index codebase. Generate navigation guide.
- **When:** Start work on new feature
- **Input:** Feature name/description (optional)
- **Output:** Context summary + relevant code files
- **Time:** <30 seconds
- See: [.github/agents/skills/spek-prepare/](.github/agents/skills/spek-prepare/)

## 2. `/spek.plan "FEATURE_DESCRIPTION"` — Generate Spec & Plan
Generate formal specification, identify ambiguities, create implementation plan with tasks.
- **When:** After prepare, ready to define scope
- **Input:** Feature description (10+ words, required)
- **Output:** spec.md, plan.md, tasks.md in `specs/{feature-slug}/`
- **Time:** <3 minutes
- **Requires:** SpecKit v0.9.6+ installed
- See: [.github/agents/skills/spek-plan/](.github/agents/skills/spek-plan/)

## 3. `/spek.implement --task TASK_ID [--mark-complete]` — Execute Task
Inject context (decisions, patterns, code), execute task, log progress & decisions.
- **When:** Ready to code specific task
- **Input:** Task ID from tasks.md (e.g., T1.1, T2.3)
- **Output:** Progress log, context injection, completion tracking
- **Time:** Varies (per-task)
- See: [.github/agents/skills/spek-implement/](.github/agents/skills/spek-implement/)

## 4. `/spek.conclude --feature FEATURE_NAME` — Extract Lessons
Analyze outcomes, extract lessons, update vault with new patterns & decisions.
- **When:** All feature tasks complete
- **Input:** Feature name (required)
- **Output:** Lessons file, updated vault, feature summary
- **Time:** <5 minutes
- See: [.github/agents/skills/spek-conclude/](.github/agents/skills/spek-conclude/)

---

## Quick Start Example

```bash
# 1. Prepare context
/spek.prepare "OAuth2 authentication"

# 2. Plan feature (generates spec.md, plan.md, tasks.md)
/spek.plan "Add OAuth2 support with Google and GitHub providers"

# 3. Implement tasks sequentially
/spek.implement --task T1.1
# [agent/developer implements]
/spek.implement --task T1.1 --mark-complete

/spek.implement --task T1.2
# [implement]
/spek.implement --task T1.2 --mark-complete

# 4. Conclude feature (extract lessons, update vault)
/spek.conclude --feature oauth2-auth
```

---

## Architecture & Planning

For comprehensive implementation plan, phases, and task sequencing:
- **Feature Spec:** [specs/001-complete-framework/spec.md](../../specs/001-complete-framework/spec.md)
- **Implementation Plan:** [specs/001-complete-framework/plan.md](../../specs/001-complete-framework/plan.md)
- **Task List:** [specs/001-complete-framework/tasks.md](../../specs/001-complete-framework/tasks.md)

For project architecture and design decisions:
- **Architecture:** [wiki/architecture.md](../../wiki/architecture.md)
- **Decisions:** [wiki/decision.md](../../wiki/decision.md)
- **Constitution:** [.specify/memory/constitution.md](.specify/memory/constitution.md)

<!-- SPECKIT END -->
