import asyncio
from typing import Optional, Any

from ..agents.base_agent import BaseAgent
from ..orchestrator.shared_state import Task
from api.models.memory_models import MemoryNode, MemoryEdge, NodeType, EdgeType
from api.persistence.surrealdb_persistence import create_node, create_edge

class DataAgent(BaseAgent):
    def __init__(self, sandbox_tool: Optional[Any] = None):
        super().__init__(name="DataAgent", sandbox_tool=sandbox_tool)

    def execute_task(self, task: Task) -> dict:
        self.log(f"Executing data task: {task.task}")
        action = task.task.lower()
        input_data = task.input_data or {}

        try:
            if "create node" in action:
                node_type_str = input_data.get("node_type")
                content = input_data.get("content")
                if not node_type_str or not content:
                    raise ValueError("Missing 'node_type' or 'content' for create node task.")

                node = MemoryNode(node_type=NodeType[node_type_str.upper()], content=content, metadata=input_data.get("metadata", {}))
                created_node = asyncio.run(create_node(node))
                if not created_node:
                    raise Exception("Failed to create node in the database.")

                result = {
                    "status": "completed",
                    "message": f"Successfully created memory node {created_node.id}.",
                    "artifacts": [created_node.model_dump_json()]
                }

            elif "create edge" in action:
                source_id = input_data.get("source_id")
                target_id = input_data.get("target_id")
                edge_type_str = input_data.get("edge_type")
                if not source_id or not target_id or not edge_type_str:
                    raise ValueError("Missing 'source_id', 'target_id', or 'edge_type' for create edge task.")

                edge = MemoryEdge(
                    source_node_id=source_id,
                    target_node_id=target_id,
                    edge_type=EdgeType[edge_type_str.upper()],
                    metadata=input_data.get("metadata", {})
                )
                created_edge = asyncio.run(create_edge(source_id, target_id, edge))
                if not created_edge:
                    raise Exception("Failed to create edge in the database.")

                result = {
                    "status": "completed",
                    "message": f"Successfully created edge {created_edge.id} from {source_id} to {target_id}.",
                    "artifacts": [created_edge.model_dump_json()]
                }

            else:
                raise NotImplementedError(f"DataAgent does not support action: {action}")

        except Exception as e:
            self.log(f"Error executing data task: {e}")
            result = {"status": "failed", "message": str(e)}

        self.log(f"Finished task: {task.task} with status: {result['status']}")
        return result
