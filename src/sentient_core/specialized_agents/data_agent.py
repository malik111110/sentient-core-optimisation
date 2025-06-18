from ..orchestrator.base_agent import BaseAgent
from ..orchestrator.shared_state import Task

class DataAgent(BaseAgent):
    def __init__(self, name: str = "DataAgent"):
        super().__init__(name)

    def execute_task(self, task: Task) -> dict:
        self.log(f"Executing task: {task.task}")
        # Mock execution
        result = {"status": "completed", "message": f"Task '{task.task}' completed by {self.name}.", "artifacts": []}
        self.log(f"Finished task: {task.task} with status: {result['status']}")
        return result
