import pytest
from sentient_core.tools.e2b_sandbox_tool import E2BSandboxTool, E2BSandboxToolInput

def test_e2b_sandbox_tool_run_python():
    """Tests that the E2BSandboxTool correctly processes a Python script request."""
    tool = E2BSandboxTool()

    # Define a sample input for a Python script
    sample_input = E2BSandboxToolInput(
        language='python',
        script='print("Hello from E2B")'
    )

    # Execute the tool's run method
    result = tool.run(sample_input)

    # Assert that the response is structured as expected
    assert result["status"] == "success"
    assert result["message"] == "E2B sandbox task dispatched for execution."
    assert isinstance(result["details"], dict)

    details = result["details"]
    assert details["language"] == "python"
    assert details["script_length"] == len(sample_input.script)
    assert "sandbox_id" in details

def test_e2b_sandbox_tool_run_node():
    """Tests that the E2BSandboxTool correctly processes a Node.js script request."""
    tool = E2BSandboxTool()

    # Define a sample input for a Node.js script
    sample_input = E2BSandboxToolInput(
        language='node',
        script='console.log("Hello from E2B");'
    )

    # Execute the tool's run method
    result = tool.run(sample_input)

    # Assert that the response is structured as expected
    assert result["status"] == "success"
    details = result["details"]
    assert details["language"] == "node"
    assert details["script_length"] == len(sample_input.script)
