"""Pytest configuration and fixtures for all tests."""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from src.sentient_core.state.db import _db_instance

# Global test configuration
pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(autouse=True)
def mock_db_connection():
    """Mock the SurrealDB connection for all tests."""
    with patch('src.sentient_core.state.db._db_instance', new_callable=AsyncMock) as mock_db:
        # Configure default return values for common DB operations
        mock_db.select.return_value = []
        mock_db.create.return_value = None
        mock_db.update.return_value = None
        mock_db.query.return_value = [{"result": []}]
        
        # Mock the context manager methods
        mock_db.__aenter__.return_value = mock_db
        mock_db.__aexit__.return_value = None
        
        # Set up the global instance for direct imports
        with patch('src.sentient_core.state.db.get_db', return_value=mock_db):
            yield mock_db

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_event_bus():
    """Mock the EventBus for testing."""
    with patch('src.sentient_core.state.event_bus.EventBus', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_state_manager():
    """Mock the StateManager for testing."""
    with patch('src.sentient_core.state.state_manager.StateManager', autospec=True) as mock:
        yield mock
