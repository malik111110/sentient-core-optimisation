from dataclasses import dataclass
from typing import Literal, Optional

# Define constants for sandbox types for clarity and to avoid magic strings
SANDBOX_TYPE_E2B = "e2b"
SANDBOX_TYPE_WEB_CONTAINER = "webcontainer"


@dataclass
class SandboxTaskRequirements:
    """Defines the requirements for a task that needs a sandbox environment."""

    # The primary programming language required for the task.
    language: Literal["python", "node", "bash", "javascript"]

    # True if the task's output is a user interface that needs immediate visual feedback.
    requires_ui_feedback: bool = False

    # True if the task must be able to run without a connection to the E2B backend.
    requires_offline: bool = False

    # True if the task handles sensitive data that requires network restrictions.
    is_data_sensitive: bool = False


def choose_sandbox(requirements: SandboxTaskRequirements) -> str:
    """
    Selects the appropriate sandbox environment based on task requirements.

    This function implements the decision tree defined in the technology
    synthesis and integration strategy document.

    Args:
        requirements: An object specifying the needs of the task.

    Returns:
        The recommended sandbox type, either 'e2b' or 'webcontainer'.
    """
    # 1. Does the task need Python or other shell binaries? -> E2B
    if requirements.language in ["python", "bash"]:
        return SANDBOX_TYPE_E2B

    # 4. Is the data sensitive and requires network blocking? -> E2B
    # This check is prioritized over UI/offline needs for security.
    if requirements.is_data_sensitive:
        return SANDBOX_TYPE_E2B

    # 2. Is immediate UI feedback required (and language is Node/JS)? -> WebContainer
    if requirements.requires_ui_feedback:
        return SANDBOX_TYPE_WEB_CONTAINER

    # 3. Is offline usage mandatory? -> WebContainer
    if requirements.requires_offline:
        return SANDBOX_TYPE_WEB_CONTAINER

    # Default case for Node/JS tasks that don't have other specific requirements.
    # WebContainer is often a lighter-weight choice for simple JS execution.
    if requirements.language in ["node", "javascript"]:
        return SANDBOX_TYPE_WEB_CONTAINER

    # Fallback to E2B if no other condition is met, as it's the more powerful option.
    return SANDBOX_TYPE_E2B
