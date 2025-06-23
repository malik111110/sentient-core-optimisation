import pytest
from unittest.mock import MagicMock, patch
from sentient_core.orchestrator.main_orchestrator import MainOrchestrator
from sentient_core.orchestrator.shared_state import Task, Plan

@pytest.fixture
def mock_e2b_tool():
    tool = MagicMock()
    tool.run.return_value = {"output": "E2B tool executed successfully", "artifacts": []}
    return tool

@pytest.fixture
def mock_webcontainer_tool():
    tool = MagicMock()
    tool.run.return_value = {"url": "http://localhost:3000", "artifacts": ["http://localhost:3000"]}
    return tool

@patch('sentient_core.orchestrator.departmental_executors.E2BSandboxTool')
@patch('sentient_core.orchestrator.departmental_executors.WebContainerTool')
@patch('sentient_core.orchestrator.main_orchestrator.CSuitePlanner')
def test_orchestrator_end_to_end_integration(MockCSuitePlanner, MockWebContainerTool, MockE2BSandboxTool, mock_e2b_tool, mock_webcontainer_tool):
    """Verify the full orchestration flow from plan creation to agent tool execution."""
    # Arrange
    # Mock the tool instances
    MockE2BSandboxTool.return_value = mock_e2b_tool
    MockWebContainerTool.return_value = mock_webcontainer_tool

    # Mock the planner to return a predefined plan
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
    orchestrator.run()

    # Assert
    # 1. Verify the planner was called
    mock_planner_instance.create_plan.assert_called_once_with("Run integration test")

    # 2. Verify the sandbox tools were used correctly
    # Backend task should use the E2B tool
    e2b_run_calls = mock_e2b_tool.run.call_args_list
    assert len(e2b_run_calls) == 1
    e2b_input = e2b_run_calls[0].args[0]
    assert e2b_input.language == 'python'
    assert "Create a Python script" in e2b_input.script

    # Frontend task should use the WebContainer tool
    wc_run_calls = mock_webcontainer_tool.run.call_args_list
    assert len(wc_run_calls) == 1
    wc_input = wc_run_calls[0].args[0]
    assert "index.html" in wc_input.file_tree
    assert "<h1>Generate an HTML preview of the results.</h1>" in wc_input.file_tree["index.html"].file.contents

    # 3. Verify the final state reflects the completed tasks
    final_state = orchestrator.state
    assert len(final_state.completed_tasks) == 2
    assert final_state.completed_tasks[0].status == 'completed'
    assert "E2B tool executed successfully" in final_state.completed_tasks[0].task # This is a bit of a hack, but it works for this test
    assert final_state.completed_tasks[1].status == 'completed'
    assert "http://localhost:3000" in final_state.completed_tasks[1].task # Same hack as above
