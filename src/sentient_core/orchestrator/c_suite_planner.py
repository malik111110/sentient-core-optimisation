# C-Suite Planner Agent using CrewAI

import json
try:
    from crewai import Agent, Task as CrewTask, Crew, Process  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    class _Stub:
        def __init__(self, *args, **kwargs):
            pass
    Agent = _Stub  # type: ignore
    CrewTask = _Stub  # type: ignore
    Crew = _Stub  # type: ignore
    class Process:  # type: ignore
        sequential = "sequential"
from .shared_state import Task # Renamed crewai.Task to avoid conflict
# from langchain_community.llms import Ollama # Example, replace with actual LLM

# Placeholder for LLM - replace with actual LLM integration later
# For now, we'll mock the LLM's behavior within the agent's execution
# llm = Ollama(model="openhermes") # Example

class CSuitePlanner:
    def __init__(self):
        self.project_architect_agent = Agent(
            role='Chief Project Architect',
            goal='Deconstruct a high-level user command into a detailed, actionable project plan. ' \
                 'The plan should identify key development phases, assign tasks to appropriate departments, ' \
                 'and define clear deliverables for each task. The output must be a structured JSON object.',
            backstory=(
                "As the Chief Project Architect of the Sentient-Core Agentic Factory, you are the first point of contact "
                "for any new project initiative. Your unparalleled ability to quickly grasp complex requirements and "
                "translate them into a comprehensive, phased execution strategy is legendary. You ensure that every "
                "project starts with a clear roadmap, enabling the departmental agents to work efficiently and in concert."
            ),
            verbose=True,
            allow_delegation=False,
            # llm=llm # Assign the LLM here when ready
        )

    def create_plan(self, command: str) -> dict:
        print(f"C-Suite Planner: Received command - '{command}'. Initiating planning sequence...")

        planning_task = CrewTask(
            description=f'Analyze the following user command and generate a detailed project plan: "{command}". ' \
                        'The plan must include a project_name (a concise, catchy name derived from the command) ' \
                        'and a list of tasks. Each task must specify a department (e.g., Research, Data, Development, Deployment) ' \
                        'and a detailed task description. Format the output as a JSON object.',
            expected_output='A JSON object representing the project plan, with keys "project_name" and "tasks". ' \
                            'The "tasks" key should hold a list of objects, each with "department" and "task" keys.',
            agent=self.project_architect_agent
        )

        planning_crew = Crew(
            agents=[self.project_architect_agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=True
        )

        # For now, since we don't have a live LLM, we'll mock the result
        # In a real scenario, you would call: result = planning_crew.kickoff()
        print("C-Suite Planner: [MOCK] CrewAI kickoff. Simulating plan generation...")
        mock_plan_json_string = '''
        {
            "project_name": "PharmaPulse Competitive Intel Dashboard",
            "tasks": [
                {"department": "Research", "task": "Identify key competitors and their market positioning in the pharma sector related to the user's focus."},
                {"department": "Research", "task": "Gather publicly available data on clinical trials, drug pipelines, and financial performance for these competitors."},
                {"department": "Data", "task": "Clean, process, and structure the gathered data into a relational format suitable for analysis and API access."},
                {"department": "BackendDevelopment", "task": "Design and implement a FastAPI backend with endpoints for accessing the processed competitive intelligence data."},
                {"department": "FrontendDevelopment", "task": "Develop a Next.js and DaisyUI frontend to display the competitive intelligence data, including interactive charts and tables."},
                {"department": "Integration", "task": "Integrate the Phi-3 LLM for on-demand summarization of competitor profiles and Q&A on the dashboard."},
                {"department": "Integration", "task": "Integrate sherpa-onnx for voice command capabilities to navigate and query the dashboard."},
                {"department": "Deployment", "task": "Package and deploy the full PharmaPulse application to Vultr cloud infrastructure."}
            ]
        }
        '''
        
        try:
            # Simulating the LLM's structured JSON output
            raw_plan = json.loads(mock_plan_json_string)
            enhanced_tasks = []
            tasks_to_add_later = []

            # Create Pydantic Task objects to assign UUIDs
            original_tasks = [Task(**t) for t in raw_plan.get("tasks", [])]

            for task in original_tasks:
                enhanced_tasks.append(task)
                # If a task is for research, create a follow-up data task
                if task.department == "Research":
                    data_task = Task(
                        department="Data",
                        task=f"Create memory node from findings of task: '{task.task[:30]}...'",
                        depends_on=[task.task_id],
                        input_data={"node_type": "CONCEPT"}
                    )
                    tasks_to_add_later.append(data_task)
            
            enhanced_tasks.extend(tasks_to_add_later)

            # --- Cross-sandbox bridge injection ---
            frontend_task = next((t for t in enhanced_tasks if t.department == "FrontendDevelopment"), None)
            backend_task = next((t for t in enhanced_tasks if t.department == "BackendDevelopment"), None)
            if frontend_task and backend_task:
                bridge_task = Task(
                    department="Bridge",
                    task="Connect frontend & backend sandboxes",
                    depends_on=[frontend_task.task_id, backend_task.task_id],
                    input_data={},
                    sandbox_type="e2b",
                )
                enhanced_tasks.append(bridge_task)

            # Convert tasks back to dictionaries for the final plan
            raw_plan['tasks'] = [t.model_dump(mode='json') for t in enhanced_tasks]

            print("C-Suite Planner: Plan successfully generated and enhanced with memory tasks (mocked).")
            return raw_plan
        except json.JSONDecodeError as e:
            print(f"C-Suite Planner: Error decoding mock JSON plan: {e}")
            # Fallback to a simpler mock plan in case of error with the complex one
            return {
                "project_name": "FallbackProject",
                "tasks": [
                    {"department": "ErrorHandling", "task": "Investigate plan generation failure."}
                ]
            }
