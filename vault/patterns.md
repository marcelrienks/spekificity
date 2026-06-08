---
title: Design Patterns & Conventions
description: Reusable patterns, conventions, and best practices
created: "2026-06-07"
version: "1.0"
---

# Design Patterns & Conventions

Repository of reusable patterns, conventions, and best practices discovered during feature development.

Each pattern follows this format:

## Pattern Template

```yaml
---
id: pat-NNN
title: [Pattern Name]
category: [Architecture|Workflow|Testing|Integration|UI|API]
created: YYYY-MM-DD
author: [Name]
status: [approved|draft|deprecated]
---

## Problem

[What problem does this pattern solve?]

## Solution

[Description of the pattern]

## Example

[Code or workflow example]

## When to Use

[Situations where this pattern applies]

## When NOT to Use

[Situations where this pattern doesn't apply]

## Related Patterns

[Links to related patterns]
```

## Pattern 1: Spec-Driven Feature Development

---
id: pat-001
title: Spec-Driven Feature Development
category: Workflow
created: 2026-06-07
author: architect
status: approved
---

### Problem

Features often lack clear specifications, leading to scope creep, ambiguity, and rework.

### Solution

Always start with a written specification (spec.md) that defines:
- User scenarios and acceptance criteria
- Success measures (testable and quantified)
- Key entities and relationships
- Assumptions and constraints
- Edge cases and failure modes

### Example

```bash
# Feature specification workflow
spek prepare FEATURE_NAME          # Load context
spek plan "Feature description"    # Generate spec.md
# Review and approve spec.md
spek implement TASK_ID             # Execute tasks
spek conclude FEATURE_NAME         # Extract lessons
```

### When to Use

All new features, significant refactors, architectural changes.

### When NOT to Use

Trivial bug fixes or documentation updates may skip full spec process.

### Related Patterns

- [Decision-Driven Architecture (dec-001)](#decision-1-use-speckit-for-spec-driven-workflows)
- Knowledge Vault Updates (pat-002)

## Pattern 2: Knowledge Vault Updates

---
id: pat-002
title: Knowledge Vault Updates
category: Workflow
created: 2026-06-07
author: architect
status: approved
---

### Problem

Architectural knowledge and design decisions are lost or scattered across code comments and docs.

### Solution

Maintain a persistent vault (decisions.md, patterns.md, lessons/) that captures:
- Architectural decisions with rationale
- Reusable patterns and conventions
- Lessons learned from completed features

Update vault during `/spek.conclude` phase.

### Example

```markdown
# In decisions.md:
- ID: dec-NNN
- Title: Choose X over Y because...
- Date: YYYY-MM-DD
- Implications: Affects modules A and B
```

### When to Use

Every completed feature; every significant architectural decision.

### When NOT to Use

Temporary decisions or experiments (mark as "draft" or "proposed" instead).

### Related Patterns

- [Spec-Driven Feature Development (pat-001)](#pattern-1-spec-driven-feature-development)
