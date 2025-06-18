# Base Agent Definition for Sentient-Core

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract base class for all specialized agents in the Sentient-Core factory."""

    def __init__(self, name: str, role: str, goal: str):
        self.name = name
        self.role = role
        self.goal = goal
        print(f"Agent {self.name} ({self.role}) initialized.")

    @abstractmethod
    def execute_task(self, task_details: Dict[str, Any], shared_state: Any) -> Dict[str, Any]:
        """
        Executes a given task.

        Args:
            task_details: A dictionary containing the specifics of the task.
            shared_state: The overall shared state of the agentic factory, allowing agents
                          to access context and store artifacts.

        Returns:
            A dictionary containing the results of the task execution, including any
            artifacts produced or errors encountered.
        """
        pass

    def log(self, message: str):
        print(f"[{self.name}]: {message}")
