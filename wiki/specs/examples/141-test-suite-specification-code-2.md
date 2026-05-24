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
