# Supabase Persistence Layer Refactor

Date: $(date +%Y-%m-%d)
Author: Cascade

## 1. Overview

This document details the refactoring of the persistence layer in the Sentient Core project from an in-memory solution to utilize Supabase as the backend database. This change affects how Agent and Task data is created, read, updated, and deleted (CRUD operations).

## 2. Changes Implemented

### 2.1. File Renaming and Imports

*   `src/api/persistence/in_memory_db.py` was renamed to `src/api/persistence/supabase_persistence.py`.
*   API routers (`agent_router.py`, `task_router.py`) were updated to import from the new `supabase_persistence.py` module.

### 2.2. Supabase Client Integration

*   The `supabase_client` (initialized in `src/clients/supabase_client.py`) is now imported and used in `supabase_persistence.py` for all database interactions.
*   The in-memory dictionaries (`db_agents`, `db_tasks`) were removed.

### 2.3. Refactored CRUD Functions

All CRUD functions for both Agents and Tasks within `supabase_persistence.py` were rewritten to interact with Supabase tables (`agents` and `tasks` respectively).

**General Changes:**
*   **Data Serialization**: UUIDs are converted to strings for Supabase compatibility (e.g., `str(agent_id)`).
*   **Enum Handling**: Enum members (e.g., `AgentStatus.ACTIVE`) are converted to their string values (e.g., `AgentStatus.ACTIVE.value`) before database operations.
*   **Datetime Formatting**: `datetime` objects are converted to ISO 8601 string format for Supabase (e.g., `now.isoformat()`).
*   **Return Types**: Functions that perform create, update, or delete operations now generally return `Optional[ModelType]` (e.g., `Optional[AgentRead]`) to account for potential database errors or not-found scenarios.
*   **Error Handling**: Basic `try-except` blocks and print statements for errors were added to aid in debugging Supabase client interactions.

**Agent CRUD Specifics:**
*   `create_agent`: Inserts a new agent record into the `agents` table.
*   `get_agent`: Selects a single agent by `agent_id`.
*   `get_agents`: Selects a list of agents with pagination (`range`).
*   `update_agent`: Updates an existing agent record by `agent_id`.
*   `delete_agent`: Deletes an agent record by `agent_id` after fetching it.

**Task CRUD Specifics:**
*   `create_task`: Inserts a new task record into the `tasks` table. `agent_id` is stored as a string if present. `started_at` and `completed_at` are omitted if `None` during creation.
*   `get_task`: Selects a single task by `task_id`.
*   `get_tasks`: Selects a list of tasks, optionally filtered by `agent_id`, with pagination.
*   `update_task`: Updates an existing task. Includes logic to set `started_at` and `completed_at` timestamps based on `TaskStatus` transitions if not explicitly provided in the update payload.
*   `delete_task`: Deletes a task record by `task_id` after fetching it.

## 3. Prerequisites for Supabase

*   **Environment Variables**: `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` must be correctly set in the environment.
*   **Database Schema**: 
    *   An `agents` table is required with columns matching the `AgentRead` Pydantic model.
    *   A `tasks` table is required with columns matching the `TaskRead` Pydantic model.
    *   Appropriate data types must be used (e.g., `UUID` for IDs, `TIMESTAMPTZ` for timestamps, `TEXT` or `VARCHAR` for strings, `JSONB` for complex types like `capabilities` or `input_data`).

## 4. Impact

*   The application now relies on an external Supabase instance for data persistence, making data durable across application restarts.
*   API endpoint tests will need to be adapted to work with the new Supabase backend, either by using a live test database or by extensively mocking the `supabase_client`.

## 5. Next Steps

*   Verify Supabase table schemas and RLS policies.
*   Adapt all relevant unit and integration tests for the API endpoints to use or mock the Supabase persistence layer.
