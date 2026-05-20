"""Pydantic models for core concepts."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path


class MemoryLayer(BaseModel):
    """Base model for memory layer data."""
    
    layer_type: str  # "user", "session", or "repo"
    loaded_at: datetime = Field(default_factory=datetime.now)
    source_path: Optional[Path] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UserMemory(MemoryLayer):
    """User-level persistent memory."""
    
    layer_type: str = "user"
    preferences: Dict[str, Any] = Field(default_factory=dict)
    skills: List[str] = Field(default_factory=list)
    patterns: Dict[str, Any] = Field(default_factory=dict)


class SessionMemory(MemoryLayer):
    """Session-scoped memory."""
    
    layer_type: str = "session"
    feature_state: Optional[Dict[str, Any]] = None
    decisions_made: List[str] = Field(default_factory=list)
    progress: Optional[str] = None


class RepoMemory(MemoryLayer):
    """Repository-scoped memory."""
    
    layer_type: str = "repo"
    architectural_decisions: Dict[str, Any] = Field(default_factory=dict)
    patterns_index: Dict[str, Any] = Field(default_factory=dict)
    vault_specs: Dict[str, Any] = Field(default_factory=dict)
    lessons: Dict[str, Any] = Field(default_factory=dict)


class Context(BaseModel):
    """Project context (3-layer memory model)."""
    
    feature_name: Optional[str] = None
    user_memory: Optional[UserMemory] = None
    session_memory: Optional[SessionMemory] = None
    repo_memory: Optional[RepoMemory] = None
    code_graph: Optional[Dict[str, Any]] = None
    loaded_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        arbitrary_types_allowed = True


class FeatureState(BaseModel):
    """Feature state tracker."""
    
    feature_name: str
    status: str = "pending"  # pending, specify, plan, implement, post, archived
    created_at: datetime = Field(default_factory=datetime.now)
    branch_name: Optional[str] = None
    spec_file: Optional[Path] = None
    plan_file: Optional[Path] = None
    tasks_file: Optional[Path] = None
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class VaultSpec(BaseModel):
    """Spec from vault."""
    
    name: str
    path: Path
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True


class ArchitecturalDecision(BaseModel):
    """Architectural decision record."""
    
    id: str
    title: str
    status: str  # accepted, rejected, superseded, deprecated
    context: str
    decision: str
    consequences: str
    date_created: datetime
    
    class Config:
        arbitrary_types_allowed = True


class Pattern(BaseModel):
    """Reusable pattern."""
    
    name: str
    category: str  # code, architecture, process, etc.
    description: str
    when_to_use: str
    example_file: Optional[Path] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True


class Lesson(BaseModel):
    """Lesson learned from feature."""
    
    feature_name: str
    date: datetime
    title: str
    insight: str
    actionable: bool = False
    related_patterns: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True


class CodeGraphNode(BaseModel):
    """Code graph node (symbol, file, module, etc.)."""
    
    node_id: str
    node_type: str  # file, function, class, module, etc.
    name: str
    path: Optional[Path] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class CodeGraphEdge(BaseModel):
    """Code graph edge (relationship between nodes)."""
    
    source_id: str
    target_id: str
    edge_type: str  # calls, references, imports, inherits, etc.
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ImpactAnalysis(BaseModel):
    """Impact analysis result."""
    
    symbol: str
    affected_files: List[Path] = Field(default_factory=list)
    affected_symbols: List[str] = Field(default_factory=list)
    risk_level: str = "medium"  # low, medium, high
    recommendations: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
