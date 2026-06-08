# Data Model: Spekificity Framework Entities

**Version:** 1.0  
**Created:** 2026-06-08  
**Feature:** Complete Spekificity Framework CLI Implementation (spec 001)

---

## Overview

Spekificity operates on 7 core entities, modeled as Pydantic v2 classes in `spekificity/core/types.py`. All entities are serializable to/from JSON and Markdown (via YAML frontmatter).

---

## Core Entities

### 1. Specification (Spec)

Formal definition of a feature, derived from user intent.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `spec-{branch}` or `spec-{date}-{name}` |
| `title` | str | Yes | Feature name |
| `description` | str | Yes | 1-2 sentence summary |
| `branch` | str | Yes | Git branch name where spec was created |
| `created` | datetime | Yes | Spec creation timestamp (ISO 8601) |
| `user_stories` | List[UserStory] | Yes | 1+ user story with priority, scenarios, acceptance criteria |
| `requirements` | List[Requirement] | Yes | Functional (FR) and non-functional requirements |
| `entities` | List[Entity] | No | Domain entities if data-focused feature |
| `success_criteria` | List[SuccessCriteria] | Yes | Measurable outcomes (SC-001, SC-002, etc.) |
| `assumptions` | List[Assumption] | Yes | Documented assumptions (Assumption-1, etc.) |
| `approved_by` | str | No | Person/agent who approved spec (optional for MVP) |
| `approved_at` | datetime | No | Approval timestamp (optional for MVP) |

**Validation Rules:**
- Title: 5-100 characters
- At least 1 user story
- At least 3 functional requirements
- At least 2 success criteria
- All success criteria must be measurable (contain: metric, threshold, time window)
- No requirement may be vague (checked against ["TBD", "TK", "TBA", "TBC"] list)
- All requirements must be traceable to user stories

**Serialization:** Markdown with YAML frontmatter (spec.md)

---

### 2. Implementation Plan (Plan)

High-level architecture and sequencing for a feature.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `plan-{spec_id}` |
| `spec_id` | str | Yes | Reference to parent Spec |
| `architecture` | str | Yes | Architecture overview (prose, no code) |
| `architecture_diagram` | str | No | Mermaid or ASCII diagram (optional) |
| `tech_stack` | List[str] | Yes | Technologies, frameworks, libraries |
| `tech_rationale` | str | Yes | Why these tech choices were made |
| `sequencing` | str | Yes | Dependency graph and critical path |
| `risks` | List[Risk] | Yes | Risks, probabilities, mitigations |
| `created_at` | datetime | Yes | Plan creation timestamp |
| `tasks_count` | int | Yes | Total number of tasks (from tasks.md) |
| `estimated_tokens` | int | Yes | Estimated total tokens for implementation |
| `estimated_hours` | float | Yes | Estimated total engineering hours |

**Related Entity: Risk**
| Field | Type | Notes |
|-------|------|-------|
| `risk` | str | Risk description (3-5 words) |
| `probability` | str | High / Medium / Low |
| `impact` | str | High / Medium / Low |
| `mitigation` | str | How to mitigate (action verb + approach) |

**Validation Rules:**
- Architecture: must be prose/concept only (no code, no function signatures)
- Tech stack: 1-5 items, each with clear justification
- Risks: at least 2 identified
- Estimated hours and tokens must be positive integers
- No circular dependencies in sequencing

**Serialization:** Markdown with YAML frontmatter (plan.md)

---

### 3. Task

A single, independently testable unit of work.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `T{phase}.{num}` (e.g., T1.1, T2.3) |
| `title` | str | Yes | Task name (5-50 chars) |
| `description` | str | Yes | What to build / test / document |
| `priority` | str | Yes | P0 (blocker) / P1 (required) / P2 (nice-to-have) |
| `dependencies` | List[str] | Yes | Task IDs this depends on (empty list if none) |
| `success_criteria` | List[str] | Yes | How to verify task is complete |
| `estimated_tokens` | int | Yes | Estimated tokens to complete |
| `estimated_hours` | float | Yes | Estimated hours to complete |
| `owner` | str | No | Person assigned (optional) |
| `status` | str | No | Not Started / In Progress / Complete / Blocked |
| `branch_from` | str | No | Which task/branch this branches from |

**Validation Rules:**
- Task must be independent (no circular dependencies)
- Success criteria must be verifiable (testable, measurable)
- Dependencies must reference existing tasks or be empty
- Estimated hours: 0.5-8 hours (tasks >8h should be split)
- Priority must be P0, P1, or P2

**Serialization:** Markdown list in tasks.md; can be converted to GitHub issues via /speckit-taskstoissues

---

### 4. Decision

An architectural, design, or technical choice made during planning or implementation.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `dec-{yyy}{mm}{dd}-{seq}` (e.g., dec-20260607-001) |
| `title` | str | Yes | Short decision name (5-50 chars) |
| `status` | str | Yes | proposed / approved / superseded / rejected |
| `date` | datetime | Yes | Decision timestamp |
| `author` | str | Yes | Who made decision |
| `decision` | str | Yes | What decision was made (1-2 sentences) |
| `rationale` | str | Yes | Why this decision (pros and cons) |
| `implications` | List[str] | Yes | Short-term and long-term impacts |
| `alternatives` | List[str] | Yes | What else was considered and why rejected |
| `related_tasks` | List[str] | No | Task IDs that implement this decision |

**Validation Rules:**
- Decision must be time-bound (date required)
- Rationale must explain at least 2 pros and 2 cons
- Status must be one of: proposed, approved, superseded, rejected
- At least 1 alternative must be documented

**Serialization:** YAML frontmatter in vault/decisions.md (append-only log)

---

### 5. Pattern

A reusable solution, convention, or best practice.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `pat-{category}-{seq}` (e.g., pat-api-001) |
| `title` | str | Yes | Pattern name (5-50 chars) |
| `category` | str | Yes | API / CLI / Testing / Database / Other |
| `description` | str | Yes | What problem does this solve? |
| `solution` | str | Yes | How to apply pattern (not code, concepts) |
| `example_file` | str | No | Path to example in codebase (e.g., `src/api/handler.py`) |
| `when_to_use` | str | Yes | Contexts where this pattern applies |
| `when_not_to_use` | str | Yes | Contexts where pattern doesn't fit |
| `related_patterns` | List[str] | No | IDs of complementary patterns |
| `created_at` | datetime | Yes | When pattern was first documented |
| `refined_by` | List[str] | No | Task IDs that refined this pattern |

**Validation Rules:**
- Category must match predefined list (API, CLI, Testing, Database, Other)
- Solution must be explained in prose/concepts (no code)
- Both "when to use" and "when not to use" required (balance important)
- Pattern must have been used successfully at least once

**Serialization:** YAML frontmatter in vault/patterns.md (append-only log)

---

### 6. Lesson

Insights and learnings extracted from a completed feature.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | str | Yes | Format: `les-{date}-{feature}` (auto-generated by vault) |
| `feature` | str | Yes | Feature branch or spec ID (e.g., `001-complete-framework`) |
| `date` | datetime | Yes | When lesson was extracted |
| `author` | str | Yes | Who documented lesson |
| `outcomes` | str | Yes | What was actually built vs planned |
| `lessons_learned` | List[str] | Yes | 2-5 key learnings from implementation |
| `new_patterns` | List[str] | No | New patterns identified |
| `refined_decisions` | List[str] | No | Decisions that should be revised |
| `recommendations` | List[str] | No | Recommendations for future features |
| `metrics` | dict | No | Actual metrics (tokens used, hours spent, etc.) |

**Validation Rules:**
- Feature must be a valid spec/branch ID
- At least 2 lessons must be documented
- Outcomes must mention specific accomplishments and misses
- Learnings must be actionable (not just "learned a lot")

**Serialization:** Individual Markdown files in vault/lessons/ (timestamped); can also be indexed in vault/lessons.md

---

### 7. TaskContext

Runtime context injected into an agent during task execution.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `task_id` | str | Yes | Which task this context is for |
| `task_description` | str | Yes | What the task is asking to do |
| `relevant_code` | List[CodeSnippet] | Yes | Code files/functions to read/modify |
| `relevant_decisions` | List[Decision] | No | Prior decisions affecting this task |
| `relevant_patterns` | List[Pattern] | No | Patterns to follow or apply |
| `prior_lessons` | List[Lesson] | No | Lessons from similar work |
| `estimated_tokens` | int | Yes | Expected context size (tokens) |
| `compressed_mode` | bool | No | Whether to compress output (Caveman mode) |
| `created_at` | datetime | Yes | Context creation timestamp |

**Related Entity: CodeSnippet**
| Field | Type | Notes |
|-------|------|-------|
| `file_path` | str | Absolute or repo-relative path |
| `function_name` | str | Function/method name (optional) |
| `lines` | tuple(int, int) | Start and end line numbers |
| `relevance` | str | High / Medium / Low |
| `description` | str | Why this code is relevant |

**Serialization:** JSON for internal use; can be formatted as Markdown for agent consumption

---

## Validation Schema

All entities validate against Pydantic v2 models in `spekificity/core/types.py`.

**Common Validations:**
- All timestamps are ISO 8601 (datetime objects)
- All IDs are non-empty strings (alphanumeric, hyphens, underscores only)
- All lists are non-empty unless marked Optional
- All descriptions are 10-1000 characters (trimmed, no trailing whitespace)

**Custom Validators:**
- Spec: all requirements traceable to stories
- Plan: architecture is prose-only (no code snippets)
- Task: dependencies are acyclic (no circular deps)
- Decision: rationale lists pros and cons
- Pattern: category is in predefined set

---

## Relationships

```
Spec (1) ──→ (1) Plan
           └──→ (N) Task
           └──→ (N) UserStory
           └──→ (N) Requirement
           └──→ (N) SuccessCriteria

Plan ──→ (N) Task
Task ──→ (N) SuccessCriteria
Task ──→ (N) RelatedDecisions

Decision ◄── vault/decisions.md (append-only log)
Pattern ◄── vault/patterns.md (append-only log)
Lesson ◄── vault/lessons/ (timestamped files)

TaskContext ──→ (N) CodeSnippet
             ──→ (N) Decision (loaded from vault)
             ──→ (N) Pattern (loaded from vault)
             ──→ (N) Lesson (loaded from vault)
```

---

## Serialization Formats

| Entity | Format | Location | Notes |
|--------|--------|----------|-------|
| Spec | Markdown + YAML | spec.md | Generated by SpecKit |
| Plan | Markdown + YAML | plan.md | Generated by SpecKit |
| Task | Markdown list | tasks.md | Generated by SpecKit |
| Decision | YAML frontmatter | vault/decisions.md | Append-only |
| Pattern | YAML frontmatter | vault/patterns.md | Append-only |
| Lesson | Markdown + YAML | vault/lessons/{date}-{feature}.md | Individual files |
| TaskContext | JSON (internal) | .specify/logs/{task_id}.log | Runtime only |

---

## Example: Complete Spec + Plan + Task

**spec.md excerpt:**
```yaml
---
id: spec-001-complete-framework
title: Complete Spekificity Framework
branch: 001-complete-framework
created: 2026-06-07
---

# Feature Specification: Complete Spekificity Framework

## User Story 1: Onboard to Feature & Load Prior Context (Priority: P1)

A developer starts work on a new feature. They run `/spek.prepare`...

## Requirements

### FR-001: Installation
Spekificity MUST be installable via `uv tool install`

### FR-002: Per-Project Initialization
`spek init` MUST initialize the `.specify/` folder structure

...

## Success Criteria

- SC-001: Users can install and initialize in under 5 minutes
- SC-002: /spek.prepare completes in under 30 seconds
```

**plan.md excerpt:**
```yaml
---
id: plan-001-complete-framework
spec_id: spec-001-complete-framework
---

# Implementation Plan

## Architecture Overview

Spekificity consists of 5 components:
1. Installation & dependency resolution
2. Vault engine for persistent knowledge
3. Code indexing via lat.md
4. SpecKit orchestration wrapper
5. Agent skills for workflow automation

## Tech Stack

- Python 3.11+
- SpecKit v0.9.6+
- lat.md (latest)
- Pydantic v2 (type contracts)
- GitPython 3.1.0+ (git operations)
```

**tasks.md excerpt:**
```markdown
## Task List

### Phase 1: Core Infrastructure

- **T1.1**: Set up Python package structure, pyproject.toml
- **T1.2**: Implement `spek --version` and `spek --help` commands
- **T1.3**: Implement dependency verification (Python 3.11+, git, uv)
  - Dependencies: none
  - Success Criteria: `spek init` reports all missing dependencies with installation links
  - Estimated Hours: 1.5
  - Estimated Tokens: 2000
```

---

**Data model complete. Ready for Phase 1 implementation.**
