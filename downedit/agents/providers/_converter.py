import json

from abc import ABC, abstractmethod

from downedit.agents.providers import (
    Role,
    Chat
)


__all__ = [
    'AutoBot',
    'DuckDuckGoConverter',
    'DeepSeekMsgConverter',
    'GoogleMsgConverter',
    'OpenAIMsgConverter',
    'XaiMsgConverter'
]


class AutoBot(ABC):
    """
    Base class for message converters.
    """
    def __init__(
        self,
        chat: Chat
    ) -> None:
        self.chat = chat

    @abstractmethod
    def convert_request(self, messages: str) -> dict:
        """
        Convert the request messages to the provider format.

        Args:
        - messages: The messages to convert.

        Returns:
        - The converted messages.
        """
        pass

    @abstractmethod
    def convert_response(self, response):
        """
        Convert the response messages from the provider format.

        Args:
        - response: The response to convert.

        Returns:
        - The converted response.
        """
        pass


class DuckDuckGoConverter(AutoBot):
    """
    A converter for transforming messages to and from the xAI format.
    """
    def __init__(
        self,
        chat: Chat
    ) -> None:
        super().__init__(chat)

    def convert_request(self, messages: str) -> dict:
        """
        Convert the request messages to the xAI format.

        Args:
        - messages: The messages to convert.

        Returns:
        - The converted messages.
        """
        self.chat.add_input(
            role=Role.user,
            message=messages
        )
        return self.chat.model_dump()

    def convert_response(self, response):
        """
        Convert the response messages from the xAI format.

        Args:
        - response: The response to convert.

        Returns:
        - The converted response.
        """
        self.chat.add_answer(
            role=Role.assistant,
            message=response
        )

        instruction = self.chat.model_dump()
        messages = instruction.get("messages", [])[-1]

        try:
            return json.loads(messages["content"])
        except json.JSONDecodeError:
            return {}