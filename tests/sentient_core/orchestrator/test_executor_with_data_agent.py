import pytest
from unittest.mock import patch, MagicMock
import asyncio
from uuid import uuid4

from src.sentient_core.orchestrator.departmental_executors import DepartmentalExecutor
from src.sentient_core.orchestrator.shared_state import Task
from src.api.models.memory_models import MemoryNode, NodeType, SurrealID

@pytest.fixture
def executor():
    """Provides an instance of the DepartmentalExecutor."""
    with patch('src.sentient_core.tools.E2BSandboxTool'), patch('src.sentient_core.tools.WebContainerTool'):
        yield DepartmentalExecutor()

@pytest.mark.asyncio
@patch('src.sentient_core.specialized_agents.data_agent.create_node')
async def test_executor_handles_data_agent_task(mock_create_node, executor):
    """Verify the DepartmentalExecutor can route a task to the DataAgent and execute it."""
    # Arrange
    async def async_create_node(*args, **kwargs):
        return MemoryNode(
            id=SurrealID("memory_node:mock_id"),
            node_type=NodeType.CONCEPT,
            content="Mocked content"
        )
    mock_create_node.side_effect = async_create_node

    data_task = Task(
        task_id=uuid4(),
        department="Data",
        task="Create a new memory node for a concept.",
        input_data={"node_type": "CONCEPT", "content": "Test concept from executor"}
    )

    # Act
    result = await executor.execute_plan([data_task])

    # Assert
    assert result["status"] == "success"
    assert len(result["results"]) == 1
    task_result = result["results"][0]
    assert task_result["status"] == "completed"
    assert "Successfully created memory node memory_node:mock_id" in task_result["message"]

    mock_create_node.assert_called_once()
    call_args = mock_create_node.call_args[0][0]
    assert isinstance(call_args, MemoryNode)
    assert call_args.node_type == NodeType.CONCEPT
    assert call_args.content == "Test concept from executor"
