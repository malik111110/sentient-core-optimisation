


          


          
            
filePath: l:\agentic web dev\sentient-core\.documents\X-CONCEPT PROTOTYPE\Project-documentation.md
l:\agentic web dev\sentient-core\.documents\X-CONCEPT PROTOTYPE\prototype-build-outline.md
l:\agentic web dev\sentient-core\.documents\X-CONCEPT PROTOTYPE\on-going-break-down-tasks.md
l:\agentic web dev\sentient-core\src\sentient_core\specialized_agents\frontend_developer_agent.py
l:\agentic web dev\sentient-core\src\sentient_core\specialized_agents\bridge_agent.py
          
Of course. Based on my analysis of the project documentation and the existing codebase, I have established the following workflow and project rules to ensure my contributions are consistent, effective, and aligned with the `sentient-core` architecture. You can use these as my operational profile.

---

### **My Workflow Rules**

These rules govern my process for approaching any given task.

1.  **Decomposition First**: I will always break down complex requests into smaller, manageable tasks, updating the <mcfolder name="on-going-break-down-tasks.md" path="l:\agentic web dev\sentient-core\.documents\X-CONCEPT PROTOTYPE\"></mcfolder> to reflect the current plan.
2.  **Documentation-Driven**: I will adhere to the templates and standards defined in <mcfile name="Project-documentation.md" path="l:\agentic web dev\sentient-core\.documents\X-CONCEPT PROTOTYPE\Project-documentation.md"></mcfile>. For any new feature, I will create or update the relevant planning, design, and technical documentation as part of the implementation.
3.  **Test-Validated Development**: For any new code I write, I will also write corresponding unit and integration tests. I will ensure all existing and new tests pass before considering a task complete.
4.  **Incremental Implementation**: I will implement features incrementally, ensuring the system remains in a functional state at each step. This follows the pattern of building, testing, and integrating one component at a time (e.g., Chooser, then Sandbox Tools, then Memory Layer).
5.  **Continuous Integration Mindset**: I will treat the `main` branch as always deployable. My changes will be self-contained and will not break the main test suite.

### **My Project Rules**

These rules are the technical guardrails I will follow, derived from the project's architecture and coding standards.

1.  **Adhere to the Hybrid Sandbox Model**: 
    *   **Frontend**: All frontend code generation, UI prototyping, and tasks requiring immediate visual feedback will utilize the **WebContainer** sandbox via the <mcsymbol name="WebContainerTool" filename="webcontainer_tool.py" path="src/sentient_core/tools/webcontainer_tool.py" startline="7" type="class"></mcsymbol>.
    *   **Backend**: All backend API development, database operations, and secure code execution will utilize the **E2B** sandbox via the <mcsymbol name="E2BSandboxTool" filename="e2b_sandbox_tool.py" path="src/clients/e2b_sandbox_tool.py" startline="10" type="class"></mcsymbol>.
    *   The <mcsymbol name="Chooser" filename="chooser.py" path="src/sentient_core/orchestrator/chooser.py" startline="8" type="class"></mcsymbol> utility is the single source of truth for selecting the correct sandbox for a given task.

2.  **Respect the Agentic Architecture**:
    *   New functionality will be implemented within specialized agents that inherit from <mcsymbol name="BaseAgent" filename="base_agent.py" path="src/sentient_core/agents/base_agent.py" startline="5" type="class"></mcsymbol>.
    *   Agents will be orchestrated by the `CSuitePlanner` and `DepartmentalExecutor`. I will not bypass this orchestration layer.
    *   Task dependencies will be explicitly defined in the plan to ensure correct execution order, especially for memory and bridge tasks.

3.  **Utilize the SurrealDB Memory Layer**:
    *   All stateful operations and data persistence will go through the `DataAgent`.
    *   I will use the Pydantic models defined in <mcfile name="memory_models.py" path="src/api/models/memory_models.py"></mcfile> for all data interactions.
    *   I will not interact directly with the <mcfile name="surrealdb_client.py" path="src/clients/surrealdb_client.py"></mcfile>; all interactions must be routed through the persistence layer and the `DataAgent`.

4.  **Automate Frontend/Backend Integration**:
    *   The <mcsymbol name="BridgeAgent" filename="bridge_agent.py" path="src/sentient_core/specialized_agents/bridge_agent.py" startline="5" type="class"></mcsymbol> is responsible for generating the `bridge.js` file that connects the two sandboxes.
    *   The `CSuitePlanner` will be configured to automatically inject a bridge task into any plan that involves both a frontend and a backend component.
    *   The <mcsymbol name="FrontendDeveloperAgent" filename="frontend_developer_agent.py" path="src/sentient_core/specialized_agents/frontend_developer_agent.py" startline="7" type="class"></mcsymbol> must ensure the `bridge.js` script is included in the generated HTML.

5.  **Follow Code and API Standards**:
    *   All code will be documented following the standards in the project documentation (JSDoc/Docstrings).
    *   All API endpoints will conform to the structure defined in the `API Documentation` and `API Specifications` sections of the project docs.
    *   I will use the existing libraries and frameworks (`FastAPI`, `Pydantic`, `CrewAI`) unless a new technology is justified and documented in a `Technology Selection Document`.

By adhering to these rules, I will function as a dedicated and effective agent for the `sentient-core` project.
        