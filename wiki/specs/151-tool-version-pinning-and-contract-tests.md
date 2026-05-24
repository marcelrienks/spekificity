# Tool Version Pinning & CLI Contract Tests


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
Date: 2026-05-21

Purpose
- Define how external tools (SpecKit, lat.md, uv, Obsidian CLI) are pinned and how simple CLI contract tests verify expected behavior.

Pinning Strategy
- Primary: declare minimal supported versions in `pyproject.toml` `dependencies` and `dev` extras.
- Reproducible installs: provide an optional lock file `uv.lock` (or `requirements.txt` for contributors not using `uv`).
- Document exact tool commands used by the orchestration layer and expected stable output formats (JSON schemas where applicable).

CLI Contract Tests
- Create lightweight integration tests under `tests/integration/cli_contracts/`:
  - `test_speckit_contract.py`: calls `specify-cli --version` and `specify-cli explain --format=json` (or the real CLI command used) and asserts JSON parseable output and presence of expected keys.
  - `test_lat_contract.py`: calls `lat query --json 'symbols'` (or configured command), asserts well-formed JSON and required fields (`name`, `type`, `file`).

Fallback & Graceful Degradation
- If a CLI version is older than required: warn in `spek prepare` and continue in degraded mode when possible.
- If CLI output shape changes: fail fast in CI contract tests and require explicit update of the contract spec and code adjustments.

Acceptance Criteria
- Lock file or explicit instructions are present in `pyproject.toml` or `install.md`.
- At least two CLI contract tests exist and run in CI with mocked endpoints if necessary.