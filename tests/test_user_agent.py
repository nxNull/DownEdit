import unittest
from unittest.mock import (
    MagicMock,
    patch
)

import os
import sys


__parent_dir = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            __file__
            )
        )
    )

if __parent_dir not in sys.path:
    sys.path.insert(
        0,
        __parent_dir
    )


from downedit.service.user_agents import UserAgent, format_mm_version
from downedit.service.platforms import Platform, Android, IOS, macOS, Linux, Windows, Mobile, Desktop
from downedit.service.user_agents import UserAgent
from downedit.service.platforms import Platform
from downedit.service.browsers import Browser, Chrome, Edge, Firefox, Safari

class TestUserAgent(unittest.TestCase):
    @patch("downedit.service.user_agents.random.choice", side_effect=lambda x: x[0] if x else None)
    @patch("downedit.service.platforms.random.choice", side_effect=lambda x: x[0] if x else None)
    @patch("downedit.service.browsers.random.choice", side_effect=lambda x: x[0] if x else None)
    def setUp(self, mock_browser_choice, mock_platform_choice, mock_ua_choice):
        self.mock_browser_choice = mock_browser_choice
        self.mock_platform_choice = mock_platform_choice
        self.mock_ua_choice = mock_ua_choice

    def test_user_agent_generation(self):
        combinations = [
            ("desktop", "windows", "chrome"),
            ("desktop", "windows", "edge"),
            ("desktop", "windows", "firefox"),
            ("desktop", "linux", "chrome"),
            ("desktop", "linux", "edge"),
            ("desktop", "linux", "firefox"),
            ("mobile", "android", "chrome"),
            ("mobile", "android", "edge"),
            ("mobile", "android", "firefox"),
            ("desktop", "macos", "chrome"),
            ("desktop", "macos", "edge"),
            ("desktop", "macos", "safari"),
            ("desktop", "macos", "firefox"),
            ("mobile", "ios", "chrome"),
            ("mobile", "ios", "edge"),
            ("mobile", "ios", "safari"),
            ("mobile", "ios", "firefox"),
        ]

        for platform_type, device_type, browser_type in combinations:
            user_agent = UserAgent(platform_type, device_type, browser_type)
            generated_ua = user_agent.generated
            self.assertIsInstance(generated_ua, str)
            self.assertGreater(len(generated_ua), 0)

            if browser_type == "chrome" and platform_type == "desktop":
                self.assertIn("Chrome", generated_ua)
            elif browser_type == "firefox":
                if platform_type == "desktop" and device_type == "macos":
                    self.assertIn("Chrome", generated_ua)
                    self.assertNotIn("Firefox", generated_ua)
                    self.assertIn("Safari", generated_ua)

            elif browser_type == "edge":
                self.assertIn("Edg", generated_ua)
            elif browser_type == "safari":
                if platform_type == "desktop" and device_type == "macos":
                    self.assertIn("Safari", generated_ua)
                    self.assertNotIn("Chrome", generated_ua)
                    self.assertNotIn("Firefox", generated_ua)
                else:
                    self.assertIn("Safari", generated_ua)


    def test_format_mm_version(self):
        self.assertEqual(format_mm_version({"major": "100", "minor": 0}, strip_zero=False), "100.0")
        self.assertEqual(format_mm_version({"major": "100", "minor": 23}), "100.23")
        self.assertEqual(format_mm_version({"major": "100", "minor": 0}, strip_zero=True), "100")
        self.assertEqual(format_mm_version({"major": "14", "minor": 5}, strip_zero=True), "14.5")


    @patch.object(Mobile, "get_types")
    @patch.object(Desktop, "get_types")
    def test_platform_initialization(self, mock_desktop_types, mock_mobile_types):
        mock_desktop_types.return_value = {"windows": "mock_windows"}
        mock_mobile_types.return_value = {"android": "mock_android"}

        platform_desktop = Platform("desktop", "windows")
        self.assertEqual(platform_desktop.os.get_types(),  {"windows": "mock_windows"})

        platform_mobile = Platform("mobile", "android")
        self.assertEqual(platform_mobile.os.get_types(), {"android": "mock_android"})

if __name__ == '__main__':


    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="chrome")
    print("----------------------------------")
    print("1: ",  id(user_agent))
    print("1: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="chrome")
    print("----------------------------------")
    print("1: ",  id(user_agent))
    print("1: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="edge")
    print("\n2: ", id(user_agent))
    print("2: ", user_agent)
    print("2: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="edge")
    print("\n2: ", id(user_agent))
    print("2: ", user_agent)
    print("2: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="firefox")
    print("\n3: ", id(user_agent))
    print("3: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="windows", browser_type="firefox")
    print("\n3: ", id(user_agent))
    print("3: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="chrome")
    print("\n4: ", id(user_agent))
    print("4: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="chrome")
    print("\n4: ", id(user_agent))
    print("4: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="edge")
    print("\n5: ", id(user_agent))
    print("5: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="edge")
    print("\n5: ", id(user_agent))
    print("5: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="firefox")
    print("\n6: ", id(user_agent))
    print("6: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="linux", browser_type="firefox")
    print("\n6: ", id(user_agent))
    print("6: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="chrome")
    print("\n7: ", id(user_agent))
    print("7: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="chrome")
    print("\n7: ", id(user_agent))
    print("7: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="edge")
    print("\n8 ID: ", id(user_agent))
    print("8: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="edge")
    print("\n8 ID: ", id(user_agent))
    print("8: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="firefox")
    print("\n9 ID: ", id(user_agent))
    print("9: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="android", browser_type="firefox")
    print("\n9 ID: ", id(user_agent))
    print("9: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="chrome")
    print("\n10 ID: ", id(user_agent))
    print("10: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="chrome")
    print("\n10 ID: ", id(user_agent))
    print("10: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="edge")
    print("\n11 ID: ", id(user_agent))
    print("11: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="edge")
    print("\n11 ID: ", id(user_agent))
    print("11: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="safari")
    print("\n12 ID: ", id(user_agent))
    print("12: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="safari")
    print("\n12 ID: ", id(user_agent))
    print("12: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="firefox")
    print("\n13 ID: ", id(user_agent))
    print("13: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop",
                           device_type="macos", browser_type="firefox")
    print("\n13 ID: ", id(user_agent))
    print("13: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="chrome")
    print("\n14 ID: ", id(user_agent))
    print("14: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="chrome")
    print("\n14 ID: ", id(user_agent))
    print("14: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="edge")
    print("\n15 ID: ", id(user_agent))
    print("15: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="edge")
    print("\n15 ID: ", id(user_agent))
    print("15: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="safari")
    print("\n16 ID: ", id(user_agent))
    print("16: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="safari")
    print("\n16 ID: ", id(user_agent))
    print("16: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="firefox")
    print("\n17 ID: ", id(user_agent))
    print("17: ", user_agent)
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile",
                           device_type="ios", browser_type="firefox")
    print("\n17 ID: ", id(user_agent))
    print("17: ", user_agent)
    print("----------------------------------")

    # Unit testing
    unittest.main()
