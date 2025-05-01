import time

import httpx
from downedit.platforms.domain import Domain
from downedit.platforms.media.bytedance.mstoken import TikTokMsToken
from downedit.platforms.media.bytedance.xbogus import TikTokXBogus
from downedit.platforms.media.bytedance.tiktok.extractor import extract_rehydration_data
from downedit.service import retry_async, httpx_capture_async
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    log
)


class TikTokClient:
    """
    KuaiShou client configuration.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.user_agent = UserAgent(
            platform_type="desktop",
            device_type="windows",
            browser_type="chrome"
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
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

    async def get_msToken(
        self,
        url: str,
        headers: dict = {},
        cookie="",
        **kwargs,
    ) -> str:
        """
        Retrieves the msToken for the given URL.
        """
        return await TikTokMsToken.get_real_ms_token(
            param=url,
            headers=self.client.headers,
            cookie=cookie,
            **kwargs
        )

    def get_xbogus(self, param_string) -> str:
        """
        Generates the xbogus value for the given parameters.
        """
        param_string += f"&X-Bogus={TikTokXBogus.get_x_bogus(
            url=param_string,
            user_agent=self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            )
        )}"

        return param_string

    async def get_client_details(self, url):
        """
        Returns the client details for TikTok.
        """
        self.client.headers["Accept"] = "*/*"
        self.client.headers["Accept-Encoding"] = "*/*"
        self.client.headers["Connection"] = "gzip, deflate"
        self.client.headers["Referer"] = Domain.TIKTOK.TIKTOK_DOMAIN

        async with self.client.semaphore:
            response = await self.client.aclient.get(url)
            response.raise_for_status()
            rehydration_data = extract_rehydration_data(response.text)

        default_scrope =  rehydration_data.get("__DEFAULT_SCOPE__", {})
        webapp_app_context = default_scrope.get("webapp.app-context", {})
        webapp_user_details = default_scrope.get("webapp.user-detail", {})

        return {
            "appId": webapp_app_context.get('appId', ""),
            "region": webapp_app_context.get('region', ""),
            "deviceId": webapp_app_context.get('wid', ""),
            'odinId': webapp_app_context.get('odinId', ""),
            'webIdLastTime': webapp_app_context.get('webIdLastTime', time.time()),
            'abTestVersions': webapp_app_context.get('abTestVersion', {}).get('versionName', '').split(','),
            'msToken': response.headers.get('x-ms-token'),
            'cookies': str(httpx.Cookies(response.cookies)),
            'secUid': webapp_user_details.get('userInfo', {}).get('user', {}).get('secUid', ""),
        }
