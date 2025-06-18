from typing import Dict, List, Optional, Union
import uuid
from datetime import datetime, timezone

from ..models.core_models import AgentRead, AgentCreate, AgentUpdate, TaskRead, TaskCreate, TaskUpdate, AgentStatus, TaskStatus
from src.clients.supabase_client import supabase_client # Import Supabase client

# All persistence is now handled by Supabase.

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

# --- Task Persistence Functions (Supabase) ---
def get_task(task_id: uuid.UUID) -> Optional[TaskRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in get_task")
        return None
    try:
        response = supabase_client.table('tasks').select("*").eq('task_id', str(task_id)).single().execute()
        if response.data:
            return TaskRead(**response.data)
    except Exception as e:
        print(f"Error fetching task {task_id} from Supabase: {e}")
    return None

def get_tasks(agent_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 100) -> List[TaskRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in get_tasks")
        return []
    try:
        query = supabase_client.table('tasks').select("*")
        if agent_id:
            query = query.eq('agent_id', str(agent_id))
        response = query.range(skip, skip + limit - 1).execute()
        if response.data:
            return [TaskRead(**item) for item in response.data]
    except Exception as e:
        print(f"Error fetching tasks from Supabase: {e}")
    return []

def create_task(task_create: TaskCreate) -> Optional[TaskRead]: # Changed return to Optional
    if not supabase_client:
        print("ERROR: Supabase client not initialized in create_task")
        return None
    now = datetime.now(timezone.utc)
    new_task_id = uuid.uuid4()
    task_data_dict = task_create.model_dump()
    task_data_dict['task_id'] = str(new_task_id)
    task_data_dict['status'] = TaskStatus.PENDING.value # Default status
    task_data_dict['created_at'] = now.isoformat()
    task_data_dict['updated_at'] = now.isoformat()
    if task_data_dict.get('agent_id') is not None:
        task_data_dict['agent_id'] = str(task_data_dict['agent_id'])
    # Ensure started_at and completed_at are not sent if None, or handle as per DB schema
    task_data_dict.pop('started_at', None) # Remove if None, Supabase handles default/NULL
    task_data_dict.pop('completed_at', None) # Remove if None, Supabase handles default/NULL

    try:
        response = supabase_client.table('tasks').insert(task_data_dict).execute()
        if response.data:
            return TaskRead(**response.data[0])
    except Exception as e:
        print(f"Error creating task in Supabase: {e}")
    return None

def update_task(task_id: uuid.UUID, task_update: TaskUpdate) -> Optional[TaskRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in update_task")
        return None
    update_data_dict = task_update.model_dump(exclude_unset=True)
    current_time_utc_iso = datetime.now(timezone.utc).isoformat()
    update_data_dict['updated_at'] = current_time_utc_iso

    # Handle status-specific timestamp updates
    if 'status' in update_data_dict:
        # Fetch current task to check its current timestamps if needed, or rely on DB triggers if possible
        # For simplicity here, we'll set them if the status implies they should be set.
        if update_data_dict['status'] == TaskStatus.RUNNING.value and not task_update.started_at:
             # Check if started_at is already set in the db by fetching the task first if strict logic is needed
            update_data_dict['started_at'] = current_time_utc_iso
        elif update_data_dict['status'] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value] and not task_update.completed_at:
            update_data_dict['completed_at'] = current_time_utc_iso
            if not task_update.started_at: # If task was moved directly to completed/failed & started_at not in payload
                # Potentially fetch task to see if started_at was already set
                update_data_dict.setdefault('started_at', current_time_utc_iso)
        # Convert enums to their values
        if isinstance(update_data_dict['status'], TaskStatus):
             update_data_dict['status'] = update_data_dict['status'].value

    if update_data_dict.get('agent_id') is not None:
        update_data_dict['agent_id'] = str(update_data_dict['agent_id'])

    try:
        response = supabase_client.table('tasks').update(update_data_dict).eq('task_id', str(task_id)).select().single().execute()
        if response.data:
            return TaskRead(**response.data)
    except Exception as e:
        print(f"Error updating task {task_id} in Supabase: {e}")
    return None

def delete_task(task_id: uuid.UUID) -> Optional[TaskRead]:
    if not supabase_client:
        print("ERROR: Supabase client not initialized in delete_task")
        return None
    task_to_delete = get_task(task_id)
    if not task_to_delete:
        return None

    try:
        response = supabase_client.table('tasks').delete().eq('task_id', str(task_id)).execute()
        if response.data or (hasattr(response, 'status_code') and 200 <= response.status_code < 300):
            return task_to_delete
    except Exception as e:
        print(f"Error deleting task {task_id} from Supabase: {e}")
    return None
