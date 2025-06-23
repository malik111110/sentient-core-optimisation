# Departmental Executor Agents using LangGraph

from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from .shared_state import Task # Task is defined in shared_state.py within the same orchestrator package
from ..tools import E2BSandboxTool, WebContainerTool
from ..specialized_agents import (
    ResearchAgent,
    DataAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    IntegrationAgent,
    DeploymentAgent
)
import logging # Ensure logging is imported

logger = logging.getLogger(__name__) # Ensure logger is defined

# Define the state for our LangGraph
class ExecutorGraphState(TypedDict):
    tasks_to_process: List[Task]
    current_task_index: int
    current_task_result: Any
    completed_task_outputs: List[Any]
    error_message: str

class DepartmentalExecutor:
    def __init__(self):
        self.workflow = StateGraph(ExecutorGraphState)
        self.e2b_tool = E2BSandboxTool()
        self.webcontainer_tool = WebContainerTool()
        self._setup_graph()
        self.app = self.workflow.compile()

        self.agent_mapping = {
            "Research": ResearchAgent,
            "Data": DataAgent,
            "BackendDevelopment": BackendDeveloperAgent,
            "FrontendDevelopment": FrontendDeveloperAgent,
            "Integration": IntegrationAgent,
            "Deployment": DeploymentAgent
            # Add other departments and their corresponding agents here
        }
        print("DepartmentalExecutor initialized with LangGraph workflow.")

    def _setup_graph(self):
        # Define nodes
        self.workflow.add_node("get_next_task", self._get_next_task)
        self.workflow.add_node("execute_single_task", self._execute_single_task)
        self.workflow.add_node("handle_error", self._handle_error)

        # Define edges
        self.workflow.set_entry_point("get_next_task")
        self.workflow.add_conditional_edges(
            "get_next_task",
            self._decide_to_execute_or_finish,
            {
                "execute": "execute_single_task",
                "finish": END,
            }
        )
        # self.workflow.add_edge("execute_single_task", "get_next_task") # Replaced by conditional edge below
        self.workflow.add_conditional_edges(
            "execute_single_task",
            self._check_task_outcome,
            {
                "success": "get_next_task",
                "error": "handle_error"
            }
        )
        self.workflow.add_edge("handle_error", END) # End if error occurs

    def _check_task_outcome(self, state: ExecutorGraphState) -> str:
        print("[LangGraph Router]: Checking task outcome...")
        if state.get('error_message') and state['error_message'] != '':
            print(f"[LangGraph Router]: Task failed with message: {state['error_message']}")
            return "error"
        else:
            print("[LangGraph Router]: Task succeeded or no error reported.")
            return "success"

    def _get_next_task(self, state: ExecutorGraphState) -> ExecutorGraphState:
        print("[LangGraph Router]: Getting next task...")
        current_index = state.get('current_task_index', 0)
        tasks = state.get('tasks_to_process', [])
        if current_index < len(tasks):
            task = tasks[current_index]
            print(f"[LangGraph Router]: Next task is '{task.task}' for department '{task.department}'.")
            return {**state, "current_task_index": current_index + 1, "current_task_result": None}
        else:
            print("[LangGraph Router]: No more tasks to process.")
            return {**state, "current_task_result": "All tasks processed"}

    def _decide_to_execute_or_finish(self, state: ExecutorGraphState) -> str:
        print("[LangGraph Router]: Deciding next step...")
        if state.get("current_task_result") == "All tasks processed":
            print("[LangGraph Router]: Decision: Finish.")
            return "finish"
        else:
            # This implies _get_next_task found a task and current_task_index is valid for the *next* task
            print("[LangGraph Router]: Decision: Execute next task.")
            return "execute"

    def _execute_single_task(self, state: ExecutorGraphState) -> ExecutorGraphState:
        current_task_index = state['current_task_index'] -1 # Index of the task just identified by _get_next_task
        task_object_to_execute = state['tasks_to_process'][current_task_index]
        department = task_object_to_execute.department
        task_description = task_object_to_execute.task
        completed_outputs = state.get('completed_task_outputs', [])
        # Create a map of completed task IDs to their full output for easy lookup
        completed_task_map = {t['task_id']: t for t in completed_outputs}

        # Check for dependencies and inject their output
        if task_object_to_execute.depends_on:
            for dep_id in task_object_to_execute.depends_on:
                if dep_id in completed_task_map:
                    dependency_output = completed_task_map[dep_id]
                    # Inject the artifact from the parent task into the current task's input_data
                    if dependency_output.get('artifacts'):
                        # Assuming the first artifact is the primary content
                        task_object_to_execute.input_data['content'] = dependency_output['artifacts'][0]
                else:
                    # This case should ideally be handled by a more robust dependency resolution logic
                    logger.warning(f"Dependency task {dep_id} not found in completed tasks.")

        logger.info(f"[{department} Executor - LangGraph Node]: Preparing task - '{task_description}'")

        agent_class = self.agent_mapping.get(department)
        if not agent_class:
            logger.error(f"No agent class found for department: {department}")
            error_message = f"No agent configured for department {department}"
            completed_outputs.append({"task": task_description, "result": error_message, "status": "failed"})
            return {**state, 
                    "current_task_result": f"Error: No agent for department {department}", 
                    "error_message": error_message,
                    "completed_task_outputs": completed_outputs}

        try:
            # Select the appropriate tool based on the task's requirements
            sandbox_type = task_object_to_execute.sandbox_type
            selected_tool = None
            if sandbox_type == 'e2b':
                selected_tool = self.e2b_tool
            elif sandbox_type == 'webcontainer':
                selected_tool = self.webcontainer_tool

            agent_instance = agent_class(sandbox_tool=selected_tool) # Instantiate the agent with the tool
            logger.info(f"Instantiated agent: {agent_instance.name} for task: {task_description}")
            
            # Call the agent's execute_task method, passing the full Task Pydantic model
            execution_outcome = agent_instance.execute_task(task_object_to_execute)
            logger.info(f"Agent {agent_instance.name} finished task '{task_description}' with outcome: {execution_outcome}")

            task_status = execution_outcome.get("status", "failed")
            message = execution_outcome.get("message", "No message from agent.")
            error_details = execution_outcome.get("error_details", "")
            artifacts = execution_outcome.get("artifacts", []) # Capture artifacts

            completed_outputs.append({
                "task_id": task_object_to_execute.task_id, # Store the task_id for dependency tracking
                "task": task_description, 
                "result": message, 
                "status": task_status, 
                "artifacts": artifacts
            })

            if task_status == "completed":
                return {**state, "current_task_result": message, "error_message": "", "completed_task_outputs": completed_outputs}
            else:
                logger.error(f"Task '{task_description}' failed. Agent message: {message}. Details: {error_details}")
                return {**state, "current_task_result": f"Task Failed: {message}", "error_message": error_details or message, "completed_task_outputs": completed_outputs}

        except Exception as e:
            logger.exception(f"Exception during agent execution for task '{task_description}': {e}")
            critical_error_message = f"Critical Error: Exception during agent execution for {task_description}: {str(e)}"
            completed_outputs.append({"task": task_description, "result": critical_error_message, "status": "failed"})
            return {**state, 
                    "current_task_result": critical_error_message, 
                    "error_message": str(e),
                    "completed_task_outputs": completed_outputs}

    def _handle_error(self, state: ExecutorGraphState) -> ExecutorGraphState:
        error_msg = state.get('error_message', 'Unknown error')
        print(f"[LangGraph Error Handler]: An error occurred: {error_msg}")
        return {**state}

    def execute_plan(self, tasks: List[Task]) -> Dict[str, Any]:
        print(f"DepartmentalExecutor: Received plan with {len(tasks)} tasks. Invoking LangGraph workflow...")
        initial_state = ExecutorGraphState(
            tasks_to_process=tasks,
            current_task_index=0,
            current_task_result=None,
            completed_task_outputs=[],
            error_message=''
        )
        
        final_state = self.app.invoke(initial_state)
        print("DepartmentalExecutor: LangGraph workflow complete.")
        return {"status": "success", "results": final_state.get('completed_task_outputs', [])}

    # This method needs to be adapted or removed if execute_plan is the new entry point
    def execute_task(self, task_details: dict) -> bool:
        # This method is now superseded by execute_plan which processes a list of tasks.
        # For compatibility with the current main_orchestrator, we can simulate a single task execution
        # or update main_orchestrator to call execute_plan directly.
        # For now, let's make it compatible by wrapping the single task.
        print("[Deprecation Warning]: execute_task is called. Consider using execute_plan for multi-task execution.")
        mock_task_obj = Task(department=task_details.get('department', 'Unknown'), 
                             task=task_details.get('task', 'Unknown Task'), 
                             status='pending')
        result = self.execute_plan([mock_task_obj])
        return result['status'] == 'success' and len(result['results']) > 0
