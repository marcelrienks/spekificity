---
description: identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
handoffs: 
  - label: build technical plan
    agent: speckit.plan
    prompt: create a plan for the spec. i am building with...
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before clarification)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_clarify` key
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

goal: detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

note: this clarification workflow is expected to run (and be completed) before invoking `/speckit.plan`. if the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

execution steps:

1. run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` from repo root **once** (combined `--json --paths-only` mode / `-json -pathsonly`). parse minimal json payload fields:
   - `feature_dir`
   - `feature_spec`
   - (optionally capture `impl_plan`, `tasks` for future chained flows.)
   - if json parsing fails, abort and instruct user to re-run `/speckit.specify` or verify feature branch environment.
   - for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").

2. load the current spec file. perform a structured ambiguity & coverage scan using this taxonomy. for each category, mark status: clear / partial / missing. produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

   functional scope & behavior:
   - core user goals & success criteria
   - explicit out-of-scope declarations
   - user roles / personas differentiation

   domain & data model:
   - entities, attributes, relationships
   - identity & uniqueness rules
   - lifecycle/state transitions
   - data volume / scale assumptions

   interaction & ux flow:
   - critical user journeys / sequences
   - error/empty/loading states
   - accessibility or localization notes

   non-functional quality attributes:
   - performance (latency, throughput targets)
   - scalability (horizontal/vertical, limits)
   - reliability & availability (uptime, recovery expectations)
   - observability (logging, metrics, tracing signals)
   - security & privacy (authn/z, data protection, threat assumptions)
   - compliance / regulatory constraints (if any)

   integration & external dependencies:
   - external services/apis and failure modes
   - data import/export formats
   - protocol/versioning assumptions

   edge cases & failure handling:
   - negative scenarios
   - rate limiting / throttling
   - conflict resolution (e.g., concurrent edits)

   constraints & tradeoffs:
   - technical constraints (language, storage, hosting)
   - explicit tradeoffs or rejected alternatives

   terminology & consistency:
   - canonical glossary terms
   - avoided synonyms / deprecated terms

   completion signals:
   - acceptance criteria testability
   - measurable definition of done style indicators

   misc / placeholders:
   - todo markers / unresolved decisions
   - ambiguous adjectives ("robust", "intuitive") lacking quantification

   for each category with partial or missing status, add a candidate question opportunity unless:
   - clarification would not materially change implementation or validation strategy
   - information is better deferred to planning phase (note internally)

3. generate (internally) a prioritized queue of candidate clarification questions (maximum 5). do not output them all at once. apply these constraints:
    - maximum of 5 total questions across the whole session.
    - each question must be answerable with either:
       - a short multiple‑choice selection (2–5 distinct, mutually exclusive options), or
       - a one-word / short‑phrase answer (explicitly constrain: "answer in <=5 words").
    - only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, ux behavior, operational readiness, or compliance validation.
    - ensure category coverage balance: attempt to cover the highest impact unresolved categories first; avoid asking two low-impact questions when a single high-impact area (e.g., security posture) is unresolved.
    - exclude questions already answered, trivial stylistic preferences, or plan-level execution details (unless blocking correctness).
    - favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests.
    - if more than 5 categories remain unresolved, select the top 5 by (impact * uncertainty) heuristic.

4. sequential questioning loop (interactive):
    - present exactly one question at a time.
    - for multiple‑choice questions:
       - **analyze all options** and determine the **most suitable option** based on:
          - best practices for the project type
          - common patterns in similar implementations
          - risk reduction (security, performance, maintainability)
          - alignment with any explicit project goals or constraints visible in the spec
       - present your **recommended option prominently** at the top with clear reasoning (1-2 sentences explaining why this is the best choice).
       - format as: `**recommended:** option [x] - <reasoning>`
       - then render all options as a markdown table:

       | option | description |
       |--------|-------------|
       | a | <option a description> |
       | b | <option b description> |
       | c | <option c description> (add d/e as needed up to 5) |
       | short | provide a different short answer (<=5 words) (include only if free-form alternative is appropriate) |

       - after the table, add: `you can reply with the option letter (e.g., "a"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`
    - for short‑answer style (no meaningful discrete options):
       - provide your **suggested answer** based on best practices and context.
       - format as: `**suggested:** <your proposed answer> - <brief reasoning>`
       - then output: `format: short answer (<=5 words). you can accept the suggestion by saying "yes" or "suggested", or provide your own answer.`
    - after the user answers:
       - if the user replies with "yes", "recommended", or "suggested", use your previously stated recommendation/suggestion as the answer.
       - otherwise, validate the answer maps to one option or fits the <=5 word constraint.
       - if ambiguous, ask for a quick disambiguation (count still belongs to same question; do not advance).
       - once satisfactory, record it in working memory (do not yet write to disk) and move to the next queued question.
    - stop asking further questions when:
       - all critical ambiguities resolved early (remaining queued items become unnecessary), or
       - user signals completion ("done", "good", "no more"), or
       - you reach 5 asked questions.
    - never reveal future queued questions in advance.
    - if no valid questions exist at start, immediately report no critical ambiguities.

5. integration after each accepted answer (incremental update approach):
    - maintain in-memory representation of the spec (loaded once at start) plus the raw file contents.
    - for the first integrated answer in this session:
       - ensure a `## clarifications` section exists (create it just after the highest-level contextual/overview section per the spec template if missing).
       - under it, create (if not present) a `### session yyyy-mm-dd` subheading for today.
    - append a bullet line immediately after acceptance: `- q: <question> → a: <final answer>`.
    - then immediately apply the clarification to the most appropriate section(s):
       - functional ambiguity → update or add a bullet in functional requirements.
       - user interaction / actor distinction → update user stories or actors subsection (if present) with clarified role, constraint, or scenario.
       - data shape / entities → update data model (add fields, types, relationships) preserving ordering; note added constraints succinctly.
       - non-functional constraint → add/modify measurable criteria in success criteria > measurable outcomes (convert vague adjective to metric or explicit target).
       - edge case / negative flow → add a new bullet under edge cases / error handling (or create such subsection if template provides placeholder for it).
       - terminology conflict → normalize term across spec; retain original only if necessary by adding `(formerly referred to as "x")` once.
    - if the clarification invalidates an earlier ambiguous statement, replace that statement instead of duplicating; leave no obsolete contradictory text.
    - save the spec file after each integration to minimize risk of context loss (atomic overwrite).
    - preserve formatting: do not reorder unrelated sections; keep heading hierarchy intact.
    - keep each inserted clarification minimal and testable (avoid narrative drift).

6. validation (performed after each write plus final pass):
   - clarifications session contains exactly one bullet per accepted answer (no duplicates).
   - total asked (accepted) questions ≤ 5.
   - updated sections contain no lingering vague placeholders the new answer was meant to resolve.
   - no contradictory earlier statement remains (scan for now-invalid alternative choices removed).
   - markdown structure valid; only allowed new headings: `## clarifications`, `### session yyyy-mm-dd`.
   - terminology consistency: same canonical term used across all updated sections.

7. write the updated spec back to `feature_spec`.

8. report completion (after questioning loop ends or early termination):
   - number of questions asked & answered.
   - path to updated spec.
   - sections touched (list names).
   - coverage summary table listing each taxonomy category with status: resolved (was partial/missing and addressed), deferred (exceeds question quota or better suited for planning), clear (already sufficient), outstanding (still partial/missing but low impact).
   - if any outstanding or deferred remain, recommend whether to proceed to `/speckit.plan` or run `/speckit.clarify` again later post-plan.
   - suggested next command.

behavior rules:

- if no meaningful ambiguities found (or all potential questions would be low-impact), respond: "no critical ambiguities detected worth formal clarification." and suggest proceeding.
- if spec file missing, instruct user to run `/speckit.specify` first (do not create a new spec here).
- never exceed 5 total asked questions (clarification retries for a single question do not count as new questions).
- avoid speculative tech stack questions unless the absence blocks functional clarity.
- respect user early termination signals ("stop", "done", "proceed").
- if no questions asked due to full coverage, output a compact coverage summary (all categories clear) then suggest advancing.
- if quota reached with unresolved high-impact categories remaining, explicitly flag them under deferred with rationale.

context for prioritization: $arguments

## post-execution checks

**check for extension hooks (after clarification)**:
check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.after_clarify` key
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
