from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState


class ResearchAgent(BaseAgent):
    """Agent responsible for research tasks such as web searching and summarisation (mock)."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="ResearchAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        await self.log(workflow_id, task.id, f"Performing research task: {task.description}")
        # Placeholder: actual research logic would integrate search_web / retrieval tools.
        summary = f"Dummy summary for task: {task.description}"
        return {
            "summary": summary,
        }
