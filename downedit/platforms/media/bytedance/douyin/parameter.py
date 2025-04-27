import re
import time

from downedit.platforms.media.bytedance.verifyfp import VerifyFp
from downedit.service import Fingerprint


class DouyinParam:
    """
    Douyin parameter configuration.
    """
    __browser_into = {}

    def __init__(self):
        pass

    @classmethod
    def get_browser_into(
        cls,
        user_agent: str,
    ) -> dict:
        """
        Get the browser parameters.
        """
        if not cls.__browser_into or cls.__browser_into.get("userAgent") != user_agent:
            cls.__browser_into = Fingerprint.browser(
                browser_type="Chrome",
                user_agent=user_agent
            )
        return cls.__browser_into

    @classmethod
    def get_video_list(
        cls,
        sec_uid: str,
        max_cursor: int,
        count: int,
        cookie_str: str,
        user_agent: str,
    ) -> dict:
        """
        Get the parameters for the item list request.
        """
        timestamp = int(time.time())
        browser_type = "Chrome"

        if not cls.__browser_into or cls.__browser_into.get("userAgent") != user_agent:
            cls.__browser_into = Fingerprint.browser(
                browser_type=browser_type,
                user_agent=user_agent
            )

            cpu_core_match = re.search(r'device_web_cpu_core=(\d+)', cookie_str)
            memory_size_match = re.search(r'device_web_memory_size=(\d+)', cookie_str)
            width_match = re.search(r'dy_swidth=(\d+)', cookie_str)
            height_match = re.search(r'dy_sheight=(\d+)', cookie_str)

            if int(cpu_core_match.group(1)):
                cls.__browser_into["hardwareConcurrency"] = int(cpu_core_match.group(1))
            if int(memory_size_match.group(1)):
                cls.__browser_into["deviceMemory"] = int(memory_size_match.group(1))
            if int(width_match.group(1)):
                cls.__browser_into["width"] = int(width_match.group(1))
            if int(height_match.group(1)):
                cls.__browser_into["height"] = int(height_match.group(1))

        return {
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
            "sec_user_id": sec_uid,
            "max_cursor": max_cursor or 0,
            "locate_item_id": "",
            "locate_query": False,
            "show_live_replay_strategy": 1,
            "need_time_list": 1,
            "time_list_query": 0,
            "whale_cut_token": "",
            "cut_version": 1,
            "count": count or 18,
            "publish_video_strategy_type": 2,
            "from_user_page": 1,
            "update_version_code": 170400,
            "pc_client_type": 1,
            "pc_libra_divert": "Windows",
            "support_h265": 1,
            "support_dash": 1,
            "version_code": 290100,
            "version_name": "29.1.0",
            "cookie_enabled": True,
            "screen_height": cls.__browser_into.get("height"),
            "screen_width": cls.__browser_into.get("width"),
            "browser_language": "en-US",
            "browser_platform": cls.__browser_into.get("platform"),
            "browser_name": cls.__browser_into.get("browserName"),
            "browser_version": cls.__browser_into.get("browserVersion"),
            "browser_online": True,
            "engine_name": "Blink",
            "engine_version": cls.__browser_into.get("browserVersion"),
            "os_name": cls.__browser_into.get("osName"),
            "os_version": cls.__browser_into.get("osVersion"),
            "cpu_core_num": cls.__browser_into.get("hardwareConcurrency"),
            "device_memory": cls.__browser_into.get("deviceMemory"),
            "platform": cls.__browser_into.get("deviceType"),
            "downlink": 1.35,
            "effective_type": "4g",
            "round_trip_time": 850,
            # "webid": 7497652773367465472,
            "uifid": "",
            "verifyFp": VerifyFp.get_verify_fp(timestamp),
            # "fp": VerifyFp.get_verify_fp(timestamp),
            "msToken": "",
            # "a_bogus": ""
        }
