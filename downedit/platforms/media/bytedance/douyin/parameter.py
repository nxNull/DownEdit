import re
import time

from downedit.platforms.media.bytedance.douyin.extractor import extract_cookie_param
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

        browser_info_match = extract_cookie_param(cookie_str)

        if browser_info_match:
            cls.__browser_into["hardwareConcurrency"] = browser_info_match.get(
                "cpu_core_num",
                cls.__browser_into.get("hardwareConcurrency", "")
            )
            cls.__browser_into["deviceMemory"] = browser_info_match.get(
                "device_memory",
                cls.__browser_into.get("deviceMemory", "")
            )
            cls.__browser_into["width"] = browser_info_match.get(
                "screen_width",
                cls.__browser_into.get("width", "")
            )
            cls.__browser_into["height"] = browser_info_match.get(
                "screen_height",
                cls.__browser_into.get("height", "")
            )

        return {
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
            "sec_user_id": sec_uid,
            "max_cursor": max_cursor or 0,
            "locate_query": "false",
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
            "cookie_enabled": "true",
            "screen_width": cls.__browser_into.get("width", 1920),
            "screen_height": cls.__browser_into.get("height", 1080),
            "browser_language": "en-US",
            "browser_platform": cls.__browser_into.get("platform"),
            "browser_name": cls.__browser_into.get("browserName"),
            "browser_version": cls.__browser_into.get("browserVersion"),
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": cls.__browser_into.get("browserVersion"),
            "os_name": cls.__browser_into.get("osName"),
            "os_version": "10",
            "cpu_core_num": cls.__browser_into.get("hardwareConcurrency", 8),
            "device_memory": cls.__browser_into.get("deviceMemory", 16),
            "platform": cls.__browser_into.get("deviceType"),
            "downlink": browser_info_match.get("downlink", 10),
            "effective_type": browser_info_match.get("effective_type", "4g"),
            "round_trip_time": browser_info_match.get("round_trip_time", 250),
            # "webid": 7497652773367465472,
            "uifid": "",
            # "verifyFp": VerifyFp.get_verify_fp(timestamp),
            # "fp": VerifyFp.get_verify_fp(timestamp),
            "msToken": "",
            # "a_bogus": ""
        }
