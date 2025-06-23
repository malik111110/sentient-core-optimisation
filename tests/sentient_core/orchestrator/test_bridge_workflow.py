import pytest
from unittest.mock import patch
from uuid import uuid4

from src.sentient_core.orchestrator.departmental_executors import DepartmentalExecutor
from src.sentient_core.orchestrator.shared_state import Task

@pytest.mark.asyncio
async def test_bridge_workflow():
    """Full workflow: frontend -> backend -> bridge."""
    # Arrange
    frontend_task = Task(
        task_id=uuid4(),
        department="FrontendDevelopment",
        task="Generate Hello UI",
        sandbox_type="webcontainer",
    )
    backend_task = Task(
        task_id=uuid4(),
        department="BackendDevelopment",
        task="FastAPI /health endpoint",
        sandbox_type="e2b",
    )
    bridge_task = Task(
        task_id=uuid4(),
        department="Bridge",
        task="Connect frontend & backend",
        depends_on=[frontend_task.task_id, backend_task.task_id],
        input_data={},
    )
    tasks = [frontend_task, backend_task, bridge_task]
    executor = DepartmentalExecutor()

    # Mock the direct outputs of the agents the bridge depends on
    with patch('src.sentient_core.specialized_agents.FrontendDeveloperAgent.execute_task') as mock_frontend_agent, \
         patch('src.sentient_core.specialized_agents.BackendDeveloperAgent.execute_task') as mock_backend_agent:
        
        mock_frontend_agent.return_value = {"status": "completed", "url": "http://frontend.test"}
        mock_backend_agent.return_value = {"status": "completed", "url": "http://backend.test"}

        # Act
        result = await executor.execute_plan(tasks)

    # Assert
    assert result["status"] == "success"
    outputs = result["results"]
    assert len(outputs) == 3

    # Verify the BridgeAgent received the correct inputs and produced its artifact
    bridge_output = next((o for o in outputs if o.get("task_id") == bridge_task.task_id), None)
    assert bridge_output is not None
    assert bridge_output["status"] == "completed"
    
    # The BridgeAgent itself creates the JS artifact based on the injected URLs
    bridge_js_artifact = bridge_output["artifacts"][0]
    assert "const backendUrl = 'http://backend.test';" in bridge_js_artifact
    assert "const frontendUrl = 'http://frontend.test';" in bridge_js_artifact
