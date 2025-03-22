import httpx

from downedit.agents.providers._config import AIConfig
from downedit.agents.providers._converter import GoogleMsgConverter
from downedit.agents.providers._providers import Provider
from downedit.service import (
    Client,
    retry_sync,
    httpx_capture_sync
)


class Google(Provider):
    """
    Google provider for interacting with Google's API.

    visit: https://ai.google.dev/
    """

    def __init__(
        self,
        service: Client = None,
        base_url: str = None,
        api_key: str = None,
        chat = None
    ):
        """
        Initialize the Google provider.

        Args:
        - service: The client to use for making requests.
        - base_url: The base URL for the provider.
        - api_key: The API key to use for authentication.
        - chat: The chat client to use for prompts.
        """
        self.transformer = GoogleMsgConverter(chat)
        self.__config = AIConfig.all_provider_configs()
        super().__init__(
            service,
            base_url,
            api_key,
            chat
        )

    def status(self):
        """
        Get the status of the provider.
        """
        ...

    @httpx_capture_sync
    @retry_sync(
        num_retries=1,
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
    def chat_completions(self, messages: str, **kwargs):
        """
        Get chat completions from the Google API.

        Args:
        - model: The model to use for completions.
        - messages: The messages to use for completions.
        - kwargs: Additional keyword arguments to pass to the API.
        """
        transformed_messages = self.transformer.convert_request(messages)
        transformed_messages.update(kwargs)

        self.service.client.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

        response = self.service.client.post(
            self.base_url,
            json=transformed_messages,
        )
        response.raise_for_status()

        return self.transformer.convert_response(response.json())