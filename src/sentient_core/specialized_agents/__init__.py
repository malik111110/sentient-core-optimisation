# Initializes the specialized_agents module

from .research_agent import ResearchAgent
from .data_agent import DataAgent
from .backend_developer_agent import BackendDeveloperAgent
from .frontend_developer_agent import FrontendDeveloperAgent
from .integration_agent import IntegrationAgent
from .deployment_agent import DeploymentAgent
from .bridge_agent import BridgeAgent

__all__ = [
    "ResearchAgent",
    "DataAgent",
    "BackendDeveloperAgent",
    "FrontendDeveloperAgent",
    "IntegrationAgent",
    "DeploymentAgent",
    "BridgeAgent"
]
