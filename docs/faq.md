# troubleshooting & faq

**version**: 1.0 | **last updated**: 2026-04-30

---

## setup phase

### q: `specify --version` fails after install

**problem**: speckit/specify installed but not on path.

**solution**:
```bash
# option 1: use full path
uv tool run specify --version

# option 2: ensure ~/.local/bin is on path
export path="$home/.local/bin:$path"
echo $path | grep ".local/bin"
```

see [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md#troubleshooting).

---

### q: `graphify --version` fails after install

**problem**: graphify installed but not on path, or python 3.11+ not found.

**solution**:
```bash
# verify python
python3 --version  # should be 3.11+

# use full path
uv tool run graphifyy --version

# or ensure path includes uv tools
export path="$home/.local/bin:$path"
```

see [setup-guides/graphify-setup.md](../setup-guides/graphify-setup.md#troubleshooting).

---

### q: `specify init .` fails

**problem**: speckit initialization error, usually due to missing python or conflicting git setup.

**solution**:
```bash
# verify prerequisites
python3 --version
git --version
which git

# try again
specify init .
```

if git complains about name/email:
```bash
git config user.name "your name"
git config user.email "your.email@example.com"
specify init .
```

---

## vault & mapping phase

### q: `/map-codebase` fails or produces empty graph

**problem**: graphify not installed, or project has no recognized source files.

**solution**:
```bash
# verify graphify
graphify --version

# check project has source files
find . -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.md" | head

# run with verbose output
graphify . --obsidian --output vault/graph/ -v
```

if vault is still empty: graphify requires at least 1 source file. add a simple test file and retry.

---

### q: vault directory is very large (>500 nodes)

**problem**: `vault/graph/` adds bulk to git repo.

**solution**: add to `.gitignore`:
```bash
echo "vault/graph/" >> .gitignore
echo "vault/lessons/" >> .gitignore  # optional — lessons are smaller
```

vault remains local; ai can still read it.

---

### q: how do i refresh the vault after adding new files?

**solution**:
```bash
/map-codebase
```

or see [workflows/map-refresh.md](../workflows/map-refresh.md) for when/how to refresh.

---

## speckit workflow phase

### q: `/context-load` returns empty summary

**problem**: vault exists but has no prior graph or lessons entries.

**solution**: this is expected on first run. proceed to `/speckit-enrich-specify`. after your first feature completes, run `/lessons-learnt` and subsequent `/context-load` calls will be richer.

---

### q: `/speckit-enrich-specify` fails or runs vanilla `/speckit.specify`

**problem**: enrichment failed, but fallback to vanilla speckit succeeded.

**solution**: check that vault is mapped:
```bash
ls vault/graph/index.md
```

if missing, run `/map-codebase` first, then retry `/speckit-enrich-specify`.

---

### q: tasks don't match my spec/plan

**problem**: speckit generated tasks but they seem incomplete or out of order.

**solution**:
1. review spec.md for clarity — vague requirements produce vague tasks
2. review plan.md — tasks should map to plan phases
3. run `/speckit.tasks` directly (not enrich version) to see raw output
4. manually edit `tasks.md` if needed — it's a template, not locked

see [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md#recovery-instructions).

---

### q: where should i store obsidian vault — in git or local-only?

**problem**: unclear whether to commit `vault/graph/` and `vault/lessons/`.

**solution**:
- **`vault/graph/`** (graphify output): usually `.gitignore` for large projects. small projects can commit.
- **`vault/lessons/`** (lessons learnt): commit — these are valuable project memory.
- **`vault/context/`** (decisions, patterns): commit — team should see these.

example `.gitignore`:
```
vault/graph/  # large; regenerate on demand with /map-codebase
# vault/lessons and vault/context stay committed
```

---

## skill errors

### q: ai says "skill not found" for `/context-load` etc.

**problem**: skill files not installed in correct location.

**solution**: check installation location:

**github copilot**:
```bash
ls .github/agents/ | grep -e "context-load|map-codebase|lessons-learnt"
```

should list: `context-load.agent.md`, `map-codebase.agent.md`, `lessons-learnt.agent.md`, etc.

**claude code**:
```bash
ls .claude/commands/ | grep -e "context-load|map-codebase|lessons-learnt"
```

should list: `context-load.md`, `map-codebase.md`, `lessons-learnt.md`, etc.

if missing: re-run `workflows/init-workflow.md` step 3 (copy skill files).

---

### q: skill produces incorrect output

**problem**: skill runs but output is wrong (e.g., graph nodes are missing, lessons not written).

**solution**: check error handling:
1. verify prerequisites (vault exists, files readable)
2. check ai session logs for error messages
3. review the skill file [skills/](../skills/) for prerequisites section
4. run skill again with verbose output if available

if persistent: open a github issue with:
- skill name
- exact command run
- error message
- presence/absence of vault

---

## token efficiency

### q: how do i reduce token usage in long sessions?

**solution**: use caveman mode:
```
/caveman lite    # for specs/plans (preserves structure)
/caveman         # for implementation (full compression)
```

see [workflows/feature-lifecycle.md#token-efficiency](../workflows/feature-lifecycle.md#token-efficiency).

---

### q: caveman mode makes output too terse

**solution**: use `/caveman lite` instead of `/caveman` (full):
```
/caveman lite  ← structured, readable
/caveman       ← ultra-compressed (for long sessions)
```

or temporarily disable:
```
stop caveman
# or
normal mode
```

---

## component updates

### q: how do i update speckit without breaking spekificity?

**solution**: spekificity is designed to be independent. update speckit with:
```bash
uv tool upgrade specify-cli
```

spekificity custom skills continue to work. only if speckit command interface changed (rare) will you need to update the adapter skills.

see [workflows/component-update.md](../workflows/component-update.md).

---

### q: can i use spekificity with different ai agents (not copilot/claude)?

**problem**: spekificity v1 supports only github copilot and claude code.

**solution**: skills are written in plain markdown + instructions. they can be adapted for other agents (v2 work). see [docs/glossary.md](../docs/glossary.md) for agent definitions.

---

## general

### q: what if i get stuck?

**solution**:
1. re-read the relevant workflow doc: [workflows/feature-lifecycle.md](../workflows/feature-lifecycle.md) or [workflows/init-workflow.md](../workflows/init-workflow.md)
2. check recovery instructions at the end of each workflow
3. verify vault exists: `ls vault/context/`
4. try `/context-load` to refresh ai session state
5. open a github issue with the specific error

---

### q: is obsidian desktop app required?

**answer**: no. obsidian vault is plain markdown. ai agents can read/write without the app. the desktop app is optional for visual exploration and notes.

see [setup-guides/obsidian-setup.md](../setup-guides/obsidian-setup.md).

---

### q: can i use spekificity on windows?

**problem**: spekificity v1 targets macos and linux (bash-based).

**solution**: windows users can:
- use wsl2 (windows subsystem for linux) — then follow macos/linux steps
- use git bash or similar — some scripts may need adaptation
- contribute windows support for v2

see [docs/glossary.md](../docs/glossary.md) under "operating constraints".

---

## still stuck?

open an issue on [github](https://github.com/marcelrienks/spekificity/issues) with:
- your os + shell
- which step/skill you're on
- exact error message or unexpected output
- vault state (does it exist? what's in it?)
