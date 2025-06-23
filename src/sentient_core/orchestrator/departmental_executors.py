# Departmental Executor Agents using LangGraph

import asyncio
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from .shared_state import Task
from ..tools import E2BSandboxTool, WebContainerTool
from ..specialized_agents import (
    ResearchAgent,
    DataAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    IntegrationAgent,
    DeploymentAgent,
    BridgeAgent,
)
import logging

logger = logging.getLogger(__name__)

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
            "Bridge": BridgeAgent,
            "Integration": IntegrationAgent,
            "Deployment": DeploymentAgent
        }
        logger.info("DepartmentalExecutor initialized with LangGraph workflow.")

    def _setup_graph(self):
        self.workflow.add_node("get_next_task", self._get_next_task)
        self.workflow.add_node("execute_single_task", self._execute_single_task)
        self.workflow.add_node("handle_error", self._handle_error)
        self.workflow.set_entry_point("get_next_task")
        self.workflow.add_conditional_edges(
            "get_next_task",
            lambda s: "execute_single_task" if s.get('current_task_index', 0) < len(s.get('tasks_to_process', [])) else END
        )
        self.workflow.add_conditional_edges(
            "execute_single_task",
            lambda s: "handle_error" if s.get('error_message') else "get_next_task"
        )
        self.workflow.add_edge("handle_error", END)

    def _get_next_task(self, state: ExecutorGraphState) -> ExecutorGraphState:
        current_index = state.get('current_task_index', 0)
        logger.info(f"[LangGraph Router]: Getting task at index {current_index}.")
        return {**state, "current_task_index": current_index + 1}

    async def _execute_single_task(self, state: ExecutorGraphState) -> ExecutorGraphState:
        current_index = state['current_task_index'] - 1
        task = state['tasks_to_process'][current_index]
        logger.info(f"Executing task: {task.task}")

        try:
            if task.depends_on:
                logger.info(f"Task '{task.task}' has dependencies. Injecting outputs.")
                task_map = {t.task_id: t for t in state['tasks_to_process']}
                for dep_id in task.depends_on:
                    dep_output = next((o for o in state['completed_task_outputs'] if o.get('task_id') == dep_id), None)
                    if dep_output and dep_id in task_map:
                        dep_task = task_map[dep_id]
                        if dep_task.department == "FrontendDevelopment":
                            task.input_data['frontend_url'] = dep_output.get('url')
                        elif dep_task.department == "BackendDevelopment":
                            task.input_data['backend_url'] = dep_output.get('url')
                        elif 'artifacts' in dep_output and dep_output['artifacts']:
                            task.input_data['content'] = dep_output['artifacts'][0]

            agent_class = self.agent_mapping.get(task.department)
            if not agent_class:
                raise ValueError(f"No agent for department: {task.department}")

            # Get the appropriate sandbox tool based on task requirements
            sandbox_tool = None
            if hasattr(task, 'sandbox_type') and task.sandbox_type:
                sandbox_tool = (
                    self.webcontainer_tool 
                    if task.sandbox_type.lower() == 'webcontainer' 
                    else self.e2b_tool
                )
            
            # Initialize agent with sandbox tool
            agent = agent_class(sandbox_tool=sandbox_tool)
            
            # Execute the task with proper async handling
            result = await agent.execute_task(task=task)

            result_with_id = {**result, "task_id": task.task_id}
            completed_outputs = state['completed_task_outputs'] + [result_with_id]

            if result.get("status") == "failed":
                return {**state, "error_message": result.get('message'), "completed_task_outputs": completed_outputs}

            return {**state, "current_task_result": result_with_id, "completed_task_outputs": completed_outputs}

        except Exception as e:
            logger.exception(f"Critical error executing task '{task.task}': {e}")
            return {**state, "error_message": str(e)}

    def _handle_error(self, state: ExecutorGraphState) -> ExecutorGraphState:
        logger.error(f"Handling error: {state.get('error_message')}")
        return {**state}

    async def execute_plan(self, tasks: List[Task]) -> Dict[str, Any]:
        logger.info(f"Executing plan with {len(tasks)} tasks.")
        initial_state = ExecutorGraphState(
            tasks_to_process=tasks, current_task_index=0, completed_task_outputs=[], error_message=''
        )
        final_state = await self.app.ainvoke(initial_state)

        if final_state.get('error_message'):
            return {"status": "failed", "results": final_state.get('completed_task_outputs', []), "error": final_state.get('error_message')}

        return {"status": "success", "results": final_state.get('completed_task_outputs', [])}