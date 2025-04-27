from downedit.platforms.domain import Domain
from downedit.platforms.media.kuaishou.hash import KuaiShouHash
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


class KuaiShouClient:
    """
    KuaiShou client configuration.
    """

    def __init__(self, client: Client = None):
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
        self.client = client or self.default_client
        self.kuai_shou_hash = KuaiShouHash()

    def get_client_details(self, input_cookie: str):
        """
        Generates KuaiShou client details.

        Returns:
            dict: A dictionary containing client details.
        """
        cookies = {
            "kpf": "PC_WEB",
            "clientid": "3",
            "kpn": "KUAISHOU_VISION"
        }

        if input_cookie:
            if 'did=' in input_cookie:
                did_value = input_cookie.split('did=')[-1].strip().split(';')[0]
                cookies["did"] = did_value.strip().replace("'", "")
            else:
                raise ValueError("The 'did' value is missing in the input cookie.")
        else:
            raise ValueError("Input cookie is missing.")

        cookie_str = f"kpf={cookies['kpf']}; clientid={cookies['clientid']}; did={cookies['did']}; kpn={cookies['kpn']}"
        return cookie_str
