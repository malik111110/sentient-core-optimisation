import pytest
import uuid
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.main import app
from src.api.models.core_models import AgentCreate, AgentRead, TaskCreate, TaskRead, TaskUpdate, TaskStatus
# NOTE: Priority enum is not defined in core_models.py, so it's excluded for now.
# If tests need it, it should be defined (e.g., in core_models.py or locally in tests)
from src.api.persistence import in_memory_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    if hasattr(in_memory_db, 'agents_db'):
        in_memory_db.agents_db.clear()
    if hasattr(in_memory_db, 'tasks_db'):
        in_memory_db.tasks_db.clear()

@pytest.fixture
def prerequisite_agent() -> AgentRead:
    agent_data = AgentCreate(
        name="TaskTestAgent",
        description="An agent specifically for testing task endpoints.",
        capabilities=["task_execution", "data_processing"]
    )
    response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    assert response.status_code == 201 # Ensure agent creation is successful
    created_agent_data = response.json()
    return AgentRead(**created_agent_data)

def test_create_task(prerequisite_agent: AgentRead):
    task_data = TaskCreate(
        name="Test Task - Sequential",
        description="A test task to be processed by an agent.",
        agent_id=prerequisite_agent.agent_id,
        input_data={"param1": "value1", "param2": 123},
        priority=1 # Using int directly as Priority enum is not in core_models
    )
    response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    
    assert response.status_code == 201
    created_task = response.json()
    
    assert created_task["name"] == task_data.name
    assert created_task["description"] == task_data.description
    assert created_task["agent_id"] == str(prerequisite_agent.agent_id)
    assert created_task["input_data"] == task_data.input_data
    assert created_task["status"] == TaskStatus.PENDING.value
    assert "task_id" in created_task
    assert "created_at" in created_task
    assert "updated_at" in created_task
    
    try:
        datetime.fromisoformat(created_task["created_at"])
        datetime.fromisoformat(created_task["updated_at"])
    except ValueError:
        pytest.fail("Timestamps are not in valid ISO format")

def test_create_task_without_agent():
    task_data = TaskCreate(
        name="Test Task - No Agent",
        description="A task created without an initial agent assignment.",
        input_data={"info": "pending agent assignment"},
        priority=2 # Using int directly as Priority enum is not in core_models
    )
    response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    
    assert response.status_code == 201
    created_task = response.json()
    
    assert created_task["name"] == task_data.name
    assert created_task["agent_id"] is None
    assert created_task["status"] == TaskStatus.PENDING.value
    assert "task_id" in created_task

def test_get_task(prerequisite_agent: AgentRead):
    # First, create a task to retrieve
    task_data = TaskCreate(
        name="Test Task - To Get",
        agent_id=prerequisite_agent.agent_id,
        input_data={"detail": "retrieval test"},
        priority=0 # Using int directly as Priority enum is not in core_models
    )
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    assert create_response.status_code == 201
    created_task_id = create_response.json()["task_id"]

    # Now, retrieve the task
    get_response = client.get(f"/api/v1/tasks/{created_task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()

    assert retrieved_task["task_id"] == created_task_id
    assert retrieved_task["name"] == task_data.name
    assert retrieved_task["agent_id"] == str(prerequisite_agent.agent_id)
    assert retrieved_task["status"] == TaskStatus.PENDING.value

def test_get_all_tasks(prerequisite_agent: AgentRead):
    # Create a couple of tasks
    task_data1 = TaskCreate(name="Task Alpha", agent_id=prerequisite_agent.agent_id, priority=1)
    client.post("/api/v1/tasks/", json=task_data1.model_dump(mode='json'))
    
    task_data2 = TaskCreate(name="Task Beta", priority=2) # No agent
    client.post("/api/v1/tasks/", json=task_data2.model_dump(mode='json'))

    # Retrieve all tasks
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks = response.json()

    assert len(tasks) >= 2
    
    task_names = [task["name"] for task in tasks]
    assert task_data1.name in task_names
    assert task_data2.name in task_names

def test_update_task(prerequisite_agent: AgentRead):
    # Create a task to update
    task_data = TaskCreate(
        name="Initial Task Name", 
        agent_id=prerequisite_agent.agent_id,
        priority=1
    )
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    assert create_response.status_code == 201
    created_task_id = create_response.json()["task_id"]

    # Update data
    update_data = TaskUpdate(
        name="Updated Task Name",
        description="This task has been updated.",
        status=TaskStatus.RUNNING,
        priority=3
    )
    
    update_response = client.put(f"/api/v1/tasks/{created_task_id}", json=update_data.model_dump(mode='json', exclude_unset=True))
    assert update_response.status_code == 200
    updated_task = update_response.json()

    assert updated_task["task_id"] == created_task_id
    assert updated_task["name"] == update_data.name
    assert updated_task["description"] == update_data.description
    assert updated_task["status"] == update_data.status.value
    assert updated_task["priority"] == update_data.priority
    assert "updated_at" in updated_task
    assert updated_task["updated_at"] != create_response.json()["updated_at"]

def test_delete_task(prerequisite_agent: AgentRead):
    # Create a task to delete
    task_data = TaskCreate(
        name="Task To Be Deleted", 
        agent_id=prerequisite_agent.agent_id,
        priority=0
    )
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    assert create_response.status_code == 201
    created_task_id = create_response.json()["task_id"]

    # Delete the task
    delete_response = client.delete(f"/api/v1/tasks/{created_task_id}")
    assert delete_response.status_code == 200 # Assuming 200 OK with deleted object returned
    
    if delete_response.status_code == 200:
        deleted_task_confirmation = delete_response.json()
        assert deleted_task_confirmation["task_id"] == created_task_id
        assert deleted_task_confirmation["name"] == task_data.name

    # Verify the task is actually deleted by trying to get it
    get_response = client.get(f"/api/v1/tasks/{created_task_id}")
    assert get_response.status_code == 404

# Other tests remain commented out for now.
