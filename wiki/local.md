# Local Pre-Merge Testing

Use this workflow to test your current branch locally before merging, without installing from GitHub.

## Why This Path

- Installs the code from your current working tree.
- Picks up local edits immediately.
- Keeps pre-merge validation focused on your branch state.

## Local Environment Setup

```bash
cd /Users/marcelrienks/workspace/code/spekificity

# Create and activate a local virtual environment
uv venv .venv
source .venv/bin/activate

# Install this working tree in editable mode + dev dependencies
uv pip install -e ".[dev]"
```

## Validate CLI from Local Code

```bash
spek --help
spek implement --help
spek conclude --help
```

## Run Quality Gates

```bash
ruff check .
pytest -q tests/unit tests/integration
```

## Optional Tool-Style Local Install

If you want to test as a uv tool from local source:

```bash
cd /Users/marcelrienks/workspace/code/spekificity
uv tool install --editable .
spek --help
```

Remove when done:

```bash
uv tool uninstall spekificity
```

## Notes

- This workflow intentionally avoids `uv tool install ... --from git+https://...` so you are testing local branch code, not remote HEAD.
- For CI-equivalent checks, run both lints and full tests before opening/merging a PR.
