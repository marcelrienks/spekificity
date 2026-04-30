---
description: execute the implementation plan by processing and executing all tasks defined in tasks.md
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before implementation)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_implement` key
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

1. run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse feature_dir and available_docs list. all paths must be absolute. for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

2. **check checklists status** (if feature_dir/checklists/ exists):
   - scan all checklist files in the checklists/ directory
   - for each checklist, count:
     - total items: all lines matching `- [ ]` or `- [x]` or `- [x]`
     - completed items: lines matching `- [x]` or `- [x]`
     - incomplete items: lines matching `- [ ]`
   - create a status table:

     ```text
     | checklist | total | completed | incomplete | status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ pass |
     | test.md   | 8     | 5         | 3          | ✗ fail |
     | security.md | 6   | 6         | 0          | ✓ pass |
     ```

   - calculate overall status:
     - **pass**: all checklists have 0 incomplete items
     - **fail**: one or more checklists have incomplete items

   - **if any checklist is incomplete**:
     - display the table with incomplete item counts
     - **stop** and ask: "some checklists are incomplete. do you want to proceed with implementation anyway? (yes/no)"
     - wait for user response before continuing
     - if user says "no" or "wait" or "stop", halt execution
     - if user says "yes" or "proceed" or "continue", proceed to step 3

   - **if all checklists are complete**:
     - display the table showing all checklists passed
     - automatically proceed to step 3

3. load and analyze the implementation context:
   - **required**: read tasks.md for the complete task list and execution plan
   - **required**: read plan.md for tech stack, architecture, and file structure
   - **if exists**: read data-model.md for entities and relationships
   - **if exists**: read contracts/ for api specifications and test requirements
   - **if exists**: read research.md for technical decisions and constraints
   - **if exists**: read quickstart.md for integration scenarios

4. **project setup verification**:
   - **required**: create/verify ignore files based on actual project setup:

   **detection & creation logic**:
   - check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - check if dockerfile* exists or docker in plan.md → create/verify .dockerignore
   - check if .eslintrc* exists → create/verify .eslintignore
   - check if eslint.config.* exists → ensure the config's `ignores` entries cover required patterns
   - check if .prettierrc* exists → create/verify .prettierignore
   - check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - check if terraform files (*.tf) exist → create/verify .terraformignore
   - check if .helmignore needed (helm charts present) → create/verify .helmignore

   **if ignore file already exists**: verify it contains essential patterns, append missing critical patterns only
   **if ignore file missing**: create with full pattern set for detected technology

   **common patterns by technology** (from plan.md tech stack):
   - **node.js/javascript/typescript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **c#/.net**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **php**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **c++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **c**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `*.dll`, `autom4te.cache/`, `config.status`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **swift**: `.build/`, `deriveddata/`, `*.swiftpm/`, `packages/`
   - **r**: `.rproj.user/`, `.rhistory`, `.rdata`, `.ruserdata`, `*.rproj`, `packrat/`, `renv/`
   - **universal**: `.ds_store`, `thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **tool-specific patterns**:
   - **docker**: `node_modules/`, `.git/`, `dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **eslint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. parse tasks.md structure and extract:
   - **task phases**: setup, tests, core, integration, polish
   - **task dependencies**: sequential vs parallel execution rules
   - **task details**: id, description, file paths, parallel markers [p]
   - **execution flow**: order and dependency requirements

6. execute implementation following the task plan:
   - **phase-by-phase execution**: complete each phase before moving to the next
   - **respect dependencies**: run sequential tasks in order, parallel tasks [p] can run together  
   - **follow tdd approach**: execute test tasks before their corresponding implementation tasks
   - **file-based coordination**: tasks affecting the same files must run sequentially
   - **validation checkpoints**: verify each phase completion before proceeding

7. implementation execution rules:
   - **setup first**: initialize project structure, dependencies, configuration
   - **tests before code**: if you need to write tests for contracts, entities, and integration scenarios
   - **core development**: implement models, services, cli commands, endpoints
   - **integration work**: database connections, middleware, logging, external services
   - **polish and validation**: unit tests, performance optimization, documentation

8. progress tracking and error handling:
   - report progress after each completed task
   - halt execution if any non-parallel task fails
   - for parallel tasks [p], continue with successful tasks, report failed ones
   - provide clear error messages with context for debugging
   - suggest next steps if implementation cannot proceed
   - **important** for completed tasks, make sure to mark the task off as [x] in the tasks file.

9. completion validation:
   - verify all required tasks are completed
   - check that implemented features match the original specification
   - validate that tests pass and coverage meets requirements
   - confirm the implementation follows the technical plan
   - report final status with summary of completed work

note: this command assumes a complete task breakdown exists in tasks.md. if tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.

10. **check for extension hooks**: after completion validation, check if `.specify/extensions.yml` exists in the project root.
    - if it exists, read it and look for entries under the `hooks.after_implement` key
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
