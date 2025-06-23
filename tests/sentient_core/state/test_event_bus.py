import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.sentient_core.state.event_bus import EventBus
from src.sentient_core.state.state_models import AgentEvent, EventType

@pytest.fixture
def mock_db():
    """Provides a mock SurrealDB client."""
    db = AsyncMock()
    db.create.return_value = None
    db.query.return_value = None
    return db

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_publish_event(mock_get_db, mock_db):
    """Verify that an event is correctly persisted."""
    # Arrange
    mock_get_db.return_value = mock_db
    event = AgentEvent(
        event_type=EventType.AGENT_STARTED,
        source_agent="TestAgent",
        workflow_id="wf_123"
    )

    # Act
    await EventBus.publish_event(event)

    # Assert
    mock_db.create.assert_awaited_once()
    call_args = mock_db.create.call_args[0]
    assert f"agent_events:{event.id}" == call_args[0]
    assert event.model_dump(by_alias=True) == call_args[1]['data']

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_get_event_history(mock_get_db, mock_db):
    """Verify that event history is retrieved and filtered correctly."""
    # Arrange
    mock_get_db.return_value = mock_db
    workflow_id = str(uuid4())
    event1 = AgentEvent(event_type=EventType.AGENT_STARTED, source_agent="A", workflow_id=workflow_id)
    event2 = AgentEvent(event_type=EventType.AGENT_COMPLETED, source_agent="A", workflow_id=workflow_id)
    
    # Mock the query result
    mock_db.query.return_value = [
        {"result": [event1.model_dump(by_alias=True), event2.model_dump(by_alias=True)]}
    ]

    # Act
    history = await EventBus.get_event_history(workflow_id)

    # Assert
    assert len(history) == 2
    assert history[0].id == event1.id
    assert history[1].id == event2.id
    mock_db.query.assert_awaited_once()
    query_str = mock_db.query.call_args[0][0]
    assert "ORDER BY created_at ASC" in query_str
    assert "event_type = $e_type" not in query_str # No filter applied

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_get_event_history_with_filter(mock_get_db, mock_db):
    """Verify that event history filtering works."""
    # Arrange
    mock_get_db.return_value = mock_db
    workflow_id = str(uuid4())
    event = AgentEvent(event_type=EventType.AGENT_COMPLETED, source_agent="A", workflow_id=workflow_id)
    mock_db.query.return_value = [
        {"result": [event.model_dump(by_alias=True)]}
    ]

    # Act
    await EventBus.get_event_history(workflow_id, event_type=EventType.AGENT_COMPLETED)

    # Assert
    mock_db.query.assert_awaited_once()
    query_str = mock_db.query.call_args[0][0]
    params = mock_db.query.call_args[0][1]
    assert "event_type = $e_type" in query_str
    assert params["e_type"] == EventType.AGENT_COMPLETED.value
