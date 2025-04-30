from urllib.parse import quote, urlencode

from downedit.platforms.domain import Domain
from downedit.platforms.media.bytedance.douyin.client import DouyinClient
from downedit.platforms.media.bytedance.douyin.extractor import extract_uifid
from downedit.platforms.media.bytedance.douyin.parameter import DouyinParam
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


class DouyinCrawler:

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
            sec-ch-ua,
            sec-ch-ua-platform,
            sec-ch-ua-mobile,
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

        self.dy_client = DouyinClient(client=self.client)
        self.dy_param = DouyinParam()

    async def fetch_user_post(
        self,
        sec_uid: str,
        max_cursor: int,
        count: int,
    ):
        """
        Fetches user posts from Douyin.

        Args:
            user_url (str): The URL of the user's profile.
            cursor (int): Pagination cursor for fetching posts.
            count (int): Number of posts to fetch.

        Returns:
            dict: A dictionary containing the user's posts.
        """
        self.client.headers["Accept"] = "application/json, text/plain, */*"
        self.client.headers["Accept-Encoding"] = "*/*"
        self.client.headers["Cookie"] = self.cookies
        self.client.headers["priority"] = "u=1, i"
        self.client.headers["Referer"] = f"{Domain.DOUYIN.DOUYIN_DOMAIN}/user/{sec_uid}"
        self.client.headers["Connection"] = "keep-alive"
        self.client.headers["Sec-Fetch-Site"] = "same-origin"
        self.client.headers["uifid"] = extract_uifid(self.cookies)

        item_list_param = self.dy_param.get_video_list(
            sec_uid=sec_uid,
            max_cursor=max_cursor,
            count=count,
            cookie_str=self.cookies,
            user_agent=self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            )
        )

        item_list_param["uifid"] = extract_uifid(self.cookies)

        param_string = urlencode(item_list_param, quote_via=quote)
        param_string = self.dy_client.get_abogus(
            param_string=param_string,
            browser_info=self.dy_param.get_browser_into(
                self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            )),
        )

        async with self.client.semaphore:
            response = await self.client.aclient.get(
                url=f"{Domain.DOUYIN.USER_POST}?{param_string}",
                headers=self.client.headers,
                timeout=5,
                follow_redirects=True,
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                return {}
