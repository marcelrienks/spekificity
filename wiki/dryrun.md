# Dry Run: Spec Implementation Validation

Date: 2026-05-21
Status: Draft

## Purpose

This document captures a dry-run validation: if all `wiki/specs` documents are implemented, in the specified order, will the resulting project fulfill the goals and constraints expressed across the `wiki/` documentation? It records findings, gaps, and concrete recommendations.

## Executive Summary

- Overall: The specs are comprehensive and, if implemented in order and with the required runtime/tooling in place, should deliver the intended outcome: a spec-driven workflow, persistent vault, CodeGraph indexing, composable skills, and automated lessons capture.
- Major risks remain that would block full parity if not addressed first (CI/test harness, vault runtime dependency, pinned external tooling, and some missing docs/files).

## High-impact Findings

1. CI and test harness missing
   - Specs reference `.github/workflows/` jobs and `tests/` layout, but no CI workflows or `tests/` directory exist. Without these the `141-test-suite-specification.md` goals (PR checks, coverage targets) cannot be validated.

2. Tests and fixtures absent
   - The roadmap and test spec expect `tests/unit`, `tests/integration`, and `tests/e2e` with fixtures (synthetic project). These are not present.

3. Obsidian CLI is a hard dependency with no fallback
   - Multiple specs and `README.md` declare Obsidian CLI mandatory for vault operations. If Obsidian CLI is unavailable or install fails, there is no documented graceful degraded mode.

4. External tool/version pinning and contract checks
   - Specs depend on SpecKit, CodeGraph, and `uv`. There are recommendations to pin versions, but the repo lacks `uv.lock` or explicit pins and lacks a small integration test confirming CLI contract expectations.

5. Referenced contributor docs missing
   - `CONTRIBUTING.md` is referenced by `wiki/install.md`/`README.md` but not present.

## Ambiguities & Minor Issues

- Some performance/coverage targets are ambitious (e.g. CodeGraph refresh <3s, `/spek.prepare` <5s, 90%+ per-module coverage). Treat these as aspirational baselines and verify after a prototype.
- Error/exit code semantics are described (exit code 0/1/2 in places) but not standardized across CLI modules; define a short return-code policy for consistency.

## Recommended Next Actions (Priority order)

1. Scaffold CI workflows and minimal `tests/` skeleton
   - Add `.github/workflows/test-pr.yaml` to run unit + integration on PRs and `performance.yaml` for scheduled runs.
   - Create `tests/` directories with the fixture scaffolding described in `wiki/specs/141-test-suite-specification.md`.

2. Implement `vault_sync` abstraction with fallback
   - Provide two adapters: `obsidian_cli` (preferred) and `git_only` (fallback). Document behavior and selection logic in `wiki/install.md`.

3. Add minimal integration checks and pinning
   - Add `pyproject.toml` / `uv.lock` pins for SpecKit, CodeGraph, and `uv` (or document required versions). Add a small integration test that verifies SpecKit/CodeGraph CLI calls used by the orchestration layer.

4. Add `CONTRIBUTING.md` or update docs to remove references

5. Establish a short CLI return-code policy and record in `wiki/conventions.md`.

## Checklist (actionable)

- [ ] Add `.github/workflows/test-pr.yaml` (PR checks)
- [ ] Add `tests/` skeleton + key fixtures
- [ ] Implement `vault_sync` abstraction (obsidian_cli + git_only)
- [ ] Add `uv.lock` / pinned tool versions
- [ ] Add `CONTRIBUTING.md`
- [ ] Add a small SpecKit/CodeGraph CLI contract integration test

## Next Steps

I can scaffold the CI workflow and `tests/` skeleton and implement the `vault_sync` adapter next. Which of these should I start with? (If you want, I'll begin by adding `tests/` and `.github/workflows/test-pr.yaml`.)
