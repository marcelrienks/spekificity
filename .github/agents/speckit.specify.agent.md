---
description: create or update the feature specification from a natural language feature description.
handoffs: 
  - label: build technical plan
    agent: speckit.plan
    prompt: create a plan for the spec. i am building with...
  - label: clarify spec requirements
    agent: speckit.clarify
    prompt: clarify specification requirements
    send: true
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before specification)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_specify` key
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

the text the user typed after `/speckit.specify` in the triggering message **is** the feature description. assume you always have it available in this conversation even if `$arguments` appears literally below. do not ask the user to repeat it unless they provided an empty command.

given that feature description, do this:

1. **generate a concise short name** (2-4 words) for the feature:
   - analyze the feature description and extract the most meaningful keywords
   - create a 2-4 word short name that captures the essence of the feature
   - use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - preserve technical terms and acronyms (oauth2, api, jwt, etc.)
   - keep it concise but descriptive enough to understand the feature at a glance
   - examples:
     - "i want to add user authentication" → "user-auth"
     - "implement oauth2 integration for the api" → "oauth2-api-integration"
     - "create a dashboard for analytics" → "analytics-dashboard"
     - "fix payment processing timeout bug" → "fix-payment-timeout"

2. **branch creation** (optional, via hook):

   if a `before_specify` hook ran successfully in the pre-execution checks above, it will have created/switched to a git branch and output json containing `branch_name` and `feature_num`. note these values for reference, but the branch name does **not** dictate the spec directory name.

   if the user explicitly provided `git_branch_name`, pass it through to the hook so the branch script uses the exact value as the branch name (bypassing all prefix/suffix generation).

3. **create the spec feature directory**:

   specs live under the default `specs/` directory unless the user explicitly provides `specify_feature_directory`.

   **resolution order for `specify_feature_directory`**:
   1. if the user explicitly provided `specify_feature_directory` (e.g., via environment variable, argument, or configuration), use it as-is
   2. otherwise, auto-generate it under `specs/`:
      - check `.specify/init-options.json` for `branch_numbering`
      - if `"timestamp"`: prefix is `yyyymmdd-hhmmss` (current timestamp)
      - if `"sequential"` or absent: prefix is `nnn` (next available 3-digit number after scanning existing directories in `specs/`)
      - construct the directory name: `<prefix>-<short-name>` (e.g., `003-user-auth` or `20260319-143022-user-auth`)
      - set `specify_feature_directory` to `specs/<directory-name>`

   **create the directory and spec file**:
   - `mkdir -p specify_feature_directory`
   - copy `.specify/templates/spec-template.md` to `specify_feature_directory/spec.md` as the starting point
   - set `spec_file` to `specify_feature_directory/spec.md`
   - persist the resolved path to `.specify/feature.json`:
     ```json
     {
       "feature_directory": "<resolved feature dir>"
     }
     ```
     write the actual resolved directory path value (for example, `specs/003-user-auth`), not the literal string `specify_feature_directory`.
     this allows downstream commands (`/speckit.plan`, `/speckit.tasks`, etc.) to locate the feature directory without relying on git branch name conventions.

   **important**:
   - you must only create one feature per `/speckit.specify` invocation
   - the spec directory name and the git branch name are independent — they may be the same but that is the user's choice
   - the spec directory and file are always created by this command, never by the hook

4. load `.specify/templates/spec-template.md` to understand required sections.

5. follow this execution flow:
    1. parse user description from arguments
       if empty: error "no feature description provided"
    2. extract key concepts from description
       identify: actors, actions, data, constraints
    3. for unclear aspects:
       - make informed guesses based on context and industry standards
       - only mark with [needs clarification: specific question] if:
         - the choice significantly impacts feature scope or user experience
         - multiple reasonable interpretations exist with different implications
         - no reasonable default exists
       - **limit: maximum 3 [needs clarification] markers total**
       - prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. fill user scenarios & testing section
       if no clear user flow: error "cannot determine user scenarios"
    5. generate functional requirements
       each requirement must be testable
       use reasonable defaults for unspecified details (document assumptions in assumptions section)
    6. define success criteria
       create measurable, technology-agnostic outcomes
       include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       each criterion must be verifiable without implementation details
    7. identify key entities (if data involved)
    8. return: success (spec ready for planning)

6. write the specification to spec_file using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

7. **specification quality validation**: after writing the initial spec, validate it against quality criteria:

   a. **create spec quality checklist**: generate a checklist file at `specify_feature_directory/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # specification quality checklist: [feature name]
      
      **purpose**: validate specification completeness and quality before proceeding to planning
      **created**: [date]
      **feature**: [link to spec.md]
      
      ## content quality
      
      - [ ] no implementation details (languages, frameworks, apis)
      - [ ] focused on user value and business needs
      - [ ] written for non-technical stakeholders
      - [ ] all mandatory sections completed
      
      ## requirement completeness
      
      - [ ] no [needs clarification] markers remain
      - [ ] requirements are testable and unambiguous
      - [ ] success criteria are measurable
      - [ ] success criteria are technology-agnostic (no implementation details)
      - [ ] all acceptance scenarios are defined
      - [ ] edge cases are identified
      - [ ] scope is clearly bounded
      - [ ] dependencies and assumptions identified
      
      ## feature readiness
      
      - [ ] all functional requirements have clear acceptance criteria
      - [ ] user scenarios cover primary flows
      - [ ] feature meets measurable outcomes defined in success criteria
      - [ ] no implementation details leak into specification
      
      ## notes
      
      - items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
      ```

   b. **run validation check**: review the spec against each checklist item:
      - for each item, determine if it passes or fails
      - document specific issues found (quote relevant spec sections)

   c. **handle validation results**:

      - **if all items pass**: mark checklist complete and proceed to step 7

      - **if items fail (excluding [needs clarification])**:
        1. list the failing items and specific issues
        2. update the spec to address each issue
        3. re-run validation until all items pass (max 3 iterations)
        4. if still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **if [needs clarification] markers remain**:
        1. extract all [needs clarification: ...] markers from the spec
        2. **limit check**: if more than 3 markers exist, keep only the 3 most critical (by scope/security/ux impact) and make informed guesses for the rest
        3. for each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## question [n]: [topic]
           
           **context**: [quote relevant spec section]
           
           **what we need to know**: [specific question from needs clarification marker]
           
           **suggested answers**:
           
           | option | answer | implications |
           |--------|--------|--------------|
           | a      | [first suggested answer] | [what this means for the feature] |
           | b      | [second suggested answer] | [what this means for the feature] |
           | c      | [third suggested answer] | [what this means for the feature] |
           | custom | provide your own answer | [explain how to provide custom input] |
           
           **your choice**: _[wait for user response]_
           ```

        4. **critical - table formatting**: ensure markdown tables are properly formatted:
           - use consistent spacing with pipes aligned
           - each cell should have spaces around content: `| content |` not `|content|`
           - header separator must have at least 3 dashes: `|--------|`
           - test that the table renders correctly in markdown preview
        5. number questions sequentially (q1, q2, q3 - max 3 total)
        6. present all questions together before waiting for responses
        7. wait for user to respond with their choices for all questions (e.g., "q1: a, q2: custom - [details], q3: b")
        8. update the spec by replacing each [needs clarification] marker with the user's selected or provided answer
        9. re-run validation after all clarifications are resolved

   d. **update checklist**: after each validation iteration, update the checklist file with current pass/fail status

8. **report completion** to the user with:
   - `specify_feature_directory` — the feature directory path
   - `spec_file` — the spec file path
   - checklist results summary
   - readiness for the next phase (`/speckit.clarify` or `/speckit.plan`)

9. **check for extension hooks**: after reporting completion, check if `.specify/extensions.yml` exists in the project root.
   - if it exists, read it and look for entries under the `hooks.after_specify` key
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

**note:** branch creation is handled by the `before_specify` hook (git extension). spec directory and file creation are always handled by this core command.

## quick guidelines

- focus on **what** users need and **why**.
- avoid how to implement (no tech stack, apis, code structure).
- written for business stakeholders, not developers.
- do not create any checklists that are embedded in the spec. that will be a separate command.

### section requirements

- **mandatory sections**: must be completed for every feature
- **optional sections**: include only when relevant to the feature
- when a section doesn't apply, remove it entirely (don't leave as "n/a")

### for ai generation

when creating this spec from a user prompt:

1. **make informed guesses**: use context, industry standards, and common patterns to fill gaps
2. **document assumptions**: record reasonable defaults in the assumptions section
3. **limit clarifications**: maximum 3 [needs clarification] markers - use only for critical decisions that:
   - significantly impact feature scope or user experience
   - have multiple reasonable interpretations with different implications
   - lack any reasonable default
4. **prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **think like a tester**: every vague requirement should fail the "testable and unambiguous" checklist item
6. **common areas needing clarification** (only if no reasonable default exists):
   - feature scope and boundaries (include/exclude specific use cases)
   - user types and permissions (if multiple conflicting interpretations possible)
   - security/compliance requirements (when legally/financially significant)

**examples of reasonable defaults** (don't ask about these):

- data retention: industry-standard practices for the domain
- performance targets: standard web/mobile app expectations unless specified
- error handling: user-friendly messages with appropriate fallbacks
- authentication method: standard session-based or oauth2 for web apps
- integration patterns: use project-appropriate patterns (rest/graphql for web services, function calls for libraries, cli args for tools, etc.)

### success criteria guidelines

success criteria must be:

1. **measurable**: include specific metrics (time, percentage, count, rate)
2. **technology-agnostic**: no mention of frameworks, languages, databases, or tools
3. **user-focused**: describe outcomes from user/business perspective, not system internals
4. **verifiable**: can be tested/validated without knowing implementation details

**good examples**:

- "users can complete checkout in under 3 minutes"
- "system supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "task completion rate improves by 40%"

**bad examples** (implementation-focused):

- "api response time is under 200ms" (too technical, use "users see results instantly")
- "database can handle 1000 tps" (implementation detail, use user-facing metric)
- "react components render efficiently" (framework-specific)
- "redis cache hit rate above 80%" (technology-specific)
