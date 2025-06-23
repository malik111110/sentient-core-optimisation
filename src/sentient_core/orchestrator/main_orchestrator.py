import asyncio
from typing import List
from .c_suite_planner import CSuitePlanner
from .departmental_executors import DepartmentalExecutor
from .shared_state import Plan, Task, OrchestratorState
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MainOrchestrator:
    def __init__(self, command: str):
        self.command = command
        self.planner = CSuitePlanner()
        self.executor = DepartmentalExecutor()
        self.state = OrchestratorState(plan=None, completed_tasks=[], final_result=None)
        logger.info("MainOrchestrator initialized.")

    async def run(self):
        logger.info(f"Received command: '{self.command}'. Starting orchestration.")
        
        # 1. Create a plan
        logger.info("Creating a plan...")
        plan_dict = self.planner.create_plan(self.command)
        tasks = [Task(**task_data) for task_data in plan_dict['tasks']]
        self.state.plan = Plan(project_name=plan_dict['project_name'], tasks=tasks)
        logger.info(f"Plan created for project: '{self.state.plan.project_name}' with {len(tasks)} tasks.")

        # 2. Execute the plan
        logger.info("Executing the plan...")
        execution_result = await self.executor.execute_plan(self.state.plan.tasks)
        
        # 3. Process results
        if execution_result["status"] == "success":
            logger.info("Plan execution completed successfully.")
            self.state.completed_tasks = execution_result["results"]
            self.state.final_result = "Orchestration successful."
        else:
            logger.error(f"Plan execution failed: {execution_result.get('error')}")
            self.state.completed_tasks = execution_result.get("results", [])
            self.state.final_result = f"Orchestration failed: {execution_result.get('error')}"

        logger.info("Orchestration finished.")

    @staticmethod
    def main(command: str):
        orchestrator = MainOrchestrator(command)
        asyncio.run(orchestrator.run())
        return orchestrator.state
