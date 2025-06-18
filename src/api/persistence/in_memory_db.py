from typing import Dict, List, Optional, Union
import uuid
from datetime import datetime, timezone

from ..models.core_models import AgentRead, AgentCreate, AgentUpdate, TaskRead, TaskCreate, TaskUpdate, AgentStatus, TaskStatus

# In-memory data stores
db_agents: Dict[uuid.UUID, AgentRead] = {}
db_tasks: Dict[uuid.UUID, TaskRead] = {}

# --- Agent Persistence Functions ---
def get_agent(agent_id: uuid.UUID) -> Optional[AgentRead]:
    return db_agents.get(agent_id)

def get_agents(skip: int = 0, limit: int = 100) -> List[AgentRead]:
    return list(db_agents.values())[skip : skip + limit]

def create_agent(agent_create: AgentCreate) -> AgentRead:
    now = datetime.now(timezone.utc)
    new_agent_id = uuid.uuid4()
    # Create an AgentRead instance from AgentCreate data
    agent_data = agent_create.model_dump()
    agent = AgentRead(
        **agent_data, # Unpack fields from AgentCreate
        agent_id=new_agent_id,
        status=AgentStatus.INACTIVE, # Default status on creation
        created_at=now,
        updated_at=now
    )
    db_agents[new_agent_id] = agent
    return agent

def update_agent(agent_id: uuid.UUID, agent_update: AgentUpdate) -> Optional[AgentRead]:
    agent = db_agents.get(agent_id)
    if agent:
        update_data = agent_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(agent, key, value)
        agent.updated_at = datetime.now(timezone.utc)
        db_agents[agent_id] = agent # Ensure the updated agent is stored back
        return agent
    return None

def delete_agent(agent_id: uuid.UUID) -> Optional[AgentRead]:
    return db_agents.pop(agent_id, None)

# --- Task Persistence Functions ---
def get_task(task_id: uuid.UUID) -> Optional[TaskRead]:
    return db_tasks.get(task_id)

def get_tasks(agent_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 100) -> List[TaskRead]:
    tasks_list = []
    if agent_id:
        for task_obj in db_tasks.values(): # Renamed to avoid conflict with 'task' variable in loop
            if task_obj.agent_id == agent_id:
                tasks_list.append(task_obj)
    else:
        tasks_list = list(db_tasks.values())
    return tasks_list[skip : skip + limit]

def create_task(task_create: TaskCreate) -> TaskRead:
    now = datetime.now(timezone.utc)
    new_task_id = uuid.uuid4()
    # Create a TaskRead instance from TaskCreate data
    task_data = task_create.model_dump()
    task = TaskRead(
        **task_data, # Unpack fields from TaskCreate
        task_id=new_task_id,
        status=TaskStatus.PENDING, # Default status
        created_at=now,
        updated_at=now
        # started_at and completed_at will be None by default as per model
    )
    db_tasks[new_task_id] = task
    return task

def update_task(task_id: uuid.UUID, task_update: TaskUpdate) -> Optional[TaskRead]:
    task = db_tasks.get(task_id)
    if task:
        update_data = task_update.model_dump(exclude_unset=True)
        
        # Handle status-specific timestamp updates
        if 'status' in update_data and task.status != update_data['status']:
            current_time_utc = datetime.now(timezone.utc)
            if update_data['status'] == TaskStatus.RUNNING and not task.started_at:
                task.started_at = current_time_utc
            elif update_data['status'] in [TaskStatus.COMPLETED, TaskStatus.FAILED] and not task.completed_at:
                task.completed_at = current_time_utc
                if not task.started_at: # If task was moved directly to completed/failed
                    task.started_at = current_time_utc
        
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now(timezone.utc)
        db_tasks[task_id] = task # Ensure the updated task is stored back
        return task
    return None

def delete_task(task_id: uuid.UUID) -> Optional[TaskRead]:
    return db_tasks.pop(task_id, None)
