# Async Architecture Specification for Sentient-Core

## Overview

This document provides detailed technical specifications for implementing async/await patterns, stateful workflows, and event-driven architecture in Sentient-Core using SurrealDB as the primary database. It includes concrete code patterns, database schemas, and integration strategies.

## Dependencies

```toml
# Add to pyproject.toml
[tool.poetry.dependencies]
aiohttp = "^3.9.0"
websockets = "^12.0"
structlog = "^23.2.0"
aiofiles = "^23.2.0"
surrealdb = "^0.3.2"  # Primary database with native async support
pydantic = "^2.5.0"
```

## Environment Configuration

```bash
# Add to .env
SURREALDB_URL=ws://localhost:8000/rpc
SURREALDB_NAMESPACE=sentient_core
SURREALDB_DATABASE=agents
SURREALDB_USERNAME=root
SURREALDB_PASSWORD=root
LOG_LEVEL=INFO
AGENT_EXECUTION_TIMEOUT=3600
MAX_CONCURRENT_AGENTS=10
EVENT_BUS_BACKEND=surrealdb
STATE_PERSISTENCE_BACKEND=surrealdb
```

## 1. Async Agent Architecture

### 1.1 Enhanced BaseAgent Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, AsyncGenerator
from contextlib import asynccontextmanager
import asyncio
from enum import Enum
from datetime import datetime
from uuid import uuid4
import structlog

logger = structlog.get_logger()

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
    
    async def _persist_checkpoint(self, checkpoint: Dict[str, Any]) -> bool:
        """Persist checkpoint to SurrealDB."""
        try:
            from ..clients.surrealdb_client import get_surrealdb_client
            db = await get_surrealdb_client()
            
            checkpoint_data = {
                "id": checkpoint["id"],
                "agent_name": checkpoint["agent_name"],
                "timestamp": checkpoint["timestamp"].isoformat(),
                "data": checkpoint["data"]
            }
            
            await db.create("agent_checkpoint", checkpoint_data)
            await db.close()
            
            logger.info(f"Persisted checkpoint {checkpoint['id']} for agent {self.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to persist checkpoint {checkpoint['id']}: {e}")
            return False
    
    async def _load_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load checkpoint from SurrealDB."""
        try:
            from ..clients.surrealdb_client import get_surrealdb_client
            db = await get_surrealdb_client()
            
            result = await db.select(f"agent_checkpoint:{checkpoint_id}")
            await db.close()
            
            if result:
                checkpoint_data = result[0] if isinstance(result, list) else result
                return {
                    "id": checkpoint_data["id"],
                    "agent_name": checkpoint_data["agent_name"],
                    "timestamp": datetime.fromisoformat(checkpoint_data["timestamp"]),
                    "data": checkpoint_data["data"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to load checkpoint {checkpoint_id}: {e}")
            return None
    
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

This specification provides the concrete implementation patterns needed to transform Sentient-Core into a fully async, stateful, and event-driven system using SurrealDB as the primary database. Each component is designed to work together while maintaining modularity and testability.