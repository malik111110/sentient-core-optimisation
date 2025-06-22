print("--- PYTHON SCRIPT EXECUTION STARTED ---") # ABSOLUTE FIRST LINE TEST
import sys
sys.stdout.flush() # FLUSH AFTER FIRST PRINT

# Main entry point for the Sentient-Core Agentic Factory

print("--- DEBUG: Before imports block ---"); sys.stdout.flush()
from .c_suite_planner import CSuitePlanner
print("--- DEBUG: After CSuitePlanner import attempt ---"); sys.stdout.flush()
# from .departmental_executors import DepartmentalExecutor
# print("--- DEBUG: After DepartmentalExecutor import attempt ---"); sys.stdout.flush()
from .shared_state import AgenticState, Plan, Task
print("--- DEBUG: After SharedState import attempt ---"); sys.stdout.flush()
print("--- DEBUG: After imports block (shared_state, c_suite_planner uncommented) ---"); sys.stdout.flush()

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

        # 2. Departmental Executors execute the plan using LangGraph workflow
        # The print statement: "Plan for project '{self.state.plan.project_name}' received. Executing tasks..." is already present before this block.
            
        # Pass the list of Task objects directly to the new execute_plan method
        execution_results = self.executor.execute_plan(self.state.plan.tasks)
            
        if execution_results.get("status") == "success":
            results_list = execution_results.get("results", [])
            # Create a mapping from task description to original Task object for easy update
            task_map = {task.task: task for task in self.state.plan.tasks}
                
            for result_detail in results_list:
                task_description = result_detail.get("task")
                task_status = result_detail.get("status") # This should be 'completed' from our mock
                if task_description in task_map:
                    original_task = task_map[task_description]
                    original_task.status = task_status # Update status on the Pydantic model instance
                    if task_status == 'completed':
                        self.state.completed_tasks.append(original_task)
                    else: # Handle other statuses if they become possible
                        print(f"Task '{original_task.task}' processed by LangGraph with status: {task_status}")
                else:
                    print(f"Warning: Result received from LangGraph for unknown task: {task_description}")
            print("\nAll tasks processed by Departmental Executor using LangGraph.")
        else:
            print("Departmental Executor (LangGraph) reported a failure in processing the plan.")
        
        print("\nAgentic Factory run complete.") # This replaces the old "All tasks executed..." print statement
        print(f"\n--- Final State ---")
        print(self.state.model_dump_json(indent=2))


if __name__ == "__main__":
    initial_command = "Test run."
    print(f"--- Starting Main Orchestrator with command: '{initial_command}' ---")
    sys.stdout.flush()
    try:
        factory = MainOrchestrator(command=initial_command)
        factory.run()
        print("--- Main Orchestrator run completed successfully. ---")
        sys.stdout.flush()
    except Exception as e:
        print(f"--- CRITICAL ERROR IN MAIN ORCHESTRATOR ---")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        # Optionally re-raise or handle as needed, for now, just printing
    finally:
        print("--- Main Orchestrator execution finished. ---")
        sys.stdout.flush()
