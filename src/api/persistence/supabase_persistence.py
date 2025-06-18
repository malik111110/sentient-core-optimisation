from typing import Dict, List, Optional, Union
import uuid
from datetime import datetime, timezone

from ..models.core_models import AgentRead, AgentCreate, AgentUpdate, TaskRead, TaskCreate, TaskUpdate, AgentStatus, TaskStatus
from src.clients.supabase_client import supabase_client # Import Supabase client

# In-memory data store for tasks (will be refactored later)
db_tasks: Dict[uuid.UUID, TaskRead] = {}

# --- Agent Persistence Functions (Supabase) ---
def get_agent(agent_id: uuid.UUID) -> Optional[AgentRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in get_agent")
        return None
    try:
        response = supabase_client.table('agents').select("*").eq('agent_id', str(agent_id)).single().execute()
        if response.data:
            return AgentRead(**response.data)
    except Exception as e:
        print(f"Error fetching agent {agent_id} from Supabase: {e}")
    return None

def get_agents(skip: int = 0, limit: int = 100) -> List[AgentRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in get_agents")
        return []
    try:
        response = supabase_client.table('agents').select("*").range(skip, skip + limit - 1).execute()
        if response.data:
            return [AgentRead(**item) for item in response.data]
    except Exception as e:
        print(f"Error fetching agents from Supabase: {e}")
    return []

def create_agent(agent_create: AgentCreate) -> Optional[AgentRead]: # Changed return to Optional for consistency
    if not supabase_client:
        print("ERROR: Supabase client not initialized in create_agent")
        return None
    now = datetime.now(timezone.utc)
    new_agent_id = uuid.uuid4()
    agent_data_dict = agent_create.model_dump()
    agent_data_dict['agent_id'] = str(new_agent_id) # Ensure UUID is string for Supabase
    agent_data_dict['status'] = AgentStatus.INACTIVE.value # Default status
    agent_data_dict['created_at'] = now.isoformat()
    agent_data_dict['updated_at'] = now.isoformat()

    try:
        response = supabase_client.table('agents').insert(agent_data_dict).execute()
        if response.data:
            # Supabase returns a list with one item on successful insert
            return AgentRead(**response.data[0])
    except Exception as e:
        print(f"Error creating agent in Supabase: {e}")
    return None

def update_agent(agent_id: uuid.UUID, agent_update: AgentUpdate) -> Optional[AgentRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in update_agent")
        return None
    update_data_dict = agent_update.model_dump(exclude_unset=True)
    update_data_dict['updated_at'] = datetime.now(timezone.utc).isoformat()

    # Convert enums to their values if present
    if 'status' in update_data_dict and isinstance(update_data_dict['status'], AgentStatus):
        update_data_dict['status'] = update_data_dict['status'].value

    try:
        response = supabase_client.table('agents').update(update_data_dict).eq('agent_id', str(agent_id)).select().single().execute()
        if response.data:
            return AgentRead(**response.data)
    except Exception as e:
        print(f"Error updating agent {agent_id} in Supabase: {e}")
    return None

def delete_agent(agent_id: uuid.UUID) -> Optional[AgentRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in delete_agent")
        return None
    # First, fetch the agent to return its data, as per original in-memory logic
    agent_to_delete = get_agent(agent_id)
    if not agent_to_delete:
        return None # Agent not found

    try:
        response = supabase_client.table('agents').delete().eq('agent_id', str(agent_id)).execute()
        # Successful delete in Supabase might not return the deleted data in response.data directly in all client versions/scenarios.
        # We rely on agent_to_delete fetched prior to deletion for the return value.
        if response.data or (hasattr(response, 'status_code') and 200 <= response.status_code < 300): # Check for successful HTTP status too
             return agent_to_delete
    except Exception as e:
        print(f"Error deleting agent {agent_id} from Supabase: {e}")
    return None

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
