import pytest
from unittest.mock import MagicMock, patch
from sentient_core.orchestrator.main_orchestrator import MainOrchestrator
from sentient_core.orchestrator.shared_state import Task, Plan

@pytest.fixture
def mock_e2b_tool():
    tool = MagicMock()
    tool.run.return_value = {"output": "E2B tool executed successfully", "status": "completed"}
    return tool

@pytest.fixture
def mock_webcontainer_tool():
    tool = MagicMock()
    tool.run.return_value = {"url": "http://localhost:3000", "status": "completed"}
    return tool

@pytest.mark.asyncio
@patch('sentient_core.orchestrator.departmental_executors.E2BSandboxTool')
@patch('sentient_core.orchestrator.departmental_executors.WebContainerTool')
@patch('sentient_core.orchestrator.main_orchestrator.CSuitePlanner')
async def test_orchestrator_end_to_end_integration(MockCSuitePlanner, MockWebContainerTool, MockE2BSandboxTool, mock_e2b_tool, mock_webcontainer_tool):
    """Verify the full orchestration flow from plan creation to agent tool execution."""
    # Arrange
    MockE2BSandboxTool.return_value = mock_e2b_tool
    MockWebContainerTool.return_value = mock_webcontainer_tool

    mock_planner_instance = MockCSuitePlanner.return_value
    mock_plan = {
        "project_name": "Integrated Test Project",
        "tasks": [
            {"department": "BackendDevelopment", "task": "Create a Python script to process data."},
            {"department": "FrontendDevelopment", "task": "Generate an HTML preview of the results."}
        ]
    }
    mock_planner_instance.create_plan.return_value = mock_plan

    # Act
    orchestrator = MainOrchestrator(command="Run integration test")
    await orchestrator.run()

    # Assert
    mock_planner_instance.create_plan.assert_called_once_with("Run integration test")

    # Verify the correct agents were instantiated and their tools were called
    assert mock_e2b_tool.run.call_count == 1
    assert mock_webcontainer_tool.run.call_count == 1

    # Verify the final state reflects the completed tasks
    final_state = orchestrator.state
    assert len(final_state.completed_tasks) == 2
    assert final_state.completed_tasks[0]["status"] == 'completed'
    assert final_state.completed_tasks[1]["status"] == 'completed'
