import httpx
from typing import Any
from urllib.parse import quote, urlencode

from downedit.platforms.domain import Domain
from downedit.platforms.media.bytedance.tiktok.client import TikTokClient
from downedit.platforms.media.bytedance.tiktok.parameter import TikTokParam
from downedit.service import retry_async, httpx_capture_async
from downedit.platforms.media.bytedance.tiktok.extractor import (
    extract_msToken,
    extract_secuid,
    extract_username
)
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    log
)


class TiktokCrawler:
    """
    TikTok profile and post crawler.

    Args:
        cookies (str): Cookies string for authentication.
        client (Client): Optional custom HTTP client.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.cookies = kwargs.get("cookies", "")
        self.user_agent = UserAgent(
            platform_type='desktop',
            device_type='windows',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            Sec-Ch-Ca,
            Sec-Ch-Ua-Platform,
            Sec-Ch-Ua-Mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

        self.tt_client = TikTokClient(client=self.client)
        self.tt_param = TikTokParam()

        self._client_details: dict[str, Any] = {}

    async def get_secUid(self, url: str) -> str:
        """
        Get the secuid from the URL.

        Args:
            url (str): The URL to extract the secuid from.

        Returns:
            str: The secuid extracted from the URL.
        """

        self.client.headers["Accept"] = "*/*"
        self.client.headers["Accept-Encoding"] = "*/*"
        # self.client.headers["Connection"] = "gzip, deflate"

        async with self.client.semaphore:
            response = await self.client.aclient.get(url)
            response.raise_for_status()
            return extract_secuid(response.text)

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
    async def fetch_user_detail(self, user_url: str) -> dict:
        """
        Fetch the user details from TikTok.
        """
        if not self._client_details:
            self._client_details = await self.tt_client.get_client_details(user_url)

        self.client.headers["Accept"] = "*/*"
        self.client.headers["Accept-Encoding"] = "*/*"
        self.client.headers["Cookie"] = self.cookies
        self.client.headers["Referer"] = user_url
        self.client.headers["Connection"] = "keep-alive"

        user_details_param = self.tt_param.get_user_details(
            sec_uid=self._client_details.get("secUid", ""),
            uniqueId=extract_username(user_url),
            user_agent=self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            ),
        )
        user_details_param["msToken"] = extract_msToken(self.cookies)[1]

        param_string = urlencode(user_details_param, quote_via=quote)
        param_string = self.tt_client.get_xbogus(param_string)

        async with self.client.semaphore:
            response = await self.client.aclient.get(
                url=f"{Domain.TIKTOK.USER_DETAIL}?{param_string}",
                headers=self.client.headers,
                timeout=5,
                follow_redirects=True,
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                return {}

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
    async def fetch_user_post(
        self,
        user_url: str,
        cursor: int,
        count: int,
    ):
        """
        Fetch the user post from TikTok.

        Args:
            user_url (str): The URL to extract the secuid from.

        Returns:
            dict: The response data from the TikTok API.
        """
        if not self._client_details:
            self._client_details = await self.tt_client.get_client_details(user_url)
            # self._client_details["secUid"] = await self.get_secUid(user_url)

        self.client.headers["Accept"] = "*/*"
        self.client.headers["Accept-Encoding"] = "*/*"
        self.client.headers["Cookie"] = self.cookies
        self.client.headers["Referer"] = Domain.TIKTOK.EXPLORE
        self.client.headers["Sec-Fetch-Site"] = "same-origin"
        self.client.headers["Connection"] = "keep-alive"

        item_list_param = self.tt_param.get_video_list(
            sec_uid=self._client_details.get("secUid", ""),
            cursor=cursor,
            count=count,
            user_agent=self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            )
        )

        # item_list_param["odinId"] = self._client_details.get("odinId", "")
        # item_list_param["device_id"] = self._client_details.get("deviceId", "")
        # item_list_param["msToken"] = await self.tt_client.get_msToken(
        #     url=f"msToken={extract_msToken(self.cookies)}",
        #     cookie=self.cookies
        # )
        item_list_param["msToken"] = extract_msToken(self.cookies)[1]

        param_string = urlencode(item_list_param, quote_via=quote)
        param_string = self.tt_client.get_xbogus(param_string)

        async with self.client.semaphore:
            response = await self.client.aclient.get(
                url=f"{Domain.TIKTOK.USER_POST}?{param_string}",
                headers=self.client.headers,
                timeout=5,
                follow_redirects=True,
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                return {}
