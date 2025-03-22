from downedit.agents.providers import Provider


class ClientAI:
    """
    Client for interacting with the LLM API.
    """
    def __init__(self, provider: Provider = None):
        self.provider = provider
        self.__chat = None

    @property
    def chat(self):
        """
        Chat client.
        """
        if not self.__chat:
            self.__chat = ChatClient(self)
        return self.__chat


class ChatClient:
    """
    Chat client. This client is used to interact with the chat completions.
    """
    def __init__(self, client: ClientAI):
        self.agclient = client
        self._completions = None

    @property
    def completions(self):
        """
        Create a chat completion object.
        """
        if not self._completions:
            self._completions = Completions(self.agclient)
        return self._completions


class Completions:
    """
    Chat completions client.
    """
    def __init__(self, parent: ClientAI):
        self.parent = parent

    def create(
        self,
        messages: str,
        **kwargs
    ):
        """
        Create a chat completion.

        Args:
        - model: The model to use for completions.
        - messages: The messages to use for completions.
        - kwargs: Additional keyword arguments to pass to the API.

        """
        provider: Provider = self.parent.provider
        return provider.chat_completions(
            messages,
            **kwargs
        )