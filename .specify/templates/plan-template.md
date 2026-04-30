# implementation plan: [feature]

**branch**: `[###-feature-name]` | **date**: [date] | **spec**: [link]
**input**: feature specification from `/specs/[###-feature-name]/spec.md`

**note**: this template is filled in by the `/speckit.plan` command. see `.specify/templates/plan-template.md` for the execution workflow.

## summary

[extract from feature spec: primary requirement + technical approach from research]

## technical context

<!--
  action required: replace the content in this section with the technical details
  for the project. the structure here is presented in advisory capacity to guide
  the iteration process.
-->

**language/version**: [e.g., python 3.11, swift 5.9, rust 1.75 or needs clarification]  
**primary dependencies**: [e.g., fastapi, uikit, llvm or needs clarification]  
**storage**: [if applicable, e.g., postgresql, coredata, files or n/a]  
**testing**: [e.g., pytest, xctest, cargo test or needs clarification]  
**target platform**: [e.g., linux server, ios 15+, wasm or needs clarification]
**project type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or needs clarification]  
**performance goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or needs clarification]  
**constraints**: [domain-specific, e.g., <200ms p95, <100mb memory, offline-capable or needs clarification]  
**scale/scope**: [domain-specific, e.g., 10k users, 1m loc, 50 screens or needs clarification]

## constitution check

*gate: must pass before phase 0 research. re-check after phase 1 design.*

[gates determined based on constitution file]

## project structure

### documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # this file (/speckit.plan command output)
├── research.md          # phase 0 output (/speckit.plan command)
├── data-model.md        # phase 1 output (/speckit.plan command)
├── quickstart.md        # phase 1 output (/speckit.plan command)
├── contracts/           # phase 1 output (/speckit.plan command)
└── tasks.md             # phase 2 output (/speckit.tasks command - not created by /speckit.plan)
```

### source code (repository root)
<!--
  action required: replace the placeholder tree below with the concrete layout
  for this feature. delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). the delivered plan must
  not include option labels.
-->

```text
# [remove if unused] option 1: single project (default)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [remove if unused] option 2: web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [remove if unused] option 3: mobile + api (when "ios/android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, ui flows, platform tests]
```

**structure decision**: [document the selected structure and reference the real
directories captured above]

## complexity tracking

> **fill only if constitution check has violations that must be justified**

| violation | why needed | simpler alternative rejected because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., repository pattern] | [specific problem] | [why direct db access insufficient] |
