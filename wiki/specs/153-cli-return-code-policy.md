# CLI Return-Code Policy

Status: DRAFT
Date: 2026-05-21

Purpose
- Standardize CLI exit codes across `spek.*` and `speckit.*` wrappers so automation and CI can interpret outcomes reliably.

Mapping (canonical)
- `0` — Success. All requested work completed with no errors.
- `1` — Partial success. Some non-fatal errors occurred (e.g., some tasks failed but workflow continued); artifacts produced but not fully complete.
- `2` — Missing artifact / precondition failure. Required input missing (e.g., attempt to implement without plan/spec). No changes applied.
- `3` — Usage / invalid arguments. CLI mis-invoked (invalid flags, help requested triggers `0` when showing help).
- `4` — Unhandled runtime error. Internal exception, precondition checks passed but execution crashed.
- `5` — Config / environment error. Misconfigured vault, missing dependencies, adapter unavailable.

Behavior Notes
- Commands should exit with the lowest-severity non-zero code that correctly represents the outcome.
- When in `--dry-run` mode, exit codes reflect what would have happened (use `0` for dry-run success even if non-dry run would have partial failures).
- Detailed machine-parsable outcome written to `--output-file` in JSON when provided; includes `exit_code`, `errors[]`, `artifacts[]`, `metrics{}`.

Examples
- `spek implement` where 2/3 tasks succeeded → exit `1`, JSON has `errors` listing failed tasks.
- `spek implement` without `plan.json` → exit `2`, JSON `errors` contains `MissingArtifactError`.

Acceptance Criteria
- `wiki/conventions.md` includes a short summary and link to this policy.
- Unit tests assert correct exit codes for representative scenarios.
