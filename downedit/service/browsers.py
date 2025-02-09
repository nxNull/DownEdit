import random


class Chrome():
    """
    Google Chrome

    Description:
        The version of Chrome is based on the WebKit version. We have used the WebKit version to determine the minor version range.

    Reference:
        https://chromereleases.googleblog.com/search/label/Stable%20updates
    """
    def __init__(self):
        pass

    def user_agents(self) -> dict:
        return {
            "windows": [
                'Mozilla/5.0 (Windows NT {windows}; Win64; x64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}',
                'Mozilla/5.0 (Windows NT {windows}; WOW64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}'
            ],
            "linux": [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}',
            ],
            "macos":[
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}'
            ],
            "android": [
                'Mozilla/5.0 (Linux; Android {android}{model}{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Mobile Safari/{webkit}'
            ],
            "ios": [
                'Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/{webkit} (KHTML, like Gecko) CriOS/{chrome} Mobile/15E148 Safari/{webkit}'
            ]
        }

    def get_versions(self):
        return  {
            '115.0.5790': {'minor_range': (0, 255), 'webkit': '537.36'},
            '116.0.5845': {'minor_range': (0, 255), 'webkit': '537.36'},
            '117.0.5938': {'minor_range': (0, 255), 'webkit': '537.36'},
            '118.0.5993': {'minor_range': (0, 255), 'webkit': '537.36'},
            '119.0.6045': {'minor_range': (0, 255), 'webkit': '537.36'},
            '120.0.6099': {'minor_range': (0, 255), 'webkit': '537.36'},
            '121.0.6167': {'minor_range': (0, 255), 'webkit': '537.36'},
            '122.0.6261': {'minor_range': (0, 255), 'webkit': '537.36'},
            '123.0.6312': {'minor_range': (0, 255), 'webkit': '537.36'},
            '124.0.6367': {'minor_range': (0, 255), 'webkit': '537.36'},
            '125.0.6422': {'minor_range': (0, 255), 'webkit': '537.36'},
            '126.0.6478': {'minor_range': (0, 255), 'webkit': '537.36'},
            '127.0.6533': {'minor_range': (0, 255), 'webkit': '537.36'},
            '128.0.6613': {'minor_range': (0, 255), 'webkit': '537.36'},
            '129.0.6668': {'minor_range': (0, 255), 'webkit': '537.36'},
            '130.0.6723': {'minor_range': (0, 255), 'webkit': '537.36'},
            '131.0.6778': {'minor_range': (0, 255), 'webkit': '537.36'},
            '132.0.6834': {'minor_range': (0, 255), 'webkit': '537.36'},
        }

class Firefox():
    """
    Mozilla Firefox

    description:
        The version of Firefox is based on the Gecko version. We have used the stable release version provided by Mozilla to determine the minor version range.

    Reference:
        https://www.mozilla.org/en-US/firefox/releases/
    """
    def __init__(self):
        pass

    def user_agents(self):
        return {
            "windows": [
                'Mozilla/5.0 (Windows NT {windows}; Win64; x64; rv:{firefox}) Gecko/20100101 Firefox/{firefox}',
                'Mozilla/5.0 (Windows NT {windows}; WOW64; rv:{firefox}) Gecko/20100101 Firefox/{firefox}',
            ],
            "linux": [
                'Mozilla/5.0 (X11; Linux x86_64; rv:{firefox}) Gecko/20100101 Firefox/{firefox}',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{firefox}) Gecko/20100101 Firefox/{firefox}',
            ],
            "macos": [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit}'
            ],
            "android": [
                'Mozilla/5.0 (Android {android}; Mobile; rv:{firefox}) Gecko/{firefox} Firefox/{firefox}'
            ],
            "ios": [
                'Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{firefox} Mobile/15E148 Safari/605.1.15'
            ]
        }

    def get_versions(self):
        return {
            '115.0': {'minor_range': (0, 3)},
            '115.1': {'minor_range': (0, 0)},
            '115.2': {'minor_range': (0, 1)},
            '115.3': {'minor_range': (0, 1)},
            '115.4': {'minor_range': (0, 0)},
            '115.5': {'minor_range': (0, 0)},
            '115.6': {'minor_range': (0, 0)},
            '115.7': {'minor_range': (0, 0)},
            '115.8': {'minor_range': (0, 0)},
            '116.0': {'minor_range': (0, 3)},
            '117.0': {'minor_range': (0, 1)},
            '118.0': {'minor_range': (0, 2)},
            '119.0': {'minor_range': (0, 1)},
            '120.0': {'minor_range': (0, 1)},
            '121.0': {'minor_range': (0, 1)},
            '122.0': {'minor_range': (0, 1)},
            '123.0': {'minor_range': (0, 1)},
            '124.0': {'minor_range': (0, 2)},
            '125.0': {'minor_range': (1, 3)},
            '126.0': {'minor_range': (0, 0)},
            '127.0': {'minor_range': (0, 2)},
            '128.0': {'minor_range': (0, 1)},
            '129.0': {'minor_range': (0, 0)},
            '130.0': {'minor_range': (0, 1)},
            '131.0': {'minor_range': (0, 3)},
            '132.0': {'minor_range': (0, 2)},
            '133.0': {'minor_range': (3, 3)},
        }

class Edge():
    """
    Microsoft Edge

    description:
        The version of Edge is based on the WebKit version. We have used the WebKit version to determine the minor version range.

    Reference:
        https://docs.microsoft.com/en-us/deployedge/microsoft-edge-release-schedule
    """
    def __init__(self):
        pass

    def user_agents(self):
        return {
            "windows": [
                'Mozilla/5.0 (Windows NT {windows}; Win64; x64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit} Edg/{chrome}',
            ],
            "linux": [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit} Edg/{chrome}',
            ],
            "macos": [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit} (KHTML, like Gecko) Chrome/{chrome} Safari/{webkit} Edg/{chrome}'
            ],
            "android": [
                'Mozilla/5.0 (Linux; Android {android}{model}{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Mobile Safari/{webkit} EdgA/{chrome}'
            ],
            "ios": [
                'Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/{webkit} (KHTML, like Gecko) Version/15.0 EdgiOS/{chrome} Mobile/15E148 Safari/{webkit}'
            ]
        }

    def get_versions(self):
        return {
            '115.0.1901': {'minor_range': (0, 99), 'webkit': '537.36'},
            '116.0.1938': {'minor_range': (0, 99), 'webkit': '537.36'},
            '117.0.2045': {'minor_range': (0, 99), 'webkit': '537.36'},
            '118.0.2088': {'minor_range': (0, 99), 'webkit': '537.36'},
            '119.0.2151': {'minor_range': (0, 99), 'webkit': '537.36'},
            '120.0.2210': {'minor_range': (0, 99), 'webkit': '537.36'},
            '121.0.2277': {'minor_range': (0, 99), 'webkit': '537.36'},
            '122.0.2365': {'minor_range': (0, 99), 'webkit': '537.36'},
            '123.0.2420': {'minor_range': (0, 99), 'webkit': '537.36'},
            '124.0.2478': {'minor_range': (0, 99), 'webkit': '537.36'},
            '125.0.2535': {'minor_range': (0, 99), 'webkit': '537.36'},
            '126.0.2592': {'minor_range': (0, 99), 'webkit': '537.36'},
            '127.0.2651': {'minor_range': (0, 99), 'webkit': '537.36'},
            '128.0.2739': {'minor_range': (0, 99), 'webkit': '537.36'},
            '129.0.2792': {'minor_range': (0, 99), 'webkit': '537.36'},
            '130.0.2849': {'minor_range': (0, 99), 'webkit': '537.36'},
            '131.0.2903': {'minor_range': (0, 99), 'webkit': '537.36'},
        }

class Safari():
    """
    Apple Safari

    description:
        The version of Safari is based on the WebKit version. We have used the WebKit version to determine the minor version range.

    Reference:
        https://developer.apple.com/documentation/safari-release-notes
    """
    def __init__(self):
        pass

    def user_agents(self):
        return {
            'macos': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit} (KHTML, like Gecko) Version/{safari} Safari/{webkit}'
            ],
            "ios": [
                'Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/{webkit} (KHTML, like Gecko) Version/{safari} Mobile/15E148 Safari/{webkit}'
            ]
        }

    def get_versions(self):
        return {
            '15': {'minor_range': (0, 6), 'webkit': '605.1.15'},
            '16': {'minor_range': (0, 6), 'webkit': '605.1.15'},
            '17': {'minor_range': (0, 6), 'webkit': '605.1.15'},
            '18': {'minor_range': (0, 2), 'webkit': '605.1.15'},
        }

class Browser():
    """
    Browser class for generating user agents and versions for different browsers.

    Args:
        browser (str): The name of the browser to use. (Chrome, Firefox, Edge, Safari). Defaults to "chrome".

    Example:
    >>> browser = Browser("chrome")
    >>> browser.get_version()
    {'major': '100', 'minor': 23, 'webkit': '537.36'}
    """
    def __init__(self, browser="chrome"):
        self.browser_name = browser.lower()
        self.browser = self._initialize_browser()

    def _initialize_browser(self):
        """
        Initializes the Browser instance with a specific browser.

        Args:
            browser (str): The name of the browser to use. Defaults to "chrome".
        """
        browser_classes = {}
        browser_classes["chrome"] = Chrome()
        browser_classes["firefox"] = Firefox()
        browser_classes["edge"] = Edge()
        browser_classes["safari"] = Safari()

        return browser_classes.get(self.browser_name, Chrome())

    def get_user_agents(self):
        """
        Retrieves the user agents for the browser.

        Returns:
            tuple: A tuple containing the user agents for the browser.
        """
        return self.browser.user_agents()

    def get_version(self):
        """
        Retrieves a random version from the browser's version set.

        Returns:
            dict: A dictionary containing the major version, minor version,
                    and possibly webkit version if available.
        """
        versions = self.browser.get_versions()
        major_version = random.choice(list(versions.keys()))
        properties = versions[major_version]

        __version = {}
        if major_version:
            __version["major"] = major_version
        if "minor_range" in properties:
            __version["minor"] = random.randint(*map(int, properties['minor_range']))
        if "webkit" in properties:
            __version["webkit"] = properties['webkit']
        return __version