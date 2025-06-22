from pydantic import BaseModel
from typing import List, Dict, Any

# A simple representation of a file tree, where keys are filenames
# and values can be file content (str) or another dictionary for subdirectories.
FileTree = Dict[str, Any]

class WebContainerToolInput(BaseModel):
    """Input model for the WebContainerTool, defining the project files and commands."""
    files: FileTree
    commands: List[str]

class WebContainerTool:
    """
    A tool for interacting with a WebContainer sandbox environment.

    This class acts as a server-side wrapper. It defines the structure of a
    WebContainer task that can be invoked by an agent. The actual execution
    is handled by the client-side UI, which listens for these tasks.
    """

    def run(self, inputs: WebContainerToolInput) -> Dict[str, Any]:
        """
        Processes the agent's request and returns a structured dictionary
        of instructions for the client-side WebContainer instance.

        Args:
            inputs: An object containing the file tree to mount and the
                    commands to execute.

        Returns:
            A dictionary confirming the dispatch of the task to the client.
        """
        print(f"Dispatching WebContainer task with {len(inputs.files)} files and {len(inputs.commands)} commands.")

        # In a real application, this would likely trigger a WebSocket event
        # to the connected client. For now, it returns a confirmation that
        # the task has been processed on the backend.
        return {
            "status": "success",
            "message": "WebContainer task dispatched to the client for execution.",
            "details": {
                "files_to_mount": list(inputs.files.keys()),
                "commands_to_run": inputs.commands,
            },
        }
