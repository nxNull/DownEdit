import re


def extract_channel_handle(url: str) -> str:
    """
    Extracts the @channel_handle from a YouTube URL.

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The extracted @handle, or None if not found.
    """
    match = re.search(
        r'(?:https?://)?(?:www\.)?youtube\.com/(@[\w\d_-]+)', url)
    if match:
        return match.group(1)
    return None


def extract_channel_url(url: str) -> str:
    """
    Extracts the channel URL from a YouTube URL.
    """
    pattern = r"^(https:\/\/www\.youtube\.com\/@[^\/\?]+)"

    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None
