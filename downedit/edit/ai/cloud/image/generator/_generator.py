from downedit.platforms    import GenImageAI
from downedit         import AIContext
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)


class GenerativeImageAI:
    """
    The generative image AI class.

    Args:
        provider (Handler): The provider for the AI image generator.
        context (str): The context for the AI image generator.
    """

    def __init__(self, provider, context: str):
        self.user_context = context
        self.ai_context = AIContext()
        self.user_agent = UserAgent(
            platform_type='mobile',
            device_type='android',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            Sec-Ch-Ua,
            Sec-Ch-Ua-Platform,
            Sec-Ch-Ua-Platform-Version,
            Sec-Ch-Ua-Mobile,
            Sec-Ch-Ua-Full-Version-List,
            Sec-Ch-Ua-Bitness,
            Sec-Ch-Ua-Arch,
            Sec-Ch-Ua-Model,
            Sec-Ch-Ua-Wow64
        """)

    async def generate(self):
        """
        Generate an image.
        """
        prov_arg = {}
        prov_arg["size"] = self.user_context.get("size", "512x512")
        prov_arg["prompt"] = self.user_context.get("prompt", "")
        prov_arg["negativePrompt"] = self.ai_context.get("negative_prompt", "")
        self.ai_context.reset(prov_arg)

        async with Client(headers=self.headers.get()) as client:
            return await GenImageAI(client, self.ai_context).generate()
