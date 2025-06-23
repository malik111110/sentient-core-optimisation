import pytest
from unittest.mock import patch
from uuid import uuid4

from src.sentient_core.orchestrator.departmental_executors import DepartmentalExecutor
from src.sentient_core.orchestrator.shared_state import Task


def test_webcontainer_smoke():
    """Ensure a FrontendDeveloperAgent task runs through WebContainerTool inside executor."""
    # Arrange
    task = Task(
        task_id=uuid4(),
        department="FrontendDevelopment",
        task="Generate hello world HTML page",
        sandbox_type="webcontainer"
    )

    executor = DepartmentalExecutor()

    # Patch the WebContainerTool.run method to avoid real execution
    with patch("src.sentient_core.tools.webcontainer_tool.WebContainerTool.run") as mock_run:
        mock_run.return_value = {
            "status": "success",
            "message": "WebContainer task dispatched to the client for execution.",
            "details": {"url": "https://example.com"}
        }

        # Act
        result = executor.execute_plan([task])

        # Assert
        mock_run.assert_called_once()
        assert result["status"] == "success"
        completed = result["results"][0]
        assert completed["status"] == "completed"
        assert completed["task_id"] == task.task_id
