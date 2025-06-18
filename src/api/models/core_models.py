from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
from uuid import UUID
from datetime import datetime

# --- Enums ---
class AgentStatus(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    PROVISIONING = "PROVISIONING"
    ERROR = "ERROR"

class TaskStatus(str, Enum): # Re-affirming existing TaskStatus
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# --- Agent Models ---
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    config: Optional[Dict[str, Any]] = None

class AgentCreate(AgentBase):
    # You can add specific fields for creation if they differ from AgentBase
    # For now, it inherits all fields.
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    status: Optional[AgentStatus] = None
    config: Optional[Dict[str, Any]] = None

class AgentRead(AgentBase):
    agent_id: UUID
    status: AgentStatus = AgentStatus.INACTIVE
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Task Models ---
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    priority: int = 0
    dependencies: List[UUID] = Field(default_factory=list)

class TaskCreate(TaskBase):
    agent_id: Optional[UUID] = None # Agent can be assigned at creation or later

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    agent_id: Optional[UUID] = None
    input_data: Optional[Dict[str, Any]] = None # Allow updating input
    output_data: Optional[Dict[str, Any]] = None # Allow setting/updating output
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    dependencies: Optional[List[UUID]] = None

class TaskRead(TaskBase):
    task_id: UUID
    agent_id: Optional[UUID] = None
    status: TaskStatus = TaskStatus.PENDING
    output_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
