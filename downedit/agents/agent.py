from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from downedit.agents.invoker import invoke_tool_sync
from downedit.agents.client import ClientAI
from downedit.agents.providers import Chat
from downedit.agents.providers import (
    CLOUD_FACTORY,
    LOCAL_FACTORY
)


__all__ = [
    "AInterface",
    "Agent"
]


@runtime_checkable
class AInterface(Protocol):
    """
    A protocol defining the interface for all agents.
    """
    def instruction(
        self,
        messages: str,
        **kwargs
    ) -> Any:
        ...

    def run(
        self,
        tasks: list
    ) -> Any:
        ...


class Agent:
    def __init__(
        self,
        type: str = "cloud",
        name: str = "duckduckgo",
        chat: Chat = None,
        **kwargs
    ):
        self.provider = self.__agent(
            type,
            name,
            chat=chat,
            **kwargs
        )
        self.client = ClientAI(self.provider)

    def __agent(
        self,
        type: str = "cloud",
        name: str = "duckduckgo",
        chat: Chat = None,
        **kwargs
    ):
        """
        Create a provider instance based on the name.
        """
        factory = CLOUD_FACTORY if type == "cloud" else LOCAL_FACTORY

        if name not in factory:
            raise ValueError(f"Invalid provider name: {name}")

        prover_class = factory.get(name, "duckduckgo")

        return prover_class(
            service = kwargs.get("service", None),
            base_url = kwargs.get("base_url", None),
            api_key = kwargs.get("api_key", None),
            chat = chat
        )

    def instruction(
        self,
        messages: str,
        **kwargs
    ) -> Any:
        """
        Get chat completions from the provider API.
        """
        return self.client.chat.completions.create(
            messages,
            **kwargs
        )

    def run(self, tasks: list = []) -> Any:
        """
        Run the agent.
        """
        for task in tasks:
            tool_name = task.get("tool_name", None)

            if tool_name is None:
                raise ValueError("Tool name is required")
            
            tool_args = task.get("tool_args", {})
            
            if not isinstance(tool_args, dict):
                raise ValueError("Tool args must be a dictionary")
            
            invoke_tool_sync(tool_name, tool_args)