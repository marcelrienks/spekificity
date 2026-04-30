---

description: "task list template for feature implementation"
---

# tasks: [feature name]

**input**: design documents from `/specs/[###-feature-name]/`
**prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**tests**: the examples below include test tasks. tests are optional - only include them if explicitly requested in the feature specification.

**organization**: tasks are grouped by user story to enable independent implementation and testing of each story.

## format: `[id] [p?] [story] description`

- **[p]**: can run in parallel (different files, no dependencies)
- **[story]**: which user story this task belongs to (e.g., us1, us2, us3)
- include exact file paths in descriptions

## path conventions

- **single project**: `src/`, `tests/` at repository root
- **web app**: `backend/src/`, `frontend/src/`
- **mobile**: `api/src/`, `ios/src/` or `android/src/`
- paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  important: the tasks below are sample tasks for illustration purposes only.
  
  the /speckit.tasks command must replace these with actual tasks based on:
  - user stories from spec.md (with their priorities p1, p2, p3...)
  - feature requirements from plan.md
  - entities from data-model.md
  - endpoints from contracts/
  
  tasks must be organized by user story so each story can be:
  - implemented independently
  - tested independently
  - delivered as an mvp increment
  
  do not keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## phase 1: setup (shared infrastructure)

**purpose**: project initialization and basic structure

- [ ] t001 create project structure per implementation plan
- [ ] t002 initialize [language] project with [framework] dependencies
- [ ] t003 [p] configure linting and formatting tools

---

## phase 2: foundational (blocking prerequisites)

**purpose**: core infrastructure that must be complete before any user story can be implemented

**⚠️ critical**: no user story work can begin until this phase is complete

examples of foundational tasks (adjust based on your project):

- [ ] t004 setup database schema and migrations framework
- [ ] t005 [p] implement authentication/authorization framework
- [ ] t006 [p] setup api routing and middleware structure
- [ ] t007 create base models/entities that all stories depend on
- [ ] t008 configure error handling and logging infrastructure
- [ ] t009 setup environment configuration management

**checkpoint**: foundation ready - user story implementation can now begin in parallel

---

## phase 3: user story 1 - [title] (priority: p1) 🎯 mvp

**goal**: [brief description of what this story delivers]

**independent test**: [how to verify this story works on its own]

### tests for user story 1 (optional - only if tests requested) ⚠️

> **note: write these tests first, ensure they fail before implementation**

- [ ] t010 [p] [us1] contract test for [endpoint] in tests/contract/test_[name].py
- [ ] t011 [p] [us1] integration test for [user journey] in tests/integration/test_[name].py

### implementation for user story 1

- [ ] t012 [p] [us1] create [entity1] model in src/models/[entity1].py
- [ ] t013 [p] [us1] create [entity2] model in src/models/[entity2].py
- [ ] t014 [us1] implement [service] in src/services/[service].py (depends on t012, t013)
- [ ] t015 [us1] implement [endpoint/feature] in src/[location]/[file].py
- [ ] t016 [us1] add validation and error handling
- [ ] t017 [us1] add logging for user story 1 operations

**checkpoint**: at this point, user story 1 should be fully functional and testable independently

---

## phase 4: user story 2 - [title] (priority: p2)

**goal**: [brief description of what this story delivers]

**independent test**: [how to verify this story works on its own]

### tests for user story 2 (optional - only if tests requested) ⚠️

- [ ] t018 [p] [us2] contract test for [endpoint] in tests/contract/test_[name].py
- [ ] t019 [p] [us2] integration test for [user journey] in tests/integration/test_[name].py

### implementation for user story 2

- [ ] t020 [p] [us2] create [entity] model in src/models/[entity].py
- [ ] t021 [us2] implement [service] in src/services/[service].py
- [ ] t022 [us2] implement [endpoint/feature] in src/[location]/[file].py
- [ ] t023 [us2] integrate with user story 1 components (if needed)

**checkpoint**: at this point, user stories 1 and 2 should both work independently

---

## phase 5: user story 3 - [title] (priority: p3)

**goal**: [brief description of what this story delivers]

**independent test**: [how to verify this story works on its own]

### tests for user story 3 (optional - only if tests requested) ⚠️

- [ ] t024 [p] [us3] contract test for [endpoint] in tests/contract/test_[name].py
- [ ] t025 [p] [us3] integration test for [user journey] in tests/integration/test_[name].py

### implementation for user story 3

- [ ] t026 [p] [us3] create [entity] model in src/models/[entity].py
- [ ] t027 [us3] implement [service] in src/services/[service].py
- [ ] t028 [us3] implement [endpoint/feature] in src/[location]/[file].py

**checkpoint**: all user stories should now be independently functional

---

[add more user story phases as needed, following the same pattern]

---

## phase n: polish & cross-cutting concerns

**purpose**: improvements that affect multiple user stories

- [ ] txxx [p] documentation updates in docs/
- [ ] txxx code cleanup and refactoring
- [ ] txxx performance optimization across all stories
- [ ] txxx [p] additional unit tests (if requested) in tests/unit/
- [ ] txxx security hardening
- [ ] txxx run quickstart.md validation

---

## dependencies & execution order

### phase dependencies

- **setup (phase 1)**: no dependencies - can start immediately
- **foundational (phase 2)**: depends on setup completion - blocks all user stories
- **user stories (phase 3+)**: all depend on foundational phase completion
  - user stories can then proceed in parallel (if staffed)
  - or sequentially in priority order (p1 → p2 → p3)
- **polish (final phase)**: depends on all desired user stories being complete

### user story dependencies

- **user story 1 (p1)**: can start after foundational (phase 2) - no dependencies on other stories
- **user story 2 (p2)**: can start after foundational (phase 2) - may integrate with us1 but should be independently testable
- **user story 3 (p3)**: can start after foundational (phase 2) - may integrate with us1/us2 but should be independently testable

### within each user story

- tests (if included) must be written and fail before implementation
- models before services
- services before endpoints
- core implementation before integration
- story complete before moving to next priority

### parallel opportunities

- all setup tasks marked [p] can run in parallel
- all foundational tasks marked [p] can run in parallel (within phase 2)
- once foundational phase completes, all user stories can start in parallel (if team capacity allows)
- all tests for a user story marked [p] can run in parallel
- models within a story marked [p] can run in parallel
- different user stories can be worked on in parallel by different team members

---

## parallel example: user story 1

```bash
# launch all tests for user story 1 together (if tests requested):
task: "contract test for [endpoint] in tests/contract/test_[name].py"
task: "integration test for [user journey] in tests/integration/test_[name].py"

# launch all models for user story 1 together:
task: "create [entity1] model in src/models/[entity1].py"
task: "create [entity2] model in src/models/[entity2].py"
```

---

## implementation strategy

### mvp first (user story 1 only)

1. complete phase 1: setup
2. complete phase 2: foundational (critical - blocks all stories)
3. complete phase 3: user story 1
4. **stop and validate**: test user story 1 independently
5. deploy/demo if ready

### incremental delivery

1. complete setup + foundational → foundation ready
2. add user story 1 → test independently → deploy/demo (mvp!)
3. add user story 2 → test independently → deploy/demo
4. add user story 3 → test independently → deploy/demo
5. each story adds value without breaking previous stories

### parallel team strategy

with multiple developers:

1. team completes setup + foundational together
2. once foundational is done:
   - developer a: user story 1
   - developer b: user story 2
   - developer c: user story 3
3. stories complete and integrate independently

---

## notes

- [p] tasks = different files, no dependencies
- [story] label maps task to specific user story for traceability
- each user story should be independently completable and testable
- verify tests fail before implementing
- commit after each task or logical group
- stop at any checkpoint to validate story independently
- avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
