---
title: "CI & Validation Workflow Specification"
status: "DRAFT"
date: "2026-05-21"
---

# CI & Validation Workflow Specification

Status: DRAFT
Date: 2026-05-21

Purpose
- Define CI requirements and acceptance criteria to ensure repository health, test coverage, and performance baselines before merge.

Goals
- Run unit + integration test suite on PRs.
- Produce coverage reports and fail on coverage regressions.
- Run scheduled performance checks (weekly/monthly) and persist baselines.
- Cache dependencies for faster runs; publish test artifacts (coverage HTML, performance logs).

Scope
- GitHub Actions as primary CI runner. Support local `pre-commit` + `tox` for maintainers.

Jobs
- `test-pr` (PR): runs `pytest` (unit+integration), `ruff`/`black` checks, coverage.
- `lint` (PR): runs `ruff`, `mypy`, `black --check`.
- `performance` (schedule): runs a small synthetic E2E with timing, stores metrics as artifacts.

Inputs & Secrets
- No sensitive inputs required for basic validation.
- Optional secrets for third-party integrations (e.g., lat.md hosted API) must be read from GitHub Secrets.

Success Criteria
- PR job exit code 0 when: tests pass, lint passes, coverage target not decreased.
- Coverage threshold default: no decrease from `main`; configurable via `CI_MIN_COVERAGE`.
- Performance job stores `performance.json` artifact with wall-time and token estimates.

Failure Modes & Actions
- Flaky test detection: re-run once automatically before failing the job.
- Long-running tests: timeouts set per job (default 20m), with alert to maintainers.

Migration Notes
- Add `.github/workflows/test-pr.yaml` to enable PR checks. Provide local `scripts/run-local-ci.sh` for contributors (see CONTRIBUTING.md).

Acceptance Tests (for the spec)
- Try opening a PR that changes only a README → CI should pass quickly (lint only).
- Introduce an artificial failing unit test → PR job should fail and report failing test.
