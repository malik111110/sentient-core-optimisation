# Shared State and Data Models for the Agentic Economy

from pydantic import BaseModel, Field
from typing import List, Dict

class Task(BaseModel):
    department: str = Field(description="The department responsible for the task.")
    task: str = Field(description="A detailed description of the task to be performed.")
    status: str = Field(default="pending", description="The current status of the task.")

class Plan(BaseModel):
    project_name: str
    tasks: List[Task]

class AgenticState(BaseModel):
    initial_command: str
    plan: Plan = None
    completed_tasks: List[Dict] = []
    artifacts: Dict = Field(default_factory=dict, description="Paths to generated code, reports, etc.")
