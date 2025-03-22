import uuid
from typing import Dict, Optional

from downedit.agents.agent import AInterface, Agent
from downedit.agents.providers import Chat
from downedit.utils import (
    log
)

__all__ = [
    "AIFactory",
]

class AIFactory:
    """
    A factory for creating AI agents instances.
    """

    def __init__(self):
        """
        Initialize the AI factory.
        """
        self.agents: Dict[str, AInterface] = {}
        self.create = Create(self)

    def get_agent(self, agent_id: str) -> Optional[AInterface]:
        """
        Retrieve an AI agent by ID.
        """
        return self.agents.get(agent_id, None)

    def list_agents(self) -> list[str]:
        """
        List all created AI agents.
        """
        return list(self.agents.keys())

    def delete_agent(self, agent_id: str) -> bool:
        """
        Remove an AI agent by ID.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False


class Create:
    """
    Create AI agents.
    """

    def __init__(self, factory: AIFactory):
        """
        Initialize the create agent.
        """
        self.factory = factory

    def cloud_agent(
        self,
        name: str,
        agent_id: Optional[str] = str(uuid.uuid4()),
        chat: Chat = None,
        **kwargs
    ) -> AInterface:
        """
        Create and store an AI agent using a cloud provider.
        """
        try:
            agent = Agent(
                type="cloud",
                name=name,
                chat=chat,
                **kwargs
            )
        except Exception as e:
            log.error(f"Failed to create {name} agent.")
            raise

        self.factory.agents[agent_id] = agent

        return self.factory.get_agent(agent_id)

    def local_agent(
        self,
        name: str,
        agent_id: Optional[str] = str(uuid.uuid4()),
        **kwargs
    ):
        """
        Create and store an AI agent locally.
        """
        try:
            agent = Agent(
                type="local",
                name=name,
                **kwargs
            )
        except Exception as e:
            log.error(f"Failed to create {name} agent.")
            raise

        pass