from uuid import uuid4
from unittest.mock import MagicMock

from src.sentient_core.specialized_agents.bridge_agent import BridgeAgent
from src.sentient_core.orchestrator.shared_state import Task


def test_bridge_js_has_enhancements():
    mocked_wc_tool = MagicMock()

    task = Task(
        task_id=uuid4(),
        department="Bridge",
        task="Connect",
        input_data={"frontend_url": "http://wc-host", "backend_url": "http://e2b-host"},
        sandbox_type="webcontainer",
    )

    agent = BridgeAgent(sandbox_tool=mocked_wc_tool)
    result = agent.execute_task(task)
    assert result["status"] == "completed"
    bridge_js = result["artifacts"][0]
    # Contains new functions
    assert "startHealthStream" in bridge_js
    assert "setupHotReload" in bridge_js
    # Uses placeholder replacement
    assert "${BACKEND_URL}" in bridge_js
