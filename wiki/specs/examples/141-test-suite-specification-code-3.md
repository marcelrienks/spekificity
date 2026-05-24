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
