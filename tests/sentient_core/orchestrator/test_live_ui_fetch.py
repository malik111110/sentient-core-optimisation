from unittest.mock import patch
from uuid import uuid4

from src.sentient_core.orchestrator.departmental_executors import DepartmentalExecutor
from src.sentient_core.orchestrator.shared_state import Task


def test_live_ui_fetch():
    """Ensure bridge.js persisted and script tag in index.html."""
    files_written = {}

    def fake_wc_run(input_obj):
        # store provided files
        files_written.update(input_obj.files)
        return {"url": "http://wc-host"}

    def fake_e2b_run(_):
        return {"status": "success", "url": "http://e2b-host"}

    frontend = Task(task_id=uuid4(), department="FrontendDevelopment", task="Hello UI", sandbox_type="webcontainer")
    backend = Task(task_id=uuid4(), department="BackendDevelopment", task="FastAPI /health", sandbox_type="e2b")
    bridge = Task(task_id=uuid4(), department="Bridge", task="connect", depends_on=[frontend.task_id, backend.task_id])

    ex = DepartmentalExecutor()

    with patch("src.sentient_core.tools.webcontainer_tool.WebContainerTool.run", side_effect=fake_wc_run) as mock_wc, \
         patch("src.sentient_core.tools.e2b_sandbox_tool.E2BSandboxTool.run", side_effect=fake_e2b_run):
        res = ex.execute_plan([frontend, backend, bridge])
        assert res["status"] == "success"
        # bridge.js should be written
        assert "bridge.js" in files_written
        assert "http://e2b-host/health" in files_written["bridge.js"]
        # index.html written and contains script tag
        assert "index.html" in files_written
        assert "script type=\"module\" src=\"bridge.js\"" in files_written["index.html"]
