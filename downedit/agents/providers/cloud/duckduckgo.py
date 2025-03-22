import json

from downedit.agents.prompts import SYSTEM_PROMPTS
from downedit.agents.providers._config import AIConfig
from downedit.agents.providers._converter import DuckDuckGoConverter
from downedit.agents.providers._providers import Provider
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers,
)
from downedit.agents.providers import (
    Role,
    Chat
)
from downedit.utils import (
    log
)



class DuckDuckGo(Provider):
    """
    DuckDuckGo provider for interacting with DuckDuckGo's API.

    visit: https://duck.ai/
    """

    def __init__(
        self,
        service: Client = None,
        base_url: str = None,
        api_key: str = None,
        chat: Chat = None
    ):
        """
        Initialize the Google provider.

        Args:
        - service: The client to use for making requests.
        - base_url: The base URL for the provider.
        - api_key: The API key to use for authentication.
        - chat: The chat client to use for prompts.
        """  
        chat.add_input(
            role=Role.user,
            message=SYSTEM_PROMPTS.model_dump_json()
        )
        self.transformer = DuckDuckGoConverter(chat)
        self.user_agent = UserAgent(
            platform_type='desktop',
            device_type='windows',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-mobile,
            sec-ch-ua-platform,
        """)
        self.headers.update({
            "Host": "duckduckgo.com",
            "Accept": "text/event-stream",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,km;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Priority": "u=1, i",
            "Referer": "https://duckduckgo.com/",
            "Origin": "https://duckduckgo.com",
            "DNT": "1",
            "Sec-GPC": "1",
            "Cookie": "dcm=3; ay=b",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        })
        self.default_client = Client(headers=self.headers.get())
        self.client = service or self.default_client
        self.__config = AIConfig.all_provider_configs()
        self._x_vqd_4 = None
        self._vqd_hash_1 = None
        super().__init__(
            self.client,
            base_url,
            api_key,
            chat
        )

        self.__simulate_client()
        self.__get_x_vqd()

    def __simulate_client(self):
        """
        Simulate a client to get the API key.
        """
        try:
            response = self.service.client.get(
                url=self.__config["duckai"]["country_url"]
            )
            response.raise_for_status()

        except Exception as e:
            pass

    def __get_x_vqd(self):
        """
        Get the API key from the service.
        """
        try:
            self.client.headers.update({
                "Cache-Control": "no-cache",
                "X-Vqd-accept": "1",
            })

            response = self.service.client.get(
                url=self.__config["duckai"]["status_url"],
                headers=self.headers.get()
            )
            response.raise_for_status()

            self._x_vqd_4 = response.headers.get("X-Vqd-4")
            self._vqd_hash_1 = response.headers.get("X-Vqd-hash-1")

            return None

        except Exception as e:
            log.error(f"{e}")
            return None

    def __stream_response(self, response):
        """
        Stream the response from the API.
        """
        response_text = response.decode("utf-8")

        messages = []
        for line in response_text.split("\n"):
            if not line.startswith("data: "):
                continue

            data = line[6:]

            if data == "[DONE]":
                continue

            try:
                message = json.loads(data).get("message", "")
                if message:
                    messages.append(message)
            except json.JSONDecodeError:
                continue

        extracted_text = "".join(messages)

        return extracted_text

    def status(self):
        """
        Get the status of the provider.
        """
        ...

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

        self.headers.update({
            "X-Vqd-4": f"{self._x_vqd_4}",
            "X-Vqd-Hash-1": f"{self._vqd_hash_1}",
        })

        with self.service.client.stream(
            "POST",
            url=self.__config["duckai"]["base_url"],
            json=transformed_messages,
            headers=self.headers.get()
        ) as response:
            response.raise_for_status()
            response_content = self.__stream_response(response.read())

            self._x_vqd_4 = response.headers.get("X-Vqd-4", self._x_vqd_4)
            self._vqd_hash_1 = response.headers.get("X-Vqd-hash-1", self._vqd_hash_1)

        return self.transformer.convert_response(response_content)