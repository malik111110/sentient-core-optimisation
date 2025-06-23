from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState
from ..tools.e2b_sandbox_tool import E2BSandboxToolInput


class BackendDeveloperAgent(BaseAgent):
    """Specialized agent for executing Python code in an E2B sandbox."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="BackendDeveloperAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        """Runs a Python script provided in the task description inside an E2B sandbox."""
        if not self.sandbox_tool:
            raise ValueError(
                "BackendDeveloperAgent requires a sandbox tool but none was provided."
            )

        script_to_run = task.description

        # Use the E2BSandboxTool
        tool_input = E2BSandboxToolInput(language="python", script=script_to_run)
        await self.log(workflow_id, task.id, "Running script in E2B sandbox...")

        sandbox_result = await self.sandbox_tool.run(tool_input)

        await self.log(workflow_id, task.id, "E2B sandbox execution finished.")

        # The returned dictionary will be automatically placed in the 'output_data' field.
        return {
            "output": sandbox_result.get("output", "No output"),
            "artifacts": sandbox_result.get("artifacts", []),
        }
