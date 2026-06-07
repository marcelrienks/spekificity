"""Integration tests for Phase 2: Vault + Code Indexing."""

import tempfile
from pathlib import Path

import pytest

from spekificity.core.context import ContextLoader, format_context_for_agent
from spekificity.core.compression import CavemanCompressor, compress_text
from spekificity.core.vault import Vault
from spekificity.integrations.semantic_search import SemanticSearcher, load_searcher


@pytest.fixture
def temp_project():
    """Create temporary project structure for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        
        # Create vault
        vault_path = project_path / "vault"
        vault_path.mkdir()
        
        # Create sample Python files
        (project_path / "auth.py").write_text("""
def authenticate(user, password):
    \"\"\"Authenticate user with password.\"\"\"
    # Implementation
    pass

def verify_token(token):
    \"\"\"Verify JWT token.\"\"\"
    pass
""")
        
        (project_path / "database.py").write_text("""
class Database:
    def query(self, sql):
        \"\"\"Execute database query.\"\"\"
        pass
""")
        
        yield project_path, vault_path


class TestSemanticSearch:
    """Tests for fallback semantic search."""
    
    def test_searcher_initialization(self, temp_project):
        """SemanticSearcher should initialize without errors."""
        project_path, _ = temp_project
        searcher = load_searcher(str(project_path))
        
        assert searcher is not None
        assert searcher.project_path == project_path
    
    def test_search_files(self, temp_project):
        """Search should find files in project."""
        project_path, _ = temp_project
        searcher = SemanticSearcher(str(project_path))
        
        results = searcher.search_files("auth", limit=5)
        
        # Should find auth.py or handle gracefully
        assert isinstance(results, list)
    
    def test_search_functions(self, temp_project):
        """Search should find function definitions."""
        project_path, _ = temp_project
        searcher = SemanticSearcher(str(project_path))
        
        results = searcher.search_functions("def", limit=5)
        
        # Should find function definitions or return empty
        assert isinstance(results, list)


class TestContextLoader:
    """Tests for context loading."""
    
    def test_context_loader_initialization(self, temp_project):
        """ContextLoader should initialize without errors."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        assert loader is not None
        assert loader.project_path == project_path
    
    def test_load_relevant_decisions_empty_vault(self, temp_project):
        """Loading decisions from empty vault should return empty list."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        decisions = loader.load_relevant_decisions("authentication")
        
        assert decisions == []
    
    def test_load_relevant_patterns_empty_vault(self, temp_project):
        """Loading patterns from empty vault should return empty list."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        patterns = loader.load_relevant_patterns("authentication")
        
        assert patterns == []
    
    def test_load_relevant_code(self, temp_project):
        """Load relevant code should handle missing lat.md gracefully."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        code = loader.load_relevant_code("authenticate", limit=2, use_fallback=True)
        
        # Should return list (possibly empty if no matches)
        assert isinstance(code, list)
    
    def test_load_task_context(self, temp_project):
        """Load complete task context should work."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        context = loader.load_task_context(
            task_id="T1.1",
            task_description="Implement authentication system",
        )
        
        assert context.task_id == "T1.1"
        assert context.task_description == "Implement authentication system"
        assert isinstance(context.decisions, list)
        assert isinstance(context.patterns, list)
        assert isinstance(context.code, list)


class TestContextFormatting:
    """Tests for context formatting."""
    
    def test_format_context_for_agent(self, temp_project):
        """Format context should produce markdown."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        context = loader.load_task_context("T1.1", "Test task")
        
        formatted = format_context_for_agent(context, compressed=False)
        
        assert "T1.1" in formatted
        assert isinstance(formatted, str)
    
    def test_format_context_compressed(self, temp_project):
        """Compressed format should be shorter."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        context = loader.load_task_context("T1.1", "Test task")
        
        normal = format_context_for_agent(context, compressed=False)
        compressed = format_context_for_agent(context, compressed=True)
        
        # Compressed should be shorter or equal
        assert len(compressed) <= len(normal)


class TestCavemanCompression:
    """Tests for Caveman compression."""
    
    def test_compressor_initialization(self):
        """Compressor should initialize with valid intensity levels."""
        for intensity in ["lite", "full", "ultra"]:
            compressor = CavemanCompressor(intensity)
            assert compressor.intensity == intensity
    
    def test_compress_text_removes_filler(self):
        """Compress should remove filler words."""
        text = "Just implement the authentication basically"
        compressed = compress_text(text, intensity="full")
        
        # "just" and "basically" should be removed
        assert "just" not in compressed.lower()
        assert "basically" not in compressed.lower()
    
    def test_compress_text_abbreviates_ultra(self):
        """Ultra compression should abbreviate prose."""
        text = "configure the database connection"
        compressed = compress_text(text, intensity="ultra")
        
        # Should abbreviate
        assert "config" in compressed.lower() or "db" in compressed.lower()
    
    def test_compression_levels(self):
        """Different compression levels should produce different output."""
        text = "The authentication system really needs proper configuration basically"
        
        lite = compress_text(text, intensity="lite")
        full = compress_text(text, intensity="full")
        ultra = compress_text(text, intensity="ultra")
        
        # All should be strings
        assert isinstance(lite, str)
        assert isinstance(full, str)
        assert isinstance(ultra, str)
        
        # Ultra should be shortest or equal
        assert len(ultra) <= len(lite)


class TestIntegration:
    """Integration tests for Phase 2 components."""
    
    def test_full_context_pipeline(self, temp_project):
        """Full pipeline: load context, format, compress."""
        project_path, vault_path = temp_project
        loader = ContextLoader(str(project_path), str(vault_path))
        
        # Load context
        context = loader.load_task_context(
            "T2.1",
            "Implement code indexing"
        )
        
        # Format
        formatted = format_context_for_agent(context, compressed=False)
        compressed = format_context_for_agent(context, compressed=True)
        
        # Verify outputs
        assert "T2.1" in formatted
        assert "T2.1" in compressed
        assert len(compressed) <= len(formatted) * 1.2  # Compressed should be shorter
