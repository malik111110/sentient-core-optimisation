import pytest
from sentient_core.orchestrator.chooser import (
    choose_sandbox,
    SandboxTaskRequirements,
    SANDBOX_TYPE_E2B,
    SANDBOX_TYPE_WEB_CONTAINER,
)


def test_choose_sandbox_for_python_returns_e2b():
    """Test that a task requiring Python correctly chooses E2B."""
    requirements = SandboxTaskRequirements(language="python")
    assert choose_sandbox(requirements) == SANDBOX_TYPE_E2B


def test_choose_sandbox_for_bash_returns_e2b():
    """Test that a task requiring Bash correctly chooses E2B."""
    requirements = SandboxTaskRequirements(language="bash")
    assert choose_sandbox(requirements) == SANDBOX_TYPE_E2B


def test_choose_sandbox_for_sensitive_data_returns_e2b():
    """Test that a Node.js task with sensitive data correctly chooses E2B for security."""
    requirements = SandboxTaskRequirements(language="node", is_data_sensitive=True)
    assert choose_sandbox(requirements) == SANDBOX_TYPE_E2B


def test_choose_sandbox_for_ui_feedback_returns_webcontainer():
    """Test that a Node.js task requiring UI feedback chooses WebContainer."""
    requirements = SandboxTaskRequirements(language="node", requires_ui_feedback=True)
    assert choose_sandbox(requirements) == SANDBOX_TYPE_WEB_CONTAINER


def test_choose_sandbox_for_offline_mode_returns_webcontainer():
    """Test that a JavaScript task requiring offline mode chooses WebContainer."""
    requirements = SandboxTaskRequirements(language="javascript", requires_offline=True)
    assert choose_sandbox(requirements) == SANDBOX_TYPE_WEB_CONTAINER


def test_choose_sandbox_for_generic_node_returns_webcontainer():
    """Test that a generic Node.js task defaults to WebContainer."""
    requirements = SandboxTaskRequirements(language="node")
    assert choose_sandbox(requirements) == SANDBOX_TYPE_WEB_CONTAINER


def test_choose_sandbox_for_generic_javascript_returns_webcontainer():
    """Test that a generic JavaScript task defaults to WebContainer."""
    requirements = SandboxTaskRequirements(language="javascript")
    assert choose_sandbox(requirements) == SANDBOX_TYPE_WEB_CONTAINER


def test_priority_of_e2b_for_sensitive_data_over_ui_feedback():
    """Test that E2B is chosen for sensitive data even if UI feedback is requested."""
    requirements = SandboxTaskRequirements(
        language="node", requires_ui_feedback=True, is_data_sensitive=True
    )
    assert choose_sandbox(requirements) == SANDBOX_TYPE_E2B
