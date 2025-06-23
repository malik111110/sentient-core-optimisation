from __future__ import annotations

"""Central Pydantic models for persisted workflow state and agent events.

These models map 1-to-1 to SurrealDB tables.  They are intentionally minimal –
only data that must survive restarts or be queried by other components is
stored here.  All runtime-only fields belong in in-memory classes.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskState(BaseModel):
    """Persisted representation of a single task inside a workflow."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="task_id")
    department: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, str] = Field(default_factory=dict)
    output_data: Dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class WorkflowStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowState(BaseModel):
    """Top-level workflow document stored in SurrealDB."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="workflow_id")
    project_name: str
    tasks: List[TaskState]
    status: WorkflowStatus = WorkflowStatus.RUNNING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class EventType(str, Enum):
    AGENT_STARTED = "agent_started"
    TASK_PROGRESS = "task_progress"
    AGENT_COMPLETED = "agent_completed"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"


class AgentEvent(BaseModel):
    """Event emitted by an agent or the orchestrator."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="event_id")
    event_type: EventType
    source_agent: str
    workflow_id: str
    task_id: Optional[str] = None
    payload: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
