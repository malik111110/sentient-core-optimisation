# SurrealDB-Focused Agentic Implementation Guide

## Overview

This guide provides a comprehensive implementation strategy for transforming Sentient-Core into a fully async, stateful, and event-driven agentic system using SurrealDB as the primary database. SurrealDB's native support for async operations, live queries, and real-time data streaming makes it ideal for agentic workflows.

## SurrealDB Advantages for Agentic Systems

### Native Async Support
- **AsyncSurrealDB** class with full async/await support <mcreference link="https://surrealdb.com/docs/sdk/python/methods" index="3">3</mcreference>
- WebSocket and HTTP binary communication protocols
- Non-blocking database operations for agent execution

### Real-Time Event Streaming
- **LIVE SELECT** statements for real-time data monitoring <mcreference link="https://surrealdb.com/docs/surrealql/statements/live" index="3">3</mcreference>
- **Live Queries** with automatic change notifications <mcreference link="https://surrealdb.com/docs/sdk/python/concepts/streaming" index="2">2</mcreference>
- Built-in pub/sub mechanism through live query subscriptions

### Advanced State Management
- Graph-based data model perfect for agent relationships
- ACID transactions for consistent state updates
- JSON Patch support for incremental state changes
- Built-in versioning and audit trails

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Async Agents  │    │  Event Bus      │    │  State Manager  │
│                 │    │  (Live Queries) │    │  (SurrealDB)    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • AsyncBaseAgent│◄──►│ • LIVE SELECT   │◄──►│ • WorkflowState │
│ • Streaming     │    │ • Subscriptions │    │ • AgentState    │
│ • Cancellation  │    │ • Real-time     │    │ • Checkpoints   │
│ • Checkpointing │    │   Notifications │    │ • Recovery      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Phase 1: SurrealDB Foundation Setup

### 1.1 Enhanced SurrealDB Client Configuration

**File: `src/sentient_core/database/surrealdb_config.py`**

```python
from typing import Optional, Dict, Any, List
import asyncio
from contextlib import asynccontextmanager
from surrealdb import AsyncSurrealDB
from surrealdb.ws import Surreal
import logging
from datetime import datetime
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

class SurrealDBConfig:
    """Enhanced SurrealDB configuration for agentic systems."""
    
    def __init__(
        self,
        url: str = "ws://localhost:8000/rpc",
        namespace: str = "sentient",
        database: str = "core",
        username: Optional[str] = None,
        password: Optional[str] = None,
        connection_pool_size: int = 10,
        enable_live_queries: bool = True
    ):
        self.url = url
        self.namespace = namespace
        self.database = database
        self.username = username
        self.password = password
        self.connection_pool_size = connection_pool_size
        self.enable_live_queries = enable_live_queries
        self._connection_pool: List[AsyncSurrealDB] = []
        self._live_query_subscriptions: Dict[str, asyncio.Queue] = {}
        
    async def initialize_connection_pool(self) -> None:
        """Initialize connection pool for high-performance operations."""
        for i in range(self.connection_pool_size):
            db = AsyncSurrealDB(self.url)
            await db.connect()
            await db.use(self.namespace, self.database)
            
            if self.username and self.password:
                await db.signin({"user": self.username, "pass": self.password})
                
            self._connection_pool.append(db)
            logger.info(f"SurrealDB connection {i+1}/{self.connection_pool_size} initialized")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get a connection from the pool."""
        if not self._connection_pool:
            await self.initialize_connection_pool()
            
        connection = self._connection_pool.pop()
        try:
            yield connection
        finally:
            self._connection_pool.append(connection)
    
    async def setup_schema(self) -> None:
        """Setup database schema for agentic workflows."""
        async with self.get_connection() as db:
            # Agent state tables
            await db.query("""
                DEFINE TABLE agent_state SCHEMAFULL;
                DEFINE FIELD agent_id ON agent_state TYPE string;
                DEFINE FIELD name ON agent_state TYPE string;
                DEFINE FIELD status ON agent_state TYPE string;
                DEFINE FIELD capabilities ON agent_state TYPE array;
                DEFINE FIELD current_task ON agent_state TYPE option<string>;
                DEFINE FIELD execution_context ON agent_state TYPE object;
                DEFINE FIELD checkpoints ON agent_state TYPE array;
                DEFINE FIELD created_at ON agent_state TYPE datetime;
                DEFINE FIELD updated_at ON agent_state TYPE datetime;
                DEFINE INDEX agent_id_idx ON agent_state COLUMNS agent_id UNIQUE;
            """)
            
            # Workflow state tables
            await db.query("""
                DEFINE TABLE workflow_state SCHEMAFULL;
                DEFINE FIELD workflow_id ON workflow_state TYPE string;
                DEFINE FIELD status ON workflow_state TYPE string;
                DEFINE FIELD current_step ON workflow_state TYPE number;
                DEFINE FIELD total_steps ON workflow_state TYPE number;
                DEFINE FIELD agent_states ON workflow_state TYPE object;
                DEFINE FIELD execution_history ON workflow_state TYPE array;
                DEFINE FIELD metadata ON workflow_state TYPE object;
                DEFINE FIELD created_at ON workflow_state TYPE datetime;
                DEFINE FIELD updated_at ON workflow_state TYPE datetime;
                DEFINE INDEX workflow_id_idx ON workflow_state COLUMNS workflow_id UNIQUE;
            """)
            
            # Event tables for audit and replay
            await db.query("""
                DEFINE TABLE agent_event SCHEMAFULL;
                DEFINE FIELD event_id ON agent_event TYPE string;
                DEFINE FIELD event_type ON agent_event TYPE string;
                DEFINE FIELD source_agent ON agent_event TYPE string;
                DEFINE FIELD target_agent ON agent_event TYPE option<string>;
                DEFINE FIELD workflow_id ON agent_event TYPE option<string>;
                DEFINE FIELD payload ON agent_event TYPE object;
                DEFINE FIELD timestamp ON agent_event TYPE datetime;
                DEFINE FIELD correlation_id ON agent_event TYPE option<string>;
                DEFINE INDEX event_timestamp_idx ON agent_event COLUMNS timestamp;
                DEFINE INDEX event_workflow_idx ON agent_event COLUMNS workflow_id;
            """)
            
            # Task execution tables
            await db.query("""
                DEFINE TABLE task_execution SCHEMAFULL;
                DEFINE FIELD task_id ON task_execution TYPE string;
                DEFINE FIELD agent_id ON task_execution TYPE string;
                DEFINE FIELD workflow_id ON task_execution TYPE option<string>;
                DEFINE FIELD status ON task_execution TYPE string;
                DEFINE FIELD input_data ON task_execution TYPE object;
                DEFINE FIELD output_data ON task_execution TYPE option<object>;
                DEFINE FIELD progress ON task_execution TYPE number;
                DEFINE FIELD error_message ON task_execution TYPE option<string>;
                DEFINE FIELD started_at ON task_execution TYPE datetime;
                DEFINE FIELD completed_at ON task_execution TYPE option<datetime>;
                DEFINE INDEX task_agent_idx ON task_execution COLUMNS agent_id;
                DEFINE INDEX task_workflow_idx ON task_execution COLUMNS workflow_id;
            """)
            
            logger.info("SurrealDB schema initialized for agentic workflows")
```

### 1.2 Real-Time Event Bus with Live Queries

**File: `src/sentient_core/events/surrealdb_event_bus.py`**

```python
from typing import Dict, Any, List, Optional, Callable, AsyncGenerator
import asyncio
import json
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field
from ..database.surrealdb_config import SurrealDBConfig
import logging

logger = logging.getLogger(__name__)

class EventType(str, Enum):
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    TASK_PROGRESS = "task_progress"
    WORKFLOW_STEP_CHANGED = "workflow_step_changed"
    STATE_CHECKPOINT = "state_checkpoint"
    SYSTEM_ALERT = "system_alert"

class AgentEvent(BaseModel):
    """Event model for SurrealDB storage."""
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    source_agent: str
    target_agent: Optional[str] = None
    workflow_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class SurrealDBEventBus:
    """Event bus implementation using SurrealDB live queries."""
    
    def __init__(self, db_config: SurrealDBConfig):
        self.db_config = db_config
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._live_queries: Dict[str, str] = {}  # subscription_id -> query_uuid
        self._event_queues: Dict[str, asyncio.Queue] = {}
        self._running = False
        
    async def start(self) -> None:
        """Start the event bus and initialize live queries."""
        self._running = True
        await self._setup_live_queries()
        asyncio.create_task(self._process_events())
        logger.info("SurrealDB Event Bus started")
    
    async def stop(self) -> None:
        """Stop the event bus and cleanup live queries."""
        self._running = False
        
        # Kill all live queries
        async with self.db_config.get_connection() as db:
            for query_uuid in self._live_queries.values():
                await db.kill(query_uuid)
                
        logger.info("SurrealDB Event Bus stopped")
    
    async def _setup_live_queries(self) -> None:
        """Setup live queries for real-time event monitoring."""
        async with self.db_config.get_connection() as db:
            # Live query for all agent events
            query_uuid = await db.live('agent_event')
            self._live_queries['all_events'] = query_uuid
            
            # Subscribe to the live query
            event_queue = await db.subscribe_live(query_uuid)
            self._event_queues['all_events'] = event_queue
            
            logger.info(f"Live query setup for agent_event table: {query_uuid}")
    
    async def _process_events(self) -> None:
        """Process incoming events from live queries."""
        while self._running:
            try:
                for subscription_id, queue in self._event_queues.items():
                    try:
                        # Non-blocking queue check
                        notification = queue.get_nowait()
                        await self._handle_notification(notification)
                    except asyncio.QueueEmpty:
                        continue
                        
                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Error processing events: {e}")
                await asyncio.sleep(1)
    
    async def _handle_notification(self, notification: Dict[str, Any]) -> None:
        """Handle incoming live query notifications."""
        try:
            action = notification.get('action')
            data = notification.get('result', {})
            
            if action in ['CREATE', 'UPDATE']:
                event = AgentEvent(**data)
                await self._dispatch_event(event)
                
        except Exception as e:
            logger.error(f"Error handling notification: {e}")
    
    async def _dispatch_event(self, event: AgentEvent) -> None:
        """Dispatch event to registered subscribers."""
        subscribers = self._subscribers.get(event.event_type, [])
        
        for callback in subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"Error in event callback: {e}")
    
    async def publish_event(self, event: AgentEvent) -> None:
        """Publish an event to the bus."""
        async with self.db_config.get_connection() as db:
            await db.create('agent_event', event.dict())
            logger.debug(f"Published event: {event.event_type} from {event.source_agent}")
    
    def subscribe(self, event_type: EventType, callback: Callable[[AgentEvent], None]) -> str:
        """Subscribe to specific event types."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
            
        self._subscribers[event_type].append(callback)
        subscription_id = str(uuid4())
        
        logger.info(f"New subscription {subscription_id} for {event_type}")
        return subscription_id
    
    async def get_event_history(
        self, 
        workflow_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[AgentEvent]:
        """Retrieve event history with filtering."""
        async with self.db_config.get_connection() as db:
            query = "SELECT * FROM agent_event"
            conditions = []
            
            if workflow_id:
                conditions.append(f"workflow_id = '{workflow_id}'")
            if agent_id:
                conditions.append(f"source_agent = '{agent_id}'")
            if event_type:
                conditions.append(f"event_type = '{event_type.value}'")
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            query += f" ORDER BY timestamp DESC LIMIT {limit}"
            
            result = await db.query(query)
            return [AgentEvent(**record) for record in result[0]['result']]
```

### 1.3 Async State Manager with SurrealDB

**File: `src/sentient_core/state/surrealdb_state_manager.py`**

```python
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from enum import Enum
from ..database.surrealdb_config import SurrealDBConfig
import logging
import json

logger = logging.getLogger(__name__)

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class StateCheckpoint(BaseModel):
    """Agent state checkpoint model."""
    checkpoint_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    workflow_id: Optional[str] = None
    execution_context: Dict[str, Any] = Field(default_factory=dict)
    progress_data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    """Workflow state model for SurrealDB."""
    workflow_id: str = Field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.PENDING
    current_step: int = 0
    total_steps: int = 0
    agent_states: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AgentState(BaseModel):
    """Agent state model for SurrealDB."""
    agent_id: str
    name: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: List[str] = Field(default_factory=list)
    current_task: Optional[str] = None
    execution_context: Dict[str, Any] = Field(default_factory=dict)
    checkpoints: List[str] = Field(default_factory=list)  # checkpoint IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SurrealDBStateManager:
    """State manager using SurrealDB for persistence."""
    
    def __init__(self, db_config: SurrealDBConfig):
        self.db_config = db_config
        
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> WorkflowState:
        """Create a new workflow state."""
        workflow = WorkflowState(**workflow_data)
        
        async with self.db_config.get_connection() as db:
            result = await db.create('workflow_state', workflow.dict())
            logger.info(f"Created workflow: {workflow.workflow_id}")
            return WorkflowState(**result[0])
    
    async def get_workflow(self, workflow_id: str) -> Optional[WorkflowState]:
        """Retrieve workflow state by ID."""
        async with self.db_config.get_connection() as db:
            result = await db.select(f'workflow_state:{workflow_id}')
            if result:
                return WorkflowState(**result[0])
            return None
    
    async def update_workflow(
        self, 
        workflow_id: str, 
        updates: Dict[str, Any]
    ) -> Optional[WorkflowState]:
        """Update workflow state."""
        updates['updated_at'] = datetime.utcnow()
        
        async with self.db_config.get_connection() as db:
            result = await db.merge(f'workflow_state:{workflow_id}', updates)
            if result:
                logger.info(f"Updated workflow: {workflow_id}")
                return WorkflowState(**result[0])
            return None
    
    async def create_agent_state(self, agent_data: Dict[str, Any]) -> AgentState:
        """Create or update agent state."""
        agent = AgentState(**agent_data)
        
        async with self.db_config.get_connection() as db:
            result = await db.create('agent_state', agent.dict())
            logger.info(f"Created agent state: {agent.agent_id}")
            return AgentState(**result[0])
    
    async def get_agent_state(self, agent_id: str) -> Optional[AgentState]:
        """Retrieve agent state by ID."""
        async with self.db_config.get_connection() as db:
            result = await db.select(f'agent_state:{agent_id}')
            if result:
                return AgentState(**result[0])
            return None
    
    async def update_agent_state(
        self, 
        agent_id: str, 
        updates: Dict[str, Any]
    ) -> Optional[AgentState]:
        """Update agent state."""
        updates['updated_at'] = datetime.utcnow()
        
        async with self.db_config.get_connection() as db:
            result = await db.merge(f'agent_state:{agent_id}', updates)
            if result:
                logger.info(f"Updated agent state: {agent_id}")
                return AgentState(**result[0])
            return None
    
    async def create_checkpoint(
        self, 
        checkpoint_data: Dict[str, Any]
    ) -> StateCheckpoint:
        """Create a state checkpoint."""
        checkpoint = StateCheckpoint(**checkpoint_data)
        
        async with self.db_config.get_connection() as db:
            # Store checkpoint
            await db.create('state_checkpoint', checkpoint.dict())
            
            # Update agent's checkpoint list
            agent_id = checkpoint.agent_id
            agent_state = await self.get_agent_state(agent_id)
            if agent_state:
                checkpoints = agent_state.checkpoints + [checkpoint.checkpoint_id]
                await self.update_agent_state(agent_id, {'checkpoints': checkpoints})
            
            logger.info(f"Created checkpoint: {checkpoint.checkpoint_id}")
            return checkpoint
    
    async def restore_from_checkpoint(
        self, 
        checkpoint_id: str
    ) -> Optional[StateCheckpoint]:
        """Restore state from checkpoint."""
        async with self.db_config.get_connection() as db:
            result = await db.select(f'state_checkpoint:{checkpoint_id}')
            if result:
                checkpoint = StateCheckpoint(**result[0])
                
                # Restore agent state
                await self.update_agent_state(
                    checkpoint.agent_id,
                    {
                        'execution_context': checkpoint.execution_context,
                        'status': AgentStatus.RUNNING
                    }
                )
                
                logger.info(f"Restored from checkpoint: {checkpoint_id}")
                return checkpoint
            return None
    
    async def get_workflow_history(
        self, 
        workflow_id: str
    ) -> List[Dict[str, Any]]:
        """Get workflow execution history."""
        workflow = await self.get_workflow(workflow_id)
        if workflow:
            return workflow.execution_history
        return []
    
    async def add_workflow_history_entry(
        self, 
        workflow_id: str, 
        entry: Dict[str, Any]
    ) -> None:
        """Add entry to workflow history."""
        workflow = await self.get_workflow(workflow_id)
        if workflow:
            history = workflow.execution_history + [{
                **entry,
                'timestamp': datetime.utcnow().isoformat()
            }]
            await self.update_workflow(workflow_id, {'execution_history': history})
```

## Phase 2: Async Agent Implementation

### 2.1 SurrealDB-Aware Async Base Agent

**File: `src/sentient_core/agents/surrealdb_async_agent.py`**

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, AsyncGenerator, List
from contextlib import asynccontextmanager
import asyncio
import logging
from datetime import datetime
from uuid import uuid4
from enum import Enum

from ..state.surrealdb_state_manager import SurrealDBStateManager, AgentStatus
from ..events.surrealdb_event_bus import SurrealDBEventBus, AgentEvent, EventType
from ..database.surrealdb_config import SurrealDBConfig
from ..orchestrator.shared_state import Task

logger = logging.getLogger(__name__)

class TaskExecutionMode(str, Enum):
    BLOCKING = "blocking"
    STREAMING = "streaming"
    BACKGROUND = "background"

class SurrealDBAsyncAgent(ABC):
    """SurrealDB-aware async base agent with state management and events."""
    
    def __init__(
        self, 
        name: str, 
        capabilities: List[str],
        db_config: SurrealDBConfig,
        state_manager: SurrealDBStateManager,
        event_bus: SurrealDBEventBus,
        sandbox_tool: Optional[Any] = None
    ):
        self.name = name
        self.agent_id = f"{name}_{str(uuid4())[:8]}"
        self.capabilities = capabilities
        self.db_config = db_config
        self.state_manager = state_manager
        self.event_bus = event_bus
        self.sandbox_tool = sandbox_tool
        
        self._execution_context: Optional[Dict[str, Any]] = None
        self._cancellation_token = asyncio.Event()
        self._pause_token = asyncio.Event()
        self._current_status = AgentStatus.IDLE
        
        # Initialize agent state in database
        asyncio.create_task(self._initialize_agent_state())
        
    async def _initialize_agent_state(self) -> None:
        """Initialize agent state in SurrealDB."""
        try:
            await self.state_manager.create_agent_state({
                'agent_id': self.agent_id,
                'name': self.name,
                'status': self._current_status,
                'capabilities': self.capabilities
            })
            logger.info(f"Agent {self.name} state initialized in SurrealDB")
        except Exception as e:
            logger.error(f"Failed to initialize agent state: {e}")
    
    @abstractmethod
    async def execute_task(
        self, 
        task: Task, 
        mode: TaskExecutionMode = TaskExecutionMode.BLOCKING
    ) -> Dict[str, Any]:
        """Execute task with specified mode."""
        pass
    
    @abstractmethod
    async def stream_execution(self, task: Task) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream task execution progress."""
        pass
    
    async def _update_status(self, status: AgentStatus) -> None:
        """Update agent status in database and publish event."""
        self._current_status = status
        
        await self.state_manager.update_agent_state(
            self.agent_id, 
            {'status': status}
        )
        
        await self.event_bus.publish_event(AgentEvent(
            event_type=EventType.AGENT_STATUS_CHANGED,
            source_agent=self.agent_id,
            payload={'new_status': status.value}
        ))
    
    async def create_checkpoint(self, checkpoint_data: Dict[str, Any]) -> str:
        """Create execution state checkpoint."""
        checkpoint = await self.state_manager.create_checkpoint({
            'agent_id': self.agent_id,
            'execution_context': self._execution_context or {},
            'progress_data': checkpoint_data
        })
        
        await self.event_bus.publish_event(AgentEvent(
            event_type=EventType.STATE_CHECKPOINT,
            source_agent=self.agent_id,
            payload={'checkpoint_id': checkpoint.checkpoint_id}
        ))
        
        return checkpoint.checkpoint_id
    
    async def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore agent state from checkpoint."""
        checkpoint = await self.state_manager.restore_from_checkpoint(checkpoint_id)
        if checkpoint:
            self._execution_context = checkpoint.execution_context
            await self._update_status(AgentStatus.RUNNING)
            return True
        return False
    
    async def cancel_execution(self) -> None:
        """Cancel current task execution."""
        self._cancellation_token.set()
        await self._update_status(AgentStatus.IDLE)
        
        await self.event_bus.publish_event(AgentEvent(
            event_type=EventType.AGENT_COMPLETED,
            source_agent=self.agent_id,
            payload={'cancelled': True}
        ))
    
    async def pause_execution(self) -> None:
        """Pause current execution."""
        self._pause_token.set()
        await self._update_status(AgentStatus.PAUSED)
    
    async def resume_execution(self) -> None:
        """Resume paused execution."""
        self._pause_token.clear()
        await self._update_status(AgentStatus.RUNNING)
    
    @asynccontextmanager
    async def execution_context(self, task: Task, workflow_id: Optional[str] = None):
        """Manage execution context lifecycle with SurrealDB persistence."""
        try:
            self._execution_context = {
                'task_id': str(task.task_id),
                'workflow_id': workflow_id,
                'start_time': datetime.utcnow(),
                'status': 'running'
            }
            
            await self.state_manager.update_agent_state(
                self.agent_id,
                {
                    'current_task': str(task.task_id),
                    'execution_context': self._execution_context
                }
            )
            
            await self._update_status(AgentStatus.RUNNING)
            
            await self.event_bus.publish_event(AgentEvent(
                event_type=EventType.AGENT_STARTED,
                source_agent=self.agent_id,
                workflow_id=workflow_id,
                payload={
                    'task_id': str(task.task_id),
                    'task_description': task.description
                }
            ))
            
            yield self._execution_context
            
        except Exception as e:
            await self._update_status(AgentStatus.FAILED)
            
            await self.event_bus.publish_event(AgentEvent(
                event_type=EventType.AGENT_FAILED,
                source_agent=self.agent_id,
                workflow_id=workflow_id,
                payload={
                    'error': str(e),
                    'task_id': str(task.task_id)
                }
            ))
            raise
            
        finally:
            self._execution_context = None
            self._cancellation_token.clear()
            self._pause_token.clear()
            
            await self.state_manager.update_agent_state(
                self.agent_id,
                {
                    'current_task': None,
                    'execution_context': {}
                }
            )
            
            await self._update_status(AgentStatus.IDLE)
    
    async def _check_cancellation_and_pause(self) -> None:
        """Check for cancellation and pause signals."""
        if self._cancellation_token.is_set():
            raise asyncio.CancelledError("Task execution cancelled")
            
        while self._pause_token.is_set():
            await asyncio.sleep(0.1)
```

## Phase 3: Integration and Testing

### 3.1 SurrealDB Integration Tests

**File: `tests/integration/test_surrealdb_integration.py`**

```python
import pytest
import asyncio
from datetime import datetime
from uuid import uuid4

from src.sentient_core.database.surrealdb_config import SurrealDBConfig
from src.sentient_core.state.surrealdb_state_manager import (
    SurrealDBStateManager, WorkflowState, AgentState
)
from src.sentient_core.events.surrealdb_event_bus import (
    SurrealDBEventBus, AgentEvent, EventType
)

@pytest.fixture
async def db_config():
    """Test database configuration."""
    config = SurrealDBConfig(
        url="ws://localhost:8000/rpc",
        namespace="test",
        database="sentient_test"
    )
    await config.initialize_connection_pool()
    await config.setup_schema()
    yield config
    
    # Cleanup
    async with config.get_connection() as db:
        await db.query("REMOVE TABLE agent_state")
        await db.query("REMOVE TABLE workflow_state")
        await db.query("REMOVE TABLE agent_event")
        await db.query("REMOVE TABLE task_execution")

@pytest.fixture
async def state_manager(db_config):
    return SurrealDBStateManager(db_config)

@pytest.fixture
async def event_bus(db_config):
    bus = SurrealDBEventBus(db_config)
    await bus.start()
    yield bus
    await bus.stop()

class TestSurrealDBStateManager:
    """Test SurrealDB state management."""
    
    async def test_workflow_lifecycle(self, state_manager):
        """Test complete workflow state lifecycle."""
        # Create workflow
        workflow_data = {
            'status': 'pending',
            'total_steps': 5,
            'metadata': {'test': True}
        }
        
        workflow = await state_manager.create_workflow(workflow_data)
        assert workflow.workflow_id
        assert workflow.status == 'pending'
        assert workflow.total_steps == 5
        
        # Update workflow
        updates = {
            'status': 'running',
            'current_step': 2
        }
        
        updated_workflow = await state_manager.update_workflow(
            workflow.workflow_id, updates
        )
        assert updated_workflow.status == 'running'
        assert updated_workflow.current_step == 2
        
        # Retrieve workflow
        retrieved_workflow = await state_manager.get_workflow(workflow.workflow_id)
        assert retrieved_workflow.workflow_id == workflow.workflow_id
        assert retrieved_workflow.status == 'running'
    
    async def test_agent_state_management(self, state_manager):
        """Test agent state persistence."""
        agent_data = {
            'agent_id': 'test_agent_001',
            'name': 'TestAgent',
            'capabilities': ['coding', 'testing']
        }
        
        agent = await state_manager.create_agent_state(agent_data)
        assert agent.agent_id == 'test_agent_001'
        assert agent.name == 'TestAgent'
        assert 'coding' in agent.capabilities
        
        # Update agent state
        updates = {
            'status': 'running',
            'current_task': 'task_123'
        }
        
        updated_agent = await state_manager.update_agent_state(
            agent.agent_id, updates
        )
        assert updated_agent.status == 'running'
        assert updated_agent.current_task == 'task_123'
    
    async def test_checkpoint_system(self, state_manager):
        """Test state checkpointing and recovery."""
        # Create agent first
        agent_data = {
            'agent_id': 'checkpoint_agent',
            'name': 'CheckpointAgent'
        }
        await state_manager.create_agent_state(agent_data)
        
        # Create checkpoint
        checkpoint_data = {
            'agent_id': 'checkpoint_agent',
            'execution_context': {'step': 3, 'data': 'test'},
            'progress_data': {'completed': 0.6}
        }
        
        checkpoint = await state_manager.create_checkpoint(checkpoint_data)
        assert checkpoint.checkpoint_id
        assert checkpoint.agent_id == 'checkpoint_agent'
        
        # Restore from checkpoint
        restored = await state_manager.restore_from_checkpoint(
            checkpoint.checkpoint_id
        )
        assert restored.checkpoint_id == checkpoint.checkpoint_id
        
        # Verify agent state was updated
        agent = await state_manager.get_agent_state('checkpoint_agent')
        assert agent.execution_context['step'] == 3

class TestSurrealDBEventBus:
    """Test SurrealDB event bus functionality."""
    
    async def test_event_publishing_and_subscription(self, event_bus):
        """Test event publishing and real-time subscription."""
        received_events = []
        
        def event_handler(event: AgentEvent):
            received_events.append(event)
        
        # Subscribe to events
        subscription_id = event_bus.subscribe(EventType.AGENT_STARTED, event_handler)
        assert subscription_id
        
        # Publish event
        test_event = AgentEvent(
            event_type=EventType.AGENT_STARTED,
            source_agent='test_agent',
            payload={'test': 'data'}
        )
        
        await event_bus.publish_event(test_event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0].event_type == EventType.AGENT_STARTED
        assert received_events[0].source_agent == 'test_agent'
    
    async def test_event_history_retrieval(self, event_bus):
        """Test event history functionality."""
        workflow_id = str(uuid4())
        
        # Publish multiple events
        events = [
            AgentEvent(
                event_type=EventType.AGENT_STARTED,
                source_agent='agent1',
                workflow_id=workflow_id,
                payload={'step': 1}
            ),
            AgentEvent(
                event_type=EventType.TASK_PROGRESS,
                source_agent='agent1',
                workflow_id=workflow_id,
                payload={'progress': 0.5}
            ),
            AgentEvent(
                event_type=EventType.AGENT_COMPLETED,
                source_agent='agent1',
                workflow_id=workflow_id,
                payload={'result': 'success'}
            )
        ]
        
        for event in events:
            await event_bus.publish_event(event)
        
        # Wait for persistence
        await asyncio.sleep(0.1)
        
        # Retrieve history
        history = await event_bus.get_event_history(workflow_id=workflow_id)
        
        assert len(history) == 3
        assert all(event.workflow_id == workflow_id for event in history)
        
        # Test filtering by event type
        progress_events = await event_bus.get_event_history(
            workflow_id=workflow_id,
            event_type=EventType.TASK_PROGRESS
        )
        
        assert len(progress_events) == 1
        assert progress_events[0].event_type == EventType.TASK_PROGRESS

if __name__ == "__main__":
    pytest.main([__file__])
```

## Deployment and Production Considerations

### SurrealDB Production Setup

```bash
# Docker Compose for SurrealDB
version: '3.8'
services:
  surrealdb:
    image: surrealdb/surrealdb:latest
    ports:
      - "8000:8000"
    command: start --log trace --user root --pass root file:///data/database.db
    volumes:
      - surrealdb_data:/data
    environment:
      - SURREAL_CAPS_ALLOW_ALL=true
    restart: unless-stopped

volumes:
  surrealdb_data:
```

### Environment Configuration

```bash
# Production .env
SURREALDB_URL=ws://surrealdb:8000/rpc
SURREALDB_NAMESPACE=sentient_prod
SURREALDB_DATABASE=core
SURREALDB_USERNAME=admin
SURREALDB_PASSWORD=secure_password
SURREALDB_CONNECTION_POOL_SIZE=20
ENABLE_LIVE_QUERIES=true
LOG_LEVEL=INFO
```

## Benefits of SurrealDB Integration

1. **Native Async Support**: Full async/await compatibility eliminates blocking operations <mcreference link="https://surrealdb.com/docs/sdk/python/methods" index="3">3</mcreference>

2. **Real-Time Events**: LIVE SELECT queries provide built-in pub/sub functionality <mcreference link="https://surrealdb.com/docs/surrealql/statements/live" index="3">3</mcreference>

3. **Graph-Based State**: Perfect for modeling complex agent relationships and dependencies

4. **Built-in Versioning**: Automatic audit trails and state history

5. **Horizontal Scaling**: Multi-node support for production deployments

6. **WebSocket Communication**: Low-latency real-time updates <mcreference link="https://surrealdb.com/docs/sdk/python/concepts/streaming" index="2">2</mcreference>

7. **ACID Transactions**: Consistent state management across concurrent operations

8. **Schema Flexibility**: Dynamic schema evolution as agent capabilities grow

This SurrealDB-focused implementation provides a robust foundation for building production-ready agentic systems with native async support, real-time event streaming, and persistent state management.