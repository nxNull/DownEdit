import json
import re
import urllib.parse, json, re


def extract_username(url: str) -> str:
    """
    Extracts the username from the Douyin URL.
    """
    match = re.search(r"/user/([^?]+)", url)

    if match:
        return match.group(1)
    else:
        raise ValueError("Username not found in the URL")


def extract_uifid(cookie_string: str) -> str:
    """
    Extracts the UIFID from the cookie string.
    """
    match = re.search(r"UIFID=([^;]+)", cookie_string)
    uifid = match.group(1) if match else None
    return uifid


def extract_cookie_param(cookie_str):
    """
    Extracts the stream recommendation feed parameters from the cookie string.
    """
    match = re.search(r'stream_recommend_feed_params=([^;]+)', cookie_str)
    if match:
        val = urllib.parse.unquote(urllib.parse.unquote(match.group(1))).strip('"')
        val = val.encode('utf-8').decode('unicode_escape')
        try:
            return json.loads(val)
        except json.JSONDecodeError as e:
            return {}
    return {}