# CONTRIBUTING & Onboarding Specification

Date: 2026-05-21

Purpose
- Provide an approachable guide for contributors: setup, common workflows, testing, and branching strategy.

Contents (to be rendered as `CONTRIBUTING.md`)
- Quick start: environment setup, `pip install -e .[dev]`, running tests locally.
- Branching: feature branches named `feature/<short-desc>`, PRs target `main`, small focused PRs.
- Commit message format: short summary + body; conventional commits recommended (optional).
- Tests: run `pytest -q`; mark slow E2E tests with `--runslow` marker; gist for adding new tests & fixtures.
- Code style: `black` + `ruff`; pre-commit hooks recommended (example config included).
- CI: explain what CI checks run on PR and how to interpret failures.
- How to add a new feature: update `wiki/specs/` with a spec file, add tests, implement, open PR.
- How to run CLI locally and emulate vault: `scripts/run-local-ci.sh` examples.

Acceptance Criteria
- `CONTRIBUTING.md` exists in repo root with the above sections and copyable commands for macOS/Linux dev environment.
