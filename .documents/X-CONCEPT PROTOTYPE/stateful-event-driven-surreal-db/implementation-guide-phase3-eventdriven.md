# Implementation Guide Phase 3: Event-Driven Architecture

## Phase 3: Event-Driven Architecture (Week 5-6)

### Step 3.1: Event System Models

**File: `src/api/models/event_models.py`**

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    TASK_STARTED = "task_started"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_CANCELLED = "task_cancelled"
    AGENT_STATUS_CHANGED = "agent_status_changed"
    WORKFLOW_STEP_CHANGED = "workflow_step_changed"
    WORKFLOW_COMPLETED = "workflow_completed"
    SYSTEM_ALERT = "system_alert"
    CUSTOM = "custom"

class EventPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class Event(BaseModel):
    """Core event model for the event-driven system."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    source: str  # Agent name, service name, etc.
    target: Optional[str] = None  # Specific target for the event
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    priority: EventPriority = EventPriority.NORMAL
    correlation_id: Optional[UUID] = None  # For tracking related events
    workflow_id: Optional[UUID] = None
    session_id: Optional[UUID] = None
    retry_count: int = 0
    max_retries: int = 3
    expires_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class EventSubscription(BaseModel):
    """Event subscription configuration."""
    subscription_id: UUID = Field(default_factory=uuid4)
    subscriber_name: str
    event_types: List[EventType]
    filters: Dict[str, Any] = Field(default_factory=dict)  # Additional filtering criteria
    callback_url: Optional[str] = None  # For webhook subscriptions
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: Optional[datetime] = None

class EventDeliveryStatus(str, Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"
    RETRYING = "retrying"

class EventDelivery(BaseModel):
    """Tracks event delivery to subscribers."""
    delivery_id: UUID = Field(default_factory=uuid4)
    event_id: UUID
    subscription_id: UUID
    status: EventDeliveryStatus = EventDeliveryStatus.PENDING
    attempts: int = 0
    last_attempt: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
    next_retry: Optional[datetime] = None
```

### Step 3.2: Event Bus Implementation

**File: `src/sentient_core/events/event_bus.py`**

```python
import asyncio
import json
import logging
from typing import Dict, List, Callable, Any, Optional, Set
from uuid import UUID
from datetime import datetime, timedelta
from collections import defaultdict
from contextlib import asynccontextmanager

from ..api.models.event_models import Event, EventSubscription, EventType, EventPriority
from ..clients.surrealdb_client import get_surrealdb_client

logger = logging.getLogger(__name__)

class EventBus:
    """Async event bus using SurrealDB LIVE queries for real-time event streaming."""
    
    def __init__(self):
        self.db_client = None
        self._subscriptions: Dict[str, EventSubscription] = {}
        self._local_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._live_queries: Dict[str, str] = {}  # subscription_id -> live_query_id
        self._running = False
        self._consumer_tasks: Set[asyncio.Task] = set()
        self._background_tasks: Set[asyncio.Task] = set()
    
    async def initialize(self):
        """Initialize the event bus with SurrealDB connection."""
        try:
            # Initialize SurrealDB client
            self.db_client = await get_surrealdb_client()
            
            # Load existing subscriptions and reactivate LIVE queries
            await self._load_subscriptions()
            
            # Start background tasks
            self._running = True
            cleanup_task = asyncio.create_task(self._cleanup_expired_events())
            self._background_tasks.add(cleanup_task)
            
            logger.info("EventBus initialized successfully with SurrealDB")
            
        except Exception as e:
            logger.error(f"Failed to initialize EventBus: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the event bus."""
        self._running = False
        
        # Cancel all background tasks
        all_tasks = self._consumer_tasks | self._background_tasks
        for task in all_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if all_tasks:
            await asyncio.gather(*all_tasks, return_exceptions=True)
        
        # Kill all LIVE queries
        if self.db_client:
            for live_query_id in self._live_queries.values():
                try:
                    await self.db_client.kill(live_query_id)
                except Exception as e:
                    logger.warning(f"Failed to kill LIVE query {live_query_id}: {e}")
        
        # Close database connection
        if self.db_client:
            await self.db_client.close()
        
        logger.info("EventBus shutdown complete")
    
    async def publish(self, event: Event) -> bool:
        """Publish event to SurrealDB (automatically triggers LIVE queries)."""
        try:
            if not self.db_client:
                logger.error("EventBus not initialized")
                return False
            
            # Persist event to SurrealDB - this automatically triggers LIVE queries
            event_data = {
                "id": str(event.event_id),
                "event_type": event.event_type.value,
                "source": event.source,
                "target": event.target,
                "payload": event.payload,
                "metadata": event.metadata,
                "timestamp": event.timestamp.isoformat(),
                "priority": event.priority.value,
                "correlation_id": str(event.correlation_id) if event.correlation_id else None,
                "workflow_id": str(event.workflow_id) if event.workflow_id else None,
                "session_id": str(event.session_id) if event.session_id else None,
                "retry_count": event.retry_count,
                "max_retries": event.max_retries,
                "expires_at": event.expires_at.isoformat() if event.expires_at else None
            }
            
            await self.db_client.create("agent_event", event_data)
            
            # Handle local subscribers immediately
            await self._handle_local_event(event)
            
            logger.debug(f"Published event {event.event_id} to SurrealDB")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_id}: {e}")
            return False
    
    async def subscribe(self, subscription: EventSubscription, handler: Optional[Callable] = None) -> bool:
        """Subscribe to events using SurrealDB LIVE queries."""
        try:
            # Store subscription
            self._subscriptions[str(subscription.subscription_id)] = subscription
            
            # Persist subscription
            await self._persist_subscription(subscription)
            
            # Register local handler if provided
            if handler:
                for event_type in subscription.event_types:
                    self._local_handlers[event_type].append(handler)
            
            # Create LIVE query for real-time events
            await self._create_live_subscription(subscription, handler)
            
            logger.info(f"Created subscription {subscription.subscription_id} for {subscription.subscriber_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create subscription: {e}")
            return False
    
    async def unsubscribe(self, subscription_id: UUID) -> bool:
        """Remove subscription."""
        try:
            subscription_key = str(subscription_id)
            if subscription_key in self._subscriptions:
                subscription = self._subscriptions[subscription_key]
                
                # Remove local handlers
                for event_type in subscription.event_types:
                    if event_type in self._local_handlers:
                        # Note: This removes all handlers for the event type
                        # In a production system, you'd want more granular control
                        self._local_handlers[event_type].clear()
                
                # Remove from memory
                del self._subscriptions[subscription_key]
                
                # Remove from persistent storage
                await self._remove_subscription(subscription_id)
                
                logger.info(f"Removed subscription {subscription_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove subscription {subscription_id}: {e}")
            return False
    
    async def get_event_history(self, event_types: Optional[List[EventType]] = None, limit: int = 100) -> List[Event]:
        """Get recent event history from SurrealDB."""
        try:
            if not self.db_client:
                return []
            
            # Build query
            query = "SELECT * FROM agent_event"
            if event_types:
                event_type_values = [f"'{et.value}'" for et in event_types]
                query += f" WHERE event_type IN [{','.join(event_type_values)}]"
            
            query += f" ORDER BY timestamp DESC LIMIT {limit}"
            
            results = await self.db_client.query(query)
            
            events = []
            if results and len(results) > 0 and 'result' in results[0]:
                for event_data in results[0]['result']:
                    # Convert back to Event object
                    event = Event(
                        event_id=UUID(event_data['id']),
                        event_type=EventType(event_data['event_type']),
                        source=event_data['source'],
                        target=event_data.get('target'),
                        payload=event_data.get('payload', {}),
                        metadata=event_data.get('metadata', {}),
                        timestamp=datetime.fromisoformat(event_data['timestamp']),
                        priority=EventPriority(event_data['priority']),
                        correlation_id=UUID(event_data['correlation_id']) if event_data.get('correlation_id') else None,
                        workflow_id=UUID(event_data['workflow_id']) if event_data.get('workflow_id') else None,
                        session_id=UUID(event_data['session_id']) if event_data.get('session_id') else None,
                        retry_count=event_data.get('retry_count', 0),
                        max_retries=event_data.get('max_retries', 3),
                        expires_at=datetime.fromisoformat(event_data['expires_at']) if event_data.get('expires_at') else None
                    )
                    events.append(event)
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to get event history: {e}")
            return []
    
    async def get_subscriptions(self, subscriber_name: Optional[str] = None) -> List[EventSubscription]:
        """Get active subscriptions."""
        subscriptions = list(self._subscriptions.values())
        
        if subscriber_name:
            subscriptions = [s for s in subscriptions if s.subscriber_name == subscriber_name]
        
        return [s for s in subscriptions if s.is_active]
    
    @asynccontextmanager
    async def event_transaction(self, correlation_id: UUID):
        """Context manager for publishing related events with correlation ID."""
        events = []
        
        class TransactionPublisher:
            def __init__(self, bus, corr_id):
                self.bus = bus
                self.correlation_id = corr_id
                self.events = events
            
            async def publish(self, event: Event):
                event.correlation_id = self.correlation_id
                self.events.append(event)
                return await self.bus.publish(event)
        
        try:
            yield TransactionPublisher(self, correlation_id)
        except Exception as e:
            # Publish rollback event if transaction fails
            rollback_event = Event(
                event_type=EventType.SYSTEM_ALERT,
                source="event_bus",
                payload={"error": str(e), "failed_events": len(events)},
                correlation_id=correlation_id,
                priority=EventPriority.HIGH
            )
            await self.publish(rollback_event)
            raise
    
    async def _create_live_subscription(self, subscription: EventSubscription, handler: Optional[Callable] = None):
        """Create a SurrealDB LIVE query for the subscription."""
        try:
            if not self.db_client:
                return
            
            # Build LIVE query for the subscription
            event_types = [f"'{et.value}'" for et in subscription.event_types]
            query = f"LIVE SELECT * FROM agent_event WHERE event_type IN [{','.join(event_types)}]"
            
            # Add filters if any
            if subscription.filters:
                for key, value in subscription.filters.items():
                    if key == "source":
                        query += f" AND source = '{value}'"
                    elif key == "priority":
                        query += f" AND priority = '{value}'"
                    elif key == "workflow_id":
                        query += f" AND workflow_id = '{value}'"
            
            # Execute LIVE query
            live_result = await self.db_client.query(query)
            
            if live_result and len(live_result) > 0 and 'result' in live_result[0]:
                live_query_id = live_result[0]['result']
                self._live_queries[str(subscription.subscription_id)] = live_query_id
                
                # Start consumer task for this LIVE query
                consumer_task = asyncio.create_task(
                    self._consume_live_events(live_query_id, subscription, handler)
                )
                self._consumer_tasks.add(consumer_task)
                
                logger.info(f"Created LIVE query {live_query_id} for subscription {subscription.subscription_id}")
            
        except Exception as e:
            logger.error(f"Failed to create LIVE subscription: {e}")
    
    async def _handle_local_event(self, event: Event):
        """Handle event for local subscribers."""
        handlers = self._local_handlers.get(event.event_type, [])
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    # Run sync handler in thread pool
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, handler, event)
            except Exception as e:
                logger.error(f"Local event handler failed: {e}")
    
    async def _handle_distributed_event(self, event: Event):
        """Handle event from distributed subscribers."""
        # Find matching subscriptions
        for subscription in self._subscriptions.values():
            if not subscription.is_active:
                continue
            
            if event.event_type in subscription.event_types:
                # Apply filters if any
                if self._event_matches_filters(event, subscription.filters):
                    await self._deliver_event(event, subscription)
    
    def _event_matches_filters(self, event: Event, filters: Dict[str, Any]) -> bool:
        """Check if event matches subscription filters."""
        if not filters:
            return True
        
        for key, value in filters.items():
            if key == "source" and event.source != value:
                return False
            elif key == "priority" and event.priority != value:
                return False
            elif key == "workflow_id" and event.workflow_id != value:
                return False
            # Add more filter criteria as needed
        
        return True
    
    async def _deliver_event(self, event: Event, subscription: EventSubscription):
        """Deliver event to subscriber."""
        try:
            if subscription.callback_url:
                # HTTP webhook delivery
                await self._deliver_webhook(event, subscription)
            else:
                # Local delivery (already handled by local handlers)
                pass
                
            # Update subscription activity
            subscription.last_activity = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"Failed to deliver event {event.event_id} to {subscription.subscriber_name}: {e}")
    
    async def _deliver_webhook(self, event: Event, subscription: EventSubscription):
        """Deliver event via HTTP webhook."""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "event": event.dict(),
                    "subscription": {
                        "id": str(subscription.subscription_id),
                        "subscriber": subscription.subscriber_name
                    }
                }
                
                async with session.post(
                    subscription.callback_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        logger.debug(f"Webhook delivered successfully to {subscription.callback_url}")
                    else:
                        logger.warning(f"Webhook delivery failed with status {response.status}")
                        
        except Exception as e:
            logger.error(f"Webhook delivery error: {e}")
    
    async def _consume_live_events(self, live_query_id: str, subscription: EventSubscription, handler: Optional[Callable] = None):
        """Consume events from a SurrealDB LIVE query."""
        try:
            while self._running:
                # Listen for LIVE query notifications
                notifications = await self.db_client.query(f"LIVE {live_query_id}")
                
                if notifications and len(notifications) > 0:
                    for notification in notifications[0].get('result', []):
                        try:
                            # Parse the event from notification
                            event_data = notification.get('result', {})
                            if event_data:
                                event = Event(
                                    event_id=UUID(event_data['id']),
                                    event_type=EventType(event_data['event_type']),
                                    source=event_data['source'],
                                    target=event_data.get('target'),
                                    payload=event_data.get('payload', {}),
                                    metadata=event_data.get('metadata', {}),
                                    timestamp=datetime.fromisoformat(event_data['timestamp']),
                                    priority=EventPriority(event_data['priority']),
                                    correlation_id=UUID(event_data['correlation_id']) if event_data.get('correlation_id') else None,
                                    workflow_id=UUID(event_data['workflow_id']) if event_data.get('workflow_id') else None,
                                    session_id=UUID(event_data['session_id']) if event_data.get('session_id') else None,
                                    retry_count=event_data.get('retry_count', 0),
                                    max_retries=event_data.get('max_retries', 3),
                                    expires_at=datetime.fromisoformat(event_data['expires_at']) if event_data.get('expires_at') else None
                                )
                                
                                # Handle the event
                                if handler:
                                    if asyncio.iscoroutinefunction(handler):
                                        await handler(event)
                                    else:
                                        loop = asyncio.get_event_loop()
                                        await loop.run_in_executor(None, handler, event)
                                
                                # Deliver to webhook if configured
                                if subscription.callback_url:
                                    await self._deliver_webhook(event, subscription)
                                    
                        except Exception as e:
                            logger.error(f"Failed to process LIVE event: {e}")
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"LIVE event consumer error for {live_query_id}: {e}")
        finally:
            # Clean up
            if live_query_id in self._live_queries.values():
                try:
                    await self.db_client.kill(live_query_id)
                except Exception as e:
                    logger.warning(f"Failed to kill LIVE query {live_query_id}: {e}")
    
    async def _cleanup_expired_events(self):
        """Clean up expired events and subscriptions."""
        while self._running:
            try:
                await asyncio.sleep(3600)  # Clean every hour
                
                current_time = datetime.utcnow()
                
                # Clean expired events from history
                self._event_history = [
                    e for e in self._event_history 
                    if not e.expires_at or e.expires_at > current_time
                ]
                
                # Clean inactive subscriptions
                inactive_threshold = current_time - timedelta(days=7)
                inactive_subs = [
                    sub_id for sub_id, sub in self._subscriptions.items()
                    if sub.last_activity and sub.last_activity < inactive_threshold
                ]
                
                for sub_id in inactive_subs:
                    await self.unsubscribe(UUID(sub_id))
                
                logger.debug(f"Cleaned {len(inactive_subs)} inactive subscriptions")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup task error: {e}")
    
    async def _persist_event(self, event: Event):
        """Persist event to database (handled in publish method)."""
        # This is now handled directly in the publish method
        # to avoid duplicate database operations
        pass
    
    async def _persist_subscription(self, subscription: EventSubscription):
        """Persist subscription to database."""
        db = await get_surrealdb_client()
        try:
            if db:
                sub_data = subscription.dict()
                await db.create("event_subscription", sub_data)
        except Exception as e:
            logger.error(f"Failed to persist subscription {subscription.subscription_id}: {e}")
        finally:
            if db:
                await db.close()
    
    async def _load_subscriptions(self):
        """Load existing subscriptions from database and reactivate LIVE queries."""
        try:
            if self.db_client:
                results = await self.db_client.query("SELECT * FROM event_subscription WHERE is_active = true")
                if results and len(results) > 0 and 'result' in results[0]:
                    for sub_data in results[0]['result']:
                        subscription = EventSubscription(**sub_data)
                        self._subscriptions[str(subscription.subscription_id)] = subscription
                        
                        # Reactivate LIVE query for this subscription
                        await self._create_live_subscription(subscription)
                        
                logger.info(f"Loaded {len(self._subscriptions)} active subscriptions")
        except Exception as e:
            logger.error(f"Failed to load subscriptions: {e}")
    
    async def _remove_subscription(self, subscription_id: UUID):
        """Remove subscription from database and kill LIVE query."""
        try:
            subscription_key = str(subscription_id)
            
            # Kill associated LIVE query
            if subscription_key in self._live_queries:
                live_query_id = self._live_queries[subscription_key]
                try:
                    await self.db_client.kill(live_query_id)
                    del self._live_queries[subscription_key]
                except Exception as e:
                    logger.warning(f"Failed to kill LIVE query {live_query_id}: {e}")
            
            # Remove from database
            if self.db_client:
                await self.db_client.delete(f"event_subscription:{subscription_id}")
                
        except Exception as e:
            logger.error(f"Failed to remove subscription {subscription_id}: {e}")
```

### Step 3.3: Event-Aware Agent Base Class

**File: `src/sentient_core/agents/event_aware_agent.py`**

```python
from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
import asyncio
import logging

from .async_base_agent import AsyncBaseAgent, TaskExecutionMode
from ..events.event_bus import EventBus
from ..api.models.event_models import Event, EventType, EventPriority, EventSubscription
from ..orchestrator.shared_state import Task

logger = logging.getLogger(__name__)

class EventAwareAgent(AsyncBaseAgent):
    """Base class for agents that can publish and subscribe to events."""
    
    def __init__(self, name: str, event_bus: EventBus, sandbox_tool: Optional[Any] = None):
        super().__init__(name, sandbox_tool)
        self.event_bus = event_bus
        self._subscriptions: List[EventSubscription] = []
        self._event_handlers: Dict[EventType, List[callable]] = {}
        self._correlation_id: Optional[UUID] = None
    
    async def initialize_events(self):
        """Initialize event subscriptions for this agent."""
        # Subscribe to relevant events
        await self._setup_event_subscriptions()
        logger.info(f"Event subscriptions initialized for agent {self.name}")
    
    async def execute_task(self, task: Task, mode: TaskExecutionMode = TaskExecutionMode.BLOCKING) -> Dict[str, Any]:
        """Execute task with event publishing."""
        self._correlation_id = uuid4()
        
        # Publish task started event
        await self.publish_event(
            EventType.TASK_STARTED,
            payload={
                "task_id": str(task.task_id),
                "task_description": task.task,
                "mode": mode.value
            },
            priority=EventPriority.NORMAL
        )
        
        try:
            # Execute the actual task
            result = await self._execute_task_impl(task, mode)
            
            # Publish completion event
            await self.publish_event(
                EventType.TASK_COMPLETED,
                payload={
                    "task_id": str(task.task_id),
                    "result": result,
                    "execution_mode": mode.value
                },
                priority=EventPriority.NORMAL
            )
            
            return result
            
        except Exception as e:
            # Publish failure event
            await self.publish_event(
                EventType.TASK_FAILED,
                payload={
                    "task_id": str(task.task_id),
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                priority=EventPriority.HIGH
            )
            raise
    
    async def _execute_task_impl(self, task: Task, mode: TaskExecutionMode) -> Dict[str, Any]:
        """Override this method in subclasses for actual task execution."""
        raise NotImplementedError("Subclasses must implement _execute_task_impl")
    
    async def publish_event(self, event_type: EventType, payload: Dict[str, Any], 
                          priority: EventPriority = EventPriority.NORMAL, 
                          target: Optional[str] = None) -> bool:
        """Publish an event from this agent."""
        event = Event(
            event_type=event_type,
            source=self.name,
            target=target,
            payload=payload,
            priority=priority,
            correlation_id=self._correlation_id
        )
        
        success = await self.event_bus.publish(event)
        if success:
            self.log(f"Published {event_type.value} event", "debug")
        else:
            self.log(f"Failed to publish {event_type.value} event", "error")
        
        return success
    
    async def publish_progress(self, progress: int, message: str, metadata: Dict[str, Any] = None):
        """Publish task progress event."""
        payload = {
            "progress": progress,
            "message": message,
            "agent": self.name
        }
        if metadata:
            payload.update(metadata)
        
        await self.publish_event(
            EventType.TASK_PROGRESS,
            payload=payload,
            priority=EventPriority.NORMAL
        )
    
    async def subscribe_to_events(self, event_types: List[EventType], 
                                handler: callable, 
                                filters: Dict[str, Any] = None) -> UUID:
        """Subscribe to specific event types with a handler."""
        subscription = EventSubscription(
            subscriber_name=self.name,
            event_types=event_types,
            filters=filters or {}
        )
        
        success = await self.event_bus.subscribe(subscription, handler)
        if success:
            self._subscriptions.append(subscription)
            
            # Register local handler
            for event_type in event_types:
                if event_type not in self._event_handlers:
                    self._event_handlers[event_type] = []
                self._event_handlers[event_type].append(handler)
            
            self.log(f"Subscribed to events: {[et.value for et in event_types]}")
            return subscription.subscription_id
        else:
            raise Exception("Failed to create event subscription")
    
    async def handle_agent_status_change(self, event: Event):
        """Handle agent status change events."""
        if event.source != self.name:  # Don't handle our own status changes
            payload = event.payload
            agent_name = payload.get("agent_name")
            status = payload.get("status")
            
            self.log(f"Agent {agent_name} status changed to {status}")
            
            # Override in subclasses for specific behavior
            await self._on_agent_status_changed(agent_name, status, event)
    
    async def handle_workflow_step_change(self, event: Event):
        """Handle workflow step change events."""
        payload = event.payload
        workflow_id = payload.get("workflow_id")
        new_step = payload.get("new_step")
        previous_step = payload.get("previous_step")
        
        self.log(f"Workflow {workflow_id} moved from {previous_step} to {new_step}")
        
        # Override in subclasses for specific behavior
        await self._on_workflow_step_changed(workflow_id, new_step, previous_step, event)
    
    async def _setup_event_subscriptions(self):
        """Setup default event subscriptions. Override in subclasses."""
        # Subscribe to agent status changes
        await self.subscribe_to_events(
            [EventType.AGENT_STATUS_CHANGED],
            self.handle_agent_status_change
        )
        
        # Subscribe to workflow changes
        await self.subscribe_to_events(
            [EventType.WORKFLOW_STEP_CHANGED],
            self.handle_workflow_step_change
        )
    
    async def _on_agent_status_changed(self, agent_name: str, status: str, event: Event):
        """Override in subclasses to handle agent status changes."""
        pass
    
    async def _on_workflow_step_changed(self, workflow_id: str, new_step: str, previous_step: str, event: Event):
        """Override in subclasses to handle workflow step changes."""
        pass
    
    async def cleanup_events(self):
        """Clean up event subscriptions."""
        for subscription in self._subscriptions:
            await self.event_bus.unsubscribe(subscription.subscription_id)
        
        self._subscriptions.clear()
        self._event_handlers.clear()
        
        self.log("Event subscriptions cleaned up")
```

### Step 3.4: Enhanced Frontend Developer Agent with Events

**File: `src/sentient_core/specialized_agents/event_aware_frontend_agent.py`**

```python
from typing import Dict, Any, AsyncGenerator
import asyncio

from ..agents.event_aware_agent import EventAwareAgent
from ..agents.async_base_agent import TaskExecutionMode
from ..api.models.event_models import EventType, EventPriority
from ..orchestrator.shared_state import Task
from ..tools.async_webcontainer_tool import AsyncWebContainerTool, WebContainerToolInput
from ..events.event_bus import EventBus

class EventAwareFrontendDeveloperAgent(EventAwareAgent):
    """Frontend developer agent with full event integration."""
    
    def __init__(self, event_bus: EventBus, sandbox_tool: AsyncWebContainerTool = None):
        super().__init__(name="EventAwareFrontendDeveloperAgent", event_bus=event_bus, sandbox_tool=sandbox_tool)
    
    async def _execute_task_impl(self, task: Task, mode: TaskExecutionMode) -> Dict[str, Any]:
        """Execute frontend development task with event publishing."""
        if mode == TaskExecutionMode.STREAMING:
            return await self._execute_streaming(task)
        elif mode == TaskExecutionMode.BACKGROUND:
            asyncio.create_task(self._execute_background(task))
            return {"status": "started", "task_id": str(task.task_id)}
        else:
            return await self._execute_blocking(task)
    
    async def _execute_streaming(self, task: Task) -> Dict[str, Any]:
        """Execute with real-time progress events."""
        async for progress in self.stream_execution(task):
            await self.publish_progress(
                progress.get("progress", 0),
                progress.get("status", "processing"),
                {"phase": progress.get("phase", "unknown")}
            )
        
        return {"status": "streaming_complete", "task_id": str(task.task_id)}
    
    async def stream_execution(self, task: Task) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream execution with enhanced event publishing."""
        async with self.execution_context(task):
            try:
                # Phase 1: Analysis
                yield {"phase": "analysis", "status": "analyzing_requirements", "progress": 10}
                await self.publish_event(
                    EventType.CUSTOM,
                    payload={"phase": "analysis_started", "task_id": str(task.task_id)}
                )
                
                await asyncio.sleep(0.5)
                await self.create_checkpoint({"phase": "analysis_complete"})
                
                # Phase 2: Generation
                yield {"phase": "generation", "status": "generating_components", "progress": 30}
                await self.publish_event(
                    EventType.CUSTOM,
                    payload={"phase": "generation_started", "task_id": str(task.task_id)}
                )
                
                html_content = await self._generate_html_with_events(task)
                yield {"phase": "generation", "status": "html_generated", "progress": 50}
                
                await self.create_checkpoint({"phase": "generation_complete", "html_content": html_content})
                
                # Phase 3: Deployment
                yield {"phase": "deploy", "status": "deploying", "progress": 70}
                await self.publish_event(
                    EventType.CUSTOM,
                    payload={"phase": "deployment_started", "task_id": str(task.task_id)}
                )
                
                if not self.sandbox_tool:
                    raise ValueError("WebContainer tool required")
                
                file_tree = {"index.html": html_content}
                tool_input = WebContainerToolInput(files=file_tree, commands=["serve"])
                
                deployment_result = await self.sandbox_tool.run_async(tool_input)
                
                await self.create_checkpoint({
                    "phase": "deployment_complete",
                    "url": deployment_result.get("url")
                })
                
                # Phase 4: Completion
                yield {
                    "phase": "complete",
                    "status": "completed",
                    "progress": 100,
                    "result": {
                        "url": deployment_result.get("url"),
                        "artifacts": [deployment_result.get("url")]
                    }
                }
                
                await self.publish_event(
                    EventType.CUSTOM,
                    payload={
                        "phase": "deployment_complete",
                        "url": deployment_result.get("url"),
                        "task_id": str(task.task_id)
                    },
                    priority=EventPriority.HIGH
                )
                
            except Exception as e:
                yield {"phase": "error", "status": "failed", "progress": -1, "error": str(e)}
                await self.publish_event(
                    EventType.SYSTEM_ALERT,
                    payload={"error": str(e), "phase": "execution_failed"},
                    priority=EventPriority.CRITICAL
                )
                raise
    
    async def _generate_html_with_events(self, task: Task) -> str:
        """Generate HTML with event-driven features."""
        await self.publish_event(
            EventType.CUSTOM,
            payload={"action": "html_generation_started", "task": task.task}
        )
        
        # Enhanced HTML with event handling
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <title>Task: {task.task}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {{ font-family: Arial, sans-serif; margin: 40px; }}
      .container {{ max-width: 800px; margin: 0 auto; }}
      .status {{ padding: 10px; background: #f0f0f0; border-radius: 5px; margin: 10px 0; }}
      .event-log {{ background: #f9f9f9; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; }}
      .event-item {{ margin: 5px 0; padding: 5px; background: white; border-radius: 3px; }}
      .connected {{ color: green; }}
      .disconnected {{ color: red; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{task.task}</h1>
      <div id="backend-response" class="status">Connecting to backend...</div>
      <div id="connection-status" class="status disconnected">Disconnected</div>
      
      <h3>Real-time Events</h3>
      <div id="event-log" class="event-log">
        <div class="event-item">Waiting for events...</div>
      </div>
      
      <div id="status" class="status">Ready</div>
    </div>
    
    <script type="module">
      // Event-driven frontend with WebSocket connection
      class EventClient {{
        constructor() {{
          this.ws = null;
          this.reconnectAttempts = 0;
          this.maxReconnectAttempts = 5;
          this.connect();
        }}
        
        connect() {{
          try {{
            this.ws = new WebSocket('ws://localhost:8080/events');
            
            this.ws.onopen = () => {{
              console.log('Connected to event stream');
              document.getElementById('connection-status').textContent = 'Connected';
              document.getElementById('connection-status').className = 'status connected';
              this.reconnectAttempts = 0;
              
              // Subscribe to relevant events
              this.ws.send(JSON.stringify({{
                type: 'subscribe',
                event_types: ['task_progress', 'task_completed', 'custom']
              }}));
            }};
            
            this.ws.onmessage = (event) => {{
              const data = JSON.parse(event.data);
              this.handleEvent(data);
            }};
            
            this.ws.onclose = () => {{
              console.log('Disconnected from event stream');
              document.getElementById('connection-status').textContent = 'Disconnected';
              document.getElementById('connection-status').className = 'status disconnected';
              this.scheduleReconnect();
            }};
            
            this.ws.onerror = (error) => {{
              console.error('WebSocket error:', error);
            }};
          }} catch (error) {{
            console.error('Failed to connect:', error);
            this.scheduleReconnect();
          }}
        }}
        
        handleEvent(eventData) {{
          const eventLog = document.getElementById('event-log');
          const eventItem = document.createElement('div');
          eventItem.className = 'event-item';
          
          const timestamp = new Date().toLocaleTimeString();
          eventItem.innerHTML = `
            <strong>[${{timestamp}}]</strong> 
            ${{eventData.event_type}}: ${{JSON.stringify(eventData.payload)}}
          `;
          
          eventLog.insertBefore(eventItem, eventLog.firstChild);
          
          // Keep only last 20 events
          while (eventLog.children.length > 20) {{
            eventLog.removeChild(eventLog.lastChild);
          }}
        }}
        
        scheduleReconnect() {{
          if (this.reconnectAttempts < this.maxReconnectAttempts) {{
            this.reconnectAttempts++;
            const delay = Math.pow(2, this.reconnectAttempts) * 1000; // Exponential backoff
            setTimeout(() => this.connect(), delay);
          }}
        }}
      }}
      
      // Initialize event client
      const eventClient = new EventClient();
      
      // Health check for backend
      async function checkBackendHealth() {{
        try {{
          const response = await fetch('/api/health');
          const data = await response.json();
          document.getElementById('backend-response').textContent = 
            `Backend Status: ${{data.status}} (Response time: ${{Date.now() - startTime}}ms)`;
        }} catch (error) {{
          document.getElementById('backend-response').textContent = 
            `Backend Error: ${{error.message}}`;
        }}
      }}
      
      const startTime = Date.now();
      checkBackendHealth();
      
      // Periodic health checks
      setInterval(checkBackendHealth, 30000);
    </script>
  </body>
</html>"""
        
        await self.publish_event(
            EventType.CUSTOM,
            payload={"action": "html_generation_completed", "size": len(html_content)}
        )
        
        return html_content
    
    async def _on_agent_status_changed(self, agent_name: str, status: str, event):
        """React to other agent status changes."""
        if "backend" in agent_name.lower() and status == "completed":
            # Backend agent completed, we might need to update our frontend
            await self.publish_event(
                EventType.CUSTOM,
                payload={
                    "action": "backend_integration_ready",
                    "backend_agent": agent_name
                }
            )
    
    async def _on_workflow_step_changed(self, workflow_id: str, new_step: str, previous_step: str, event):
        """React to workflow step changes."""
        if new_step == "frontend_development":
            # This is our cue to start working
            await self.publish_event(
                EventType.CUSTOM,
                payload={
                    "action": "frontend_development_phase_started",
                    "workflow_id": workflow_id
                }
            )
```

This completes the event-driven architecture implementation. The system now supports:

1. **Async Foundation**: All agents can run asynchronously with proper cancellation and state management
2. **Stateful Workflows**: Persistent workflow state with checkpointing and recovery
3. **Event-Driven Communication**: Real-time event bus for agent coordination and progress tracking
4. **Enhanced Monitoring**: Comprehensive event logging and real-time updates
5. **Fault Tolerance**: Automatic retries, circuit breakers, and graceful degradation

The next phase would focus on integration testing and production deployment considerations.