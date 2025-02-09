import httpx
from typing import Dict, Union, Any

from downedit.service import retry_async, httpx_capture_async
from downedit.service import Client

__all__ = ["DouyinWid", "TiktokWid"]

class DouyinWid:
    """
    Retrieves the web ID from the Douyin API.
    """

    _API = "https://mcs.zijieapi.com/webid"
    _PARAMS = {
        "aid": "6383",
        "sdk_version": "5.1.18_zip",
        "device_platform": "web"
    }

    def __init__(self, headers: dict):
        self.headers = headers

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
    async def _fetch_webid_data(
        self,
        headers: dict,
        data: str,
        **kwargs: Any
    ) -> httpx.Response:
        """
        Performs the HTTP request to fetch the web ID.
        """
        async with Client(headers=headers) as client:
            response = await client.aclient.post(
                self._API,
                params=self._PARAMS,
                data=data,
                headers=headers,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

    def _extract_web_id(self, response_json: dict) -> str | None:
        """
        Extracts the web ID from the response JSON.
        """
        return response_json.get("web_id")

    async def get_web_id(
        self,
        headers: dict = None,
        **kwargs: Any
    ) -> str | None:
        """
        Fetches the web ID from Douyin API.

        Args:
            headers: Optional; overrides default headers.
            **kwargs: Additional keyword arguments for the HTTP request (e.g., proxy).

        Returns:
            The web ID (str) if found, None otherwise.
        """
        headers = headers or self.headers
        user_agent = headers.get("User-Agent")
        data = (
            f'{{"app_id":6383,"url":"https://www.douyin.com/","user_agent":"{user_agent}","referer":"https://www'
            f'.douyin.com/","user_unique_id":""}}'
        )

        try:
            response = await self._fetch_webid_data(headers, data, **kwargs)
            return self._extract_web_id(response.json())
        except Exception as e:
            # log error
            return None

class TiktokWid:
    """
    A class to handle TTWid registration and extraction for both ixigua and TikTok services.
    """

    _API_IXIGUA = "https://ttwid.bytedance.com/ttwid/union/register/"
    _API_TIKTOK = "https://www.tiktok.com/ttwid/check/"

    _DATA_IXIGUA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"",'
        '"source":"node"},"cbUrlProtocol":"https","union":true}'
    )
    _DATA_TIKTOK = (
        '{"aid":1988,"service":"www.tiktok.com","union":false,"unionHost":"","needFid":false,"fid":"",'
        '"migrate_priority":0}'
    )

    def __init__(self, headers: dict):
        self.headers = headers

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
    async def _fetch_data(self, data: str, api_url: str, **kwargs: Any) -> httpx.Response:
        """
        Performs the HTTP request to fetch TTWid data from the given API URL.
        """
        async with Client(headers=self.headers) as client:
            response = await client.aclient.post(
                api_url,
                data=data,
                headers=self.headers,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

    def _extract_ttwid(self, response_json: dict) -> Dict[str, str] | None:
        """
        Extracts the TTWid value from the response JSON.
        """
        if "ttwid" in response_json:
            return {"ttwid": response_json["ttwid"]}
        return None

    async def get_tt_wid(
        self,
        service: str = "tiktok",
        cookie: str = "",
        **kwargs: Any
    ) -> Dict[str, str] | None:
        """
        Fetches the TTWid from the appropriate API based on the service (ixigua or tiktok).

        Args:
            service: The service to fetch TTWid from, either "ixigua" or "tiktok".
            cookie: Cookie for the request (used for TikTok service).
            **kwargs: Additional keyword arguments for the HTTP request (e.g., proxy).

        Returns:
            A dictionary with the ttwid or None if not found.
        """
        if service == "tiktok":
            api_url = self._API_TIKTOK
            data = self._DATA_TIKTOK
            headers = {
                **self.headers,
                "Cookie": cookie,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        else:
            api_url = self._API_IXIGUA
            data = self._DATA_IXIGUA
            headers = self.headers

        try:
            response = await self._fetch_data(data, api_url, headers=headers, **kwargs)
            return self._extract_ttwid(response.json())
        except Exception as e:
            # log error
            return None
