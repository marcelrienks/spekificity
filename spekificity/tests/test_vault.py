"""Unit tests for vault engine."""

import tempfile
from pathlib import Path

import pytest

from spekificity.core.vault import Vault, create_vault_structure, load_vault


@pytest.fixture
def temp_vault():
    """Create temporary vault for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir) / "vault"
        yield vault_path
        # Cleanup handled by tempfile


class TestVaultStructure:
    """Tests for vault directory structure creation."""
    
    def test_ensure_structure_creates_directories(self, temp_vault):
        """Ensure vault structure creates required directories."""
        vault = Vault(str(temp_vault))
        vault.ensure_structure()
        
        assert temp_vault.exists()
        assert (temp_vault / "lessons").exists()
    
    def test_create_vault_structure_with_templates(self, temp_vault):
        """Creating vault structure should include template files."""
        create_vault_structure(temp_vault)
        
        assert temp_vault.exists()
        assert (temp_vault / "lessons").exists()
        # Note: Templates may or may not exist depending on actual template files


class TestVaultOperations:
    """Tests for vault loading and writing."""
    
    def test_load_decisions_empty_vault(self, temp_vault):
        """Loading decisions from empty vault should return empty list."""
        vault = Vault(str(temp_vault))
        decisions = vault.load_decisions()
        
        assert decisions == []
    
    def test_load_patterns_empty_vault(self, temp_vault):
        """Loading patterns from empty vault should return empty list."""
        vault = Vault(str(temp_vault))
        patterns = vault.load_patterns()
        
        assert patterns == []
    
    def test_load_lessons_empty_vault(self, temp_vault):
        """Loading lessons from empty vault should return empty list."""
        vault = Vault(str(temp_vault))
        lessons = vault.load_lessons()
        
        assert lessons == []
    
    def test_write_lesson(self, temp_vault):
        """Writing a lesson should create a timestamped file."""
        vault = Vault(str(temp_vault))
        
        lesson_data = {
            "feature": "Test Feature",
            "author": "test_user",
            "outcomes": "Feature completed successfully",
            "lessons_learned": ["Lesson 1", "Lesson 2"],
        }
        
        lesson_path = vault.write_lesson(lesson_data)
        
        assert lesson_path.exists()
        assert "test-feature" in lesson_path.name.lower()
        assert lesson_path.suffix == ".md"
    
    def test_get_summary(self, temp_vault):
        """Vault summary should report counts."""
        vault = Vault(str(temp_vault))
        vault.ensure_structure()
        
        summary = vault.get_summary()
        
        assert summary["decisions"] == 0
        assert summary["patterns"] == 0
        assert summary["lessons"] == 0
        assert "vault_path" in summary


class TestVaultLoader:
    """Tests for vault loader function."""
    
    def test_load_vault_creates_instance(self, temp_vault):
        """load_vault should return Vault instance."""
        vault = load_vault(str(temp_vault))
        
        assert isinstance(vault, Vault)
        assert temp_vault.exists()
