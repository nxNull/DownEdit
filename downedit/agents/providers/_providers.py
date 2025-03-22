from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Any,
    Dict,
    Type
)

from downedit.service import Client


CLOUD_FACTORY: Dict[str, Type['Provider']] = {}
LOCAL_FACTORY: Dict[str, type[Any]] = {}


class Registers(ABC):
    """
    Base class for all providers.

    Args:
    - service: The client to use for making requests.
    - base_url: The base URL for the provider.
    - api_key: The API key to use for authentication.
    - chat: The chat instance to use for chat completions.
    """
    def __init__(
        self,
        service: Client = None,
        base_url: str = None,
        api_key: str = None,
        chat = None,
    ):
        self.service = service
        self.base_url = base_url
        self.api_key = api_key
        self.chat = chat

    @abstractmethod
    def status(self):
        """
        Get the status of the provider.
        """
        pass

    @abstractmethod
    def chat_completions(self, messages: str):
        """
        Chat completion calls, to be implemented by each provider.
        """
        pass


class Provider(Registers):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        CLOUD_FACTORY[cls.__name__.lower()] = cls
