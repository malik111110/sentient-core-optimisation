import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from src.main import app
from src.api.models.core_models import AgentRead, AgentStatus, TaskCreate, TaskRead, TaskStatus

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
    
    assert created_task_json["task_id"] == str(created_task_id)
    assert created_task_json["name"] == task_create_payload.name
    assert created_task_json["agent_id"] is None
    assert created_task_json["status"] == TaskStatus.PENDING.value
    assert created_task_json["priority"] == task_create_payload.priority
