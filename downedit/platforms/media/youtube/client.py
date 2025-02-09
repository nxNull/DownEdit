import random
import string

class YoutubeIOS():
    """
    Youtube mobile client for iOS

    description:
        The Youtube client version and configuration is based on stable releases and the supported Apple devices.

    Reference:
        https://www.theyoutube.com/versions/
    """
    def __init__(self):
        pass

    def get_ios_versions(self):
        return ["19.29.1", "19.30.1", "19.31.1", "19.32.2", "19.33.1"]

    def get_ios_models(self):
        """
        Apple iPhone Models

        description:
            The list of Apple iPhone models that are supported by the service.

        Reference:
            https://everymac.com/systems/apple/iphone/
        """
        return ["iPhone16,2", "iPhone15,3", "iPhone14,4", "iPhone13,3"]

    def get_ios_os_versions(self):
        """
        iOS Versions

        description:
            The supported iOS versions for the Youtube client.

        Reference:
            https://ipsw.me/product/iPhone
        """
        return ["17.5.1.21F90", "17.6.1.21G90", "17.7.1.21H90", "17.8.1.21I90"]

class YoutubeClient:
    """
    Handles Youtube Client configuration.
    """
    def __init__(self):
        self.youtube = YoutubeIOS()

    def get_client_details(self):
        """
        Generates Youtube client details for iOS.

        Returns:
            dict: A dictionary containing client details.
        """
        client_version = random.choice(self.youtube.get_ios_versions())
        device_model = random.choice(self.youtube.get_ios_models())
        os_version = random.choice(self.youtube.get_ios_os_versions())

        details = {}
        details["clientName"] = "IOS"
        details["clientVersion"] = client_version
        details["deviceMake"] = "Apple"
        details["deviceModel"] = device_model
        details["hl"] = "en"
        details["osName"] = "iPhone"
        details["osVersion"] = os_version
        details["timeZone"] = "UTC"
        details["userAgent"] = f"com.google.ios.youtube/{client_version} ({device_model}; U; CPU iOS {os_version} like Mac OS X;)"
        details["gl"] = "US"
        details["utcOffsetMinutes"] = 0

        return details


    async def create_payload(self, video_id):
        """
        Creates the payload for Youtube API requests.

        Args:
            video_id (str): The video identifier.

        Returns:
            dict: A dictionary containing the request payload.
        """
        client_details = self.get_client_details()
        yt_payload = {}
        yt_payload["videoId"] = str(video_id)
        yt_payload["contentCheckOk"] = True
        yt_payload["context"] = {
            "client": client_details
        }

        return yt_payload

    async def create_headers(self, client_details):
        """
        Creates headers for Youtube API requests.

        Args:
            client_details (dict): The client details.

        Returns:
            dict: A dictionary containing the request headers.
        """
        headers = {}
        headers["User-Agent"] = client_details["userAgent"]

        return headers