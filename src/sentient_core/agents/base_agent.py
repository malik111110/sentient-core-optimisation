# Base Agent Definition for Sentient-Core

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..orchestrator.shared_state import Task

class BaseAgent(ABC):
    """Abstract base class for all specialized agents in the Sentient-Core factory."""

    def __init__(self, name: str, sandbox_tool: Optional[Any] = None):
        self.name = name
        self.sandbox_tool = sandbox_tool
        self.log(f"Agent {self.name} initialized.")
        if self.sandbox_tool:
            self.log(f"Equipped with tool: {self.sandbox_tool.__class__.__name__}")

    @abstractmethod
    def execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Executes a given task.

        Args:
            task: A Pydantic model object containing the specifics of the task.

        Returns:
            A dictionary containing the results of the task execution, including any
            artifacts produced or errors encountered.
        """
        pass

    def log(self, message: str):
        print(f"[{self.name}]: {message}")
