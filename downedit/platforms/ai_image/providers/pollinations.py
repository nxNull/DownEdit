import httpx
import random
import asyncio
import urllib.parse

from downedit import AIContext
from downedit.service import Client
from downedit.service import retry_async, httpx_capture_async
from downedit.platforms import Domain
from downedit.platforms.ai_image.base import ImageAIService
from downedit.utils import (
    log
)


class Pollinations(ImageAIService):
    def __init__(
        self,
        service: Client,
        context: AIContext
    ):
        super().__init__(service, context)
        _size_value = self.context.get("size")
        self.extract_dimensions(_size_value)
        self.context.set("seed", int(random.random() * 2147483647))
        self.context.set("model", "flux")
        self.context.set("token", "desktophut")
        self.context.set("nologo", True)
        self.context.set("safe", False)

    def extract_dimensions(self, size_value):
        """
        Extract width and height from the size value.
        """
        if 'x' in size_value:
            width, height = map(int, size_value.split('x'))
        else:
            width = 1020
            height = 1020

        self.context.set("width", width)
        self.context.set("height", height)
    
    def _build_request_params(self):
        """
        Build and encode query parameters for the API request.
        """
        params = {}
        context_data = self.context.json()
        negative_prompt = None
        
        if "negativePrompt" in context_data and context_data["negativePrompt"]:
            negative_prompt = urllib.parse.quote(context_data["negativePrompt"])
        
        excluded_keys = ["prompt", "key", "size", "negativePrompt"]
        params.update({
            k: v for k, v in context_data.items() 
            if k not in excluded_keys and v is not None
        })
        
        param_items = [f"{k}={v}" for k, v in params.items()]
        
        if negative_prompt is not None:
            param_items.append(f"negative_prompt={negative_prompt}")
        
        return "&".join(param_items)

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
        Generates an image using the Pollinations API.
        """
        prompt = self.context.get("prompt", "")
        encoded_prompt = urllib.parse.quote(prompt)
        
        params = self._build_request_params()
        
        base_url = f"{Domain.AI_IMAGE.POLLINATIONS.GENERATE_IMAGE}{encoded_prompt}"
        url = f"{base_url}?{params}" if params else base_url
            
        request_headers = self.service.headers
        request_proxies = self.service.proxies
        self.service.timeout = 30
        
        async with self.service.semaphore:
            content_request = self.service.aclient.build_request(
                method="GET",
                url=url,
                headers=request_headers,
                timeout=self.service.timeout
            )
            
            response = await self.service.aclient.send(
                request=content_request,
                follow_redirects=True
            )

            if not response.text.strip() or not response.content:
                await asyncio.sleep(0.5)

            response.raise_for_status()

            return {
                "data": {
                    "fileId": f"{self.context.get('seed')}",
                    "url": url
                }
            }