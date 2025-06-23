from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.sentient_core.state.event_bus import EventBus
from src.sentient_core.state.state_manager import StateManager
from src.sentient_core.state.state_models import AgentEvent, EventType, TaskState, TaskStatus


class BaseAgent(ABC):
    """Abstract base class for stateful, event-driven agents."""

    def __init__(self, name: str, sandbox_tool: Optional[Any] = None):
        self.name = name
        self.sandbox_tool = sandbox_tool

    @abstractmethod
    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        """
        Core logic implementation for the agent's task.

        Args:
            task: The specific task state object for this agent to execute.

        Returns:
            A dictionary containing the results to be saved as output_data.
        """
        pass

    async def execute_task(self, workflow_id: str, task_id: str) -> None:
        """Orchestrates the full lifecycle of a task execution."""
        await self._publish_event(workflow_id, task_id, EventType.AGENT_STARTED)
        await StateManager.update_task_status(workflow_id, task_id, status=TaskStatus.IN_PROGRESS)

        try:
            workflow = await StateManager.get_workflow(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")

            task = next((t for t in workflow.tasks if t.id == task_id), None)
            if not task:
                raise ValueError(f"Task {task_id} not found in workflow {workflow_id}.")

            await self.log(workflow_id, task_id, f"Starting task: {task.description}")

            output_data = await self._execute_task_impl(workflow_id, task)

            await StateManager.update_task_status(
                workflow_id,
                task_id,
                status=TaskStatus.COMPLETED,
                output_data=output_data,
            )
            await self._publish_event(workflow_id, task_id, EventType.AGENT_COMPLETED)
            await self.log(workflow_id, task_id, "Task completed successfully.")

        except Exception as e:
            await self.log(workflow_id, task_id, f"Error executing task: {e}", level="error")
            await StateManager.update_task_status(
                workflow_id,
                task_id,
                status=TaskStatus.FAILED,
                output_data={"error": str(e)},
            )

    async def log(self, workflow_id: str, task_id: str, message: str, level: str = "info") -> None:
        """Logs a message by publishing a TASK_PROGRESS event."""
        print(f"[{self.name}][{level.upper()}]: {message}")
        await self._publish_event(
            workflow_id,
            task_id,
            EventType.TASK_PROGRESS,
            payload={"level": level, "message": message},
        )

    async def _publish_event(
        self, workflow_id: str, task_id: str, event_type: EventType, payload: Optional[Dict] = None
    ) -> None:
        """Helper to construct and publish an agent event."""
        event = AgentEvent(
            event_type=event_type,
            source_agent=self.name,
            workflow_id=workflow_id,
            task_id=task_id,
            payload=payload or {},
        )
        await EventBus.publish_event(event)
