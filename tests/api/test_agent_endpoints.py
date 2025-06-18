import pytest
import uuid
from fastapi.testclient import TestClient
from src.main import app # app instance from src/main.py
from src.api.models.core_models import AgentCreate, AgentRead, AgentUpdate, AgentStatus
from src.api.persistence import in_memory_db # To clear db for test isolation

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    """Fixture to clear in-memory database before each test."""
    in_memory_db.db_agents.clear()
    in_memory_db.db_tasks.clear() # Though not directly used here, good practice
    yield # This is where the test runs

def test_read_api_v1_root():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Sentient Core API v1"}

def test_create_agent():
    agent_data = AgentCreate(
        name="Test Agent Alpha",
        description="An agent for testing creation.",
        capabilities=["test", "create"],
        config={"param1": "value1"}
    )
    response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    assert response.status_code == 201
    created_agent = AgentRead(**response.json())
    assert created_agent.name == agent_data.name
    assert created_agent.description == agent_data.description
    assert created_agent.capabilities == agent_data.capabilities
    assert created_agent.config == agent_data.config
    assert created_agent.agent_id is not None
    assert created_agent.status == AgentStatus.INACTIVE
    assert created_agent.created_at is not None
    assert created_agent.updated_at is not None
    assert created_agent.created_at == created_agent.updated_at # Initially

def test_get_specific_agent():
    # First, create an agent
    agent_data = AgentCreate(name="Test Agent Beta", description="For get test")
    create_response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    assert create_response.status_code == 201
    agent_id = create_response.json()["agent_id"]

    # Get the agent back
    response = client.get(f"/api/v1/agents/{agent_id}")
    assert response.status_code == 200
    retrieved_agent = AgentRead(**response.json())
    assert retrieved_agent.agent_id == uuid.UUID(agent_id) # Ensure UUID conversion
    assert retrieved_agent.name == agent_data.name

def test_get_nonexistent_agent():
    non_existent_uuid = uuid.uuid4()
    response = client.get(f"/api/v1/agents/{non_existent_uuid}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found"

def test_list_agents():
    # Create a couple of agents
    client.post("/api/v1/agents/", json=AgentCreate(name="Agent One").model_dump())
    client.post("/api/v1/agents/", json=AgentCreate(name="Agent Two").model_dump())

    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    agents_list = response.json()
    assert isinstance(agents_list, list)
    assert len(agents_list) == 2
    for agent_dict in agents_list:
        agent = AgentRead(**agent_dict) # Validate structure
        assert agent.agent_id is not None

def test_update_agent():
    # Create an agent
    agent_data = AgentCreate(name="Agent Gamma", description="Before update")
    create_response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    agent_id = create_response.json()["agent_id"]
    original_created_at = create_response.json()["created_at"]

    # Update the agent
    update_payload = AgentUpdate(name="Agent Gamma Updated", status=AgentStatus.ACTIVE, description="After update")
    response = client.put(f"/api/v1/agents/{agent_id}", json=update_payload.model_dump(exclude_unset=True))
    assert response.status_code == 200
    updated_agent = AgentRead(**response.json())
    assert updated_agent.name == "Agent Gamma Updated"
    assert updated_agent.status == AgentStatus.ACTIVE
    assert updated_agent.description == "After update"
    assert updated_agent.agent_id == uuid.UUID(agent_id)
    assert updated_agent.created_at == original_created_at # Should not change
    assert updated_agent.updated_at > original_created_at

def test_update_nonexistent_agent():
    non_existent_uuid = uuid.uuid4()
    update_payload = AgentUpdate(name="Doesn't Matter")
    response = client.put(f"/api/v1/agents/{non_existent_uuid}", json=update_payload.model_dump(exclude_unset=True))
    assert response.status_code == 404

def test_delete_agent():
    # Create an agent
    agent_data = AgentCreate(name="Agent Delta", description="To be deleted")
    create_response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    agent_id = create_response.json()["agent_id"]

    # Delete the agent
    response = client.delete(f"/api/v1/agents/{agent_id}")
    assert response.status_code == 200 # As per our router returning the deleted agent
    deleted_agent_data = response.json()
    assert deleted_agent_data["agent_id"] == agent_id

    # Verify it's gone
    get_response = client.get(f"/api/v1/agents/{agent_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_agent():
    non_existent_uuid = uuid.uuid4()
    response = client.delete(f"/api/v1/agents/{non_existent_uuid}")
    assert response.status_code == 404
