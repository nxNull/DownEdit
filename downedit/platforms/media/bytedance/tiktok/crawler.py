

class TiktokCrawler:

    def __init__(self) -> None:
        pass

    async def get_secuid(self, url: str) -> str:
        """
        Get the secuid from the URL.

        Args:
            url (str): The URL to extract the secuid from.

        Returns:
            str: The secuid extracted from the URL.
        """
