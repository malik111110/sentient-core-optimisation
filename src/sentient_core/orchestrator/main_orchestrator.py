# Main entry point for the Sentient-Core Agentic Factory

from .c_suite_planner import CSuitePlanner
from .departmental_executors import DepartmentalExecutor
from .shared_state import AgenticState, Plan, Task

class MainOrchestrator:
    def __init__(self, command: str):
        print("Agentic Factory Initializing...")
        self.state = AgenticState(initial_command=command)
        self.planner = CSuitePlanner()
        self.executor = DepartmentalExecutor()
        print("Agentic Factory Initialized.")

    def run(self):
        print(f"Executing command: {self.state.initial_command}")
        
        # 1. C-Suite Planner creates the plan
        plan_dict = self.planner.create_plan(self.state.initial_command)
        
        # Validate and store the plan in the shared state using Pydantic models
        self.state.plan = Plan(**plan_dict)
        
        print(f"Plan for project '{self.state.plan.project_name}' received. Executing tasks...")

        # 2. Departmental Executors execute the plan task by task
        for task in self.state.plan.tasks:
            task.status = 'in_progress'
            success = self.executor.execute_task(task.model_dump())
            
            if success:
                task.status = 'completed'
                self.state.completed_tasks.append(task)
            else:
                task.status = 'failed'
                print(f"Task failed: {task.task}. Halting execution.")
                break
        
        print("\nAll tasks executed. Factory run complete.")
        print(f"\n--- Final State ---")
        print(self.state.model_dump_json(indent=2))


if __name__ == "__main__":
    initial_command = "Build a competitive intelligence dashboard for pharma."
    factory = MainOrchestrator(command=initial_command)
    factory.run()
