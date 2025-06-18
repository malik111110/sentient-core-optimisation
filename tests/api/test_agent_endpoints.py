import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from src.main import app # app instance from src/main.py
from src.api.models.core_models import AgentCreate, AgentRead, AgentUpdate, AgentStatus
# We will patch the supabase_client within the persistence module directly in tests

client = TestClient(app)

# No longer need to clear in-memory DB as we are mocking persistence

def test_read_api_v1_root():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Sentient Core API v1"}

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_create_agent(mock_supabase_client):
    agent_data = AgentCreate(
        name="Test Agent Alpha",
        description="An agent for testing creation.",
        capabilities=["test", "create"],
        config={"param1": "value1"}
    )

    # Mock Supabase response for insert
    mock_response = MagicMock()
    # Simulate the data returned by Supabase after insert
    # This needs to match what AgentRead expects, including generated fields
    created_agent_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    mock_response.data = [{
        **agent_data.model_dump(),
        "agent_id": str(created_agent_id),
        "status": AgentStatus.INACTIVE.value,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }]
    mock_supabase_client.table().insert().execute.return_value = mock_response

    response = client.post("/api/v1/agents/", json=agent_data.model_dump())
    
    assert response.status_code == 201
    created_agent_response_data = response.json()
    assert created_agent_response_data["name"] == agent_data.name
    assert created_agent_response_data["description"] == agent_data.description
    assert created_agent_response_data["capabilities"] == agent_data.capabilities
    assert created_agent_response_data["config"] == agent_data.config
    assert uuid.UUID(created_agent_response_data["agent_id"]) # Check if it's a valid UUID string
    assert created_agent_response_data["status"] == AgentStatus.INACTIVE.value
    assert created_agent_response_data["created_at"] is not None
    assert created_agent_response_data["updated_at"] is not None
    # Timestamps might not be exactly equal due to isoformat conversion and back, compare dates or be lenient
    # For this mock, they are set to the same 'now' value, so they should match after parsing
    assert datetime.fromisoformat(created_agent_response_data["created_at"]) == datetime.fromisoformat(created_agent_response_data["updated_at"])

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_specific_agent(mock_supabase_client):
    agent_id_str = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expected_agent_data = {
        "agent_id": agent_id_str,
        "name": "Test Agent Beta",
        "description": "For get test",
        "capabilities": [],
        "config": {},
        "status": AgentStatus.INACTIVE.value,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    mock_response = MagicMock()
    mock_response.data = expected_agent_data
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_response

    response = client.get(f"/api/v1/agents/{agent_id_str}")
    assert response.status_code == 200
    retrieved_agent = AgentRead(**response.json())
    assert str(retrieved_agent.agent_id) == agent_id_str
    assert retrieved_agent.name == expected_agent_data["name"]

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_get_nonexistent_agent(mock_supabase_client):
    non_existent_uuid = str(uuid.uuid4())
    mock_response = MagicMock()
    mock_response.data = None # Simulate agent not found
    # Alternative for some Supabase client versions: raise an error that results in None
    # from postgrest.exceptions import APIError
    # mock_supabase_client.table().select().eq().single().execute.side_effect = APIError(...)
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_response 

    response = client.get(f"/api/v1/agents/{non_existent_uuid}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found"

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_list_agents(mock_supabase_client):
    now = datetime.now(timezone.utc)
    agents_data = [
        {"agent_id": str(uuid.uuid4()), "name": "Agent One", "status": AgentStatus.INACTIVE.value, "created_at": now.isoformat(), "updated_at": now.isoformat(), "description": "", "capabilities": [], "config": {}},
        {"agent_id": str(uuid.uuid4()), "name": "Agent Two", "status": AgentStatus.INACTIVE.value, "created_at": now.isoformat(), "updated_at": now.isoformat(), "description": "", "capabilities": [], "config": {}}
    ]
    mock_response = MagicMock()
    mock_response.data = agents_data
    mock_supabase_client.table().select().range().execute.return_value = mock_response

    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    agents_list_response = response.json()
    assert isinstance(agents_list_response, list)
    assert len(agents_list_response) == 2
    assert agents_list_response[0]["name"] == "Agent One"
    assert agents_list_response[1]["name"] == "Agent Two"

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_update_agent(mock_supabase_client):
    agent_id_str = str(uuid.uuid4())
    original_created_at_dt = datetime.now(timezone.utc) - timedelta(days=1)
    original_created_at_iso = original_created_at_dt.isoformat()

    # Mock the initial state if get_agent is called internally by update_agent (it's not directly, but good for complex cases)
    # For this test, we primarily care about the update().execute() response.
    update_payload = AgentUpdate(name="Agent Gamma Updated", status=AgentStatus.ACTIVE, description="After update")
    
    updated_agent_data_from_db = {
        "agent_id": agent_id_str,
        "name": update_payload.name,
        "description": update_payload.description,
        "capabilities": [], # Assuming not updated
        "config": {}, # Assuming not updated
        "status": update_payload.status.value,
        "created_at": original_created_at_iso, # Should remain the same
        "updated_at": datetime.now(timezone.utc).isoformat() # Should be new
    }
    mock_update_response = MagicMock()
    mock_update_response.data = updated_agent_data_from_db
    mock_supabase_client.table().update().eq().select().single().execute.return_value = mock_update_response

    response = client.put(f"/api/v1/agents/{agent_id_str}", json=update_payload.model_dump(exclude_unset=True))
    assert response.status_code == 200
    updated_agent_response = response.json()
    assert updated_agent_response["name"] == "Agent Gamma Updated"
    assert updated_agent_response["status"] == AgentStatus.ACTIVE.value
    assert updated_agent_response["description"] == "After update"
    assert updated_agent_response["agent_id"] == agent_id_str
    assert updated_agent_response["created_at"] == original_created_at_iso
    assert datetime.fromisoformat(updated_agent_response["updated_at"]) > original_created_at_dt

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_update_nonexistent_agent(mock_supabase_client):
    non_existent_uuid_str = str(uuid.uuid4())
    update_payload = AgentUpdate(name="Doesn't Matter")
    
    mock_update_response = MagicMock()
    mock_update_response.data = None # Simulate agent not found for update
    mock_supabase_client.table().update().eq().select().single().execute.return_value = mock_update_response

    response = client.put(f"/api/v1/agents/{non_existent_uuid_str}", json=update_payload.model_dump(exclude_unset=True))
    assert response.status_code == 404

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_delete_agent(mock_supabase_client):
    agent_id_str = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    agent_to_delete_data = {
        "agent_id": agent_id_str,
        "name": "Agent Delta", 
        "description": "To be deleted",
        "capabilities": [], "config": {},
        "status": AgentStatus.INACTIVE.value,
        "created_at": now.isoformat(), 
        "updated_at": now.isoformat()
    }

    # Mock for the get_agent call inside delete_agent
    mock_get_response = MagicMock()
    mock_get_response.data = agent_to_delete_data
    
    # Mock for the delete call
    mock_delete_response = MagicMock()
    mock_delete_response.data = [agent_to_delete_data] # Supabase delete might return the deleted record(s)
    # Or if it doesn't return data but a status: mock_delete_response.status_code = 200 (or 204)

    # Chain the mocks: first for get, then for delete
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response
    mock_supabase_client.table().delete().eq().execute.return_value = mock_delete_response

    response = client.delete(f"/api/v1/agents/{agent_id_str}")
    assert response.status_code == 200
    deleted_agent_response_data = response.json()
    assert deleted_agent_response_data["agent_id"] == agent_id_str

    # Verify it's gone (mock get_agent to return None now)
    mock_get_response_after_delete = MagicMock()
    mock_get_response_after_delete.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response_after_delete
    
    get_response = client.get(f"/api/v1/agents/{agent_id_str}")
    assert get_response.status_code == 404

@patch('src.api.persistence.supabase_persistence.supabase_client')
def test_delete_nonexistent_agent(mock_supabase_client):
    non_existent_uuid_str = str(uuid.uuid4())
    
    # Mock for the get_agent call inside delete_agent, returning None
    mock_get_response = MagicMock()
    mock_get_response.data = None
    mock_supabase_client.table().select().eq().single().execute.return_value = mock_get_response

    response = client.delete(f"/api/v1/agents/{non_existent_uuid_str}")
    assert response.status_code == 404

# Need to import timedelta for test_update_agent
from datetime import timedelta
