from __future__ import annotations

"""EventBus provides a publish/subscribe interface for agent events.

Events are persisted to SurrealDB for durability and historical analysis.
This implementation does not yet include real-time subscription (`LIVE SELECT`)
but provides the core persistence methods.
"""

from typing import List, Optional

from .db import get_db
from .state_models import AgentEvent, EventType

_EVENT_TABLE = "agent_events"


class EventBus:
    """High-level API for publishing and retrieving agent events."""

    @staticmethod
    async def publish_event(event: AgentEvent) -> None:
        """Persist an event to the SurrealDB event table."""
        db = await get_db()
        record_id = f"{_EVENT_TABLE}:{event.id}"
        await db.create(record_id, data=event.model_dump(by_alias=True))

    @staticmethod
    async def get_event_history(
        workflow_id: str,
        event_type: Optional[EventType] = None,
    ) -> List[AgentEvent]:
        """Retrieve all historical events for a workflow, with optional filtering."""
        db = await get_db()
        
        query = f"SELECT * FROM {_EVENT_TABLE} WHERE workflow_id = $wf_id"
        params = {"wf_id": workflow_id}

        if event_type:
            query += " AND event_type = $e_type"
            params["e_type"] = event_type.value
            
        query += " ORDER BY created_at ASC;"

        res = await db.query(query, params)
        
        if not res or not res[0].get('result'):
            return []

        return [AgentEvent.model_validate(item) for item in res[0]['result']]
