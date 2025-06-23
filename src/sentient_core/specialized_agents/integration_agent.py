from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState


class IntegrationAgent(BaseAgent):
    """Agent responsible for integration testing and glue-code generation (mock)."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="IntegrationAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        await self.log(workflow_id, task.id, f"Running integration task: {task.description}")
        # Placeholder: real integration logic would go here
        return {
            "message": f"Task '{task.description}' completed by {self.name}.",
            "artifacts": [],
        }
