import pytest
from unittest.mock import patch, MagicMock
import asyncio

from src.sentient_core.orchestrator.shared_state import Task
from src.sentient_core.specialized_agents.data_agent import DataAgent
from src.api.models.memory_models import MemoryNode, MemoryEdge, NodeType, EdgeType, SurrealID

@pytest.fixture
def data_agent():
    """Provides an instance of the DataAgent for testing."""
    return DataAgent()

@pytest.mark.asyncio
@patch('src.sentient_core.specialized_agents.data_agent.create_node')
async def test_data_agent_create_node_success(mock_create_node, data_agent):
    """Verify DataAgent successfully handles a 'create node' task."""
    # Arrange
    mock_create_node.return_value = MemoryNode(
        id=SurrealID("memory_node:test_id"),
        node_type=NodeType.CONCEPT,
        content="Test content"
    )
    task = Task(
        task_id="uuid1",
        task="create node for concept",
        input_data={"node_type": "CONCEPT", "content": "Test content"}
    )

    # Act
    result = data_agent.execute_task(task)

    # Assert
    assert result["status"] == "completed"
    assert "Successfully created memory node" in result["message"]
    assert "memory_node:test_id" in result["message"]
    mock_create_node.assert_called_once()

@pytest.mark.asyncio
@patch('src.sentient_core.specialized_agents.data_agent.create_edge')
async def test_data_agent_create_edge_success(mock_create_edge, data_agent):
    """Verify DataAgent successfully handles a 'create edge' task."""
    # Arrange
    mock_create_edge.return_value = MemoryEdge(
        id=SurrealID("relates_to:edge_id"),
        source_node_id=SurrealID("memory_node:source"),
        target_node_id=SurrealID("memory_node:target"),
        edge_type=EdgeType.RELATES_TO
    )
    task = Task(
        task_id="uuid2",
        task="create edge between nodes",
        input_data={
            "source_id": "memory_node:source",
            "target_id": "memory_node:target",
            "edge_type": "RELATES_TO"
        }
    )

    # Act
    result = data_agent.execute_task(task)

    # Assert
    assert result["status"] == "completed"
    assert "Successfully created edge" in result["message"]
    mock_create_edge.assert_called_once()

def test_data_agent_invalid_input(data_agent):
    """Verify DataAgent returns a failed status with invalid input."""
    # Arrange
    task = Task(
        task_id="uuid3",
        task="create node", # Missing input_data
        input_data={}
    )

    # Act
    result = data_agent.execute_task(task)

    # Assert
    assert result["status"] == "failed"
    assert "Missing 'node_type' or 'content'" in result["message"]

def test_data_agent_unsupported_action(data_agent):
    """Verify DataAgent returns a failed status for an unsupported action."""
    # Arrange
    task = Task(
        task_id="uuid4",
        task="delete the database",
        input_data={}
    )

    # Act
    result = data_agent.execute_task(task)

    # Assert
    assert result["status"] == "failed"
    assert "DataAgent does not support action" in result["message"]
