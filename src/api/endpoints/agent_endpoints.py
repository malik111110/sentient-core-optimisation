from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict
from src.api.models.core_models import Agent, Task, TaskStatus

router = APIRouter()

# In-memory storage (for now, will be replaced by database)
db_agents: Dict[str, Agent] = {}
db_tasks: Dict[str, Task] = {}

@router.post("/agents/", response_model=Agent, status_code=201)
async def create_agent(agent: Agent = Body(...)):
    """
    Create a new agent.
    """
    if agent.id in db_agents:
        raise HTTPException(status_code=409, detail="Agent with this ID already exists")
    db_agents[agent.id] = agent
    return agent

@router.get("/agents/", response_model=List[Agent])
async def list_agents():
    """
    Get a list of all available agents.
    """
    return list(db_agents.values())

@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """
    Retrieve a specific agent by its ID.
    """
    if agent_id not in db_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agents[agent_id]

@router.post("/agents/{agent_id}/tasks", response_model=Task, status_code=202)
async def create_task_for_agent(agent_id: str, task_input: Dict = Body(...)):
    """
    Create and start a new task for a specific agent.
    """
    if agent_id not in db_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    new_task = Task(agent_id=agent_id, input_data=task_input)
    db_tasks[new_task.id] = new_task
    
    # In a real scenario, this would trigger the agent to run the task asynchronously
    # For now, we'll just set it to RUNNING
    new_task.status = TaskStatus.RUNNING
    
    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task_status(task_id: str):
    """
    Get the status and result of a specific task.
    """
    if task_id not in db_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_tasks[task_id]
