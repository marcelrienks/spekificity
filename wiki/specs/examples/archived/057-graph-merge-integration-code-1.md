```json
{
  "version": "1.0",
  "merge": {
    "strategy": "union-with-dedup",
    "deduplication": {
      "codeNodes": "by (file, symbol, symbolType)",
      "docNodes": "by (file, heading, level)",
      "crossType": "keep separate (code and doc are different)"
    },
    "linkDiscovery": {
      "codeToDocPatterns": [
        "vault/path#heading in comments/docstrings",
        "decision/pattern name mentions",
        "See [doc] comments"
      ],
      "docToCodePatterns": [
        "src/path/file.ts code paths",
        "import statements",
        "function/class name mentions"
      ]
    },
    "backreferenceComputation": "bidirectional mirrors (A→B means B←A)",
    "sortOrder": ["code nodes by (file, symbol)", "doc nodes by (file, heading)", "skill nodes by command"]
  },
  "validation": {
    "noDuplicateIds": true,
    "backreferencesSymmetric": true,
    "allFilesExist": true,
    "noOrphanedNodes": false,
    "nodeTypesValid": true
  }
}
```
