import os
import pytest
from unittest.mock import patch, MagicMock
from src.clients.e2b_sandbox_tool import run_in_e2b_sandbox, E2BSandboxToolInput

# --- Mocks for E2B SDK ---

class MockLog:
    def __init__(self, line):
        self.line = line

class MockError:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class MockRunResult:
    def __init__(self, logs, error=None):
        self.logs = [MockLog(log) for log in logs]
        self.error = error

class MockSandbox:
    def __init__(self, api_key, on_stdout, on_stderr):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run_code(self, script, language=None):
        if "error" in script:
            return MockRunResult([], error=MockError("RuntimeError", "Something went wrong"))
        return MockRunResult(["Hello from E2B"])

# --- Tests ---

@pytest.fixture
def mock_e2b_sandbox():
    with patch('src.clients.e2b_sandbox_tool.Sandbox', new=MockSandbox) as mock:
        yield mock

@patch.dict(os.environ, {"E2B_API_KEY": "YOUR_E2B_API_KEY_HERE"})
def test_run_python_successfully(mock_e2b_sandbox):
    """Tests successful Python script execution in the E2B sandbox."""
    output_lines = []

    def on_output(line):
        output_lines.append(line)

    input_data = E2BSandboxToolInput(
        script='print("Hello from E2B")',
        on_output=on_output
    )

    result = run_in_e2b_sandbox(input_data)

    assert result == "Hello from E2B"
    # The mock doesn't call on_output, but we test the return value


def test_api_key_missing():
    """Tests that the function raises an error if the API key is not set."""
    with pytest.raises(ValueError, match="E2B_API_KEY environment variable not set."):
        run_in_e2b_sandbox(E2BSandboxToolInput(script='print("test")'))

@patch.dict(os.environ, {"E2B_API_KEY": "YOUR_E2B_API_KEY_HERE"})
def test_execution_with_error(mock_e2b_sandbox):
    """Tests that the function raises an exception when the script fails."""
    input_data = E2BSandboxToolInput(script='raise ValueError("error")')

    with pytest.raises(Exception, match="E2B execution failed: RuntimeError: Something went wrong"):
        run_in_e2b_sandbox(input_data)
