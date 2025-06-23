from __future__ import annotations

from typing import Any, Dict, Optional

from ..agents.base_agent import BaseAgent
from ..state.state_models import TaskState
from api.models.memory_models import EdgeType, MemoryEdge, MemoryNode, NodeType
from api.persistence.surrealdb_persistence import create_edge, create_node


class DataAgent(BaseAgent):
    """Specialized agent for interacting with the SurrealDB memory layer."""

    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="DataAgent", sandbox_tool=sandbox_tool)

    async def _execute_task_impl(self, workflow_id: str, task: TaskState) -> Dict[str, Any]:
        """Handles creation of memory nodes and edges."""
        action = task.description.lower()
        input_data = task.input_data

        if "create node" in action:
            node_type_str = input_data.get("node_type")
            content = input_data.get("content")
            if not node_type_str or not content:
                raise ValueError("Missing 'node_type' or 'content' for create node task.")

            node = MemoryNode(
                node_type=NodeType[node_type_str.upper()],
                content=content,
                metadata=input_data.get("metadata", {}),
            )
            created_node = await create_node(node)
            if not created_node:
                raise Exception("Failed to create node in the database.")

            return {
                "node_id": created_node.id,
                "message": f"Successfully created memory node {created_node.id}.",
            }

        elif "create edge" in action:
            source_id = input_data.get("source_id")
            target_id = input_data.get("target_id")
            edge_type_str = input_data.get("edge_type")
            if not source_id or not target_id or not edge_type_str:
                raise ValueError(
                    "Missing 'source_id', 'target_id', or 'edge_type' for create edge task."
                )

            edge = MemoryEdge(
                source_node_id=source_id,
                target_node_id=target_id,
                edge_type=EdgeType[edge_type_str.upper()],
                metadata=input_data.get("metadata", {}),
            )
            created_edge = await create_edge(source_id, target_id, edge)
            if not created_edge:
                raise Exception("Failed to create edge in the database.")

            return {
                "edge_id": created_edge.id,
                "message": f"Successfully created edge {created_edge.id} from {source_id} to {target_id}.",
            }

        else:
            raise NotImplementedError(f"DataAgent does not support action: {action}")
