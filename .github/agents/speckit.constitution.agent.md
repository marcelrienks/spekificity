---
description: create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: build specification
    agent: speckit.specify
    prompt: implement the feature specification based on the updated constitution. i want to build...
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before constitution update)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_constitution` key
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

    wait for the result of the hook command before proceeding to the outline.
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## outline

you are updating the project constitution at `.specify/memory/constitution.md`. this file is a template containing placeholder tokens in square brackets (e.g. `[project_name]`, `[principle_1_name]`). your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

**note**: if `.specify/memory/constitution.md` does not exist yet, it should have been initialized from `.specify/templates/constitution-template.md` during project setup. if it's missing, copy the template first.

follow this execution flow:

1. load the existing constitution at `.specify/memory/constitution.md`.
   - identify every placeholder token of the form `[all_caps_identifier]`.
   **important**: the user might require less or more principles than the ones used in the template. if a number is specified, respect that - follow the general template. you will update the doc accordingly.

2. collect/derive values for placeholders:
   - if user input (conversation) supplies a value, use it.
   - otherwise infer from existing repo context (readme, docs, prior constitution versions if embedded).
   - for governance dates: `ratification_date` is the original adoption date (if unknown ask or mark todo), `last_amended_date` is today if changes are made, otherwise keep previous.
   - `constitution_version` must increment according to semantic versioning rules:
     - major: backward incompatible governance/principle removals or redefinitions.
     - minor: new principle/section added or materially expanded guidance.
     - patch: clarifications, wording, typo fixes, non-semantic refinements.
   - if version bump type ambiguous, propose reasoning before finalizing.

3. draft the updated constitution content:
   - replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - ensure each principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - ensure governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. consistency propagation checklist (convert prior checklist into active validations):
   - read `.specify/templates/plan-template.md` and ensure any "constitution check" or rules align with updated principles.
   - read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like claude only) remain when generic guidance is required.
   - read any runtime guidance docs (e.g., `readme.md`, `docs/quickstart.md`, or agent-specific guidance files if present). update references to principles changed.

5. produce a sync impact report (prepend as an html comment at top of the constitution file after update):
   - version change: old → new
   - list of modified principles (old title → new title if renamed)
   - added sections
   - removed sections
   - templates requiring updates (✅ updated / ⚠ pending) with file paths
   - follow-up todos if any placeholders intentionally deferred.

6. validation before final output:
   - no remaining unexplained bracket tokens.
   - version line matches report.
   - dates iso format yyyy-mm-dd.
   - principles are declarative, testable, and free of vague language ("should" → replace with must/should rationale where appropriate).

7. write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. output a final summary to the user with:
   - new version and bump rationale.
   - any files flagged for manual follow-up.
   - suggested commit message (e.g., `docs: amend constitution to vx.y.z (principle additions + governance update)`).

formatting & style requirements:

- use markdown headings exactly as in the template (do not demote/promote levels).
- wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- keep a single blank line between sections.
- avoid trailing whitespace.

if the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

if critical info missing (e.g., ratification date truly unknown), insert `todo(<field_name>): explanation` and include in the sync impact report under deferred items.

do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

## post-execution checks

**check for extension hooks (after constitution update)**:
check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.after_constitution` key
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
