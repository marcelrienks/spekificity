# workflow: first-time project initialisation

## purpose

get a developer from zero to a fully operational spekificity-enabled project. after completing this workflow, all tools are installed, all custom skills are active in the ai agent, and the developer can immediately begin a speckit feature lifecycle with graph-aware context.

> **token efficiency tip**: activate `/caveman lite` before starting this workflow to compress ai confirmation messages without losing step accuracy.

## prerequisites

before starting, verify:

| check | command | expected |
|-------|---------|----------|
| python 3.11+ | `python3 --version` | `python 3.11.x` or higher |
| `uv` installed | `uv --version` | any version string |
| `git` installed | `git --version` | any version string |
| ai agent active | (in editor) | github copilot or claude code connected |

if `uv` is not installed:
```bash
curl -lssf https://astral.sh/uv/install.sh | sh
```

---

## step 1 — install speckit/specify (global)

> **idempotency check**: if `specify --version` already returns a version, skip to step 2.

```bash
specify --version 2>/dev/null && echo "already installed — skip to step 2" || \
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

verify:
```bash
specify --version
# expected: specify-cli x.x.x (≥ 0.8.0)
```

see [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for troubleshooting.

---

## step 2 — install graphify (global)

> **idempotency check**: if `graphify --version` already returns a version, skip to step 3.

```bash
graphify --version 2>/dev/null && echo "already installed — skip to step 3" || \
  uv tool install graphifyy
```

verify:
```bash
graphify --version
# expected: graphifyy x.x.x (≥ 0.5.5)
```

see [setup-guides/graphify-setup.md](../setup-guides/graphify-setup.md) for troubleshooting.

---

## step 3 — initialise speckit in your project

> **idempotency check**: if `.specify/` already exists in your project, skip to step 4.

```bash
cd /path/to/your/project

ls .specify/ 2>/dev/null && echo "already initialised — skip to step 4" || specify init .
```

when `specify init .` prompts:
- **ai assistant**: `copilot` (github copilot) or `claude` (claude code)
- **script type**: `sh`

this creates `.specify/`, `.github/agents/`, and `.github/copilot-instructions.md`.

see [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for configuration details.

---

## step 4 — install spekificity custom skills

> **idempotency check**: run the copy commands with `-n` (no-overwrite) to skip existing files, or `-f` to update.

**copy skill library directories into your project**:
```bash
cp -r /path/to/spekificity/skills ./skills
cp -r /path/to/spekificity/workflows ./workflows
cp -r /path/to/spekificity/setup-guides ./setup-guides
```

**for github copilot** — distribute to agent directory:
```bash
mkdir -p .github/agents
cp skills/map-codebase/skill.md .github/agents/map-codebase.agent.md
cp skills/lessons-learnt/skill.md .github/agents/lessons-learnt.agent.md
cp skills/context-load/skill.md .github/agents/context-load.agent.md
cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
```

**for claude code** — distribute to commands directory:
```bash
mkdir -p .claude/commands
cp skills/map-codebase/skill.md .claude/commands/map-codebase.md
cp skills/lessons-learnt/skill.md .claude/commands/lessons-learnt.md
cp skills/context-load/skill.md .claude/commands/context-load.md
cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
```

verify (copilot example):
```bash
ls .github/agents/ | grep -e "map-codebase|lessons|context-load|speckit-enrich"
# expected: 6 files listed
```

---

## step 5 — initialise the vault context structure

> **idempotency check**: if `vault/context/decisions.md` already exists, skip to step 6.

copy the vault context placeholder files:
```bash
cp -r /path/to/spekificity/vault/context ./vault/context
```

or create them manually:
```bash
mkdir -p vault/context vault/lessons vault/graph/nodes
cp /path/to/spekificity/vault/context/decisions.md vault/context/decisions.md
cp /path/to/spekificity/vault/context/patterns.md vault/context/patterns.md
```

---

## step 6 — build the initial codebase map

> **skip if**: your project has fewer than 5 source files or is brand new. return to this step once you have meaningful source files.

in your ai chat session, invoke:
```
/map-codebase
```

the ai will run `graphify . --obsidian --output vault/graph/` and create:
- `vault/graph/index.md` — master node list
- `vault/graph/nodes/` — one file per code/doc node
- `vault/graph/graph_report.md` — human/ai-readable summary

see [workflows/map-refresh.md](map-refresh.md) for when to re-run this step.

---

## step 7 — verify installation

run each of the following checks:

```bash
# tools
specify --version     # ≥ 0.8.0
graphify --version    # ≥ 0.5.5

# speckit
ls .specify/          # extensions.yml  memory/  scripts/  templates/

# spekificity skills (choose your agent)
ls .github/agents/    # should include map-codebase.agent.md etc.
ls .claude/commands/  # should include map-codebase.md etc.

# vault
ls vault/             # graph/  lessons/  context/
ls vault/context/     # decisions.md  patterns.md
```

in your ai chat session, verify the agent can read the skill:
```
/context-load
# expected: "context loaded. x graph nodes, y decisions, z patterns. ready."
```

---

## step 8 — next steps

installation complete. your enriched speckit workflow is ready:

```
/context-load                      ← load vault context (run at start of every session)
/speckit-enrich-specify            ← start a new feature (graph-aware spec)
/speckit-enrich-plan               ← plan the feature (graph-aware plan)
/speckit.tasks                     ← generate tasks (standard speckit)
/speckit-enrich-implement          ← implement + auto-update vault + lessons
```

see [workflows/feature-lifecycle.md](feature-lifecycle.md) for the full enriched workflow.

---

## decision points

| situation | action |
|-----------|--------|
| `specify --version` already ≥ 0.8.0 | skip step 1 |
| `graphify --version` already ≥ 0.5.5 | skip step 2 |
| `.specify/` already exists | skip step 3 |
| skill files already in `.github/agents/` | skip/update step 4 |
| project has no source files yet | skip step 6; run `/map-codebase` later |
| using claude code only | skip copilot copy commands in step 4 |
| using github copilot only | skip claude copy commands in step 4 |

## recovery from partial failures

- **failure in step 1–2 (install)**: re-run the install command; `uv tool install` is idempotent
- **failure in step 3 (specify init)**: run `specify init .` again; it will not overwrite your constitution
- **failure in step 4 (skill copy)**: re-run the `cp` commands; use `-f` to overwrite stale copies
- **failure in step 6 (map-codebase)**: check `graphify --version` first; see error handling in [skills/map-codebase/skill.md](../skills/map-codebase/skill.md)
