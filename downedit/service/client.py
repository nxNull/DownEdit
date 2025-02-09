import asyncio
import ssl
import httpx

from .proxy import Proxy
from .headers import Headers

class Client:
    """
    Base class for creating an HTTP client.
    """
    def __init__(
        self,
        proxies: Proxy = None,
        max_retries: int = 5,
        max_connections: int = 10,
        timeout: int = 10,
        max_tasks: int = 10,
        headers: Headers = {},
        ssl: ssl.SSLContext | str | bool = False
    ):
        self.proxies         = proxies.to_httpx_format() if proxies else {}
        self.headers         = headers if headers else {}
        self.max_tasks       = max_tasks
        self.semaphore       = asyncio.Semaphore(max_tasks)
        self.max_connections = max_connections
        self.timeout         = timeout
        self.max_retries     = max_retries
        self.limits          = httpx.Limits(max_connections=self.max_connections)
        self.timeout_config  = httpx.Timeout(self.timeout)
        self.ssl             = ssl

        self._aclient = None
        self._client  = None

    @property
    def aclient(self):
        """
        Property for the async client.

        Returns:
            httpx.AsyncClient: The async client.
        """
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(
                headers=self.headers,
                verify=self.ssl,
                timeout=self.timeout_config,
                limits=self.limits,
                # http2=True,
            )
        return self._aclient

    @property
    def client(self):
        """
        Property for the client.

        Returns:
            httpx.Client: The client
        """
        if self._client is None:
            self._client = httpx.Client(
                headers=self.headers,
                proxies=self.proxies,
                verify=self.ssl,
                timeout=self.timeout_config,
                limits=self.limits,
            )
        return self._client

    async def close(self):
        """
        Close the client.
        """
        if self._client: self.client.close()
        if self._aclient: await self.aclient.aclose()

    async def __aenter__(self):
        """
        Async context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Close the client when exiting the context manager.
        """
        await self.close()