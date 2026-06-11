# Implementation Plan: Full Platform Implementation

**Branch**: `003-full-platform-impl` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-full-platform-impl/spec.md`

## Summary

Implement the complete Spekificity platform in four phases. Each phase has a distinct type of work and a clean review gate before the next begins.

| Phase | What | Deliverable |
|-------|------|-------------|
| **P1: Foundation** | Package infrastructure | `pyproject.toml` updates, `utils.py`, `prerequisites.py` |
| **P2: Integration modules** | Three independent Python modules + unit tests | `lat_md/`, `vault/`, `speckit/` |
| **P3: Skill files** | Markdown authoring + distribution logic | 7 `.md` files in `spekificity/skills/`, `skills_install/` module |
| **P4: CLI** | Orchestration + integration test | `cli.py`, `test_init_flow.py` |

P1 must land first — it provides shared utilities and unblocks testing of P2–P4. P2 modules are parallel within their phase (no dependencies between lat_md, vault, speckit). P3 can be authored in parallel with P2. P4 depends on all prior phases.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `click>=8.0` (CLI framework), `shutil` (file copy), `importlib.resources` (package data access), `subprocess` (external tool invocation), `pathlib` (path handling), `json` (MCP config read/write); config write uses inline YAML string — no PyYAML dep needed

**Storage**: Filesystem only — `.spek/` directory tree, per-integration MCP config files, `.git/hooks/post-commit`, `.spek/config.yaml`

**Testing**: pytest; `tmp_path` fixture for isolated filesystem tests; `unittest.mock.patch` for subprocess mocking

**Target Platform**: macOS, Windows, Linux (cross-platform CLI)

**Project Type**: CLI tool / Python package (installable via `uv tool install`)

**Performance Goals**: `spek init` completes in under 5 minutes on a clean project (most time is 3rd-party tool install); no latency requirements on skill file reads

**Constraints**: Python 3.11+ only; requires `uv` and `git` in PATH before running; no sudo; must be idempotent

**Scale/Scope**: Single-developer CLI tool; no concurrency; ~7 skill files + ~12 Python modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Development | ✅ PASS | Spec exists, reviewed, and approved |
| II. Token Efficiency | ✅ PASS | Skill files use Caveman; lat.md pre-index avoids file scanning |
| III. Deterministic 4-Stage Workflow | ✅ PASS | Following Prepare → Plan → Implement → Conclude |
| IV. Persistent Memory | ✅ PASS | Plan archived to `.spek/vault/` on conclude |
| V. Simplicity & Composability | ✅ PASS | CLI does one thing; skill files are independent markdown |

All gates pass. No complexity violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/003-full-platform-impl/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   ├── cli-contract.md
│   ├── config-schema.md
│   └── mcp-config-schemas.md
└── tasks.md             # /speckit-tasks output — not created here
```

### Source Code (repository root)

```text
spekificity/
├── __init__.py
│
├── utils.py                        # P1: shared subprocess runner + [OK]/[SKIP]/[WARN]/[ERROR] formatter
├── prerequisites.py                # P1: verify Python 3.11+, uv, Node.js 22+, git in PATH
│
├── lat_md/                         # P2: lat.md integration module
│   ├── __init__.py
│   ├── install.py                  # detect/install lat.md via npm
│   ├── index.py                    # lat init (code) + lat init --docs (doc)
│   ├── mcp_config.py               # write lat MCP entry per integration, merge-safe
│   └── git_hook.py                 # write .git/hooks/post-commit (lat update)
│
├── vault/                          # P2: Obsidian vault module
│   ├── __init__.py
│   ├── install.py                  # detect/install Obsidian (brew/winget/URL); two-phase halt
│   ├── scaffold.py                 # mkdir .spek/vault/, lessons/, memory/, lat/; write decisions.md, patterns.md
│   └── init.py                     # obsidian open-vault; obsidian create initial files
│
├── speckit/                        # P2: SpecKit module
│   ├── __init__.py
│   ├── install.py                  # detect/install specify-cli via uv tool install
│   ├── init.py                     # run specify init
│   └── config.py                   # write .spek/config.yaml
│
├── skills_install/                 # P3: skill file distribution
│   ├── __init__.py
│   ├── integrations.py             # integration → (skills_dir, flat|subfolder) mapping + MCP config mapping
│   └── copy.py                     # copy spekificity/skills/ → target dir; idempotent (never overwrite)
│
├── skills/                         # P3: bundled agent skill files (package data)
│   ├── spek-prepare.md
│   ├── spek-plan.md
│   ├── spek-implement.md
│   ├── spek-conclude.md
│   ├── spek-lessons.md
│   ├── spek-context.md
│   └── spek-map.md
│
└── cli.py                          # P4: spek init command; orchestrates P1–P3 modules

tests/
├── unit/
│   ├── test_prerequisites.py       # P1
│   ├── test_utils.py               # P1
│   ├── lat_md/
│   │   ├── test_install.py         # P2
│   │   ├── test_index.py           # P2
│   │   ├── test_mcp_config.py      # P2
│   │   └── test_git_hook.py        # P2
│   ├── vault/
│   │   ├── test_install.py         # P2
│   │   ├── test_scaffold.py        # P2
│   │   └── test_init.py            # P2
│   ├── speckit/
│   │   ├── test_install.py         # P2
│   │   ├── test_init.py            # P2
│   │   └── test_config.py          # P2
│   └── skills_install/
│       ├── test_integrations.py    # P3
│       └── test_copy.py            # P3
└── integration/
    └── test_init_flow.py           # P4: full end-to-end spek init

pyproject.toml                      # P1: add pytest dev dep, package-data for skills/*.md
```

**Structure Decision**: Single project layout. Modules grouped by phase. `vault/scaffold.py` also owns `.spek/memory/` and `.spek/lat/` directory creation (all `.spek/` subdirs in one place). `skills_install/` is separate from `skills/` — content and distribution are different concerns. `cli.py` is intentionally thin: it reads flags/prompts, calls each module in order, and handles the exit code. No business logic in `cli.py`.

## P5: Gap Fixes (post-review)

Three gaps found in implementation review. All are self-contained fixes.

| Gap | File | Fix |
|-----|------|-----|
| FR-002: No version validation | `spekificity/prerequisites.py` | Parse `python --version` / `node --version` output; extract major.minor; `sys.exit(1)` if Python < 3.11 or Node < 22 |
| FR-011/SC-006: Wrong halt text | `spekificity/vault/install.py` | Replace `_print_registration_instructions()` body with verbatim text from `wiki/setup.md` "Phase 1 halt" block |
| FR-020: Wrong skill section headers | `spekificity/skills/*.md` (all 7) | Rewrite each file to use `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria` in that order |

**Version parsing approach** (FR-002):
```python
import re, sys as _sys

def _check_version(cmd: str, min_major: int, min_minor: int) -> bool:
    raw = _get_version(cmd) or ""
    m = re.search(r"(\d+)\.(\d+)", raw)
    if not m:
        return False
    return (int(m.group(1)), int(m.group(2))) >= (min_major, min_minor)
```
Python check: `python --version` → parse `3.X.Y` → require `(3, 11)`.
Node check: `node --version` → parse `vX.Y.Z` → require `(22, 0)`.
`uv` and `git`: PATH presence only, no version constraint.

## P6: Gap Fixes (analysis-review)

Two bugs found in code correctness audit. Both self-contained fixes.

| Gap | File(s) | Fix |
|-----|---------|-----|
| Linux vault crash | `spekificity/cli.py` | `init_vault()` called when `obsidian_result.status == "skipped"` (Linux path) → `RuntimeError` since `obsidian` not in PATH. Add `elif status == "skipped"` guard before `else: init_vault()`. Spec edge case: "Linux → continue remaining steps without vault setup." |
| Cline MCP flat key | `spekificity/lat_md/mcp_config.py`, `spekificity/skills_install/integrations.py` | `servers_key="cline.mcpServers"` fed into `split(".")` navigation writes nested `{"cline": {"mcpServers": {...}}}`. VS Code `settings.json` requires literal flat key `{"cline.mcpServers": {...}}`. Fix: bypass split-navigation for flat-key integrations; add a test covering the cline case. |

**Linux vault guard** (`spekificity/cli.py`):
```python
obsidian_result = install_obsidian()
scaffold_vault(project_path)
needs_exit_2 = False
if obsidian_result.status == "needs_user_action":
    needs_exit_2 = True
    print_status("SKIP", "Obsidian CLI not registered — skipping vault init; register CLI and re-run spek init")
elif obsidian_result.status == "skipped":
    print_status("SKIP", "vault init skipped (Linux — Obsidian not available)")
else:
    init_vault(project_path)
```

**Cline flat-key fix** (`spekificity/lat_md/mcp_config.py`):

Two options; pick one:

*Option A* — Add `flat_key: bool` field to `INTEGRATION_MCP_CONFIG` tuples; when `True`, use `config.setdefault(servers_key, {})` directly without `split(".")`:
```python
# integrations.py
"cline": (".vscode/settings.json", "cline.mcpServers", {}, True),  # flat_key=True

# mcp_config.py
def write_mcp_config(config_path, servers_key, extra_fields, integration, flat_key=False):
    ...
    if flat_key:
        servers = config.setdefault(servers_key, {})
    else:
        keys = servers_key.split(".")
        node = config
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        servers = node.setdefault(keys[-1], {})
```

*Option B* — Keep tuple shape; special-case only `cline` in `write_mcp_config` by checking if `integration == "cline"`.

Option A preferred — generalises cleanly if other integrations need flat keys.

New test required (`tests/unit/lat_md/test_mcp_config.py`):
```python
def test_cline_writes_flat_key(self, tmp_path):
    config_path = tmp_path / ".vscode" / "settings.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_mcp_config(config_path, "cline.mcpServers", {}, "cline", flat_key=True)
    data = json.loads(config_path.read_text())
    assert "cline.mcpServers" in data          # flat key, not nested
    assert "cline" not in data                 # no nested {"cline": {...}}
    assert "lat" in data["cline.mcpServers"]
```

## P7: Gap Fixes (wiki-compliance audit)

Five gaps found comparing code against `wiki/setup.md`, `wiki/architecture.md`, and `wiki/skills.md`. I1 and I2 are HIGH — block correct SpecKit integration. I3–I5 are MEDIUM.

| ID | Gap | File(s) | Fix |
|----|-----|---------|-----|
| I1 | `specify init` missing `--integration` flag | `spekificity/speckit/init.py`, `spekificity/speckit/config.py`, `spekificity/cli.py` | Thread `integration: str` param into `run_specify_init(project_path, integration)`; call `["specify", "init", "--integration", integration]`. Update `tests/unit/speckit/test_init.py` to assert `--integration` in command. |
| I2 | `specify-cli` installed without `--from git+...` | `spekificity/speckit/install.py` | Add `"--from", "git+https://github.com/github/spec-kit.git"` to install command. Update `tests/unit/speckit/test_install.py` to assert full command. |
| I3 | No git repo validity check | `spekificity/prerequisites.py` | After `git` PATH check, run `git rev-parse --git-dir`; if non-zero exit, print `[ERROR] Not in a git repository. Run git init first.` and `sys.exit(1)`. Add test for this case. |
| I4 | `obsidian open-vault` wrong arg format | `spekificity/vault/init.py` | Change `["obsidian", "open-vault", str(vault_path)]` to `["obsidian", "open-vault", f"path={vault_path}"]` per `wiki/setup.md`. Update unit test. |
| I5 | Initial vault files created via filesystem, not Obsidian CLI | `spekificity/vault/scaffold.py`, `spekificity/vault/init.py` | Move `decisions.md`, `patterns.md`, `lessons/.keep` creation from `scaffold_vault` into `init_vault` (Phase 2 — when obsidian is in PATH). Use `obsidian create` CLI commands instead of `path.write_text`. `scaffold_vault` still creates dirs only. |

**I1 — `run_specify_init` signature change:**
```python
# speckit/init.py
def run_specify_init(project_path: Path, integration: str) -> None:
    specify_dir = project_path / ".specify"
    if specify_dir.exists():
        print_status("SKIP", ".specify/ already exists — skipping specify init")
        return
    run_command(["specify", "init", "--integration", integration], "specify init")
    print_status("OK", "SpecKit initialized (.specify/)")

# cli.py — update call site:
run_specify_init(project_path, integration)
```

**I2 — speckit install command:**
```python
# speckit/install.py
run_command(
    ["uv", "tool", "install", "specify-cli", "--from", "git+https://github.com/github/spec-kit.git"],
    "install specify-cli via uv",
)
```

**I3 — git repo check in prerequisites:**
```python
# prerequisites.py — add after git PATH check, before returning results:
import subprocess as _sp
try:
    _sp.run(["git", "rev-parse", "--git-dir"], check=True, capture_output=True)
except _sp.CalledProcessError:
    print("[ERROR] Not in a git repository. Run: git init")
    sys.exit(1)
```
Add this check at the END of `check_prerequisites()` after all tool checks pass, so it only runs when `git` is confirmed in PATH.

**I4 — obsidian open-vault named arg:**
```python
# vault/init.py
run_command(["obsidian", "open-vault", f"path={vault_path}"], "obsidian open-vault")
```

**I5 — move initial file creation into init_vault:**
```python
# vault/scaffold.py — create dirs only:
dirs = [
    project_path / ".spek" / "vault" / "lessons",
    project_path / ".spek" / "memory",
    project_path / ".spek" / "lat",
]
# No file writes in scaffold_vault

# vault/init.py — add file creation via Obsidian CLI after open-vault:
_FILES = [
    ("file=decisions", "content=# Decisions"),
    ("file=patterns",  "content=# Patterns"),
    ("path=lessons/.keep", "content="),
]
for file_arg, content_arg in _FILES:
    dest = ...  # derive expected path from file_arg
    if not dest.exists():
        run_command(
            ["obsidian", "create", file_arg, content_arg, "vault=vault"],
            f"obsidian create {file_arg}",
        )
```
Update tests: `test_scaffold.py` asserts dirs created, no files; `test_init.py` asserts `obsidian create` called for each missing file.

**Execution order:** I2 is independent. I1 requires threading `integration` param through call chain (init.py + cli.py). I3 adds one check to prerequisites.py. I4 is one-line. I5 reshuffles scaffold/init responsibilities — largest change but bounded to two files.

## P8: Auto-Tagging & Auto-Wikilink Insertion

Gap from decision.md: documented as "enabled by default in `/spek.conclude` lesson generation step" — no code existed. This phase closes that gap.

### New Module: `spekificity/vault/autolink.py`

```python
@dataclass
class AutolinkResult:
    links_inserted: int = 0
    tags_added: list[str] = field(default_factory=list)
    skipped: bool = False

_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "it",
    "its", "this", "that", "these", "those", "we", "i", "you", "he",
    "she", "they", "my", "your", "our", "their", "not", "no", "if",
    "then", "when", "so", "there", "here",
})

def _build_vault_index(vault_path: Path) -> dict[str, Path]:
    # key = normalized stem (lowercase, hyphens → spaces)
    # scans .spek/vault/ recursively for .md files

def _extract_keywords(text: str) -> list[str]:
    # strip markdown syntax, split into words/phrases
    # remove stopwords, deduplicate, return list

def _match_keywords(
    keywords: list[str],
    vault_index: dict[str, Path],
    threshold: float,
) -> list[tuple[str, Path]]:
    # SequenceMatcher ratio comparison per keyword vs each vault key
    # return (keyword, vault_path) pairs where ratio >= threshold

def _insert_wikilinks(text: str, matches: list[tuple[str, Path]]) -> tuple[str, int]:
    # for each match: replace bare keyword (not inside [[...]]) with [[keyword]]
    # returns (updated_text, count_inserted)

def _add_frontmatter_tags(text: str, tags: list[str]) -> str:
    # if YAML block exists (--- lines): merge tags list
    # if absent: prepend ---\ntags: [t1, t2]\n---\n
    # no-op if tags list empty

def process_lesson(
    lesson_path: Path,
    vault_path: Path,
    config: dict,
) -> AutolinkResult:
    autolink_cfg = config.get("autolink", {})
    if not autolink_cfg.get("enabled", True):
        print_status("SKIP", "autolink disabled in config")
        return AutolinkResult(skipped=True)
    threshold = autolink_cfg.get("threshold", 0.8)
    keyword_tags = autolink_cfg.get("keyword_tags", {})
    # orchestrate: read lesson → extract → match → insert → tag → write
```

**Dependencies:** `re`, `difflib.SequenceMatcher`, `pathlib` — stdlib only. No external NLP deps.

### Updates to Existing Files

| File | Change |
|------|--------|
| `spekificity/speckit/config.py` | Add `autolink` block to YAML template: `enabled: true`, `threshold: 0.8`, `keyword_tags: {}` |
| `spekificity/skills/spek-lessons.md` | Add Step 5: run `process_lesson()` on lesson file; add `[[wikilinks]] inserted` and `tags generated` to Exit Criteria |
| `spekificity/skills/spek-conclude.md` | Update Step 2 note to state autolink runs automatically inside `/spek.lessons` |

### New Test File: `tests/unit/vault/test_autolink.py`

Cover: `_build_vault_index` (correct stems), `_extract_keywords` (stopword removal), `_match_keywords` (above/below threshold), `_insert_wikilinks` (bare vs already-linked), `_add_frontmatter_tags` (create/merge), `process_lesson` (skip-if-disabled, idempotency, links count).

### Source Code Changes

```text
spekificity/
└── vault/
    └── autolink.py                   # P8: new module

tests/
└── unit/
    └── vault/
        └── test_autolink.py          # P8: new test file
```

Plus edits to `speckit/config.py`, `skills/spek-lessons.md`, `skills/spek-conclude.md`.

### Tasks (T052–T056)

See tasks.md for numbered breakdown.

**Execution order:** T052 first (module). T053, T054 can run parallel to each other after T052. T055 and T056 depend on T052 content being settled; parallel to each other.

## Complexity Tracking

> No constitution violations to justify.
