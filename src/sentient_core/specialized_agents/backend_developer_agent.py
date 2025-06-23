from ..agents.base_agent import BaseAgent
from ..orchestrator.shared_state import Task
from typing import Optional, Any
from ..tools.e2b_sandbox_tool import E2BSandboxToolInput

class BackendDeveloperAgent(BaseAgent):
    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="BackendDeveloperAgent", sandbox_tool=sandbox_tool)

    def execute_task(self, task: Task) -> dict:
        self.log(f"Executing task: {task.task}")

        if not self.sandbox_tool:
            return {"status": "failed", "message": "BackendDeveloperAgent requires a sandbox tool but none was provided."}

        # Assume the task description is a Python script for now
        # In a real scenario, this would involve more complex generation
        script_to_run = task.task
        
        try:
            # Use the E2BSandboxTool
            tool_input = E2BSandboxToolInput(language='python', script=script_to_run)
            self.log(f"Running script in E2B sandbox...")
            sandbox_result = self.sandbox_tool.run(tool_input)
            self.log(f"E2B sandbox execution finished.")

            # Format the result
            result = {
                "status": "completed",
                "message": f"Task '{task.task}' executed. Output: {sandbox_result.get('output', 'No output')}",
                "artifacts": sandbox_result.get('artifacts', [])
            }

        except Exception as e:
            self.log(f"An error occurred during sandbox execution: {e}")
            result = {"status": "failed", "message": f"Error executing task in sandbox: {e}"}

        self.log(f"Finished task: {task.task} with status: {result['status']}")
        return result
