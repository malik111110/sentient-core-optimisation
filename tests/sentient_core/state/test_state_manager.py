import pytest
from unittest.mock import AsyncMock, patch

from src.sentient_core.state.state_manager import StateManager
from src.sentient_core.state.state_models import WorkflowState, TaskState, TaskStatus, WorkflowStatus

@pytest.fixture
def mock_db():
    """Provides a mock SurrealDB client."""
    db = AsyncMock()
    db.select.return_value = []
    db.create.return_value = None
    db.update.return_value = None
    db.query.return_value = None
    return db

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_create_and_get_workflow(mock_get_db, mock_db):
    """Verify workflow creation and retrieval."""
    # Arrange
    mock_get_db.return_value = mock_db
    task = TaskState(department="Test", description="Run test")
    workflow = WorkflowState(project_name="Test Project", tasks=[task])

    # Mock the select call to return the created workflow
    mock_db.select.return_value = [workflow.model_dump(by_alias=True)]

    # Act
    created = await StateManager.create_workflow(workflow)
    retrieved = await StateManager.get_workflow(workflow.id)

    # Assert
    assert created.id == workflow.id
    mock_db.create.assert_awaited_once()
    assert retrieved is not None
    assert retrieved.id == workflow.id
    assert retrieved.project_name == "Test Project"

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_update_task_status(mock_get_db, mock_db):
    """Verify task status can be updated."""
    # Arrange
    mock_get_db.return_value = mock_db
    workflow_id = "wf_123"
    task_id = "task_abc"

    # Act
    await StateManager.update_task_status(
        workflow_id,
        task_id,
        status=TaskStatus.COMPLETED,
        output_data={"result": "success"}
    )

    # Assert
    mock_db.query.assert_awaited_once()
    query_str = mock_db.query.call_args[0][0]
    assert "tasks[$idx].status = $status" in query_str
    assert "tasks[$idx].output_data = $out" in query_str

@pytest.mark.asyncio
@patch('src.sentient_core.state.db.get_db')
async def test_set_workflow_status(mock_get_db, mock_db):
    """Verify workflow status can be updated."""
    # Arrange
    mock_get_db.return_value = mock_db
    workflow_id = "wf_123"

    # Act
    await StateManager.set_workflow_status(workflow_id, WorkflowStatus.COMPLETED)

    # Assert
    mock_db.update.assert_awaited_once_with(
        f"workflow_state:{workflow_id}",
        {"status": WorkflowStatus.COMPLETED}
    )
