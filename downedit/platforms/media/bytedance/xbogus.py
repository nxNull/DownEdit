import json
import time
import base64
import hashlib

import urllib.parse

from downedit.service.fingerprint import Fingerprint
from downedit.service.serialization import format_mm_version
from downedit.service.user_agents import UserAgent

__all__ = ["XBogus"]

class XBogus:
    """
    A class to generate the X-Bogus value for a given URL path.
    """
    def __init__(self, user_agent: str = "") -> None:
        self.Array = [None for _ in range(48)] + list(range(10)) + [None for _ in range(39)] + list(range(10, 16))
        self.character = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
        self.user_agent = (
            user_agent
            if user_agent is not None and user_agent != ""
            else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

    def md5_str_to_array(self, md5_str):
        """
        Convert a string to an array of integers using the md5 hashing algorithm.
        """
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]
        else:
            array = []
            idx = 0
            while idx < len(md5_str):
                array.append(
                    (self.Array[ord(md5_str[idx])] << 4)
                    | self.Array[ord(md5_str[idx + 1])]
                )
                idx += 2
            return array

    def md5_encrypt(self, url_params):
        """
        Encrypt the URL path using multiple rounds of md5 hashing.
        """
        hashed_url_params = self.md5_str_to_array(
            self.md5(self.md5_str_to_array(self.md5(url_params)))
        )
        return hashed_url_params

    def md5(self, input_data):
        """
        Calculate the md5 hash value of the input data.
        """
        if isinstance(input_data, str):
            array = self.md5_str_to_array(input_data)
        elif isinstance(input_data, list):
            array = input_data
        else:
            raise ValueError("Invalid input type. Expected str or list.")

        md5_hash = hashlib.md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    def encoding_conversion(
        self, a, b, c, e, d, t, f, r, n, o, i, _, x, u, s, l, v, h, p
    ):
        """
        Perform encoding conversion.
        """
        y = [a]
        y.append(int(i))
        y.extend([b, _, c, x, e, u, d, s, t, l, f, v, r, h, n, p, o])
        re = bytes(y).decode("ISO-8859-1")
        return re

    def encoding_conversion2(self, a, b, c):
        """
        Perform an encoding conversion on the given input values and return the result.
        """
        return chr(a) + chr(b) + c

    def rc4_encrypt(self, key, data):
        """
        Encrypt data using the RC4 algorithm.
        """
        S = list(range(256))
        j = 0
        encrypted_data = bytearray()

        # Initialize the S box
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        # Generate the ciphertext
        i = j = 0
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            encrypted_byte = byte ^ S[(S[i] + S[j]) % 256]
            encrypted_data.append(encrypted_byte)

        return encrypted_data

    def calculation(self, a1, a2, a3):
        """
        Perform a calculation using bitwise operations on the given input values and return the result.
        """
        x1 = (a1 & 255) << 16
        x2 = (a2 & 255) << 8
        x3 = x1 | x2 | a3
        return (
            self.character[(x3 & 16515072) >> 18]
            + self.character[(x3 & 258048) >> 12]
            + self.character[(x3 & 4032) >> 6]
            + self.character[x3 & 63]
        )

    def getXBogus(self, url_params):
        """
        Get the X-Bogus value.
        """

        array1 = self.md5_str_to_array(
            self.md5(
                base64.b64encode(
                    self.rc4_encrypt(b"\x00\x01\x0c", self.user_agent.encode("ISO-8859-1"))
                ).decode("ISO-8859-1")
            )
        )

        array2 = self.md5_str_to_array(
            self.md5(self.md5_str_to_array("d41d8cd98f00b204e9800998ecf8427e"))
        )
        url_params_array = self.md5_encrypt(url_params)

        timer = int(time.time())
        ct = 536919696
        array3 = []
        array4 = []
        xb_ = ""

        new_array = [
            64, 0.00390625, 1, 12,
            url_params_array[14], url_params_array[15], array2[14], array2[15], array1[14], array1[15],
            timer >> 24 & 255, timer >> 16 & 255, timer >> 8 & 255, timer & 255,
            ct >> 24 & 255, ct >> 16 & 255, ct >> 8 & 255, ct & 255
        ]

        xor_result = new_array[0]
        for i in range(1, len(new_array)):
            b = new_array[i]
            if isinstance(b, float):
                b = int(b)
            xor_result ^= b

        new_array.append(xor_result)

        idx = 0
        while idx < len(new_array):
            array3.append(new_array[idx])
            try:
                array4.append(new_array[idx + 1])
            except IndexError:
                pass
            idx += 2

        merge_array = array3 + array4

        garbled_code = self.encoding_conversion2(
            2,
            255,
            self.rc4_encrypt(
                "ÿ".encode("ISO-8859-1"),
                self.encoding_conversion(*merge_array).encode("ISO-8859-1"),
            ).decode("ISO-8859-1"),
        )

        idx = 0
        while idx < len(garbled_code):
            xb_ += self.calculation(
                ord(garbled_code[idx]),
                ord(garbled_code[idx + 1]),
                ord(garbled_code[idx + 2]),
            )
            idx += 3
        self.params = "%s&X-Bogus=%s" % (url_params, xb_)
        self.xb = xb_
        return (self.params, self.xb, self.user_agent)

if __name__ == "__main__":
    platform_type, device_type, browser_type = "Desktop", "Windows", "Chrome"
    user_agent = UserAgent(platform_type=platform_type, device_type=device_type, browser_type=browser_type)
    browser_info = Fingerprint.browser(browser_type=browser_type, user_agent=user_agent)
    xb = XBogus(user_agent=user_agent)

    dy_url_param_dict = {}
    dy_url_param_dict["device_platform"] = "webapp"
    dy_url_param_dict["aid"] = 6383
    dy_url_param_dict["channel"] = "channel_pc_web"
    dy_url_param_dict["sec_user_id"] = "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
    dy_url_param_dict["max_cursor"] = 0
    dy_url_param_dict["locate_query"] = False
    dy_url_param_dict["show_live_replay_strategy"] = 1
    dy_url_param_dict["need_time_list"] = 1
    dy_url_param_dict["time_list_query"] = 0
    dy_url_param_dict["whale_cut_token"] = ""
    dy_url_param_dict["cut_version"] = 1
    dy_url_param_dict["count"] = 18
    dy_url_param_dict["publish_video_strategy_type"] = 2
    dy_url_param_dict["pc_client_type"] = 1
    dy_url_param_dict["version_code"] = 170400
    dy_url_param_dict["version_name"] = "17.4.0"
    dy_url_param_dict["cookie_enabled"] = True
    dy_url_param_dict["screen_width"] = browser_info.get("width")
    dy_url_param_dict["screen_height"] = browser_info.get("height")
    dy_url_param_dict["browser_language"] = "zh-CN"
    dy_url_param_dict["browser_platform"] = "Win32"
    dy_url_param_dict["browser_name"] = browser_type
    dy_url_param_dict["browser_version"] = format_mm_version(user_agent.browser_version)
    dy_url_param_dict["browser_online"] = True
    dy_url_param_dict["engine_name"] = "Blink"
    dy_url_param_dict["engine_version"] = format_mm_version(user_agent.browser_version)
    dy_url_param_dict["os_name"] = device_type
    dy_url_param_dict["os_version"] = "10"
    dy_url_param_dict["cpu_core_num"] = browser_info.get("hardwareConcurrency")
    dy_url_param_dict["device_memory"] = browser_info.get("deviceMemory")
    dy_url_param_dict["platform"] = "PC"
    dy_url_param_dict["downlink"] = 10
    dy_url_param_dict["effective_type"] = "4g"
    dy_url_param_dict["round_trip_time"] = 50
    dy_url_param_dict["webid"] = "7335414539335222835"
    dy_url_param_dict["msToken"] = "p9Y7fUBuq9DKvAuN27Peml6JbaMqG2ZcXfFiyDv1jcHrCN00uidYqUgSuLsKl1onC-E_n82m-aKKYE0QGEmxIWZx9iueQ6WLbvzPfqnMk4GBAlQIHcDzxb38FLXXQxAm"

    douying_params = urllib.parse.urlencode(dy_url_param_dict)
    dy_xbogus = xb.getXBogus(douying_params)

    tk_url_param_dict = {}
    tk_url_param_dict["WebIdLastTime"] = 1713796127
    tk_url_param_dict["abTestVersion"] = "[object Object]"
    tk_url_param_dict["aid"] = 1988
    tk_url_param_dict["appType"] = "t"
    tk_url_param_dict["app_language"] = "zh-Hans"
    tk_url_param_dict["app_name"] = "tiktok_web"
    tk_url_param_dict["browser_name"] = "Mozilla"
    tk_url_param_dict["browser_online"] = True
    tk_url_param_dict["browser_platform"] = "Win32"
    tk_url_param_dict["browser_version"] = "5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F123.0.0.0%20Safari%2F537.36"
    tk_url_param_dict["channel"] = "tiktok_web"
    tk_url_param_dict["device_id"] = "7360698239018452498"
    tk_url_param_dict["odinId"] = "7360698115047851026"
    tk_url_param_dict["region"] = "TW"
    tk_url_param_dict["tz_name"] = "Asia%2FHong_Kong"
    tk_url_param_dict["uniqueId"] = "rei_toy625"

    tiktok_params = urllib.parse.urlencode(tk_url_param_dict)
    tk_xbogus = xb.getXBogus(tiktok_params)

    print(json.dumps(dy_xbogus, indent=4))
    print(f"url: {dy_xbogus[0]}, xbogus:{dy_xbogus[1]}, ua: {dy_xbogus[2]}")
    print(json.dumps(dy_xbogus, indent=4))
    print(f"url: {tk_xbogus[0]}, xbogus:{tk_xbogus[1]}, ua: {tk_xbogus[2]}")
