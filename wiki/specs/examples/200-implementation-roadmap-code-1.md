```
spekificity/
├── src/
│   ├── spekificity/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                 # CLI entry point
│   │   │   ├── prepare.py              # /spek.prepare skill
│   │   │   ├── context.py              # /spek.context skill
│   │   │   ├── plan.py                 # /spek.plan skill
│   │   │   ├── map.py                  # /spek.map skill
│   │   │   ├── implement.py            # /spek.implement skill
│   │   │   ├── post.py                 # /spek.conclude skill
│   │   │   └── lessons.py              # /spek.lessons skill
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── lat_index.py           # lat.md core
│   │   │   ├── indexer.py              # File indexing
│   │   │   ├── query.py                # Graph queries
│   │   │   └── schema.py               # Node/edge schema
│   │   ├── vault/
│   │   │   ├── __init__.py
│   │   │   ├── loader.py               # Vault context loading
│   │   │   ├── sync.py                 # Git sync automation
│   │   │   └── formatter.py            # Markdown formatting
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── session.py              # Session memory ops
│   │   │   ├── context_layer.py        # 3-layer context
│   │   │   └── enrichment.py           # Enrichment layers
│   │   ├── orchestration/
│   │   │   ├── __init__.py
│   │   │   ├── speckit_wrapper.py      # SpecKit orchestration
│   │   │   ├── workflow.py             # Feature workflow
│   │   │   └── error_handling.py       # Error/recovery
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── git_ops.py              # Git operations
│   │       └── validators.py           # Input validation
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .spek/
│   └── lat_index.db
├── wiki/
└── pyproject.toml
```
