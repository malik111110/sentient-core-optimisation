# Archon Framework Integration Guide

**ID:** guide:feature:archon_framework_integration  
**Source Reference(s):** /python agents/Archon  
**Last Validated:** June 2025

## 1. Purpose

Implement the Archon multi-agent framework for orchestrating specialized AI agents within the Genesis Engine, providing a robust foundation for agent coordination, task distribution, and collaborative problem-solving.

## 2. Key Concepts

- **Agent Orchestration**: Central coordination of multiple specialized agents
- **Task Decomposition**: Breaking complex tasks into agent-specific subtasks
- **Agent Communication**: Structured messaging and data exchange between agents
- **State Management**: Centralized state tracking across agent interactions
- **Tool Integration**: Unified tool access and execution across agents
- **Workflow Automation**: Automated agent workflow execution and monitoring
- **Error Recovery**: Robust error handling and agent failure recovery
- **Performance Monitoring**: Real-time agent performance and health tracking

## 3. Required Dependencies

### Python Dependencies
```python
# requirements.txt
archon-ai>=0.2.0
pydantic>=2.5.0
langchain>=0.1.0
langchain-core>=0.1.0
langchain-community>=0.0.10
openai>=1.10.0
anthropicai>=0.8.0
fastapi>=0.104.0
uvicorn>=0.24.0
redis>=5.0.0
celery>=5.3.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic-settings>=2.1.0
structlog>=23.2.0
prometheus-client>=0.19.0
aioredis>=2.0.0
aiofiles>=23.2.0
typer>=0.9.0
rich>=13.7.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
factory-boy>=3.3.0
```

### Environment Variables
```bash
# Archon Configuration
ARCHON_ENVIRONMENT=development
ARCHON_LOG_LEVEL=INFO
ARCHON_DEBUG=true

# Agent Configuration
MAX_CONCURRENT_AGENTS=10
AGENT_TIMEOUT=300
AGENT_RETRY_ATTEMPTS=3
AGENT_HEARTBEAT_INTERVAL=30

# LLM Provider Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/archon_db
REDIS_URL=redis://localhost:6379/0

# Message Queue Configuration
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Monitoring and Observability
PROMETHEUS_PORT=8000
JAEGER_ENDPOINT=http://localhost:14268/api/traces
LOG_FORMAT=json

# Security
API_SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
ALLOWED_HOSTS=localhost,127.0.0.1

# Performance Tuning
WORKER_PROCESSES=4
WORKER_CONNECTIONS=1000
MAX_REQUESTS_PER_WORKER=1000
REQUEST_TIMEOUT=60
```

## 4. Step-by-Step Implementation Plan

### 4.1 Core Framework Setup
1. Install Archon framework and dependencies
2. Configure agent orchestration engine
3. Set up agent registry and discovery
4. Implement agent lifecycle management
5. Configure communication protocols

### 4.2 Agent Development and Registration
1. Define agent interfaces and contracts
2. Implement specialized agent classes
3. Create agent capability definitions
4. Set up agent registration system
5. Implement agent health monitoring

### 4.3 Task Management and Orchestration
1. Design task decomposition algorithms
2. Implement task routing and assignment
3. Create workflow execution engine
4. Set up task progress tracking
5. Implement result aggregation

### 4.4 Communication and State Management
1. Set up message passing infrastructure
2. Implement shared state management
3. Create event-driven communication
4. Set up data persistence layer
5. Implement conflict resolution mechanisms

### 4.5 Monitoring and Observability
1. Implement performance metrics collection
2. Set up distributed tracing
3. Create agent health dashboards
4. Implement alerting and notifications
5. Set up log aggregation and analysis

## 5. Core Code Example

### 5.1 Archon Framework Configuration
```python
# src/config/archon_config.py
from pydantic import BaseSettings, Field
from typing import Dict, List, Optional
import os

class ArchonConfig(BaseSettings):
    """Archon framework configuration"""
    
    # Core settings
    environment: str = Field(default="development", env="ARCHON_ENVIRONMENT")
    debug: bool = Field(default=False, env="ARCHON_DEBUG")
    log_level: str = Field(default="INFO", env="ARCHON_LOG_LEVEL")
    
    # Agent settings
    max_concurrent_agents: int = Field(default=10, env="MAX_CONCURRENT_AGENTS")
    agent_timeout: int = Field(default=300, env="AGENT_TIMEOUT")
    agent_retry_attempts: int = Field(default=3, env="AGENT_RETRY_ATTEMPTS")
    agent_heartbeat_interval: int = Field(default=30, env="AGENT_HEARTBEAT_INTERVAL")
    
    # LLM settings
    openai_api_key: str = Field(env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(env="ANTHROPIC_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    anthropic_model: str = Field(default="claude-3-sonnet-20240229", env="ANTHROPIC_MODEL")
    
    # Database settings
    database_url: str = Field(env="DATABASE_URL")
    redis_url: str = Field(env="REDIS_URL")
    
    # Message queue settings
    celery_broker_url: str = Field(env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(env="CELERY_RESULT_BACKEND")
    
    # Security settings
    api_secret_key: str = Field(env="API_SECRET_KEY")
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY")
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    
    # Performance settings
    worker_processes: int = Field(default=4, env="WORKER_PROCESSES")
    worker_connections: int = Field(default=1000, env="WORKER_CONNECTIONS")
    max_requests_per_worker: int = Field(default=1000, env="MAX_REQUESTS_PER_WORKER")
    request_timeout: int = Field(default=60, env="REQUEST_TIMEOUT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global configuration instance
config = ArchonConfig()
```

### 5.2 Base Agent Implementation
```python
# src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import uuid
import structlog

logger = structlog.get_logger()

class AgentCapability(BaseModel):
    """Defines what an agent can do"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    required_tools: List[str] = []
    estimated_duration: Optional[int] = None  # in seconds
    complexity_level: int = Field(ge=1, le=10, default=5)

class AgentMessage(BaseModel):
    """Message structure for agent communication"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    recipient_id: Optional[str] = None  # None for broadcast
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    priority: int = Field(ge=1, le=10, default=5)

class AgentState(BaseModel):
    """Agent state tracking"""
    agent_id: str
    status: str  # idle, busy, error, offline
    current_task_id: Optional[str] = None
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    error_count: int = 0
    total_tasks_completed: int = 0

class TaskResult(BaseModel):
    """Result of task execution"""
    task_id: str
    agent_id: str
    status: str  # success, failure, partial
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseAgent(ABC):
    """Base class for all Archon agents"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.state = AgentState(agent_id=agent_id, status="idle")
        self.capabilities: List[AgentCapability] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        self.logger = logger.bind(agent_id=agent_id, agent_name=name)
        
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute a specific task"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities"""
        pass
    
    async def start(self):
        """Start the agent"""
        self.is_running = True
        self.state.status = "idle"
        self.logger.info("Agent started")
        
        # Start message processing loop
        asyncio.create_task(self._message_processing_loop())
        asyncio.create_task(self._heartbeat_loop())
    
    async def stop(self):
        """Stop the agent"""
        self.is_running = False
        self.state.status = "offline"
        self.logger.info("Agent stopped")
    
    async def send_message(self, message: AgentMessage):
        """Send message to another agent or broadcast"""
        # This would be implemented by the orchestrator
        pass
    
    async def receive_message(self, message: AgentMessage):
        """Receive message from another agent"""
        await self.message_queue.put(message)
    
    async def _message_processing_loop(self):
        """Process incoming messages"""
        while self.is_running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(), 
                    timeout=1.0
                )
                await self._handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error("Error processing message", error=str(e))
    
    async def _handle_message(self, message: AgentMessage):
        """Handle incoming message"""
        self.logger.debug("Received message", message_type=message.message_type)
        
        if message.message_type == "task_assignment":
            await self._handle_task_assignment(message)
        elif message.message_type == "status_request":
            await self._handle_status_request(message)
        elif message.message_type == "shutdown":
            await self.stop()
        else:
            await self._handle_custom_message(message)
    
    async def _handle_task_assignment(self, message: AgentMessage):
        """Handle task assignment"""
        task = message.content.get("task")
        if not task:
            self.logger.error("Invalid task assignment message")
            return
        
        self.state.status = "busy"
        self.state.current_task_id = task.get("id")
        
        try:
            start_time = datetime.utcnow()
            result = await self.execute_task(task)
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            result.execution_time = execution_time
            self.state.total_tasks_completed += 1
            
            # Send result back
            response = AgentMessage(
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type="task_result",
                content={"result": result.dict()},
                correlation_id=message.id
            )
            await self.send_message(response)
            
        except Exception as e:
            self.logger.error("Task execution failed", error=str(e))
            self.state.error_count += 1
            
            error_result = TaskResult(
                task_id=task.get("id", "unknown"),
                agent_id=self.agent_id,
                status="failure",
                error=str(e),
                execution_time=0
            )
            
            response = AgentMessage(
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type="task_result",
                content={"result": error_result.dict()},
                correlation_id=message.id
            )
            await self.send_message(response)
        
        finally:
            self.state.status = "idle"
            self.state.current_task_id = None
    
    async def _handle_status_request(self, message: AgentMessage):
        """Handle status request"""
        response = AgentMessage(
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            message_type="status_response",
            content={
                "state": self.state.dict(),
                "capabilities": [cap.dict() for cap in self.get_capabilities()]
            },
            correlation_id=message.id
        )
        await self.send_message(response)
    
    async def _handle_custom_message(self, message: AgentMessage):
        """Handle custom message types - override in subclasses"""
        self.logger.debug("Unhandled message type", message_type=message.message_type)
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeat"""
        from ..config.archon_config import config
        
        while self.is_running:
            try:
                self.state.last_heartbeat = datetime.utcnow()
                
                heartbeat = AgentMessage(
                    sender_id=self.agent_id,
                    message_type="heartbeat",
                    content={"state": self.state.dict()}
                )
                await self.send_message(heartbeat)
                
                await asyncio.sleep(config.agent_heartbeat_interval)
            except Exception as e:
                self.logger.error("Heartbeat failed", error=str(e))
                await asyncio.sleep(5)  # Retry after 5 seconds
```

### 5.3 Specialized Agent Implementation
```python
# src/agents/code_generation_agent.py
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentCapability, TaskResult
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import ast
import subprocess
import tempfile
import os

class CodeGenerationAgent(BaseAgent):
    """Agent specialized in code generation and analysis"""
    
    def __init__(self, agent_id: str = "code_gen_agent"):
        super().__init__(
            agent_id=agent_id,
            name="Code Generation Agent",
            description="Generates, analyzes, and validates code in multiple programming languages"
        )
        self.llm = OpenAI(temperature=0.1)
        self.supported_languages = ["python", "javascript", "typescript", "java", "go", "rust"]
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="generate_code",
                description="Generate code based on requirements",
                input_schema={
                    "type": "object",
                    "properties": {
                        "requirements": {"type": "string"},
                        "language": {"type": "string", "enum": self.supported_languages},
                        "style": {"type": "string", "default": "clean"},
                        "include_tests": {"type": "boolean", "default": False}
                    },
                    "required": ["requirements", "language"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "explanation": {"type": "string"},
                        "tests": {"type": "string"},
                        "dependencies": {"type": "array", "items": {"type": "string"}}
                    }
                },
                estimated_duration=30,
                complexity_level=7
            ),
            AgentCapability(
                name="analyze_code",
                description="Analyze code for quality, security, and performance",
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "language": {"type": "string"},
                        "analysis_type": {
                            "type": "string", 
                            "enum": ["quality", "security", "performance", "all"]
                        }
                    },
                    "required": ["code", "language"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "issues": {"type": "array"},
                        "suggestions": {"type": "array"},
                        "metrics": {"type": "object"},
                        "score": {"type": "number"}
                    }
                },
                estimated_duration=15,
                complexity_level=6
            ),
            AgentCapability(
                name="refactor_code",
                description="Refactor code for better structure and maintainability",
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "language": {"type": "string"},
                        "refactor_goals": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["code", "language"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "refactored_code": {"type": "string"},
                        "changes_made": {"type": "array"},
                        "improvement_summary": {"type": "string"}
                    }
                },
                estimated_duration=45,
                complexity_level=8
            )
        ]
    
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute code generation task"""
        task_type = task.get("type")
        task_id = task.get("id", "unknown")
        
        try:
            if task_type == "generate_code":
                result = await self._generate_code(task.get("parameters", {}))
            elif task_type == "analyze_code":
                result = await self._analyze_code(task.get("parameters", {}))
            elif task_type == "refactor_code":
                result = await self._refactor_code(task.get("parameters", {}))
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="success",
                result=result,
                execution_time=0  # Will be set by base class
            )
            
        except Exception as e:
            self.logger.error("Code generation task failed", error=str(e))
            return TaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                status="failure",
                error=str(e),
                execution_time=0
            )
    
    async def _generate_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on requirements"""
        requirements = params.get("requirements")
        language = params.get("language")
        style = params.get("style", "clean")
        include_tests = params.get("include_tests", False)
        
        # Create prompt for code generation
        prompt_template = PromptTemplate(
            input_variables=["requirements", "language", "style"],
            template="""
            Generate {style} {language} code that meets the following requirements:
            
            Requirements: {requirements}
            
            Please provide:
            1. Clean, well-documented code
            2. Brief explanation of the approach
            3. List of any dependencies needed
            
            Code:
            """
        )
        
        prompt = prompt_template.format(
            requirements=requirements,
            language=language,
            style=style
        )
        
        # Generate code using LLM
        generated_code = await self.llm.agenerate([prompt])
        code = generated_code.generations[0][0].text.strip()
        
        # Extract code, explanation, and dependencies
        code_parts = self._parse_generated_response(code)
        
        result = {
            "code": code_parts.get("code", code),
            "explanation": code_parts.get("explanation", "Generated code"),
            "dependencies": code_parts.get("dependencies", [])
        }
        
        # Generate tests if requested
        if include_tests:
            test_code = await self._generate_tests(result["code"], language)
            result["tests"] = test_code
        
        # Validate syntax if possible
        if language == "python":
            try:
                ast.parse(result["code"])
                result["syntax_valid"] = True
            except SyntaxError as e:
                result["syntax_valid"] = False
                result["syntax_error"] = str(e)
        
        return result
    
    async def _analyze_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for various aspects"""
        code = params.get("code")
        language = params.get("language")
        analysis_type = params.get("analysis_type", "all")
        
        analysis_result = {
            "issues": [],
            "suggestions": [],
            "metrics": {},
            "score": 0
        }
        
        # Basic syntax check
        if language == "python":
            try:
                ast.parse(code)
                analysis_result["metrics"]["syntax_valid"] = True
            except SyntaxError as e:
                analysis_result["issues"].append({
                    "type": "syntax_error",
                    "message": str(e),
                    "severity": "high"
                })
                analysis_result["metrics"]["syntax_valid"] = False
        
        # Code complexity analysis
        lines_of_code = len([line for line in code.split('\n') if line.strip()])
        analysis_result["metrics"]["lines_of_code"] = lines_of_code
        
        if lines_of_code > 100:
            analysis_result["suggestions"].append({
                "type": "complexity",
                "message": "Consider breaking down large functions into smaller ones",
                "severity": "medium"
            })
        
        # Security analysis (basic)
        if analysis_type in ["security", "all"]:
            security_issues = self._check_security_issues(code, language)
            analysis_result["issues"].extend(security_issues)
        
        # Calculate overall score
        total_issues = len(analysis_result["issues"])
        high_severity = len([i for i in analysis_result["issues"] if i.get("severity") == "high"])
        
        if high_severity > 0:
            analysis_result["score"] = max(0, 50 - (high_severity * 20))
        else:
            analysis_result["score"] = max(0, 100 - (total_issues * 10))
        
        return analysis_result
    
    async def _refactor_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Refactor code for better structure"""
        code = params.get("code")
        language = params.get("language")
        refactor_goals = params.get("refactor_goals", ["improve_readability"])
        
        # Create refactoring prompt
        goals_text = ", ".join(refactor_goals)
        prompt_template = PromptTemplate(
            input_variables=["code", "language", "goals"],
            template="""
            Refactor the following {language} code to achieve these goals: {goals}
            
            Original code:
            {code}
            
            Please provide:
            1. Refactored code
            2. List of changes made
            3. Summary of improvements
            
            Refactored code:
            """
        )
        
        prompt = prompt_template.format(
            code=code,
            language=language,
            goals=goals_text
        )
        
        # Generate refactored code
        refactored_response = await self.llm.agenerate([prompt])
        refactored_text = refactored_response.generations[0][0].text.strip()
        
        # Parse the response
        refactored_parts = self._parse_generated_response(refactored_text)
        
        return {
            "refactored_code": refactored_parts.get("code", refactored_text),
            "changes_made": refactored_parts.get("changes", []),
            "improvement_summary": refactored_parts.get("summary", "Code refactored")
        }
    
    async def _generate_tests(self, code: str, language: str) -> str:
        """Generate test code for the given code"""
        prompt_template = PromptTemplate(
            input_variables=["code", "language"],
            template="""
            Generate comprehensive unit tests for the following {language} code:
            
            {code}
            
            Please provide complete test code with appropriate test framework.
            """
        )
        
        prompt = prompt_template.format(code=code, language=language)
        test_response = await self.llm.agenerate([prompt])
        return test_response.generations[0][0].text.strip()
    
    def _parse_generated_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract different components"""
        # This is a simplified parser - in practice, you'd want more robust parsing
        parts = {}
        
        # Extract code blocks
        import re
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            parts["code"] = code_blocks[0].strip()
        
        # Extract explanations and other parts
        lines = response.split('\n')
        current_section = None
        content = []
        
        for line in lines:
            if line.lower().startswith('explanation:'):
                if current_section:
                    parts[current_section] = '\n'.join(content)
                current_section = 'explanation'
                content = [line.split(':', 1)[1].strip()]
            elif line.lower().startswith('dependencies:'):
                if current_section:
                    parts[current_section] = '\n'.join(content)
                current_section = 'dependencies'
                content = []
            elif current_section:
                content.append(line)
        
        if current_section and content:
            parts[current_section] = '\n'.join(content)
        
        return parts
    
    def _check_security_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Basic security issue detection"""
        issues = []
        
        # Common security patterns to check
        security_patterns = {
            "sql_injection": ["execute(", "query(", "SELECT", "INSERT", "UPDATE", "DELETE"],
            "command_injection": ["os.system", "subprocess.call", "eval(", "exec("],
            "hardcoded_secrets": ["password", "api_key", "secret", "token"]
        }
        
        for issue_type, patterns in security_patterns.items():
            for pattern in patterns:
                if pattern.lower() in code.lower():
                    issues.append({
                        "type": issue_type,
                        "severity": "high" if issue_type != "hardcoded_secrets" else "medium",
                        "pattern": pattern
                    })
        
        return issues

#### 5.3.1 Agent Tool Definition and Usage

Effective agents often rely on a set of tools to perform specific actions, interact with external systems, or process data. Archon agents can be equipped with tools, and their usage should be clearly defined.

**A. Defining a Tool:**

Tools can be defined as classes, often inheriting from a base tool class if using a framework like LangChain, or simply as structured components with clear input and output schemas, typically using Pydantic.

```python
# src/tools/code_execution_tool.py
from pydantic import BaseModel, Field
from typing import Dict, Any
import subprocess
import tempfile
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uvicorn

from ..orchestrator.agent_orchestrator import orchestrator, Task, Workflow
from ..agents.code_generation_agent import CodeGenerationAgent
from ..config.archon_config import config

app = FastAPI(
    title="Archon Agent Framework API",
    description="API for managing and orchestrating AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class TaskRequest(BaseModel):
    type: str
    parameters: Dict[str, Any]
    priority: int = 5
    timeout: int = 300
    dependencies: List[str] = []

class WorkflowRequest(BaseModel):
    name: str
    description: str
    tasks: List[TaskRequest]

class TaskResponse(BaseModel):
    id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the orchestrator and agents"""
    await orchestrator.start()
    
    # Register default agents
    code_agent = CodeGenerationAgent()
    await orchestrator.register_agent(code_agent)
    
    print("Archon Framework API started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await orchestrator.stop()
    print("Archon Framework API stopped")

@app.get("/")
async def root():
    return {"message": "Archon Agent Framework API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": len(orchestrator.agents),
        "tasks": len(orchestrator.tasks),
        "workflows": len(orchestrator.workflows)
    }

@app.get("/agents")
async def list_agents():
    """List all registered agents"""
    agents = []
    for agent_id, agent in orchestrator.agents.items():
        agents.append({
            "id": agent_id,
            "name": agent.name,
            "description": agent.description,
            "status": agent.state.status,
            "capabilities": [cap.dict() for cap in agent.get_capabilities()]
        })
    return agents

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent details"""
    if agent_id not in orchestrator.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = orchestrator.agents[agent_id]
    return {
        "id": agent_id,
        "name": agent.name,
        "description": agent.description,
        "status": agent.state.status,
        "capabilities": [cap.dict() for cap in agent.get_capabilities()],
        "state": agent.state.dict()
    }

@app.post("/tasks", response_model=TaskResponse)
async def submit_task(task_request: TaskRequest):
    """Submit a new task"""
    task = Task(
        type=task_request.type,
        parameters=task_request.parameters,
        priority=task_request.priority,
        timeout=task_request.timeout,
        dependencies=task_request.dependencies
    )
    
    task_id = await orchestrator.submit_task(task)
    return TaskResponse(id=task_id, status="pending")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task status and result"""
    task = await orchestrator.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    response = TaskResponse(
        id=task.id,
        status=task.status
    )
    
    if task.result:
        if task.result.status == "success":
            response.result = task.result.result
        else:
            response.error = task.result.error
    
    return response

@app.get("/tasks")
async def list_tasks(status: Optional[str] = None, limit: int = 100):
    """List tasks with optional filtering"""
    tasks = []
    for task in list(orchestrator.tasks.values())[-limit:]:
        if status and task.status != status:
            continue
        
        task_data = {
            "id": task.id,
            "type": task.type,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "assigned_agent_id": task.assigned_agent_id
        }
        
        if task.completed_at:
            task_data["completed_at"] = task.completed_at.isoformat()
        
        tasks.append(task_data)
    
    return tasks

@app.post("/workflows")
async def submit_workflow(workflow_request: WorkflowRequest):
    """Submit a new workflow"""
    tasks = []
    for task_req in workflow_request.tasks:
        task = Task(
            type=task_req.type,
            parameters=task_req.parameters,
            priority=task_req.priority,
            timeout=task_req.timeout,
            dependencies=task_req.dependencies
        )
        tasks.append(task)
    
    workflow = Workflow(
        name=workflow_request.name,
        description=workflow_request.description,
        tasks=tasks
    )
    
    workflow_id = await orchestrator.submit_workflow(workflow)
    return {"id": workflow_id, "status": "pending"}

@app.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow status"""
    workflow = await orchestrator.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "status": workflow.status,
        "created_at": workflow.created_at.isoformat(),
        "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
        "tasks": [
            {
                "id": task.id,
                "type": task.type,
                "status": task.status,
                "assigned_agent_id": task.assigned_agent_id
            }
            for task in workflow.tasks
        ]
    }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "orchestrator_metrics": orchestrator.metrics,
        "agent_count": len(orchestrator.agents),
        "active_tasks": len([t for t in orchestrator.tasks.values() if t.status in ["pending", "assigned", "running"]]),
        "completed_tasks": len([t for t in orchestrator.tasks.values() if t.status == "completed"]),
        "failed_tasks": len([t for t in orchestrator.tasks.values() if t.status == "failed"])
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        workers=config.worker_processes if not config.debug else 1
    )
```

## 6. Common Pitfalls & Error Handling

### 6.1 Agent Communication Issues
- **Problem**: Messages lost or delayed between agents
- **Solution**: Implement message acknowledgment and retry mechanisms
- **Prevention**: Use reliable message queues (Redis, RabbitMQ)

### 6.2 Task Deadlocks
- **Problem**: Circular dependencies in task workflows
- **Solution**: Implement dependency cycle detection
- **Detection**: Graph analysis of task dependencies

### 6.3 Agent Failure Recovery
- **Problem**: Agents crash or become unresponsive
- **Solution**: Implement health monitoring and automatic restart
- **Prevention**: Use supervisor processes and circuit breakers

### 6.4 Resource Contention
- **Problem**: Multiple agents competing for limited resources
- **Solution**: Implement resource pooling and queuing
- **Optimization**: Use priority-based scheduling

## 7. Performance Optimization

### 7.1 Agent Pool Management
- Implement dynamic agent scaling based on load
- Use agent specialization for better performance
- Implement agent warm-up and caching strategies

### 7.2 Task Scheduling Optimization
- Use priority queues for task management
- Implement load balancing across agents
- Optimize task batching and parallel execution

### 7.3 Communication Optimization
- Use connection pooling for agent communication
- Implement message compression and batching
- Optimize serialization and deserialization

## 8. Integration with Genesis Engine

### 8.1 Multi-Agent Coordination
- Integrate with Genesis agent architecture
- Implement cross-framework agent communication
- Create unified agent registry and discovery

### 8.2 Task Distribution
- Use Archon for complex multi-step workflows
- Implement task decomposition strategies
- Create adaptive task routing based on agent capabilities

### 8.3 Monitoring and Observability
- Integrate with Genesis monitoring systems
- Implement distributed tracing across agents
- Create unified dashboards and alerting

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Set up agent specialization and workflow automation*