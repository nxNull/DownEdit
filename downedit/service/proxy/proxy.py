class Proxy:
    """
    A class to manage and resolve proxy settings.
    """

    def __init__(self, proxies: dict = None):
        """
        Initializes the Proxy class with the given proxies.

        Args:
            proxies (dict): A dictionary of proxy settings.
        """
        self.proxies = proxies or {"all://": None}

    def get_proxy(self, scheme: str) -> str:
        """
        Retrieves the proxy URL based on the given scheme.

        Args:
            scheme (str): The scheme of the URL ('http', 'https', or 'all').

        Returns:
            str: The proxy URL or None if no proxy is set.
        """
        return self.proxies.get(f"{scheme}://") or self.proxies.get("all://")

    def to_httpx_format(self) -> dict:
        """
        Converts the proxy settings to the format expected by httpx.

        Returns:
            dict: A dictionary of proxies formatted for httpx.
        """
        formatted_proxies = {
            key.replace("all", "http"): value for key, value in self.proxies.items()
        }
        if "all://" in self.proxies:
            formatted_proxies["https"] = self.proxies["all://"]
        return formatted_proxies