# Implementation Guide: Async/Stateful/Event-Driven Enhancements

## Overview

This guide provides step-by-step implementation instructions for transforming Sentient-Core into a fully async, stateful, and event-driven system. Follow these phases sequentially to ensure system stability throughout the transition.

## Prerequisites

### Required Dependencies

```toml
# Add to pyproject.toml or requirements.txt

# Async support
aiohttp = "^3.9.0"
aiofiles = "^23.2.0"
websockets = "^12.0"

# Task queue and background processing
celery = "^5.3.0"
redis = "^5.0.0"
aioredis = "^2.0.0"

# Event streaming
server-sent-events = "^0.8.0"

# Enhanced async database support
asyncpg = "^0.29.0"  # If using PostgreSQL
aiosqlite = "^0.19.0"  # If using SQLite

# Monitoring and observability
prometheus-client = "^0.19.0"
structlog = "^23.2.0"
```

### Environment Configuration

```bash
# .env additions
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
WEBSOCKET_URL=ws://localhost:8080/ws
EVENT_BUS_BACKEND=redis  # or 'memory' for development
STATE_PERSISTENCE_BACKEND=surrealdb  # or 'postgresql'
```

## Phase 1: Async Foundation (Week 1-2)

### Step 1.1: Create Async Base Agent

**File: `src/sentient_core/agents/async_base_agent.py`**

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, AsyncGenerator, List
from contextlib import asynccontextmanager
import asyncio
import logging
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum

from ..orchestrator.shared_state import Task

logger = logging.getLogger(__name__)

class TaskExecutionMode(str, Enum):
    BLOCKING = "blocking"
    STREAMING = "streaming"
    BACKGROUND = "background"

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class AsyncBaseAgent(ABC):
    """Enhanced async base class for all agents."""
    
    def __init__(self, name: str, sandbox_tool: Optional[Any] = None):
        self.name = name
        self.sandbox_tool = sandbox_tool
        self._execution_context: Optional[Dict[str, Any]] = None
        self._cancellation_token = asyncio.Event()
        self._pause_token = asyncio.Event()
        self._state_checkpoints: List[Dict[str, Any]] = []
        self._current_status = ExecutionStatus.PENDING
        logger.info(f"AsyncAgent {self.name} initialized")
    
    @abstractmethod
    async def execute_task(self, task: Task, mode: TaskExecutionMode = TaskExecutionMode.BLOCKING) -> Dict[str, Any]:
        """Execute task with specified mode."""
        pass
    
    @abstractmethod
    async def stream_execution(self, task: Task) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream task execution progress."""
        pass
    
    async def cancel_execution(self) -> None:
        """Cancel current task execution."""
        logger.info(f"Cancelling execution for agent {self.name}")
        self._cancellation_token.set()
        self._current_status = ExecutionStatus.CANCELLED
    
    async def pause_execution(self) -> None:
        """Pause current task execution."""
        logger.info(f"Pausing execution for agent {self.name}")
        self._pause_token.set()
        self._current_status = ExecutionStatus.PAUSED
    
    async def resume_execution(self) -> None:
        """Resume paused task execution."""
        logger.info(f"Resuming execution for agent {self.name}")
        self._pause_token.clear()
        self._current_status = ExecutionStatus.RUNNING
    
    async def create_checkpoint(self, checkpoint_data: Dict[str, Any]) -> str:
        """Create execution state checkpoint."""
        checkpoint_id = str(uuid4())
        checkpoint = {
            "id": checkpoint_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": checkpoint_data,
            "agent_name": self.name,
            "status": self._current_status.value
        }
        self._state_checkpoints.append(checkpoint)
        await self._persist_checkpoint(checkpoint)
        logger.debug(f"Created checkpoint {checkpoint_id} for agent {self.name}")
        return checkpoint_id
    
    async def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore agent state from checkpoint."""
        checkpoint = await self._load_checkpoint(checkpoint_id)
        if checkpoint:
            self._execution_context = checkpoint["data"]
            logger.info(f"Restored agent {self.name} from checkpoint {checkpoint_id}")
            return True
        logger.warning(f"Failed to restore agent {self.name} from checkpoint {checkpoint_id}")
        return False
    
    @asynccontextmanager
    async def execution_context(self, task: Task):
        """Manage execution context lifecycle."""
        try:
            self._execution_context = {
                "task_id": str(task.task_id),
                "start_time": datetime.utcnow().isoformat(),
                "status": ExecutionStatus.RUNNING.value
            }
            self._current_status = ExecutionStatus.RUNNING
            yield self._execution_context
        except asyncio.CancelledError:
            self._current_status = ExecutionStatus.CANCELLED
            raise
        except Exception as e:
            self._current_status = ExecutionStatus.FAILED
            logger.error(f"Execution failed for agent {self.name}: {e}")
            raise
        finally:
            if self._current_status == ExecutionStatus.RUNNING:
                self._current_status = ExecutionStatus.COMPLETED
            self._execution_context = None
            self._cancellation_token.clear()
            self._pause_token.clear()
    
    async def _check_cancellation(self):
        """Check if execution should be cancelled."""
        if self._cancellation_token.is_set():
            raise asyncio.CancelledError("Task execution cancelled")
    
    async def _check_pause(self):
        """Check if execution should be paused."""
        if self._pause_token.is_set():
            logger.info(f"Agent {self.name} paused, waiting for resume...")
            while self._pause_token.is_set():
                await asyncio.sleep(0.1)
            logger.info(f"Agent {self.name} resumed")
    
    async def _persist_checkpoint(self, checkpoint: Dict[str, Any]):
        """Persist checkpoint to storage (implement based on chosen backend)."""
        # TODO: Implement based on chosen persistence backend
        pass
    
    async def _load_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load checkpoint from storage (implement based on chosen backend)."""
        # TODO: Implement based on chosen persistence backend
        return None
    
    def log(self, message: str, level: str = "info"):
        """Enhanced logging with structured format."""
        log_data = {
            "agent": self.name,
            "status": self._current_status.value,
            "message": message
        }
        getattr(logger, level)(f"[{self.name}]: {message}", extra=log_data)
```

### Step 1.2: Convert Existing Agents

**File: `src/sentient_core/specialized_agents/async_frontend_developer_agent.py`**

```python
from typing import Dict, Any, AsyncGenerator
import asyncio
import json

from ..agents.async_base_agent import AsyncBaseAgent, TaskExecutionMode
from ..orchestrator.shared_state import Task
from ..tools.async_webcontainer_tool import AsyncWebContainerTool, WebContainerToolInput

class AsyncFrontendDeveloperAgent(AsyncBaseAgent):
    """Async frontend development agent."""
    
    def __init__(self, sandbox_tool: AsyncWebContainerTool = None):
        super().__init__(name="AsyncFrontendDeveloperAgent", sandbox_tool=sandbox_tool)
    
    async def execute_task(self, task: Task, mode: TaskExecutionMode = TaskExecutionMode.BLOCKING) -> Dict[str, Any]:
        """Execute frontend development task."""
        async with self.execution_context(task) as ctx:
            if mode == TaskExecutionMode.STREAMING:
                result = {"status": "streaming", "stream_id": str(task.task_id)}
                # Start streaming in background
                asyncio.create_task(self._stream_to_client(task))
                return result
            elif mode == TaskExecutionMode.BACKGROUND:
                asyncio.create_task(self._execute_background(task))
                return {"status": "started", "task_id": str(task.task_id)}
            else:
                return await self._execute_blocking(task)
    
    async def stream_execution(self, task: Task) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream frontend development progress."""
        async with self.execution_context(task):
            try:
                # Phase 1: Requirements Analysis
                yield {"phase": "analysis", "status": "analyzing_requirements", "progress": 10}
                await self._check_cancellation()
                await self._check_pause()
                await asyncio.sleep(0.5)  # Simulate analysis time
                
                # Create checkpoint
                await self.create_checkpoint({"phase": "analysis_complete", "requirements": task.task})
                
                # Phase 2: Component Generation
                yield {"phase": "generation", "status": "generating_components", "progress": 30}
                await self._check_cancellation()
                await self._check_pause()
                
                html_content = await self._generate_html_async(task)
                yield {"phase": "generation", "status": "html_generated", "progress": 50}
                
                await self.create_checkpoint({"phase": "generation_complete", "html_content": html_content})
                
                # Phase 3: Building UI
                yield {"phase": "build", "status": "building_ui", "progress": 70}
                await self._check_cancellation()
                await self._check_pause()
                
                if not self.sandbox_tool:
                    raise ValueError("WebContainer tool required for deployment")
                
                # Phase 4: Deployment
                yield {"phase": "deploy", "status": "deploying", "progress": 90}
                
                file_tree = {"index.html": html_content}
                tool_input = WebContainerToolInput(files=file_tree, commands=["serve"])
                
                deployment_result = await self.sandbox_tool.run_async(tool_input)
                
                await self.create_checkpoint({
                    "phase": "deployment_complete", 
                    "url": deployment_result.get("url")
                })
                
                # Phase 5: Completion
                yield {
                    "phase": "complete", 
                    "status": "completed", 
                    "progress": 100,
                    "result": {
                        "url": deployment_result.get("url"),
                        "artifacts": [deployment_result.get("url")]
                    }
                }
                
            except asyncio.CancelledError:
                yield {"phase": "cancelled", "status": "cancelled", "progress": -1}
                raise
            except Exception as e:
                yield {"phase": "error", "status": "failed", "progress": -1, "error": str(e)}
                raise
    
    async def _execute_blocking(self, task: Task) -> Dict[str, Any]:
        """Traditional blocking execution with checkpoints."""
        if not self.sandbox_tool:
            raise ValueError("WebContainer tool required")
        
        # Create checkpoint before major operations
        await self.create_checkpoint({"phase": "pre_generation", "task": task.dict()})
        
        # Generate HTML content
        html_content = await self._generate_html_async(task)
        await self._check_cancellation()
        
        await self.create_checkpoint({"phase": "post_generation", "html_generated": True})
        
        # Deploy to WebContainer
        file_tree = {"index.html": html_content}
        tool_input = WebContainerToolInput(files=file_tree, commands=["serve"])
        
        result = await self.sandbox_tool.run_async(tool_input)
        await self._check_cancellation()
        
        await self.create_checkpoint({"phase": "deployed", "url": result.get("url")})
        
        return {
            "status": "completed",
            "message": f"Frontend deployed at {result.get('url')}",
            "artifacts": [result.get("url")]
        }
    
    async def _execute_background(self, task: Task):
        """Execute task in background with progress updates."""
        try:
            async for progress in self.stream_execution(task):
                # In a real implementation, this would publish to event bus
                self.log(f"Background progress: {progress}")
        except Exception as e:
            self.log(f"Background execution failed: {e}", "error")
    
    async def _generate_html_async(self, task: Task) -> str:
        """Generate HTML content asynchronously."""
        await asyncio.sleep(0.1)  # Simulate async generation
        
        return f"""<!DOCTYPE html>
<html>
  <head>
    <title>Task: {task.task}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {{ font-family: Arial, sans-serif; margin: 40px; }}
      .container {{ max-width: 800px; margin: 0 auto; }}
      .status {{ padding: 10px; background: #f0f0f0; border-radius: 5px; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{task.task}</h1>
      <div id="backend-response" class="status">Connecting to backend...</div>
      <div id="status" class="status">Ready</div>
    </div>
    <script type="module" src="bridge.js"></script>
  </body>
</html>"""
```

### Step 1.3: Create Async Sandbox Tools

**File: `src/sentient_core/tools/async_webcontainer_tool.py`**

```python
import asyncio
import json
import websockets
from typing import Dict, Any, AsyncGenerator
from uuid import uuid4
import logging

from .webcontainer_tool import WebContainerToolInput

logger = logging.getLogger(__name__)

class AsyncWebContainerTool:
    """Async WebContainer integration with real-time communication."""
    
    def __init__(self, websocket_url: str = "ws://localhost:8080/ws"):
        self.websocket_url = websocket_url
        self._active_sessions: Dict[str, websockets.WebSocketServerProtocol] = {}
        self._connection_pool = []
        self._max_connections = 10
    
    async def run_async(self, inputs: WebContainerToolInput) -> Dict[str, Any]:
        """Execute WebContainer task asynchronously."""
        session_id = str(uuid4())
        
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                self._active_sessions[session_id] = websocket
                
                # Send task to WebContainer
                task_message = {
                    "type": "execute_task",
                    "session_id": session_id,
                    "files": inputs.files,
                    "commands": inputs.commands,
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                await websocket.send(json.dumps(task_message))
                logger.info(f"Sent task to WebContainer session {session_id}")
                
                # Wait for completion with timeout
                timeout = 300  # 5 minutes
                async with asyncio.timeout(timeout):
                    async for message in websocket:
                        data = json.loads(message)
                        
                        if data["type"] == "task_completed":
                            logger.info(f"WebContainer task {session_id} completed")
                            return data["result"]
                        elif data["type"] == "task_error":
                            logger.error(f"WebContainer task {session_id} failed: {data['error']}")
                            raise Exception(data["error"])
                        elif data["type"] == "task_progress":
                            logger.debug(f"WebContainer task {session_id} progress: {data['progress']}")
                            
        except asyncio.TimeoutError:
            logger.error(f"WebContainer task {session_id} timed out")
            raise Exception("WebContainer task execution timed out")
        except websockets.exceptions.ConnectionClosed:
            logger.error(f"WebContainer connection closed for session {session_id}")
            raise Exception("WebContainer connection lost")
        finally:
            if session_id in self._active_sessions:
                del self._active_sessions[session_id]
    
    async def stream_execution(self, inputs: WebContainerToolInput) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream WebContainer execution progress."""
        session_id = str(uuid4())
        
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                task_message = {
                    "type": "stream_task",
                    "session_id": session_id,
                    "files": inputs.files,
                    "commands": inputs.commands
                }
                
                await websocket.send(json.dumps(task_message))
                
                async for message in websocket:
                    data = json.loads(message)
                    yield data
                    
                    if data["type"] in ["task_completed", "task_error"]:
                        break
                        
        except websockets.exceptions.ConnectionClosed:
            yield {"type": "connection_error", "error": "WebSocket connection closed"}
    
    async def cancel_task(self, session_id: str) -> bool:
        """Cancel a running WebContainer task."""
        if session_id in self._active_sessions:
            websocket = self._active_sessions[session_id]
            try:
                await websocket.send(json.dumps({
                    "type": "cancel_task",
                    "session_id": session_id
                }))
                return True
            except Exception as e:
                logger.error(f"Failed to cancel WebContainer task {session_id}: {e}")
        return False
    
    async def health_check(self) -> bool:
        """Check WebContainer service health."""
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                await websocket.send(json.dumps({"type": "health_check"}))
                response = await websocket.recv()
                data = json.loads(response)
                return data.get("status") == "healthy"
        except Exception:
            return False
```

## Step 1.4: Migration Strategy

**File: `src/sentient_core/migration/async_migration.py`**

```python
"""Migration utilities for converting sync agents to async."""

import asyncio
import inspect
from typing import Any, Callable, Dict
from functools import wraps

class AsyncMigrationWrapper:
    """Wrapper to gradually migrate sync agents to async."""
    
    def __init__(self, sync_agent):
        self.sync_agent = sync_agent
        self.name = getattr(sync_agent, 'name', 'UnknownAgent')
    
    async def execute_task(self, task, mode=None) -> Dict[str, Any]:
        """Execute sync agent task in async context."""
        if hasattr(self.sync_agent, 'execute_task'):
            if inspect.iscoroutinefunction(self.sync_agent.execute_task):
                return await self.sync_agent.execute_task(task)
            else:
                # Run sync method in thread pool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self.sync_agent.execute_task, task)
        else:
            raise NotImplementedError("Agent must implement execute_task method")

def async_compatible(sync_func: Callable) -> Callable:
    """Decorator to make sync functions async-compatible."""
    @wraps(sync_func)
    async def async_wrapper(*args, **kwargs):
        if inspect.iscoroutinefunction(sync_func):
            return await sync_func(*args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, sync_func, *args, **kwargs)
    return async_wrapper

# Usage example:
# from ..specialized_agents.frontend_developer_agent import FrontendDeveloperAgent
# sync_agent = FrontendDeveloperAgent()
# async_agent = AsyncMigrationWrapper(sync_agent)
```

## Phase 2: State Management (Week 3-4)

### Step 2.1: Workflow State Models

**File: `src/api/models/workflow_models.py`**

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class WorkflowStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StateCheckpoint(BaseModel):
    """Individual state checkpoint."""
    checkpoint_id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    step_name: str
    agent_name: Optional[str] = None
    checkpoint_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_recoverable: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    """Persistent workflow state model."""
    workflow_id: UUID = Field(default_factory=uuid4)
    session_id: Optional[UUID] = None
    current_step: str
    step_history: List[str] = Field(default_factory=list)
    state_data: Dict[str, Any] = Field(default_factory=dict)
    agent_states: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    checkpoints: List[StateCheckpoint] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class WorkflowStateCreate(BaseModel):
    """Model for creating new workflow state."""
    session_id: Optional[UUID] = None
    initial_step: str = "initialized"
    initial_data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowStateUpdate(BaseModel):
    """Model for updating workflow state."""
    current_step: Optional[str] = None
    state_data: Optional[Dict[str, Any]] = None
    agent_states: Optional[Dict[str, Dict[str, Any]]] = None
    status: Optional[WorkflowStatus] = None
    metadata: Optional[Dict[str, Any]] = None
```

### Step 2.2: State Management Service

**File: `src/sentient_core/state/workflow_state_manager.py`**

```python
import asyncio
import json
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
import logging

from ..api.models.workflow_models import WorkflowState, StateCheckpoint, WorkflowStatus
from ..clients.surrealdb_client import get_surrealdb_client

logger = logging.getLogger(__name__)

class WorkflowStateManager:
    """Manages persistent workflow state with SurrealDB backend."""
    
    def __init__(self):
        self._state_cache: Dict[UUID, WorkflowState] = {}
        self._cache_ttl = 3600  # 1 hour
        self._cleanup_task = None
    
    async def initialize(self):
        """Initialize the state manager."""
        # Start cache cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_cache_periodically())
        logger.info("WorkflowStateManager initialized")
    
    async def shutdown(self):
        """Shutdown the state manager."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("WorkflowStateManager shutdown")
    
    async def create_workflow(self, initial_state: Dict[str, Any], session_id: Optional[UUID] = None) -> WorkflowState:
        """Create new workflow with initial state."""
        workflow = WorkflowState(
            session_id=session_id,
            current_step="initialized",
            state_data=initial_state,
            metadata={"created_by": "orchestrator"}
        )
        
        # Persist to database
        db = await get_surrealdb_client()
        try:
            if db:
                workflow_data = workflow.dict()
                await db.create("workflow_state", workflow_data)
                logger.info(f"Created workflow {workflow.workflow_id}")
        except Exception as e:
            logger.error(f"Failed to persist workflow {workflow.workflow_id}: {e}")
        finally:
            if db:
                await db.close()
        
        # Cache the workflow
        self._state_cache[workflow.workflow_id] = workflow
        return workflow
    
    async def get_workflow(self, workflow_id: UUID) -> Optional[WorkflowState]:
        """Get workflow by ID, from cache or database."""
        # Check cache first
        if workflow_id in self._state_cache:
            return self._state_cache[workflow_id]
        
        # Load from database
        db = await get_surrealdb_client()
        try:
            if db:
                workflow_data = await db.select(f"workflow_state:{workflow_id}")
                if workflow_data:
                    workflow = WorkflowState(**workflow_data)
                    self._state_cache[workflow_id] = workflow
                    return workflow
        except Exception as e:
            logger.error(f"Failed to load workflow {workflow_id}: {e}")
        finally:
            if db:
                await db.close()
        
        return None
    
    async def update_workflow_step(self, workflow_id: UUID, new_step: str, state_updates: Dict[str, Any] = None) -> bool:
        """Update workflow to new step with optional state changes."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return False
        
        # Create checkpoint before step change
        checkpoint = StateCheckpoint(
            workflow_id=workflow_id,
            step_name=workflow.current_step,
            checkpoint_data=workflow.state_data.copy(),
            metadata={"previous_step": workflow.current_step}
        )
        
        # Update workflow
        workflow.step_history.append(workflow.current_step)
        workflow.current_step = new_step
        workflow.updated_at = datetime.utcnow()
        
        if state_updates:
            workflow.state_data.update(state_updates)
        
        workflow.checkpoints.append(checkpoint)
        
        # Persist changes
        success = await self._persist_workflow(workflow)
        if success:
            self._state_cache[workflow_id] = workflow
            logger.info(f"Updated workflow {workflow_id} to step '{new_step}'")
        
        return success
    
    async def create_agent_checkpoint(self, workflow_id: UUID, agent_name: str, agent_state: Dict[str, Any]) -> Optional[str]:
        """Create checkpoint for specific agent state."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
        
        checkpoint = StateCheckpoint(
            workflow_id=workflow_id,
            step_name=f"agent_{agent_name}_checkpoint",
            agent_name=agent_name,
            checkpoint_data=agent_state,
            metadata={"agent": agent_name}
        )
        
        # Persist checkpoint
        db = await get_surrealdb_client()
        try:
            if db:
                checkpoint_data = checkpoint.dict()
                await db.create("state_checkpoint", checkpoint_data)
                
                # Update workflow's agent state
                workflow.agent_states[agent_name] = agent_state
                await self._persist_workflow(workflow)
                
                logger.info(f"Created agent checkpoint for {agent_name} in workflow {workflow_id}")
                return str(checkpoint.checkpoint_id)
        except Exception as e:
            logger.error(f"Failed to create agent checkpoint: {e}")
        finally:
            if db:
                await db.close()
        
        return None
    
    async def recover_workflow(self, workflow_id: UUID, target_step: Optional[str] = None) -> bool:
        """Recover workflow from failure or interruption."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False
        
        if target_step:
            # Find checkpoint for target step
            target_checkpoint = None
            for checkpoint in reversed(workflow.checkpoints):
                if checkpoint.step_name == target_step and checkpoint.is_recoverable:
                    target_checkpoint = checkpoint
                    break
            
            if target_checkpoint:
                workflow.current_step = target_step
                workflow.state_data = target_checkpoint.checkpoint_data.copy()
                workflow.status = WorkflowStatus.ACTIVE
                workflow.updated_at = datetime.utcnow()
                
                success = await self._persist_workflow(workflow)
                if success:
                    self._state_cache[workflow_id] = workflow
                    logger.info(f"Recovered workflow {workflow_id} to step '{target_step}'")
                    return True
        
        return False
    
    async def list_workflows(self, session_id: Optional[UUID] = None, status: Optional[WorkflowStatus] = None) -> List[WorkflowState]:
        """List workflows with optional filtering."""
        db = await get_surrealdb_client()
        workflows = []
        
        try:
            if db:
                query = "SELECT * FROM workflow_state"
                conditions = []
                
                if session_id:
                    conditions.append(f"session_id = '{session_id}'")
                if status:
                    conditions.append(f"status = '{status.value}'")
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                results = await db.query(query)
                if results and len(results) > 0:
                    for workflow_data in results[0]['result']:
                        workflows.append(WorkflowState(**workflow_data))
        except Exception as e:
            logger.error(f"Failed to list workflows: {e}")
        finally:
            if db:
                await db.close()
        
        return workflows
    
    async def _persist_workflow(self, workflow: WorkflowState) -> bool:
        """Persist workflow to database."""
        db = await get_surrealdb_client()
        try:
            if db:
                workflow_data = workflow.dict()
                await db.update(f"workflow_state:{workflow.workflow_id}", workflow_data)
                return True
        except Exception as e:
            logger.error(f"Failed to persist workflow {workflow.workflow_id}: {e}")
        finally:
            if db:
                await db.close()
        return False
    
    async def _cleanup_cache_periodically(self):
        """Periodically clean up old cache entries."""
        while True:
            try:
                await asyncio.sleep(300)  # Clean every 5 minutes
                current_time = datetime.utcnow()
                
                expired_workflows = []
                for workflow_id, workflow in self._state_cache.items():
                    age = (current_time - workflow.updated_at).total_seconds()
                    if age > self._cache_ttl:
                        expired_workflows.append(workflow_id)
                
                for workflow_id in expired_workflows:
                    del self._state_cache[workflow_id]
                
                if expired_workflows:
                    logger.debug(f"Cleaned {len(expired_workflows)} expired workflows from cache")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")
```

This implementation guide provides the concrete steps and code needed to implement the async/stateful/event-driven enhancements. Continue with the remaining phases following this pattern, ensuring each component is thoroughly tested before moving to the next phase.