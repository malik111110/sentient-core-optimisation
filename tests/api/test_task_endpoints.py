import pytest
import uuid
from fastapi.testclient import TestClient
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from src.main import app
from src.api.models.core_models import AgentCreate, AgentRead, TaskCreate, TaskRead, TaskUpdate, TaskStatus, AgentStatus
# Priority enum is handled as int in tests if not defined in core_models

client = TestClient(app)

# No longer need clear_db_before_each_test as persistence is mocked

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
        status=AgentStatus.ACTIVE, # Or INACTIVE, as appropriate for tests
        config={},
        created_at=now,
        updated_at=now
    )

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_create_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_data = TaskCreate(
        name="Test Task - Sequential",
        description="A test task to be processed by an agent.",
        agent_id=prerequisite_agent.agent_id,
        input_data={"param1": "value1", "param2": 123},
        priority=1
    )

    mock_response = MagicMock()
    created_task_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    mock_response.data = [{
        "task_id": str(created_task_id),
        "name": task_data.name,
        "description": task_data.description,
        "agent_id": str(task_data.agent_id),
        "input_data": task_data.input_data,
        "output_data": None,
        "status": TaskStatus.PENDING.value,
        "priority": task_data.priority,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "started_at": None,
        "completed_at": None,
        "dependencies": []
    }]
    mock_supabase_client.table().insert().execute.return_value = mock_response

    response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    
    assert response.status_code == 201
    created_task_json = response.json()
    
    assert created_task_json["name"] == task_data.name
    assert created_task_json["description"] == task_data.description
    assert created_task_json["agent_id"] == str(prerequisite_agent.agent_id)
    assert created_task_json["input_data"] == task_data.input_data
    assert created_task_json["status"] == TaskStatus.PENDING.value
    assert "task_id" in created_task_json
    assert uuid.UUID(created_task_json["task_id"]) # Valid UUID
    assert datetime.fromisoformat(created_task_json["created_at"])
    assert datetime.fromisoformat(created_task_json["updated_at"])

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_create_task_without_agent(mock_supabase_client):
    task_data = TaskCreate(
        name="Test Task - No Agent",
        description="A task created without an initial agent assignment.",
        input_data={"info": "pending agent assignment"},
        priority=2
    )

    mock_response = MagicMock()
    created_task_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    mock_response.data = [{
        "task_id": str(created_task_id),
        "name": task_data.name,
        "description": task_data.description,
        "agent_id": None, # Explicitly None
        "input_data": task_data.input_data,
        "output_data": None,
        "status": TaskStatus.PENDING.value,
        "priority": task_data.priority,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "started_at": None,
        "completed_at": None,
        "dependencies": []
    }]
    mock_supabase_client.table().insert().execute.return_value = mock_response

    response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    
    assert response.status_code == 201
    created_task_json = response.json()
    
    assert created_task_json["name"] == task_data.name
    assert created_task_json["agent_id"] is None
    assert created_task_json["status"] == TaskStatus.PENDING.value
    assert "task_id" in created_task_json
    assert uuid.UUID(created_task_json["task_id"])

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
    mock_response = MagicMock()
    mock_response.data = expected_task_data # .single() returns a dict, not a list
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_response

    get_response = client.get(f"/api/v1/tasks/{task_id_str}")
    assert get_response.status_code == 200
    retrieved_task_json = get_response.json()

    assert retrieved_task_json["task_id"] == task_id_str
    assert retrieved_task_json["name"] == expected_task_data["name"]
    assert retrieved_task_json["agent_id"] == agent_id_str
    assert retrieved_task_json["status"] == TaskStatus.PENDING.value

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_all_tasks(mock_supabase_client, prerequisite_agent: AgentRead):
    now = datetime.now(timezone.utc)
    agent_id_str = str(prerequisite_agent.agent_id)
    
    tasks_db_data = [
        {
            "task_id": str(uuid.uuid4()), "name": "Task Alpha", "agent_id": agent_id_str, 
            "status": TaskStatus.PENDING.value, "priority": 1, "created_at": now.isoformat(), 
            "updated_at": now.isoformat(), "description": "", "input_data": {}, "output_data": None,
            "started_at": None, "completed_at": None, "dependencies": []
        },
        {
            "task_id": str(uuid.uuid4()), "name": "Task Beta", "agent_id": None, 
            "status": TaskStatus.COMPLETED.value, "priority": 2, "created_at": now.isoformat(), 
            "updated_at": now.isoformat(), "description": "", "input_data": {}, "output_data": {"result": "done"},
            "started_at": None, "completed_at": None, "dependencies": []
        }
    ]
    mock_response = MagicMock()
    mock_response.data = tasks_db_data
    mock_supabase_client.table().select().range().execute.return_value = mock_response

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks_list_json = response.json()

    assert len(tasks_list_json) == 2
    task_names = [task["name"] for task in tasks_list_json]
    assert "Task Alpha" in task_names
    assert "Task Beta" in task_names
    assert tasks_list_json[0]["agent_id"] == agent_id_str
    assert tasks_list_json[1]["agent_id"] is None

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_update_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_id_str = str(uuid.uuid4())
    agent_id_str = str(prerequisite_agent.agent_id)
    original_created_at_dt = datetime.now(timezone.utc) - timedelta(days=1)
    original_updated_at_dt = original_created_at_dt + timedelta(hours=1)

    update_data_payload = TaskUpdate(
        name="Updated Task Name",
        description="This task has been updated.",
        status=TaskStatus.RUNNING,
        priority=3
    )
    
    updated_task_from_db = {
        "task_id": task_id_str,
        "name": update_data_payload.name,
        "description": update_data_payload.description,
        "agent_id": agent_id_str, 
        "input_data": {"original": "data"}, 
        "output_data": None,
        "status": update_data_payload.status.value,
        "priority": update_data_payload.priority,
        "created_at": original_created_at_dt.isoformat(), 
        "updated_at": datetime.now(timezone.utc).isoformat(), 
        "started_at": None, 
        "completed_at": None,
        "dependencies": []
    }
    if update_data_payload.status == TaskStatus.RUNNING:
        updated_task_from_db["started_at"] = datetime.now(timezone.utc).isoformat()

    mock_update_response = MagicMock()
    mock_update_response.data = updated_task_from_db 
    mock_supabase_client.table().update().eq().select().single().execute.return_value = mock_update_response
    
    update_response = client.put(f"/api/v1/tasks/{task_id_str}", json=update_data_payload.model_dump(mode='json', exclude_unset=True))
    assert update_response.status_code == 200
    updated_task_json = update_response.json()

    assert updated_task_json["task_id"] == task_id_str
    assert updated_task_json["name"] == update_data_payload.name
    assert updated_task_json["description"] == update_data_payload.description
    assert updated_task_json["status"] == update_data_payload.status.value
    assert updated_task_json["priority"] == update_data_payload.priority
    assert datetime.fromisoformat(updated_task_json["updated_at"]) > original_updated_at_dt

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_delete_task(mock_supabase_client, prerequisite_agent: AgentRead):
    task_id_str = str(uuid.uuid4())
    agent_id_str = str(prerequisite_agent.agent_id)
    now = datetime.now(timezone.utc)

    task_to_delete_data = {
        "task_id": task_id_str,
        "name": "Task To Be Deleted",
        "description": "Original description",
        "agent_id": agent_id_str,
        "input_data": {}, "output_data": None,
        "status": TaskStatus.PENDING.value, "priority": 0,
        "created_at": now.isoformat(), "updated_at": now.isoformat(),
        "started_at": None, "completed_at": None, "dependencies": []
    }

    mock_get_response = MagicMock()
    mock_get_response.data = task_to_delete_data 
    
    mock_delete_op_response = MagicMock()
    mock_delete_op_response.data = [task_to_delete_data] 
    
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response
    mock_supabase_client.table().delete().eq().execute.return_value = mock_delete_op_response
    
    delete_response = client.delete(f"/api/v1/tasks/{task_id_str}")
    assert delete_response.status_code == 200
    
    deleted_task_confirmation_json = delete_response.json()
    assert deleted_task_confirmation_json["task_id"] == task_id_str
    assert deleted_task_confirmation_json["name"] == task_to_delete_data["name"]

    mock_get_after_delete_response = MagicMock()
    mock_get_after_delete_response.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_after_delete_response
    
    get_response_after_delete = client.get(f"/api/v1/tasks/{task_id_str}")
    assert get_response_after_delete.status_code == 404

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_nonexistent_task(mock_supabase_client):
    non_existent_task_id = str(uuid.uuid4())
    mock_response = MagicMock()
    mock_response.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_response

    response = client.get(f"/api/v1/tasks/{non_existent_task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_update_nonexistent_task(mock_supabase_client):
    non_existent_task_id = str(uuid.uuid4())
    update_payload = TaskUpdate(name="Doesn't Matter")
    
    mock_update_response = MagicMock()
    mock_update_response.data = None
    mock_supabase_client.table().update().eq().select().single().execute.return_value = mock_update_response

    response = client.put(f"/api/v1/tasks/{non_existent_task_id}", json=update_payload.model_dump(mode='json', exclude_unset=True))
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_delete_nonexistent_task(mock_supabase_client):
    non_existent_task_id = str(uuid.uuid4())
    
    mock_get_response = MagicMock()
    mock_get_response.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response

    response = client.delete(f"/api/v1/tasks/{non_existent_task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
