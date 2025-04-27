import re


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
