# Caveman Integration Specification



Date: 2026-05-23

Purpose
- Define the integration contract for "Caveman" compression mode used across Spekificity.
- Clarify that Caveman is an internal skill/mode (not an external CLI) and document configuration, invocation points, and test fixtures.

Scope
- Lessons generation (`/spek.conclude`)
- Vault compression and storage (`/memories/repo` writes)
- Session-level mode selection and API for compression/expansion
- Test fixtures and contract for unit/integration tests

Background
- Caveman is a writing-style compression mode intended to reduce token usage when generating and persisting lessons, summaries, and other large textual artifacts.
- Caveman is implemented as an internal skill and transform pipeline (CavemanEncoder/CavemanDecoder) that runs in-process; it is not a third-party CLI nor an installable package.

Design Goals
- Preserve technical accuracy and searchable keywords while reducing verbosity (~30–90% depending on mode).
- Be reversible or partially reversible where needed (store both compressed text and a short extraction map when required).
- Configurable per-session, per-feature, and per-command.
- Testable via deterministic encoder/decoder mocks in unit and integration tests.

Modes and Defaults
- `lite` (approx. 30% reduction) — human-readable; recommended for first-time docs.
- `full` (approx. 75% reduction) — default; terse but precise.
- `ultra` (approx. 90% reduction) — minimal token budget; lossy by design.
- Default mode: `full` (unless overridden by user preference or feature config).

Configuration (example)
```yaml
caveman:
  enabled: true
  default_mode: full
  allow_ultra: false  # disallow ultra in shared/team repos by default
  preserve_keywords: true
  store_expansion_map: true  # optional, stores a map to aid partial expansion
```

API / Invocation Points
- `CavemanEncoder.compress(text: str, mode: str='full') -> CompressedArtifact`
  - `CompressedArtifact`: { "mode": "full", "content": "...", "keywords": [...], "map": {...} }
- `CavemanDecoder.expand(artifact: CompressedArtifact, hints: Optional[dict]) -> str`
- Integration hooks:
  - `spek.conclude` — call `CavemanEncoder.compress()` when persisting lessons to vault.
  - `vault.write` — if compression enabled and `store_expansion_map` false, store only compressed content; otherwise store both compressed and expansion map.
  - `spek.lessons --mode=[lite|full|ultra]` — CLI flag to override session default.

Storage Contracts
- Compressed content must include metadata: `mode`, `version`, `generated_by`, `timestamp`.
- If `store_expansion_map` is true, the map must be stored alongside compressed content as `artifact.map.json`.
- Backwards compatibility: older compressed lessons must still be readable by `CavemanDecoder` that supports earlier `version` values.

Testing & Fixtures
- Unit tests:
  - `tests/unit/test_caveman_encoder.py` — verifies compression ratios, deterministic transformations for canonical inputs, and keyword preservation.
  - `tests/unit/test_caveman_decoder.py` — verifies expansion fidelity within acceptable bounds (for `lite` and `full`), and expected lossy behavior for `ultra`.
- Fixtures:
  - `mock_caveman`: `class MockCavemanAdapter` with `compress()` and `expand()` deterministic stubs used by integration tests.
  - Example fixture in `tests/fixtures/conftest.py`:

```python
class MockCavemanAdapter:
    def compress(self, text, mode='full'):
        # simple deterministic stub: return first N tokens + mode metadata
        tokens = text.split()[:max(10, len(text)//4)]
        return {"mode": mode, "content": " ".join(tokens), "keywords": [tokens[0]]}

    def expand(self, artifact, hints=None):
        # naive expand: return artifact['content'] + ' (expanded)'
        return artifact['content'] + ' (expanded)'
```

- Integration tests:
  - `tests/integration/test_caveman_integration.py` — uses `MockCavemanAdapter` to validate that `spek.conclude` writes compressed artifacts and that CLI `spek.lessons --mode=lite` respects mode override.

Docs & References
- Canonical quick reference: [wiki/patterns/caveman-compression-mode-quick-ref.md](../patterns/caveman-compression-mode-quick-ref.md)
- Implementation notes: implement encoder/decoder as pure functions to facilitate offline testing and deterministic mocking.

Migration Notes
- Replace any documentation that treats Caveman as an external tool or installable package with notes stating it is an internal skill/mode. No user-level install is required.

Acceptance Criteria
- All internal references to Caveman in `wiki` and `specs` should point to this integration spec or the quick-ref.
- No docs or scripts should instruct users to `install caveman` via package manager or external binary.
- Tests include `MockCavemanAdapter` fixture and at least one integration test referencing it.

Open Items
- Decide whether to expose a server-side HTTP endpoint for corpus-wide expansion on demand (future work).
- Whether to always store the expansion map (privacy/storage tradeoff).


*** End of Spec