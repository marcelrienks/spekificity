---
description: perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before analysis)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_analyze` key
- if the yaml cannot be parsed or is invalid, skip hook checking silently and continue normally
- filter out hooks where `enabled` is explicitly `false`. treat hooks without an `enabled` field as enabled by default.
- for each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - if the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - if the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the hookexecutor implementation
- for each executable hook, output the following based on its `optional` flag:
  - **optional hook** (`optional: true`):
    ```
    ## extension hooks

    **optional pre-hook**: {extension}
    command: `/{command}`
    description: {description}

    prompt: {prompt}
    to execute: `/{command}`
    ```
  - **mandatory hook** (`optional: false`):
    ```
    ## extension hooks

    **automatic pre-hook**: {extension}
    executing: `/{command}`
    execute_command: {command}

    wait for the result of the hook command before proceeding to the goal.
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## goal

identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. this command must run only after `/speckit.tasks` has successfully produced a complete `tasks.md`.

## operating constraints

**strictly read-only**: do **not** modify any files. output a structured analysis report. offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**constitution authority**: the project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. constitution conflicts are automatically critical and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. if a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/speckit.analyze`.

## execution steps

### 1. initialize analysis context

run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` once from repo root and parse json for feature_dir and available_docs. derive absolute paths:

- spec = feature_dir/spec.md
- plan = feature_dir/plan.md
- tasks = feature_dir/tasks.md

abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

### 2. load artifacts (progressive disclosure)

load only the minimal necessary context from each artifact:

**from spec.md:**

- overview/context
- functional requirements
- success criteria (measurable outcomes — e.g., performance, security, availability, user success, business impact)
- user stories
- edge cases (if present)

**from plan.md:**

- architecture/stack choices
- data model references
- phases
- technical constraints

**from tasks.md:**

- task ids
- descriptions
- phase grouping
- parallel markers [p]
- referenced file paths

**from constitution:**

- load `.specify/memory/constitution.md` for principle validation

### 3. build semantic models

create internal representations (do not include raw artifacts in output):

- **requirements inventory**: for each functional requirement (fr-###) and success criterion (sc-###), record a stable key. use the explicit fr-/sc- identifier as the primary key when present, and optionally also derive an imperative-phrase slug for readability (e.g., "user can upload file" → `user-can-upload-file`). include only success criteria items that require buildable work (e.g., load-testing infrastructure, security audit tooling), and exclude post-launch outcome metrics and business kpis (e.g., "reduce support tickets by 50%").
- **user story/action inventory**: discrete user actions with acceptance criteria
- **task coverage mapping**: map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like ids or key phrases)
- **constitution rule set**: extract principle names and must/should normative statements

### 4. detection passes (token-efficient analysis)

focus on high-signal findings. limit to 50 findings total; aggregate remainder in overflow summary.

#### a. duplication detection

- identify near-duplicate requirements
- mark lower-quality phrasing for consolidation

#### b. ambiguity detection

- flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- flag unresolved placeholders (todo, tktk, ???, `<placeholder>`, etc.)

#### c. underspecification

- requirements with verbs but missing object or measurable outcome
- user stories missing acceptance criteria alignment
- tasks referencing files or components not defined in spec/plan

#### d. constitution alignment

- any requirement or plan element conflicting with a must principle
- missing mandated sections or quality gates from constitution

#### e. coverage gaps

- requirements with zero associated tasks
- tasks with no mapped requirement/story
- success criteria requiring buildable work (performance, security, availability) not reflected in tasks

#### f. inconsistency

- terminology drift (same concept named differently across files)
- data entities referenced in plan but absent in spec (or vice versa)
- task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- conflicting requirements (e.g., one requires next.js while other specifies vue)

### 5. severity assignment

use this heuristic to prioritize findings:

- **critical**: violates constitution must, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **high**: duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **medium**: terminology drift, missing non-functional task coverage, underspecified edge case
- **low**: style/wording improvements, minor redundancy not affecting execution order

### 6. produce compact analysis report

output a markdown report (no file writes) with the following structure:

## specification analysis report

| id | category | severity | location(s) | summary | recommendation |
|----|----------|----------|-------------|---------|----------------|
| a1 | duplication | high | spec.md:l120-134 | two similar requirements ... | merge phrasing; keep clearer version |

(add one row per finding; generate stable ids prefixed by category initial.)

**coverage summary table:**

| requirement key | has task? | task ids | notes |
|-----------------|-----------|----------|-------|

**constitution alignment issues:** (if any)

**unmapped tasks:** (if any)

**metrics:**

- total requirements
- total tasks
- coverage % (requirements with >=1 task)
- ambiguity count
- duplication count
- critical issues count

### 7. provide next actions

at end of report, output a concise next actions block:

- if critical issues exist: recommend resolving before `/speckit.implement`
- if only low/medium: user may proceed, but provide improvement suggestions
- provide explicit command suggestions: e.g., "run /speckit.specify with refinement", "run /speckit.plan to adjust architecture", "manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. offer remediation

ask the user: "would you like me to suggest concrete remediation edits for the top n issues?" (do not apply them automatically.)

### 9. check for extension hooks

after reporting, check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.after_analyze` key
- if the yaml cannot be parsed or is invalid, skip hook checking silently and continue normally
- filter out hooks where `enabled` is explicitly `false`. treat hooks without an `enabled` field as enabled by default.
- for each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - if the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - if the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the hookexecutor implementation
- for each executable hook, output the following based on its `optional` flag:
  - **optional hook** (`optional: true`):
    ```
    ## extension hooks

    **optional hook**: {extension}
    command: `/{command}`
    description: {description}

    prompt: {prompt}
    to execute: `/{command}`
    ```
  - **mandatory hook** (`optional: false`):
    ```
    ## extension hooks

    **automatic hook**: {extension}
    executing: `/{command}`
    execute_command: {command}
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## operating principles

### context efficiency

- **minimal high-signal tokens**: focus on actionable findings, not exhaustive documentation
- **progressive disclosure**: load artifacts incrementally; don't dump all content into analysis
- **token-efficient output**: limit findings table to 50 rows; summarize overflow
- **deterministic results**: rerunning without changes should produce consistent ids and counts

### analysis guidelines

- **never modify files** (this is read-only analysis)
- **never hallucinate missing sections** (if absent, report them accurately)
- **prioritize constitution violations** (these are always critical)
- **use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **report zero issues gracefully** (emit success report with coverage statistics)

## context

$arguments
