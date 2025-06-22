import os
from e2b_code_interpreter import Sandbox
from typing import List, Optional, Callable


class E2BSandboxToolInput:
    """Input payload for executing tasks inside an E2B sandbox."""

    def __init__(
        self,
        script: str,
        language: str = "python",
        on_output: Optional[Callable[[str], None]] = None,
    ):
        self.script = script
        self.language = language
        self.on_output = on_output


def run_in_e2b_sandbox(input_data: E2BSandboxToolInput) -> str:
    """Spawns an E2B sandbox, executes a script, and returns the output."""
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        raise ValueError("E2B_API_KEY environment variable not set.")

    try:
        with Sandbox(
            api_key=api_key,
            on_stdout=input_data.on_output,
            on_stderr=input_data.on_output,
        ) as sandbox:
            if input_data.language == "python":
                result = sandbox.run_code(input_data.script)
            elif input_data.language == "node":
                # E2B's run_node is basic; for complex projects, use shell commands
                result = sandbox.run_code(input_data.script, language="javascript")
            else:
                raise ValueError(f"Unsupported language: {input_data.language}")

            # The `run_...` methods in the Python SDK are blocking and return a result object.
            # The result object contains stdout, stderr, and any errors.
            if result.error:
                raise Exception(f"E2B execution failed: {result.error.name}: {result.error.value}")

            return "\n".join(log.line for log in result.logs)

    except Exception as e:
        # Broad exception to catch sandbox creation failures, timeouts, etc.
        if input_data.on_output:
            input_data.on_output(f"E2B Sandbox Error: {e}")
        raise
