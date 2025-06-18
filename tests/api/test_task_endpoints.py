import pytest
import uuid
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.main import app # app instance from src/main.py
from src.api.models.core_models import AgentCreate, AgentRead, TaskCreate, TaskRead, TaskUpdate, TaskStatus, Priority
from src.api.persistence import in_memory_db # To clear db for test isolation

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    """Fixture to clear in-memory database before each test."""
    in_memory_db.db_agents.clear()
    in_memory_db.db_tasks.clear()
    yield

@pytest.fixture
def prerequisite_agent() -> AgentRead:
    """Fixture to create a prerequisite agent for task tests."""
    agent_data = AgentCreate(name="Task Handler Agent", description="Agent for task tests")
    response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    assert response.status_code == 201
    return AgentRead(**response.json())

def test_create_task(prerequisite_agent: AgentRead):
    task_data = TaskCreate(
        agent_id=prerequisite_agent.agent_id,
        name="Test Task Alpha",
        description="A task for creation testing.",
        input_data={"key": "value"},
        priority=Priority.MEDIUM,
        dependencies=[uuid.uuid4()] # Example dependency
    )
    response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json')) # mode='json' for UUIDs
    assert response.status_code == 201
    created_task = TaskRead(**response.json())

    assert created_task.name == task_data.name
    assert created_task.agent_id == prerequisite_agent.agent_id
    assert created_task.description == task_data.description
    assert created_task.input_data == task_data.input_data
    assert created_task.priority == task_data.priority
    # Compare dependencies as strings because UUIDs might be stringified in JSON
    assert [str(dep) for dep in created_task.dependencies] == [str(dep) for dep in task_data.dependencies]
    assert created_task.task_id is not None
    assert created_task.status == TaskStatus.PENDING
    assert created_task.created_at is not None
    assert created_task.updated_at is not None
    assert created_task.started_at is None
    assert created_task.completed_at is None
    assert created_task.created_at == created_task.updated_at

def test_get_specific_task(prerequisite_agent: AgentRead):
    task_data = TaskCreate(agent_id=prerequisite_agent.agent_id, name="Test Task Beta")
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    task_id = create_response.json()["task_id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = TaskRead(**response.json())
    assert retrieved_task.task_id == task_id
    assert retrieved_task.name == task_data.name

def test_get_nonexistent_task():
    non_existent_uuid = uuid.uuid4()
    response = client.get(f"/api/v1/tasks/{non_existent_uuid}")
    assert response.status_code == 404

def test_list_tasks(prerequisite_agent: AgentRead):
    # Create a couple of tasks
    task_data1 = TaskCreate(agent_id=prerequisite_agent.agent_id, name="Task Gamma 1")
    client.post("/api/v1/tasks/", json=task_data1.model_dump(mode='json'))
    task_data2 = TaskCreate(agent_id=prerequisite_agent.agent_id, name="Task Gamma 2", priority=Priority.HIGH)
    client.post("/api/v1/tasks/", json=task_data2.model_dump(mode='json'))

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks = [TaskRead(**item) for item in response.json()]
    assert len(tasks) >= 2 # Check for at least 2, could be more if other tests ran without full clear
    
    # Basic check for presence of created tasks by name
    task_names = [t.name for t in tasks]
    assert task_data1.name in task_names
    assert task_data2.name in task_names

def test_list_tasks_with_filters(prerequisite_agent: AgentRead):
    agent_id_filter = prerequisite_agent.agent_id
    other_agent_id = uuid.uuid4() # A different agent_id for filtering

    # Create tasks for the main agent
    client.post("/api/v1/tasks/", json=TaskCreate(agent_id=agent_id_filter, name="Filter Task A", status=TaskStatus.PENDING).model_dump(mode='json'))
    client.post("/api/v1/tasks/", json=TaskCreate(agent_id=agent_id_filter, name="Filter Task B", status=TaskStatus.RUNNING).model_dump(mode='json'))
    # Create a task for another agent (should be filtered out)
    client.post("/api/v1/tasks/", json=TaskCreate(agent_id=other_agent_id, name="Other Agent Task").model_dump(mode='json'))

    # Filter by agent_id
    response_agent_filter = client.get(f"/api/v1/tasks/?agent_id={agent_id_filter}")
    assert response_agent_filter.status_code == 200
    tasks_agent_filter = [TaskRead(**item) for item in response_agent_filter.json()]
    assert len(tasks_agent_filter) == 2
    for task in tasks_agent_filter:
        assert task.agent_id == agent_id_filter

    # Filter by status
    response_status_filter = client.get(f"/api/v1/tasks/?status={TaskStatus.RUNNING.value}") # Use .value for enum
    assert response_status_filter.status_code == 200
    tasks_status_filter = [TaskRead(**item) for item in response_status_filter.json()]
    assert len(tasks_status_filter) >= 1 # At least one running task
    for task in tasks_status_filter:
        assert task.status == TaskStatus.RUNNING
        if task.name == "Filter Task B": # Check our specific running task
             assert task.agent_id == agent_id_filter


def test_update_task_status_and_data(prerequisite_agent: AgentRead):
    task_data = TaskCreate(agent_id=prerequisite_agent.agent_id, name="Task Epsilon - To Update")
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    task_id = create_response.json()["task_id"]
    original_created_at_str = create_response.json()["created_at"]
    original_created_at = datetime.fromisoformat(original_created_at_str)


    # Update to RUNNING
    update_payload_running = TaskUpdate(status=TaskStatus.RUNNING)
    response_running = client.put(f"/api/v1/tasks/{task_id}", json=update_payload_running.model_dump(exclude_unset=True))
    assert response_running.status_code == 200
    running_task = TaskRead(**response_running.json())
    assert running_task.status == TaskStatus.RUNNING
    assert running_task.started_at is not None
    assert running_task.completed_at is None
    assert datetime.fromisoformat(running_task.updated_at) > original_created_at
    first_started_at_str = running_task.started_at # Store for next check

    # Update to COMPLETED
    update_payload_completed = TaskUpdate(status=TaskStatus.COMPLETED, output_data={"result": "success"})
    response_completed = client.put(f"/api/v1/tasks/{task_id}", json=update_payload_completed.model_dump(exclude_unset=True))
    assert response_completed.status_code == 200
    completed_task = TaskRead(**response_completed.json())
    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.output_data == {"result": "success"}
    assert completed_task.started_at == first_started_at_str # Should not change if already set
    assert completed_task.completed_at is not None
    assert datetime.fromisoformat(completed_task.updated_at) > datetime.fromisoformat(running_task.updated_at)

def test_update_nonexistent_task():
    non_existent_uuid = uuid.uuid4()
    update_payload = TaskUpdate(name="Doesn't Matter")
    response = client.put(f"/api/v1/tasks/{non_existent_uuid}", json=update_payload.model_dump(exclude_unset=True))
    assert response.status_code == 404

def test_delete_task(prerequisite_agent: AgentRead):
    task_data = TaskCreate(agent_id=prerequisite_agent.agent_id, name="Task Delta - To Delete")
    create_response = client.post("/api/v1/tasks/", json=task_data.model_dump(mode='json'))
    task_id = create_response.json()["task_id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task():
    non_existent_uuid = uuid.uuid4()
    response = client.delete(f"/api/v1/tasks/{non_existent_uuid}")
    assert response.status_code == 404
