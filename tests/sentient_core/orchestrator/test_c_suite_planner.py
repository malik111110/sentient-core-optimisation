import pytest
from unittest.mock import patch

from src.sentient_core.orchestrator.c_suite_planner import CSuitePlanner

@patch('crewai.Crew.kickoff') # We don't need the crew to actually run
def test_planner_injects_memory_task_with_dependency(mock_kickoff):
    """Verify that the CSuitePlanner correctly injects a Data task with a dependency for a Research task."""
    # Arrange
    planner = CSuitePlanner()
    command = "Create a report on AI trends."
    
    # Mock the return value of the planning crew
    mock_plan_json_string = '''
    {
        "project_name": "AI Trend Report",
        "tasks": [
            {"department": "Research", "task": "Gather data on the latest AI trends."},
            {"department": "BackendDevelopment", "task": "Build an API for the report."}
        ]
    }
    '''
    mock_kickoff.return_value = mock_plan_json_string

    # Act
    final_plan = planner.create_plan(command)

    # Assert
    tasks = final_plan.get('tasks', [])
    
    # 1. Check that the total number of tasks is correct (original + injected)
    assert len(tasks) == 3, "A memory task should have been added."

    # 2. Find the original research task and the new data task
    research_tasks = [t for t in tasks if t['department'] == 'Research']
    data_tasks = [t for t in tasks if t['department'] == 'Data']
    
    assert len(research_tasks) == 1, "There should be one research task."
    assert len(data_tasks) == 1, "A data task should have been injected."
    
    research_task = research_tasks[0]
    data_task = data_tasks[0]

    # 3. Verify the dependency
    assert data_task['depends_on'] is not None, "The data task should have a dependency."
    assert isinstance(data_task['depends_on'], list), "depends_on should be a list."
    assert data_task['depends_on'][0] == research_task['task_id'], "The data task should depend on the research task."

    # 4. Verify the data task's input data
    assert data_task['input_data'] == {"node_type": "CONCEPT"}, "The input_data for the data task is incorrect."
