import pytest
from uuid import uuid4

from src.sentient_core.state.state_manager import StateManager
from src.sentient_core.state.state_models import WorkflowState, TaskState, TaskStatus, WorkflowStatus

@pytest.mark.asyncio
async def test_create_and_get_workflow(mock_db):
    """Verify workflow creation and retrieval."""
    # Arrange
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
    assert len(retrieved.tasks) == 1
    assert retrieved.tasks[0].department == "Test"
    assert retrieved.tasks[0].description == "Run test"

@pytest.mark.asyncio
async def test_update_task_status(mock_db):
    """Verify task status can be updated."""
    # Arrange
    workflow_id = str(uuid4())
    task_id = str(uuid4())
    
    # Mock the select to return a workflow with the task
    mock_db.select.return_value = [{
        "id": workflow_id,
        "tasks": {
            task_id: {
                "id": task_id,
                "status": TaskStatus.PENDING,
                "output_data": {}
            }
        }
    }]

    # Act
    await StateManager.update_task_status(
        workflow_id=workflow_id,
        task_id=task_id,
        status=TaskStatus.IN_PROGRESS,
        output_data={"key": "value"}
    )

    # Assert
    mock_db.update.assert_awaited_once()
    call_args = mock_db.update.call_args[0]
    assert f"workflows:{workflow_id}" == call_args[0]
    assert f"tasks.{task_id}.status" in call_args[1]
    assert call_args[1][f"tasks.{task_id}.status"] == TaskStatus.IN_PROGRESS
    assert f"tasks.{task_id}.output_data" in call_args[1]
    assert call_args[1][f"tasks.{task_id}.output_data"] == {"key": "value"}

@pytest.mark.asyncio
async def test_set_workflow_status(mock_db):
    """Verify workflow status can be updated."""
    # Arrange
    workflow_id = str(uuid4())
    
    # Mock the select to return a workflow
    mock_db.select.return_value = [{
        "id": workflow_id,
        "status": WorkflowStatus.RUNNING,
        "tasks": {}
    }]

    # Act
    await StateManager.set_workflow_status(workflow_id, WorkflowStatus.COMPLETED)

    # Assert
    mock_db.update.assert_awaited_once()
    call_args = mock_db.update.call_args[0]
    assert f"workflows:{workflow_id}" == call_args[0]
    assert "status" in call_args[1]
    assert call_args[1]["status"] == WorkflowStatus.COMPLETED.value  # Note: .value for enum string value
    
    # Verify we're using the correct SurrealDB update syntax
    assert "=" in str(mock_db.update.call_args[1])  # Check we're using the update syntax
