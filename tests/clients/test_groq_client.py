import pytest
from unittest.mock import MagicMock
from src.clients.groq_client import GroqService

@pytest.fixture
def mock_groq_client(mocker):
    """Mocks the Groq API client."""
    mock_client = MagicMock()
    mocker.patch('src.clients.groq_client.Groq', return_value=mock_client)
    return mock_client

@pytest.fixture
def groq_service(mocker):
    """Provides an instance of GroqService with a mocked environment variable."""
    def mock_os_get(key, default=None):
        if key == 'GROQ_API_KEY':
            return 'fake_api_key'
        return default
    mocker.patch('os.environ.get', side_effect=mock_os_get)
    return GroqService()

def test_get_completion_success(groq_service, mock_groq_client):
    """Tests a successful completion from the Groq API."""
    # Arrange
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a test completion."
    mock_groq_client.chat.completions.create.return_value = mock_response

    # Act
    prompt = "Test prompt"
    result = groq_service.get_completion(prompt)

    # Assert
    assert result == "This is a test completion."
    mock_groq_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )

def test_get_completion_api_error(groq_service, mock_groq_client):
    """Tests the error handling when the Groq API call fails."""
    # Arrange
    mock_groq_client.chat.completions.create.side_effect = Exception("API Error")

    # Act
    result = groq_service.get_completion("Test prompt")

    # Assert
    assert result == "Error: Could not get completion from Groq."

def test_groq_service_no_api_key(mocker):
    """Tests that GroqService raises an error if the API key is not set."""
    # Arrange
    mocker.patch('os.environ.get', return_value=None)

    # Act & Assert
    with pytest.raises(ValueError, match="GROQ_API_KEY environment variable not set."):
        GroqService()
