import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.models.core_models import Agent, Task, TaskStatus

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Welcome to the Sentient Core API!"}

def test_create_and_get_agent():
    # Create a new agent
    agent_data = {"name": "Test Agent", "description": "An agent for testing purposes."}
    response = client.post("/v1/agents/", json=agent_data)
    assert response.status_code == 201
    created_agent = response.json()
    assert created_agent["name"] == agent_data["name"]
    agent_id = created_agent["id"]

    # Get the agent back
    response = client.get(f"/v1/agents/{agent_id}")
    assert response.status_code == 200
    retrieved_agent = response.json()
    assert retrieved_agent["id"] == agent_id
    assert retrieved_agent["name"] == agent_data["name"]

def test_get_nonexistent_agent():
    response = client.get("/v1/agents/nonexistent-id")
    assert response.status_code == 404

def test_list_agents():
    # Clear previous state if necessary or ensure test isolation
    # For this simple in-memory db, we rely on test execution order or could reset db
    response = client.get("/v1/agents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_task():
    # First, create an agent to assign the task to
    agent_data = {"name": "Task Agent", "description": "An agent for running tasks."}
    agent_response = client.post("/v1/agents/", json=agent_data)
    agent_id = agent_response.json()["id"]

    # Now, create a task for that agent
    task_input = {"prompt": "Summarize this text...", "text": "A long text..."}
    task_response = client.post(f"/v1/agents/{agent_id}/tasks", json=task_input)
    assert task_response.status_code == 202
    created_task = task_response.json()
    assert created_task["agent_id"] == agent_id
    assert created_task["input_data"] == task_input
    assert created_task["status"] == TaskStatus.RUNNING
    task_id = created_task["id"]

    # Get the task status back
    status_response = client.get(f"/v1/tasks/{task_id}")
    assert status_response.status_code == 200
    retrieved_task = status_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["status"] == TaskStatus.RUNNING

def test_get_nonexistent_task():
    response = client.get("/v1/tasks/nonexistent-id")
    assert response.status_code == 404
