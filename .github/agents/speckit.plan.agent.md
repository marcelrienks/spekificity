---
description: execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: create tasks
    agent: speckit.tasks
    prompt: break the plan into tasks
    send: true
  - label: create checklist
    agent: speckit.checklist
    prompt: create a checklist for the following domain...
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before planning)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_plan` key
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

1. **setup**: run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse json for feature_spec, impl_plan, specs_dir, branch. for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

2. **load context**: read feature_spec and `.specify/memory/constitution.md`. load impl_plan template (already copied).

3. **execute plan workflow**: follow the structure in impl_plan template to:
   - fill technical context (mark unknowns as "needs clarification")
   - fill constitution check section from constitution
   - evaluate gates (error if violations unjustified)
   - phase 0: generate research.md (resolve all needs clarification)
   - phase 1: generate data-model.md, contracts/, quickstart.md
   - phase 1: update agent context by running the agent script
   - re-evaluate constitution check post-design

4. **stop and report**: command ends after phase 2 planning. report branch, impl_plan path, and generated artifacts.

5. **check for extension hooks**: after reporting, check if `.specify/extensions.yml` exists in the project root.
   - if it exists, read it and look for entries under the `hooks.after_plan` key
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

## phases

### phase 0: outline & research

1. **extract unknowns from technical context** above:
   - for each needs clarification → research task
   - for each dependency → best practices task
   - for each integration → patterns task

2. **generate and dispatch research agents**:

   ```text
   for each unknown in technical context:
     task: "research {unknown} for {feature context}"
   for each technology choice:
     task: "find best practices for {tech} in {domain}"
   ```

3. **consolidate findings** in `research.md` using format:
   - decision: [what was chosen]
   - rationale: [why chosen]
   - alternatives considered: [what else evaluated]

**output**: research.md with all needs clarification resolved

### phase 1: design & contracts

**prerequisites:** `research.md` complete

1. **extract entities from feature spec** → `data-model.md`:
   - entity name, fields, relationships
   - validation rules from requirements
   - state transitions if applicable

2. **define interface contracts** (if project has external interfaces) → `/contracts/`:
   - identify what interfaces the project exposes to users or other systems
   - document the contract format appropriate for the project type
   - examples: public apis for libraries, command schemas for cli tools, endpoints for web services, grammars for parsers, ui contracts for applications
   - skip if project is purely internal (build scripts, one-off tools, etc.)

3. **agent context update**:
   - update the plan reference between the `<!-- speckit start -->` and `<!-- speckit end -->` markers in `.github/copilot-instructions.md` to point to the plan file created in step 1 (the impl_plan path)

**output**: data-model.md, /contracts/*, quickstart.md, updated agent context file

## key rules

- use absolute paths for filesystem operations; use project-relative paths for references in documentation and agent context files
- error on gate failures or unresolved clarifications
