from ..agents.base_agent import BaseAgent
from ..orchestrator.shared_state import Task
from typing import Optional, Any, Dict

class BridgeAgent(BaseAgent):
    """Agent that stitches together frontend & backend sandbox outputs.

    It expects ``task.input_data`` to contain::

        {
            "frontend_url": "http://<webcontainer-host>",
            "backend_url": "http://<e2b-host>"
        }

    The agent generates a small ``bridge.js`` snippet that calls the backend
    and returns it as an artifact so the Front-end can import it.
    """

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="BridgeAgent", sandbox_tool=sandbox_tool)

    def execute_task(self, task: Task) -> Dict[str, Any]:
        self.log(f"Executing bridge task: {task.task}")

        frontend_url = task.input_data.get("frontend_url")
        backend_url = task.input_data.get("backend_url")
        if not frontend_url or not backend_url:
            return {
                "status": "failed",
                "message": "BridgeAgent requires 'frontend_url' and 'backend_url' in input_data",
            }

        bridge_js = f"""
const BACKEND_URL = '{backend_url}';

export async function backendHealth() {{
  const res = await fetch(`${{BACKEND_URL}}/health`);
  if (!res.ok) throw new Error('Backend unreachable');
  const data = await res.json();
  document.getElementById('backend-response').innerText = JSON.stringify(data);
  return data;
}}

export function startHealthStream() {{
  const evt = new EventSource(`${{BACKEND_URL}}/health/stream`);
  evt.onmessage = (e) => {{
    document.getElementById('backend-response').innerText = e.data;
  }};
  evt.onerror = (err) => console.error('SSE error', err);
}}

export function setupHotReload() {{
  // Vite-style hot reload support inside WebContainer
  if (import.meta.hot) {{
    import.meta.hot.accept(() => window.location.reload());
  }}
}}
"""

        # Persist bridge.js to the WebContainer file system if a WebContainerTool is available.
        if self.sandbox_tool and hasattr(self.sandbox_tool, "run"):
            try:
                from ..tools.webcontainer_tool import WebContainerToolInput, WebContainerTool
                if isinstance(self.sandbox_tool, WebContainerTool):
                    wc_input = WebContainerToolInput(files={"bridge.js": bridge_js}, commands=[])
                    self.sandbox_tool.run(wc_input)
            except Exception as exc:
                # Non-fatal – continue even if write fails
                self.log(f"Failed to write bridge.js via sandbox_tool: {exc}")
        result = {
            "status": "completed",
            "message": "bridge.js generated linking frontend & backend",
            "artifacts": [bridge_js],
        }
        self.log("Bridge task completed")
        return result
