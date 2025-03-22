import uuid

from downedit.agents.providers import Chat

from ._factory import AIFactory
from .agent import AInterface


class SIMA:
    """
    Single Instruction Multi-Agents.
    """

    def __init__(self) -> None:
        self._ai_factory = AIFactory()
    
    def create_agent(
        self,
        agent_type: str,
        agent_id: str = str(uuid.uuid4()),
        provider_name: str = "duckduckgo",
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> str:
        """
        Create a single agent using the factory.

        Args:
            agent_type (str): The type of agent to create.
            agent_id (str): The ID of the agent.
            provider_name (str): The name of the provider.
            model (str): The model to use for the agent.
            **kwargs: Provider specific keyword arguments.

        Returns:
            Agent: The created agent.
        """
        create = {}
        create["cloud"] = self._ai_factory.create.cloud_agent
        create["local"] = self._ai_factory.create.local_agent

        agent = create.get(agent_type.lower())
        if agent is None:
            raise ValueError(
                f"Invalid agent type: {agent_type}. Must be 'cloud' or 'local'"
            )

        chat_instance = Chat(
            model=model,
            messages=[]
        )

        agent(
            name=provider_name,
            agent_id=agent_id,
            model=model,
            chat=chat_instance,
            **kwargs
        )

        return agent_id

    def instruction(
        self,
        agent_id: str,
        messages: str,
        **kwargs
    ) -> dict:
        """
        Send an instruction to an agent.

        Args:
            agent_id (str): The ID of the agent.
            messages (str): The messages to send to the agent.
            **kwargs: Additional keyword arguments to pass to the agent.

        Returns:
            str: The response from the agent.
        """
        agent = self._ai_factory.get_agent(agent_id)

        return agent.instruction(
            messages,
            **kwargs
        )

    def run(self, agent_id: str, tasks: list = []):
        """
        Run the agent.

        Args:
            agent_id (str): The ID of the agent.

        Returns:
            str: The response from the agent.
        """
        agent = self._ai_factory.get_agent(agent_id)
        return agent.run(tasks)