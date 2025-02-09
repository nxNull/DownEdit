import random
from typing import Tuple, Union

from downedit.utils import Singleton
from .browsers import Browser
from .platforms import Platform
from .serialization import format_mm_version


class UserAgent():
    """
    User agent configuration.

    Args:
        platform_type (str, optional): The platform type. Defaults to "desktop".
        device_type (str, optional): The device type. Defaults to "windows".
        browser_type (str, optional): The browser type. Defaults to "chrome".

    Attributes:
        platform_type (str): The platform type.
        browser_type (str): The browser type.
        device_type (str): The device type.
        browser (Browser): The browser instance.
        platform (Platform): The platform instance.
        generated (str): The generated user agent string.
        platform_version (dict): The platform version.
        browser_version (dict): The browser version.

    Examples:
    >>> user_agent = UserAgent()
    >>> print(user_agent)
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4664.45 Safari/537.36
    """
    def __init__(
        self,
        platform_type="desktop",
        device_type="windows",
        browser_type="chrome"
    ):
        self.platform_type = platform_type.lower()
        self.device_type = device_type.lower()
        self.browser_type = browser_type.lower()

        self.browser = Browser(self.browser_type)
        self.platform = Platform(self.platform_type, self.device_type)

        self.generated = self.__generate()

        self.platform_version: dict
        self.browser_version: dict

    def __generate(self) -> str:
        """
        Generate a user agent string based on the platform, device, and browser types.

        Returns:
            str: A user agent string.
        """
        self.platform_version = self.platform.get_version()
        self.browser_version = self.browser.get_version()

        browser_ua = self.browser.get_user_agents()
        browser_template = random.choice(
            browser_ua.get(str(self.device_type), [])
        )

        replacements = {}
        replacements["{windows}"] = self.platform_version.get("major", "")
        replacements["{webkit}"] = self.browser_version.get("webkit", "")
        replacements["{chrome}"] = format_mm_version(self.browser_version)
        replacements["{edge}"] = format_mm_version(self.browser_version)
        replacements["{firefox}"] = format_mm_version(self.browser_version, strip_zero=True)
        replacements["{linux}"] = self.platform_version.get("major", "")
        replacements["{android}"] = self.platform_version.get("major", "").replace(".0", "")
        replacements["{model}"] = f"; {self.platform_version.get('platform_model', '')}"
        replacements["{build}"] = f"; Build/{self.platform_version.get('build_number', '')}"
        replacements["{ios}"] = format_mm_version(self.platform_version, strip_zero=True).replace(".", "_")
        replacements["{safari}"] = format_mm_version(self.browser_version)

        for key, value in replacements.items():
            browser_template = browser_template.replace(key, str(value))

        # Remove any remaining placeholders (e.g., if model/build not found)
        browser_template = browser_template.replace('{build}', '').replace('{model}', '')

        return browser_template

    def __str__(self) -> str:
        return self.generated