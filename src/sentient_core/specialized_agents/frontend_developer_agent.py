from ..agents.base_agent import BaseAgent
from ..orchestrator.shared_state import Task
from typing import Optional, Any
from ..tools.webcontainer_tool import WebContainerToolInput, WebContainerTool
from typing import Dict, Any

class FrontendDeveloperAgent(BaseAgent):
    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="FrontendDeveloperAgent", sandbox_tool=sandbox_tool)

    def execute_task(self, task: Task) -> dict:
        self.log(f"Executing task: {task.task}")

        if not self.sandbox_tool or not isinstance(self.sandbox_tool, WebContainerTool):
            return {"status": "failed", "message": "FrontendDeveloperAgent requires a sandbox tool but none was provided."}

        # Generate a simple index.html string
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <title>Task</title>
  </head>
  <body>
    <h1>{task.task}</h1>
    <div id=\"backend-response\"></div>
    <script type=\"module\" src=\"bridge.js\"></script>
  </body>
</html>"""
        file_tree: Dict[str, Any] = {"index.html": html_content}

        try:
            # Prepare input for WebContainerTool
            tool_input = WebContainerToolInput(files=file_tree, commands=["serve"])
            self.log("Running file tree in WebContainer sandbox...")
            sandbox_result = self.sandbox_tool.run(tool_input)
            self.log(f"WebContainer sandbox execution finished.")

            # Format the result
            result = {
                "status": "completed",
                "message": f"Task '{task.task}' executed. URL: {sandbox_result.get('url', 'No URL')}",
                "artifacts": [sandbox_result.get('url')] if sandbox_result.get('url') else []
            }

        except Exception as e:
            self.log(f"An error occurred during sandbox execution: {e}")
            result = {"status": "failed", "message": f"Error executing task in sandbox: {e}"}

        self.log(f"Finished task: {task.task} with status: {result['status']}")
        return result
