import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.api.models.memory_models import MemoryNode, MemoryEdge, NodeType, EdgeType, SurrealID
from src.api.persistence.surrealdb_persistence import create_node, get_node, create_edge

@pytest.fixture
def mock_surreal_client():
    """Provides a mock SurrealDB client with async methods."""
    mock_db = AsyncMock()
    mock_db.create = AsyncMock()
    mock_db.select = AsyncMock()
    mock_db.query = AsyncMock()
    mock_db.close = AsyncMock()
    return mock_db

@pytest.mark.asyncio
@patch('src.api.persistence.surrealdb_persistence.get_surrealdb_client')
async def test_create_node_success(mock_get_client, mock_surreal_client):
    """Verify successful creation of a MemoryNode."""
    # Arrange
    mock_get_client.return_value = mock_surreal_client
    node_to_create = MemoryNode(node_type=NodeType.CONCEPT, content="Test concept")
    mock_surreal_client.create.return_value = {
        "id": "memory_node:test_id",
        **node_to_create.model_dump()
    }

    # Act
    created_node = await create_node(node_to_create)

    # Assert
    assert created_node is not None
    assert created_node.id == "memory_node:test_id"
    assert created_node.content == "Test concept"
    mock_surreal_client.create.assert_called_once_with("memory_node", node_to_create.model_dump(exclude_none=True, exclude={'id'}))
    mock_surreal_client.close.assert_called_once()

@pytest.mark.asyncio
@patch('src.api.persistence.surrealdb_persistence.get_surrealdb_client')
async def test_get_node_success(mock_get_client, mock_surreal_client):
    """Verify successful retrieval of a MemoryNode."""
    # Arrange
    mock_get_client.return_value = mock_surreal_client
    node_id = SurrealID("memory_node:test_id")
    mock_node_data = {
        "id": node_id,
        "node_type": NodeType.CONCEPT,
        "content": "Fetched concept"
    }
    mock_surreal_client.select.return_value = mock_node_data

    # Act
    fetched_node = await get_node(node_id)

    # Assert
    assert fetched_node is not None
    assert fetched_node.id == node_id
    assert fetched_node.content == "Fetched concept"
    mock_surreal_client.select.assert_called_once_with(node_id)
    mock_surreal_client.close.assert_called_once()

@pytest.mark.asyncio
@patch('src.api.persistence.surrealdb_persistence.get_surrealdb_client')
async def test_create_edge_success(mock_get_client, mock_surreal_client):
    """Verify successful creation of a MemoryEdge."""
    # Arrange
    mock_get_client.return_value = mock_surreal_client
    source_id = SurrealID("memory_node:source")
    target_id = SurrealID("memory_node:target")
    edge_to_create = MemoryEdge(
        source_node_id=source_id,
        target_node_id=target_id,
        edge_type=EdgeType.RELATES_TO
    )
    mock_query_result = [{
        'result': [{
            'id': 'relates_to:test_edge_id',
            'in': source_id,
            'out': target_id,
            'edge_type': 'RELATES_TO',
            'weight': 1.0
        }]
    }]
    mock_surreal_client.query.return_value = mock_query_result

    # Act
    created_edge = await create_edge(source_id, target_id, edge_to_create)

    # Assert
    assert created_edge is not None
    assert created_edge.id == "relates_to:test_edge_id"
    assert created_edge.source_node_id == source_id
    assert created_edge.target_node_id == target_id
    mock_surreal_client.query.assert_called_once()
    mock_surreal_client.close.assert_called_once()
