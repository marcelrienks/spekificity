# Contributing to Spekificity

This document describes how to set up a development environment, run tests locally, and contribute changes.

Quick start (macOS / Linux)

1. Create a virtualenv and install dev dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

2. Run unit tests

```bash
pytest tests/unit -q
```

3. Run full test-suite (including integration)

```bash
pytest -q
```

Coding standards
- Format: `black .`
- Lint: `ruff .`
- Type-check (optional): `mypy src`

Branching & PRs
- Create a feature branch: `feature/<short-desc>`.
- Open small, focused PRs targeting `main` with descriptive titles and summaries.

Tests & CI
- Add unit tests for new behavior under `tests/unit/`.
- Mark slow E2E tests with `@pytest.mark.slow` and run them only in scheduled CI.

How to add a spec
- Add a new file under `wiki/specs/` describing goals, acceptance criteria, test cases, and migration notes.

Local vault emulation
- For features that interact with a vault, use the `tests/fixtures/mock_vault` helper in `conftest.py`.

Contact
- Open an issue or reach out via PR comments for help.
