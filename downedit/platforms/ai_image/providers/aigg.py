import httpx
import asyncio

from downedit import AIContext
from downedit.service import Client
from downedit.service import retry_async, httpx_capture_async
from downedit.platforms import Domain
from downedit.platforms.ai_image.base import ImageAIService
from downedit.utils import (
    log
)


class AIGG(ImageAIService):
    def __init__(
        self,
        service: Client,
        context: AIContext
    ):
        super().__init__(service, context)
        _size_value = self.context.get("size")
        self.extract_dimensions(_size_value)
        self.context.set("quantity", 1)

    def extract_dimensions(self, size_value):
        """
        Extract width and height from the size value.
        """
        if 'x' in size_value:
            width, height = map(int, size_value.split('x'))
        else:
            width = 512
            height = int(size_value)

        self.context.set("width", width)
        self.context.set("height", height)

    @httpx_capture_async
    @retry_async(
        num_retries=3,
        delay=1,
        exceptions=(
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
        ),
    )
    async def generate(self):
        """
        Generates an image using the AIGG API.
        """
        request_method = "POST"
        request_headers = self.service.headers
        request_proxies = self.service.proxies
        self.service.timeout = 18

        async with self.service.semaphore:
            content_request = self.service.aclient.build_request(
                method=request_method,
                url=Domain.AI_IMAGE.AIGG.GENERATE_IMAGE,
                headers=request_headers,
                timeout=self.service.timeout,
                json=self.context.json()
            )

            response = await self.service.aclient.send(
                request=content_request,
                follow_redirects=True
            )

            if not response.text.strip() or not response.content:
                await asyncio.sleep(0.5)

            response.raise_for_status()
            return response.json()