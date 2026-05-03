# contract: spek cli sub-command interface

**feature**: `003-spek-full-workflow-cli`
**version**: 1.0
**date**: 2026-05-03

---

## overview

this contract defines the public interface of the `spek` cli — its sub-commands, accepted arguments, outputs, and exit codes. any change to this interface constitutes a breaking change and requires a version bump.

---

## entry point

```
spek <command> [arguments] [flags]
```

`spek` is a single bash executable at `bin/spek`. it routes to dedicated implementation scripts in `.spekificity/bin/`.

---

## sub-commands

### `spek setup`

**purpose**: detect and install all required and optional prerequisites.

**invocation**:
```
spek setup [--dry-run] [--skip-optional]
```

**flags**:
| flag | description |
|------|-------------|
| `--dry-run` | detect tools but do not install anything; report status only |
| `--skip-optional` | skip optional tool installation; install required tools only |

**output format**:
```
[spek] checking prerequisites...
[spek] ✓ python3 3.11.9 — ok
[spek] ✓ uv 0.4.18 — ok
[spek] ✗ specify — not found, installing...
[speckit] <specify installer output>
[spek] ✓ specify 0.8.0 — installed
[spek] ⚠ obsidian — manual install required: https://obsidian.md
[spek] setup complete. required tools: 4/4 ✓ | optional tools: 2/3 (obsidian pending)
[spek] run: spek init
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | all required tools installed successfully |
| 1 | one or more required tools could not be installed |
| 0 | optional tools missing (warning only, not failure) |

**post-condition**: writes tool status to `.spekificity/config.json` (`tools.*` fields).

---

### `spek init`

**purpose**: orchestrate initialisation of all underlying tools in sequence.

**invocation**:
```
spek init [--force]
```

**flags**:
| flag | description |
|------|-------------|
| `--force` | re-run all init steps even if already initialised (overrides idempotency check) |

**output format**:
```
[spek] initialising spekificity platform...
[spek] checking prerequisites... ✓
[speckit] <specify init output>
[spek] speckit initialised ✓
[graphify] <graphify setup output>
[spek] graphify configured ✓
[spek] obsidian vault structure created ✓
[spek] installing skills...
[spek]   ✓ spek.context-load
[spek]   ✓ spek.map-codebase
[spek]   ✓ spek.lessons-learnt
[spek]   ✓ spek.prepare
[spek]   ✓ spek.automate
[spek]   ✓ spek.post
[spek] skill index updated ✓
[spek] init complete. run: spek status
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | all init steps succeeded |
| 1 | a required tool is not installed (setup must be run first) |
| 2 | a non-recoverable init step failed (details in output) |

**idempotency**: each step checks current state before acting. re-running `spek init` on an already-initialised project completes in < 30 seconds with no destructive actions.

**post-condition**: `.spekificity/config.json` reflects `initialized_at` and all tool statuses. `.spekificity/skill-index.md` is created/updated.

---

### `spek prepare`

**purpose**: prime the ai session with current project context before any feature workflow.

**invocation**:
```
spek prepare [--force-refresh]
```

**flags**:
| flag | description |
|------|-------------|
| `--force-refresh` | force graph rebuild even if graph is fresh |

**output format**:
```
[spek] starting preparation phase...
[spek] checking graph state... stale (last commit: 2026-05-03 14:32, graph: 2026-05-02 09:15)
[graphify] refreshing graph...
[spek] graph refreshed ✓
[spek] loading vault context...
[spek] surfacing recent lessons...
[spek] preparation complete. ai session is ready for feature work.
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | preparation complete |
| 1 | platform not initialised (spek init must be run first) |

**note**: `spek prepare` is a thin shell wrapper that triggers the ai to read and execute `/spek.prepare` skill. the actual preparation logic is in the skill.

---

### `spek automate "<feature description>"`

**purpose**: autonomously execute the full speckit feature lifecycle for the given description.

**invocation**:
```
spek automate "<feature description>" [--skip-preflight] [--no-pr]
spek automate --resume
```

**arguments**:
| argument | description |
|----------|-------------|
| `"<feature description>"` | natural-language feature description passed to speckit spec step |

**flags**:
| flag | description |
|------|-------------|
| `--skip-preflight` | skip branch creation and working tree check (for use when branch already exists) |
| `--no-pr` | skip pr creation at post-flight |
| `--resume` | resume from last saved workflow state (no feature description needed) |

**output format**:
```
[spek] starting automated feature lifecycle...
[spek] preflight: checking working tree... ✓ clean
[spek] preflight: creating branch 003-add-user-login... ✓
[spek] --- step 1/6: spec ---
[speckit] <speckit specify output>
[spek] spec complete ✓ (specs/003-add-user-login/spec.md)
[spek] --- step 2/6: plan ---
...
[spek] ❓ question for you: <question from speckit>
> <developer answer>
[spek] answer recorded. continuing...
...
[spek] post-flight: writing lessons learnt...
[spek] post-flight: refreshing graph...
[spek] post-flight: creating pull request...
[spek] PR created: https://github.com/org/repo/pull/42
[spek] automate complete ✓
```

**interactive qa format**:
```
[spek] ❓ speckit needs clarification (step: plan)
[spek] question: <question text>
> 
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | full lifecycle completed, pr created (or skipped with --no-pr) |
| 1 | platform not initialised |
| 2 | preflight failed (uncommitted changes, branch conflict) |
| 3 | unrecoverable error mid-workflow (state saved, resume available) |

**post-condition**: workflow-state.json written after each step. on exit code 3, `status: "halted"` is set.

---

### `spek post`

**purpose**: execute post-implementation tasks after manual or automated feature completion.

**invocation**:
```
spek post [--no-lessons] [--no-graph]
```

**flags**:
| flag | description |
|------|-------------|
| `--no-lessons` | skip lessons learnt capture |
| `--no-graph` | skip graph refresh |

**output format**:
```
[spek] running post-implementation tasks...
[spek] invoking lessons learnt skill...
[spek] graph refresh (incremental)...
[graphify] <incremental refresh output>
[spek] post tasks complete ✓
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | all post tasks completed |
| 1 | platform not initialised |

---

### `spek status`

**purpose**: display current platform state — init status, installed skills, tool versions, vault currency.

**invocation**:
```
spek status [--json]
```

**flags**:
| flag | description |
|------|-------------|
| `--json` | output as json (for scripting) |

**output format**:
```
[spek] platform status
  spekificity: v0.3.0
  initialized: 2026-05-01 10:00
  tools:
    speckit 0.8.0 ✓
    graphify 1.2.3 ✓
    gh 2.47.0 (authenticated) ✓
    obsidian — manual install pending ⚠
  skills: 6 active
  vault: vault/graph/index.md — fresh (last updated: 2026-05-03 14:00)
  active workflow: none
```

**exit codes**:
| code | condition |
|------|-----------|
| 0 | status displayed |
| 1 | platform not initialised |

---

### `spek update`

**purpose**: update the spekificity custom layer (scripts, skills, workflows) without touching underlying tool configuration.

**invocation**:
```
spek update [--check]
```

**flags**:
| flag | description |
|------|-------------|
| `--check` | report available updates without applying them |

**exit codes**:
| code | condition |
|------|-----------|
| 0 | update applied successfully |
| 1 | update failed (details in output) |
| 0 | already on latest version |

---

## output conventions (fr-020)

all `spek` output is prefixed to distinguish source:

| prefix | source |
|--------|--------|
| `[spek]` | spek orchestration layer |
| `[speckit]` | output from speckit/specify |
| `[graphify]` | output from graphify |
| `[obsidian]` | vault write operations |

interactive prompts use `>` as the input prompt. questions from speckit are prefixed with `[spek] ❓`.

---

## breaking change policy

changes to this contract that affect existing users:
- adding a required argument to an existing sub-command
- changing exit code meanings
- removing a sub-command
- changing the `workflow-state.json` schema in a backwards-incompatible way

changes that are not breaking:
- adding new optional flags
- adding new sub-commands
- adding new output lines (as long as existing lines are preserved)
