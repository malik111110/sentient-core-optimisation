import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from src.sentient_core.orchestrator.main_orchestrator import MainOrchestrator
from src.sentient_core.orchestrator.shared_state import Task, Plan
from src.api.models.memory_models import MemoryNode, NodeType, SurrealID

@patch('src.sentient_core.orchestrator.main_orchestrator.CSuitePlanner')
@patch('src.sentient_core.orchestrator.departmental_executors.ResearchAgent')
@patch('src.sentient_core.specialized_agents.data_agent.create_node')
def test_full_memory_workflow(mock_create_node, mock_research_agent, mock_planner):
    """Verify the full workflow from planning to memory creation with dependencies."""
    # Arrange
    # 1. Mock the Planner to return a plan with a dependency
    research_task_id = uuid4()
    mock_plan = Plan(
        project_name="Test Memory Project",
        tasks=[
            Task(task_id=research_task_id, department="Research", task="Find the capital of France."),
            Task(department="Data", task="Store research findings.", depends_on=[research_task_id], input_data={"node_type": "CONCEPT"})
        ]
    )
    mock_planner.return_value.create_plan.return_value = mock_plan.model_dump()

    # 2. Mock the ResearchAgent to return a result with an artifact
    mock_research_instance = mock_research_agent.return_value
    mock_research_instance.execute_task.return_value = {
        "status": "completed",
        "message": "Research complete.",
        "artifacts": ["The capital of France is Paris."]
    }

    # 3. Mock the DataAgent's persistence layer
    async def async_create_node(node: MemoryNode):
        assert node.content == "The capital of France is Paris."
        return MemoryNode(id=SurrealID("memory_node:final_id"), **node.model_dump())
    mock_create_node.side_effect = async_create_node

    # 4. Instantiate the Orchestrator
    with patch('src.sentient_core.tools.E2BSandboxTool'), patch('src.sentient_core.tools.WebContainerTool'):
        orchestrator = MainOrchestrator(command="Test command")
        orchestrator.planner = mock_planner()

    # Act
    orchestrator.run()

    # Assert
    # Verify that the DataAgent's create_node was called, which is the final step
    mock_create_node.assert_called_once()
    
    # Check the final state for completion
    assert len(orchestrator.state.completed_tasks) == 2
    data_task_result = next(t for t in orchestrator.state.completed_tasks if t.department == 'Data')
    assert data_task_result.status == 'completed'
