import unittest

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


from downedit.service.platforms import (
    IOS,
    Android,
    Linux,
    Windows,
    macOS
)

class TestPlatforms(unittest.TestCase):

    def setUp(self):
        self.android = Android()
        self.ios = IOS()
        self.macos = macOS()
        self.linux = Linux()
        self.windows = Windows()

    def test_android_versions(self):
        versions = self.android.get_versions()
        print("Testing Android Versions")
        self.assertIn('8.0', versions)
        self.assertIn('10.0', versions)
        self.assertIn('14.0', versions)
        version_8_0 = versions['8.0']
        self.assertEqual(version_8_0['minor_range'], (0, 5))
        self.assertTrue(len(version_8_0['build_number']) > 0)
        print("Android Versions Test Passed")

    def test_android_models(self):
        models = self.android.get_models()
        print("Testing Android Models")
        self.assertIn('SM-G920A', models)
        self.assertIn('SM-G930A', models)
        self.assertNotIn('SM-G9999', models)
        print("Android Models Test Passed")

    def test_ios_versions(self):
        versions = self.ios.get_versions()
        print("Testing iOS Versions")
        self.assertIn('14.0', versions)
        self.assertIn('15.1', versions)
        self.assertIn('17.0', versions)
        ios_14_0 = versions['14.0']
        self.assertEqual(ios_14_0['minor_range'], (0, 1))
        print("iOS Versions Test Passed")

    def test_macos_versions(self):
        versions = self.macos.get_versions()
        print("Testing macOS Versions")
        self.assertIn('10.11', versions)
        self.assertIn('11.0', versions)
        self.assertIn('12.5', versions)
        macos_10_11 = versions['10.11']
        self.assertEqual(macos_10_11['minor_range'], (0, 6))
        print("macOS Versions Test Passed")

    def test_linux_versions(self):
        versions = self.linux.get_versions()
        print("Testing Linux Versions")
        self.assertIn('5.0', versions)
        self.assertIn('5.10', versions)
        self.assertIn('6.0', versions)
        linux_5_0 = versions['5.0']
        self.assertEqual(linux_5_0['minor_range'], (0, 21))
        print("Linux Versions Test Passed")
    
    def test_windows_versions(self):
        versions = self.windows.get_versions()
        print("Testing Windows Versions")
        self.assertIn('6.1', versions)
        self.assertIn('10.0', versions)
        self.assertNotIn('6.0', versions)
        windows_6_1 = versions['6.1']
        self.assertTrue(len(windows_6_1) == 0)
        print("Windows Versions Test Passed")
        

if __name__ == '__main__':
    unittest.main()