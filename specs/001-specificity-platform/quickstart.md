# quickstart: spekificity platform

**date**: 2026-04-29  
**time to complete**: ~20–30 minutes (first-time setup)

this guide gets you from zero to a running spekificity-enabled project. follow the steps in order. each step is executable by an ai agent or a developer in a terminal.

---

## prerequisites

before starting, ensure the following are available:

| tool | install command | verify |
|------|----------------|--------|
| python 3.11+ | [python.org](https://python.org) | `python3 --version` |
| `uv` (python package runner) | `curl -lssf https://astral.sh/uv/install.sh \| sh` | `uv --version` |
| git | os package manager | `git --version` |
| github copilot or claude code | ai provider setup | active in your editor |

---

## step 1 — install speckit/specify (global)

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

verify:
```bash
specify --version
# expected: specify-cli x.x.x
```

see [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for troubleshooting.

---

## step 2 — install graphify (global)

```bash
uv tool install graphifyy
```

verify:
```bash
graphify --version
# expected: graphifyy x.x.x
```

see [setup-guides/graphify-setup.md](../setup-guides/graphify-setup.md) for troubleshooting.

---

## step 3 — initialise your project with specify

inside your project folder:

```bash
cd /path/to/your/project
specify init .
```

when prompted, select:
- ai assistant: `copilot` or `claude`
- script type: `sh`

this installs the standard speckit workflow into `.github/agents/` and `.specify/`.

---

## step 4 — install spekificity custom skills

clone or copy the spekificity `skills/` and `workflows/` directories into your project:

```bash
# if using spekificity as a reference repo:
cp -r /path/to/spekificity/skills ./skills
cp -r /path/to/spekificity/workflows ./workflows
cp -r /path/to/spekificity/setup-guides ./setup-guides
```

for github copilot — copy skills to agent directory:
```bash
cp skills/map-codebase/skill.md .github/agents/map-codebase.agent.md
cp skills/lessons-learnt/skill.md .github/agents/lessons-learnt.agent.md
cp skills/context-load/skill.md .github/agents/context-load.agent.md
cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
```

for claude code — copy skills to commands directory:
```bash
mkdir -p .claude/commands
cp skills/map-codebase/skill.md .claude/commands/map-codebase.md
cp skills/lessons-learnt/skill.md .claude/commands/lessons-learnt.md
cp skills/context-load/skill.md .claude/commands/context-load.md
cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
```

---

## step 5 — build the initial codebase map

in your ai chat session:

```
/map-codebase
```

the ai will run `graphify . --obsidian --output vault/graph/` and create:
- `vault/graph/index.md`
- `vault/graph/nodes/*.md`
- `vault/graph/graph_report.md`

for a brand-new empty project, skip this step — return to it once you have source files.

---

## step 6 — start a feature lifecycle

your enriched speckit workflow is ready. use these commands in order:

```
/context-load                      ← load vault context into ai session
/speckit-enrich-specify            ← write spec (graph-aware)
/speckit-enrich-plan               ← write plan (graph-aware)
/speckit.tasks                     ← generate tasks (standard speckit)
/speckit-enrich-implement          ← implement + auto-update vault
```

or use standard speckit commands directly — spekificity is additive:
```
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
```

---

## step 7 — reduce tokens with caveman

at any point in a session, activate caveman mode:
```
/caveman
```

for workflow steps that require structured output (specs, plans), use lite mode to avoid over-compression:
```
/caveman lite
```

---

## updating components independently

| component | update command | spekificity changes needed |
|-----------|---------------|---------------------------|
| speckit | `uv tool upgrade specify-cli` | none (unless speckit command interface changed) |
| graphify | `uv tool upgrade graphifyy` | update `skills/map-codebase/skill.md` if cli args changed |
| obsidian app | download from obsidian.md | none (vault is plain markdown) |
| spekificity skills | `git pull` in spekificity repo → re-copy skills | run step 4 again |

---

## obsidian app (optional)

obsidian is **not required** for the spekificity workflow. the vault is plain markdown — ai agents read it directly.

if you want a visual graph browser:
1. download obsidian from [obsidian.md](https://obsidian.md)
2. open obsidian → open folder as vault → select your project's `vault/` directory
3. use the graph view to visualise node relationships

see [setup-guides/obsidian-setup.md](../setup-guides/obsidian-setup.md) for details.
