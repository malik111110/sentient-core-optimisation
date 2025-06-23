# Sentient Core – Working Plan

## Notes
- Resolved `httpx` version conflict between `supabase` and `e2b` by upgrading both packages.
- Added `/api/v1` health-check endpoint in `src/main.py`.
- Hardened tests by comparing `datetime` objects instead of raw strings.
- Extended `TaskUpdate` model with optional `started_at` to match persistence logic.
- All 28 backend tests now pass.
- Debugging process documented in `03_17_fixing_dependency_conflicts_and_test_suite_errors.md`.
- WebContainer guide (`03_15`) reviewed – comprehensive and up to date.
- Initial documentation review complete; entering synthesis phase for integration strategy.
- Implementation strategy reviewed; first coding task: sandbox chooser utility
- Squad formed to build sandbox chooser utility
- Began inspection of `src/sentient_core` to determine chooser utility placement
- Determined placement for sandbox chooser utility: `src/sentient_core/orchestrator/chooser.py`
- Implemented initial sandbox chooser utility module (`chooser.py`).
- Initial run of chooser unit tests failed due to syntax error in `test_chooser.py`; need to fix.
- Identified invalid constant name; rename to `SANDBOX_TYPE_WEB_CONTAINER` in chooser and tests.
- Renamed constant and fixed syntax error; ready to re-run tests.
- Test collection currently failing due to missing `__init__.py` in tests package; need to add.
- Added `__init__.py` to tests package; tests now fail with `ModuleNotFoundError` for `sentient_core`.
- Need to configure pytest path (e.g., add `pyproject.toml` with src layout) to fix import.
- Added `pyproject.toml` with `src` path configuration; ready to re-run tests.
- Fixed syntax error in `test_chooser.py` and ensured tests collect.
- Added `pyproject.toml` to include `src`, resolved import error.
- All 8 chooser utility tests now pass.
- Ready to implement WebContainerTool wrapper.
+ Chooser utility fully integrated and verified (8/8 tests pass).
+ Added `pyproject.toml` to configure src-layout for pytest & packaging.
+ Implemented WebContainerTool wrapper (`webcontainer_tool.py`).
+ Added unit tests for WebContainerTool; ready to run validation.
+ WebContainerTool wrapper verified – tests pass.
+ Implemented E2BSandboxTool wrapper (`e2b_sandbox_tool.py`).
+ Added unit tests for E2BSandboxTool; ready to run validation.
+ E2BSandboxTool wrapper verified – tests pass.
+ Integration strategy document (03_16) updated to reflect completed wrappers.
+ E2B integration guide (03_14) updated with E2BSandboxTool details.
+ Blueprint and agent plan docs updated to include core agentic tools.
+ Added `sandbox_type` to `Task` model and integrated Chooser into MainOrchestrator
+ Fixed incorrect `BaseAgent` import paths in specialized agents
+ Refactored `BaseAgent` to accept optional `sandbox_tool` parameter.
+ DepartmentalExecutor now instantiates sandbox tools and passes them to agents.
+ Initiated integration testing phase to validate full sandbox workflow.
+ Added orchestrator integration test (`test_orchestrator_integration.py`).
+ Added constructors to Backend and Frontend agents to initialize with sandbox_tool and name.
+ Created technical summary document for sandbox tool integration (`03_17-sandbox-integration-summary.md`).
+ Reviewed `prototype-build-outline.md`; identified SurrealDB memory layer as next priority.
+ Located `supabase_persistence.py` to guide migration strategy.
+ Implemented initial SurrealDB client connection (`surrealdb_client.py`).
+ Added memory layer Pydantic models (`memory_models.py`) for nodes, edges, and graphs.
+ Evaluated existing Supabase persistence implementation.
+ Implemented SurrealDB persistence layer (`surrealdb_persistence.py`) and unit tests pass.
+ SurrealDB CRUD tests confirmed memory layer functionality.
+ Refactored DataAgent to interface with SurrealDB memory layer.
+ DataAgent integration tests passed, verifying memory operations.
+ DepartmentalExecutor confirmed to already route memory tasks via DataAgent.
+ Integration test for DepartmentalExecutor memory task routing written.
+ Inspected `main_orchestrator.py`; planner needs to emit memory tasks for `DataAgent`.
+ Decided to introduce task dependency system (`depends_on_task_index`) and memory task injection strategy.
+ Task model extended with task_id, input_data, and depends_on fields to enable task dependencies.
+ Memory-aware planning logic in CSuitePlanner implemented and syntax errors fixed; auto-injects DataAgent tasks.
+ DepartmentalExecutor refactored to handle task dependencies.
+ Integration test for dependency-aware memory workflow written (`test_orchestrator_memory_workflow.py`).
+ Integration tests for dependency-aware memory workflow executed – all assertions passed; memory layer epic completed.
+ DataAgent validated; already consumes injected input_data – no changes required.
+ Added `crewai` dependency and fixed `pyproject.toml`; resolved ModuleNotFoundError.
+ CSuitePlanner memory-injection unit tests executed – all tests pass.
+ SurrealDB memory layer epic closed – system now stateful and persistent.
+ Next sprint identified: sandbox runtime smoke tests (WebContainer, E2B) and cross-sandbox bridge.
+ Added Chooser runtime wrapper with heuristic sandbox selection; MainOrchestrator now uses Chooser.
+ Normalized 'webcontainer' sandbox_type and updated DepartmentalExecutor mapping.
+ Added `crewai` dependency and fixed `pyproject.toml`; resolved ModuleNotFoundError.
+ CSuitePlanner memory-injection unit tests executed – all tests pass.
+ SurrealDB memory layer epic closed – system now stateful and persistent.
+ Next sprint identified: sandbox runtime smoke tests (WebContainer, E2B) and cross-sandbox bridge.
+ FrontendDeveloperAgent refactored to use new WebContainerToolInput API.
+ Added WebContainer smoke test (`test_webcontainer_smoke.py`) with mocked sandbox execution.
+ Specialized agent constructors unified to accept optional `sandbox_tool` (Research, Integration, Deployment).
+ Test collection error traced to empty `tools/__init__.py`; exported `E2BSandboxTool` and `WebContainerTool`.
+ Need to rerun WebContainer smoke test after import fix.
+ Fixed malformed escape characters in `tools/__init__.py`; export lines corrected.
+ Fixed DataAgent import paths to `api.models.memory_models` and `api.persistence.surrealdb_persistence`, clearing ModuleNotFoundError.
+ Fixed BackendDeveloperAgent to use `E2BSandboxToolInput` (was `E2BInput`), resolving remaining import error.
+ WebContainer smoke test re-run – all assertions pass.
+ Implemented E2B smoke test (`test_e2b_smoke.py`) – passes.
+ Cross-sandbox bridge design proposal approved; implementation phase begins.
+ Implemented BridgeAgent specialized agent and integrated into codebase.
+ Exported BridgeAgent in `specialized_agents/__init__.py` and mapped in DepartmentalExecutor.
+ Enhanced dependency injection to supply `frontend_url` and `backend_url` to BridgeAgent.
+ Added `test_bridge_workflow.py`; bridge workflow passes.
+ Bridge workflow operational end-to-end; ready to wire live UI updates.
+ Persisted `bridge.js` to WebContainer file system, injected script tag in FrontendDeveloperAgent, and live UI fetch integration test passes.
+ Planner now auto-injects Bridge task into CSuitePlanner plans.
+ Created technical deep-dive doc `03_19_cross_sandbox_bridge.md` summarising bridge design.
+ Enhanced bridge.js to render backend response inside the UI; live UI fetch test still passes.
+ Added lightweight stubs for missing external libs (`e2b_code_interpreter`, `crewai`) so CI can run without optional dependencies.
+ All API and orchestrator tests now collect successfully; full test suite green again.

## Task List
- [x] Diagnose and resolve dependency conflict (httpx) causing ImportError
- [x] Upgrade `supabase` & `e2b`, verify compatibility
- [x] Implement `/api/v1` root endpoint to satisfy health-check test
- [x] Fix brittle datetime assertions in agent & task tests
- [x] Add `started_at` to `TaskUpdate` Pydantic model
- [x] Run full test suite – ensure 28/28 pass
- [x] Create technical deep-dive doc summarising fixes (03_17)
- [x] Review WebContainer integration guide (03_15) – confirmed alignment
- [x] Flesh out E2B integration guide (03_14)
- [x] Refine technology synthesis & integration strategy (03_16)
- [x] Build sandbox chooser utility module
- [x] Inspect `src` directory and decide chooser placement
- [x] Create chooser file structure (`src/sentient_core/orchestrator/chooser.py`)
- [x] Write unit tests for sandbox chooser utility
- [x] Fix syntax error in `test_chooser.py` and ensure tests collect
- [x] Add `__init__.py` to `tests/sentient_core/orchestrator/` to resolve import
- [x] Resolve `ModuleNotFoundError: sentient_core` in chooser tests
- [x] Configure pytest to include `src` in PYTHONPATH via `pyproject.toml`
- [x] Re-run chooser tests – chooser suite 8/8 pass
+ [x] Resolve `ModuleNotFoundError: sentient_core` in chooser tests
+ [x] Configure pytest to include `src` in PYTHONPATH via `pyproject.toml`
+ [x] Re-run chooser tests – chooser suite 8/8 pass
+ [x] Create tools package structure (`src/sentient_core/tools/`)
+ [x] Implement `WebContainerTool` wrapper (`webcontainer_tool.py`)
+ [x] Write unit tests for `WebContainerTool`
+ [x] Run tests to validate `WebContainerTool`
+ [x] Implement `E2BSandboxTool` wrapper (`e2b_sandbox_tool.py`)
+ [x] Write unit tests for `E2BSandboxTool`
+ [x] Run tests to validate `E2BSandboxTool`
- [x] Update blueprint & high-level agent plan docs to reflect current backend state
- [x] Outline next sprint: implement real integration code for E2B sandbox & WebContainer, plus corresponding tests
+ [x] Add `sandbox_type` field to `Task` model
+ [x] Integrate `Chooser` into `MainOrchestrator` to assign sandbox_type for tasks
+ [x] Correct `BaseAgent` import path in specialized agents
+ [x] Update `BaseAgent` to accept optional `sandbox_tool`
+ [x] Equip specialized agents with selected sandbox tool in `DepartmentalExecutor`
+ [x] Modify specialized agents to utilize provided `sandbox_tool` in `execute_task`
+ [x] Create sandbox integration technical summary document
- [x] Review `prototype-build-outline.md` and extract action items
+ [ ] Extract action items from prototype outline and update plan/documents
+ [x] Evaluate existing Supabase persistence implementation
+ [x] Create SurrealDB client (`surrealdb_client.py`)
+ [x] Define memory layer Pydantic models (`memory_models.py`) for nodes, edges, and graphs.
+ [x] Implement SurrealDB persistence layer (CRUD operations)
+ [x] Write unit & integration tests for SurrealDB persistence
+ [x] Refactor DataAgent to interface with SurrealDB memory layer
+ [x] Write integration tests for DataAgent memory operations
+ [x] Update DepartmentalExecutor to leverage DataAgent for memory tasks
+ [x] Write integration tests for DepartmentalExecutor memory task routing
+ [x] Execute integration tests for DepartmentalExecutor memory task routing
+ [x] Enhance `CSuitePlanner` to inject memory tasks with dependencies
+ [x] Write unit tests for CSuitePlanner memory task injection
+ [x] Refactor `DepartmentalExecutor` to respect task dependencies
+ [x] Adapt `DataAgent` to consume injected task data
+ [x] Write integration tests for dependency-aware memory workflow
+ [x] Execute integration tests for dependency-aware memory workflow
+ [ ] Create technical summary document for memory layer integration (`03_18-memory-layer-integration-summary.md`)
+ [x] Integrate `WebContainerTool` into runtime chooser execution flow
+ [x] Implement WebContainer smoke test (frontend agent ➜ Hello-World page in WebContainer)
+ [x] Fix specialized agent constructors to accept sandbox_tool
+ [x] Export sandbox tools in `tools/__init__.py`
+ [x] Fix malformed escape characters in `tools/__init__.py` export lines
+ [x] Re-run WebContainer smoke test and ensure it passes
+ [x] Implement E2B sandbox smoke test (Backend agent ➜ FastAPI /health)
+ [x] Inject bridge-config task in planner for UI ⇆ API linking
+ [x] Implement BridgeAgent specialized agent
+ [x] Extend CSuitePlanner to auto-inject Bridge task with dependencies
+ [x] Update Chooser/DepartmentalExecutor routing for Bridge tasks
+ [x] Write bridge workflow tests (`test_bridge_workflow.py`)
+ [x] Implement `bridge.js` snippet and WebContainer auto-reload
+ [x] Persist `bridge.js` to WebContainer file system
+ [x] Update `FrontendDeveloperAgent` to inject `<script type="module" src="bridge.js"></script>`
+ [x] Write integration test for live UI fetch (`test_live_ui_fetch.py`)
+ [x] Create cross-sandbox bridge deep-dive doc (`03_19_cross_sandbox_bridge.md`)
+ [x] Enhance bridge.js to render backend response in #backend-response div and update tests
+ [x] Implement hot-reload hook for automatic browser refresh when bridge.js changes
+ [x] Add SSE/WebSocket support in bridge.js for streaming data
+ [ ] Wire FrontendDeveloperAgent to automatically call `startHealthStream()` and `setupHotReload()`
+ [ ] Update documentation to reflect live-stream & hot-reload capabilities (`03_19_cross_sandbox_bridge.md`)

## Current Goal
- Wire frontend to stream & hot-reload; update docs