# SurrealDB Persistence Layer for Memory and Knowledge Graphs

from typing import List, Optional, Dict, Any
from ..models.memory_models import MemoryNode, MemoryEdge, SurrealID
from src.clients.surrealdb_client import get_surrealdb_client

# --- MemoryNode Persistence ---

async def create_node(node: MemoryNode) -> Optional[MemoryNode]:
    """Creates a new memory node in SurrealDB."""
    db = await get_surrealdb_client()
    if not db:
        return None
    try:
        node_data = node.model_dump(exclude_none=True, exclude={'id'})
        # SurrealDB's Python driver can take the dict directly
        created_records = await db.create("memory_node", node_data)
        if created_records:
            # The driver returns a list of created records
            created_data = created_records[0]
            return MemoryNode(**created_data)
        return None
    except Exception as e:
        print(f"Error creating memory node: {e}")
        return None
    finally:
        await db.close()

async def get_node(node_id: SurrealID) -> Optional[MemoryNode]:
    """Retrieves a memory node by its SurrealDB ID."""
    db = await get_surrealdb_client()
    if not db:
        return None
    try:
        node_data = await db.select(node_id)
        return MemoryNode(**node_data) if node_data else None
    except Exception as e:
        print(f"Error retrieving node {node_id}: {e}")
        return None
    finally:
        await db.close()

# --- MemoryEdge Persistence ---

async def create_edge(source_node_id: SurrealID, target_node_id: SurrealID, edge_data: MemoryEdge) -> Optional[MemoryEdge]:
    """Creates a directed edge between two memory nodes."""
    db = await get_surrealdb_client()
    if not db:
        return None
    try:
        # The RELATE query is the standard way to create edges in SurrealDB
        # Example: RELATE person:1->likes->person:2 CONTENT { created_at: time::now() };
        edge_content = edge_data.model_dump(exclude={'id', 'source_node_id', 'target_node_id'}, exclude_none=True)
        query = f"RELATE {source_node_id}->{edge_data.edge_type.value}->{target_node_id} CONTENT {edge_content};"
        result = await db.query(query)
        # The result of a RELATE query is often a list containing the created edge
        if result and result[0] and result[0]['result']:
            created_edge = result[0]['result'][0]
            return MemoryEdge(**created_edge)
        return None
    except Exception as e:
        print(f"Error creating edge: {e}")
        return None
    finally:
        await db.close()

# --- KnowledgeGraph Retrieval ---

async def get_graph_from_node(start_node_id: SurrealID, depth: int = 1) -> Optional[Dict[str, Any]]:
    """Retrieves a subgraph starting from a given node up to a certain depth."""
    db = await get_surrealdb_client()
    if not db:
        return None
    try:
        # Using a graph query to fetch nodes and edges
        # Example: SELECT * FROM memory_node WHERE id = <start_node_id> FETCH edge, edge.in, edge.out
        query = f"SELECT * FROM {start_node_id} FETCH * LIMIT 100;"
        # A more complex query for depth > 1 would be needed
        # For now, this is a simplified version
        result = await db.query(query)
        if result and result[0] and result[0]['result']:
            return result[0]['result'][0]
        return None
    except Exception as e:
        print(f"Error retrieving graph from node {start_node_id}: {e}")
        return None
    finally:
        await db.close()
