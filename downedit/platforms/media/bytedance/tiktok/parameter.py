import time

from downedit.platforms.media.bytedance.verifyfp import VerifyFp
from downedit.service import Fingerprint


class TikTokParam:
    """
    TikTok parameter configuration.
    """
    __browser_into = {}

    def __init__(self):
        pass

    @classmethod
    def get_video_list(
        cls,
        sec_uid: str,
        cursor: int,
        count: int,
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
            cls.__browser_into["userAgent"].replace(
                "Mozilla/5.0", "5.0"
            )

        return {
            "WebIdLastTime": timestamp,
            "aid": 1988,
            "app_language": 'en',
            "app_name": 'tiktok_web',
            "browser_language": 'en-US',
            "browser_name": browser_type,
            "browser_online": True,
            "browser_platform": cls.__browser_into.get("platform"),
            "browser_version": cls.__browser_into.get("userAgent"),
            "channel": 'tiktok_web',
            "cookie_enabled": True,
            "count": count or 35,
            "coverFormat": 2,
            "cursor": cursor or 0,
            "data_collection_enabled": "true",
            "device_id": "",
            "device_platform": "web_pc",
            "focus_state": "true",
            "from_page": "user",
            "history_len": 9,
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "language": "en",
            "needPinnedItemIds": "true",
            # "odinId": 7485043939747021832,
            "os": "windows",
            "post_item_list_request_type": 0,
            "priority_region": "",
            "referer": "",
            "region": "KH",
            "root_referer": "",
            "screen_height": cls.__browser_into.get("height"),
            "screen_width": cls.__browser_into.get("width"),
            "secUid": sec_uid,
            "tz_name": "Asia/Bangkok",
            "user_is_login": "False",
            "verifyFp": VerifyFp.get_verify_fp(timestamp),
            "webcast_language": "en",
            "msToken": "",
            "X-Bogus": "",
            "X-Gnarly": ""
        }
