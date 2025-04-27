from time import time
from json import dumps
from typing import Any
import urllib.parse

import httpx

from downedit.platforms.domain import Domain
from downedit.platforms.media.bytedance.xbogus import TikTokXBogus

TIKTOK_DATA = dumps({
    "magic": 538969122,
    "version": 1,
    "dataType": 8,
    "strData": "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",
    "tspFromClient": int(time() * 1000),
})

TIKTOK_TOKEN = "msToken=gDZCQCRbBEpVlh3y15umYcXhyEKcqh5TJ4TDeelDcudy6RfaXQQiFcdmCmKqgEBkyA006pIjFX7rqyihnLrZLoxA3J8QdOSHvbtFC8k0bMxxxs1lg86sIgaMWw7oP--wyJu8x0GCA-Mc"


class TikTokMsToken():

    @classmethod
    async def get_ms_token(
        cls,
        params: str = "",
        headers: dict = {},
        **kwargs
    ) -> str | None:
        """
        Get the msToken from TikTok.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                Domain.TIKTOK.REPORT,
                params=params,
                content=TIKTOK_DATA,
                headers=headers
            )

            response.raise_for_status()
            return str(httpx.Cookies(response.cookies).get("msToken", ""))

    @classmethod
    async def get_real_ms_token(
        self,
        param: Any,
        headers: dict = {},
        cookie="",
        **kwargs,
    ) -> str | None:
        """
        Get the real msToken from TikTok.

        Args:
            headers (dict): Headers to be used in the request.
            cookie (str): Cookie to be used in the request.
            **kwargs: Additional keyword arguments.
        """
        headers.update({
            "Cookie": cookie or TIKTOK_TOKEN,
        })

        if isinstance(param, dict):
            param = urllib.parse.urlencode(param)

        xbogus = TikTokXBogus().get_x_bogus(
            param,
            headers.get("User-Agent") or headers.get("user-agent"),
        )

        param_xbogus = param + "&X-Bogus=" + xbogus

        return await self.get_ms_token(
            params=param_xbogus,
            headers=headers,
            **kwargs,
        )
