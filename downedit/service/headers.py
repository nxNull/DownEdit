from .user_agents import UserAgent
from .client_hints import ClientHints
from downedit.utils import Singleton



class Headers():
    """
    The Headers class.

    Description:
        The Headers class generates the headers for the Client Hints.

    Args:
        user_agent (UserAgent): The UserAgent object.
        client_hints (ClientHints): The ClientHints object.

    References:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-CH
    """
    def __init__(self, user_agent: UserAgent, client_hints: ClientHints):
        self.user_agent = user_agent
        self.client_hints = client_hints
        self._headers = {}
        self._is_generated = False

    def _reset_headers(self) -> None:
        """
        Reset the headers to the default state.

        Args:
            None

        References:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Client_hints#low_entropy_hints
        """
        self._headers = {'user-agent': str(self.user_agent)}

        if self.user_agent.browser_type in ('chrome', 'edge') :
            self._add_standard_hints()

        self._is_generated = True

    def _add_standard_hints(self) -> None:
        """
        Adds the standard Client Hints to the headers.
        """
        standard_hints = ['sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform']
        for hint in standard_hints:
            self._add_hint(hint)

    def _add_hint(self, key: str) -> None:
        """
        Add a Client Hints hint to the headers.

        Args:
            key (str): The hint name.
        """
        hint_map = {
            'sec-ch-ua'                  : 'brands',
            'sec-ch-ua-full-version-list': 'brands_full_version_list',
            'sec-ch-ua-platform'         : 'platform',
            'sec-ch-ua-platform-version' : 'platform_version',
            'sec-ch-ua-mobile'           : 'mobile',
            'sec-ch-ua-bitness'          : 'bitness',
            'sec-ch-ua-arch'             : 'architecture',
            'sec-ch-ua-model'            : 'model',
            'sec-ch-ua-wow64'            : 'wow64'
        }
        if key in hint_map:
            self._headers[key] = getattr(self.client_hints, hint_map[key])

    def accept_ch(self, value: str) -> None:
        """
        Parse the Sec-CH-UA header and add the appropriate Client Hints to the headers.

        Args:
            value (str): The value of the Sec-CH-UA header.

        References:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Client_hints#low_entropy_hints
        """
        self._reset_headers()

        if self.user_agent.browser_type not in ('chrome', 'edge') :
            return

        for hint in map(str.strip, value.split(',')):
            self._add_hint(hint.lower())

    def update(self, additional_headers: dict) -> None:
        """
        Updates the existing headers with the provided additional headers.

        Args:
            additional_headers (dict): The additional headers.
        """
        if not self._is_generated:
            self._reset_headers()
        self._headers.update(additional_headers)

    def get(self) -> dict:
        """
        Get the headers.

        Returns:
            dict: The headers.
        """
        if not self._is_generated:
            self._reset_headers()
        return self._headers

    def get_value(self, key: str) -> str:
        """
        Get a specific header by key.

        Args:
            key (str): The header key to retrieve.

        Returns:
            str: The value of the header if it exists, otherwise None.
        """
        if not self._is_generated:
            self._reset_headers()
        return self._headers.get(key, None)