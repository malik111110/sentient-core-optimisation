from __future__ import annotations

"""CRUD helper around SurrealDB for persisting `WorkflowState`.

All public methods are async and safe to call from any coroutine.  This module
*never* caches workflow documents – authoritative state lives in SurrealDB so
multiple processes / micro-services can share the same view.
"""

from typing import Optional

from .db import get_db
from .state_models import TaskStatus, WorkflowState

_WORKFLOW_TABLE = "workflow_state"


class StateManager:
    """High-level API for manipulating workflow documents."""

    # ---------------------------------------------------------------------
    # Creation helpers
    # ---------------------------------------------------------------------
    @staticmethod
    async def create_workflow(state: WorkflowState) -> WorkflowState:
        db = await get_db()
        # SurrealDB will use the provided `workflow_id` as the record ID.
        record_id = f"{_WORKFLOW_TABLE}:{state.id}"
        await db.create(record_id, data=state.model_dump(by_alias=True))
        return state

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------
    @staticmethod
    async def get_workflow(workflow_id: str) -> Optional[WorkflowState]:
        db = await get_db()
        record_id = f"{_WORKFLOW_TABLE}:{workflow_id}"
        res = await db.select(record_id)
        if not res:
            return None
        return WorkflowState.model_validate(res[0])

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------
    @staticmethod
    async def update_task_status(
        workflow_id: str,
        task_id: str,
        *,
        status: TaskStatus,
        output_data: Optional[dict] = None,
    ) -> None:
        """Set `status` (and optionally `output_data`) of a task inside workflow."""
        db = await get_db()
        # Use SurrealDB array modification syntax to update nested task.
        query = (
            "UPDATE $wf SET tasks[$idx].status = $status RETURN AFTER;"
            + (" UPDATE $wf SET tasks[$idx].output_data = $out RETURN AFTER;" if output_data else "")
        )
        await db.query(
            query,
            {
                "wf": f"{_WORKFLOW_TABLE}:{workflow_id}",
                "idx": f"WHERE task_id = '{task_id}'",  # pseudo; will be interpolated by SurrealDB
                "status": status.value,
                "out": output_data or {},
            },
        )

    @staticmethod
    async def set_workflow_status(workflow_id: str, status: str) -> None:
        db = await get_db()
        await db.update(f"{_WORKFLOW_TABLE}:{workflow_id}", {"status": status})
