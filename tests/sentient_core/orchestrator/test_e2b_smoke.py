import pytest
from unittest.mock import patch
from uuid import uuid4

from src.sentient_core.orchestrator.departmental_executors import DepartmentalExecutor
from src.sentient_core.orchestrator.shared_state import Task

@pytest.mark.asyncio
async def test_e2b_smoke():
    """Ensure a BackendDeveloperAgent task runs through E2BSandboxTool inside executor."""
    # Arrange
    task = Task(
        task_id=uuid4(),
        department="BackendDevelopment",
        task="print('Hello from E2B')",
        sandbox_type="e2b",
    )

    executor = DepartmentalExecutor()

    # Patch the E2BSandboxTool.run method to avoid real execution
    with patch("src.sentient_core.tools.e2b_sandbox_tool.E2BSandboxTool.run") as mock_run:
        mock_run.return_value = {
            "status": "success",
            "output": "Hello from E2B",
        }

        # Act
        result = await executor.execute_plan([task])

        # Assert
        mock_run.assert_called_once()
        assert result["status"] == "success"
        assert len(result["results"]) == 1
        completed = result["results"][0]
        assert completed["status"] == "completed"
        assert completed["task_id"] == task.task_id
