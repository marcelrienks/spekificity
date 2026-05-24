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
