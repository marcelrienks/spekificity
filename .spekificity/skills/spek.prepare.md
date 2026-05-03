# /spek.prepare — preparation phase skill

## description

primes the AI session with full codebase context before any feature work begins. reads vault context (decisions, patterns, recent lessons), confirms the graph is current, and surfaces relevant knowledge so subsequent speckit commands benefit from complete project awareness.

run this skill after `spek prepare` completes its graph check, or invoke it directly at the start of any session on a spekificity-enabled project.

## trigger

```
/spek.prepare
```

## prerequisites

- `spek prepare` has been run (graph check/rebuild complete)
- `vault/` directory exists with `context/` subdirectory
- `.spekificity/config.json` exists (run `spek init` if missing)

## inputs

none required. all paths are read from `.spekificity/config.json`.

## steps

### step 1 — read vault path from config

read `.spekificity/config.json` and extract `vault.path`. use this as the base for all vault file paths:

```
VAULT_PATH = config.vault.path  (default: vault/)
```

if `config.json` is absent or `vault.path` is unset, fall back to `vault/`.

### step 2 — load architectural decisions

read `${VAULT_PATH}/context/decisions.md` in full.

if the file is absent or empty: log `[spek] ⚠ decisions.md not found — no architectural context available` and continue.

### step 3 — load patterns

read `${VAULT_PATH}/context/patterns.md` in full.

if absent or empty: log `[spek] ⚠ patterns.md not found — no pattern context available` and continue.

### step 4 — surface recent lessons

scan `${VAULT_PATH}/lessons/` for the three most recently dated entries (sort by `YYYY-MM-DD` filename prefix, descending). read and summarise each:

- feature slug and date
- one-line summary of what worked well
- one-line summary of decisions made

if `vault/lessons/` is empty or absent: log `[spek] ℹ no lessons entries yet` and continue.

### step 5 — check active workflow state

check if `.spekificity/workflow-state.json` exists and has `status: "in-progress"` or `status: "halted"`.

if active: log `[spek] ℹ active workflow found: <feature_branch> (step: <current_step>)` — this signals the developer that an automate session can be resumed with `spek automate --resume`.

if absent or `status: "complete"`: continue silently.

### step 6 — confirm readiness

output a brief readiness summary:

```
[spek] preparation complete ✓
  decisions:  <N> architectural decisions loaded
  patterns:   <N> patterns loaded
  lessons:    <N> recent entries surfaced
  graph:      <fresh | stale | absent>
  workflow:   <active: feature-name | none>
  ready for feature work.
```

if caveman mode is active, compress this summary.

## outputs

| output | location | description |
|--------|----------|-------------|
| active context | AI working memory | decisions, patterns, lessons held in session |
| readiness summary | terminal | printed confirmation with counts |

## error handling

- **vault entirely absent**: log `[spek] ⚠ vault not found — context unavailable. run 'spek init' then 'spek prepare'.` halt.
- **config.json absent**: fall back to default paths (`vault/`). warn but continue.
- **all vault files empty**: load with message `[spek] ℹ vault is empty — no prior context. ready for first feature.`

## notes

- this skill is read-only. it never modifies any files.
- recommended before every `/speckit.specify` or `/spek.automate` invocation.
- if caveman mode is available, activate it after loading context to keep subsequent session tokens low: `/caveman` or `/caveman lite`.
