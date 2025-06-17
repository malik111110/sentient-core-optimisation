import pytest
from unittest.mock import MagicMock, patch
from src.clients.fetchai_adapter import FetchAIAdapter

@pytest.fixture
def mock_agent(mocker):
    """Mocks the uagents.Agent class."""
    mock = MagicMock()
    mocker.patch('src.clients.fetchai_adapter.Agent', return_value=mock)
    return mock

def test_adapter_initialization(mock_agent):
    """Tests that the adapter initializes a uagents.Agent correctly."""
    # Arrange
    name = "test_agent"
    seed = "test_seed"

    # Act
    adapter = FetchAIAdapter(name=name, seed=seed)

    # Assert
    from src.clients.fetchai_adapter import Agent
    Agent.assert_called_once_with(name=name, seed=seed)
    assert adapter.agent is not None
    # Check that the startup event handler was registered
    mock_agent.on_event.assert_called_once_with("startup")

def test_run_method(mock_agent):
    """Tests that the adapter's run method calls the agent's run method."""
    # Arrange
    adapter = FetchAIAdapter(name="test_agent", seed="test_seed")

    # Act
    adapter.run()

    # Assert
    mock_agent.run.assert_called_once()
