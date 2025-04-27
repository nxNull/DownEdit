import random

from downedit import AIContext
from downedit.service import Client
from downedit.platforms.ai_image.base import BaseAIGen
from downedit.platforms.ai_image.providers import (
    AIGG,
    Perchance,
    PerchanceCC,
    Pollinations
)
from downedit.utils import (
    log
)

class GenImageAI(BaseAIGen):
    def __init__(
        self,
        service: Client,
        context: AIContext
    ):
        super().__init__(
            service,
            context
        )
        self.providers = self._get_providers()

    def _get_providers(self):
        """
        Returns a list of AI image providers.
        """
        # provider_classes = [Perchance, PerchanceCC, AIGG, Pollinations]
        provider_classes = [Pollinations]
        selected_provider = random.choice(provider_classes)

        prov_arg = {}
        prov_arg["key"] = "RANDOM"
        prov_arg["size"] = self.context.get("size", "512x512")
        prov_arg["prompt"] = self.context.get("prompt")
        prov_arg["negativePrompt"] = self.context.get("negativePrompt")
        self.context.reset(prov_arg)
        return selected_provider(self.service, self.context)