---
description: generate a custom checklist for the current feature based on user requirements.
---

## checklist purpose: "unit tests for english"

**critical concept**: checklists are **unit tests for requirements writing** - they validate the quality, clarity, and completeness of requirements in a given domain.

**not for verification/testing**:

- ❌ not "verify the button clicks correctly"
- ❌ not "test error handling works"
- ❌ not "confirm the api returns 200"
- ❌ not checking if code/implementation matches the spec

**for requirements quality validation**:

- ✅ "are visual hierarchy requirements defined for all card types?" (completeness)
- ✅ "is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- ✅ "are hover state requirements consistent across all interactive elements?" (consistency)
- ✅ "are accessibility requirements defined for keyboard navigation?" (coverage)
- ✅ "does the spec define what happens when logo image fails to load?" (edge cases)

**metaphor**: if your spec is code written in english, the checklist is its unit test suite. you're testing whether the requirements are well-written, complete, unambiguous, and ready for implementation - not whether the implementation works.

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before checklist generation)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_checklist` key
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

    wait for the result of the hook command before proceeding to the execution steps.
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## execution steps

1. **setup**: run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse json for feature_dir and available_docs list.
   - all file paths must be absolute.
   - for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

2. **clarify intent (dynamic)**: derive up to three initial contextual clarifying questions (no pre-baked catalog). they must:
   - be generated from the user's phrasing + extracted signals from spec/plan/tasks
   - only ask about information that materially changes checklist content
   - be skipped individually if already unambiguous in `$arguments`
   - prefer precision over breadth

   generation algorithm:
   1. extract signals: feature domain keywords (e.g., auth, latency, ux, api), risk indicators ("critical", "must", "compliance"), stakeholder hints ("qa", "review", "security team"), and explicit deliverables ("a11y", "rollback", "contracts").
   2. cluster signals into candidate focus areas (max 4) ranked by relevance.
   3. identify probable audience & timing (author, reviewer, qa, release) if not explicit.
   4. detect missing dimensions: scope breadth, depth/rigor, risk emphasis, exclusion boundaries, measurable acceptance criteria.
   5. formulate questions chosen from these archetypes:
      - scope refinement (e.g., "should this include integration touchpoints with x and y or stay limited to local module correctness?")
      - risk prioritization (e.g., "which of these potential risk areas should receive mandatory gating checks?")
      - depth calibration (e.g., "is this a lightweight pre-commit sanity list or a formal release gate?")
      - audience framing (e.g., "will this be used by the author only or peers during pr review?")
      - boundary exclusion (e.g., "should we explicitly exclude performance tuning items this round?")
      - scenario class gap (e.g., "no recovery flows detected—are rollback / partial failure paths in scope?")

   question formatting rules:
   - if presenting options, generate a compact table with columns: option | candidate | why it matters
   - limit to a–e options maximum; omit table if a free-form answer is clearer
   - never ask the user to restate what they already said
   - avoid speculative categories (no hallucination). if uncertain, ask explicitly: "confirm whether x belongs in scope."

   defaults when interaction impossible:
   - depth: standard
   - audience: reviewer (pr) if code-related; author otherwise
   - focus: top 2 relevance clusters

   output the questions (label q1/q2/q3). after answers: if ≥2 scenario classes (alternate / exception / recovery / non-functional domain) remain unclear, you may ask up to two more targeted follow‑ups (q4/q5) with a one-line justification each (e.g., "unresolved recovery path risk"). do not exceed five total questions. skip escalation if user explicitly declines more.

3. **understand user request**: combine `$arguments` + clarifying answers:
   - derive checklist theme (e.g., security, review, deploy, ux)
   - consolidate explicit must-have items mentioned by user
   - map focus selections to category scaffolding
   - infer any missing context from spec/plan/tasks (do not hallucinate)

4. **load feature context**: read from feature_dir:
   - spec.md: feature requirements and scope
   - plan.md (if exists): technical details, dependencies
   - tasks.md (if exists): implementation tasks

   **context loading strategy**:
   - load only necessary portions relevant to active focus areas (avoid full-file dumping)
   - prefer summarizing long sections into concise scenario/requirement bullets
   - use progressive disclosure: add follow-on retrieval only if gaps detected
   - if source docs are large, generate interim summary items instead of embedding raw text

5. **generate checklist** - create "unit tests for requirements":
   - create `feature_dir/checklists/` directory if it doesn't exist
   - generate unique checklist filename:
     - use short, descriptive name based on domain (e.g., `ux.md`, `api.md`, `security.md`)
     - format: `[domain].md`
   - file handling behavior:
     - if file does not exist: create new file and number items starting from chk001
     - if file exists: append new items to existing file, continuing from the last chk id (e.g., if last item is chk015, start new items at chk016)
   - never delete or replace existing checklist content - always preserve and append

   **core principle - test the requirements, not the implementation**:
   every checklist item must evaluate the requirements themselves for:
   - **completeness**: are all necessary requirements present?
   - **clarity**: are requirements unambiguous and specific?
   - **consistency**: do requirements align with each other?
   - **measurability**: can requirements be objectively verified?
   - **coverage**: are all scenarios/edge cases addressed?

   **category structure** - group items by requirement quality dimensions:
   - **requirement completeness** (are all necessary requirements documented?)
   - **requirement clarity** (are requirements specific and unambiguous?)
   - **requirement consistency** (do requirements align without conflicts?)
   - **acceptance criteria quality** (are success criteria measurable?)
   - **scenario coverage** (are all flows/cases addressed?)
   - **edge case coverage** (are boundary conditions defined?)
   - **non-functional requirements** (performance, security, accessibility, etc. - are they specified?)
   - **dependencies & assumptions** (are they documented and validated?)
   - **ambiguities & conflicts** (what needs clarification?)

   **how to write checklist items - "unit tests for english"**:

   ❌ **wrong** (testing implementation):
   - "verify landing page displays 3 episode cards"
   - "test hover states work on desktop"
   - "confirm logo click navigates home"

   ✅ **correct** (testing requirements quality):
   - "are the exact number and layout of featured episodes specified?" [completeness]
   - "is 'prominent display' quantified with specific sizing/positioning?" [clarity]
   - "are hover state requirements consistent across all interactive elements?" [consistency]
   - "are keyboard navigation requirements defined for all interactive ui?" [coverage]
   - "is the fallback behavior specified when logo image fails to load?" [edge cases]
   - "are loading states defined for asynchronous episode data?" [completeness]
   - "does the spec define visual hierarchy for competing ui elements?" [clarity]

   **item structure**:
   each item should follow this pattern:
   - question format asking about requirement quality
   - focus on what's written (or not written) in the spec/plan
   - include quality dimension in brackets [completeness/clarity/consistency/etc.]
   - reference spec section `[spec §x.y]` when checking existing requirements
   - use `[gap]` marker when checking for missing requirements

   **examples by quality dimension**:

   completeness:
   - "are error handling requirements defined for all api failure modes? [gap]"
   - "are accessibility requirements specified for all interactive elements? [completeness]"
   - "are mobile breakpoint requirements defined for responsive layouts? [gap]"

   clarity:
   - "is 'fast loading' quantified with specific timing thresholds? [clarity, spec §nfr-2]"
   - "are 'related episodes' selection criteria explicitly defined? [clarity, spec §fr-5]"
   - "is 'prominent' defined with measurable visual properties? [ambiguity, spec §fr-4]"

   consistency:
   - "do navigation requirements align across all pages? [consistency, spec §fr-10]"
   - "are card component requirements consistent between landing and detail pages? [consistency]"

   coverage:
   - "are requirements defined for zero-state scenarios (no episodes)? [coverage, edge case]"
   - "are concurrent user interaction scenarios addressed? [coverage, gap]"
   - "are requirements specified for partial data loading failures? [coverage, exception flow]"

   measurability:
   - "are visual hierarchy requirements measurable/testable? [acceptance criteria, spec §fr-1]"
   - "can 'balanced visual weight' be objectively verified? [measurability, spec §fr-2]"

   **scenario classification & coverage** (requirements quality focus):
   - check if requirements exist for: primary, alternate, exception/error, recovery, non-functional scenarios
   - for each scenario class, ask: "are [scenario type] requirements complete, clear, and consistent?"
   - if scenario class missing: "are [scenario type] requirements intentionally excluded or missing? [gap]"
   - include resilience/rollback when state mutation occurs: "are rollback requirements defined for migration failures? [gap]"

   **traceability requirements**:
   - minimum: ≥80% of items must include at least one traceability reference
   - each item should reference: spec section `[spec §x.y]`, or use markers: `[gap]`, `[ambiguity]`, `[conflict]`, `[assumption]`
   - if no id system exists: "is a requirement & acceptance criteria id scheme established? [traceability]"

   **surface & resolve issues** (requirements quality problems):
   ask questions about the requirements themselves:
   - ambiguities: "is the term 'fast' quantified with specific metrics? [ambiguity, spec §nfr-1]"
   - conflicts: "do navigation requirements conflict between §fr-10 and §fr-10a? [conflict]"
   - assumptions: "is the assumption of 'always available podcast api' validated? [assumption]"
   - dependencies: "are external podcast api requirements documented? [dependency, gap]"
   - missing definitions: "is 'visual hierarchy' defined with measurable criteria? [gap]"

   **content consolidation**:
   - soft cap: if raw candidate items > 40, prioritize by risk/impact
   - merge near-duplicates checking the same requirement aspect
   - if >5 low-impact edge cases, create one item: "are edge cases x, y, z addressed in requirements? [coverage]"

   **🚫 absolutely prohibited** - these make it an implementation test, not a requirements test:
   - ❌ any item starting with "verify", "test", "confirm", "check" + implementation behavior
   - ❌ references to code execution, user actions, system behavior
   - ❌ "displays correctly", "works properly", "functions as expected"
   - ❌ "click", "navigate", "render", "load", "execute"
   - ❌ test cases, test plans, qa procedures
   - ❌ implementation details (frameworks, apis, algorithms)

   **✅ required patterns** - these test requirements quality:
   - ✅ "are [requirement type] defined/specified/documented for [scenario]?"
   - ✅ "is [vague term] quantified/clarified with specific criteria?"
   - ✅ "are requirements consistent between [section a] and [section b]?"
   - ✅ "can [requirement] be objectively measured/verified?"
   - ✅ "are [edge cases/scenarios] addressed in requirements?"
   - ✅ "does the spec define [missing aspect]?"

6. **structure reference**: generate the checklist following the canonical template in `.specify/templates/checklist-template.md` for title, meta section, category headings, and id formatting. if template is unavailable, use: h1 title, purpose/created meta lines, `##` category sections containing `- [ ] chk### <requirement item>` lines with globally incrementing ids starting at chk001.

7. **report**: output full path to checklist file, item count, and summarize whether the run created a new file or appended to an existing one. summarize:
   - focus areas selected
   - depth level
   - actor/timing
   - any explicit user-specified must-have items incorporated

**important**: each `/speckit.checklist` command invocation uses a short, descriptive checklist filename and either creates a new file or appends to an existing one. this allows:

- multiple checklists of different types (e.g., `ux.md`, `test.md`, `security.md`)
- simple, memorable filenames that indicate checklist purpose
- easy identification and navigation in the `checklists/` folder

to avoid clutter, use descriptive types and clean up obsolete checklists when done.

## example checklist types & sample items

**ux requirements quality:** `ux.md`

sample items (testing the requirements, not the implementation):

- "are visual hierarchy requirements defined with measurable criteria? [clarity, spec §fr-1]"
- "is the number and positioning of ui elements explicitly specified? [completeness, spec §fr-1]"
- "are interaction state requirements (hover, focus, active) consistently defined? [consistency]"
- "are accessibility requirements specified for all interactive elements? [coverage, gap]"
- "is fallback behavior defined when images fail to load? [edge case, gap]"
- "can 'prominent display' be objectively measured? [measurability, spec §fr-4]"

**api requirements quality:** `api.md`

sample items:

- "are error response formats specified for all failure scenarios? [completeness]"
- "are rate limiting requirements quantified with specific thresholds? [clarity]"
- "are authentication requirements consistent across all endpoints? [consistency]"
- "are retry/timeout requirements defined for external dependencies? [coverage, gap]"
- "is versioning strategy documented in requirements? [gap]"

**performance requirements quality:** `performance.md`

sample items:

- "are performance requirements quantified with specific metrics? [clarity]"
- "are performance targets defined for all critical user journeys? [coverage]"
- "are performance requirements under different load conditions specified? [completeness]"
- "can performance requirements be objectively measured? [measurability]"
- "are degradation requirements defined for high-load scenarios? [edge case, gap]"

**security requirements quality:** `security.md`

sample items:

- "are authentication requirements specified for all protected resources? [coverage]"
- "are data protection requirements defined for sensitive information? [completeness]"
- "is the threat model documented and requirements aligned to it? [traceability]"
- "are security requirements consistent with compliance obligations? [consistency]"
- "are security failure/breach response requirements defined? [gap, exception flow]"

## anti-examples: what not to do

**❌ wrong - these test implementation, not requirements:**

```markdown
- [ ] chk001 - verify landing page displays 3 episode cards [spec §fr-001]
- [ ] chk002 - test hover states work correctly on desktop [spec §fr-003]
- [ ] chk003 - confirm logo click navigates to home page [spec §fr-010]
- [ ] chk004 - check that related episodes section shows 3-5 items [spec §fr-005]
```

**✅ correct - these test requirements quality:**

```markdown
- [ ] chk001 - are the number and layout of featured episodes explicitly specified? [completeness, spec §fr-001]
- [ ] chk002 - are hover state requirements consistently defined for all interactive elements? [consistency, spec §fr-003]
- [ ] chk003 - are navigation requirements clear for all clickable brand elements? [clarity, spec §fr-010]
- [ ] chk004 - is the selection criteria for related episodes documented? [gap, spec §fr-005]
- [ ] chk005 - are loading state requirements defined for asynchronous episode data? [gap]
- [ ] chk006 - can "visual hierarchy" requirements be objectively measured? [measurability, spec §fr-001]
```

**key differences:**

- wrong: tests if the system works correctly
- correct: tests if the requirements are written correctly
- wrong: verification of behavior
- correct: validation of requirement quality
- wrong: "does it do x?"
- correct: "is x clearly specified?"

## post-execution checks

**check for extension hooks (after checklist generation)**:
check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.after_checklist` key
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
