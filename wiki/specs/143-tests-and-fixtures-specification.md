---
title: "Tests & Fixtures Specification"
status: "DRAFT"
date: "2026-05-21"
---

# Tests & Fixtures Specification

Status: DRAFT
Date: 2026-05-21

Purpose
- Specify the required test layout, fixture contracts, and synthetic project artifacts to validate behavior described in other specs.

Layout
-- `tests/unit/` — fast, fully mocked unit tests; each module under `src/spekificity` should have a `test_*.py` file.
- `tests/integration/` — integration tests that use real Spekificity code but mock external tools (SpecKit, external CLIs).
- `tests/e2e/` — slow end-to-end tests that operate on a synthetic project in `tests/fixtures/synthetic_project/`.
- `tests/fixtures/` — contains `synthetic_project/`, `mock_specs/`, `mock_plans/`, and `conftest.py` providing standardized fixtures.

Fixture Contracts
- `mock_speckit` should implement `prepare`, `specify`, `plan`, `implement`, `post` stubs as shown in `141-test-suite-specification.md`.
- `mock_lat` should respond to `lat_query(query)` with deterministic JSON, and support simulated `TimeoutError`.
- `mock_vault` should implement read/write methods for decisions, patterns, specs, plans, and lessons and operate on temporary directories.

Synthetic Project
- Small Python repo with 3 source files, 1 test file and a minimal `.spekificity/config.yaml`.
- Used by E2E tests to validate lat.md integration and file-level diffs.

Performance & Flakiness
- Unit tests: target median runtime per test < 50ms.
- Integration tests: target median runtime per test < 1s.
- E2E tests: run in scheduled job only by default; mark as `slow` with pytest markers.

Acceptance Criteria
- A fresh checkout with `pip install -e .[dev]` and `pytest -q` should run unit tests and at least one integration test using the defined fixtures.
