import json
import httpx

from downedit.platforms.media.kuaishou.client import KuaiShouClient
from downedit.platforms.domain import Domain
from downedit.platforms.media.kuaishou.parameter import KuaishouParam
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

class KuaishouCrawler:
    def __init__(self, *args, **kwargs):
        self.cookies = kwargs.get("cookies", "")
        self.user_agent = UserAgent(
            platform_type='desktop',
            device_type='windows',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-platform,
            sec-ch-ua-mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

        self.ks_client = KuaiShouClient()
        self.ks_param = KuaishouParam()

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
    async def fetch_user_live_videos(self, principalId: str, pcursor: str = "", cookies: str = ""):
        """
        Crawls the user information.
        """
        self.client.headers["Accept"] = "application/json, text/plain, */*"
        self.client.headers["Connection"] = "keep-alive"
        # cookies = await self.ks_client.get_client_details()
        # get cookies from class
        self.client.headers["Cookie"] = self.cookies
        self.client.headers["Host"] = "live.kuaishou.com"
        self.client.headers["Referer"] = Domain.KUAI_SHOU.PROFILE_URL + principalId

        async with self.client.semaphore:
            response = await self.client.aclient.get(
                url=Domain.KUAI_SHOU.PUBLIC_PROFILE,
                params = {
                    "count": 12,
                    "pcursor": pcursor,
                    "principalId": principalId,
                    "hasMore": "true"
                },
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                return {}


        json_response = response.json()
        data = json_response.get("data", {})

        return {
            "result": data.get("result", 0),
            "pcursor": data.get("pcursor", ""),
            "videos": data.get("list", [])
        }

    @httpx_capture_async
    @retry_async(
        num_retries=3,
        delay=5,
        exceptions=(
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
        ),
    )
    async def fetch_user_feed_videos(
        self,
        principalId: str,
        pcursor: str = "",
        count: int = 18,
    ):
        """
        Crawls the user information.
        """
        self.client.headers["Accept"] = "*/*"
        self.client.headers["Accept-Language"] = "en-US,en;q=0.9"
        self.client.headers["Content-Type"] = "application/json"
        self.client.headers["Connection"] = "keep-alive"
        cookies = self.ks_client.get_client_details(self.cookies)
        # log.info(f"cookies: {cookies}")
        self.client.headers["Cookie"] = cookies
        self.client.headers["Host"] = "www.kuaishou.com"
        self.client.headers["Origin"] = Domain.KUAI_SHOU.KAUI_SHOU_DOMAIN
        self.client.headers["Referer"] = Domain.KUAI_SHOU.FEED_PROFILE_URL + principalId
        self.client.headers["Sec-Fetch-Site"] = "same-origin"

        async with self.client.semaphore:
            response = await self.client.aclient.post(
                url=Domain.KUAI_SHOU.DATA_URL,
                data= json.dumps(
                    self.ks_param.get_video_list(
                        principalId,
                        pcursor,
                        count
                    )
                ),
                timeout=10,
                follow_redirects=True,
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                return {}
