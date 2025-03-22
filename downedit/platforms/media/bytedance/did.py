import httpx

from re import compile

from downedit.platforms.domain import Domain
from downedit.service import retry_async, httpx_capture_async
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)

class TikTokDid:
    """
    Retrieves the device ID and cookie from TikTok.
    """

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
    async def _fetch_tiktok_data(
        self,
        headers: dict,
        **kwargs
    ) -> httpx.Response:
        """
        Performs the HTTP request to TikTok's API.
        """
        async with Client(headers=headers) as client:
            response = await client.aclient.get(
                Domain.TIKTOK.EXPLORE,
                headers=headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response

    def _extract_device_id(self, response_text: str) -> str:
        """
        Extracts the device ID from the response text.
        """
        DEVICE_ID_REGEX = compile(r'"wid":"(\d{19})"')
        match = DEVICE_ID_REGEX.search(response_text)
        return match.group(1) if match else ""

    def _extract_cookie(
        self,
        response_cookies: httpx.Cookies
    ) -> str:
        """
        Extracts the cookie from the response cookies.
        """
        return "; ".join(f"{key}={value}" for key, value in response_cookies.items())

    async def get_device_id(
        self,
        headers: dict = None,
        **kwargs
    ) -> tuple[str, str]:
        """
        Fetches the TikTok device ID and cookie.

        Args:
            headers: Optional; overrides default headers.
            **kwargs: Additional keyword arguments for the HTTP request (e.g., proxy).

        Returns:
            A tuple containing the device ID (str) and cookie (str). Returns ("", "") if not found.
        """
        headers = headers or self.headers
        headers["Referer"] = Domain.TIKTOK.TIKTOK_DOMAIN

        response = await self._fetch_tiktok_data(headers, **kwargs)
        device_id = self._extract_device_id(response.text)
        cookie = self._extract_cookie(response.cookies)
        return device_id, cookie

    async def get_device_ids(
        self,
        number: int = 1,
        headers: dict = None,
        **kwargs
    ) -> list[tuple[str, str]]:
        """
        Fetches multiple TikTok device IDs and cookies.

        Args:
            number: The number of IDs to fetch.
            headers: Optional; overrides default headers.
            **kwargs: Additional keyword arguments for the HTTP request (e.g., proxy).

        Returns:
            A list of tuples, where each tuple contains a device ID and cookie.
        """
        return [
            await self.get_device_id(headers, **kwargs)
            for _ in range(number)
        ] if number > 0 else []