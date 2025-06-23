# Async/Stateful/Event-Driven Architecture Specification

## Overview

This document provides detailed technical specifications for implementing async/await patterns, stateful workflows, and event-driven architecture in Sentient-Core. It includes concrete code patterns, database schemas, and integration strategies.

## 1. Async Agent Architecture

### 1.1 Enhanced BaseAgent Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, AsyncGenerator
from contextlib import asynccontextmanager
import asyncio
from enum import Enum

class TaskExecutionMode(str, Enum):
    BLOCKING = "blocking"
    STREAMING = "streaming"
    BACKGROUND = "background"

class AsyncBaseAgent(ABC):
    """Enhanced async base class for all agents."""
    
    def __init__(self, name: str, sandbox_tool: Optional[Any] = None):
        self.name = name
        self.sandbox_tool = sandbox_tool
        self._execution_context: Optional[Dict[str, Any]] = None
        self._cancellation_token = asyncio.Event()
        self._state_checkpoints: List[Dict[str, Any]] = []
    
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
        self._cancellation_token.set()
    
    async def create_checkpoint(self, checkpoint_data: Dict[str, Any]) -> str:
        """Create execution state checkpoint."""
        checkpoint_id = str(uuid4())
        checkpoint = {
            "id": checkpoint_id,
            "timestamp": datetime.utcnow(),
            "data": checkpoint_data,
            "agent_name": self.name
        }
        self._state_checkpoints.append(checkpoint)
        await self._persist_checkpoint(checkpoint)
        return checkpoint_id
    
    async def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore agent state from checkpoint."""
        checkpoint = await self._load_checkpoint(checkpoint_id)
        if checkpoint:
            self._execution_context = checkpoint["data"]
            return True
        return False
    
    @asynccontextmanager
    async def execution_context(self, task: Task):
        """Manage execution context lifecycle."""
        try:
            self._execution_context = {
                "task_id": task.task_id,
                "start_time": datetime.utcnow(),
                "status": "running"
            }
            yield self._execution_context
        finally:
            self._execution_context = None
            self._cancellation_token.clear()
```

### 1.2 Async Specialized Agents

```python
class AsyncFrontendDeveloperAgent(AsyncBaseAgent):
    """Async frontend development agent."""
    
    async def execute_task(self, task: Task, mode: TaskExecutionMode = TaskExecutionMode.BLOCKING) -> Dict[str, Any]:
        async with self.execution_context(task) as ctx:
            if mode == TaskExecutionMode.STREAMING:
                return await self._execute_streaming(task)
            elif mode == TaskExecutionMode.BACKGROUND:
                asyncio.create_task(self._execute_background(task))
                return {"status": "started", "task_id": str(task.task_id)}
            else:
                return await self._execute_blocking(task)
    
    async def stream_execution(self, task: Task) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream frontend development progress."""
        async with self.execution_context(task):
            yield {"status": "analyzing_requirements", "progress": 10}
            await asyncio.sleep(0.1)  # Simulate work
            
            yield {"status": "generating_components", "progress": 30}
            await asyncio.sleep(0.2)
            
            yield {"status": "building_ui", "progress": 60}
            await asyncio.sleep(0.3)
            
            # Check for cancellation
            if self._cancellation_token.is_set():
                yield {"status": "cancelled", "progress": 60}
                return
            
            yield {"status": "deploying", "progress": 90}
            await asyncio.sleep(0.1)
            
            yield {"status": "completed", "progress": 100, "result": "Frontend deployed"}
    
    async def _execute_blocking(self, task: Task) -> Dict[str, Any]:
        """Traditional blocking execution."""
        if not self.sandbox_tool:
            raise ValueError("Sandbox tool required")
        
        # Create checkpoint before major operations
        await self.create_checkpoint({"phase": "pre_generation", "task": task.dict()})
        
        # Generate HTML content
        html_content = await self._generate_html_async(task)
        
        await self.create_checkpoint({"phase": "post_generation", "html_generated": True})
        
        # Deploy to WebContainer
        result = await self.sandbox_tool.run_async({
            "files": {"index.html": html_content},
            "commands": ["serve"]
        })
        
        await self.create_checkpoint({"phase": "deployed", "url": result.get("url")})
        
        return {
            "status": "completed",
            "message": f"Frontend deployed at {result.get('url')}",
            "artifacts": [result.get("url")]
        }
```

## 2. Stateful Workflow Management

### 2.1 Workflow State Schema

```python
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

class StateCheckpoint(BaseModel):
    """Individual state checkpoint."""
    checkpoint_id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    step_name: str
    agent_name: Optional[str] = None
    checkpoint_data: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_recoverable: bool = True

class WorkflowStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

### 2.2 State Management Service

```python
class WorkflowStateManager:
    """Manages persistent workflow state."""
    
    def __init__(self, db_client):
        self.db = db_client
        self._state_cache: Dict[UUID, WorkflowState] = {}
    
    async def create_workflow(self, initial_state: Dict[str, Any]) -> WorkflowState:
        """Create new workflow with initial state."""
        workflow = WorkflowState(
            current_step="initialized",
            state_data=initial_state
        )
        
        await self.db.create("workflow_state", workflow.dict())
        self._state_cache[workflow.workflow_id] = workflow
        return workflow
    
    async def update_workflow_step(self, workflow_id: UUID, new_step: str, state_updates: Dict[str, Any] = None) -> bool:
        """Update workflow to new step with optional state changes."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False
        
        # Create checkpoint before step change
        checkpoint = StateCheckpoint(
            workflow_id=workflow_id,
            step_name=workflow.current_step,
            checkpoint_data=workflow.state_data.copy()
        )
        
        # Update workflow
        workflow.step_history.append(workflow.current_step)
        workflow.current_step = new_step
        workflow.updated_at = datetime.utcnow()
        
        if state_updates:
            workflow.state_data.update(state_updates)
        
        workflow.checkpoints.append(checkpoint)
        
        # Persist changes
        await self.db.update(f"workflow_state:{workflow_id}", workflow.dict())
        self._state_cache[workflow_id] = workflow
        
        return True
    
    async def create_agent_checkpoint(self, workflow_id: UUID, agent_name: str, agent_state: Dict[str, Any]) -> str:
        """Create checkpoint for specific agent state."""
        checkpoint = StateCheckpoint(
            workflow_id=workflow_id,
            step_name=f"agent_{agent_name}_checkpoint",
            agent_name=agent_name,
            checkpoint_data=agent_state
        )
        
        await self.db.create("state_checkpoint", checkpoint.dict())
        return str(checkpoint.checkpoint_id)
    
    async def recover_workflow(self, workflow_id: UUID, target_step: Optional[str] = None) -> bool:
        """Recover workflow from failure or interruption."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False
        
        if target_step:
            # Find checkpoint for target step
            target_checkpoint = None
            for checkpoint in reversed(workflow.checkpoints):
                if checkpoint.step_name == target_step:
                    target_checkpoint = checkpoint
                    break
            
            if target_checkpoint:
                workflow.current_step = target_step
                workflow.state_data = target_checkpoint.checkpoint_data.copy()
                workflow.status = WorkflowStatus.ACTIVE
                await self.db.update(f"workflow_state:{workflow_id}", workflow.dict())
                return True
        
        return False
```

## 3. Event-Driven Architecture

### 3.1 Event System Core

```python
class Event(BaseModel):
    """Base event model."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    source: str
    target: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[UUID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EventBus:
    """Async event bus for agent communication."""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[Event] = []
    
    async def publish(self, event: Event) -> None:
        """Publish event to all subscribers."""
        self._event_history.append(event)
        
        # Persist event
        if self.redis:
            await self.redis.lpush(f"events:{event.event_type}", event.json())
        
        # Notify subscribers
        pattern_matches = self._find_matching_patterns(event.event_type)
        for pattern in pattern_matches:
            for handler in self._subscribers[pattern]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")
    
    async def subscribe(self, pattern: str, handler: Callable) -> str:
        """Subscribe to events matching pattern."""
        subscription_id = str(uuid4())
        self._subscribers[pattern].append(handler)
        return subscription_id
    
    async def publish_agent_event(self, agent_name: str, event_type: str, payload: Dict[str, Any]) -> None:
        """Convenience method for agent events."""
        event = Event(
            event_type=f"agent.{event_type}",
            source=agent_name,
            payload=payload
        )
        await self.publish(event)
    
    async def publish_workflow_event(self, workflow_id: UUID, event_type: str, payload: Dict[str, Any]) -> None:
        """Convenience method for workflow events."""
        event = Event(
            event_type=f"workflow.{event_type}",
            source="orchestrator",
            payload={"workflow_id": str(workflow_id), **payload}
        )
        await self.publish(event)
```

### 3.2 Agent Event Integration

```python
class EventAwareAgent(AsyncBaseAgent):
    """Base agent with event publishing capabilities."""
    
    def __init__(self, name: str, event_bus: EventBus, sandbox_tool: Optional[Any] = None):
        super().__init__(name, sandbox_tool)
        self.event_bus = event_bus
        self._setup_event_handlers()
    
    async def _setup_event_handlers(self):
        """Setup event subscriptions for this agent."""
        await self.event_bus.subscribe(f"agent.{self.name}.*", self._handle_agent_event)
        await self.event_bus.subscribe("workflow.*", self._handle_workflow_event)
    
    async def _handle_agent_event(self, event: Event):
        """Handle events directed at this agent."""
        if event.event_type.endswith(".cancel"):
            await self.cancel_execution()
        elif event.event_type.endswith(".pause"):
            await self._pause_execution()
        elif event.event_type.endswith(".resume"):
            await self._resume_execution()
    
    async def _handle_workflow_event(self, event: Event):
        """Handle workflow-level events."""
        if event.event_type == "workflow.step_completed":
            # React to workflow step completion
            pass
    
    async def execute_task(self, task: Task, mode: TaskExecutionMode = TaskExecutionMode.BLOCKING) -> Dict[str, Any]:
        """Execute task with event publishing."""
        # Publish task start event
        await self.event_bus.publish_agent_event(
            self.name, 
            "task.started", 
            {"task_id": str(task.task_id), "task_type": task.task}
        )
        
        try:
            result = await super().execute_task(task, mode)
            
            # Publish success event
            await self.event_bus.publish_agent_event(
                self.name,
                "task.completed",
                {"task_id": str(task.task_id), "result": result}
            )
            
            return result
            
        except Exception as e:
            # Publish error event
            await self.event_bus.publish_agent_event(
                self.name,
                "task.failed",
                {"task_id": str(task.task_id), "error": str(e)}
            )
            raise
```

## 4. Enhanced Sandbox Tools

### 4.1 Async WebContainer Tool

```python
class AsyncWebContainerTool:
    """Async WebContainer integration with real-time communication."""
    
    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self._active_sessions: Dict[str, websockets.WebSocketServerProtocol] = {}
    
    async def run_async(self, inputs: WebContainerToolInput) -> Dict[str, Any]:
        """Execute WebContainer task asynchronously."""
        session_id = str(uuid4())
        
        async with websockets.connect(self.websocket_url) as websocket:
            self._active_sessions[session_id] = websocket
            
            # Send task to WebContainer
            task_message = {
                "type": "execute_task",
                "session_id": session_id,
                "files": inputs.files,
                "commands": inputs.commands
            }
            
            await websocket.send(json.dumps(task_message))
            
            # Wait for completion
            async for message in websocket:
                data = json.loads(message)
                
                if data["type"] == "task_completed":
                    del self._active_sessions[session_id]
                    return data["result"]
                elif data["type"] == "task_error":
                    del self._active_sessions[session_id]
                    raise Exception(data["error"])
    
    async def stream_execution(self, inputs: WebContainerToolInput) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream WebContainer execution progress."""
        session_id = str(uuid4())
        
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
```

## 5. Integration Patterns

### 5.1 Async Orchestrator Enhancement

```python
class AsyncMainOrchestrator:
    """Enhanced orchestrator with full async/event support."""
    
    def __init__(self, command: str, event_bus: EventBus, state_manager: WorkflowStateManager):
        self.command = command
        self.event_bus = event_bus
        self.state_manager = state_manager
        self.planner = CSuitePlanner()
        self.executor = AsyncDepartmentalExecutor(event_bus, state_manager)
    
    async def run(self) -> WorkflowState:
        """Run orchestration with full async/state/event support."""
        # Create workflow state
        workflow = await self.state_manager.create_workflow({
            "command": self.command,
            "status": "planning"
        })
        
        try:
            # Publish workflow start event
            await self.event_bus.publish_workflow_event(
                workflow.workflow_id,
                "started",
                {"command": self.command}
            )
            
            # Planning phase
            await self.state_manager.update_workflow_step(
                workflow.workflow_id,
                "planning",
                {"status": "creating_plan"}
            )
            
            plan_dict = await self.planner.create_plan_async(self.command)
            tasks = [Task(**task_data) for task_data in plan_dict['tasks']]
            
            await self.state_manager.update_workflow_step(
                workflow.workflow_id,
                "executing",
                {
                    "plan": plan_dict,
                    "tasks": [task.dict() for task in tasks],
                    "status": "executing_tasks"
                }
            )
            
            # Execute tasks with streaming progress
            async for progress in self.executor.execute_plan_stream(tasks, workflow.workflow_id):
                await self.event_bus.publish_workflow_event(
                    workflow.workflow_id,
                    "progress",
                    progress
                )
            
            # Complete workflow
            await self.state_manager.update_workflow_step(
                workflow.workflow_id,
                "completed",
                {"status": "completed", "final_result": "Success"}
            )
            
            await self.event_bus.publish_workflow_event(
                workflow.workflow_id,
                "completed",
                {"result": "Success"}
            )
            
            return await self.state_manager.get_workflow(workflow.workflow_id)
            
        except Exception as e:
            await self.state_manager.update_workflow_step(
                workflow.workflow_id,
                "failed",
                {"status": "failed", "error": str(e)}
            )
            
            await self.event_bus.publish_workflow_event(
                workflow.workflow_id,
                "failed",
                {"error": str(e)}
            )
            
            raise
```

This specification provides the concrete implementation patterns needed to transform Sentient-Core into a fully async, stateful, and event-driven system. Each component is designed to work together while maintaining modularity and testability.