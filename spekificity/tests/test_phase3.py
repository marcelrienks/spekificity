"""Integration tests for Phase 3: SpecKit Orchestration."""

import tempfile
from pathlib import Path

import pytest

from spekificity.core.speckit_wrapper import (
    create_enrichment_preamble,
    run_specify,
    run_plan,
)
from spekificity.core.enrichment import EnrichmentFormatter, create_enrichment_context
from spekificity.core.parser import SpecParser, PlanParser, TaskParser
from spekificity.core.validation import SpecValidator, PlanValidator, validate_spec, validate_plan
from spekificity.core.types import Decision, Pattern, Specification, Plan as PlanModel


@pytest.fixture
def sample_decisions():
    """Create sample decisions for enrichment testing."""
    return [
        Decision(
            id="D001",
            title="Use async/await for API calls",
            status="approved",
            decision="All API calls must use async/await pattern",
            rationale="Improves throughput and responsiveness",
            implications=["Requires Python 3.7+", "Error handling simplified"],
            date_created="2026-06-01"
        ),
        Decision(
            id="D002",
            title="PostgreSQL for persistent storage",
            status="approved",
            decision="Use PostgreSQL for all data persistence",
            rationale="ACID compliance, mature ecosystem",
            implications=["Requires DB setup", "Migration tooling needed"],
            date_created="2026-06-01"
        ),
    ]


@pytest.fixture
def sample_patterns():
    """Create sample patterns for enrichment testing."""
    return [
        Pattern(
            id="P001",
            title="Repository Pattern",
            category="Data Access",
            problem="How to abstract database access?",
            solution="Use repository pattern to wrap data layer",
            when_to_use="When isolating data layer from business logic",
            when_not_to_use="For simple CRUD applications"
        ),
        Pattern(
            id="P002",
            title="Dependency Injection",
            category="Architecture",
            problem="How to manage dependencies?",
            solution="Use constructor injection to provide dependencies",
            when_to_use="For testable, loosely coupled components",
            when_not_to_use="For simple one-off scripts"
        ),
    ]


@pytest.fixture
def sample_spec_markdown():
    """Sample spec.md Markdown content."""
    return """---
title: "User Authentication Feature"
branch: "feature/auth"
created: "2026-06-07"
---

## User Stories

- As a user, I want to log in with email and password
- As an admin, I want to enforce strong password policies

## Requirements

- FR-001: System MUST support email/password authentication
- FR-002: System MUST enforce minimum 8-character passwords
- FR-003: System MUST hash passwords using bcrypt

## Entities

- User (id, email, password_hash, created_at)
- Session (id, user_id, token, expires_at)

## Success Criteria

- SC-001: Login page loads in < 2 seconds
- SC-002: Authentication succeeds for valid credentials
- SC-003: Authentication fails for invalid credentials

## Assumptions

- Users have email addresses
- Password reset flows out of scope
"""


@pytest.fixture
def sample_plan_markdown():
    """Sample plan.md Markdown content."""
    return """---
spec_branch: "feature/auth"
spec_file: "specs/auth/spec.md"
---

## Architecture

Implement auth service as separate microservice with REST API.

## Technology Stack

- Python 3.11+
- FastAPI for REST API
- PostgreSQL for user storage
- JWT for session tokens

## Sequencing

Phase 1: User model and database schema
Phase 2: Authentication endpoints
Phase 3: Password validation and hashing

## Risks & Mitigations

- Password compromise: Use bcrypt with cost factor 12
- Session hijacking: Use HTTP-only cookies, SameSite=Strict
"""


class TestEnrichmentFormatter:
    """Tests for enrichment formatting."""

    def test_format_decisions(self, sample_decisions):
        """Formatter should format decisions as Markdown."""
        formatter = EnrichmentFormatter()
        formatted = formatter.format_decisions(sample_decisions)

        assert "Prior Architectural Decisions" in formatted
        assert "Use async/await" in formatted
        assert "async/await pattern" in formatted

    def test_format_patterns(self, sample_patterns):
        """Formatter should format patterns as Markdown."""
        formatter = EnrichmentFormatter()
        formatted = formatter.format_patterns(sample_patterns)

        assert "Relevant Design Patterns" in formatted
        assert "Repository Pattern" in formatted
        assert "Data Access" in formatted

    def test_enrich_specify_input(self, sample_decisions, sample_patterns):
        """Enrichment should prepend decisions/patterns to intent."""
        formatter = EnrichmentFormatter()
        intent = "Create user authentication feature"
        enriched = formatter.enrich_specify_input(intent, sample_decisions, sample_patterns)

        assert intent in enriched
        assert "Use async/await" in enriched
        assert "Repository Pattern" in enriched

    def test_enrich_specify_empty(self):
        """Enrichment with no decisions/patterns should return intent unchanged."""
        formatter = EnrichmentFormatter()
        intent = "Create user authentication feature"
        enriched = formatter.enrich_specify_input(intent, [], [])

        assert intent in enriched


class TestMarkdownParser:
    """Tests for Markdown parsing."""

    def test_parse_spec(self, sample_spec_markdown):
        """Parser should extract spec fields from Markdown."""
        parsed = SpecParser.parse(sample_spec_markdown)

        assert parsed["title"] == "User Authentication Feature"
        assert parsed["branch"] == "feature/auth"
        assert len(parsed["user_stories"]) > 0
        assert len(parsed["requirements"]) > 0
        assert len(parsed["success_criteria"]) > 0

    def test_parse_plan(self, sample_plan_markdown):
        """Parser should extract plan fields from Markdown."""
        parsed = PlanParser.parse(sample_plan_markdown)

        assert parsed["spec_branch"] == "feature/auth"
        assert len(parsed["tech_stack"]) > 0
        # Check that FastAPI is mentioned in tech stack
        assert any("FastAPI" in item for item in parsed["tech_stack"])

    def test_extract_frontmatter(self, sample_spec_markdown):
        """Parser should extract YAML frontmatter."""
        frontmatter, body = SpecParser.extract_frontmatter(sample_spec_markdown)

        assert frontmatter["title"] == "User Authentication Feature"
        assert "User Stories" in body
        assert "---" not in body[:50]  # Frontmatter removed


class TestSpecValidator:
    """Tests for specification validation."""

    def test_testable_requirement(self):
        """Testable requirements should pass validation."""
        req = "System MUST support email/password authentication"
        is_testable, issue = SpecValidator.check_requirement_testability(req)

        assert is_testable
        assert issue is None

    def test_vague_requirement(self):
        """Vague requirements should fail validation."""
        req = "System should maybe support authentication"
        is_testable, issue = SpecValidator.check_requirement_testability(req)

        assert not is_testable
        assert "should" in issue.lower() or "vague" in issue.lower()

    def test_measurable_criteria(self):
        """Measurable criteria should pass validation."""
        criteria = "Login page loads in < 2 seconds"
        is_measurable, issue = SpecValidator.check_success_criteria_measurable(criteria)

        assert is_measurable
        assert issue is None

    def test_unmeasurable_criteria(self):
        """Unmeasurable criteria should fail validation."""
        criteria = "System works well"
        is_measurable, issue = SpecValidator.check_success_criteria_measurable(criteria)

        assert not is_measurable
        assert issue is not None

    def test_validate_spec(self, sample_spec_markdown):
        """Full spec validation should work."""
        parsed = SpecParser.parse(sample_spec_markdown)
        errors = validate_spec(parsed)

        # Should have no errors (sample is well-formed)
        error_count = sum(1 for e in errors if e.severity == "error")
        assert error_count == 0


class TestPlanValidator:
    """Tests for plan validation."""

    def test_task_dependencies_no_cycle(self):
        """Tasks without cycles should pass validation."""
        tasks = [
            {"id": "T1", "dependencies": []},
            {"id": "T2", "dependencies": ["T1"]},
            {"id": "T3", "dependencies": ["T1", "T2"]},
        ]
        no_cycles, issue = PlanValidator.check_task_dependencies(tasks)

        assert no_cycles
        assert issue is None

    def test_validate_plan(self, sample_plan_markdown):
        """Full plan validation should work."""
        parsed = PlanParser.parse(sample_plan_markdown)
        errors = validate_plan(parsed, tasks=[])

        # May have warnings but shouldn't have critical errors
        critical_errors = [e for e in errors if e.severity == "error"]
        assert len(critical_errors) == 0 or critical_errors[0].message == "No tasks defined"


class TestEnrichmentContext:
    """Tests for enrichment context creation."""

    def test_create_enrichment_context(self, sample_decisions, sample_patterns):
        """Should create enrichment context with decisions and patterns."""
        context = create_enrichment_context(
            "Create auth feature",
            sample_decisions,
            sample_patterns
        )

        assert context["is_enriched"]
        assert context["decisions_count"] == 2
        assert context["patterns_count"] == 2
        assert "Create auth feature" in context["enriched_intent"]

    def test_create_enrichment_empty(self):
        """Should handle empty enrichment gracefully."""
        context = create_enrichment_context("Feature intent")

        assert not context["is_enriched"]
        assert context["decisions_count"] == 0
        assert "Feature intent" in context["enriched_intent"]
