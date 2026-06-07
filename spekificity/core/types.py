"""Type contracts and Pydantic models for Spekificity artifacts."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ────────────────────────────────────────────────────────────────
# Specification Models
# ────────────────────────────────────────────────────────────────

class UserScenario(BaseModel):
    """User story or acceptance scenario."""
    
    id: str = Field(..., description="User story ID (US-001, US-002)")
    title: str = Field(..., description="User story title")
    priority: str = Field(..., description="Priority (P0, P1, P2, P3)")
    description: str = Field(..., description="User story narrative")
    acceptance_criteria: List[str] = Field(default_factory=list, description="Acceptance criteria (Given-When-Then)")


class SuccessCriteria(BaseModel):
    """Measurable success criterion."""
    
    id: str = Field(..., description="Success criteria ID (SC-001, SC-002)")
    description: str = Field(..., description="Criterion description")
    measurable: bool = Field(default=True, description="Is this measurable/quantified?")
    target: Optional[str] = Field(None, description="Target value or threshold")


class Assumption(BaseModel):
    """Project assumption or constraint."""
    
    id: str = Field(..., description="Assumption ID (A-001, A-002)")
    description: str = Field(..., description="Assumption text")
    category: str = Field(default="general", description="Category (technical, business, scope, etc.)")


class Entity(BaseModel):
    """Domain entity or data structure."""
    
    name: str = Field(..., description="Entity name")
    description: str = Field(..., description="Entity description")
    fields: List[str] = Field(default_factory=list, description="Field names")


class Specification(BaseModel):
    """Complete feature specification."""
    
    title: str = Field(..., description="Feature title")
    branch: str = Field(..., description="Git branch name (e.g., 001-complete-framework)")
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None
    
    # Content
    user_scenarios: List[UserScenario] = Field(default_factory=list)
    success_criteria: List[SuccessCriteria] = Field(default_factory=list)
    assumptions: List[Assumption] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    
    # Metadata
    requirements: List[str] = Field(default_factory=list, description="Functional requirements (FR-001, etc.)")
    scope: str = Field(default="", description="Scope boundaries and exclusions")


# ────────────────────────────────────────────────────────────────
# Plan Models
# ────────────────────────────────────────────────────────────────

class Task(BaseModel):
    """Implementation task."""
    
    id: str = Field(..., description="Task ID (T1.1, T2.3, etc.)")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    
    # Execution
    priority: str = Field(..., description="Priority (P0=blocker, P1=critical, P2=unblocks, P3=polish)")
    dependencies: List[str] = Field(default_factory=list, description="Task IDs this depends on")
    estimated_tokens: int = Field(default=0, description="Estimated tokens for implementation")
    estimated_hours: float = Field(default=1.0, description="Estimated hours to complete")
    
    # Success
    acceptance_criteria: List[str] = Field(default_factory=list, description="Task acceptance criteria")
    success_indicators: List[str] = Field(default_factory=list, description="How to verify task complete")
    
    # Status
    status: str = Field(default="not-started", description="Status (not-started, in-progress, completed, blocked)")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Phase(BaseModel):
    """Implementation phase."""
    
    id: str = Field(..., description="Phase ID (Phase 1, Phase 2, etc.)")
    name: str = Field(..., description="Phase name")
    description: str = Field(..., description="Phase goals and deliverables")
    tasks: List[Task] = Field(default_factory=list)
    estimated_tokens: int = Field(default=0)
    estimated_weeks: float = Field(default=1.0)


class Plan(BaseModel):
    """Implementation plan."""
    
    spec_branch: str = Field(..., description="Feature branch name")
    spec_file: str = Field(..., description="Path to spec.md")
    created: datetime = Field(default_factory=datetime.utcnow)
    
    # Architecture
    architecture: str = Field(default="", description="Architecture overview")
    tech_stack: List[str] = Field(default_factory=list, description="Technology choices")
    
    # Phases & tasks
    phases: List[Phase] = Field(default_factory=list)
    
    # Analysis
    risks: List[dict] = Field(default_factory=list, description="Identified risks with mitigations")
    decisions: List[str] = Field(default_factory=list, description="Related decision IDs")


# ────────────────────────────────────────────────────────────────
# Decision & Knowledge Models
# ────────────────────────────────────────────────────────────────

class Decision(BaseModel):
    """Architectural decision record."""
    
    id: str = Field(..., description="Decision ID (dec-001, dec-002)")
    title: str = Field(..., description="Decision title")
    status: str = Field(..., description="Status (approved, proposed, rejected, superseded)")
    date: datetime = Field(default_factory=datetime.utcnow)
    author: str = Field(default="", description="Decision author/owner")
    
    # Content
    problem: str = Field(default="", description="Problem statement")
    decision: str = Field(default="", description="What was decided")
    rationale: str = Field(default="", description="Why this decision")
    implications: List[str] = Field(default_factory=list, description="Consequences")
    alternatives: List[str] = Field(default_factory=list, description="Alternatives considered")


class Pattern(BaseModel):
    """Reusable design pattern."""
    
    id: str = Field(..., description="Pattern ID (pat-001, pat-002)")
    title: str = Field(..., description="Pattern name")
    category: str = Field(default="general", description="Pattern category (Architecture, Workflow, etc.)")
    created: datetime = Field(default_factory=datetime.utcnow)
    author: str = Field(default="", description="Pattern author")
    status: str = Field(default="approved", description="Status (approved, draft, deprecated)")
    
    # Content
    problem: str = Field(default="", description="Problem this pattern solves")
    solution: str = Field(default="", description="Pattern description")
    example: str = Field(default="", description="Code or workflow example")
    when_to_use: str = Field(default="", description="When to apply this pattern")
    when_not_to_use: str = Field(default="", description="When NOT to use this pattern")


class Lesson(BaseModel):
    """Lesson learned from completed feature."""
    
    id: str = Field(default="", description="Lesson ID (optional)")
    feature: str = Field(..., description="Feature name")
    date: datetime = Field(default_factory=datetime.utcnow)
    author: str = Field(default="", description="Author of lesson")
    
    # Outcomes
    outcomes: str = Field(default="", description="What was actually built")
    spec_alignment: str = Field(default="", description="How aligned with original spec")
    
    # Learning
    lessons_learned: List[str] = Field(default_factory=list, description="Key learnings")
    surprises: List[str] = Field(default_factory=list, description="Unexpected outcomes")
    
    # Knowledge extraction
    new_patterns: List[str] = Field(default_factory=list, description="New patterns identified")
    new_decisions: List[str] = Field(default_factory=list, description="New decisions made")
    refined_patterns: List[str] = Field(default_factory=list, description="Patterns refined based on this feature")


# ────────────────────────────────────────────────────────────────
# Context Models
# ────────────────────────────────────────────────────────────────

class CodeContext(BaseModel):
    """Relevant code sections for a task."""
    
    file_path: str = Field(..., description="File path")
    line_range: Optional[tuple[int, int]] = Field(None, description="(start_line, end_line)")
    snippet: str = Field(default="", description="Code snippet")
    relevance: str = Field(default="high", description="Relevance (high, medium, low)")


class TaskContext(BaseModel):
    """Complete context for executing a task."""
    
    task_id: str = Field(..., description="Task ID")
    task_description: str = Field(...)
    
    # Relevant knowledge
    decisions: List[Decision] = Field(default_factory=list, description="Relevant past decisions")
    patterns: List[Pattern] = Field(default_factory=list, description="Relevant patterns")
    code: List[CodeContext] = Field(default_factory=list, description="Relevant code sections")
    
    # Execution context
    working_directory: str = Field(default="", description="Working directory for this task")
    environment: dict = Field(default_factory=dict, description="Environment variables")
    
    # Metadata
    estimated_tokens: int = Field(default=0)
    context_compressed: bool = Field(default=False, description="Is context compressed with Caveman?")


# ────────────────────────────────────────────────────────────────
# Progress & Session Models
# ────────────────────────────────────────────────────────────────

class ProgressLog(BaseModel):
    """Task progress log entry."""
    
    task_id: str = Field(..., description="Task ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str = Field(..., description="Action taken (started, progressed, completed, failed)")
    details: str = Field(default="", description="Details of action")
    decisions_made: List[str] = Field(default_factory=list, description="Decisions logged during task")


class SessionSummary(BaseModel):
    """Summary of a development session."""
    
    feature: str = Field(..., description="Feature name")
    started: datetime = Field(default_factory=datetime.utcnow)
    ended: Optional[datetime] = None
    tasks_completed: List[str] = Field(default_factory=list, description="Task IDs completed")
    decisions_logged: List[str] = Field(default_factory=list, description="Decision IDs created")
    lessons_identified: List[str] = Field(default_factory=list, description="Lessons learned")
    token_usage: int = Field(default=0, description="Total tokens used in session")
