import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta

from src.main import app
from src.api.models.core_models import AgentRead, AgentStatus, TaskCreate, TaskRead, TaskStatus, TaskUpdate

client = TestClient(app)

@pytest.fixture
def prerequisite_agent() -> AgentRead:
    """Provides a mock AgentRead object for task tests."""
    agent_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    return AgentRead(
        agent_id=agent_id,
        name="MockTaskTestAgent",
        description="A mock agent for testing task endpoints.",
        capabilities=["task_execution"],
        status=AgentStatus.ACTIVE,
        config={},
        created_at=now,
        updated_at=now
    )

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_nonexistent_task(mock_supabase_client):
    non_existent_task_id = str(uuid.uuid4())
    mock_response = MagicMock()
    mock_response.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_response

    response = client.get(f"/api/v1/tasks/{non_existent_task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
# 
# 
@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_create_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_create_payload = TaskCreate(
        name="Test Task - Create",
        description="A test task to be created.",
        agent_id=prerequisite_agent.agent_id,
        input_data={"key": "value"},
        priority=1
    )

    mock_insert_response = MagicMock()
    created_task_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    
    # Simulate the data structure returned by Supabase after insert
    mock_insert_response.data = [{
        "task_id": str(created_task_id),
        "name": task_create_payload.name,
        "description": task_create_payload.description,
        "agent_id": str(task_create_payload.agent_id),
        "input_data": task_create_payload.input_data,
        "output_data": None, # Default for new task
        "status": TaskStatus.PENDING.value, # Default for new task
        "priority": task_create_payload.priority,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "started_at": None,
        "completed_at": None,
        "dependencies": [] # Assuming empty for new task
    }]
    mock_supabase_client.table().insert().execute.return_value = mock_insert_response

    response = client.post("/api/v1/tasks/", json=task_create_payload.model_dump(mode='json'))
    
    assert response.status_code == 201, response.text
    created_task_json = response.json()
    
    assert created_task_json["task_id"] == str(created_task_id)
    assert created_task_json["name"] == task_create_payload.name
    assert created_task_json["description"] == task_create_payload.description
    assert created_task_json["agent_id"] == str(prerequisite_agent.agent_id)
    assert created_task_json["input_data"] == task_create_payload.input_data
    assert created_task_json["status"] == TaskStatus.PENDING.value
    assert created_task_json["priority"] == task_create_payload.priority
    assert datetime.fromisoformat(created_task_json["created_at"]) # Check if valid isoformat
    assert datetime.fromisoformat(created_task_json["updated_at"])
    assert created_task_json["output_data"] is None
    assert created_task_json["started_at"] is None
    assert created_task_json["completed_at"] is None
    assert created_task_json["dependencies"] == []
# 
# 
@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_create_task_without_agent(mock_supabase_client):
    task_create_payload = TaskCreate(
        name="Test Task - No Agent",
        description="A task created without an initial agent assignment.",
        agent_id=None, # Explicitly None
        input_data={"info": "pending agent assignment"},
        priority=2
    )

    mock_insert_response = MagicMock()
    created_task_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    mock_insert_response.data = [{
        "task_id": str(created_task_id),
        "name": task_create_payload.name,
        "description": task_create_payload.description,
        "agent_id": None, # Supabase returns None for null UUIDs
        "input_data": task_create_payload.input_data,
        "output_data": None,
        "status": TaskStatus.PENDING.value,
        "priority": task_create_payload.priority,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "started_at": None,
        "completed_at": None,
        "dependencies": []
    }]
    mock_supabase_client.table().insert().execute.return_value = mock_insert_response

    response = client.post("/api/v1/tasks/", json=task_create_payload.model_dump(mode='json'))

    assert response.status_code == 201, response.text
    created_task_json = response.json()
    assert created_task_json["agent_id"] is None
    assert created_task_json["name"] == task_create_payload.name
# 
# 
@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_id_str = str(uuid.uuid4())
    agent_id_str = str(prerequisite_agent.agent_id)
    now = datetime.now(timezone.utc)

    expected_task_data = {
        "task_id": task_id_str,
        "name": "Test Task - To Get",
        "description": "A task to retrieve",
        "agent_id": agent_id_str,
        "input_data": {"detail": "retrieval test"},
        "output_data": None,
        "status": TaskStatus.PENDING.value,
        "priority": 0,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "started_at": None,
        "completed_at": None,
        "dependencies": []
    }
    mock_get_response = MagicMock()
    # .single() in Supabase client returns a dict directly, not a list of one dict
    mock_get_response.data = expected_task_data 
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response

    get_response = client.get(f"/api/v1/tasks/{task_id_str}")
    assert get_response.status_code == 200, get_response.text
    retrieved_task_json = get_response.json()

    assert retrieved_task_json["task_id"] == task_id_str
    assert retrieved_task_json["name"] == expected_task_data["name"]
    assert retrieved_task_json["agent_id"] == agent_id_str
    assert retrieved_task_json["status"] == TaskStatus.PENDING.value # Ensure enum value is checked
    assert retrieved_task_json["priority"] == expected_task_data["priority"]
#     assert datetime.fromisoformat(retrieved_task_json["created_at"])
#     assert datetime.fromisoformat(retrieved_task_json["updated_at"])
# 
# 
@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_all_tasks(mock_supabase_client, prerequisite_agent: AgentRead):
    now = datetime.now(timezone.utc)
    agent_id_str = str(prerequisite_agent.agent_id)
    
    tasks_db_data = [
        {
            "task_id": str(uuid.uuid4()), "name": "Task Alpha", "agent_id": agent_id_str, 
            "status": TaskStatus.PENDING.value, "priority": 1, "created_at": now.isoformat(), 
            "updated_at": now.isoformat(), "description": "First task", "input_data": {}, "output_data": None,
            "started_at": None, "completed_at": None, "dependencies": []
        },
        {
            "task_id": str(uuid.uuid4()), "name": "Task Beta", "agent_id": None, 
            "status": TaskStatus.COMPLETED.value, "priority": 2, "created_at": now.isoformat(), 
            "updated_at": now.isoformat(), "description": "Second task", "input_data": {}, "output_data": {"result": "done"},
            "started_at": now.isoformat(), "completed_at": now.isoformat(), "dependencies": []
        }
    ]
    mock_get_all_response = MagicMock()
    mock_get_all_response.data = tasks_db_data
    # Assuming the actual call in supabase_persistence uses range() for pagination, even if not explicitly tested here.
    # If it's just .select().execute() for all, adjust mock accordingly.
    mock_supabase_client.table().select().range().execute.return_value = mock_get_all_response 

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200, response.text
    tasks_list_json = response.json()

    assert len(tasks_list_json) == 2
    task_names = [task["name"] for task in tasks_list_json]
    assert "Task Alpha" in task_names
    assert "Task Beta" in task_names
# 
#     # Verify details of the first task (Task Alpha)
#     assert tasks_list_json[0]["agent_id"] == agent_id_str
#     assert tasks_list_json[0]["name"] == "Task Alpha"
#     assert tasks_list_json[0]["status"] == TaskStatus.PENDING.value
# 
#     # Verify details of the second task (Task Beta)
#     assert tasks_list_json[1]["agent_id"] is None
#     assert tasks_list_json[1]["name"] == "Task Beta"
#     assert tasks_list_json[1]["status"] == TaskStatus.COMPLETED.value
#     assert tasks_list_json[1]["output_data"] == {"result": "done"}
# 
# 
@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_update_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_id_str = str(uuid.uuid4())
    agent_id_str = str(prerequisite_agent.agent_id)
    original_created_at_dt = datetime.now(timezone.utc) - timedelta(days=1)
    # original_updated_at_dt = original_created_at_dt + timedelta(hours=1) # Not strictly needed for mock setup

    update_data_payload = TaskUpdate(
        name="Updated Task Name",
        description="This task has been updated.",
        status=TaskStatus.RUNNING,
        priority=3
    )
    
    current_time_dt = datetime.now(timezone.utc)
    current_time_iso = current_time_dt.isoformat()
    updated_task_from_db = {
        "task_id": task_id_str,
        "name": update_data_payload.name,
        "description": update_data_payload.description,
        "agent_id": agent_id_str, 
        "input_data": {"original": "data"}, # Assuming input_data is not changed by this update
        "output_data": None, # Assuming output_data is not changed by this update
        "status": update_data_payload.status.value,
        "priority": update_data_payload.priority,
        "created_at": original_created_at_dt.isoformat(), 
        "updated_at": current_time_iso, 
        "started_at": None, 
        "completed_at": None,
        "dependencies": []
    }
    if update_data_payload.status == TaskStatus.RUNNING:
        updated_task_from_db["started_at"] = current_time_iso

    mock_update_response = MagicMock()
    mock_update_response.data = updated_task_from_db 
    mock_supabase_client.table().update().eq().select().single().execute.return_value = mock_update_response
    
    update_response = client.put(f"/api/v1/tasks/{task_id_str}", json=update_data_payload.model_dump(mode='json', exclude_unset=True))
    assert update_response.status_code == 200, update_response.text
    updated_task_json = update_response.json()

    assert updated_task_json["task_id"] == task_id_str
    assert updated_task_json["name"] == update_data_payload.name
    assert updated_task_json["description"] == update_data_payload.description
    assert updated_task_json["status"] == update_data_payload.status.value
    assert updated_task_json["priority"] == update_data_payload.priority
    # Compare datetime objects for robustness against string format differences (Z vs +00:00)
    assert datetime.fromisoformat(updated_task_json["updated_at"]) == current_time_dt
    if update_data_payload.status == TaskStatus.RUNNING:
        assert datetime.fromisoformat(updated_task_json["started_at"]) == current_time_dt
    else:
        assert updated_task_json["started_at"] is None # Or check original value if not None
# 
# 
# @patch('src.api.persistence.supabase_persistence.supabase_client')
# def test_delete_task(mock_supabase_client, prerequisite_agent: AgentRead):
#     task_id_str = str(uuid.uuid4())
#     agent_id_str = str(prerequisite_agent.agent_id)
#     now = datetime.now(timezone.utc)
# 
#     task_to_delete_data = {
#         "task_id": task_id_str,
#         "name": "Task To Be Deleted",
#         "description": "Original description",
#         "agent_id": agent_id_str,
#         "input_data": {},
#         "output_data": None,
#         "status": TaskStatus.PENDING.value,
#         "priority": 0,
#         "created_at": now.isoformat(),
#         "updated_at": now.isoformat(),
#         "started_at": None,
#         "completed_at": None,
#         "dependencies": []
#     }
# 
#     # Mock for the get_task call within delete_task persistence function
#     mock_get_response_before_delete = MagicMock()
#     mock_get_response_before_delete.data = task_to_delete_data 
#     
#     # Mock for the delete operation itself
#     mock_delete_op_response = MagicMock()
#     mock_delete_op_response.data = [task_to_delete_data] # Supabase delete often returns list of deleted items
#     
#     # Mock for the get_task call after delete (to confirm it's gone)
#     mock_get_response_after_delete = MagicMock()
#     mock_get_response_after_delete.data = None
# 
#     # Configure the side_effect for multiple calls to execute()
#     # 1st call: get_task before delete (in persistence.delete_task)
#     # 2nd call: delete operation (in persistence.delete_task)
#     # 3rd call: get_task after delete (in this test)
#     mock_supabase_client.table().select().eq().single().execute.side_effect = [
#         mock_get_response_before_delete,
#         mock_get_response_after_delete
#     ]
#     mock_supabase_client.table().delete().eq().execute.return_value = mock_delete_op_response
#     
#     # Perform the delete operation
#     delete_response = client.delete(f"/api/v1/tasks/{task_id_str}")
#     assert delete_response.status_code == 200, delete_response.text
#     
#     deleted_task_confirmation_json = delete_response.json()
#     assert deleted_task_confirmation_json["task_id"] == task_id_str
#     assert deleted_task_confirmation_json["name"] == task_to_delete_data["name"]
# 
#     # Attempt to get the task after deletion
#     get_response_after_actual_delete = client.get(f"/api/v1/tasks/{task_id_str}")
#     assert get_response_after_actual_delete.status_code == 404, get_response_after_actual_delete.text
