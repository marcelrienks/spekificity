```
tests/
├── unit/                          # majority of tests, fastest, fully mocked
│   ├── test_enrichment_layer.py
 │   ├── test_feature_state.py
 │   ├── test_context_injection.py
 │
 │   ├── test_prepare_workflow.py
 │   ├── test_plan_workflow.py
 │   ├── test_post_workflow.py
 │   └── test_full_pipeline.py
│
├── e2e/                           # small portion of tests, slowest, synthetic fixtures
│   ├── test_full_workflow.py
│   ├── test_error_scenarios.py
│   ├── test_multi_feature.py
│   ├── test_state_persistence.py
│   └── test_performance_baseline.py
│
├── fixtures/                      # Shared test data & synthetic projects
│   ├── synthetic_project/        # Small 5-file repo for E2E testing
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── utils.py
│   │   │   └── config.py
│   │   ├── tests/
│   │   │   └── test_main.py
│   │   └── .spek/
│   │       └── config.yaml
│   │
│   ├── mock_specs/               # Pre-built spec JSONs for fixtures
│   │   ├── complete_spec.json
│   │   ├── partial_spec.json
│   │   └── invalid_spec.json
│   │
│   ├── mock_plans/               # Pre-built plan JSONs
│   │   ├── complete_plan.json
│   │   └── error_plan.json
│   │
│   └── conftest.py              # pytest fixtures (mocks, temp dirs, etc.)
│
└── ci/                           # CI/CD configuration
    ├── .github/workflows/
    │   ├── test-pr.yaml         # Run on PR, full suite
    │   ├── test-local.yaml      # Optional GitHub-hosted runner job
    │   └── performance.yaml     # Performance tracking (monthly)
    │
    └── pre-commit-hooks/
        ├── run-unit-tests.sh    # Local pre-commit hook (unit tests only)
        └── run-quick-tests.sh   # Local quick check (critical path)
```
