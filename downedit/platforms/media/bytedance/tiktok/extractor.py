import json
import re

__all__ = [
    "extract_username",
    "extract_secuid",
    "extract_msToken",
    "extract_rehydration_data",
]


def extract_username(url: str) -> str:
    pattern = r"https://www\.tiktok\.com/@([a-zA-Z0-9._]+)"

    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        raise ValueError("Username not found in the URL")


def extract_secuid(string: str) -> str:
    """
    Extracts the secuid from the URL.
    """
    return re.compile('"secUid":"([a-zA-Z0-9_-]+)"').findall(string)[0]


def extract_msToken(string: str):
    """
    Extracts the msToken from the URL.
    """
    msTokenList = re.findall(r'msToken=([^;]+)', string)
    return msTokenList


def extract_rehydration_data(html_text):
    pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" [^>]*>\s*(\{.*?\})\s*</script>'
    match = re.search(pattern, html_text, re.DOTALL)
    if match:
        json_text = match.group(1)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse rehydration JSON.")
    else:
        raise ValueError("Could not find rehydration script in HTML.")
