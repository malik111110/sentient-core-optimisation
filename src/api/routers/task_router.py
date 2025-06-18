from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
import uuid

from ..models.core_models import TaskCreate, TaskRead, TaskUpdate
from ..persistence import in_memory_db as db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskCreate):
    """
    Create a new task.
    """
    return db.create_task(task_create=task)

@router.get("/", response_model=List[TaskRead])
async def list_all_tasks(agent_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of all tasks, optionally filtered by agent_id.
    """
    tasks = db.get_tasks(agent_id=agent_id, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def get_specific_task(task_id: uuid.UUID):
    """
    Retrieve a specific task by its ID.
    """
    task = db.get_task(task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(task_id: uuid.UUID, task_update: TaskUpdate):
    """
    Update an existing task.
    """
    updated_task = db.update_task(task_id=task_id, task_update=task_update)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=TaskRead)
async def delete_specific_task(task_id: uuid.UUID):
    """
    Delete a specific task by its ID.
    """
    deleted_task = db.delete_task(task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return deleted_task
