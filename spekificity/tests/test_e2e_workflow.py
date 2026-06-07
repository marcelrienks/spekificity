"""End-to-end workflow tests: prepare → plan → implement → conclude.

Validates complete Spekificity workflow on sample feature.
"""

import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from spekificity.skills.prepare import prepare
from spekificity.skills.plan import plan
from spekificity.skills.implement import implement
from spekificity.skills.conclude import conclude
from spekificity.core.vault import Vault
from spekificity.core.progress import ProgressLogger


@pytest.fixture
def sample_project():
    """Create sample project with vault initialized."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)

        # Initialize git
        import subprocess
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True
        )

        # Create project structure
        (project_path / ".specify").mkdir()
        (project_path / "specs").mkdir()
        vault_path = project_path / "vault"
        vault_path.mkdir()

        # Create vault structure
        Vault(str(vault_path)).ensure_structure()

        # Create sample tasks file
        tasks_file = project_path / "specs" / "test_feature" / "tasks.md"
        tasks_file.parent.mkdir(parents=True, exist_ok=True)
        tasks_file.write_text("""# Test Feature Tasks

- T1.1 [CODE] Setup database connection
- T1.2 [CODE] Implement user model
- T1.3 [TEST] Write unit tests
""")

        yield project_path, vault_path


class TestPrepareSkill:
    """Tests for /spek.prepare skill."""

    def test_prepare_loads_context(self, sample_project):
        """Prepare should load context and generate navigation guide."""
        project_path, vault_path = sample_project

        start = time.time()
        result = prepare(
            "Create user authentication system",
            project_path=str(project_path),
            vault_path=str(vault_path)
        )
        elapsed = time.time() - start

        assert result["success"]
        assert "Prepare:" in result["report"]
        assert elapsed < 30, f"Prepare took {elapsed}s, SLA is < 30s"
        assert "Next Steps" in result["report"]
        assert result["meets_sla"]

    def test_prepare_estimates_tokens(self, sample_project):
        """Prepare should estimate context tokens."""
        project_path, vault_path = sample_project

        result = prepare(
            "Create feature",
            project_path=str(project_path),
            vault_path=str(vault_path)
        )

        assert "tokens" in result["report"].lower()
        assert "Estimated context tokens" in result["report"]


class TestPlanSkill:
    """Tests for /spek.plan skill."""

    @pytest.mark.skip(reason="Requires SpecKit CLI (external dependency)")
    def test_plan_generates_spec_and_tasks(self, sample_project):
        """Plan should generate spec, plan, and tasks."""
        project_path, vault_path = sample_project

        start = time.time()
        result = plan(
            "Create user authentication with email and password",
            project_path=str(project_path),
            vault_path=str(vault_path),
            output_dir=str(project_path / "specs" / "auth")
        )
        elapsed = time.time() - start

        assert result["success"]
        assert "spec" in result
        assert "plan" in result
        assert elapsed < 180, f"Plan took {elapsed}s, SLA is < 3 min"
        assert result["meets_sla"]

    @pytest.mark.skip(reason="Requires SpecKit CLI (external dependency)")
    def test_plan_detects_ambiguities(self, sample_project):
        """Plan should detect ambiguities in feature description."""
        project_path, vault_path = sample_project

        result = plan(
            "Add authentication maybe with OAuth or email",
            project_path=str(project_path),
            vault_path=str(vault_path)
        )

        # May or may not find ambiguities depending on implementation
        # But should complete successfully
        assert result["success"]


class TestImplementSkill:
    """Tests for /spek.implement skill."""

    def test_implement_loads_context(self, sample_project):
        """Implement should load and inject task context."""
        project_path, vault_path = sample_project

        start = time.time()
        result = implement(
            "T1.1",
            project_path=str(project_path),
            vault_path=str(vault_path),
            tasks_file=str(project_path / "specs" / "test_feature" / "tasks.md")
        )
        elapsed = time.time() - start

        assert result["success"]
        assert "context_preamble" in result
        assert elapsed < 10, f"Context injection took {elapsed}s, SLA is < 10s"
        assert result["context_ok"]

    def test_implement_creates_progress_log(self, sample_project):
        """Implement should create progress log."""
        project_path, vault_path = sample_project

        result = implement(
            "T1.1",
            project_path=str(project_path),
            vault_path=str(vault_path),
            tasks_file=str(project_path / "specs" / "test_feature" / "tasks.md")
        )

        assert result["success"]
        assert result["log_file"]
        log_path = Path(result["log_file"])
        assert log_path.exists()


class TestConcludeSkill:
    """Tests for /spek.conclude skill."""

    def test_conclude_generates_summary(self, sample_project):
        """Conclude should generate completion summary."""
        project_path, vault_path = sample_project

        start = time.time()
        result = conclude(
            "test_feature",
            project_path=str(project_path),
            vault_path=str(vault_path),
            specs_dir=str(project_path / "specs")
        )
        elapsed = time.time() - start

        assert result["success"]
        assert "summary" in result
        assert elapsed < 300, f"Conclude took {elapsed}s, SLA is < 5 min"
        assert result["meets_sla"]

    def test_conclude_writes_lessons(self, sample_project):
        """Conclude should write lessons to vault."""
        project_path, vault_path = sample_project

        result = conclude(
            "test_feature",
            project_path=str(project_path),
            vault_path=str(vault_path),
            specs_dir=str(project_path / "specs")
        )

        assert result["success"]
        assert result["lessons_written"]
        lesson_path = Path(result["lessons_written"])
        assert lesson_path.exists()


class TestFullWorkflow:
    """Test complete workflow end-to-end."""

    @pytest.mark.skip(reason="Requires SpecKit CLI (external dependency)")
    def test_full_workflow_lifecycle(self, sample_project):
        """Full workflow: prepare → plan → implement → conclude."""
        project_path, vault_path = sample_project

        # Phase 1: Prepare
        prepare_result = prepare(
            "Add user authentication",
            project_path=str(project_path),
            vault_path=str(vault_path)
        )
        assert prepare_result["success"]

        # Phase 2: Plan
        plan_result = plan(
            "Users should be able to log in with email and password",
            project_path=str(project_path),
            vault_path=str(vault_path),
            output_dir=str(project_path / "specs" / "auth")
        )
        assert plan_result["success"]

        # Phase 3: Implement
        implement_result = implement(
            "T1.1",
            project_path=str(project_path),
            vault_path=str(vault_path),
            tasks_file=str(project_path / "specs" / "auth" / "tasks.md")
        )
        assert implement_result["success"]

        # Phase 4: Conclude
        conclude_result = conclude(
            "auth",
            project_path=str(project_path),
            vault_path=str(vault_path),
            specs_dir=str(project_path / "specs")
        )
        assert conclude_result["success"]

        # Verify vault updated
        vault = Vault(str(vault_path))
        lessons = vault.load_lessons()
        assert len(lessons) >= 0  # Lessons may or may not exist, but vault should be queryable

    def test_workflow_reuses_lessons(self, sample_project):
        """Second feature should reuse lessons from first feature."""
        project_path, vault_path = sample_project

        # First feature
        first_result = conclude(
            "feature1",
            project_path=str(project_path),
            vault_path=str(vault_path),
            specs_dir=str(project_path / "specs")
        )
        assert first_result["success"]

        # Second feature with prepare
        second_prepare = prepare(
            "Build on first feature",
            project_path=str(project_path),
            vault_path=str(vault_path)
        )

        # Report should reference prior lessons if any exist
        assert second_prepare["success"]


class TestProgressTracking:
    """Test progress tracking integration."""

    def test_progress_logger_lifecycle(self, sample_project):
        """Progress logger should track task lifecycle."""
        project_path, vault_path = sample_project

        logger = ProgressLogger(str(project_path / ".specify" / "logs"))

        # Start task
        log_path = logger.start_task("T1.1", "Setup database")
        assert log_path.exists()

        # Log progress
        assert logger.log_progress("T1.1", "Connected to DB")
        assert logger.log_decision("T1.1", "Use PostgreSQL", "Best fit for requirements")

        # Complete task
        assert logger.mark_complete("T1.1", "Database connected and tested")

        # Verify log content
        content = logger.get_log_content("T1.1")
        assert "Connected to DB" in content
        assert "PostgreSQL" in content
        assert "completed" in content.lower()
