# Multi-Agent Architecture Guide

**ID:** guide:feature:multi_agent_architecture  
**Source Reference(s):** /python agents/Archon  
**Last Validated:** January 2025

## 1. Purpose

Implement a sophisticated multi-agent system using LangGraph and PydanticAI for orchestrating specialized AI agents that collaborate to complete complex software development tasks.

## 2. Key Concepts

- **LangGraph**: Graph-based workflow orchestration for agent coordination
- **PydanticAI**: Type-safe agent definitions with structured outputs
- **State Management**: Centralized state using TypedDict and Pydantic models
- **Agent Coordination**: Event-driven communication between specialized agents
- **Tool Integration**: Shared tool ecosystem across all agents
- **Workflow Orchestration**: Conditional routing and parallel execution patterns

## 3. Required Dependencies

### Python Packages
```python
# Core agent framework
langgraph = "^0.2.0"
pydantic-ai = "^0.0.13"
pydantic = "^2.5.0"

# LLM integration
openai = "^1.0.0"
anthropics = "^0.8.0"

# Database and storage
supabase = "^2.0.0"
sqlalchemy = "^2.0.0"

# Async and utilities
aiohttp = "^3.9.0"
streamlit = "^1.28.0"
python-dotenv = "^1.0.0"

# Development tools
black = "^23.0.0"
mypy = "^1.7.0"
pytest = "^7.4.0"
```

### Environment Variables
```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
EMBEDDING_PROVIDER=OpenAI
EMBEDDING_BASE_URL=https://api.openai.com/v1

# Database Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# Agent Configuration
AGENT_MODEL=gpt-4
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

## 4. Step-by-Step Implementation Plan

### 4.1 State Schema Definition
1. Define TypedDict for workflow state
2. Create Pydantic models for agent inputs/outputs
3. Implement state validation and serialization
4. Set up state persistence mechanisms

### 4.2 Agent Definition with PydanticAI
1. Create base agent class with common functionality
2. Define specialized agents for different domains
3. Implement tool integration and dependency injection
4. Set up agent configuration and model selection

### 4.3 LangGraph Workflow Creation
1. Define graph nodes for each agent
2. Implement conditional routing logic
3. Set up parallel execution patterns
4. Configure error handling and retry mechanisms

### 4.4 Tool Integration System
1. Create shared tool registry
2. Implement tool authentication and permissions
3. Set up tool result caching and optimization
4. Handle tool failures and fallbacks

### 4.5 Communication and Coordination
1. Implement agent-to-agent messaging
2. Set up event-driven coordination patterns
3. Create workflow monitoring and logging
4. Implement human-in-the-loop capabilities

## 5. Core Code Example

### 5.1 State Schema Definition
```python
from typing import TypedDict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentType(str, Enum):
    ARCHITECT = "architect"
    FRONTEND = "frontend"
    BACKEND = "backend"
    TESTER = "tester"
    DEBUGGER = "debugger"

class TaskResult(BaseModel):
    agent_type: AgentType
    status: TaskStatus
    output: Any
    metadata: dict = Field(default_factory=dict)
    timestamp: str
    execution_time: float

class ProjectRequirements(BaseModel):
    description: str
    features: List[str]
    tech_stack: List[str]
    constraints: List[str] = Field(default_factory=list)
    priority: str = "medium"

class WorkflowState(TypedDict):
    """Central state for the multi-agent workflow"""
    project_id: str
    requirements: ProjectRequirements
    current_agent: Optional[AgentType]
    task_results: List[TaskResult]
    generated_code: dict  # file_path -> content
    errors: List[str]
    workflow_status: TaskStatus
    metadata: dict
```

### 5.2 Base Agent Implementation
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from abc import ABC, abstractmethod
import asyncio
from typing import Any, Dict

class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(
        self,
        agent_type: AgentType,
        model: Model,
        tools: List[Any] = None,
        system_prompt: str = ""
    ):
        self.agent_type = agent_type
        self.model = model
        self.tools = tools or []
        
        # Create PydanticAI agent
        self.agent = Agent(
            model=model,
            system_prompt=system_prompt,
            tools=self.tools,
            retries=3
        )
    
    @abstractmethod
    async def execute_task(
        self, 
        state: WorkflowState, 
        context: RunContext
    ) -> TaskResult:
        """Execute the agent's specialized task"""
        pass
    
    async def run_with_context(
        self, 
        prompt: str, 
        context_data: Dict[str, Any]
    ) -> Any:
        """Run agent with contextual information"""
        try:
            result = await self.agent.run(
                prompt,
                message_history=[],
                context=context_data
            )
            return result.data
        except Exception as e:
            raise AgentExecutionError(f"{self.agent_type} failed: {str(e)}")

class AgentExecutionError(Exception):
    """Custom exception for agent execution failures"""
    pass
```

### 5.3 Specialized Agent Implementation
```python
from datetime import datetime
import time

class ArchitectAgent(BaseAgent):
    """Agent responsible for system architecture and planning"""
    
    def __init__(self, model: Model):
        system_prompt = """
        You are an expert software architect. Your role is to:
        1. Analyze project requirements
        2. Design system architecture
        3. Select appropriate technology stack
        4. Create implementation plan
        5. Define component interfaces
        
        Always provide structured, actionable outputs.
        """
        
        super().__init__(
            agent_type=AgentType.ARCHITECT,
            model=model,
            system_prompt=system_prompt,
            tools=[self.analyze_requirements, self.design_architecture]
        )
    
    async def execute_task(
        self, 
        state: WorkflowState, 
        context: RunContext
    ) -> TaskResult:
        """Execute architecture planning task"""
        start_time = time.time()
        
        try:
            # Analyze requirements
            requirements = state["requirements"]
            
            prompt = f"""
            Analyze the following project requirements and create a detailed architecture plan:
            
            Description: {requirements.description}
            Features: {', '.join(requirements.features)}
            Tech Stack: {', '.join(requirements.tech_stack)}
            Constraints: {', '.join(requirements.constraints)}
            
            Provide:
            1. System architecture diagram (text description)
            2. Component breakdown
            3. Technology recommendations
            4. Implementation phases
            5. Risk assessment
            """
            
            result = await self.run_with_context(
                prompt, 
                {"requirements": requirements.dict()}
            )
            
            execution_time = time.time() - start_time
            
            return TaskResult(
                agent_type=self.agent_type,
                status=TaskStatus.COMPLETED,
                output=result,
                metadata={
                    "components_identified": len(result.get("components", [])),
                    "technologies_recommended": len(result.get("technologies", [])),
                    "phases_planned": len(result.get("phases", []))
                },
                timestamp=datetime.now().isoformat(),
                execution_time=execution_time
            )
            
        except Exception as e:
            return TaskResult(
                agent_type=self.agent_type,
                status=TaskStatus.FAILED,
                output={"error": str(e)},
                metadata={},
                timestamp=datetime.now().isoformat(),
                execution_time=time.time() - start_time
            )
    
    async def analyze_requirements(self, requirements: dict) -> dict:
        """Tool for analyzing project requirements"""
        # Implementation for requirement analysis
        return {
            "complexity": "medium",
            "estimated_duration": "2-3 weeks",
            "key_challenges": ["scalability", "security"]
        }
    
    async def design_architecture(self, requirements: dict) -> dict:
        """Tool for designing system architecture"""
        # Implementation for architecture design
        return {
            "pattern": "microservices",
            "components": ["api-gateway", "auth-service", "data-service"],
            "database": "postgresql"
        }

class FrontendAgent(BaseAgent):
    """Agent responsible for frontend development"""
    
    def __init__(self, model: Model):
        system_prompt = """
        You are an expert frontend developer. Your role is to:
        1. Create React components with TypeScript
        2. Implement responsive designs
        3. Integrate with backend APIs
        4. Ensure accessibility and performance
        5. Follow modern React patterns (hooks, context, etc.)
        
        Always generate production-ready, well-documented code.
        """
        
        super().__init__(
            agent_type=AgentType.FRONTEND,
            model=model,
            system_prompt=system_prompt,
            tools=[self.generate_component, self.create_api_integration]
        )
    
    async def execute_task(
        self, 
        state: WorkflowState, 
        context: RunContext
    ) -> TaskResult:
        """Execute frontend development task"""
        start_time = time.time()
        
        try:
            # Get architecture decisions from previous agents
            architecture_result = next(
                (r for r in state["task_results"] 
                 if r.agent_type == AgentType.ARCHITECT),
                None
            )
            
            if not architecture_result:
                raise AgentExecutionError("Architecture planning required first")
            
            prompt = f"""
            Based on the architecture plan, create frontend components:
            
            Architecture: {architecture_result.output}
            Requirements: {state['requirements'].dict()}
            
            Generate:
            1. Main application component
            2. Feature-specific components
            3. API integration layer
            4. Routing configuration
            5. State management setup
            """
            
            result = await self.run_with_context(
                prompt,
                {
                    "architecture": architecture_result.output,
                    "requirements": state["requirements"].dict()
                }
            )
            
            # Update generated code in state
            if "components" in result:
                for component_name, component_code in result["components"].items():
                    state["generated_code"][f"src/components/{component_name}.tsx"] = component_code
            
            execution_time = time.time() - start_time
            
            return TaskResult(
                agent_type=self.agent_type,
                status=TaskStatus.COMPLETED,
                output=result,
                metadata={
                    "components_generated": len(result.get("components", {})),
                    "api_integrations": len(result.get("api_calls", [])),
                    "lines_of_code": sum(len(code.split('\n')) 
                                        for code in result.get("components", {}).values())
                },
                timestamp=datetime.now().isoformat(),
                execution_time=execution_time
            )
            
        except Exception as e:
            return TaskResult(
                agent_type=self.agent_type,
                status=TaskStatus.FAILED,
                output={"error": str(e)},
                metadata={},
                timestamp=datetime.now().isoformat(),
                execution_time=time.time() - start_time
            )
    
    async def generate_component(self, spec: dict) -> str:
        """Tool for generating React components"""
        # Implementation for component generation
        return "// Generated React component code"
    
    async def create_api_integration(self, endpoints: list) -> dict:
        """Tool for creating API integration layer"""
        # Implementation for API integration
        return {"api_client": "// API client code", "hooks": "// Custom hooks"}
```

### 5.4 LangGraph Workflow Definition
```python
from langgraph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import Literal

class MultiAgentWorkflow:
    """LangGraph-based multi-agent workflow orchestrator"""
    
    def __init__(self, agents: Dict[AgentType, BaseAgent]):
        self.agents = agents
        self.graph = self._create_workflow_graph()
    
    def _create_workflow_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        # Add agent nodes
        workflow.add_node("architect", self._run_architect)
        workflow.add_node("frontend", self._run_frontend)
        workflow.add_node("backend", self._run_backend)
        workflow.add_node("tester", self._run_tester)
        workflow.add_node("debugger", self._run_debugger)
        
        # Define workflow edges
        workflow.set_entry_point("architect")
        
        # Conditional routing based on architecture decisions
        workflow.add_conditional_edges(
            "architect",
            self._route_after_architecture,
            {
                "frontend_backend": ["frontend", "backend"],
                "frontend_only": "frontend",
                "backend_only": "backend",
                "error": "debugger"
            }
        )
        
        # Parallel execution for frontend and backend
        workflow.add_edge("frontend", "tester")
        workflow.add_edge("backend", "tester")
        
        # Testing and debugging flow
        workflow.add_conditional_edges(
            "tester",
            self._route_after_testing,
            {
                "success": END,
                "needs_debugging": "debugger",
                "needs_rework": "architect"
            }
        )
        
        workflow.add_conditional_edges(
            "debugger",
            self._route_after_debugging,
            {
                "fixed": "tester",
                "needs_rework": "architect",
                "critical_error": END
            }
        )
        
        return workflow.compile()
    
    async def _run_architect(self, state: WorkflowState) -> WorkflowState:
        """Execute architect agent"""
        agent = self.agents[AgentType.ARCHITECT]
        result = await agent.execute_task(state, {})
        
        state["task_results"].append(result)
        state["current_agent"] = AgentType.ARCHITECT
        
        if result.status == TaskStatus.FAILED:
            state["errors"].append(f"Architecture planning failed: {result.output}")
        
        return state
    
    async def _run_frontend(self, state: WorkflowState) -> WorkflowState:
        """Execute frontend agent"""
        agent = self.agents[AgentType.FRONTEND]
        result = await agent.execute_task(state, {})
        
        state["task_results"].append(result)
        state["current_agent"] = AgentType.FRONTEND
        
        return state
    
    async def _run_backend(self, state: WorkflowState) -> WorkflowState:
        """Execute backend agent"""
        agent = self.agents[AgentType.BACKEND]
        result = await agent.execute_task(state, {})
        
        state["task_results"].append(result)
        state["current_agent"] = AgentType.BACKEND
        
        return state
    
    async def _run_tester(self, state: WorkflowState) -> WorkflowState:
        """Execute testing agent"""
        agent = self.agents[AgentType.TESTER]
        result = await agent.execute_task(state, {})
        
        state["task_results"].append(result)
        state["current_agent"] = AgentType.TESTER
        
        return state
    
    async def _run_debugger(self, state: WorkflowState) -> WorkflowState:
        """Execute debugger agent"""
        agent = self.agents[AgentType.DEBUGGER]
        result = await agent.execute_task(state, {})
        
        state["task_results"].append(result)
        state["current_agent"] = AgentType.DEBUGGER
        
        return state
    
    def _route_after_architecture(
        self, 
        state: WorkflowState
    ) -> Literal["frontend_backend", "frontend_only", "backend_only", "error"]:
        """Route workflow after architecture planning"""
        architect_result = state["task_results"][-1]
        
        if architect_result.status == TaskStatus.FAILED:
            return "error"
        
        # Analyze architecture output to determine routing
        output = architect_result.output
        has_frontend = "frontend" in str(output).lower()
        has_backend = "backend" in str(output).lower() or "api" in str(output).lower()
        
        if has_frontend and has_backend:
            return "frontend_backend"
        elif has_frontend:
            return "frontend_only"
        elif has_backend:
            return "backend_only"
        else:
            return "frontend_backend"  # Default to full stack
    
    def _route_after_testing(
        self, 
        state: WorkflowState
    ) -> Literal["success", "needs_debugging", "needs_rework"]:
        """Route workflow after testing"""
        tester_result = state["task_results"][-1]
        
        if tester_result.status == TaskStatus.COMPLETED:
            # Check if tests passed
            if tester_result.output.get("all_tests_passed", False):
                return "success"
            else:
                return "needs_debugging"
        else:
            return "needs_rework"
    
    def _route_after_debugging(
        self, 
        state: WorkflowState
    ) -> Literal["fixed", "needs_rework", "critical_error"]:
        """Route workflow after debugging"""
        debugger_result = state["task_results"][-1]
        
        if debugger_result.status == TaskStatus.COMPLETED:
            if debugger_result.output.get("issues_resolved", False):
                return "fixed"
            else:
                return "needs_rework"
        else:
            return "critical_error"
    
    async def execute_workflow(
        self, 
        initial_state: WorkflowState
    ) -> WorkflowState:
        """Execute the complete multi-agent workflow"""
        try:
            final_state = await self.graph.ainvoke(initial_state)
            final_state["workflow_status"] = TaskStatus.COMPLETED
            return final_state
        except Exception as e:
            initial_state["workflow_status"] = TaskStatus.FAILED
            initial_state["errors"].append(f"Workflow execution failed: {str(e)}")
            return initial_state
```

### 5.5 Workflow Orchestrator
```python
from pydantic_ai.models import OpenAIModel
import asyncio

class AgentOrchestrator:
    """Main orchestrator for the multi-agent system"""
    
    def __init__(self):
        self.model = OpenAIModel("gpt-4")
        self.agents = self._initialize_agents()
        self.workflow = MultiAgentWorkflow(self.agents)
    
    def _initialize_agents(self) -> Dict[AgentType, BaseAgent]:
        """Initialize all specialized agents"""
        return {
            AgentType.ARCHITECT: ArchitectAgent(self.model),
            AgentType.FRONTEND: FrontendAgent(self.model),
            AgentType.BACKEND: BackendAgent(self.model),
            AgentType.TESTER: TesterAgent(self.model),
            AgentType.DEBUGGER: DebuggerAgent(self.model)
        }
    
    async def create_project(
        self, 
        requirements: ProjectRequirements
    ) -> WorkflowState:
        """Create a new project using the multi-agent workflow"""
        
        # Initialize workflow state
        initial_state: WorkflowState = {
            "project_id": f"project_{int(time.time())}",
            "requirements": requirements,
            "current_agent": None,
            "task_results": [],
            "generated_code": {},
            "errors": [],
            "workflow_status": TaskStatus.PENDING,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "workflow_version": "1.0"
            }
        }
        
        # Execute workflow
        final_state = await self.workflow.execute_workflow(initial_state)
        
        # Save results to database
        await self._save_project_results(final_state)
        
        return final_state
    
    async def _save_project_results(self, state: WorkflowState):
        """Save project results to database"""
        # Implementation for saving to Supabase
        pass

# Usage example
async def main():
    orchestrator = AgentOrchestrator()
    
    requirements = ProjectRequirements(
        description="Create a task management web application",
        features=[
            "User authentication",
            "Task creation and editing",
            "Project organization",
            "Real-time collaboration",
            "Mobile responsive design"
        ],
        tech_stack=["React", "TypeScript", "FastAPI", "PostgreSQL"],
        constraints=["Must be accessible", "Performance optimized"],
        priority="high"
    )
    
    result = await orchestrator.create_project(requirements)
    
    print(f"Project Status: {result['workflow_status']}")
    print(f"Generated Files: {len(result['generated_code'])}")
    print(f"Agents Executed: {len(result['task_results'])}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 6. Common Pitfalls & Error Handling

### 6.1 Agent Communication Failures
- **Problem**: Agents fail to share context properly
- **Solution**: Implement robust state serialization and validation
- **Prevention**: Use Pydantic models for all inter-agent communication

### 6.2 Workflow Deadlocks
- **Problem**: Circular dependencies between agents
- **Solution**: Implement timeout mechanisms and circuit breakers
- **Detection**: Monitor workflow execution times and agent dependencies

### 6.3 Model Rate Limiting
- **Problem**: LLM API rate limits cause workflow failures
- **Solution**: Implement exponential backoff and request queuing
- **Monitoring**: Track API usage and implement cost controls

### 6.4 State Consistency Issues
- **Problem**: Concurrent state modifications cause data corruption
- **Solution**: Use atomic operations and state locking mechanisms
- **Prevention**: Design immutable state updates where possible

## 7. Performance Optimization

### 7.1 Parallel Execution
- Execute independent agents concurrently
- Use asyncio for I/O-bound operations
- Implement agent result caching

### 7.2 Memory Management
- Implement state cleanup for completed workflows
- Use streaming for large outputs
- Monitor memory usage per agent

### 7.3 Model Optimization
- Use appropriate model sizes for different tasks
- Implement prompt caching
- Optimize context window usage

## 8. Integration with Genesis Engine

### 8.1 Streamlit UI Integration
- Real-time workflow progress display
- Interactive agent configuration
- Result visualization and export

### 8.2 Supabase Integration
- Workflow state persistence
- Agent performance analytics
- User session management

### 8.3 WebContainer Integration
- Execute generated code in secure environment
- Real-time preview of agent outputs
- Interactive debugging capabilities

---

*Implementation Status: Ready for Genesis Engine integration*  
*Next Steps: Integrate with WebContainer execution environment and implement UI components*