import pytest
from sentient_core.tools.webcontainer_tool import WebContainerTool, WebContainerToolInput

def test_webcontainer_tool_run():
    """Tests that the WebContainerTool correctly processes input and returns a structured response."""
    tool = WebContainerTool()

    # Define a sample input that an agent would provide
    sample_input = WebContainerToolInput(
        files={
            "index.js": "console.log('hello world');",
            "package.json": '{"dependencies": {}}'
        },
        commands=["npm install", "node index.js"]
    )

    # Execute the tool's run method
    result = tool.run(sample_input)

    # Assert that the response is structured as expected
    assert result["status"] == "success"
    assert result["message"] == "WebContainer task dispatched to the client for execution."
    assert isinstance(result["details"], dict)

    details = result["details"]
    assert details["files_to_mount"] == ["index.js", "package.json"]
    assert details["commands_to_run"] == ["npm install", "node index.js"]

def test_webcontainer_tool_run_with_empty_input():
    """Tests the tool's behavior with empty files and commands."""
    tool = WebContainerTool()

    empty_input = WebContainerToolInput(files={}, commands=[])

    result = tool.run(empty_input)

    assert result["status"] == "success"
    assert result["details"]["files_to_mount"] == []
    assert result["details"]["commands_to_run"] == []
