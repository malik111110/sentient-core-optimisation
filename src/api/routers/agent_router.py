from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
import uuid

from ..models.core_models import AgentCreate, AgentRead, AgentUpdate
from ..persistence import supabase_persistence as db # Using an alias for brevity

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
async def create_new_agent(agent: AgentCreate):
    """
    Create a new agent.
    """
    return db.create_agent(agent_create=agent)

@router.get("/", response_model=List[AgentRead])
async def list_all_agents(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of all agents.
    """
    agents = db.get_agents(skip=skip, limit=limit)
    return agents

@router.get("/{agent_id}", response_model=AgentRead)
async def get_specific_agent(agent_id: uuid.UUID):
    """
    Retrieve a specific agent by its ID.
    """
    agent = db.get_agent(agent_id=agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentRead)
async def update_existing_agent(agent_id: uuid.UUID, agent_update: AgentUpdate):
    """
    Update an existing agent.
    """
    updated_agent = db.update_agent(agent_id=agent_id, agent_update=agent_update)
    if not updated_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return updated_agent

@router.delete("/{agent_id}", response_model=AgentRead) # Or just status_code=204 if no body
async def delete_specific_agent(agent_id: uuid.UUID):
    """
    Delete a specific agent by its ID.
    """
    deleted_agent = db.delete_agent(agent_id=agent_id)
    if not deleted_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return deleted_agent # Or return a confirmation message/status
