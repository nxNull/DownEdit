from downedit.platforms.media.bytedance.abogus import DouyinAbogus
from downedit.service import retry_async, httpx_capture_async
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    log
)


class DouyinClient:
    """
    Douyin client configuration.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.user_agent = UserAgent(
            platform_type="desktop",
            device_type="windows",
            browser_type="chrome"
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-full-version-list,
            sec-ch-ua-platform,
            sec-ch-ua-platform-version,
            sec-ch-ua-mobile,
            sec-ch-ua-bitness,
            sec-ch-ua-arch,
            sec-ch-ua-model,
            sec-ch-ua-wow64
        """)
        self.default_client = Client(headers=self.headers.get())
        self.client: Client = kwargs.get("client", self.default_client)

    def get_abogus(self, param_string, browser_info) -> str:
        """
        Generates the xbogus value for the given parameters.
        """
        fingerprint = (
            f"{browser_info.get("width")}|{browser_info.get("height")}|{browser_info.get("outerWidth")}|{browser_info.get("outerHeight")}|"
            f"{browser_info.get("availLeft")}|{browser_info.get("availTop")}|0|0|{browser_info.get("availWidth")}|{browser_info.get("availHeight")}|"
            f"{browser_info.get("availTop")}|{browser_info.get("availWidth")}|{browser_info.get("width")}|{browser_info.get("height")}|24|24|{browser_info.get("platform")}"
        )

        param_string += f"&a_bogus={DouyinAbogus.get_a_bogus(
            url_params=param_string,
            fingerprint=fingerprint,
            user_agent=self.client.headers.get(
                "User-Agent",
                self.client.headers.get("user-agent", "")
            )
        )}"

        return param_string
