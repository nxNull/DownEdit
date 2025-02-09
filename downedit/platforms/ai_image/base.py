from abc import ABC, abstractmethod

from downedit import AIContext
from downedit.service import Client
from downedit.utils import (
    log
)


class ImageAIService(ABC):
    def __init__(
        self,
        service: Client,
        context: AIContext
    ):
        self.service = service
        self.context = context

    @abstractmethod
    async def generate(self):
        pass


class BaseAIGen(ABC):
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context
        self.providers: ImageAIService = self._get_providers()

    @abstractmethod
    def _get_providers(self):
        """
        Returns a list of AI image providers.
        """
        pass

    async def generate(self):
        """
        Generates an image using a selected provider.
        """
        return await self.providers.generate()