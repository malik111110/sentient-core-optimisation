from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState


class BridgeAgent(BaseAgent):
    """Agent that stitches together frontend & backend sandbox outputs."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="BridgeAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        """Generates a bridge.js script to link frontend and backend services."""
        frontend_url = task.input_data.get("frontend_url")
        backend_url = task.input_data.get("backend_url")
        if not frontend_url or not backend_url:
            raise ValueError(
                "BridgeAgent requires 'frontend_url' and 'backend_url' in input_data"
            )

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
                from ..tools.webcontainer_tool import WebContainerTool, WebContainerToolInput

                if isinstance(self.sandbox_tool, WebContainerTool):
                    wc_input = WebContainerToolInput(files={"src/bridge.js": bridge_js}, commands=[])
                    await self.sandbox_tool.run(wc_input)
                    await self.log(workflow_id, task.id, "Successfully wrote bridge.js to WebContainer.")
            except Exception as exc:
                # Non-fatal – continue even if write fails
                await self.log(
                    workflow_id,
                    task.id,
                    f"Failed to write bridge.js via sandbox_tool: {exc}",
                    level="warn",
                )

        return {
            "status": "completed",
            "message": "bridge.js generated linking frontend & backend",
            "artifacts": [bridge_js],
        }
