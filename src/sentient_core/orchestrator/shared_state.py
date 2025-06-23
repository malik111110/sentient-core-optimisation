# Shared State and Data Models for the Agentic Economy

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import UUID, uuid4

class Task(BaseModel):
    task_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the task.")
    department: str = Field(description="The department responsible for the task.")
    task: str = Field(description="A detailed description of the task to be performed.")
    status: str = Field(default="pending", description="The current status of the task.")
    sandbox_type: Optional[str] = Field(default=None, description="The type of sandbox environment required for the task (e.g., 'e2b', 'web-container').")
    input_data: Dict = Field(default_factory=dict, description="Data required for the task, such as parameters or content.")
    depends_on: List[UUID] = Field(default_factory=list, description="A list of task IDs that this task depends on.")

class Plan(BaseModel):
    project_name: str
    tasks: List[Task]

class AgenticState(BaseModel):
    initial_command: str
    plan: Plan = None
    completed_tasks: List[Dict] = []
    artifacts: Dict = Field(default_factory=dict, description="Paths to generated code, reports, etc.")
