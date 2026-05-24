---
consolidated-from:
  - 141-test-suite-specification-code-1.md
  - 141-test-suite-specification-code-2.md
  - 141-test-suite-specification-code-3.md
  - 141-test-suite-specification-code-4.md
  - 141-test-suite-specification-code-5.md
consolidated-at: 2026-05-24T12:05:00Z
---

# Examples: 141 — Test Suite Specification

Consolidated test-suite examples and mocks used for testing workflows.

## Source: 141-test-suite-specification-code-1.md

```yaml
name: Test on PR

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run:
          pip install -e .
          pip install pytest pytest-cov pytest-mock
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml
      
      - name: Run integration tests
        run: pytest tests/integration/ -v --cov=src --cov-report=xml --cov-append
      
      - name: Run E2E tests (quick subset)
        run: pytest tests/e2e/test_full_workflow.py -v --cov=src --cov-report=xml --cov-append
        timeout-minutes: 5
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

## Source: 141-test-suite-specification-code-2.md

```python
class MockVault:
    """Simulates Obsidian vault file I/O."""
    
    def __init__(self, temp_dir):
        self.root = temp_dir
        self.decisions = []
        self.patterns = []
        self.specs = {}
        self.plans = {}
        self.lessons = {}
    
    def read_decisions(self):
        """Return vault decisions."""
        return self.decisions
    
    def read_patterns(self):
        """Return vault patterns."""
        return self.patterns
    
    def write_spec(self, feature_id, spec_dict):
        """Save spec JSON."""
        self.specs[feature_id] = spec_dict
    
    def write_plan(self, feature_id, plan_dict):
        """Save plan JSON."""
        self.plans[feature_id] = plan_dict
    
    def write_lesson(self, feature_id, lesson_dict):
        """Save lesson markdown."""
        self.lessons[feature_id] = lesson_dict
    
    def file_not_found_error(self, path):
        """Raise error if file not found."""
        raise FileNotFoundError(f"Vault file not found: {path}")
```

## Source: 141-test-suite-specification-code-3.md

```python
class MockLatAdapter:
    """Simulates the lat.md adapter: maps spec tool names to lat.md CLI/MCP semantics."""
    
    def __init__(self):
        self.symbols = [
            {"name": "main", "type": "function", "file": "main.py", "line": 10},
            {"name": "log_output", "type": "function", "file": "utils.py", "line": 5},
            {"name": "Config", "type": "class", "file": "config.py", "line": 1},
            # ... 47 more mock symbols
        ]
    
    def lat_symbols(self, file_path):
        """Return symbols in file."""
        return [s for s in self.symbols if s["file"] == file_path]
    
    def lat_definition(self, symbol_name):
        """Return symbol definition."""
        sym = next((s for s in self.symbols if s["name"] == symbol_name), None)
        return sym or {"error": "Symbol not found"}
    
    def lat_references(self, symbol_name):
        """Return all references to symbol."""
        return [{"file": "main.py", "line": 15}, {"file": "utils.py", "line": 8}]
    
    def lat_impact(self, symbol_name):
        """Return impact radius (affected symbols)."""
        return {
            "direct": ["caller1", "caller2"],
            "transitive": ["indirect1", "indirect2"],
            "estimate_impact": "medium"
        }
    
    def lat_query(self, query):
        """Return results from free-form query."""
        if "timeout" in query:
            raise TimeoutError("Query timeout (3s)")
        return {"results": self.symbols[:5]}
```

## Source: 141-test-suite-specification-code-4.md

```python
class MockSpecKitAdapter:
    """Simulates SpecKit command responses for testing."""
    
    def prepare(self, feature_name, config):
        """Return success."""
        return {"status": "success", "feature": feature_name}
    
    def specify(self, constitution, enriched_context):
        """Return mock spec JSON."""
        return {
            "feature_name": "add-logging",
            "requirements": ["Add logging to main.py", "Add logging to utils.py"],
            "scope": "core",
            "status": "specified"
        }
    
    def plan(self, spec, enriched_context):
        """Return mock plan JSON (3 tasks)."""
        return {
            "feature_name": "add-logging",
            "tasks": [
                {"id": 1, "name": "Add logging imports", "file": "main.py"},
                {"id": 2, "name": "Add logging calls", "file": "utils.py"},
                {"id": 3, "name": "Update config", "file": "config.py"}
            ],
            "status": "planned"
        }
    
    def implement(self, task, enriched_context):
        """Return mock implementation result."""
        return {
            "task_id": task["id"],
            "status": "success",
            "code_generated": f"# Logging added to {task['file']}",
            "diff": "mock diff here"
        }
    
    def post(self, feature_state):
        """Return success."""
        return {"status": "success", "feature_complete": True}
```

## Source: 141-test-suite-specification-code-5.md

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
