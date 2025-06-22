# 03_17: Fixing Dependency Conflicts and Test Suite Errors

**Date:** 2025-06-23

## 1. Problem Summary

After installing the `supabase` Python package, the test suite began failing. The initial failure was an `ImportError` related to the `httpx` library, which prevented the tests from being collected. After resolving the import error, several new test failures emerged, including a `404 Not Found` error, multiple `AssertionError`s related to datetime string formats, and an `AttributeError` on a Pydantic model.

## 2. Diagnostic Process

1.  **Initial `ImportError`:** The traceback clearly showed a dependency conflict. `e2b==1.5.2` required `httpx>=0.27.0`, while the newly installed `supabase==2.3.0` required `httpx<0.25.0`. The installation of `supabase` had downgraded `httpx` to an incompatible version for `e2b`.
2.  **Test Suite Analysis:** After upgrading both `supabase` and `e2b` to their latest versions to resolve the conflict, a full test run revealed three distinct categories of failures:
    *   `FAILED tests/api/test_agent_endpoints.py::test_read_api_v1_root`: Returned a `404` instead of `200`.
    *   `FAILED tests/api/test_agent_endpoints.py::test_update_agent` & `FAILED tests/api/test_task_endpoints.py::test_update_task`: Both failed on an `AssertionError` when comparing two equivalent ISO 8601 datetime strings (one ending in `Z`, the other in `+00:00`).
    *   `FAILED tests/api/test_task_endpoints.py::test_update_task`: Also raised an `AttributeError: 'TaskUpdate' object has no attribute 'started_at'`, indicating a mismatch between the Pydantic model and the business logic in the persistence layer.

## 3. Resolution Steps

An iterative approach was taken to resolve each failure:

1.  **Dependency Conflict:** Executed `pip install --upgrade supabase e2b` to allow the resolver to find a compatible dependency tree.
2.  **`404` on `/api/v1`:** Added a new root endpoint `@app.get("/api/v1")` in `src/main.py` to satisfy the test's expectation.
3.  **Datetime Assertions:** Modified the failing tests in `tests/api/test_agent_endpoints.py` and `tests/api/test_task_endpoints.py`. Instead of comparing datetime strings directly, the code now parses both the expected and actual timestamp strings into `datetime` objects before the assertion, making the tests robust to formatting variations.
4.  **`AttributeError` on `TaskUpdate`:** Added the missing field `started_at: Optional[datetime] = None` to the `TaskUpdate` class definition in `src/api/models/core_models.py`.

After these changes were applied, a final run of the test suite confirmed that all 28 tests passed successfully.

## 4. Broader Impact

This resolution reinforces the stability of the API layer. It ensures that the Supabase persistence and E2B sandbox features can coexist without dependency issues. The incident also highlights the importance of robust testing practices, such as comparing `datetime` objects rather than their string representations, to avoid fragile tests.
