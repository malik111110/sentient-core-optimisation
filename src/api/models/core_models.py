from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
import uuid

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    # Further agent configuration can be added here

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    input_data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    output_data: Optional[Dict[str, Any]] = None
