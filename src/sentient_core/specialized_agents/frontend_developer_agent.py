from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState
from ..tools.webcontainer_tool import WebContainerTool, WebContainerToolInput


class FrontendDeveloperAgent(BaseAgent):
    """Specialized agent for running simple web applications in a WebContainer sandbox."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="FrontendDeveloperAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        """Creates an index.html file and serves it in a WebContainer."""
        if not self.sandbox_tool or not isinstance(self.sandbox_tool, WebContainerTool):
            raise ValueError(
                "FrontendDeveloperAgent requires a WebContainerTool but none was provided."
            )

        # Generate a simple index.html string
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <title>Task</title>
  </head>
  <body>
    <h1>{task.description}</h1>
    <div id=\"backend-response\"></div>
    <script type=\"module\" src=\"./src/bridge.js\"></script>
  </body>
</html>"""
        file_tree: Dict[str, Any] = {"index.html": html_content}

        # Prepare input for WebContainerTool
        tool_input = WebContainerToolInput(files=file_tree, commands=["serve"])
        await self.log(workflow_id, task.id, "Running file tree in WebContainer sandbox...")
        sandbox_result = await self.sandbox_tool.run(tool_input)
        await self.log(workflow_id, task.id, "WebContainer sandbox execution finished.")

        url = sandbox_result.get("url")
        return {
            "message": f"Task '{task.description}' executed. URL: {url}",
            "artifacts": [url] if url else [],
        }
