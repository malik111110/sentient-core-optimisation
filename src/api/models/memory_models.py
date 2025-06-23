# Pydantic Models for SurrealDB Memory Layer

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, NewType
from enum import Enum
from uuid import UUID
from datetime import datetime

# SurrealDB specific ID type
SurrealID = NewType('SurrealID', str)

class NodeType(str, Enum):
    """Type of the memory node, indicating its content."""
    CONCEPT = "CONCEPT"
    CODE_SNIPPET = "CODE_SNIPPET"
    FILE = "FILE"
    USER_REQUEST = "USER_REQUEST"
    AGENT_ACTION = "AGENT_ACTION"
    ERROR = "ERROR"
    PLAN_STEP = "PLAN_STEP"

class EdgeType(str, Enum):
    """Type of relationship between two memory nodes."""
    RELATES_TO = "RELATES_TO"
    DEPENDS_ON = "DEPENDS_ON"
    GENERATES = "GENERATES"
    FIXES = "FIXES"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    CLARIFIES = "CLARIFIES"

# --- Memory Layer Models ---

class MemoryNode(BaseModel):
    """Represents a single node in the knowledge graph."""
    id: Optional[SurrealID] = Field(None, description="SurrealDB record ID, e.g., 'node:uuid'")
    node_type: NodeType
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    agent_id: Optional[UUID] = None # Link to the agent who created this memory
    task_id: Optional[UUID] = None # Link to the task this memory is associated with

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class MemoryEdge(BaseModel):
    """Represents a directed edge between two nodes in the knowledge graph."""
    id: Optional[SurrealID] = Field(None, description="SurrealDB record ID, e.g., 'edge:uuid'")
    source_node_id: SurrealID = Field(..., alias="in")
    target_node_id: SurrealID = Field(..., alias="out")
    edge_type: EdgeType
    weight: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class KnowledgeGraph(BaseModel):
    """Represents a subgraph of related memories."""
    nodes: List[MemoryNode]
    edges: List[MemoryEdge]
