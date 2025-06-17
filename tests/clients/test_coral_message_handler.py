import pytest
from src.clients.coral_message_handler import CoralMessageHandler

@pytest.fixture
def handler():
    """Provides an instance of CoralMessageHandler."""
    return CoralMessageHandler()

def test_handler_initialization(handler, mocker):
    """Tests that the handler initializes correctly."""
    # Arrange
    mock_print = mocker.patch('builtins.print')
    
    # Act
    CoralMessageHandler(base_url="http://test.url")

    # Assert
    mock_print.assert_called_once_with("CoralMessageHandler initialized for API endpoint: http://test.url")

def test_create_thread(handler):
    """Tests that create_thread returns a string thread ID."""
    # Act
    thread_id = handler.create_thread(topic="Test Topic")

    # Assert
    assert isinstance(thread_id, str)
    assert len(thread_id) > 0

def test_send_message(handler):
    """Tests that send_message returns True."""
    # Act
    result = handler.send_message(thread_id="test_id", author="test_author", content="test_content")

    # Assert
    assert result is True

def test_get_thread_history(handler):
    """Tests that get_thread_history returns the placeholder list."""
    # Act
    history = handler.get_thread_history(thread_id="test_id")

    # Assert
    assert isinstance(history, list)
    assert len(history) == 1
    assert history[0]['author'] == "system"
