# Small CLI Contract Integration Test (SpecKit / lat.md)


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
Date: 2026-05-21

Goal
- Provide a minimal, fast integration test asserting that the external tooling's CLI outputs match expected JSON shapes used by the orchestration layer.

Tests (high-level)
- `tests/integration/cli_contracts/test_speckit_contract.py`
  - Run: `specify --version` → assert exit `0` and human-readable version.
  - Run: `specify explain --format=json --input tests/fixtures/mock_specs/complete_spec.json` (or the real CLI command used) → assert JSON parseable and contains `feature_name`, `requirements`, `tasks` keys.

- `tests/integration/cli_contracts/test_lat_contract.py`
  - Run: `lat --version` → assert exit `0`.
  - Run: `lat query --json 'symbols' --path tests/fixtures/synthetic_project/src` → assert JSON and fields `name,type,file,line` exist in first result.

Mocking & CI
- These tests should run with mocks in CI when the real CLIs are unavailable. Provide environment variable `SKIP_CLI_CONTRACTS=true` to skip when unavailable (but require at least one run on CI with real tools).

Acceptance Criteria
- Contract tests present and green in at least one CI run using provided `uv.lock` or installed toolset.