---
description: generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: 
  - label: analyze for consistency
    agent: speckit.analyze
    prompt: run a project analysis for consistency
    send: true
  - label: implement project
    agent: speckit.implement
    prompt: start the implementation in phases
    send: true
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before tasks generation)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_tasks` key
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

1. **setup**: run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse feature_dir and available_docs list. all paths must be absolute. for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

2. **load design documents**: read from feature_dir:
   - **required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **optional**: data-model.md (entities), contracts/ (interface contracts), research.md (decisions), quickstart.md (test scenarios)
   - note: not all projects have all documents. generate tasks based on what's available.

3. **execute task generation workflow**:
   - load plan.md and extract tech stack, libraries, project structure
   - load spec.md and extract user stories with their priorities (p1, p2, p3, etc.)
   - if data-model.md exists: extract entities and map to user stories
   - if contracts/ exists: map interface contracts to user stories
   - if research.md exists: extract decisions for setup tasks
   - generate tasks organized by user story (see task generation rules below)
   - generate dependency graph showing user story completion order
   - create parallel execution examples per user story
   - validate task completeness (each user story has all needed tasks, independently testable)

4. **generate tasks.md**: use `.specify/templates/tasks-template.md` as structure, fill with:
   - correct feature name from plan.md
   - phase 1: setup tasks (project initialization)
   - phase 2: foundational tasks (blocking prerequisites for all user stories)
   - phase 3+: one phase per user story (in priority order from spec.md)
   - each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - final phase: polish & cross-cutting concerns
   - all tasks must follow the strict checklist format (see task generation rules below)
   - clear file paths for each task
   - dependencies section showing story completion order
   - parallel execution examples per story
   - implementation strategy section (mvp first, incremental delivery)

5. **report**: output path to generated tasks.md and summary:
   - total task count
   - task count per user story
   - parallel opportunities identified
   - independent test criteria for each story
   - suggested mvp scope (typically just user story 1)
   - format validation: confirm all tasks follow the checklist format (checkbox, id, labels, file paths)

6. **check for extension hooks**: after tasks.md is generated, check if `.specify/extensions.yml` exists in the project root.
   - if it exists, read it and look for entries under the `hooks.after_tasks` key
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

context for task generation: $arguments

the tasks.md should be immediately executable - each task must be specific enough that an llm can complete it without additional context.

## task generation rules

**critical**: tasks must be organized by user story to enable independent implementation and testing.

**tests are optional**: only generate test tasks if explicitly requested in the feature specification or if user requests tdd approach.

### checklist format (required)

every task must strictly follow this format:

```text
- [ ] [taskid] [p?] [story?] description with file path
```

**format components**:

1. **checkbox**: always start with `- [ ]` (markdown checkbox)
2. **task id**: sequential number (t001, t002, t003...) in execution order
3. **[p] marker**: include only if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[story] label**: required for user story phase tasks only
   - format: [us1], [us2], [us3], etc. (maps to user stories from spec.md)
   - setup phase: no story label
   - foundational phase: no story label  
   - user story phases: must have story label
   - polish phase: no story label
5. **description**: clear action with exact file path

**examples**:

- ✅ correct: `- [ ] t001 create project structure per implementation plan`
- ✅ correct: `- [ ] t005 [p] implement authentication middleware in src/middleware/auth.py`
- ✅ correct: `- [ ] t012 [p] [us1] create user model in src/models/user.py`
- ✅ correct: `- [ ] t014 [us1] implement userservice in src/services/user_service.py`
- ❌ wrong: `- [ ] create user model` (missing id and story label)
- ❌ wrong: `t001 [us1] create model` (missing checkbox)
- ❌ wrong: `- [ ] [us1] create user model` (missing task id)
- ❌ wrong: `- [ ] t001 [us1] create model` (missing file path)

### task organization

1. **from user stories (spec.md)** - primary organization:
   - each user story (p1, p2, p3...) gets its own phase
   - map all related components to their story:
     - models needed for that story
     - services needed for that story
     - interfaces/ui needed for that story
     - if tests requested: tests specific to that story
   - mark story dependencies (most stories should be independent)

2. **from contracts**:
   - map each interface contract → to the user story it serves
   - if tests requested: each interface contract → contract test task [p] before implementation in that story's phase

3. **from data model**:
   - map each entity to the user story(ies) that need it
   - if entity serves multiple stories: put in earliest story or setup phase
   - relationships → service layer tasks in appropriate story phase

4. **from setup/infrastructure**:
   - shared infrastructure → setup phase (phase 1)
   - foundational/blocking tasks → foundational phase (phase 2)
   - story-specific setup → within that story's phase

### phase structure

- **phase 1**: setup (project initialization)
- **phase 2**: foundational (blocking prerequisites - must complete before user stories)
- **phase 3+**: user stories in priority order (p1, p2, p3...)
  - within each story: tests (if requested) → models → services → endpoints → integration
  - each phase should be a complete, independently testable increment
- **final phase**: polish & cross-cutting concerns
